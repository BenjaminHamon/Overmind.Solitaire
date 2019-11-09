import datetime
import subprocess

import commands.artifact
import commands.clean
import commands.editor
import commands.package


def get_command_list():
	return [
		commands.artifact,
		commands.clean,
		commands.editor,
		commands.package,
	]


def load_configuration(environment):
	configuration = {
		"project": "Overmind.Solitaire",
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
	configuration["copyright"] = "Copyright (c) 2019 Benjamin Hamon"

	configuration["unity_project_path"] = "UnityClient"
	configuration["package_platforms"] = [ "Android", "Linux", "Windows" ]
	configuration["package_configurations"] = [ "Debug", "Release" ]

	configuration["project_identifier_for_artifact_server"] = "Solitaire"

	configuration["filesets"] = {
		"package": {
			"path_in_workspace": ".build/Packages/{platform}/{configuration}",
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
