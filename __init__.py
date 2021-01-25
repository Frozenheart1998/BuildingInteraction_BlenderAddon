# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import bmesh
import os

bl_info = {
    "name" : "test",
    "author" : "lincoln",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

class TEST_OT_adjust(bpy.types.Operator):
    bl_idname = "lincoln.adjust"
    bl_label = "adjust"
    bl_options = {"REGISTER","UNDO"}

    # my_float: number of extrdusion
    my_float: bpy.props.FloatProperty(name="Number of Adjustment")

    def execute(self, context):
        print(self.my_float)
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(self.my_float, 0, 0)})
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class TEST_OT_reset(bpy.types.Operator):
    bl_idname = "lincoln.reset"
    bl_label = "reset"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.data.objects[0].select_set( state = True )

        bpy.ops.object.delete()
        bpy.ops.import_scene.obj(filepath='./Building.obj', axis_forward='-Z', axis_up='Y')

        bpy.context.view_layer.objects.active = bpy.data.objects[0]

        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        

class TEST_OT_save(bpy.types.Operator):
    bl_idname = "lincoln.save"
    bl_label = "save"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path)
        target_file = os.path.join(directory, 'NewBuilding.obj')

        bpy.ops.export_scene.obj(filepath=target_file)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class TEST_PT_Interaction(bpy.types.Panel):
    bl_idname = "TEST_PT_Interaction"
    bl_label = "Interaction test"

    # label category
    bl_category = "Tool"

    # ui_type
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "mesh_edit"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Interaction",icon="BLENDER")
        row = layout.row()

        # generate button
        row.operator("lincoln.adjust",text="Adjust",icon="CUBE").my_float = 0
        row.operator("lincoln.reset",text="Reset",icon="CUBE")
        row.operator("lincoln.save",text="save",icon="CUBE")



def register():
    bpy.utils.register_class(TEST_OT_adjust)
    bpy.utils.register_class(TEST_OT_reset)
    bpy.utils.register_class(TEST_OT_save)
    bpy.utils.register_class(TEST_PT_Interaction)
    ...

def unregister():
    bpy.utils.unregister_class(TEST_PT_Interaction)
    ...
