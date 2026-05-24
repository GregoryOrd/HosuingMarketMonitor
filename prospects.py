from pydantic import BaseModel
from typing import Optional

class Prospect(BaseModel):
    price: int
    addr: str
    beds: int
    baths: float
    town: str
    url: str
    postingDate: str
    listingId: str
    lat: float
    lon: float
    liked: int

    notes: str = ""
    size_sq_ft: int = 0

    def __str__(self) -> str:
        return (
            f"Prospect({self.price},{self.addr},{self.beds},"
            f"{self.baths},{self.town},{self.url},"
            f"{self.postingDate},{self.listingId},"
            f"{self.lat},{self.lon},{self.liked})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Prospect):
            return False
        return self.listingId == other.listingId
