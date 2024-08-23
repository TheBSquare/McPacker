
from McPacker.utils.jsonify import Jsonified
from McPacker.dtypes.loader import FabricLoader, ForgeLoader, BaseLoader, to_loader
from . import BaseFacet, CategoryFacet, ProjectTypeFacet


class SearchRequest(Jsonified):
    query: str
    facets: list[BaseFacet]
    loader: BaseLoader
    is_one: bool

    def __init__(
        self,
        query: str,
        facets: list[BaseFacet] = None,
        is_one: bool = False
    ):
        if not facets:
            facets = []

        self.query = query
        self.is_one = is_one

        self.raw_facets = facets + self.get_default_facets()
        self.facets = ''.join((
            "[", ','.join(list(map(str, self.raw_facets))), "]"
        ))

        self.loader = self._find_loader()

        self.fields = ["query", "facets"]

    def _find_loader(self):
        for facet in self.raw_facets:
            if not isinstance(facet, CategoryFacet):
                continue

            for value in facet.raw_data:
                loader = to_loader(value)

                if loader:
                    return loader

        raise ValueError("No loader specified in search request")

    def _get_default_facets(self) -> list[BaseFacet]:
        return []

    def get_default_facets(self) -> list[BaseFacet]:
        return [
            ProjectTypeFacet(values=["mod"]),
            *self._get_default_facets()
        ]


class SearchForgeRequest(SearchRequest):
    def _get_default_facets(self) -> list[BaseFacet]:
        return [
            CategoryFacet(values=[ForgeLoader()])
        ]


class SearchFabricRequest(SearchRequest):
    def _get_default_facets(self) -> list[BaseFacet]:
        return [
            CategoryFacet(values=[FabricLoader()])
        ]
