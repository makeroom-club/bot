import json
import pathlib
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    filename: str
    welcome_message_id: Optional[int] = None

    def __post_init__(self):
        self._path = pathlib.Path(self.filename)

    def load(self):
        path = self._path

        if not path.exists():
            self.save()
            return

        with path.open() as file:
            data = json.load(file)

        self.welcome_message_id = data['welcome_message_id']

    def save(self):
        path = self._path

        with path.open('w') as file:
            json.dump(
                {
                    'welcome_message_id': self.welcome_message_id,
                },
                file
            )
