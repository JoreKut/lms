from enum import Enum
from typing import Any

__all__ = ["BaseApiEnum"]


class BaseApiEnum(Enum):
    """Base ENUM model."""

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        try:
            return self.value == other.value
        except:
            pass
        try:
            if isinstance(other, str):
                return self.value == other
        except:
            pass
        return NotImplemented

    def check_equal(self, other) -> bool:
        """Use check_equal because pydantic return value of enum on
        property."""

        return self.__eq__(other)

    def __hash__(self) -> Any:
        if self.value is None:
            return hash("None")

        return hash(self.value)
