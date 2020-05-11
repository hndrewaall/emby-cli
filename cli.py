import sys

import click


@click.group()
def cli():
    pass


@cli.command("get-policy")
@click.argument("user", type=str)
def get_policy(user: str):
    pass


if __name__ == "__main__":
    sys.exit(cli())
