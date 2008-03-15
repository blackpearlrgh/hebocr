#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Generated with glade2py script
# glade2py script can be found at hocr web site http://hocr.berlios.de

# Copyright (C) 2008 Yaacov Zamir <kzamir_a_walla.co.il>

import sys, os
import threading
import time

import pygtk
pygtk.require('2.0')

import gtk, gtk.glade
import pango

from hocr import *

# set global paths
# FIXME: this can change from system to system
app_name = "hocr-gtk"
locale_dir = '/usr/share/locale'
glade_file = 'hocr-gtk.glade'
glade_dir = '/usr/share/hocr-gtk/glade/'
logo_filename = '/usr/share/pixmaps/hocr1-128.png'

# import the locale system
try:
    import locale
    import gettext
    locale.setlocale(locale.LC_ALL, "")
    gtk.glade.bindtextdomain(app_name, locale_dir)
    gettext.install(app_name, locale_dir, unicode=1)
except (IOError,locale.Error), e:
    print "WARNING: Can't load locale"
    _ = lambda x : x

# gpl text
gpl_text = """
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# program info
app_version = "0.1.1"
copyright = "Copyright (C) Yaacov Zamir <kzamir@walla.co.il>"
comments = _("Hocr-GTK, Hebrew optical character recognition\ngraphical front end (GTK)\n\n")
comments += hocr_get_build_string()
artists = [_("Shlomi Israel <sijproject@gmail.com>")]
authors = [_("Yaacov Zamir <kzamir@walla.co.il>")]

# set global functions
def update_preview_cb(file_chooser, preview):
    filename = file_chooser.get_preview_filename()
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 128, 128)
        preview.set_from_pixbuf(pixbuf)
        have_preview = True
    except:
        have_preview = False
    file_chooser.set_preview_widget_active(have_preview)
    return

def show_error_message(message):
    dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR ,message_format = message ,buttons=gtk.BUTTONS_OK)
    dlg.run()
    dlg.destroy()

class ProgressSet(threading.Thread):
    "set the fraction of the progressbar"
    
    # thread event, stops the thread if it is set.
    stopthread = threading.Event()
        
    def run(self):
        "run while thread is alive."
        
        # importing the progressbar from the global scope
        global progressbar 
        global hocr_obj
        
        self.stopthread.clear()
        
        # main loop
        while not self.stopthread.isSet() :
            # acquiring the gtk global mutex
            gtk.gdk.threads_enter()
            # set the fraction
            progressbar.set_fraction(1.0 * hocr_obj.progress / 100.0)
            # releasing the gtk global mutex
            gtk.gdk.threads_leave()
            
            # delaying 
            time.sleep(0.2)
        
    def stop(self):
        "stop main loop"
        progressbar.set_fraction(1.0 * hocr_obj.progress / 100.0)
        self.stopthread.set()

class RunOCR(threading.Thread):
    def run(self):
        # importing the ocr object from the global scope
        global main_window
        global hocr_obj
        global menuitem_clear
        global textbuffer
        global textview
        global progressbar 
        global image_window_type
        global hocr_pixbuf
        global pixbuf
        global image
        
        ps = ProgressSet()
        
        # set cursor to gtk.gdk.WATCH and print processing on the progress bar
        textview.get_parent_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        progressbar.show()
        
        # do ocr
        ps.start()
        hocr_obj.do_ocr()
        ps.stop()
        
        # set the new image in image window
        if image_window_type == 0:
            hocr_pixbuf = pixbuf.copy()
        else:
            # create an hocr pixbuf
            if image_window_type == 1:
                pix = hocr_pixbuf = hocr_obj.get_bitmap_pixbuf ()
            if image_window_type == 2:
                pix = self.hocr_pixbuf = hocr_obj.get_layout_pixbuf ()
            # create a gtk pixbuf
            hocr_pixbuf = gtk.gdk.pixbuf_new_from_data(
                ho_pixbuf_get_data_string(pix),
                gtk.gdk.COLORSPACE_RGB, 0, 8, 
                pix.width, pix.height, pix.rowstride)
        
        main_window.on_image_refresh(None, None)
        
        # return original cursor and print idle on the progress bar
        textview.get_parent_window().set_cursor(None)
        progressbar.hide()
        
        # set text
        if hocr_obj.get_text():
            if menuitem_clear.get_active():
                textbuffer.set_text(hocr_obj.get_text())
            else:
                textbuffer.insert_at_cursor(hocr_obj.get_text())
            textview.grab_focus()

# set main window class
class MainWindow:
    def __init__(self):
        global progressbar 
        global hocr_obj
        global menuitem_clear
        global textbuffer
        global textview
        global pixbuf
        global hocr_pixbuf
        global image
        
        # create widget tree ...
        xml = False
        if os.path.isfile(glade_file):
            xml = gtk.glade.XML(glade_file, 'window_main', app_name)
        else:
            if os.path.isfile(glade_dir + glade_file):
               xml = gtk.glade.XML(glade_dir + glade_file, 'window_main', app_name)
        
        if not xml:
            print "ERROR: Can't load glade GUI file, check your install."
            show_error_message(_("Can't load hocr's glade GUI file, check your install.\nExit program."))
            sys.exit(0)
        
        # connect handlers
        xml.signal_autoconnect(self)

        # widgets
        self.window_main = xml.get_widget('window_main')
        self.image = xml.get_widget('image')
        self.textview = xml.get_widget('textview')
        self.progressbar = xml.get_widget('progressbar')
        self.statusbar1 = xml.get_widget('statusbar1')
        
        progressbar = self.progressbar
        textview = self.textview
        image = self.image
        
        # init progress bar and hide it
        progressbar.set_text(_("Processing..."))
        progressbar.hide()
        
        # text 
        self.textbuffer =  self.textview.get_buffer()
        self.clipboard = gtk.Clipboard()
        self.textview.grab_focus()
        
        textbuffer = self.textbuffer
        
        # image
        self.preview = gtk.Image()
        self.filename = ""
        pixbuf = None
        hocr_pixbuf = None
        self.zoom_factor = 1.0
                
        # hocr_pixbuf options
        self.menuitem_orig = xml.get_widget('menuitem_orig')
        self.menuitem_bw = xml.get_widget('menuitem_bw')
        self.menuitem_layout = xml.get_widget('menuitem_layout')
        
        # edit
        self.menuitem_clear = xml.get_widget('menuitem_clear')
        self.menuitem_html = xml.get_widget('menuitem_html')
        self.menuitem_nikud = xml.get_widget('menuitem_nikud')
        self.menuitem_column_auto = xml.get_widget('menuitem_column_auto')
        self.menuitem_column_one = xml.get_widget('menuitem_column_one')
        
        self.menuitem_font_1 = xml.get_widget('menuitem_font_1')
        self.menuitem_font_2 = xml.get_widget('menuitem_font_2')
        self.menuitem_font_3 = xml.get_widget('menuitem_font_3')
        self.menuitem_font_4 = xml.get_widget('menuitem_font_4')
        self.menuitem_font_5 = xml.get_widget('menuitem_font_5')
        self.menuitem_font_6 = xml.get_widget('menuitem_font_6')
        
        menuitem_clear = self.menuitem_clear
        
        # ocr
        self.hocr_obj = Hocr()
        
        hocr_obj = self.hocr_obj
    
    # signal handlers
    def on_window_main_delete_event(self, widget, obj):
        "on_window_main_delete_event activated"
        gtk.main_quit()

    def on_imagemenuitem_new_activate(self, obj, event = None):
        "on_imagemenuitem_new_activate activated"
        global pixbuf
        global hocr_pixbuf
        
        chooser = gtk.FileChooserDialog(_("Open.."),
            None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.set_preview_widget(self.preview)
        chooser.connect("update-preview", update_preview_cb, self.preview)
        
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.filename = chooser.get_filename()
            # get new image
            pixbuf = gtk.gdk.pixbuf_new_from_file (self.filename)
            # clean processed image
            hocr_pixbuf = None
            
            factor = self.zoom_factor
            w = pixbuf.get_width()
            h = pixbuf.get_height()
            window_pixbuf = pixbuf.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
            self.image.set_from_pixbuf(window_pixbuf)
            self.progressbar.set_fraction(0)
            
        elif response == gtk.RESPONSE_CANCEL:
            print _('Closed, no files selected')
        
        chooser.destroy()
        
        self.textview.grab_focus()
        
    def on_imagemenuitem_save_activate(self, obj, event = None):
        "on_imagemenuitem_save_activate activated"
        chooser = gtk.FileChooserDialog(_("Save.."),
            None,
            gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
            thefile = open(filename, 'w')
            thefile.write (self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter()))
            thefile.close()
        elif response == gtk.RESPONSE_CANCEL:
            print _('Closed, no files selected')
        
        chooser.destroy()
        
        self.textview.grab_focus()
        
    def on_menuitem_apply_activate(self, obj, event = None):
        "on_menuitem_apply_activate activated"
        global pixbuf
        
        if not (self.filename and pixbuf) :
            return
        
        # create hocr pixbuf
        pix = ho_pixbuf_new (pixbuf.get_n_channels(), 
            pixbuf.get_width(), pixbuf.get_height (),
            pixbuf.get_rowstride ())
        
        ho_pixbuf_set_data (pix, pixbuf.get_pixels())
        
        # set ocr options
        self.hocr_obj.set_pixbuf(pix)
        self.hocr_obj.set_html(self.menuitem_html.get_active())
        self.hocr_obj.set_nikud(self.menuitem_nikud.get_active())
        if self.menuitem_column_auto.get_active():
              self.hocr_obj.set_paragraph_setup(0)
        else:
              self.hocr_obj.set_paragraph_setup(1)
        if self.menuitem_font_1.get_active():
              self.hocr_obj.set_font (0)
        if self.menuitem_font_2.get_active():
              self.hocr_obj.set_font (1)
        if self.menuitem_font_3.get_active():
              self.hocr_obj.set_font (2)
        if self.menuitem_font_4.get_active():
              self.hocr_obj.set_font (3)
        if self.menuitem_font_5.get_active():
              self.hocr_obj.set_font (4)
        if self.menuitem_font_6.get_active():
              self.hocr_obj.set_font (5)
        
        # run ocr
        ro = RunOCR()
        ro.start()
    
    def on_imagemenuitem_quit_activate(self, obj, event = None):
        "on_imagemenuitem_quit_activate activated"
        gtk.main_quit()

    def on_imagemenuitem_cut_activate(self, obj, event = None):
        "on_imagemenuitem_cut_activate activated"
        self.textbuffer.cut_clipboard(self.clipboard, True)

    def on_imagemenuitem_copy_activate(self, obj, event = None):
        "on_imagemenuitem_copy_activate activated"
        self.textbuffer.copy_clipboard(self.clipboard)

    def on_imagemenuitem_paste_activate(self, obj, event = None):
        "on_imagemenuitem_paste_activate activated"
        self.textbuffer.paste_clipboard(self.clipboard, None, True)

    def on_imagemenuitem_delete_activate(self, obj, event = None):
        "on_imagemenuitem_delete_activate activated"
        self.textbuffer.delete_selection(True, True)

    def on_menuitem_zoom_in_activate(self, obj, event = None):
        "on_menuitem_zoom_in_activate activated"
        global pixbuf
        global hocr_pixbuf
        
        self.zoom_factor *= 1.2
        
        pix = hocr_pixbuf
        
        if not pix:
            pix = pixbuf
            
        if not pix:
            return
        
        factor = self.zoom_factor
        w = pix.get_width()
        h = pix.get_height()
        window_pixbuf = pix.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
        self.image.set_from_pixbuf(window_pixbuf)

    def on_menuitem_zoom_out_activate(self, obj, event = None):
        "on_menuitem_zoom_out_activate activated"
        global pixbuf
        global hocr_pixbuf
        
        self.zoom_factor *= 0.8
        
        pix = hocr_pixbuf
        
        if not pix:
            pix = pixbuf
            
        if not pix:
            return
        
        factor = self.zoom_factor
        w = pix.get_width()
        h = pix.get_height()
        window_pixbuf = pix.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
        self.image.set_from_pixbuf(window_pixbuf)

    def on_menuitem_zoom_100_activate(self, obj, event = None):
        "on_menuitem_zoom_100_activate activated"
        global pixbuf
        global hocr_pixbuf
        
        self.zoom_factor = 1.0
        
        pix = hocr_pixbuf
        
        if not pix:
            pix = pixbuf
            
        if not pix:
            return
        
        factor = self.zoom_factor
        w = pix.get_width()
        h = pix.get_height()
        window_pixbuf = pix.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
        self.image.set_from_pixbuf(window_pixbuf)
    
    def on_menuitem_best_fit_activate(self, obj, event = None):
        "on_menuitem_best_fit_activate activated"
        global pixbuf
        global hocr_pixbuf
        
        pix = hocr_pixbuf
        
        if not pix:
            pix = pixbuf
            
        if not pix:
            return
        
        w = pix.get_width()
        h = pix.get_height()
        width, height = self.window_main.get_size()
        
        # give image some leeway
        if width > 100:
            width -= 40;
        self.zoom_factor = 1.0 * width / w
                
        factor = self.zoom_factor
        
        window_pixbuf = pix.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
        self.image.set_from_pixbuf(window_pixbuf)
    
    def on_image_refresh(self, obj, event = None):
        "on_menuitem_best_fit_activate activated"
        global pixbuf
        global hocr_pixbuf
        
        pix = hocr_pixbuf
        
        if not pix:
            pix = pixbuf
            
        if not pix:
            return
        
        w = pix.get_width()
        h = pix.get_height()
                        
        factor = self.zoom_factor
        
        window_pixbuf = pix.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
        self.image.set_from_pixbuf(window_pixbuf)
        
    def on_imagemenuitem_about_activate(self, obj, event = None):
        "on_imagemenuitem_about_activate activated"
        dialog = gtk.AboutDialog()
        dialog.set_name(app_name)
        dialog.set_version(app_version)
        dialog.set_copyright(copyright)
        dialog.set_comments(comments)
        logo_pix = gtk.gdk.pixbuf_new_from_file(logo_filename)
        dialog.set_logo(logo_pix)
        dialog.set_license(gpl_text)
        dialog.set_translator_credits(_("translator-credits"))
        dialog.set_artists(artists)
        dialog.set_authors(authors)
        dialog.run()
        
        dialog.destroy()
        
        self.textview.grab_focus()
        
    def on_menuitem_select_font_activate(self, obj, event = None):
        "on_imagemenuitem_about_activate activated"
        dialog = gtk.FontSelectionDialog(_("Set text font"))
        
        dialog.run()
        self.textview.modify_font(pango.FontDescription(dialog.get_font_name()))
        dialog.destroy()
        
        self.textview.grab_focus()
        
    def on_toolbutton_open_clicked(self, obj, event = None):
        "on_toolbutton_open_clicked activated"
        self.on_imagemenuitem_new_activate(self, None)

    def on_toolbutton_apply_clicked(self, obj, event = None):
        "on_toolbutton_apply_clicked activated"
        self.on_menuitem_apply_activate(self, None)

    def on_toolbutton_save_clicked(self, obj, event = None):
        "on_toolbutton_save_clicked activated"
        self.on_imagemenuitem_save_activate(self, None)

    def on_toolbutton_zoom_in_clicked(self, obj, event = None):
        "on_toolbutton_zoom_in_clicked activated"
        self.on_menuitem_zoom_in_activate(self, None)

    def on_toolbutton_zoom_out_clicked(self, obj, event = None):
        "on_toolbutton_zoom_out_clicked activated"
        self.on_menuitem_zoom_out_activate(self, None)

    def on_toolbutton_zoom_100_clicked(self, obj, event = None):
        "on_toolbutton_zoom_100_clicked activated"
        self.on_menuitem_zoom_100_activate(self, None)
    
    def on_toolbutton_best_fit_clicked(self, obj, event = None):
        "on_toolbutton_zoom_100_clicked activated"
        self.on_menuitem_best_fit_activate(self, None)
    
    def on_toolbutton_quit_clicked(self, obj, event = None):
        "on_toolbutton_quit_clicked activated"
        gtk.main_quit()
    
    def on_menuitem_orig_toggled(self, obj, event = None):
        "on_menuitem_orig_toggled activated"
        global image_window_type
        global hocr_pixbuf
        global pixbuf
        
        # is this item active ?
        if not obj.get_active():
            return 
            
        image_window_type = 0
        
        # do we have an hocr pixbuf ?
        if not hocr_pixbuf:
            return
        
        # get the new image 
        pix = hocr_pixbuf = pixbuf.copy()
        
        #
        if not pix:
            pix = pixbuf
            
        if not pix:
            return
                        
        factor = self.zoom_factor
        w = pix.get_width()
        h = pix.get_height()
        
        window_pixbuf = pix.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
        self.image.set_from_pixbuf(window_pixbuf)

    def on_menuitem_bw_toggled(self, obj, event = None):
        "on_menuitem_bw_toggled activated"
        global image_window_type
        global hocr_pixbuf
        global pixbuf
        
        if not obj.get_active():
            return 
            
        image_window_type = 1
               
        # do we have an hocr pixbuf ?
        if not hocr_pixbuf:
            return
        
        # get the new image 
        ho_pix = self.hocr_obj.get_bitmap_pixbuf ()
        
        # create a gtk pixbuf
        pix = hocr_pixbuf = gtk.gdk.pixbuf_new_from_data(
                ho_pixbuf_get_data_string(ho_pix),
                gtk.gdk.COLORSPACE_RGB, 0, 8, 
                ho_pix.width, ho_pix.height, ho_pix.rowstride)
                
        #
        if not pix:
            pix = pixbuf
            
        if not pix:
            return
                        
        factor = self.zoom_factor
        w = pix.get_width()
        h = pix.get_height()
        
        window_pixbuf = pix.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
        self.image.set_from_pixbuf(window_pixbuf)

    def on_menuitem_layout_toggled(self, obj, event = None):
        "on_menuitem_layout_toggled activated"
        global image_window_type
        global hocr_pixbuf
        global pixbuf
        
        if not obj.get_active():
            return 
            
        image_window_type = 2
        
        # do we have an hocr pixbuf ?
        if not hocr_pixbuf:
            return
         
        # get the new image 
        ho_pix = self.hocr_obj.get_layout_pixbuf ()
        
        # create a gtk pixbuf
        pix = hocr_pixbuf = gtk.gdk.pixbuf_new_from_data(
                ho_pixbuf_get_data_string(ho_pix),
                gtk.gdk.COLORSPACE_RGB, 0, 8, 
                ho_pix.width, ho_pix.height, ho_pix.rowstride)
        
        #
        if not pix:
            pix = pixbuf
            
        if not pix:
            return
                        
        factor = self.zoom_factor
        w = pix.get_width()
        h = pix.get_height()
        
        window_pixbuf = pix.scale_simple(int(w * factor), int(h * factor), gtk.gdk.INTERP_NEAREST)
        self.image.set_from_pixbuf(window_pixbuf)
    
# run main loop
def main():
    global main_window
    
    main_window = MainWindow()
    main_window.window_main.show()
    gtk.main()

#Initializing the gtk's thread engine
gtk.gdk.threads_init()

# things we need global
progressbar = None
hocr_obj = None
menuitem_clear = None
textbuffer = None
textview = None
image_window_type = 0
hocr_pixbuf = None
pixbuf = None
image = None
main_window = None

if __name__ == "__main__":
    main()

