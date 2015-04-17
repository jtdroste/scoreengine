import ConfigParser

"""
Taken from https://wiki.python.org/moin/ConfigParserExamples
"""
def getConfig(file, section):
    bool_list = ['raise_on_warnings', 'buffered', 'ip_changing', 'logging']
    int_list = ['interval']
    
    dict1 = {}
    
    Config = ConfigParser.ConfigParser()
    Config.read(file)
    options = Config.options(section)
    for option in options:
        if option in bool_list:
            dict1[option] = Config.getboolean(section, option)
        elif option in int_list:
            dict1[option] = Config.getint(section, option)
        else:
            dict1[option] = Config.get(section, option)
    
    return dict1

