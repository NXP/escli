#####################################
#
# Copyright 2019 NXP
#
#####################################

import sys
import json as jsn
import click
import esclicore.app as esapp
from esclicore import utils
from . import config as c


@click.group()
def instance():
    """docker or application instances management"""
    pass


@instance.command()
@click.option('--device_id', type=int, help="device's id", required=True)
@click.option('--app_id', type=int, help="applicastion's id", required=True)
@click.option('--app_version', help="applicastion's version default latest", default=None)
@click.option('--hostnet', is_flag=True, help="overvide app with  host network", default=False)

def deploy(device_id, app_id, app_version, hostnet):
    """Deploy one application to device, same as "escli app deploy". """

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/deployment/applications"}

    if device_id is None:
        click.echo("A device ID is needed.")
        sys.exit(1)

    if app_id is None:
        click.echo("A application ID is needed.")
        sys.exit(1)

    app = esapp.App(kargs)
    try:
        dict_resp= app.deploy_app_to_device(device_id, app_id, hostnet, app_version)
    except Exception as e:
        sys.exit("failed to deploy applications:  %s" %str(e))

    if dict_resp == None:
        sys.exit("failed to deploy application")

    try:
        click.echo("Success to deploy instance %s" %dict_resp['metadata']['name'])
    except Exception:
        click.echo("Success to deploy instance %s" %dict_resp['items'][0]['metadata']['name'])


@instance.command('list', short_help='query and list the docker instances of user')
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)
@click.option('--max_width', type=int, help="display max width, default 150", default=150)
def list(json, max_width):
    """query and list the docker instances"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)
    try:
        dict_resp= app.instances()
    except Exception as e:
        sys.exit("failed to query instance:  %s" %str(e))

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return

    app.print_instances(dict_resp, max_width=max_width)

@instance.command('logs', short_help='show the docker instance log')
@click.option('--name',help="docker instance name,  get name by instance list", required=True)
def logs(name):
    """show the docker instance log"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/deployment/applications"}
    app = esapp.App(kargs)
    try:
        resp= app.instance_log(name)
    except Exception as e:
        sys.exit("Failed: %s" %str(e))

    click.echo(eval(resp))

@instance.command('describe', short_help='show history and event for docker instance')
@click.option('--name',help="docker instance name,  get name by instance list", required=True)
def describe(name):
    """show history and event for the docker instances"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/deployment/applications"}
    app = esapp.App(kargs)
    try:
        resp= app.instance_history(name)
    except Exception as e:
        sys.exit("Failed: %s" %str(e))

    click.echo(eval(resp))


@instance.command('delete', short_help='delete the docker instance')
@click.option('--name',help="docker instance name,  get name by instance list", required=True)
def del_instance(name):
    """delete the docker instances"""
    if name is None:
        click.echo("docker instance name is needed.")
        sys.exit(1)
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)
    try:
        dict_resp= app.del_instance_by_name(name.split())
    except Exception as e:
        sys.exit("failed to delete instance:  %s" %str(e))

    click.echo("Success to delete")

@instance.command('reboot', short_help='reboot the docker instance, remember to backup your instance data')
@click.option('--name',help="docker instance name,  get name by instance list", required=True)
@click.option('--max_width', type=int, help="display max width", default=150)
def reboot(name, max_width):
    """reboot the docker instances"""
    if name is None:
        click.echo("docker instance name is needed.")
        sys.exit(1)
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)
    try:
        dict_resp= app.reboot_instance_by_name(name)
        app.print_instances(dict_resp, max_width=max_width)
    except Exception as e:
        sys.exit("Failed: %s" %str(e))

    click.echo("Success")



