import datetime
import importlib
import os
import subprocess
import sys


def load_configuration(environment):
	configuration = {
		"project_identifier": "Overmind.Solitaire",
		"project_name": "Overmind Solitaire",
		"project_version": { "identifier": "1.0" },
	}

	branch = subprocess.check_output([ environment["git_executable"], "rev-parse", "--abbrev-ref", "HEAD" ]).decode("utf-8").strip()
	revision = subprocess.check_output([ environment["git_executable"], "rev-parse", "--short=10", "HEAD" ]).decode("utf-8").strip()
	revision_date = int(subprocess.check_output([ environment["git_executable"], "show", "--no-patch", "--format=%ct", revision ]).decode("utf-8").strip())
	revision_date = datetime.datetime.utcfromtimestamp(revision_date).replace(microsecond = 0).isoformat() + "Z"

	configuration["project_version"]["branch"] = branch
	configuration["project_version"]["revision"] = revision
	configuration["project_version"]["date"] = revision_date
	configuration["project_version"]["numeric"] = "{identifier}".format(**configuration["project_version"])
	configuration["project_version"]["full"] = "{identifier}-{revision}".format(**configuration["project_version"])

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

	configuration["filesets"] = {
		"package": {
			"path_in_workspace": os.path.join(configuration["artifact_directory"], "Packages", "{platform}", "{configuration}"),
			"file_patterns": [ "**" ],
		},
	}

	configuration["artifacts"] = {
		"package": {
			"file_name": "{project}_{version}_Package_{platform}_{configuration}",
			"path_in_repository": "Packages",
			"filesets": [
				{ "identifier": "package", "path_in_archive": "." },
			],
		},
	}

	return configuration


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
