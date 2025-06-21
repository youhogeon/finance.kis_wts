import json
import os
from dataclasses import dataclass


@dataclass
class Config:
    account_pw: str
    browser_cert_pw: str

    @classmethod
    def load_config(cls, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Configuration file '{filename}' not found.")

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return cls(**data)


CONFIG = Config.load_config("config.json")