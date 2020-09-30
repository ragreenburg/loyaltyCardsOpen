#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi, sqlite3 as sqlite
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio

con = sqlite.connect('ydb.db')

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def entered_tab(self, button):

        searchEntry = builder.get_object("searchEntry")
        listbox = builder.get_object("listbox")
        searchParam = searchEntry.get_text()
        searchParamDef = "%"+searchParam+"%"
        print ("searchParamDef="+searchParamDef)
        with con:

            cur = con.cursor()
            cur.execute("SELECT CARD_NAME FROM CARD where CARD_NAME LIKE ? " , (searchParamDef,))
            rows = cur.fetchall()
            for row in rows:
                print (row[0])
                listbox.add(ListBoxRowWithData(row[0]))
            listbox.show_all()
       
    def on_button_clicked(self, button):
        entry = builder.get_object("cardNameEntry")
        barcodeEntry = builder.get_object("barcodeEntry")
        frontImage = builder.get_object("frontImage")
        
        frontImage1 = frontImage.get_file()
        
        #print(frontImage1)
        x = bytes(frontImage1)
        

        cardName =str(entry.get_text())
        barcodeEntry =str(barcodeEntry.get_text())
        print ('Card Name: %s' % cardName + ' '+ 'barcodeEntry: %s' % barcodeEntry)
        
        with con:
            cur = con.cursor()
            cur.execute('INSERT INTO CARD(CARD_NAME, BARCODE, IMAGE) VALUES (?,?,?)', (cardName, barcodeEntry, x))


builder = Gtk.Builder()
builder.add_from_file("TestGlade.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()

Gtk.main()
