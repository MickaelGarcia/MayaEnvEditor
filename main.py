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


class mayaEditorUI(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mayaEditorUI, self).__init__(*args, **kwargs)
        self.setStyleSheet("""QSplitter::handle:horizontal {
                           background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                               stop:0 #eee, stop:1 #ccc);
                           width: 4px;
                           border-radius: 4px;
                           }""")
        self.mayaEnvs = None

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

        splitter.addWidget(mayaVersionsWidgets)
        splitter.addWidget(workspaceWidget)


        self.mayaVersions.itemClicked.connect(self.populateVariables)


        self.populateVersions()

    def populateVersions(self):
        self.mayaVersions.clear()
        self.mayaEnvs = Core.getMayaEnvs()
        for verison in self.mayaEnvs.keys():
            QtWidgets.QTreeWidgetItem(self.mayaVersions, [verison])
    
    def populateVariables(self):
        self.variablesView.clear()
        selectedVersion = self.mayaVersions.selectedItems()[0].text(0)
        currentVars = self.mayaEnvs[selectedVersion]
        for var in currentVars:
            QtWidgets.QTreeWidgetItem(self.variablesView, [var.name, var.value, str(var.varType())])

app = QtWidgets.QApplication(sys.argv)
window = mayaEditorUI()
window.show()
sys.exit(app.exec_())
