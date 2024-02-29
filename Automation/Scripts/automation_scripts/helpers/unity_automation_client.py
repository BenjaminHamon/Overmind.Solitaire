import os
from typing import Dict, Optional

from automation_scripts.toolkit.unity.unity_editor_arguments import UnityEditorArguments
from automation_scripts.toolkit.unity.unity_editor_client import UnityEditorClient


class UnityAutomationClient:


    def __init__(self, editor_client: UnityEditorClient, command_namespace: str) -> None:
        self._editor_client = editor_client
        self._command_namespace = command_namespace


    async def build_asset_bundles(self,
            platform: str, asset_bundle_directory: str,
            log_file_path: Optional[str] = None, simulate: bool = False) -> None:

        command = "BuildAssetBundles"

        command_arguments = {
            "platform": platform,
            "assetBundleDirectory": os.path.abspath(asset_bundle_directory),
        }

        build_target = self._convert_platform_to_unity_build_target(platform)

        await self.run_command(command, command_arguments, build_target, log_file_path = log_file_path, simulate = simulate)


    async def run_command(self, # pylint: disable = too-many-arguments
            command: str, command_arguments: Dict[str,str],
            build_target: Optional[str] = None, log_file_path: Optional[str] = None, simulate: bool = False) -> None:

        unity_arguments = UnityEditorArguments(batch_mode = True, enable_graphics = False, quit_on_completion = True, build_target = build_target)

        command_fully_qualified = self._command_namespace + "." + command
        command_arguments_formatted = [ "-executeMethodArguments" ] + [ key + "=" + value for key, value in command_arguments.items() ]

        await self._editor_client.execute(
            unity_arguments, command_fully_qualified,  command_arguments_formatted, log_file_path = log_file_path, simulate = simulate)


    def _convert_platform_to_unity_build_target(self, platform: str) -> Optional[str]:
        if platform is None:
            return None

        if platform == "Android":
            return "Android"
        if platform == "Linux":
            return "Linux64"
        if platform == "Windows":
            return "Win64"

        raise ValueError("Unsupported platform: '%s'" % platform)
