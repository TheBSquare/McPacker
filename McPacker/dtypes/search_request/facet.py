
from McPacker.utils.jsonify import JsonifiedProperty


class BaseFacet(JsonifiedProperty):
    prefix = "base"

    def __init__(self, values: list[str]):
        if not isinstance(values, list):
            values = [values]

        self.raw_data = values
        self.data = ''.join((
            "[",
            ','.join(list(map(
                lambda x: f"\"{self.prefix}:{x}\"",
                self.raw_data
            ))),
            "]"
        ))

        self.field = "data"

    def __str__(self):
        return self.data


class ProjectTypeFacet(BaseFacet):
    prefix = "project_type"


class CategoryFacet(BaseFacet):
    prefix = "categories"


class VersionsFacet(BaseFacet):
    prefix = "versions"


class ClientSideFacet(BaseFacet):
    prefix = "client_side"


class ServerSideFacet(BaseFacet):
    prefix = "server_side"


class OpenSourceFacet(BaseFacet):
    prefix = "open_source"


class TitleFacet(BaseFacet):
    prefix = "title"


class AuthorFacet(BaseFacet):
    prefix = "author"


class FollowsFacet(BaseFacet):
    prefix = "follows"


class ProjectIdFacet(BaseFacet):
    prefix = "project_id"


class LicenseFacet(BaseFacet):
    prefix = "license"


class DownloadsFacet(BaseFacet):
    prefix = "downloads"


class ColorFacet(BaseFacet):
    prefix = "color"


class CreatedTimestampFacet(BaseFacet):
    prefix = "created_timestamp"


class ModifiedTimestampFacet(BaseFacet):
    prefix = "modified_timestamp"
