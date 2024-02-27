import argparse
import glob
import logging
import os
import shutil

from bhamon_development_toolkit.automation.automation_command import AutomationCommand
from bhamon_development_toolkit.python.python_package import PythonPackage

from automation_scripts.configuration.project_configuration import ProjectConfiguration


logger = logging.getLogger("Main")


class CleanCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        return subparsers.add_parser("clean", help = "clean the workspace")


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        project_configuration: ProjectConfiguration = kwargs["configuration"]

        logger.info("Cleaning the workspace")
        logger.info("")

        artifact_directory = "Artifacts"
        all_python_packages = project_configuration.list_automation_packages()
        all_unity_projects = project_configuration.list_unity_projects()

        self.clean_artifacts(artifact_directory, simulate = simulate)
        for python_package in all_python_packages:
            self.clean_python_package(python_package, simulate = simulate)
        self._remove_directory(".pytest_cache", simulate = simulate)
        for unity_project in all_unity_projects:
            self.clean_unity_project(unity_project.path, simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)


    def clean_artifacts(self, artifact_directory: str, simulate: bool = False) -> None:
        self._remove_directory(artifact_directory, simulate = simulate)


    def clean_python_package(self, python_package: PythonPackage, simulate: bool = False) -> None:
        directories_to_remove = [
            os.path.join(python_package.path_to_sources, "build"),
            os.path.join(python_package.path_to_sources, "dist"),
            os.path.join(python_package.path_to_sources, python_package.name_for_file_system + ".egg-info"),
        ]

        for directory in directories_to_remove:
            self._remove_directory(directory, simulate = simulate)

        metadata_file_path = os.path.join(python_package.path_to_sources, "__metadata__.py")
        self._remove_file(metadata_file_path, simulate = simulate)

        self.clean_python_cache(python_package.path_to_sources, simulate = simulate)
        if python_package.path_to_tests is not None:
            self.clean_python_cache(python_package.path_to_tests, simulate = simulate)


    def clean_python_cache(self, source_directory: str, simulate: bool = False) -> None:
        if not os.path.exists(source_directory):
            return

        directories_to_remove = glob.glob(os.path.join(source_directory, "**", "__pycache__"), recursive = True)

        for directory in directories_to_remove:
            self._remove_directory(directory, simulate = simulate)


    def clean_unity_project(self, unity_project_path: str, simulate: bool = False) -> None:
        directories_to_remove = [
            os.path.join(unity_project_path, "Library"),
            os.path.join(unity_project_path, "Logs"),
            os.path.join(unity_project_path, "obj"),
            os.path.join(unity_project_path, "Temp"),
        ]

        files_to_remove: list[str] = []
        files_to_remove += glob.glob(os.path.join(unity_project_path, "*.sln"))
        files_to_remove += glob.glob(os.path.join(unity_project_path, "*.csproj"))

        for directory in directories_to_remove:
            self._remove_directory(directory, simulate = simulate)
        for file_path in files_to_remove:
            self._remove_file(file_path, simulate = simulate)


    def _remove_directory(self, directory_to_remove: str, simulate: bool = False) -> None:
        if os.path.exists(directory_to_remove):
            logger.debug("Removing directory '%s'", directory_to_remove)
            if not simulate:
                shutil.rmtree(directory_to_remove)


    def _remove_file(self, file_to_remove: str, simulate: bool = False) -> None:
        if os.path.exists(file_to_remove):
            logger.debug("Removing file '%s'", file_to_remove)
            if not simulate:
                os.remove(file_to_remove)
