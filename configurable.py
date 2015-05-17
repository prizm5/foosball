import ConfigParser
import os.path


__author__ = 'nilscreque'


class Configurable(object):
    def __init__(self, fname='pusher.ini'):
        if os.path.isfile(fname):
            self.Config = ConfigParser.ConfigParser()
            self.Config.read(fname)
        else:
            raise 'config not found'

    def ConfigSectionMap(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1
