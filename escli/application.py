#####################################
#
# Copyright 2018 NXP
#
#####################################

import sys
import json as jsn
import click
import esclicore.app as esapp
from esclicore import utils
from . import config as c


@click.group()
def app():
    """applications management"""
    pass


@app.command('create', short_help='create a new application')
@click.option('--name',  help="application name to be created", required=True)
@click.option('--image_name', help="docker image name eg: media_server:latest", required=True)
#@click.option('--version',  help="application version default 1806", default="1806")
@click.option('--vendor_id',  type=int, help="vendor_id default null", default=None)
@click.option('--commands',  help="docker application command default null", default="")
@click.option('--cmdargs',  help="args of application command default null", default="")
@click.option('--pic',  help="application skin picture file default null", default="")
@click.option('--description', help="Description, default null", default="")
def create(name, image_name, vendor_id, commands, cmdargs, pic, description):
    """Create a new Application."""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)

    registry_id = 0
    m_list = app.get_registry()['mirrors']
    for m in m_list:
        if m['name'] == "hub.docker.com":
            registry_id = m['id']

    input_mirror = image_name.split('/')[0]
    for m in m_list:
        if m['name'] == input_mirror:
            registry_id = m['id']

    # Gen image name and version/tag
    nl =  image_name.split(':')
    if len(nl) != 2:
        sys.exit("wrong image format, see help")
    _image_name = nl[0]
    _image_version = nl[1]

    click.echo("Image info: %s %s:%s" %(str(registry_id), _image_name, _image_version))

    try:
        dict_resp= app.create(name, registry_id, _image_name, _image_version, \
                vendor_id, pic, commands, cmdargs, description)
    except Exception as e:
        sys.exit("failed to create applications:  %s" %str(e))

    if dict_resp == None:
        click.echo("fail to create application")
        sys.exit(1)

    click.echo("Success to create application %s" %name)

@app.command()
@click.option('--id', type=int, help="applicastion's id default None(list all applications)", default=None)
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)
@click.pass_context
def list(ctx, id, json):
    """List your Applications"""

    if id != None:
        return ctx.invoke(show, id=id)

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)
    try:
        dict_resp= app.query_apps()
    except Exception as e:
        sys.exit("failed to query applications:  %s" %str(e))

    if dict_resp == None:
        click.echo("fail to get application list")
        sys.exit(1)

    if not 'applications' in dict_resp:
        sys.exit("error result: %s" %str(dict_resp))

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return
    try:
        app.print_details(dict_resp)
    except Exception as e:
        sys.exit("failed to print applications:  %s" %str(e))

@app.command()
@click.option('--id', type=int, help="applicastion's id", required=True)

def show(id):
    """query and show specific application (id given) same as "escl app list --id xx" """

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)
    try:
        dict_resp= app.show(id)
    except Exception as e:
        sys.exit("Fail applications:  %s" %str(e))

    if dict_resp == None:
        sys.exit("Fail: response format error")
    try:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    except Exception as e:
        sys.exit("Fail Application:  %s" %str(e))

@app.command()
@click.option('--device_id', type=int, help="device's id", required=True)
@click.option('--app_id', type=int, help="applicastion's id", required=True)
@click.option('--app_version', help="applicastion's version default latest", default=None)
@click.option('--hostnet', is_flag=True, help="overvide app with  host network", default=False)

def deploy(device_id, app_id, app_version, hostnet):
    """Deploy one application to device"""

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


@app.command()
@click.option('--id', type=int, help="delete according to application id", required=True)

def delete(id):
    """Remove a application"""
    if id is None:
        click.echo("A application ID is needed.")
        sys.exit(1)

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)
    try:
        dict_resp= app.delete_app_by_id(id)
    except Exception as e:
        sys.exit("failed to delete instance:  %s" %str(e))

    click.echo("Success to delete")

@app.command('instance', short_help='query and list the docker instances of user')
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)
def instance(json):
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

    app.print_instances(dict_resp)

@app.command('del-instance', short_help='delete the docker instance')
@click.option('--name', help="delete according to docker instance name", default=None, required=True)
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






