import dataclasses


@dataclasses.dataclass(frozen = True)
class UnityProject:
    path: str
