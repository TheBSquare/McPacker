
import json
import os.path
import click

from McPacker.api import Api
from McPacker.dtypes.search_request import SearchRequest, CategoryFacet
from McPacker.dtypes.loader import to_loader
from McPacker.utils import version_to_int


@click.group()
def group():
    pass


@group.command('render', help="Command to render modpack")
@click.argument('path', type=str)
def render(path: str):
    file_name = path
    path = f"{path}.json"

    if not os.path.isfile(path):
        return print(f"Error: no such modpack in path \"{path}\"")

    print("Creating data dir")
    if not os.path.isdir(os.path.join(file_name, "info")):
        os.makedirs(os.path.join(file_name, "info"))

    try:
        data = json.load(open(path))

    except Exception as err:
        return print(f"Error: can't open modpack file \"{path}\"")

    if "mods" not in data or "loader" not in data:
        return print(f"Error: wrong modpack format it have to contain field \"mods\" and \"loader\"")

    slugs = data.pop("mods")
    loader = data.pop("loader")

    if not isinstance(slugs, list):
        return print(f"Error: \"mods\" field have to be type list")

    for slug in slugs:
        if not isinstance(slug, str):
            return print(f"Error: \"mods\" field habe to contain only type str")

    if not isinstance(loader, str):
        return print(f"Error: \"loader\" field have to be type str")

    loader = to_loader(loader)
    if not loader:
        return print(f"Error: not found such loader \"{loader}\"")

    api = Api()
    rendered_mods = []

    slugs = [slug.split("/")[-1] for slug in slugs]

    for i, slug in enumerate(slugs):
        print(f"\rRendering {i+1}/{len(slugs)} mods", end="")

        results = api.search(
            SearchRequest(
                query=slug,
                facets=[
                    CategoryFacet(values=[loader])
                ],
                is_one=True
            )
        )

        mod = api.load_dependencies(results[0])
        rendered_mods.append(mod)

    print(end="\n\n")

    raw = []
    for mod in rendered_mods:
        raw.append(mod.to_dict())

    raw_mods_path = os.path.join(
        file_name,
        "info",
        "mods.json",
    )
    with open(raw_mods_path, "w") as f:
        json.dump(raw, f)

    print(f"Creating compatibilities")

    compats = {}
    for mod in rendered_mods:
        for version in mod.versions:
            if version.game_version not in compats:
                compats.update({
                    version.game_version: []
                })

            compats[version.game_version].append({
                "name": mod.slug,
                "version": version.to_dict()
            })

    if not len(compats):
        return f"Error: can't find any compatibility"

    compats_mods_path = os.path.join(
        file_name,
        "info",
        "compatibilities.json"
    )
    with open(compats_mods_path, "w") as f:
        json.dump(compats, f)

    print("Searching best compatibility")
    best_compat = None

    for game_version in compats:
        if not best_compat:
            best_compat = {
                "version": game_version,
                "loader": str(loader),
                "mods": compats[game_version]
            }

        elif len(best_compat['mods']) < len(compats[game_version]):
            best_compat = {
                "version": game_version,
                "loader": str(loader),
                "mods": compats[game_version]
            }

        elif len(best_compat['mods']) == len(compats[game_version]) and \
                version_to_int(best_compat['version']) < version_to_int(game_version):

            best_compat = {
                "version": game_version,
                "loader": str(loader),
                "mods": compats[game_version]
            }

    print(f"Found best compatibility with {len(best_compat['mods'])}/{len(slugs)}")
    print(f"Target version: {best_compat['version']}")
    print(f"Skipped {len(slugs)-len(best_compat['mods'])} mods:")

    i = 1

    pack = [mod['name'] for mod in best_compat['mods']]
    for slug in slugs:
        if slug not in pack:
            results = api.search(
                SearchRequest(
                    query=slug,
                    facets=[
                        CategoryFacet(values=[loader])
                    ],
                    is_one=True
                )
            )

            mod = api.load_dependencies(results[0])
            rendered_mods.append(mod)

            versions = [version.game_version for version in mod.versions]
            print(f"{i}. {mod.slug}: {versions}")
            i += 1

    complete_mods_path = os.path.join(
        f"{file_name}_pack.json"
    )
    with open(complete_mods_path, "w") as f:
        json.dump(best_compat, f)
