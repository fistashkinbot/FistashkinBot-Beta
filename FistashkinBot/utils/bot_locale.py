import disnake
from pathlib import Path
from typing import Self, Optional
import json


class BotLocal:
    def __init__(self, key: str) -> Self:
        self.key = key

    @property
    def load(self) -> dict[disnake.Locale, Optional[str]]:
        data: dict = {}
        for key in Path("./localization/").glob("*.json"):
            if disnake.Locale.__members__.get(key.stem):
                data[disnake.Locale[key.stem]] = key.stem
                with key.open(encoding="utf-8") as file:
                    load: dict[str, str] = json.load(file) or {}
                data[disnake.Locale[key.stem]] = load.get(self.key) or self.key
            continue
        return data

    def get(self, local: disnake.Locale) -> Optional[str]:
        return self.load.get(local) or self.load.get(disnake.Locale.en_US)

    @property
    def get_localized(self) -> disnake.Localized:
        load = self.load
        return disnake.Localized(string=load.get(disnake.Locale.en_US), data=load)

    @property
    def __len__(self) -> int:
        return len(self.load.keys())

    @property
    def __bool__(self) -> bool:
        return len(self.load) != 0