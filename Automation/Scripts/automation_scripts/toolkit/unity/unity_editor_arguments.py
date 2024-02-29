
import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen = True)
class UnityEditorArguments:
    batch_mode: bool
    enable_graphics: bool
    quit_on_completion: bool

    build_target: Optional[str] = None
