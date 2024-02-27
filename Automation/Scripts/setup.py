# cspell:words bhamon dateutil

import os
import sys

import setuptools

workspace_directory = os.path.abspath(os.path.join("..", ".."))
automation_setup_directory = os.path.join(workspace_directory, "Automation", "Setup")

sys.path.insert(0, automation_setup_directory)

import automation_helpers # pylint: disable = import-error, wrong-import-position


def run_setup() -> None:
    project_configuration = automation_helpers.load_project_configuration(workspace_directory)

    setuptools.setup(
		name = "automation-scripts",
		description = "Automation scripts for %s" % project_configuration["ProjectDisplayName"],
        version = project_configuration["ProjectVersionFull"],
        author = project_configuration["Author"],
        author_email = project_configuration["AuthorEmail"],
        packages = setuptools.find_packages(include = [ "automation_scripts", "automation_scripts.*" ]),

        python_requires = "~= 3.9",

        extras_require = {
            "dev": [
                "bhamon-development-toolkit ~= 2.0.1",
                "mockito ~= 1.4.0",
                "pylint ~= 3.1.0",
                "pytest ~= 8.0.2",
                "pytest-asyncio ~= 0.23.5",
                "pytest-json ~= 0.4.0",
                "python-dateutil ~= 2.8.2",
                "PyYAML ~= 6.0.1",
            ],
        },
    )


run_setup()
