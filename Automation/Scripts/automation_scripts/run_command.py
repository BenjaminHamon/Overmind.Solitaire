import argparse
import logging
import sys
from typing import List

from bhamon_development_toolkit.asyncio_extensions.asyncio_context import AsyncioContext
from bhamon_development_toolkit.automation.automation_command import AutomationCommand

from automation_scripts.configuration import configuration_manager
from automation_scripts.configuration.project_environment import ProjectEnvironment
from automation_scripts.helpers import automation_helpers


logger = logging.getLogger("Main")


def main():
    with automation_helpers.execute_in_workspace(__file__):
        environment = ProjectEnvironment()
        configuration = configuration_manager.load_configuration()
        command_collection = list_commands()

        argument_parser = create_argument_parser(command_collection)
        arguments = argument_parser.parse_args()
        command_instance: AutomationCommand = arguments.command_instance

        automation_helpers.configure_logging(arguments)

        automation_helpers.log_script_information(configuration, arguments.simulate)
        command_instance.check_requirements(arguments, environment = environment, configuration = configuration)

        asyncio_context = AsyncioContext()
        asyncio_context.run(command_instance.run_async(arguments, environment = environment, configuration = configuration, simulate = arguments.simulate))


def create_argument_parser(command_collection: List[str]) -> argparse.ArgumentParser:
    main_parser = automation_helpers.create_argument_parser()

    subparsers = main_parser.add_subparsers(title = "commands", metavar = "<command>")
    subparsers.required = True

    for command in command_collection:
        command_instance = automation_helpers.create_command_instance(command)
        command_parser = command_instance.configure_argument_parser(subparsers)
        command_parser.set_defaults(command_instance = command_instance)

    return main_parser


def list_commands() -> List[str]:
    return [
        "automation_scripts.commands.application_package.ApplicationPackageCommand",
        "automation_scripts.commands.asset_bundles.AssetBundlesCommand",
        "automation_scripts.commands.clean.CleanCommand",
        "automation_scripts.commands.editor.EditorCommand",
        "automation_scripts.commands.info.InfoCommand",
    ]


if __name__ == "__main__":
    try:
        main()
    except Exception: # pylint: disable = broad-except
        logger.error("Script failed", exc_info = True)
        sys.exit(1)
