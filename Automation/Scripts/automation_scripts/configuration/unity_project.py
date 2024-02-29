import dataclasses


@dataclasses.dataclass(frozen = True)
class UnityProject:
    path: str
    command_namespace: str
