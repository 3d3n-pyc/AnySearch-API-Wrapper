from dataclasses import dataclass

@dataclass
class INFO:
    version: str
    count: int
    servers: int

@dataclass
class PatchNote:
    version: str
    data: list[str]

@dataclass
class Server:
    name: str
    results: list[str]

@dataclass
class KeyTier:
    emoji: str
    raw: str

@dataclass
class KeyStatus:
    tier: KeyTier
    expires: int
