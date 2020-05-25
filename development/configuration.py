import datetime
import importlib
import os
import subprocess
import sys


def load_configuration(environment):
	configuration = {
		"project_identifier": "Overmind.Solitaire",
		"project_name": "Overmind Solitaire",
		"project_version": load_project_version(environment["git_executable"], "1.0"),
	}

	configuration["author"] = "Benjamin Hamon"
	configuration["author_email"] = "hamon.benjamin@gmail.com"
	configuration["organization"] = ""
	configuration["project_url"] = "https://github.com/BenjaminHamon/Overmind.Solitaire"
	configuration["copyright"] = "Copyright (c) 2020 Benjamin Hamon"

	configuration["development_toolkit"] = "git+https://github.com/BenjaminHamon/DevelopmentToolkit@{revision}#subdirectory=toolkit"
	configuration["development_toolkit_revision"] = "a4ad1edfb956641c420d42ff369087cffb6d7584"
	configuration["development_dependencies"] = [ "pylint" ]

	configuration["unity_project_path"] = "UnityClient"
	configuration["package_platforms"] = [ "Android", "Linux", "Windows" ]
	configuration["package_configurations"] = [ "Debug", "Release" ]

	configuration["project_identifier_for_artifact_server"] = "Solitaire"

	configuration["artifact_directory"] = "Artifacts"

	configuration["filesets"] = load_filesets(configuration["artifact_directory"])
	configuration["artifacts"] = load_artifacts()

	return configuration


def load_project_version(git_executable, identifier):
	branch = subprocess.check_output([ git_executable, "rev-parse", "--abbrev-ref", "HEAD" ], universal_newlines = True).strip()
	revision = subprocess.check_output([ git_executable, "rev-parse", "--short=10", "HEAD" ], universal_newlines = True).strip()
	revision_date = int(subprocess.check_output([ git_executable, "show", "--no-patch", "--format=%ct", revision ], universal_newlines = True).strip())
	revision_date = datetime.datetime.utcfromtimestamp(revision_date).replace(microsecond = 0).isoformat() + "Z"

	return {
		"identifier": identifier,
		"numeric": identifier,
		"full": identifier + "+" + revision,
		"branch": branch,
		"revision": revision,
		"date": revision_date,
	}


def load_filesets(artifact_directory):
	return {
		"package": {
			"path_in_workspace": os.path.join(artifact_directory, "Packages", "{platform}", "{configuration}"),
			"file_patterns": [ "**" ],
		},
	}


def load_artifacts():
	return {
		"package": {
			"file_name": "{project}_{version}_Package_{platform}_{configuration}",
			"path_in_repository": "Packages",
			"filesets": [
				{ "identifier": "package", "path_in_archive": "." },
			],
		},
	}


def load_commands():
	all_modules = [
		"development.commands.artifact",
		"development.commands.clean",
		"development.commands.develop",
		"development.commands.editor",
		"development.commands.package",
	]

	return [ import_command(module) for module in all_modules ]


def import_command(module_name):
	try:
		return {
			"module_name": module_name,
			"module": importlib.import_module(module_name),
		}

	except ImportError:
		return {
			"module_name": module_name,
			"exception": sys.exc_info(),
		}
