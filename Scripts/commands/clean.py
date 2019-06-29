import glob
import logging
import os
import shutil


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	return subparsers.add_parser("clean", help = "clean the workspace")


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	clean(configuration["unity_project_path"], arguments.simulate)


def clean(unity_project_path, simulate):
	logging.info("Cleaning the workspace")
	print("")

	directories_to_clean = [
		{ "display_name": "Build", "path": ".build" },
		{ "display_name": "Build artifacts", "path": ".artifacts" },
		{ "display_name": "Unity cache", "path": os.path.join(unity_project_path, "Library") },
		{ "display_name": "Unity logs", "path": os.path.join(unity_project_path, "Logs") },
		{ "display_name": "Unity temporary files", "path": os.path.join(unity_project_path, "Temp") },
	]

	for directory in directories_to_clean:
		if os.path.exists(directory["path"]):
			logging.info("Removing directory '%s' (Path: %s)", directory["display_name"], directory["path"])
			if not simulate:
				shutil.rmtree(directory["path"])

	for file_path in glob.glob(os.path.join(unity_project_path, "*.sln")):
		logging.info("Removing generated solution '%s'", file_path)
		if not simulate:
			os.remove(file_path)
	for file_path in glob.glob(os.path.join(unity_project_path, "*.csproj")):
		logging.info("Removing generated project '%s'", file_path)
		if not simulate:
			os.remove(file_path)
