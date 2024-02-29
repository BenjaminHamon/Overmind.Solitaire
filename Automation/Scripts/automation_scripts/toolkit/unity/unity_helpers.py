import os
import platform
import re


def find_unity_executable(unity_version: str) -> str:
    if platform.system() == "Windows":
        return os.path.join(os.environ["ProgramFiles"], "Unity", "Hub", "Editor", unity_version, "Editor", "Unity.exe")

    raise ValueError("Unsupported system: '%s'" % platform.system())


def get_unity_version(unity_project_path: str) -> str:
    version_file_path = os.path.join(unity_project_path, "ProjectSettings", "ProjectVersion.txt")
    with open(version_file_path, mode = "r", encoding = "utf-8") as version_file:
        version_text = version_file.read()

    version_match = re.search(r"^m_EditorVersion: (?P<version>[0-9a-z\.]*)$", version_text, flags = re.MULTILINE)
    if version_match is None:
        raise RuntimeError("Version information not found (Path: '%s')" % version_file_path)

    return version_match.group("version")
