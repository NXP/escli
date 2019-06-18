#####################################
#
# Copyright 2018 NXP
#
#####################################

import sys
import json as jsn
import click
import esclicore.vendor as esvdr
import esclicore.app as esapp
import esclicore.model as esmodel
from . import config as c


@click.group()
def vendor():
    """manufacturer vendor management."""
    pass


@vendor.command('create', short_help='create a new manufacturer vendor, admin is required')
@click.option('--name', help="vendor name", default=None, required=True)
def create(name):
    """Create a new manufacturer vendor."""

    if name is None:
        click.echo("A name is needed.")
        sys.exit(1)

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version']}

    try:
        dict_resp= esvdr.Vendor(kargs).create(name)
    except Exception as e:
        sys.exit(e)

    if dict_resp == None:
        sys.exit(1)

    try:
        esvdr.print_details(dict_resp)
    except Exception as e:
        sys.exit(e)

@vendor.command('list', short_help='query and show the vendor list')
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)

def list(limit, offset, json):
    """Show your vendor list"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version']}
    vendor = esvdr.Vendor(kargs)
    try:
        dict_resp= vendor.get_vendors()
    except Exception as e:
        sys.exit(e)

    if dict_resp == None:
        click.echo("fail to get vendor list")
        sys.exit(1)

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return 
    try:
        vendor.print_details(dict_resp)
    except Exception as e:
        sys.exit(e)

@vendor.command('delete', short_help="Remove a vendor by vendor id, admin is required")
@click.option('--id', type=int, help="delete according to id", default=None, required=True)

def delete(id):
    """Remove a vendor by vendor id, admin is required"""
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version']}

    if id == None:
        click.echo("vendor id is needed")
        sys.exit(1)

    try:
        dict_resp= esvdr.Vendor(kargs).delete_vendor_by_id(id)
    except Exception as e:
        sys.exit(e)

    if 'message' in dict_resp:
        print(dict_resp['message'])

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit(1)


@click.group()
def repo():
    """docker's repository registry."""
    pass

@repo.command('list', short_help='query and show the docker registry list')
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)

def list(json):
    """Show your query list"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)
    try:
        dict_resp= app.get_registry()
    except Exception as e:
        sys.exit("failed to query registry:  %s" %str(e))

    if dict_resp == None:
        click.echo("fail to get registry list")
        sys.exit(1)

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return
    try:
        app.print_registry(dict_resp)
    except Exception as e:
        sys.exit("failed to query registry:  %s" %str(e))

@repo.command('get-login')
@click.option('-y', '--yes', is_flag=True, help="Assume yes to questions", default=False)

def get_login(yes):
    """get a docker command to login edgescale registry with username 
       and password.
    """
    click.echo("*** The previous docker login token will be expired")
    if not yes and not click.confirm('*** Do you want to continue?'):
        sys.exit(0)

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    app = esapp.App(kargs)
    try:
        dict_resp= app.get_registry_login()
    except Exception as e:
        sys.exit("failed: %s" %str(e))

    if 'status' in dict_resp and dict_resp['status'] == 'success':
        click.echo("*** Command to login edgescale registry:\n\t %s" %dict_resp['cmd'])
    else:
        sys.exit("failed to get login command")


@click.group()
def model():
    """model of device management."""
    pass

@model.command('list', short_help='query and show the available model list')
@click.option('--id', type=int, help='model ID', default=None)
@click.option('--limit', type=int, help="display item number", default=20, show_default=True)
@click.option('--offset', type=int, help="item offset from which to show", default=0, show_default=True)
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)

def list(id, limit, offset, json):
    """Show your model list"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/models"}
    kargs['params'] = {"limit": limit, "offset": offset}
    if id != None:
        kargs["url_path"] = "/models/%s" %(str(id))

    model = esmodel.Model(kargs)
    try:
        dict_resp= model.get_models()
    except Exception as e:
        sys.exit("failed to query models:  %s" %str(e))

    if dict_resp == None:
        click.echo("fail to get models list")
        sys.exit(1)

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return
    try:
        model.print_details(dict_resp)
    except Exception as e:
        sys.exit("failed:  %s" %str(e))

@model.command('create', short_help='Create new model name, Eg: yun-ls1043a-gateway-nxp')
@click.option('--name', help='model name', required=True)
@click.option('--public', is_flag=True, help="create model as public, default False", default=False)
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)
def create(name, public, json):
    """Create new model name, Eg: yun-ls1043a-gateway-nxp"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/models"}
    model = esmodel.Model(kargs)
    try:
        dict_resp= model.create(name, public)
    except Exception as e:
        sys.exit("Model create Error: %s" %str(e))

    if dict_resp == None:
        click.echo("Fail to create")
        sys.exit(1)

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return

    if 'id' in dict_resp:
        click.echo("Success: %s id %s Created" %(name, dict_resp['id']))

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit(1)

@model.command('update')
@click.option('--id', type=int, help='model ID', required=True)
@click.option('--name', help='model name', required=True)
def update(id, name):
    """Update model with a new name"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/models"}
    model = esmodel.Model(kargs)
    try:
        dict_resp= model.update(id, name)
    except Exception as e:
        sys.exit("Error: %s" %str(e))

    if dict_resp == None:
        click.echo("Unkonw error: try --debug")
        sys.exit(1)

    if 'status' in dict_resp and dict_resp['status'].lower() == 'success':
        click.echo("Success to update")
        return

    if 'message' in dict_resp:
        print(dict_resp['message'])


@model.command('delete')
@click.option('--id', type=int, help='model ID', required=True)
def delete(id):
    """Delete model by ID"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/models"}
    model = esmodel.Model(kargs)
    try:
        dict_resp= model.delete_model_by_id(id)
    except Exception as e:
        sys.exit("Error: %s" %str(e))

    if dict_resp == None:
        click.echo("Unkonw error: try --debug")
        sys.exit(1)

    if 'status' in dict_resp and dict_resp['status'].lower() == 'success':
        click.echo("Success to delete")
        return

    if 'message' in dict_resp:
        print(dict_resp['message'])
        sys.exit(1)

