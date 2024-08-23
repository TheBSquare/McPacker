
from McPacker.utils.jsonify import Jsonified


class ModLink(Jsonified):
    id: str
    version_id: str
    game_version_id: str
    file_name: str

    def __init__(self, id: str, version_id: str, game_version_id: str, file_name: str):
        self.id = id
        self.version_id = version_id
        self.game_version_id = game_version_id
        self.file_name = file_name

        self.fields = ["id", "version_id", "game_version_id", "file_name"]
