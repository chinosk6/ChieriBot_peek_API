from configobj import ConfigObj  


def readobj(filename, sect, item, default: str = ''):
    config = ConfigObj(filename, encoding='UTF8')
    try:
        res = config[sect][item]
    except:
        res = default

    return(res)

def writeobj(filename, sect, item, value):
    config = ConfigObj(filename, encoding='UTF8')
    if(sect not in config):
        config[sect] = {}

    config[sect][item] = value
 
    config.write()