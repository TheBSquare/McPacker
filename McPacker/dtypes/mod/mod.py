
import typing

from McPacker.utils.jsonify import Jsonified
from McPacker.dtypes.loader import BaseLoader

from . import ModVersion


class Mod(Jsonified):
    id: str
    slug: str
    author: str
    title: str
    description: str
    categories: list[str]
    downloads: int
    follows: int
    loader: typing.Type[BaseLoader]
    versions: list[ModVersion]
    client_side: str
    server_side: str

    def __init__(
        self,
        id: str,
        slug: str,
        author: str,
        title: str,
        description: str,
        categories: list[str],
        downloads: int,
        follows: int,
        loader: typing.Type[BaseLoader],
        client_side: str,
        server_side: str,
        versions: list[ModVersion] = None
    ):
        self.id = id
        self.slug = slug
        self.author = author
        self.title = title
        self.description = description
        self.categories = categories
        self.downloads = downloads
        self.follows = follows
        self.loader = loader
        self.client_side = client_side
        self.server_side = server_side
        self.versions = versions if versions else []

        self.fields = [
            "id", "slug", "author", "title",
            "description", "categories", "downloads",
            "follows", "loader", "versions",
            "client_side", "server_side"
        ]

    def __str__(self):
        return f"{self.__class__.__name__}({self.id}:{self.slug})"

    def add_version(self, version: ModVersion):
        is_game_version = False

        for i, temp_version in enumerate(self.versions):
            if temp_version.game_version != version.game_version:
                continue

            is_game_version = True

            if temp_version > version:
                continue

            del self.versions[i]
            return self.versions.append(version)

        if not is_game_version:
            return self.versions.append(version)
