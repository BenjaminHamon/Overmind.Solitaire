import logging

import development.commands.editor


logger = logging.getLogger("Main")


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	return subparsers.add_parser("reimport", help = "reimport all assets for the Unity project")


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	reimport(environment["unity_executable"], configuration["unity_project_path"], arguments.simulate)


def reimport(unity_executable, unity_project_path, simulate):
	logger.info("Reimporting assets for '%s'", unity_project_path)
	development.commands.editor.run_editor_command(unity_executable, unity_project_path, None, None, simulate)
