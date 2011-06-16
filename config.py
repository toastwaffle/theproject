'''
config.py
Author: Samuel Littley

Provides class Config for saving and accessing configuration for project
'''

import os
import xml.dom.minidom as minidom

class Config():
    def __init__(self,xmlpath):
        try:
            if os.path.exists(xmlpath):
                self.configfile = minidom.parse(open(xmlpath,'w+'))
            else:
                self.configfile = self.create_config_file(xmlpath)            
        except IOError:
            print "Could not open config file"

    def create_config_file(self,xmlpath):
        try:
            configfile = open(xmlpath,'w+')
        except IOError:
            print "Could not create config file"
        impl = minidom.getDOMImplementation()
        newconf = impl.createDocument(None, "theproject", None)
        top_element = newconf.documentElement
        config = newconf.createElement("config")
        config = top_element.appendChild(config)
        gitsection = config.appendChild(newconf.createElement("section_git"))
        ftpsection = config.appendChild(newconf.createElement("section_ftp"))
        instsection = config.appendChild(newconf.createElement("section_inst"))
        dwldsection = config.appendChild(newconf.createElement("section_dwld"))
        gitsection.appendChild(newconf.createElement("defaultprofile"))
        gitsection.appendChild(newconf.createElement("profiles"))
        ftpsection.appendChild(newconf.createElement("defaultprofile"))
        ftpsection.appendChild(newconf.createElement("profiles"))
        instsection.appendChild(newconf.createElement("defaultprofile"))
        instsection.appendChild(newconf.createElement("configpath"))
        instsection.appendChild(newconf.createElement("profiles"))
        dwldsection.appendChild(newconf.createElement("dwldlocation"))
        newconf.writexml(configfile,indent="",addindent="\t",newl="\n")
        return newconf

    def get_parsed_xml(self);
        return self.configfile
