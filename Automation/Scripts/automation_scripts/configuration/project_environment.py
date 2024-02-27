from automation_scripts.toolkit.unity import unity_helpers


class ProjectEnvironment:


    def get_unity_executable(self, unity_version: str) -> str:
        return unity_helpers.find_unity_executable(unity_version)


    def get_unity_executable_from_project_path(self, unity_project_path: str) -> str:
        unity_version = unity_helpers.get_unity_version(unity_project_path)
        return unity_helpers.find_unity_executable(unity_version)
