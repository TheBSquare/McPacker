
from datetime import datetime, date

from McPacker.utils.jsonify import Jsonified
from McPacker.utils import version_to_int
from . import ModLink


class ModVersion(Jsonified):
    id: str
    version: str
    game_version: str
    dependencies: list[ModLink]
    added_date: int
    client_side: str
    server_side: str

    def __init__(
        self,
        id: str,
        version: str,
        game_version: str,
        dependencies: list[ModLink],
        added_date: int,
        client_side: str,
        server_side: str
    ):

        self.id = id
        self.version = version
        self.game_version = game_version
        self.dependencies = dependencies
        self.added_date = added_date
        self.client_side = client_side
        self.server_side = server_side

        self.fields = [
            "id", "version", "game_version", "dependencies", "added_date",
            "client_side", "server_side"
        ]

    def __int__(self):
        return version_to_int(self.version)

    def __str__(self):
        return f"{self.__class__.__name__}({self.id}:{self.version}:{self.game_version})"

    def __lt__(self, other):
        return self.added_date < other.added_date

    def __eq__(self, other):
        return self.added_date == other.added_date
