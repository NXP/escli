#####################################
#
# Copyright 2018 NXP
#
#####################################

import os
import sys
import click
import logging
import esclicore.user as user
import esclicore.device as device
from . import config as c



@click.command('login', short_help='login to edgescale')

@click.option('--username', '-u', prompt="Your username", help="user name", default=None)
@click.option('--password', '-p', prompt="Please input user's Password", hide_input=True, help="user password")


def login(username, password):
    """
    Login with username and password.

    Save the token inside `~/edgescale/token.txt`
    """
    if username is None:
        click.echo("user name is needed")
        sys.exit(1)

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version']}
    try:
        user.login(kargs, username=username, password=password)
    except Exception as e:
        sys.exit(e)
        
    click.secho("Success to login", fg='green', bold=True)

@click.command('logout', short_help='Logout from Edgescale')
def logout():
    """Logout and remove the token."""
    try:
       user.logout()
    except Exception as e:
        sys.exit(e)
    #click.secho("Logged out :)", fg='green', bold=True)
