import ConfigParser

config_path = 'ocmi.conf'
config = ConfigParser.RawConfigParser()
config.read(config_path)


def c(group, field):
    """Get configuration value"""
    return config.get(group, field)

def cs(group, field, value):
    """Set configuration value"""
    config.set(group, field, value)
    print group, field, value
    with open(config_path, 'wb') as configfile:
        config.write(configfile)

def clist(group):
    """List configuration values"""
    return config.items(group)

