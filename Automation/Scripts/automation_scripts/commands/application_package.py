import argparse
import logging
import os
from typing import Callable, List

from bhamon_development_toolkit.automation.automation_command import AutomationCommand
from bhamon_development_toolkit.automation.automation_command_group import AutomationCommandGroup

from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.configuration.project_environment import ProjectEnvironment
from automation_scripts.helpers import automation_factory


logger = logging.getLogger("Main")


class ApplicationPackageCommand(AutomationCommandGroup):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        local_parser: argparse.ArgumentParser = subparsers.add_parser("application-package", help = "commands related to application packages")

        command_collection: List[Callable[[],AutomationCommand]] = [
            _BuildCommand,
        ]

        self.add_commands(local_parser, command_collection)

        return local_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


class _BuildCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        local_parser: argparse.ArgumentParser = subparsers.add_parser("build", help = "build an application package")
        local_parser.add_argument("--platform", required = True, metavar = "<platform>", help = "set the platform to build for")
        local_parser.add_argument("--configuration", required = True, metavar = "<configuration>", help = "set the configuration to build with")
        return local_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        raise NotImplementedError("Not supported")


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        project_environment: ProjectEnvironment = kwargs["environment"]
        project_configuration: ProjectConfiguration = kwargs["configuration"]
        platform: str = arguments.platform
        configuration: str = arguments.configuration

        unity_project = project_configuration.list_unity_projects()[0] # FIXME
        log_file_path = os.path.join("Artifacts", "Editor", "BuildApplicationPackage.log")
        asset_bundle_directory = os.path.join("Artifacts", "AssetBundles", platform)
        package_directory = os.path.join("Artifacts", "ApplicationPackages", platform + "-" + configuration)

        unity_automation_client = automation_factory.create_unity_automation_client(project_environment, unity_project)

        await unity_automation_client.build_application_package(
            platform, configuration, asset_bundle_directory, package_directory, log_file_path = log_file_path, simulate = simulate)
