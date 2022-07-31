import json
import pathlib
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Role:
    emoji: str
    role_id: int

    @classmethod
    def from_dict(cls, data):
        return cls(
            emoji=data['emoji'],
            role_id=data['role_id'],
        )

    def to_dict(self):
        return {'role_id': self.role_id}


@dataclass
class Guild:
    guild_id: int
    welcome_message_id: Optional[int] = None
    roles: dict[str, Role] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data):
        return cls(
            guild_id=data['guild_id'],
            welcome_message_id=data['welcome_message_id'],
            roles={
                emoji: Role.from_dict({
                    'emoji': emoji,
                    **role_data
                }) for emoji, role_data in data['roles'].items()
            },
        )

    def to_dict(self):
        return {
            'welcome_message_id': self.welcome_message_id,
            'roles': {
                emoji: role.to_dict()
                for emoji, role in self.roles.items()
            },
        }


@dataclass
class Config:
    filename: str
    guilds: dict[int, Guild] = field(default_factory=dict)

    def __post_init__(self):
        self._path = pathlib.Path(self.filename)

    def load(self):
        path = self._path

        if not path.exists():
            self.save()
            return

        with path.open() as file:
            data = json.load(file)

        self.guilds = {
            int(guild_id): Guild.from_dict({
                'guild_id': int(guild_id),
                **guild_data
            }) for guild_id, guild_data in data.items()
        }

    def save(self):
        self._path.write_text(json.dumps({
            guild_id: guild.to_dict()
            for guild_id, guild in self.guilds.items()
        }))
