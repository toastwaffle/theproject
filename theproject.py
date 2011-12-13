#!/usr/bin/env python

#Created by toastwaffle && starcube
#github.com/toastwaffle && github.com/starcube

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
sys.path.append(os.getcwd())
import gitftp
import cms
import downloader
import gobject

class Base:        
    def destroy(self, widget, data=None):
        gtk.main_quit()
        
    def btnSettingsEvent(self, widget):
        print "btnSettingsEvent entered..."

    def __init__(self):
        gobject.threads_init()
        gtk.gdk.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(350,400)
        self.window.set_title("TheProject")
        self.window.show()
        self.window.connect("destroy", self.destroy)      

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.notebook.show_tabs = True
        self.notebook.show_border = True

        self.btnSettings = gtk.Button("Settings")
        self.btnSettings.connect("clicked", self.btnSettingsEvent)
        self.btnSettings.show()
        
        self.spnWorking = gtk.Spinner()
        self.spnWorking.num_steps = 12

        self.txtStatus = gtk.Label("   ")
        self.txtStatus.show()

        self.vbox = gtk.VBox(False, 3)

        self.table = gtk.Table(1, 3, False)
        self.table.attach(self.btnSettings, 0, 1, 0, 1)
        self.table.attach(self.spnWorking, 1, 2, 0, 1)
        self.table.attach(self.txtStatus, 2, 3, 0, 1)
        self.table.show()

        self.gitftp = gitftp.GitFTP(self)
        self.cms = cms.CMS(self)
        self.downloader = downloader.Downloader(self)

        self.notebook.append_page(self.gitftp.page)
        self.notebook.set_tab_label_text(self.gitftp.page, "Git / FTP")
        
        self.notebook.append_page(self.cms.page)
        self.notebook.set_tab_label_text(self.cms.page, "Auto Installs")

        self.notebook.append_page(self.downloader.page)
        self.notebook.set_tab_label_text(self.downloader.page, "Downloader")

        self.notebook.show()
        self.vbox.pack_start(self.notebook, True, True, 0)
        self.vbox.pack_start(self.table, False, False, 0)
        self.vbox.show()
        self.window.add(self.vbox)

    def main(self):
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()

if __name__ == "__main__":
    base = Base()
    base.main()
