import argparse
import datetime
import os

import mockito
import pytest

from bhamon_development_toolkit.automation import automation_helpers
from bhamon_development_toolkit.automation.project_version import ProjectVersion
from bhamon_development_toolkit.python.python_package import PythonPackage

from automation_scripts.commands.clean import CleanCommand
from automation_scripts.configuration.project_configuration import ProjectConfiguration


def get_project_configuration():
    project_configuration = mockito.mock(spec = ProjectConfiguration)
    project_configuration.project_identifier = "MyProjectIdentifier" # type: ignore
    project_configuration.project_display_name = "My Project Display Name" # type: ignore
    project_configuration.project_version = ProjectVersion( # type: ignore
        identifier = "1.0", revision = "abcde", revision_date = datetime.datetime(2020, 1, 1), branch = None)
    project_configuration.copyright = "Copyright (c) 2020 MyProject Contributors" # type: ignore

    mockito.when(project_configuration).list_automation_packages() \
        .thenReturn([ PythonPackage("my-python-package", "MyPythonPackage/Sources", "MyPythonPackage/Tests") ])
    mockito.when(project_configuration).list_unity_projects().thenReturn([ "MyUnityProject" ])

    return project_configuration


def create_project_files() -> None:
    os.makedirs("MyUnityProject")
    with open("MyUnityProject/MyUnityProject.sln", mode = "w", encoding = "utf-8"):
        pass


@pytest.mark.asyncio
async def test_run(tmpdir):
    with automation_helpers.execute_in_workspace(tmpdir):
        project_configuration = get_project_configuration()
        create_project_files()

        command = CleanCommand()
        await command.run_async(argparse.Namespace(), configuration = project_configuration, simulate = False)
        
        assert not os.path.exists("MyUnityProject/MyUnityProject.sln")


@pytest.mark.asyncio
async def test_run_with_simulate(tmpdir):
    with automation_helpers.execute_in_workspace(tmpdir):
        project_configuration = get_project_configuration()
        create_project_files()

        command = CleanCommand()
        await command.run_async(argparse.Namespace(), configuration = project_configuration, simulate = True)
        
        assert os.path.exists("MyUnityProject/MyUnityProject.sln")
