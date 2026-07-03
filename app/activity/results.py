from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ActivitySummary:

    action: str
    card_name: str
    created_at: datetime
