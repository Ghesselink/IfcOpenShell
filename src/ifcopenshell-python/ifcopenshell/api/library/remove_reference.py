# IfcOpenShell - IFC toolkit and geometry engine
# Copyright (C) 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of IfcOpenShell.
#
# IfcOpenShell is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IfcOpenShell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IfcOpenShell.  If not, see <http://www.gnu.org/licenses/>.

import ifcopenshell
import ifcopenshell.util.element


class Usecase:
    def __init__(self, file: ifcopenshell.file, reference: ifcopenshell.entity_instance):
        """Removes a library reference

        Any products which have relationships to this reference will not be
        removed.

        :param reference: The IfcLibraryReference entity you want to remove
        :type reference: ifcopenshell.entity_instance.entity_instance
        :return: None
        :rtype: None

        Example:

        .. code:: python

            library = ifcopenshell.api.run("library.add_library", model, name="Brickschema")
            reference = ifcopenshell.api.run("library.add_reference", model, library=library)
            # Let's change our mind and remove it.
            ifcopenshell.api.run("library.remove_reference", model, reference=reference)
        """
        self.file = file
        self.settings = {"reference": reference}

    def execute(self) -> None:
        for rel in self.settings["reference"].LibraryRefForObjects:
            history = rel.OwnerHistory
            self.file.remove(rel)
            if history:
                ifcopenshell.util.element.remove_deep2(self.file, history)
        self.file.remove(self.settings["reference"])
