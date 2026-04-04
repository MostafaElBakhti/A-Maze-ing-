from dataclasses import dataclass, field

@dataclass
class Cell:
    walls: dict[str, bool] = field(

    )