# cspell:words levelname

import contextlib
import json
import logging
import os
import subprocess
from typing import Generator


@contextlib.contextmanager
def execute_in_workspace(script_path: str) -> Generator[None,None,None]:
    current_directory = os.getcwd()
    workspace_directory = resolve_workspace_root(script_path)

    os.chdir(workspace_directory)

    try:
        yield
    finally:
        os.chdir(current_directory)


def resolve_workspace_root(script_path: str) -> str:
    directory = os.path.dirname(os.path.realpath(script_path))

    while True:
        if os.path.isdir(os.path.join(directory, ".git")):
            return directory
        if os.path.dirname(directory) == directory:
            raise RuntimeError("Failed to resolve the workspace root")
        directory = os.path.dirname(directory)


def configure_logging(verbosity: str) -> None:
    logging.basicConfig(
        level = logging.getLevelName(verbosity.upper()),
        format = "[{levelname}][{name}] {message}",
        datefmt = "%Y-%m-%dT%H:%M:%S",
        style = "{")


def load_project_configuration(workspace_directory: str) -> dict:
    project_information_file_path = os.path.join(workspace_directory, "ProjectConfiguration.json")
    with open(project_information_file_path, mode = "r", encoding = "utf-8") as project_information_file:
        project_configuration = json.load(project_information_file)

    revision = get_current_revision()
    project_configuration["ProjectVersionFull"] = project_configuration["ProjectVersionIdentifier"] + "+" + revision[:10]

    return project_configuration


def get_current_revision() -> str:
    git_command = [ "git", "rev-list", "--max-count", "1", "HEAD" ]
    git_command_result = subprocess.run(git_command, check = True, capture_output = True, text = True, encoding = "utf-8")
    return git_command_result.stdout.strip()
