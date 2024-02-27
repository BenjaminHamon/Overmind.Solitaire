import json

from bhamon_development_toolkit.automation.project_version import ProjectVersion
from bhamon_development_toolkit.revision_control.git_client import GitClient

from automation_scripts.configuration.project_configuration import ProjectConfiguration


def load_configuration() -> ProjectConfiguration:
    json_file_path = "ProjectConfiguration.json"
    with open(json_file_path, mode = "r", encoding = "utf-8") as json_file:
        project_configuration_as_dict = json.load(json_file)

    return ProjectConfiguration(
        project_identifier = project_configuration_as_dict["ProjectIdentifier"],
        project_display_name = project_configuration_as_dict["ProjectDisplayName"],
        project_version = load_project_version(project_configuration_as_dict["ProjectVersionIdentifier"]),
        copyright_text = project_configuration_as_dict["Copyright"],
        author = project_configuration_as_dict["Author"],
        author_email = project_configuration_as_dict["AuthorEmail"],
    )


def load_project_version(identifier: str) -> ProjectVersion:
    git_client = GitClient("git")

    revision = git_client.get_current_revision()
    revision_date = git_client.get_revision_date(revision)
    branch = git_client.get_current_branch()

    return ProjectVersion(
        identifier = identifier,
        revision = revision,
        revision_date = revision_date,
        branch = branch,
    )
