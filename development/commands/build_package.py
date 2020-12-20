import logging
import os

import development.configuration
import development.commands.editor


logger = logging.getLogger("Main")


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	parser = subparsers.add_parser("build-package", help = "build a game package")
	parser.add_argument("--platform", required = True, choices = configuration["build_platforms"],
		metavar = "<platform>", help = "set the platform to build for (%s)" % ", ".join(configuration["build_platforms"]))
	parser.add_argument("--configuration", required = True, choices = configuration["build_configurations"],
		metavar = "<configuration>", help = "set the configuration to build with (%s)" % ", ".join(configuration["build_configurations"]))
	return parser


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	unity_executable = environment["unity_executable"]
	unity_project_path = configuration["unity_project_path"]
	asset_bundle_directory = os.path.join(configuration["artifact_directory"], "AssetBundles", arguments.platform)
	package_directory = os.path.join(configuration["artifact_directory"], "Packages", arguments.platform, arguments.configuration)

	build_package(unity_executable, unity_project_path, arguments.platform, arguments.configuration, asset_bundle_directory, package_directory, simulate = arguments.simulate)


def build_package(unity_executable, unity_project_path, platform, configuration, asset_bundle_directory, package_directory, simulate): # pylint: disable = too-many-arguments
	logger.info("Building package for platform '%s' with configuration '%s'", platform, configuration)

	unity_platform = development.configuration.convert_to_unity_platform(platform)

	command_arguments = {
		"platform": platform,
		"configuration": configuration,
		"assetBundleDirectory": os.path.abspath(asset_bundle_directory),
		"packageDirectory": os.path.abspath(package_directory),
	}

	development.commands.editor.run_editor_command(
		unity_executable, unity_project_path, "BuildPackage", command_arguments, target_platform = unity_platform, simulate = simulate)
