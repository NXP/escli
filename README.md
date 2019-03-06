## escli

This is a CLI for use with [Edgescale](https://www.edgescale.org).

> Before using this tool please setup Edgescale by following instructions over on the main repo.


### Get started: Build and Install from source

This is a python package, and can be installed with python-setuptool, the package dependency(click,texttable) will be installed automatically

```
$ git clone {url_of_escli}.git
```

```
$ cd escli
```

```
$ sudo python setup.py install --record files.txt
```

### Run the CLI

The main commands supported by the CLI are:

* `escli login` - stores basic auth credentials for Edgescale
* `escli logout` - removes basic auth credentials

Help for all of the commands supported by the CLI can be found by running:

* `escli [-h, --help]`

```
Usage: escli [OPTIONS] COMMAND [ARGS]...

  CLI to interact with Edgescale server and execute your commands, default
  config file is  ~/.edgescale/cli_conf.ini

Options:
  -H, --host TEXT  edgescale host server address
  --debug          enable debug mode, default False
  -h, --help       Show this message and exit.

Commands:
  app       applications management
  builder   builder management.
  device    device register and management.
  instance  docker or application instances management
  login     login to edgescale
  logout    Logout from Edgescale
  model     model of device management.
  repo      docker's repository registry.
  solution  solution image management.
  task      service to deploy application or solution.
  vendor    manufacturer vendor management.
```

* `escli [command] [-h, --help]`

```
osc@mercrury:~$ escli app
Usage: escli app [OPTIONS] COMMAND [ARGS]...

  applications management

Options:
  -h, --help  Show this message and exit.

Commands:
  create        create a new application
  del-instance  delete the docker instance
  delete        Remove a application
  deploy        Deploy one application to device
  instance      query and list the docker instances of user
  list          List your Applications
```

### edgescale cli conf

The default configuration file is  "~/.edgescale/cli_conf.ini", modify it if needed.

```
osc@mercrury:~$ cat ~/.edgescale/cli_conf.ini
[edgescale]
host = https://api.edgescale.org
api_version = v1
```

You can customise the Dockerfile or code for any of the templates. Just create a new directory and copy in the templates folder from this repository. The templates in your current working directory are always used for builds.

See also: `escli new --help`

### Remove the escli package

```
$ cat files.txt | xargs sudo rm -rf
```
