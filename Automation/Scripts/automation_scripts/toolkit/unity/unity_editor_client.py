import logging
import os
import subprocess
from typing import List, Optional

from bhamon_development_toolkit.processes import process_helpers
from bhamon_development_toolkit.processes.exceptions.process_exception import ProcessException
from bhamon_development_toolkit.processes.exceptions.process_start_exception import ProcessStartException
from bhamon_development_toolkit.processes.executable_command import ExecutableCommand
from bhamon_development_toolkit.processes.process_options import ProcessOptions
from bhamon_development_toolkit.processes.process_output_handler import ProcessOutputHandler
from bhamon_development_toolkit.processes.process_output_logger import ProcessOutputLogger
from bhamon_development_toolkit.processes.process_runner import ProcessRunner

from automation_scripts.toolkit.unity.unity_editor_arguments import UnityEditorArguments


logger = logging.getLogger("Unity")


class UnityEditorClient:


    def __init__(self, process_runner: ProcessRunner, unity_executable: str, project_path: str) -> None:
        self._process_runner = process_runner
        self._unity_executable = unity_executable
        self._project_path = project_path


    def launch(self, log_file_path: Optional[str] = None, simulate: bool = False) -> None:
        command = ExecutableCommand(self._unity_executable)
        command.add_arguments([ "-projectPath", self._project_path ])
        command.add_internal_arguments([ "-logFile", os.path.abspath(log_file_path) ] if log_file_path is not None else [], [])

        logger.info("Launching editor (Project: '%s')", self._project_path)
        logger.info("+ %s", process_helpers.format_executable_command(command.get_command_for_logging()))

        if not simulate:
            try:
                subprocess.Popen(command.get_command()) # pylint: disable = consider-using-with
            except FileNotFoundError as exception:
                exception_message = "Executable not found: '%s'" % (command.executable_name)
                raise ProcessStartException(exception_message, command.executable_path, None) from exception


    async def run(self,
            unity_arguments: UnityEditorArguments, custom_arguments: Optional[List[str]] = None,
            log_file_path: Optional[str] = None, simulate: bool = False) -> None:

        command_as_object = ExecutableCommand(self._unity_executable)
        command_as_object.add_arguments([ "-projectPath", self._project_path ])

        command_as_object.add_arguments([ "-batchMode" ] if unity_arguments.batch_mode else [])
        command_as_object.add_arguments([ "-noGraphics" ] if not unity_arguments.enable_graphics else [])
        command_as_object.add_arguments([ "-quit" ] if unity_arguments.quit_on_completion else [])
        command_as_object.add_arguments([ "-buildTarget", unity_arguments.build_target ] if unity_arguments.build_target is not None else [])
        command_as_object.add_internal_arguments([ "-logFile", "-" ], [])

        if custom_arguments is not None:
            command_as_object.add_arguments(custom_arguments)

        process_options = ProcessOptions()
        output_handlers: List[ProcessOutputHandler] = []
        if log_file_path is not None:
            output_handlers.append(ProcessOutputLogger(process_helpers.create_raw_logger(log_file_path = log_file_path)))

        logger.info("+ %s", process_helpers.format_executable_command(command_as_object.get_command_for_logging()))

        if not simulate:
            await self._process_runner.run(command_as_object, process_options, output_handlers)


    async def reimport(self,
            build_target: Optional[str] = None, enable_graphics = False,
            log_file_path: Optional[str] = None, simulate: bool = False) -> None:

        unity_arguments = UnityEditorArguments(
            batch_mode = True,
            enable_graphics = enable_graphics,
            quit_on_completion = True,
            build_target = build_target)

        logger.info("Reimporting (Project: '%s')", self._project_path)

        try:
            await self.run(unity_arguments, log_file_path = log_file_path, simulate = simulate)
        except ProcessException as exception:
            raise RuntimeError("Reimport failed") from exception


    async def execute(self, # pylint: disable = too-many-arguments
            unity_arguments: UnityEditorArguments, method: str, method_arguments: Optional[List[str]] = None,
            log_file_path: Optional[str] = None, simulate: bool = False) -> None:

        custom_arguments = [ "-executeMethod", method ]
        if method_arguments is not None:
            custom_arguments += method_arguments

        try:
            await self.run(unity_arguments, custom_arguments, log_file_path = log_file_path, simulate = simulate)
        except ProcessException as exception:
            raise RuntimeError("Unity execute failed") from exception
