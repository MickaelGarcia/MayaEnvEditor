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

import os
import re
import ctypes.wintypes
import variables

CSIDL_PERSONAL= 5
SHGFP_TYPE_CURRENT= 0
SEPARATOR = ["="]
UNDO_HISTORIC = []

buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
MAYA_PATH = (os.path.join(buf.value, "maya"))


# Gell Document dir and mayas dirs to get all maya.env possibles, and return a dictonary for all maya version found in key, and all variables set as values
def getMayaEnvs():
    # Auto detect maya ducment path and, for all version, get maya.env file
    dirInMayaPath = os.listdir(MAYA_PATH)
    mayaEnvs =  []
    fullMayDict = {}
    for dir in dirInMayaPath:
        if re.match("^\d*$", dir):
            mayaEnvs.append(os.path.join(MAYA_PATH, dir, "Maya.env"))
            for mayaEnv in mayaEnvs:
                fullMayDict[dir] = getEnvVar(mayaEnv)

    return fullMayDict

# With maya.env path, return a dict of all variables except for commented lignes
def getEnvVar(mayaEnvPath):
    # mayaEnvPath (str): path of maya.env file.
    with open (mayaEnvPath, "r") as f:
        mayaVar = f.readlines()
    
    mayaVars = []
    for var in mayaVar:
        if not var.startswith("\\\\"):
            for sep in SEPARATOR:
                if '\n' in var:
                    var = var.replace("\n", "")
                sepVar = var.split(sep)
                if "\\" in sepVar[1]:
                    mayaVars.append(variables.Variable(sepVar[0], mayaEnvPath, sepVar[1], str))
                elif isinstance(eval(sepVar[1]), bool):
                    mayaVars.append(variables.Variable(sepVar[0], mayaEnvPath, sepVar[1], bool))
                else:
                    mayaVars.append(variables.Variable(sepVar[0], mayaEnvPath, sepVar[1], None))
    return mayaVars

# Edit a varaible object content.
def editVariable(variable):
    # variable (variables.Variable): one variable object of maya environment variable datas.
    mayaVariables = getEnvVar(variable.path)
    editedVar = mayaVariables
    isNewVar = False
    for nb, mayaVar in enumerate(mayaVariables):
        if mayaVar.name == variable.name:
            editedVar[nb] = variable
            isNewVar = False
            break
        else:
            isNewVar = True
    if isNewVar:
        editedVar.append(variable)
    return mayaVariables

# Right in maya.env file with the given collection of varialbes 
# Warning : If muliple path in collection, only the first path would be readed
def writeEnvs(mayaEnvs):
    # mayaEnvs (list[variables.Variable]) collection of maya environement variables
    global UNDO_HISTORIC
    path = mayaEnvs[0].path
    newMayaEnvs = str()
    for mayaEnv in mayaEnvs:
        if mayaEnv.path == path:
            if newMayaEnvs == "":
                newMayaEnvs = mayaEnv.name +"="+ str(mayaEnv.value)
            else:
                newMayaEnvs += "\n" + mayaEnv.name +"="+ str(mayaEnv.value)
    with open(path, "r") as f:
        UNDO_HISTORIC.append([path, f.read()])

    with open (path, "w") as f:
        f.write(newMayaEnvs)
    return newMayaEnvs

def undo():
    global UNDO_HISTORIC
    if UNDO_HISTORIC == []:
        print("# WARNING : No Historic Found !")
        return
    with open(UNDO_HISTORIC[-1][0], "w") as f:
        f.write(UNDO_HISTORIC[-1][1])
    del UNDO_HISTORIC[-1]

newVar = variables.Variable("NEW_VAR", os.path.join(MAYA_PATH, "2022", "maya.env"), True, bool)

replaceVar = getMayaEnvs()["2022"][0]
replaceVar.setValue(r"C:\Users\mickaelg\Documents\Toonkit\Toonkit_Module_OscarBlur_2022_1_5_61\Maya2022")
newEnv = editVariable(replaceVar)

# writeEnvs(newEnv)

undo()