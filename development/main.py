import argparse
import logging
import os
import sys

sys.path.insert(0, os.path.join(sys.path[0], ".."))

import development.configuration # pylint: disable = wrong-import-position
import development.environment # pylint: disable = wrong-import-position


logger = logging.getLogger("Main")


def main():
	with development.environment.execute_in_workspace(__file__):
		environment_instance = development.environment.load_environment()
		configuration_instance = development.configuration.load_configuration(environment_instance)
		command_list = development.configuration.load_commands()

		arguments = parse_arguments(environment_instance, configuration_instance, command_list)
		development.environment.configure_logging(environment_instance, arguments)

		show_project_information(configuration_instance, arguments.simulate)
		arguments.func(environment_instance, configuration_instance, arguments)


def parse_arguments(environment_instance, configuration_instance, command_list):
	all_log_levels = development.environment.all_log_levels

	main_parser = argparse.ArgumentParser()
	main_parser.add_argument("--simulate", action = "store_true",
			help = "perform a test run, without writing changes")
	main_parser.add_argument("--verbosity", choices = all_log_levels,
			metavar = "<level>", help = "set the logging level (%s)" % ", ".join(all_log_levels))
	main_parser.add_argument("--log-file",
			metavar = "<file_path>", help = "set the log file path")
	main_parser.add_argument("--log-file-verbosity", choices = all_log_levels,
			metavar = "<level>", help = "set the logging level for the log file (%s)" % ", ".join(all_log_levels))
	main_parser.add_argument("--results",
			metavar = "<file_path>", help = "set the file path where to store command results")

	subparsers = main_parser.add_subparsers(title = "commands", metavar = "<command>")
	subparsers.required = True

	for command in [ command for command in command_list if "module" in command ]:
		command_parser = command["module"].configure_argument_parser(environment_instance, configuration_instance, subparsers)
		command_parser.set_defaults(func = command["module"].run)

	return main_parser.parse_args()


def show_project_information(configuration_instance, simulate):
	logger.info("%s %s", configuration_instance["project_name"], configuration_instance["project_version"]["full"])
	logger.info("Script executing in '%s' %s", os.getcwd(), "(simulation)" if simulate else '')
	print("")


if __name__ == "__main__":
	main()
