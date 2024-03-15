import inspect
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
    def func(obj, *args, **kwargs):
        logging.debug(f"calling {c}")
        getattr(obj, c)(*args, **kwargs)

    return func

for n in ['list_files', 
          'status',
          'test_env',
          'setup_env',
          ]:

    command_name = n.replace('_', '-')

    f = click.pass_obj(bind_function(n))
    
    inspect.signature(getattr(CTAComputeClient, n))

    for p in inspect.signature(getattr(CTAComputeClient, n)).parameters.values():
        if p.name == "self":
            continue
        
        if p.default == p.empty:
            f = click.argument(p.name)(f)
        else:
            f = click.option(f"--{p.name}", default=p.default)(f)

    f = cli.command(name=command_name)(f)

if __name__ == "__main__":
    cli(obj={})