import click
from . import CTAComputeClient

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = CTAComputeClient()
    ctx.obj.login()
    


@cli.command()
@click.pass_obj
def status(obj):
    print(obj.client.all_systems())


if __name__ == "__main__":
    cli(obj={})