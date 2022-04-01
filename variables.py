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

class Variable():
    def __init__(self, variableName, variablePath, variableValue, varaibleType):
        self.variableName = variableName
        self.variablePath = variablePath
        self.variableType = varaibleType
        self.variableValue = variableValue

    @property
    def value(self):
        return self.variableValue
    @property
    def path(self):
        return self.variablePath
    
    @property
    def name(self):
        return self.variableName

    def varType(self):
        return self.variableType
    
    def setValue(self, value):
        self.variableValue = value

    def __eq__(self, obj):
        isSameName = self.variableName == obj.name
        isSamePath = self.variablePath == obj.path
        isSameType = self.variableType == obj.varType()
        siSameValue = self.variableValue == obj.value

        if not isSameName or not isSamePath or not isSameType or not siSameValue:
            return False
        else:
            return True
            
    def __ne__(self, obj):
        return not self == obj