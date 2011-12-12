#!/usr/bin/env python

#Created by toastwaffle && starcube
#github.com/toastwaffle && github.com/starcube

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
sys.path.append(os.getcwd())
import ftplib

class CMS:
    def __init__(self,parent):
        self.cboInstallPresets = gtk.combo_box_new_text()
        self.cboInstallPresets.append_text("Wordpress")
        self.cboInstallPresets.append_text("Contao")
        self.cboInstallPresets.append_text("Joomla")
        self.cboInstallPresets.append_text("CMS Made Simple")
        self.cboInstallPresets.set_active(0)
        self.cboInstallPresets.show()
        
        self.table = gtk.Table(1, 2, False)
        self.table.attach(self.cboInstallPresets, 0, 1, 0, 1)
        self.table.show()
        
        self.vbox = gtk.VBox(False, 3)
        self.vbox.pack_start(self.table, True, False, 0)
        self.vbox.show()

        self.page = gtk.Frame()
        self.page.add(self.vbox)
        self.page.show()
