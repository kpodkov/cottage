import click

from reservation.commands import reservation


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option()
def entrypoint(context: click.Context):
    try:
        context.get_usage()
    except Exception as ex:
        context.fail(f'{ex}')


entrypoint.add_command(reservation)
entrypoint()
