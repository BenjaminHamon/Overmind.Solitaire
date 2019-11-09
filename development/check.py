import logging
import os
import sys

sys.path.insert(0, os.path.join(sys.path[0], ".."))

import development.configuration # pylint: disable = wrong-import-position
import development.environment # pylint: disable = wrong-import-position


logger = logging.getLogger("Main")


def main():
	current_directory = os.getcwd()
	script_path = os.path.realpath(__file__)
	workspace_directory = os.path.dirname(os.path.dirname(script_path))

	os.chdir(workspace_directory)

	try:
		development.environment.configure_logging(logging.INFO)
		command_list = development.configuration.load_commands()

		check_commands(command_list)

	finally:
		os.chdir(current_directory)


def check_commands(command_list):
	for command in command_list:
		if "exception" in command:
			logger.error("Command '%s' is unavailable", command["module_name"], exc_info = command["exception"])
			print("")


if __name__ == "__main__":
	main()
