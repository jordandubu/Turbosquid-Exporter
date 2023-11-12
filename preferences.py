import os
import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
from .__init__ import ADDON_NAME

class AddonPreferences(AddonPreferences):
    bl_idname = ADDON_NAME

    library_path: StringProperty(
        name="Library Path",
        subtype='DIR_PATH',
        default=os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Blender Foundation", "Blender", "3.6", "scripts", "addons", "Turbosquid Exporter", "render_scenes")
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "library_path")
