import argparse
import logging

from bhamon_development_toolkit.automation.automation_command import AutomationCommand

from automation_scripts.configuration.project_configuration import ProjectConfiguration


logger = logging.getLogger("Main")


class InfoCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        return subparsers.add_parser("info", help = "show project information")


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        project_configuration: ProjectConfiguration = kwargs["configuration"]

        logger.info("ProjectIdentifier: %s", project_configuration.project_identifier)
        logger.info("ProjectDisplayName: %s", project_configuration.project_display_name)
        logger.info("ProjectVersion: %s", project_configuration.project_version.full_identifier)
        logger.info("Copyright: %s", project_configuration.copyright)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
