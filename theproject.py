#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class Base:
    def destroy(self, widget, data=None):
        gtk.main_quit()

    def btnPushEvent():
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(350,400)
        self.window.set_title("TheProject")
        self.window.show()
        self.window.connect("destroy", self.destroy)      

        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.show_tabs = True
        notebook.show_border = True

        dialog = gtk.FileChooserDialog("Open...", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            print dialog.get_filename(), 'Selected'
        elif response == gtk.RESPONSE_CANCEL:
            print 'You didnt choose any files!'
        dialog.hide()

        btnPush = gtk.Button("Push")
        btnPush.connect("clicked", self.btnPushEvent)
        btnPush.show()

        fixedLayout = gtk.Fixed()
        fixedLayout.put(btnPush, 0, 250)
        fixedLayout.show()

        page1 = gtk.Frame()
        page1.add(fixedLayout)
        page1.show()
        notebook.append_page(page1)
        notebook.set_tab_label_text(page1, "Git / FTP")

        page2 = gtk.Label("This is gonna be replaced by content...\n...Soon...\n...Hopefully...;)")
        page2.show()
        notebook.append_page(page2)
        notebook.set_tab_label_text(page2, "Auto Installs")

        page3 = gtk.Label("This is gonna be replaced by content...\n...Soon...\n...Hopefully...;)")
        page3.show()
        notebook.append_page(page3)
        notebook.set_tab_label_text(page3, "Downloader")

        notebook.show()
        self.window.add(notebook)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
