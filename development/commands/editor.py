import logging
import re
import subprocess


logger = logging.getLogger("Main")


information_messages = [
	re.compile(r"^Loading GUID <-> Path mappings\.\.\."),
	re.compile(r"^Loading Asset Database\.\.\."),
	re.compile(r"^AssetDatabase consistency checks\.\.\."),
	re.compile(r"^Initialize engine version: "),
	re.compile(r"^Load scene 'Assets/"),
	re.compile(r"^Complete build size "),
	re.compile(r"^Exiting batchmode "),
	re.compile(r"^\[ScriptCompilation\]"),
	re.compile(r"^\[PackageBuilder\]"),
	re.compile(r"^Exiting "),
]

warning_messages = [
	re.compile(r"^WARNING: "),
	re.compile(r"warning CS[0-9]+: "),
]

error_messages = [
	re.compile(r"^ERROR: "),
	re.compile(r"^[a-zA-Z0-9_]*Exception: "),
	re.compile(r"error CS[0-9]+:"),
	re.compile(r"^Aborting batchmode due to failure:"),
	re.compile(r"^executeMethod method [a-zA-Z0-9_\.]+ threw exception\."),
	re.compile(r"'[a-zA-Z0-9_\-\./\\]*' is an incorrect path for a scene file\."),
]


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	return subparsers.add_parser("editor", help = "launch the editor")


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	launch_editor(environment["unity_executable"], configuration["unity_project_path"], simulate = arguments.simulate)


def launch_editor(unity_executable, unity_project_path, simulate):
	logger.info("Launching editor for '%s'", unity_project_path)

	unity_command = [ unity_executable, "-projectPath", unity_project_path ]

	logger.info("+ %s", " ".join(("'" + x + "'") if " " in x else x for x in unity_command))
	if not simulate:
		subprocess.Popen(unity_command)


def run_editor_command(unity_executable, unity_project_path, command, command_arguments, simulate):
	unity_command = [ unity_executable, "-projectPath", unity_project_path ]
	unity_command += [ "-batchMode", "-noGraphics", "-quit", "-logFile", "-" ]

	if command:
		unity_command += [ "-executeMethod", "Overmind.Solitaire.UnityClient.Editor.EditorCommand." + command ]
	if command_arguments:
		unity_command += [ "-executeMethodArguments" ] + [ key + "=" + value for key, value in command_arguments.items() ]

	logger.info("+ %s", " ".join(("'" + x + "'") if " " in x else x for x in unity_command))
	print("")

	if not simulate:
		process = subprocess.Popen(unity_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)

		for line in process.stdout:
			line = line.rstrip()
			_log_unity_output(line)

		print("")

		result = process.wait()
		if result != 0:
			raise RuntimeError("Unity editor command '%s' failed" % command)


def _log_unity_output(line):

	def _match_message(line, message_regex_collection):
		for message_regex in message_regex_collection:
			match = re.search(message_regex, line)
			if match:
				return match
		return None

	if _match_message(line, error_messages) is not None:
		logger.error(line)
	elif _match_message(line, warning_messages) is not None:
		logger.warning(line)
	elif _match_message(line, information_messages) is not None:
		logger.info(line)
	else:
		logger.debug(line)
