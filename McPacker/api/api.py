import os.path

import requests
from datetime import datetime

from McPacker.dtypes.mod import ModLink, ModVersion, Mod
from McPacker.dtypes.loader import BaseLoader
from McPacker.dtypes.search_request import SearchRequest


class Api:
    headers = {
        "User-Agent": "TheBSquare/McPacker (minka.denis@gmail.com)"
    }
    base = "https://api.modrinth.com/v2"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = self.headers

    def search(self, request: SearchRequest) -> list[Mod]:
        if request.is_one:
            mod = self.get_project(request.query, request.loader)
            return [mod]

        response = self.session.get(
            f"{self.base}/search",
            params=request.to_dict()
        )

        data = response.json()

        mods = []
        for raw_mod in data["hits"]:
            mod = Mod(
                id=raw_mod["project_id"],
                slug=raw_mod["slug"],
                author=raw_mod["author"],
                title=raw_mod["title"],
                description=raw_mod["description"],
                categories=raw_mod["categories"],
                downloads=raw_mod["downloads"],
                follows=raw_mod["follows"],
                loader=request.loader,
                client_side=raw_mod["client_side"],
                server_side=raw_mod["server_side"]
            )

            mods.append(mod)

        if not len(mods):
            mods = [
                Mod(
                    id=None,
                    slug=request.query,
                    author=None,
                    title=None,
                    description=None,
                    categories=None,
                    downloads=None,
                    follows=None,
                    loader=request.loader,
                    client_side=None,
                    server_side=None
                )
            ]

        return mods

    def get_project(self, slug, loader) -> Mod:
        response = self.session.get(
            f"{self.base}/project/{slug}"
        )

        if response.status_code != 200:
            return Mod(
                id=None,
                slug=slug,
                author=None,
                title=None,
                description=None,
                categories=None,
                downloads=None,
                follows=None,
                loader=loader,
                client_side=None,
                server_side=None
            )

        raw_mod = response.json()
        return Mod(
            id=raw_mod["id"],
            slug=raw_mod["slug"],
            author=None,
            title=raw_mod["title"],
            description=raw_mod["description"],
            categories=raw_mod["categories"],
            downloads=raw_mod["downloads"],
            follows=raw_mod["followers"],
            loader=loader,
            client_side=raw_mod["client_side"],
            server_side=raw_mod["server_side"]
        )

    def load_dependencies(self, mod: Mod) -> Mod:
        if not mod.id:
            return mod

        response = self.session.get(
            f"{self.base}/project/{mod.id}/version",
            params={
                "loaders": f"[\"{mod.loader}\"]"
            }
        )

        data = response.json()

        for version in data:
            for game_version in version["game_versions"]:
                mod.add_version(
                    ModVersion(
                        id=version["id"],
                        version=version["version_number"],
                        game_version=game_version,
                        dependencies=[
                            ModLink(
                                id=dependency["project_id"],
                                version_id=dependency["version_id"],
                                game_version_id=game_version,
                                file_name=dependency['file_name']
                            )
                            for dependency in version["dependencies"]
                        ],
                        added_date=datetime.fromisoformat(version["date_published"][:-1]).timestamp(),
                        client_side=mod.client_side,
                        server_side=mod.server_side
                    )
                )

        return mod

    def download_version(self, version: ModVersion, output: str):
        response = self.session.get(
            f"{self.base}/version/{version.id}",
        )

        data = response.json()

        files = data["files"]

        if not len(files):
            return

        filename = files[0]['filename']
        to_download = files[0]['url']

        path = os.path.join(output, filename)
        response = requests.get(to_download, allow_redirects=True)

        with open(path, "wb") as f:
            f.write(response.content)

        return path

    def download_mod_link(self, link: ModLink, loader: BaseLoader, output: str):
        if link.version_id:
            return self.download_version(
                ModVersion(
                    id=link.version_id,
                    version=None,
                    game_version=None,
                    dependencies=[],
                    added_date=0,
                    client_side=None,
                    server_side=None
                ),
                output=output
            )

        mod = self.get_project(link.id, loader)
        self.load_dependencies(mod)

        best_version = None

        for version in mod.versions:
            if version.game_version != link.game_version_id or \
                    version.game_version not in link.game_version_id or \
                    link.game_version_id not in version.game_version:
                continue

            if not best_version or best_version < version:
                best_version = version

        if not best_version:
            return None

        return self.download_version(best_version, output)
