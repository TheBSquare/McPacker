
import typing

from . import BaseLoader


def to_loader(name: str | typing.Type[BaseLoader]) -> typing.Type[BaseLoader]:
    if isinstance(name, BaseLoader) or issubclass(name.__class__, BaseLoader):
        return name

    return {
        loader.string: loader()
        for loader in BaseLoader.__subclasses__()
    }.get(name.lower())
