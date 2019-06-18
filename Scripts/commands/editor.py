import logging
import subprocess


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
