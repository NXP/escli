#####################################
#
# Copyright 2018 NXP
#
#####################################

import click
import logging
from . import user
from . import device
from . import app
from . import mix
from . import task
from . import builder
from . import solution
from . import instance
from . import config as c

log = logging.getLogger("")


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-H', '--host', default='', help='edgescale host server address')
@click.option('--debug',is_flag=True, default=False, help='enable debug mode, default False')

def cli(host, debug):
    """
    CLI to interact with Edgescale server and execute your commands,
    default config file is  ~/.edgescale/cli_conf.ini
    """

    c.cfg  = c.load_cfg()
    if host != '':
        c.cfg['host'] = host

    if debug:
        log.setLevel(logging.DEBUG)

def add_commands(cli):
    cli.add_command(user.login)
    cli.add_command(user.logout)
    cli.add_command(device)
    cli.add_command(app)
    cli.add_command(task)
    cli.add_command(solution)
    cli.add_command(instance)
    cli.add_command(builder)
    cli.add_command(mix.vendor)
    cli.add_command(mix.repo)
    cli.add_command(mix.model)

add_commands(cli)
