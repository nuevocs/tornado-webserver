from dataclasses import dataclass

@dataclass
class MeasData:
    grpid: int
    date: int
    category_id: int
    device_id: str
    type: int
    value: int
    key: str

