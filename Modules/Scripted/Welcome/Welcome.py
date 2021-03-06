#============================================================================
#
# Copyright (c) Kitware Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#============================================================================

import imp, sys, os, unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

class Welcome(ScriptedLoadableModule):
  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    parent.title = "Welcome"
    parent.categories = ["TubeTK"]
    parent.contributors = ["Johan Andruejol (Kitware)"]
    parent.helpText = """You should not see this"""
    parent.acknowledgementText = """"""

    self.parent = parent

class WelcomeWidget(ScriptedLoadableModuleWidget):
  def setup(self):
    # Add a button to return to the welcome module in the status bar
    statusBar = slicer.util.mainWindow().statusBar()

    self.ReturnToWelcome = qt.QPushButton(statusBar)
    self.ReturnToWelcome.objectName = 'ReturnToWelcomeScreenButton'
    self.ReturnToWelcome.text = 'Return to Welcome screen'
    self.ReturnToWelcome.connect('clicked()', self.selectWelcomeModule)
    statusBar.addPermanentWidget(self.ReturnToWelcome, 1 )

    self.LoadData = qt.QPushButton(statusBar)
    self.LoadData.objectName = 'LoadData'
    self.LoadData.text = 'Load Data'
    self.LoadData.connect('clicked()', self.selectLoadData)
    statusBar.addPermanentWidget(self.LoadData, 1 )

    self.SaveData = qt.QPushButton(statusBar)
    self.SaveData.objectName = 'SaveData'
    self.SaveData.text = 'Save Data'
    self.SaveData.connect('clicked()', self.selectSaveData)
    statusBar.addPermanentWidget(self.SaveData, 1 )

    self.SaveScreenshot = qt.QPushButton(statusBar)
    self.SaveScreenshot.objectName = 'SaveScreenshot'
    self.SaveScreenshot.text = 'Save Screenshot'
    self.SaveScreenshot.connect('clicked()', self.selectSaveScreenshot)
    statusBar.addPermanentWidget(self.SaveScreenshot, 1 )

    self.Quit = qt.QPushButton(statusBar)
    self.Quit.objectName = 'Quit'
    self.Quit.text = 'Quit'
    self.Quit.connect('clicked()', self.selectQuit)
    statusBar.addPermanentWidget(self.Quit, 1 )

    slicer.util.mainWindow().moduleSelector().connect('moduleSelected(QString)',
      self.onModuleSelected)
    self.onModuleSelected()

    # Collapse the data probe button by default
    dataProbeCollapsibleButton = slicer.util.findChildren(text='Data Probe')
    if dataProbeCollapsibleButton is not None:
        dataProbeCollapsibleButton[0].collapsed = True

  def selectWelcomeModule(self):
    slicer.util.selectModule('Welcome')

  def selectLoadData(self):
    slicer.util.openAddDataDialog()

  def selectSaveData(self):
    slicer.util.openSaveDataDialog()

  def selectSaveScreenshot(self):
    slicer.util.openSaveDataDialog()

  def selectQuit(self):
    slicer.util.quit()

  def hideWidget(self, parent, name):
    w = self.findWidget(parent, name)
    if w:
      w.hide()
    else:
      print('Could not find widget named %s' %name)

  def onModuleSelected(self, module = 'Welcome'):
    moduleIsWelcome = (module == 'Welcome')
    mainWindow = slicer.util.mainWindow()
    mainWindow.setPanelDockWidgetVisible(not moduleIsWelcome)
    self.ReturnToWelcome.setVisible(not moduleIsWelcome)
    self.LoadData.setVisible(not moduleIsWelcome)
    self.SaveData.setVisible(not moduleIsWelcome)
    self.SaveScreenshot.setVisible(not moduleIsWelcome)
    self.Quit.setVisible(not moduleIsWelcome)

    if not moduleIsWelcome:
      return

    slicer.app.layoutManager().setLayout(
      slicer.vtkMRMLLayoutNode.SlicerLayoutUserView)
    mainWindow.moduleSelector().hide()
    self.hideWidget(mainWindow, 'CaptureToolBar')
    self.hideWidget(mainWindow, 'DialogToolBar')
    self.hideWidget(mainWindow, 'MainToolBar')
    #self.hideWidget(mainWindow, 'menubar')
    self.hideWidget(mainWindow, 'ModuleToolBar')
    self.hideWidget(mainWindow, 'MouseModeToolBar')
    self.hideWidget(mainWindow, 'ViewersToolBar')
    self.hideWidget(mainWindow, 'ViewToolBar')

  ## UTILS ##
  def findWidget(self, widget, objectName):
    if widget.objectName == objectName:
        return widget
    else:
        children = []
        for w in widget.children():
            resulting_widget = self.findWidget(w, objectName)
            if resulting_widget:
                return resulting_widget
        return None
