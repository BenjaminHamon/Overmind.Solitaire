import os
from typing import List

from bhamon_development_toolkit.automation.project_version import ProjectVersion
from bhamon_development_toolkit.python.python_package import PythonPackage

from automation_scripts.configuration.unity_project import UnityProject


class ProjectConfiguration:


    def __init__(self, # pylint: disable = too-many-arguments
            project_identifier: str,
            project_display_name: str,
            project_version: ProjectVersion,
            copyright_text: str,
            author: str,
            author_email: str) -> None:

        self.project_identifier = project_identifier
        self.project_display_name = project_display_name
        self.project_version = project_version

        self.copyright = copyright_text

        self.author = author
        self.author_email = author_email


    def get_artifact_default_parameters(self) -> dict:
        return {
            "project": self.project_identifier,
            "version": self.project_version.identifier,
            "revision": self.project_version.revision_short,
        }


    def list_automation_packages(self) -> List[PythonPackage]:
        return [
            PythonPackage(
                identifier = "automation-scripts",
                path_to_sources = os.path.join("Automation", "Scripts"),
                path_to_tests = os.path.join("Automation", "Tests")),
        ]


    def list_unity_projects(self) -> List[UnityProject]:
        return [
            UnityProject(
                path = "UnityClient",
                command_namespace = "Overmind.Solitaire.UnityClient.Editor.EditorCommand",
            )
        ]
