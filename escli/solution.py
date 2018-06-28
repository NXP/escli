#####################################
#
# Copyright 2018 NXP
#
#####################################

import sys
import json as jsn
import click
import esclicore.solution as es
from esclicore import utils
from . import config as c


@click.group()
def solution():
    """solution image management."""
    pass


@solution.command('create', short_help='create a solution image')
@click.option('--name',  help="solution name and version Eg: lsdk_solutionname1:version2", required=True)
@click.option('--image_url', help="solution image url Eg: http://sun.ap.testhost/testpath/testimgage.tgz", required=True)
@click.option('--model_id', type=int, help="model's id, escli model list", default=4, required=True)
@click.option('--public_key', help="image signed public key default null", default=None)
@click.option('--private',  is_flag=True, help="make the image as private, default False", default=False)
def create(name, image_url, model_id, public_key, private):
    """Create and upload a solution."""
    import os
    import os.path

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/solutions"}

    nl = name.split(":")
    if len(nl) != 2:
        sys.exit('Fail: name format should be as "solutionname1:version1"')

    __name = nl[0]
    __version = nl[1]

    image_name = os.path.basename(image_url)
    solution = es.Solution(kargs)

    #dict_resp = solution.create(__name, __version, model_id, image_url, not private, public_key)
    try:
        dict_resp = solution.create(__name, __version, model_id, image_url, not private, public_key)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

    if dict_resp == None:
        sys.exit("Fail: error response")

    try:
        click.echo("Success to create a solution id: %s" %(str(dict_resp["id"])))
    except Exception as e:
        sys.exit("Fail: %s %s" %(str(e), str(dict_resp)))

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit(1)

@solution.command()
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)
@click.option('--id', type=int, help="solution id, default None(list all)", default=None, show_default=True)
@click.pass_context

def list(ctx, id, json):
    """List your solution items"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/solutions"}
    if id != None:
       return ctx.invoke(show, id=id, json=json)

    solution = es.Solution(kargs)
    try:
        dict_resp= solution.list()
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

    if dict_resp == None:
        click.echo("Fail: error response")
        sys.exit(1)

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return
    try:
        solution.print_list(dict_resp)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))


@solution.command()
@click.option('--id', type=int, help="solution id", default=None, show_default=True, required=True)
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)

def show(id, json):
    """show a specific solution information (id given) same as "escli solution list --id=xxx" """

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/solutions"}
    solution = es.Solution(kargs)
    try:
        dict_resp= solution.show(id)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

    if dict_resp == None:
        click.echo("fail to get solution list")
        sys.exit(1)

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return
    try:
        solution.print_list(dict_resp)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

@solution.command()
@click.option('--id', type=int, help="solution id", default=None, show_default=True, required=True)
@click.option('--image_url', help="solution image url Eg: http://sun.ap.testhost/testpath/testimgage.tgz", required=True)
@click.option('--private',  is_flag=True, help="make the image as private, default False", default=False)
@click.pass_context

def update(ctx, id, image_url, private):
    """update solution image_url and permission """

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/solutions"}
    solution = es.Solution(kargs)
    try:
        dict_resp= solution.update(id, image_url, private)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

    if dict_resp == None:
        click.echo("fail to update solution")
        sys.exit(1)
    try:
        click.echo("Success to update solution id: %s" %(str(dict_resp["id"])))
    except Exception as e:
        sys.exit("Fail: %s %s" %(str(e), str(dict_resp)))

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit(1)


    ctx.invoke(show, id=id)

@solution.command()
@click.option('--id', help="delete according to solution id", default=None, required=True)
@click.option('--name', help="delete according to solution name", default=None)

def delete(id, name):
    """Remove solution by id or name"""
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/solutions"}

    if name != None:
        click.echo("remove solution by name is not supported yet")
        sys.exit(1)
    try:
        dict_resp= es.Solution(kargs).delete_solution_by_id(id)
    except Exception as e:
        sys.exit("failed to delete solution:  %s" %str(e))

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit("Fail: %s"%str(dict_resp))

    try:
        click.echo("Success: %s" %(str(dict_resp["message"])))
    except Exception as e:
        sys.exit("Fail: %s %s" %(str(e), str(dict_resp)))

@solution.command()
def deploy():
    """Deploy solution image to board, use "escli task deploy_solution --device_id xx --id yy" instead"""
    sys.exit('Error: use "escli task deploy-solution --device_id xx --id yy" instead')

