import argparse
import logging
import os
import sys

sys.path.insert(0, os.path.join(sys.path[0], ".."))

import development.configuration # pylint: disable = wrong-import-position
import development.environment # pylint: disable = wrong-import-position


def main():
	script_path = os.path.realpath(__file__)
	workspace_directory = os.path.dirname(os.path.dirname(script_path))
	os.chdir(workspace_directory)

	environment_instance = development.environment.load_environment()
	configuration_instance = development.configuration.load_configuration(environment_instance)

	arguments = parse_arguments(environment_instance, configuration_instance)
	development.environment.configure_logging(logging.getLevelName(arguments.verbosity.upper()))

	show_project_information(configuration_instance, arguments.simulate)
	arguments.func(environment_instance, configuration_instance, arguments)


def parse_arguments(environment_instance, configuration_instance):
	all_log_levels = [ "debug", "info", "warning", "error", "critical" ]

	main_parser = argparse.ArgumentParser()
	main_parser.add_argument("--verbosity", choices = all_log_levels, default = "info",
		metavar = "<level>", help = "set the logging level (%s)" % ", ".join(all_log_levels))
	main_parser.add_argument("--simulate", action = "store_true", help = "perform a simulated run")
	main_parser.add_argument("--results", metavar = "<path>", help = "set the file path where to store execution results")

	subparsers = main_parser.add_subparsers(title = "commands", metavar = "<command>")
	subparsers.required = True

	for command_module in development.configuration.get_command_list():
		command_parser = command_module.configure_argument_parser(environment_instance, configuration_instance, subparsers)
		command_parser.set_defaults(func = command_module.run)

	return main_parser.parse_args()


def show_project_information(configuration_instance, simulate):
	logging.info("%s %s", configuration_instance["project_name"], configuration_instance["project_version"]["full"])
	logging.info("Script executing in %s %s", os.getcwd(), "(simulation)" if simulate else '')
	print("")


if __name__ == "__main__":
	main()
