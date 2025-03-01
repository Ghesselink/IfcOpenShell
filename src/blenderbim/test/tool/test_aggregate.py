# BlenderBIM Add-on - OpenBIM Blender Add-on
# Copyright (C) 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BlenderBIM Add-on.
#
# BlenderBIM Add-on is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.

import bpy
import ifcopenshell
import blenderbim.core.tool
import blenderbim.tool as tool
from test.bim.bootstrap import NewFile
from blenderbim.tool.aggregate import Aggregate as subject


class TestImplementsTool(NewFile):
    def test_run(self):
        assert isinstance(subject(), blenderbim.core.tool.Aggregate)


class TestCanAggregate(NewFile):
    def test_elements_can_aggregate(self):
        ifc = ifcopenshell.file()
        tool.Ifc.set(ifc)
        element = ifc.createIfcElementAssembly()
        element_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(element, element_obj)
        subelement = ifc.createIfcBeam()
        subelement_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(subelement, subelement_obj)
        assert subject.can_aggregate(element_obj, subelement_obj) is True

    def test_spatial_elements_can_aggregate(self):
        ifc = ifcopenshell.file()
        tool.Ifc.set(ifc)
        element = ifc.createIfcSite()
        element_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(element, element_obj)
        subelement = ifc.createIfcBuilding()
        subelement_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(subelement, subelement_obj)
        assert subject.can_aggregate(element_obj, subelement_obj) is True

    def test_spatial_elements_can_aggregate_2x3(self):
        ifc = ifcopenshell.file(schema="IFC2X3")
        tool.Ifc.set(ifc)
        element = ifc.createIfcSite()
        element_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(element, element_obj)
        subelement = ifc.createIfcBuilding()
        subelement_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(subelement, subelement_obj)
        assert subject.can_aggregate(element_obj, subelement_obj) is True

    def test_spatial_elements_and_projects_can_aggregate(self):
        ifc = ifcopenshell.file()
        tool.Ifc.set(ifc)
        element = ifc.createIfcProject()
        element_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(element, element_obj)
        subelement = ifc.createIfcBuilding()
        subelement_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(subelement, subelement_obj)
        assert subject.can_aggregate(element_obj, subelement_obj) is True

    def test_spatial_elements_and_projects_can_aggregate_2x3(self):
        ifc = ifcopenshell.file(schema="IFC2X3")
        tool.Ifc.set(ifc)
        element = ifc.createIfcProject()
        element_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(element, element_obj)
        subelement = ifc.createIfcBuilding()
        subelement_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(subelement, subelement_obj)
        assert subject.can_aggregate(element_obj, subelement_obj) is True

    def test_unlinked_elements_cannot_aggregate(self):
        ifc = ifcopenshell.file()
        tool.Ifc.set(ifc)
        element_obj = bpy.data.objects.new("Object", None)
        subelement_obj = bpy.data.objects.new("Object", None)
        assert subject.can_aggregate(element_obj, subelement_obj) is False

    def test_aggregates_with_meshes_are_invalid(self):
        ifc = ifcopenshell.file()
        tool.Ifc.set(ifc)
        element = ifc.createIfcElementAssembly()
        element_obj = bpy.data.objects.new("Object", bpy.data.meshes.new("Mesh"))
        tool.Ifc.link(element, element_obj)
        subelement = ifc.createIfcBeam()
        subelement_obj = bpy.data.objects.new("Object", None)
        tool.Ifc.link(subelement, subelement_obj)
        assert subject.can_aggregate(element_obj, subelement_obj) is False


class TestDisableEditing(NewFile):
    def test_run(self):
        obj = bpy.data.objects.new("Object", None)
        subject.enable_editing(obj)
        subject.disable_editing(obj)
        assert obj.BIMObjectAggregateProperties.is_editing is False


class TestEnableEditing(NewFile):
    def test_run(self):
        obj = bpy.data.objects.new("Object", None)
        subject.enable_editing(obj)
        assert obj.BIMObjectAggregateProperties.is_editing is True


class TestGetContainer(NewFile):
    def test_run(self):
        ifc = ifcopenshell.file()
        tool.Ifc.set(ifc)
        element = ifc.createIfcWall()
        container = ifc.createIfcBuildingStorey()
        ifcopenshell.api.run("spatial.assign_container", ifc, products=[element], relating_structure=container)
        assert subject.get_container(element) == container
