from dataclasses import asdict, dataclass


@dataclass
class RecipeType:
    title: str
    description: str
    author_id: int
    image_url: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)
