from datetime import datetime, timezone
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class User:
    email: str
    password: str
    id: UUID = field(default_factory=uuid4)
    is_enabled: bool = field(
        default=False
    )  # account has been activated (default False at creation)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    modified_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
