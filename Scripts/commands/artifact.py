import argparse
import copy
import filecmp
import glob
import logging
import os
import shutil
import zipfile

import workspace


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument

	def parse_key_value_parameter(argument_value):
		key_value = argument_value.split("=")
		if len(key_value) != 2:
			raise argparse.ArgumentTypeError("invalid key value parameter: '%s'" % argument_value)
		return (key_value[0], key_value[1])

	command_list = [ "show", "package", "verify", "upload" ]

	parser = subparsers.add_parser("artifact", formatter_class = argparse.RawTextHelpFormatter,
		help = "execute commands related to build artifacts")
	parser.add_argument("artifact", choices = configuration["artifacts"].keys(),
		metavar = "<artifact>", help = "set an artifact definition to use for the commands")
	parser.add_argument("--command", choices = command_list, nargs = "+", dest = "artifact_commands",
		metavar = "<command>", help = "set the command(s) to execute for the artifact" + "\n" + "(%s)" % ", ".join(command_list))
	parser.add_argument("--parameters", nargs = "*", type = parse_key_value_parameter, default = [],
		metavar = "<key=value>", help = "set parameters for the artifact")
	parser.add_argument("--overwrite", action = "store_true",
		help = "overwrite existing artifact on upload")
	return parser


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	parameters = {
		"project": configuration["project"],
		"version": configuration["project_version"]["full"],
	}

	parameters.update(arguments.parameters)

	artifact = configuration["artifacts"][arguments.artifact]
	artifact_name = artifact["file_name"].format(**parameters)
	local_artifact_path = os.path.join(".artifacts", artifact["path_in_repository"], artifact_name)

	if "upload" in arguments.artifact_commands:
		remote_artifact_path = os.path.join(configuration["artifact_repository"], artifact["path_in_repository"], artifact_name)

	if "show" in arguments.artifact_commands:
		artifact_files = list_artifact_files(artifact, configuration, parameters)
		show(artifact_name, artifact_files)
		print("")
	if "package" in arguments.artifact_commands:
		artifact_files = merge_artifact_mapping(map_artifact_files(artifact, configuration, parameters))
		package(local_artifact_path, artifact_files, arguments.simulate)
		print("")
	if "verify" in arguments.artifact_commands:
		verify(local_artifact_path, arguments.simulate)
		print("")
	if "upload" in arguments.artifact_commands:
		upload(local_artifact_path, remote_artifact_path, arguments.overwrite, arguments.simulate)
		save_results(artifact_name, arguments.artifact, arguments.results, arguments.simulate)
		print("")


def show(artifact_name, artifact_files):
	logging.info("Artifact '%s'", artifact_name)

	for file_path in artifact_files:
		logging.info("+ '%s'", file_path)


def package(artifact_path, artifact_files, simulate):
	logging.info("Packaging artifact '%s'", os.path.basename(artifact_path))

	if len(artifact_files) == 0:
		raise RuntimeError("The artifact is empty")

	logging.info("Writing '%s'", artifact_path + ".zip")

	artifact_directory = os.path.dirname(artifact_path)
	if not simulate and not os.path.isdir(artifact_directory):
		os.makedirs(artifact_directory)

	if simulate:
		for source, destination in artifact_files:
			logging.info("+ '%s' => '%s'", source, destination)
	else:
		with zipfile.ZipFile(artifact_path + ".zip.tmp", "w", zipfile.ZIP_DEFLATED) as artifact_file:
			for source, destination in artifact_files:
				logging.info("+ '%s' => '%s'", source, destination)
				artifact_file.write(source, destination)
		shutil.move(artifact_path + ".zip.tmp", artifact_path + ".zip")


def verify(artifact_path, simulate):
	logging.info("Verifying artifact '%s'", os.path.basename(artifact_path))
	logging.info("Reading '%s'", artifact_path + ".zip")

	if not simulate:
		with zipfile.ZipFile(artifact_path + ".zip", 'r') as artifact_file:
			if artifact_file.testzip():
				raise RuntimeError('Artifact package is corrupted')


def upload(local_artifact_path, remote_artifact_path, overwrite, simulate):
	logging.info("Uploading artifact '%s'", os.path.basename(local_artifact_path))

	if not overwrite and os.path.exists(remote_artifact_path + ".zip"):
		raise ValueError("Artifact already exists")

	logging.info("Copying '%s' to '%s'", local_artifact_path + ".zip", remote_artifact_path + ".zip")

	remote_artifact_directory = os.path.dirname(remote_artifact_path)
	if not simulate and not os.path.isdir(remote_artifact_directory):
		os.makedirs(remote_artifact_directory)

	if not simulate:
		shutil.copyfile(local_artifact_path + ".zip", remote_artifact_path + ".zip.tmp")
		shutil.move(remote_artifact_path + ".zip.tmp", remote_artifact_path + ".zip")


def save_results(artifact_name, artifact_type, result_file_path, simulate):
	artifact_information = {
		"name": artifact_name,
		"type": artifact_type,
	}

	if result_file_path:
		results = workspace.load_results(result_file_path)
		results["artifacts"].append(artifact_information)
		if not simulate:
			workspace.save_results(result_file_path, results)


def list_artifact_files(artifact, configuration, parameters):
	all_files = []

	for fileset_options in artifact["filesets"]:
		fileset = configuration["filesets"][fileset_options["identifier"]]
		if "parameters" in fileset_options:
			fileset_parameters = copy.deepcopy(fileset_options["parameters"])
			fileset_parameters.update(parameters)
		else:
			fileset_parameters = parameters
		all_files += load_fileset(fileset, fileset_parameters)

	all_files.sort()

	return all_files


def map_artifact_files(artifact, configuration, parameters):
	all_files = []

	for fileset_options in artifact["filesets"]:
		fileset = configuration["filesets"][fileset_options["identifier"]]
		if "parameters" in fileset_options:
			fileset_parameters = copy.deepcopy(fileset_options["parameters"])
			fileset_parameters.update(parameters)
		else:
			fileset_parameters = parameters

		path_in_workspace = fileset["path_in_workspace"].format(**fileset_parameters)
		for source in load_fileset(fileset, fileset_parameters):
			destination = source
			if "path_in_archive" in fileset_options:
				destination = os.path.join(fileset_options["path_in_archive"], os.path.relpath(source, path_in_workspace))
			all_files.append((source, destination.replace("\\", "/")))

	all_files.sort()

	return all_files


def merge_artifact_mapping(artifact_files):
	merged_files = []
	has_conflicts = False

	for destination in set(dst for src, dst in artifact_files):
		source_collection = [ src for src, dst in artifact_files if dst == destination ]
		for source in source_collection[1:]:
			if not filecmp.cmp(source_collection[0], source):
				has_conflicts = True
				logging.error("Mapping conflict: %s, %s => %s", source_collection[0], source, destination)
		merged_files.append((source_collection[0], destination))

	if has_conflicts:
		raise ValueError("Artifact mapper has conflicts")

	merged_files.sort()

	return merged_files


def load_fileset(fileset, parameters):
	matched_files = []
	path_in_workspace = fileset["path_in_workspace"].format(**parameters)
	for file_pattern in fileset["file_patterns"]:
		matched_files += glob.glob(os.path.join(path_in_workspace, file_pattern.format(**parameters)), recursive = True)

	selected_files = []
	for file_path in matched_files:
		file_path = file_path.replace("\\", "/")
		if os.path.isfile(file_path):
			selected_files.append(file_path)

	selected_files.sort()
	return selected_files
