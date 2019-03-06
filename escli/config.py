#####################################
#
# Copyright 2018 NXP
#
#####################################

import os
try:
    import ConfigParser as configparser
except:
    import configparser


cfgfile = os.path.expanduser("~/.edgescale/") + "cli_conf.ini"
config = configparser.RawConfigParser()
cfg={}

def create_default_cfg(cfgfile):

    config.add_section('edgescale')

    config.set('edgescale', 'host', "https://api.edgescale.org")
    config.set('edgescale', 'api_version', "v1")

    with open(cfgfile, 'wb') as configfile:
        config.write(configfile)
    
def load_cfg():

    if not os.path.exists(os.path.dirname(cfgfile)):
        try:
            os.makedirs(os.path.dirname(cfgfile))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise Exception("create %s" %cfgfile) 
    # Whether cfgfile exists
    try:
        fn = open(cfgfile, 'r') 

    # Ceate and save the default value into conf file
    except:
        create_default_cfg(cfgfile) 

    config.read(cfgfile)
    for section in config.sections():
        for option in config.options(section):
            #print option
            cfg[option] = config.get(section, option)

    return cfg


if __name__ == '__main__':
    print(load_cfg())
