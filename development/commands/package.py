import logging
import os

import development.commands.editor


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	parser = subparsers.add_parser("package", help = "generate a standalone package")
	parser.add_argument("--platform", required = True, choices = configuration["package_platforms"],
		metavar = "<platform>", help = "set the package platform (%s)" % ", ".join(configuration["package_platforms"]))
	parser.add_argument("--configuration", required = True, choices = configuration["package_configurations"],
		metavar = "<configuration>", help = "set the package configuration (%s)" % ", ".join(configuration["package_configurations"]))
	return parser


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	unity_executable = environment["unity_2019_executable"]
	unity_project_path = configuration["unity_project_path"]
	package_path = os.path.join(".build", "Packages", arguments.platform, arguments.configuration)

	package(unity_executable, unity_project_path, arguments.platform, arguments.configuration, package_path, arguments.simulate)


def package(unity_executable, unity_project_path, platform, configuration, destination, simulate): # pylint: disable = too-many-arguments
	logging.info("Packaging for platform '%s' with configuration '%s'", platform, configuration)
	logging.info("Writing package to '%s'", destination)

	command_arguments = {
		"platform": platform,
		"configuration": configuration,
		"destination": os.path.abspath(destination),
	}

	development.commands.editor.run_editor_command(unity_executable, unity_project_path, "GeneratePackage", command_arguments, simulate)
