#####################################
#
# Copyright 2018 NXP
#
#####################################

import sys
import json as jsn
import click
import esclicore.builder as esb
from esclicore import utils
from . import config as c

@click.group()
def builder():
    """builder management."""
    pass

@builder.command('list-projects', short_help='list all the build projects.')
@click.option('--orderBy', type=click.Choice(["name", "status", "created", "updated"]), default="name")
@click.option('--status', type=click.Choice(["all", "InProgress", "Succeeded", "Failed", "Pended"]), default="all")

def list_projects(orderby, status):
    """list your build projects"""

    filters={'orderby': orderby, "status": status}
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/builder", "params": filters}
    try:
        dict_resp= esb.Builder(kargs).get_projects()
    except Exception as e:
        sys.exit("failed to query projects:  %s" %str(e))
    print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    if dict_resp == None:
        click.echo("failed to get project list")
        sys.exit(1)
    
@builder.command('list-environments', short_help='list all the build environments.')

def list_environments():
    """list your build environments"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/builder"}
    try:
        dict_resp= esb.Builder(kargs).get_environments()
    except Exception as e:
        sys.exit("failed to query environments:  %s" %str(e))
    print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    if dict_resp == None:
        click.echo("failed to get environment list")
        sys.exit(1)
    
@builder.command('list-repositories', short_help='list all the build repositories.')

def list_repositories():
    """list your build repositories"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/builder"}
    try:
        dict_resp= esb.Builder(kargs).get_repositories()
    except Exception as e:
        sys.exit("failed to query repositories:  %s" %str(e))
    print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    if dict_resp == None:
        click.echo("failed to get repositorie list")
        sys.exit(1)

@builder.command('get-project', short_help='gets information about build project.')
@click.option('--name', help="project name", prompt="Project name: ", default='', required=True)

def get_project(name):
    """gets information about build project"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/builder"}
    try:
        dict_resp= esb.Builder(kargs).query_project(name)
    except Exception as e:
        sys.exit("failed to query project:  %s" %str(e))
    print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    if dict_resp == None:
        click.echo("failed to get project details")
        sys.exit(1)

@builder.command('create-project', short_help='create a new build project.')
@click.option('--name', help="project name", prompt="Project name: ", default="", required=True)
@click.option('--image', help="environment image", prompt="Environment image: ", default="", required=True)
@click.option('--source', help="source location", prompt="Source location: ", default="", required=True)
@click.option('--description', help="project description", default="")
@click.option('--auto-poll/--no-auto-poll', help="poll for source changes automatically", default=False)
@click.option('--timeout', help="timeout in minutes", default=40)

def create_project(name, image, source, description, auto_poll, timeout):
    """create a new build project"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/builder"}
    if not name:
        sys.exit("name can't be empty.")
    if not image:
        sys.exit("image can't be empty. Try 'escli builder list-envrionments'")
    if not source:
        sys.exit("source can't be empty.")
    if auto_poll:
        pollForSourceChanges = "true"
    else:
        pollForSourceChanges = "false"
    try:
        dict_resp= esb.Builder(kargs).create_project(name, image, source, description, pollForSourceChanges, timeout)
    except Exception as e:
        sys.exit("failed to create project:  %s" %str(e))
    print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    if dict_resp == None:
        click.echo("failed to create new project")
        sys.exit(1)

@builder.command('update-project', short_help='update a build project.')
@click.option('--name', help="project name", prompt="Project name: ", default="", required=True)
@click.option('--image', help="environment image", prompt="Environment image: ", default="", required=True)
@click.option('--source', help="source location", prompt="Source location: ", default="", required=True)
@click.option('--description', help="project description", default="")
@click.option('--auto-poll/--no-auto-poll', help="poll for source changes automatically", default=False)
@click.option('--timeout', help="timeout in minutes", default=40)

def update_project(name, image, source, description, auto_poll, timeout):
    """update a build project"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/builder"}
    if not name:
        sys.exit("name can't be empty.")
    if not image:
        sys.exit("image can't be empty. Try 'escli builder list-envrionments'")
    if not source:
        sys.exit("source can't be empty.")
    if auto_poll:
        pollForSourceChanges = "true"
    else:
        pollForSourceChanges = "false"
    try:
        dict_resp= esb.Builder(kargs).update_project(name, image, source, description, pollForSourceChanges, timeout)
    except Exception as e:
        sys.exit("failed to update project:  %s" %str(e))
    print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    if dict_resp == None:
        click.echo("failed to update project")
        sys.exit(1)

@builder.command('delete-project', short_help='delete build project.')
@click.option('--name', help="project name", prompt="Project name: ", default='', required=True)

def delete_project(name):
    """delete build project"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/builder"}
    try:
        dict_resp= esb.Builder(kargs).delete_project(name)
    except Exception as e:
        sys.exit("failed to delete project:  %s" %str(e))
    print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    if dict_resp == None:
        click.echo("failed to delete project")
        sys.exit(1)

@builder.command('start-project-build', short_help='start build project.')
@click.option('--name', help="project name", prompt="Project name: ", default='', required=True)

def start_project_build(name):
    """start build project"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/builder"}
    try:
        dict_resp= esb.Builder(kargs).start_project_build(name)
    except Exception as e:
        sys.exit("failed to start project:  %s" %str(e))
    print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    if dict_resp == None:
        click.echo("failed to start project")
        sys.exit(1)

