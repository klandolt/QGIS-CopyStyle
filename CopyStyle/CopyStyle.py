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
from qgis.PyQt.QtCore import QTranslator, Qt, QCoreApplication, QLocale, QSettings
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
        
        # Name menuentry in "Plugins"
        self.menu_name = "Copy Style"
        
        # Toolbar Vars:
        self.toolbar = None
        
        # Objects for Klick-Buttons
        self.btn_style_copy = None
        self.btn_style_past = None
        
        # Initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        
        # Declare instance attributes
        self.actions = []
        
        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        
        # --- Translation INITIALIZE ---
        self.translator = QTranslator()
        # Get Lang Code ("de", "en", ...)
        locale = QgsSettings().value('locale/userLocale', QLocale.system().name())
        # Truncate if, for example, the locale returns "de_CH" but we only want to use "de"
        lang = locale[0:2] 
        
        # Path to the .qm file in the i18n folder
        qm_file = os.path.join(self.plugin_dir, 'i18n', f'copystyle_{lang}.qm')
        
        # Wenn die Datei existiert, in QGIS einspeisen
        if os.path.exists(qm_file):
            self.translator.load(qm_file)
            QCoreApplication.installTranslator(self.translator)


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
        # Create Toolbar
        self.toolbar = self.iface.addToolBar("Copy Style")
        self.toolbar.setObjectName("CopyStyle")
        
        # --- BUTTON 1: Style copy ---
        icon_import = os.path.join(os.path.dirname(__file__), 'icons', 'style_copy.png')
        btn_text_copy = self.tr("Style copy")
        self.btn_style_copy = QAction(QIcon(icon_import), btn_text_copy, self.iface.mainWindow())
        self.btn_style_copy.triggered.connect(self.style_copy)
        self.toolbar.addAction(self.btn_style_copy)
        self.iface.addPluginToMenu(self.menu_name, self.btn_style_copy)
        
        # --- BUTTON 2: Style Paste ---
        icon_process = os.path.join(os.path.dirname(__file__), 'icons', 'style_paste.png')
        btn_text_past = self.tr("Style paste")
        self.btn_style_past = QAction(QIcon(icon_process), btn_text_past, self.iface.mainWindow())
        self.btn_style_past.triggered.connect(self.style_paste)
        self.toolbar.addAction(self.btn_style_past)
        self.iface.addPluginToMenu(self.menu_name, self.btn_style_past)
        
        # Force it to dock vertically on the left side
        main_window = self.iface.mainWindow()
        main_window.addToolBar(Qt.LeftToolBarArea, self.toolbar)


    def tr(self, message):
        # Nutzt QCoreApplication, damit kein QObject geerbt werden muss
        return QCoreApplication.translate(self.__class__.__name__, message)


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
        print(self.tr("Button: Style Copy"))
        
        if self.check_layer() is False:
            return
        
        self.iface.actionCopyLayerStyle().trigger() 
        self.iface.messageBar().pushMessage("Info", self.tr("Style copied!"), level=Qgis.Info, duration=3)


    def style_paste(self):
        # Code for Button Style Paste
        print(self.tr("Button: Style Paste"))
        
        if self.check_layer() is False:
            return
        
        self.iface.actionPasteLayerStyle().trigger()
        self.iface.messageBar().pushMessage("Info", self.tr("Style insertet!"), level=Qgis.Info, duration=3)


    def check_layer(self):
        #Get Active Layer
        layer = self.iface.activeLayer()
        #Check
        if layer is not None:
            print(f"Aktiver Layer: {layer.name()}")
            print(f"Layer-Typ: {layer.type().name}") # e.g., VectorLayer oder RasterLayer
            return True
        else:
            self.iface.messageBar().pushMessage(self.tr("Error"), self.tr("Please select a layer in the Layers panel first!"), level=Qgis.Critical, duration=10)
            return False
