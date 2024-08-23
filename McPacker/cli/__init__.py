
from . import render
from . import download
import click


execute = click.CommandCollection(
    sources=[
        render.group,
        download.group
    ],
    help='Use "mcpacker <command> -h/--help" to see more info about a command',
)
