import contextlib
import json
import logging
import os
import platform
import sys


all_log_levels = [ "debug", "info", "warning", "error", "critical" ]


@contextlib.contextmanager
def execute_in_workspace(script_path):
	current_directory = os.getcwd()
	workspace_directory = resolve_workspace_root(script_path)

	os.chdir(workspace_directory)

	try:
		yield
	finally:
		os.chdir(current_directory)


def resolve_workspace_root(script_path):
	directory = os.path.dirname(os.path.realpath(script_path))

	while True:
		if os.path.isdir(os.path.join(directory, ".git")):
			return directory
		if os.path.dirname(directory) == directory:
			raise RuntimeError("Failed to resolve the workspace root")
		directory = os.path.dirname(directory)


def create_default_environment():
	return {
		"logging_stream_level": "info",
		"logging_stream_format": "[{levelname}][{name}] {message}",
		"logging_stream_date_format": "%Y-%m-%dT%H:%M:%S",
		"logging_stream_traceback": False,

		"logging_file_level": "debug",
		"logging_file_format": "[{levelname}][{name}] {message}",
		"logging_file_date_format": "%Y-%m-%dT%H:%M:%S",
		"logging_file_traceback": True,
		"logging_file_mode": "w",
		"logging_file_paths": [],

		"logging_summary_format": "[{levelname}][{name}] {message}",
		"logging_summary_date_format": "%Y-%m-%dT%H:%M:%S",

		"git_executable": "git",
		"scp_executable": "scp",
		"ssh_executable": "ssh",
		"unity_executable": find_unity(),
	}


def load_environment():
	environment_instance = create_default_environment()
	environment_instance.update(_load_environment_transform(os.path.join(os.path.expanduser("~"), "environment.json")))
	environment_instance.update(_load_environment_transform("environment.json"))
	return environment_instance


def _load_environment_transform(transform_file_path):
	if not os.path.exists(transform_file_path):
		return {}
	with open(transform_file_path) as transform_file:
		return json.load(transform_file)


def configure_logging(environment_instance, arguments):
	if arguments is not None and getattr(arguments, "verbosity", None) is not None:
		environment_instance["logging_stream_level"] = arguments.verbosity
	if arguments is not None and getattr(arguments, "verbosity", None) == "debug":
		environment_instance["logging_stream_traceback"] = True
	if arguments is not None and getattr(arguments, "log_file_verbosity", None) is not None:
		environment_instance["logging_file_level"] = arguments.log_file_verbosity
	if arguments is not None and getattr(arguments, "log_file", None) is not None:
		environment_instance["logging_file_paths"].append(arguments.log_file)

	environment_instance["logging_stream_levelno"] = logging.getLevelName(environment_instance["logging_stream_level"].upper())
	environment_instance["logging_file_levelno"] = logging.getLevelName(environment_instance["logging_file_level"].upper())

	logging.root.setLevel(logging.DEBUG)

	logging.addLevelName(logging.DEBUG, "Debug")
	logging.addLevelName(logging.INFO, "Info")
	logging.addLevelName(logging.WARNING, "Warning")
	logging.addLevelName(logging.ERROR, "Error")
	logging.addLevelName(logging.CRITICAL, "Critical")

	configure_log_stream(environment_instance, sys.stdout)
	for log_file_path in environment_instance["logging_file_paths"]:
		configure_log_file(environment_instance, log_file_path)


def configure_log_stream(environment_instance, stream):
	formatter = logging.Formatter(environment_instance["logging_stream_format"], environment_instance["logging_stream_date_format"], "{")
	stream_handler = logging.StreamHandler(stream)
	stream_handler.setLevel(environment_instance["logging_stream_levelno"])
	stream_handler.formatter = formatter
	logging.root.addHandler(stream_handler)


def configure_log_file(environment_instance, file_path):
	if os.path.dirname(file_path):
		os.makedirs(os.path.dirname(file_path), exist_ok = True)

	formatter = logging.Formatter(environment_instance["logging_file_format"], environment_instance["logging_file_date_format"], "{")
	file_handler = logging.FileHandler(file_path, mode = environment_instance["logging_file_mode"], encoding = "utf-8")
	file_handler.setLevel(environment_instance["logging_file_levelno"])
	file_handler.formatter = formatter
	logging.root.addHandler(file_handler)


def find_unity():
	if platform.system() == "Windows":
		return os.path.join(os.environ["ProgramFiles"], "Unity", "Hub", "Editor", "{version}", "Editor", "Unity.exe")
	return "unity_{version}"
