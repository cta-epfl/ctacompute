import click
from . import CTAComputeClient

import logging

@click.group()
@click.option('--verbose', is_flag=True)
@click.pass_context
def cli(ctx, verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    logging.debug("cli")
    ctx.obj = CTAComputeClient()
    ctx.obj.login()

def bind_function(c):
    def func(obj):
        logging.debug(f"calling {c}")
        getattr(obj, c)()

    return func

for n in ['list_files', 
          'status',
          'test_env',
          'setup_env',
          ]:

    command_name = n.replace('_', '-')

    cli.command(name=command_name)(click.pass_obj(bind_function(n)))

if __name__ == "__main__":
    cli(obj={})