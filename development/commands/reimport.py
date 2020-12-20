import logging

import development.configuration
import development.commands.editor


logger = logging.getLogger("Main")


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	parser = subparsers.add_parser("reimport", help = "reimport all assets for the Unity project")
	parser.add_argument("--platform", choices = configuration["build_platforms"],
		metavar = "<platform>", help = "set the platform to reimport for (%s)" % ", ".join(configuration["build_platforms"]))
	return parser


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	unity_executable = environment["unity_executable"]
	unity_project_path = configuration["unity_project_path"]

	reimport(unity_executable, unity_project_path, arguments.platform, simulate = arguments.simulate)


def reimport(unity_executable, unity_project_path, platform, simulate):
	logger.info("Reimporting assets for '%s'", platform if platform is not None else "default")

	unity_platform = development.configuration.convert_to_unity_platform(platform)

	development.commands.editor.run_editor_command(
		unity_executable, unity_project_path, None, None, target_platform = unity_platform, simulate = simulate)
