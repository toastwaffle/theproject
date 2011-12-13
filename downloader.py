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
import threading
import webbrowser
import gobject

class WorkerThread(threading.Thread):
    def __init__(self,function,parent):
        threading.Thread.__init__(self)
        self.function = function
        self.parent = parent
        
    def run(self):
        self.parent.still_working = True
        self.function()
        self.parent.still_working = False
        
    def stop(self):
        self = None

class Downloader:
    def prgbPulse(self):
        if self.pulse_on == True:
            self.prgbDownload.pulse()
        return self.still_working # 1 = repeat, 0 = stop

    def btnDownloadEvent(self, widget):
        WT = WorkerThread(self.download,self)
        WT.start()
        gobject.timeout_add(100, self.prgbPulse)
        
    def download(self):
        self.pulse_on = True
        try:
            with gtk.gdk.lock:
                dlfrom = self.edtDownloadFromLocation.get_text()
                dlto = self.edtDownloadToLocation.get_text()
            print "Opening URL"
            urlfile = urllib2.urlopen(dlfrom)
            print "Opened URL"
            if urlfile.geturl().split('.')[-1] != dlfrom.split('.')[-1]:
                filename = dlfrom.split('/')[-1]
            else:
                filename = urlfile.geturl().split('/')[-1]
            if dlto[-1] == '/':
                dlto += filename
            print "Opening File"
            fileh = open(dlto,'wb')
            print "Opened File"
            chunk = 4096
            downloaded = 0
            contentlength = urlfile.info().getheaders("Content-Length")
            if len(contentlength) != 0:
                filesize = int(meta.getheaders("Content-Length")[0])
                with gtk.gdk.lock:
                    self.pulse_on = False
                    self.prgbDownload.set_fraction(0)
                    self.prgbDownload.set_text("Downloaded: %s Bytes. Remaining: %s Bytes."%(downloaded,filesize-downloaded))
            else:
                with gtk.gdk.lock:
                    self.prgbDownload.set_text("Downloaded: %s Bytes"%downloaded)
            print "Starting Download"
            while 1:
                data = urlfile.read(chunk)
                downloaded += len(data)
                if len(contentlength) != 0:
                    with gtk.gdk.lock:
                        self.prgbDownload.set_fraction(downloaded/filesize)
                        self.prgbDownload.set_text("Downloaded: %s Bytes. Remaining: %s Bytes."%(downloaded,filesize-downloaded))
                else:
                    with gtk.gdk.lock:
                        self.prgbDownload.set_text("Downloaded: %s Bytes"%downloaded)
                if not data:
                    break
                fileh.write(data)
            fileh.close()
            print "Done."
            self.lastfile = dlto+filename
            with gtk.gdk.lock:
                self.btnOpenFile.show()
        except urllib2.URLError:
            with gtk.gdk.lock:
                self.pulse_on = False
                self.prgbDownload.set_fraction(0)
                lblError = gtk.Label("Could Not Connect to URL.")
                lblError.show()
                errordialog = gtk.Dialog("Error.", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                errordialog.vbox.pack_start(lblError)
                result = errordialog.run()
                errordialog.hide()
        except urllib2.HTTPError as error:
            with gtk.gdk.lock:
                self.pulse_on = False
                self.prgbDownload.set_fraction(0)
                lblError = gtk.Label("HTTP Error "+str(error.code)+".\nPlease check the URL and try again later")
                lblError.show()
                errordialog = gtk.Dialog("Error.", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                errordialog.vbox.pack_start(lblError)
                result = errordialog.run()
                errordialog.hide()
        except IOError as (errno,strerror):
            with gtk.gdk.lock:
                self.pulse_on = False
                self.prgbDownload.set_fraction(0)
                lblError = gtk.Label("I/O Error "+str(errno)+".\n"+strerror)
                lblError.show()
                errordialog = gtk.Dialog("Error.", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                errordialog.vbox.pack_start(lblError)
                result = errordialog.run()
                errordialog.hide()

            

    def btnOpenFileEvent(self,widget):
        webbrowser.open(self.lastfile)

    def __init__(self,parent):
        gobject.threads_init()
        gtk.gdk.threads_init()
        self.parent = parent
        
        self.prgbDownload = gtk.ProgressBar(adjustment=None)
        self.prgbDownload.show()

        self.edtDownloadFromLocation = gtk.Entry()
        self.edtDownloadFromLocation.show()

        self.lblDownloadFromLocation = gtk.Label("Download From: ")
        self.lblDownloadFromLocation.show()

        self.edtDownloadToLocation = gtk.Entry()
        self.edtDownloadToLocation.set_text(os.path.expanduser('~/Downloads'))
        self.edtDownloadToLocation.show()

        self.lblDownloadToLocation = gtk.Label("Download To: ")
        self.lblDownloadToLocation.show()

        self.btnDownload = gtk.Button("Download")
        self.btnDownload.connect("clicked", self.btnDownloadEvent)
        self.btnDownload.show()

        self.btnOpenFile = gtk.Button("Open File")
        self.btnOpenFile.connect("clicked", self.btnOpenFileEvent)

        self.vbox = gtk.VBox(False, 3)
        self.vbox.pack_start(self.lblDownloadFromLocation, False, False, 0)
        self.vbox.pack_start(self.edtDownloadFromLocation, False, False, 0)
        self.vbox.pack_start(self.lblDownloadToLocation, False, False, 0)
        self.vbox.pack_start(self.edtDownloadToLocation, False, False, 0)
        self.vbox.pack_start(self.btnDownload, False, False, 0)
        self.vbox.pack_start(self.prgbDownload, True, False, 0)
        self.vbox.pack_start(self.btnOpenFile, False, False, 0)
        self.vbox.show()

        self.page = gtk.Frame()
        self.page.add(self.vbox)
        self.page.show()
