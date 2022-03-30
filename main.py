"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Maya Environment Editor, Python Maya library and module.
    Author : Mickael GARCIA - Toonkit
    Copyright (C) 2014-2022 Toonkit
    http://toonkit-studio.com/

    Maya Environment Editor is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Maya Environment Editor is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Maya Environment Editor.  If not, see <http://www.gnu.org/licenses/>
-------------------------------------------------------------------------------
"""

import sys
import re
import variables
import ME_core as Core
from qtpy import QtWidgets, QtCore

STYLE_SHEET = """QSplitter::handle:horizontal {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #eee, stop:1 #ccc);
width: 4px;
border-radius: 4px;
}"""


class mayaEditorUI(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mayaEditorUI, self).__init__(*args, **kwargs)

        self.mayaEnvs = None
        # self.setStyleSheet(STYLE_SHEET)
        
        self.setWindowTitle("Maya Environement Editor")
        centralWidget = QtWidgets.QWidget()
        centralLayout = QtWidgets.QHBoxLayout()
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(centralLayout)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        centralLayout.addWidget(splitter)

        mayaVersionsWidgets = QtWidgets.QWidget()
        mayaVersionsLayout = QtWidgets.QHBoxLayout()
        self.mayaVersions = QtWidgets.QTreeWidget()
        self.mayaVersions.setHeaderLabel("Maya Versions")
        self.mayaVersions.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
        mayaVersionsWidgets.setLayout(mayaVersionsLayout)
        mayaVersionsLayout.addWidget(self.mayaVersions)

        workspaceWidget = QtWidgets.QWidget()
        workspaceLayout = QtWidgets.QVBoxLayout()
        workspaceWidget.setLayout(workspaceLayout)

        self.variablesView = QtWidgets.QTreeWidget()
        self.variablesView.setHeaderLabels(["Name", "Values", "Type"])
        workspaceLayout.addWidget(self.variablesView)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.setAlignment(QtCore.Qt.AlignRight)
        self.addButton = QtWidgets.QPushButton("Add")
        self.editButton = QtWidgets.QPushButton("Edit")
        spacer = QtWidgets.QSpacerItem(25,10)
        self.removeButton = QtWidgets.QPushButton("Remove")

        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addSpacerItem(spacer)
        buttonLayout.addWidget(self.removeButton)

        workspaceLayout.addLayout(buttonLayout)

        saveButton = QtWidgets.QPushButton("Save")
        workspaceLayout.addWidget(saveButton)

        splitter.addWidget(mayaVersionsWidgets)
        splitter.addWidget(workspaceWidget)

        self.mayaVersions.itemClicked.connect(self.populateVariables)
        self.addButton.clicked.connect(self.newVariable)

        self.populateVersions()


    def populateVersions(self):
        self.mayaVersions.clear()
        self.mayaEnvs = Core.getMayaEnvs()
        mayaVersions = reversed(list(self.mayaEnvs.keys()))
        for verison in mayaVersions:
            QtWidgets.QTreeWidgetItem(self.mayaVersions, [verison])
    
    def populateVariables(self):
        self.variablesView.clear()
        selectedVersion = self.mayaVersions.selectedItems()[0].text(0)
        currentVars = self.mayaEnvs[selectedVersion]
        for var in currentVars:
            QtWidgets.QTreeWidgetItem(self.variablesView, [var.name, var.value, str(var.varType())])
    
    def newVariable(self):
        dialog = NewVariable(self)
        dialog.exec_()


class NewVariable(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super(NewVariable, self).__init__(parent)
        self.model = model
        self.setWindowTitle("Add New Variable")
        self.baseLayout = QtWidgets.QVBoxLayout()
        typeLayout = QtWidgets.QHBoxLayout()
        typeLabel = QtWidgets.QLabel("Variable Type")
        self.typeSelect = QtWidgets.QComboBox()
        self.typeSelect.addItems(["Path", "Bool", "Str"])
        varNameLayout = QtWidgets.QHBoxLayout()
        varNameLabel = QtWidgets.QLabel("Variable Name : ")
        self.varNameText = QtWidgets.QLineEdit()
        varNameLayout.addWidget(varNameLabel)
        varNameLayout.addWidget(self.varNameText)

        typeLayout.addWidget(typeLabel)
        typeLayout.addWidget(self.typeSelect)
        self.baseLayout.addLayout(typeLayout)
        self.baseLayout.addLayout(varNameLayout)

        self.setLayout(self.baseLayout)

        self.typeSelect.currentIndexChanged.connect(self.variableChaged)
        self.variableChaged()

        # Paths
        self.pathLayout = QtWidgets.QHBoxLayout()
        pathLabel = QtWidgets.QLabel("Path Value :")
        self.pathValue = QtWidgets.QLineEdit()
        pathButton = QtWidgets.QPushButton("...")
        self.pathLayout.addWidget(pathLabel)
        self.pathLayout.addWidget(self.pathValue)
        self.pathLayout.addWidget(pathButton)
        self.baseLayout.addLayout(self.pathLayout)

    def variableChaged(self):
        typeSelected = self.typeSelect.currentIndex

app = QtWidgets.QApplication(sys.argv)
window = mayaEditorUI()
window.show()
sys.exit(app.exec_())
