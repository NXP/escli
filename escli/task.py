#####################################
#
# Copyright 2018 NXP
#
#####################################

import sys
import json as jsn
import click
import esclicore.task as estask
import esclicore.app as esapp
from esclicore import utils
from . import config as c


@click.group()
def task():
    """service to deploy application or solution."""
    pass


@task.command('deploy-app', short_help='create a task to deploy app')
@click.option('--device_id', help="device id list", default=None, required=True)
@click.option('--app_id', type=int, help="application's id", required=True)
@click.option('--app_version', help="application's version default latest", default="latest")
def deploy_app(device_id, app_id, app_version):
    """Create task to deploy application."""
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/applications"}
    versions = esapp.App(kargs).get_app_version_by_id(app_id)

    kargs.update({"url_path": "/tasks"})
    if not app_version in versions:
        sys.exit("Fail: app_version \"%s\" not found, available list：%s" \
            %(str(app_version), str(jsn.dumps(versions))))

    task = estask.Task(kargs)
    try:
        dict_resp= task.create_app_task(device_id, app_version, app_id)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

    if dict_resp == None:
        sys.exit("Fail: error response")

    try:
        click.echo("Success to create a task id: %s" %(str(dict_resp["task_id"])))
    except Exception as e:
        sys.exit("Fail: %s %s" %(str(e), str(dict_resp)))

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit(1)

@task.command('deploy-solution', short_help='create a task to deploy solution')
@click.option('--device_id', help="device id list", default=None, required=True)
@click.option('--id', type=int, help="solution's id", required=True)
def deploy_solution(device_id, id):
    """Create task to deploy solution image to a board given."""
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/tasks"}
    task = estask.Task(kargs)
    try:
        dict_resp= task.create_solution_task(device_id, id)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

    if dict_resp == None:
        sys.exit("Fail: error response")

    try:
        click.echo("Success to create a task id: %s" %(str(dict_resp["task_id"])))
    except Exception as e:
        sys.exit("Fail: %s %s" %(str(e), str(dict_resp)))

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit(1)

@task.command()
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)
@click.option('--id', type=int, help="task id, default None(list all)", default=None, show_default=True)
@click.pass_context

def list(ctx, id, json):
    """List your task items"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/tasks"}
    if id != None:
       return ctx.invoke(show, id=id, json=json)

    task = estask.Task(kargs)
    try:
        dict_resp= task.list()
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

    if dict_resp == None:
        click.echo("Fail: error response")
        sys.exit(1)

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return
    try:
        task.print_list(dict_resp)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))


@task.command()
@click.option('--id', type=int, help="task id", default=None, show_default=True, required=True)
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)

def show(id, json):
    """show a specific task information (id given) same as "escli task list --id=" """

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/tasks"}
    task = estask.Task(kargs)
    try:
        dict_resp= task.show(id)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))

    if dict_resp == None:
        click.echo("fail to get task list")
        sys.exit(1)

    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
        return

    try:
        task.print_show(dict_resp)
    except Exception as e:
        sys.exit("Fail:  %s" %str(e))


@task.command()
@click.option('--id', type=int, help="delete according to task id", default=None, required=True)
@click.option('--name', help="delete according to task name", default=None)

def delete(id, name):
    """Remove task by id or name"""
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/tasks"}

    if name != None:
        click.echo("remove task by name is not supported yet")
        sys.exit(1)
    try:
        dict_resp= estask.Task(kargs).delete_task_by_id(id)
    except Exception as e:
        sys.exit("failed to delete task:  %s" %str(e))

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit("Fail: %s"%str(dict_resp))

    try:
        click.echo("Success: %s" %(str(dict_resp["message"])))
    except Exception as e:
        sys.exit("Fail: %s %s" %(str(e), str(dict_resp)))


