#####################################
#
# Copyright 2018 NXP
#
#####################################

import sys
import base64
import json as jsn
import click
import esclicore.device as esdev
from esclicore import utils
from . import config as c


@click.group()
def device():
    """device register and management."""
    pass


@device.command('create', short_help='create a new device.')
@click.option('--description', '-d', help="Description", default=None)
@click.option('--fuid',  help="device's fuid", default=None, required=True)
@click.option('--model_id', type=int, help="device model's id", required=True)
@click.pass_context
def create(ctx, description, fuid, model_id):
    """Create a new API."""
    if fuid is None:
        click.echo("A device fuid is needed.")
        sys.exit(1)

    if model_id is None:
        click.echo("A device model is needed.")
        sys.exit(1)

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/est/device"}
    fuid_uid = esdev.Device(kargs).fuid_to_uid(fuid)

    kargs["url_path"] = "/devices"
    kargs['request_body'] = {
        'device': {'fuid': fuid_uid, 'model_id': model_id}
    }
    try:
        dict_resp= esdev.Device(kargs).create_device()
    except Exception as e:
        sys.exit("failed to create device:  %s" %str(e))

    if dict_resp == None:
        sys.exit(1)

    if 'message' in dict_resp:
        print(dict_resp['message'])

    if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
        sys.exit(1)
    try:
        click.echo("device %s created success" %(dict_resp["name"]))
        #dict_resp= esdev.Device(kargs).query_device_by_id(dict_resp["id"])
        esdev.print_device_details(dict_resp)

    except Exception as e:
        sys.exit("failed to get device info:  %s" %str(e))

    return ctx.invoke(get_cert, name=dict_resp["name"])

@device.command()
@click.option('--id', type=int, help="same as escl device show --id=yy", default=None)
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)
@click.pass_context
def list(ctx, id, json):
    """List your Devices"""

    if id !=None:
        return ctx.invoke(show, id=id, json=json)

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/devices"}
    try:
        dict_resp= esdev.Device(kargs).get_devices()
    except Exception as e:
        sys.exit("failed to query device:  %s" %str(e))

    if dict_resp == None:
        click.echo("fail to get device list")
        sys.exit(1)

    if not 'results' in dict_resp:
        sys.exit("error result: %s" %str(dict_resp))

    # Output with default format
    if json:
        esdev.print_device_json(dict_resp)
    else:
        esdev.print_device(dict_resp)


@device.command()
@click.option('--id', type=int, help="device id", default=None, required=True)
@click.option('--json', is_flag=True, help="output format, json or default summary format", default=False)

def show(id, json):
    """show device information"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/devices"}
    try:
        dict_resp= esdev.Device(kargs).query_device_by_id(id)
    except:
        sys.exit(1)

    if dict_resp == None:
        click.echo("fail to get device list")
        sys.exit(1)

    if not 'device_info' in dict_resp:
        sys.exit("error result: %s" %str(dict_resp))

    # Output with default format
    if json:
        print(jsn.dumps(dict_resp, sort_keys=True, indent=4))
    else:
        esdev.print_device_details(dict_resp)


@device.command()
@click.option('--id', type=int, help="delete according to device id", default=None, required=True)
@click.option('--name', help="delete according to device name", default=None)

def delete(id, name):
    """Remove device by id or name"""
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/devices"}

    if name != None:
        click.echo("remove device by name is not supported yet")
        sys.exit(1)

    try:
        dict_resp= esdev.Device(kargs).delete_device_by_id(id)
    except Exception as e:
        sys.exit("failed to delete device:  %s" %str(e))

    try:
        if "success" in  dict_resp['status'].lower():
            click.echo("%s" %dict_resp["message"])
    except Exception as e:
        sys.exit("failed to delete device: %s" %str(e))

    # comments it because reset API have BUG
    #esdev.print_device_details(dict_resp)

@device.command('get-cert')
@click.option('--id', type=int, help="get device certification according to device id", default=None)
@click.option('--name', help="get device certification according to device name", default=None, required=True)

def get_cert(id, name):
    """Get device private key & certifcation by device id or device name"""
    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/devices/certificates"}

    if id != None:
        click.echo("id is not supported yet")
        sys.exit(1)
    try:
        click.echo("Generating device certification data")
        resp= esdev.Device(kargs).get_device_cert(name)
    except Exception as e:
        sys.exit("failed to get device certification:  %s" %str(e))

    certfile = name + ".sh"
    with open(certfile, "w+") as f:
        f.write(eval(resp))
    click.echo("Success: saved certification data to %s" %certfile)
    click.echo("Install it to device SD card with command:\n\t # sh %s\n" %certfile)

@device.command("upload-db")
@click.option('-f', type=click.File(), help="csv format db file, a example file: example/dev_db.csv", required=True)
def upload_db(f):
    """upload device db to cloud"""

    kargs={'host': c.cfg['host'], "api_version": c.cfg['api_version'], "url_path": "/enroll/device"}

    ret = 0
    click.echo("uploading", nl=False)
    while True:
        data = ''
        lines = f.readlines(10000)
        if not lines:
            break
        for line in lines:
            if "fuid" in line.lower() and "oemid" in  line.lower():
                continue
            if len(line) < 20:
                click.echo("\n item: %s too short, should > 20 character,skip it\n" %line, nl=False)
                continue
            if line.count(',') != 3:
                sys.exit("\ncsv db format error, should be: \"FUID,OEMID,SK_PUB_X,SK_PUB_Y\"\n")
            data += line
        #print len(data)
        click.echo("...", nl=False)
        data64 = base64.b64encode(data)
        try:
            dict_resp= esdev.Device(kargs).upload_device_db(data64)
        except Exception as e:
            sys.exit("Fail: %s" %str(e))

        click.echo("", nl=False)

        if 'status' in dict_resp and dict_resp['status'].lower() != 'success':
            ret = ret + 1
    if ret != 0:
        click.echo("FAIL")
    else:
        click.echo("Success")
    sys.exit(ret)
