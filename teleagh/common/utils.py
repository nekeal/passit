from enum import Enum
from typing import List, Tuple


class CustomEnum(Enum):

    def __str__(self) -> str:
        return self.name

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(tag.name, tag.value) for tag in cls]


def setup_view(view, request, *args, **kwargs):
    """
    Initializes generic view or viewset with passed params
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
