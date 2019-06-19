import logging
import os
import subprocess

import commands.editor


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	parser = subparsers.add_parser("package", help = "generate a standalone package")
	parser.add_argument("--platform", required = True, choices = configuration["package_platforms"],
		metavar = "<platform>", help = "set the package platform (%s)" % ", ".join(configuration["package_platforms"]))
	parser.add_argument("--configuration", required = True, choices = configuration["package_configurations"],
		metavar = "<configuration>", help = "set the package configuration (%s)" % ", ".join(configuration["package_configurations"]))
	return parser


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	parameters = {
		"project": configuration["project"],
		"version": configuration["project_version"]["full"],
		"platform": arguments.platform,
		"configuration": arguments.configuration,
	}
	
	artifact = configuration["artifacts"]["package"]
	artifact_name = artifact["file_name"].format(**parameters)
	local_artifact_path = os.path.join(".artifacts", artifact["path_in_repository"], artifact_name)

	package(environment["unity_2019_executable"], configuration["unity_project_path"], arguments.platform, arguments.configuration, local_artifact_path, arguments.simulate)


def package(unity_executable, unity_project_path, platform, configuration, destination, simulate):
	logging.info("Packaging for platform '%s' with configuration '%s'", platform, configuration)
	logging.info("Writing package to '%s'", destination)

	command_arguments = {
		"platform": platform,
		"configuration": configuration,
		"destination": os.path.abspath(destination),
	}

	commands.editor.run_editor_command(unity_executable, unity_project_path, "GeneratePackage", command_arguments, simulate)
