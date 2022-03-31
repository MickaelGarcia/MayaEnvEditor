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
import os
import ME_core as Core
from qtpy import QtWidgets, QtCore

STYLE_SHEET = """QSplitter::handle:horizontal {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #eee, stop:1 #ccc);
width: 4px;
border-radius: 4px;
}"""
VAR_TYPE = ["<class 'path'>", str(bool), str(str)]

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
        self.addButton.setEnabled(False)
        self.editButton = QtWidgets.QPushButton("Edit")
        self.editButton.setEnabled(False)
        spacer = QtWidgets.QSpacerItem(25,10)
        self.removeButton = QtWidgets.QPushButton("Remove")
        self.removeButton.setEnabled(False)

        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addSpacerItem(spacer)
        buttonLayout.addWidget(self.removeButton)

        workspaceLayout.addLayout(buttonLayout)

        saveButton = QtWidgets.QPushButton("Save")
        saveButton.setEnabled(False)
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
        self.addButton.setEnabled(True)
        self.editButton.setEnabled(True)
        self.removeButton.setEnabled(True)
        self.variablesView.clear()
        selectedVersion = self.mayaVersions.selectedItems()[0].text(0)
        currentVars = self.mayaEnvs[selectedVersion]
        for var in currentVars:
            QtWidgets.QTreeWidgetItem(self.variablesView, [var.name, var.value, str(var.varType())])
    
    def newVariable(self):
        dialog = NewVariable(self)
        dialog.exec_()

        valuesDialog = dialog.toReturn
        if not valuesDialog:
            return
        else:
            QtWidgets.QTreeWidgetItem(self.variablesView, [*valuesDialog])

    def editVariable(self):
        dialog = NewVariable(self)
        dialog.exec_()

        valuesDialog = dialog.toReturn
        if not valuesDialog:
            return
        else:
            pass


class NewVariable(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super(NewVariable, self).__init__(parent)
        self.model = model
        self.toReturn = None
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

        # Paths
        self.pathLayout = QtWidgets.QHBoxLayout()
        pathLabel = QtWidgets.QLabel("Path Value :")
        self.pathValue = QtWidgets.QLineEdit()
        pathButton = QtWidgets.QPushButton("...")
        self.pathLayout.addWidget(pathLabel)
        self.pathLayout.addWidget(self.pathValue)
        self.pathLayout.addWidget(pathButton)
        self.baseLayout.addLayout(self.pathLayout)

        # Bool
        self.boolLayout = QtWidgets.QHBoxLayout()
        boolLabel = QtWidgets.QLabel("Bool Value :")
        self.boolValue = QtWidgets.QComboBox()
        self.boolValue.addItems(["True", "False"])
        self.boolLayout.addWidget(boolLabel)
        self.boolLayout.addWidget(self.boolValue)
        self.baseLayout.addLayout(self.boolLayout)

        # Str
        self.strLayout = QtWidgets.QHBoxLayout()
        strLabel = QtWidgets.QLabel("Str Value :")
        self.strValue = QtWidgets.QLineEdit()
        self.strLayout.addWidget(strLabel)
        self.strLayout.addWidget(self.strValue)
        self.baseLayout.addLayout(self.strLayout)
        
        # Buttont
        self.dialogButtonLayout = QtWidgets.QHBoxLayout()
        self.dialogBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(self.dialogBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.dialogButtonLayout.addWidget(self.buttonBox)
        self.baseLayout.addLayout(self.dialogButtonLayout)

        self.typeSelect.currentIndexChanged.connect(self.variableChanged)
        self.variableChanged()

    def variableChanged(self):
        typeSelected = self.typeSelect.currentIndex()
        if typeSelected == 0:
            showLayoutContant(self.pathLayout)
            hideLayoutContant(self.boolLayout)
            hideLayoutContant(self.strLayout)
        elif typeSelected == 1:
            hideLayoutContant(self.pathLayout)
            showLayoutContant(self.boolLayout)
            hideLayoutContant(self.strLayout)
        elif typeSelected == 2:
            hideLayoutContant(self.pathLayout)
            hideLayoutContant(self.boolLayout)
            showLayoutContant(self.strLayout)

    def accept(self):
        varName = self.varNameText.text().upper()
        values = [os.path.join(self.pathValue.text()), self.boolValue.currentText(), self.strValue.text()]
        value = values[self.typeSelect.currentIndex()]
        valueType = VAR_TYPE[self.typeSelect.currentIndex()]
        self.toReturn = (varName, value, valueType)
        self.done(1)

    def reject(self):
        self.done(0)

def hideLayoutContant(layout):
    for i in range(layout.count()):
        layout.itemAt(i).widget().hide()

def showLayoutContant(layout):
    for i in range(layout.count()):
        layout.itemAt(i).widget().show()


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mayaEditorUI()
    window.show()
    sys.exit(app.exec_())
