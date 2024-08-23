
import click
import os
import json

from McPacker.api import Api
from McPacker.dtypes.loader import to_loader
from McPacker.dtypes.search_request import SearchRequest, CategoryFacet
from McPacker.dtypes.mod import Mod, ModVersion, ModLink


@click.group()
def group():
    pass


@group.command('download', help="Command to download modpack")
@click.argument('path', type=str)
@click.argument("side", type=str)
def download(path: str, side: str):
    if side.lower() not in ["server", "client"]:
        return print(f"Error: side have to be \"server\" or \"client\", got \"{side}\"")

    file_name = path
    path = f"{path}_pack.json"

    if not os.path.isfile(path):
        return print(f"Error: no such modpack in path \"{path}\"")

    print("Creating data dir")
    output_dir = os.path.join(file_name.replace('_pack', ''), side.lower(), "mods")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    try:
        data = json.load(open(path))

    except Exception as err:
        return print(f"Error: can't open modpack file \"{path}\"")

    api = Api()

    loader = to_loader(data["loader"])
    mods = data["mods"]

    downloaded_dependencies = []

    for mod in mods:
        version = mod["version"]

        version = ModVersion(
            id=version["id"],
            version=version["version"],
            game_version=version["game_version"],
            dependencies=[
                ModLink(
                    id=dependency["id"],
                    version_id=dependency["version_id"],
                    game_version_id=dependency["game_version_id"],
                    file_name=dependency["file_name"]
                )
                for dependency in version["dependencies"]
            ],
            added_date=version["added_date"],
            client_side=version["client_side"],
            server_side=version["server_side"]
        )

        if side == "server" and version.server_side == "unsupported":
            print(f"skipping mod {mod['name']} that is not supported server side")
            continue

        elif side == "client" and version.client_side == "unsupported":
            print(f"skipping mod {mod['name']} that is not supported client side")
            continue

        downloaded = api.download_version(version, output_dir)
        print(f"Downloaded mod: {downloaded}")

        for dependency in version.dependencies:
            if dependency.id in downloaded_dependencies:
                continue

            downloaded_dependencies.append(dependency.id)
            downloaded = api.download_mod_link(dependency, loader, output_dir)

            if downloaded:
                print(f"Downloaded dependency: {downloaded}")

            else:

                result = api.search(
                    SearchRequest(
                        query=dependency.id,
                        facets=[
                            CategoryFacet(values=[loader])
                        ],
                        is_one=True
                    )
                )
                dependency_mod = api.load_dependencies(result[0])
                versions = [version.game_version for version in dependency_mod.versions]

                print(f"Can't find compatible dependency version {dependency_mod.slug}, avaible: {versions}")

        print()
