
from McPacker.utils.jsonify import JsonifiedProperty


class BaseLoader(JsonifiedProperty):
    string: str = "base_loader"

    def __init__(self):
        self.string = self.string
        self.field = "string"

    def __str__(self):
        return self.string


from .loader import ForgeLoader, FabricLoader
from .utils import to_loader
