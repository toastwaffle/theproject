#!/usr/bin/env python

#Created by toastwaffle && starcube
#github.com/toastwaffle && github.com/starcube

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
sys.path.append(os.getcwd())
import urllib2

class Downloader:
    def btnDownloadEvent(self, widget):
        urlfile = urllib2.urlopen(self.edtDownloadLocation.get_text())
        data_list = []
        chunk = 4096
        while 1:
            data = urlfile.read(chunk)
            if not data:
                print "done."
                break
            data_list.append(data)
            self.prgbDownload.set_text("Read %s bytes"%len(data))

    def __init__(self,parent):
        self.parent = parent
        
        self.prgbDownload = gtk.ProgressBar(adjustment=None)
        self.prgbDownload.show()

        self.edtDownloadLocation = gtk.Entry()
        self.edtDownloadLocation.show()

        self.lblDownloadLocation = gtk.Label("Download location: ")
        self.lblDownloadLocation.show()

        self.btnDownload = gtk.Button("Download")
        self.btnDownload.connect("clicked", self.btnDownloadEvent)
        self.btnDownload.show()

        self.vbox = gtk.VBox(False, 3)
        self.vbox.pack_start(self.lblDownloadLocation, True, False, 0)
        self.vbox.pack_start(self.edtDownloadLocation, True, False, 0)
        self.vbox.pack_start(self.btnDownload, True, False, 0)
        self.vbox.pack_start(self.prgbDownload, True, False, 0)
        self.vbox.show()

        self.page = gtk.Frame()
        self.page.add(self.vbox)
        self.page.show()
