import logging
import os

import development.configuration
import development.commands.editor


logger = logging.getLogger("Main")


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	parser = subparsers.add_parser("build-asset-bundles", help = "build asset bundles")
	parser.add_argument("--platform", required = True, choices = configuration["build_platforms"],
		metavar = "<platform>", help = "set the platform to build for (%s)" % ", ".join(configuration["build_platforms"]))
	return parser


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	unity_executable = environment["unity_executable"]
	unity_project_path = configuration["unity_project_path"]
	asset_bundle_directory = os.path.join(configuration["artifact_directory"], "AssetBundles", arguments.platform)

	build_asset_bundles(unity_executable, unity_project_path, arguments.platform, asset_bundle_directory, simulate = arguments.simulate)


def build_asset_bundles(unity_executable, unity_project_path, platform, asset_bundle_directory, simulate): # pylint: disable = too-many-arguments
	logger.info("Building asset bundles for platform '%s'", platform)

	unity_platform = development.configuration.convert_to_unity_platform(platform)

	command_arguments = {
		"platform": platform,
		"assetBundleDirectory": os.path.abspath(asset_bundle_directory),
	}

	development.commands.editor.run_editor_command(
		unity_executable, unity_project_path, "BuildAssetBundles", command_arguments, target_platform = unity_platform, simulate = simulate)
