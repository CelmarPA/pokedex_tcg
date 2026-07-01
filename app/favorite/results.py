from dataclasses import dataclass


@dataclass(slots=True)
class ToggleResult:

    added: bool
