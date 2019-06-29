import logging
import os
import re
import subprocess
import uuid


information_messages = [
	re.compile(r"^Loading GUID <-> Path mappings..."),
	re.compile(r"^Loading Asset Database..."),
	re.compile(r"^AssetDatabase consistency checks..."),
	re.compile(r"^Initialize engine version: "),
	re.compile(r"^- Starting compile "),
	re.compile(r"^- Finished compile "),
	re.compile(r"^Load scene 'Assets/"),
	re.compile(r"^Complete build size "),
	re.compile(r"^Exiting batchmode "),
	re.compile(r"^\[ScriptCompilation\]"),
]


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	return subparsers.add_parser("editor", help = "launch the editor")


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	launch_editor(environment["unity_2019_executable"], configuration["unity_project_path"], arguments.simulate)


def launch_editor(unity_executable, unity_project_path, simulate):
	logging.info("Launching the editor")

	unity_command = [ unity_executable, "-projectPath", unity_project_path ]

	logging.info("+ %s", " ".join(("'" + x + "'") if " " in x else x for x in unity_command))
	if not simulate:
		subprocess.Popen(unity_command)


def run_editor_command(unity_executable, unity_project_path, command, command_arguments, simulate):
	log_file_path = os.path.join(".logs", "%s_%s.log" % (command, str(uuid.uuid4())))

	unity_command = [ unity_executable, "-projectPath", unity_project_path ]
	unity_command += [ "-batchMode", "-noGraphics", "-quit", "-logFile", "-" ]
	unity_command += [ "-executeMethod", "Overmind.Solitaire.UnityClient.Editor.EditorCommand." + command ]

	if command_arguments:
		unity_command += [ "-executeMethodArguments" ] + [ key + "=" + value for key, value in command_arguments.items() ]

	logging.info("+ %s", " ".join(("'" + x + "'") if " " in x else x for x in unity_command))
	print("")

	if not simulate:
		os.makedirs(os.path.dirname(log_file_path), exist_ok = True)

		with open(log_file_path, "w") as log_file:
			log_file.write("# Workspace: '%s'\n" % os.getcwd())
			log_file.write("# Command: %s\n" % " ".join(("'" + x + "'") if " " in x else x for x in unity_command))
			log_file.write("\n")

			process = subprocess.Popen(unity_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)

			for line in process.stdout:
				line = line.rstrip()
				_log_unity_output(line)

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

	if line.startswith("ERROR: "):
		logging.error(line[len("ERROR: "):])
	elif line.startswith("WARNING: "):
		logging.warning(line[len("WARNING: "):])
	elif _match_message(line, information_messages) is not None:
		logging.info(line)
	else:
		logging.debug(line)
