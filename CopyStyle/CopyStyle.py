# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CopyStyle
                                 A QGIS plugin for Layer Style Copy & Paste
                              -------------------
        begin                : 2026-09-29
        copyright            : (C) 2026 by Kevin Landolt
        email                : qgis@klandolt.ch
 ***************************************************************************/

"""
from qgis.PyQt.QtCore import Qt, QCoreApplication
from qgis.core import QgsSettings, Qgis
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

import os.path


class CopyStyle:

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        
        # Name des Menüeintrags unter "Erweiterungen"
        self.menu_name = "Copy Style"
        
        #Toolbar Vars:
        self.toolbar = None
        
        # Die separaten Klick-Buttons
        self.btn_style_copy = None
        self.btn_style_past = None
        
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Declare instance attributes
        self.actions = []

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
        # Create Toolbar
        self.toolbar = self.iface.addToolBar("Copy Style")
        self.toolbar.setObjectName("CopyStyle")

        # --- BUTTON 1: Style copy ---
        icon_import = os.path.join(os.path.dirname(__file__), 'icons', 'style_copy.png')
        self.btn_style_copy = QAction(QIcon(icon_import), "Style kopieren", self.iface.mainWindow())
        self.btn_style_copy.triggered.connect(self.style_copy)
        self.toolbar.addAction(self.btn_style_copy)
        self.iface.addPluginToMenu(self.menu_name, self.btn_style_copy)

        # --- BUTTON 2: Style Paste ---
        icon_process = os.path.join(os.path.dirname(__file__), 'icons', 'style_paste.png')
        self.btn_style_past = QAction(QIcon(icon_process), "Style Einfügen", self.iface.mainWindow())
        self.btn_style_past.triggered.connect(self.style_paste)
        self.toolbar.addAction(self.btn_style_past)
        self.iface.addPluginToMenu(self.menu_name, self.btn_style_past)

        # Force it to dock vertically on the left side
        main_window = self.iface.mainWindow()
        main_window.addToolBar(Qt.LeftToolBarArea, self.toolbar)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        
        # Remove Actions from Toolbar
        self.toolbar.removeAction(self.btn_style_copy)
        self.toolbar.removeAction(self.btn_style_past)

        # Remove Toolbar from QGIS MainWindows
        if self.toolbar is not None:
            main_window = self.iface.mainWindow()
            main_window.removeToolBar(self.toolbar)

        # Destroy Vars
        self.toolbar.deleteLater()
        self.toolbar = None
        
        # Aus dem QGIS-Menü entfernen
        self.iface.removePluginMenu(self.menu_name, self.btn_style_copy)
        self.iface.removePluginMenu(self.menu_name, self.btn_style_past)
        

    def style_copy(self):
        # Code for Button Style Copy
        print("Button: Style Copy")
        self.iface.actionCopyLayerStyle().trigger() 
        self.iface.messageBar().pushMessage("Info", "Style kopiert!", level=Qgis.Info, duration=3)

    def style_paste(self):
        # Code for Button Style Paste
        print("Button: Style Paste")
        self.iface.actionPasteLayerStyle().trigger()
        self.iface.messageBar().pushMessage("Info", "Style übertragen!", level=Qgis.Info, duration=3)

