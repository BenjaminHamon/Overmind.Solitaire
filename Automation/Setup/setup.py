# cspell:words pyvenv

import argparse
import logging
import os
import sys

import automation_helpers
import python_helpers


logger = logging.getLogger("Main")


python_versions = [ "3.9", "3.10", "3.11" ]
venv_directory = ".venv"


def main() -> None:

    # Prevent active pyvenv from overriding a python executable specified in a command
    if "__PYVENV_LAUNCHER__" in os.environ:
        del os.environ["__PYVENV_LAUNCHER__"]

    with automation_helpers.execute_in_workspace(__file__):
        arguments = parse_arguments()
        automation_helpers.configure_logging(arguments.verbosity)
        project_configuration = automation_helpers.load_project_configuration(".")

        log_script_information(project_configuration, simulate = arguments.simulate)

        logger.info("Setting up local workspace (Path: %s)", os.getcwd())

        python_system_executable = python_helpers.find_and_check_system_python_executable(python_versions)
        venv_python_executable = python_helpers.get_venv_python_executable(venv_directory)
        python_package_collection = [ "Automation/Scripts[dev]" ]

        python_helpers.setup_virtual_environment(python_system_executable, venv_directory, simulate = arguments.simulate)
        python_helpers.install_python_packages(venv_python_executable, python_package_collection, simulate = arguments.simulate)


def parse_arguments() -> argparse.Namespace:
    all_log_levels = [ "debug", "info", "warning", "error", "critical" ]

    main_parser = argparse.ArgumentParser()
    main_parser.add_argument("--simulate", action = "store_true",
        help = "perform a test run, without writing changes")
    main_parser.add_argument("--verbosity", choices = all_log_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(all_log_levels))

    return main_parser.parse_args()


def log_script_information(configuration: dict, simulate: bool = False) -> None:
    if simulate:
        logger.info("(( The script is running as a simulation ))")
        logger.info("")

    logger.info("%s %s", configuration["ProjectDisplayName"], configuration["ProjectVersionFull"])
    logger.info("Script executing in '%s'", os.getcwd())
    logger.info("")


if __name__ == "__main__":
    try:
        main()
    except Exception: # pylint: disable = broad-except
        logger.error("Script failed", exc_info = True)
        sys.exit(1)
