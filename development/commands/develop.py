import logging
import os
import subprocess
import sys


logger = logging.getLogger("Main")


def configure_argument_parser(environment, configuration, subparsers): # pylint: disable = unused-argument
	return subparsers.add_parser("develop", help = "setup workspace for development")


def run(environment, configuration, arguments): # pylint: disable = unused-argument
	python_executable = sys.executable
	python_package_repository = environment.get("python_package_repository_web_url", None)

	logger.info("Installing development toolkit")
	development_toolkit_package = configuration["development_toolkit"].format(revision = configuration["development_toolkit_revision"])
	install_packages(python_executable, python_package_repository, [ development_toolkit_package ], simulate = arguments.simulate)
	print("")

	if len(configuration.get("development_dependencies", [])) > 0:
		logger.info("Installing development dependencies")
		install_packages(python_executable, python_package_repository, configuration["development_dependencies"], simulate = arguments.simulate)
		print("")


def install_packages(python_executable, python_package_repository, package_collection, simulate):
	install_command = [ python_executable, "-m", "pip", "install", "--upgrade" ]
	install_command += [ "--extra-index", python_package_repository ] if python_package_repository is not None else []

	for package in package_collection:
		install_command += [ "--editable", package ] if os.path.isdir(package) else [ package ]

	logger.info("+ %s", " ".join(("'" + x + "'") if " " in x else x for x in install_command))
	if not simulate:
		subprocess.check_call(install_command)
