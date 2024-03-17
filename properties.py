#!/usr/bin/python3
# copyright (c) 2023 - DUBU JORDAN

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import os
import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty
)

from .operators import RenderingOperator, TestConnectionOperator, CreateProductOperator, ImportHelperBoxOperator, OpenLibraryPathOperator, ImportSceneOperator
from .panels import RenderingOperatorPanel
from .preferences import AddonPreferences
from .__init__ import ADDON_NAME


def get_render_scenes(self, context):
    items = []
    preferences = context.preferences.addons[ADDON_NAME].preferences
    library_path = preferences.library_path

    for file_name in os.listdir(library_path):
        if file_name.endswith(".blend"):
            items.append((file_name, file_name, ""))

    return items

bpy.types.Scene.render_scene = bpy.props.EnumProperty(
    items=get_render_scenes,
    name="Render Scene",
    description="Select the render scene"
)



def register():
    bpy.utils.register_class(ImportSceneOperator)
    bpy.types.Scene.show_rendering_section = bpy.props.BoolProperty(default=True, description="Toggle the rendering section")
    bpy.types.Scene.show_register_section = bpy.props.BoolProperty(default=True, description="Toggle the register section")
    bpy.types.Scene.show_product_info_section = bpy.props.BoolProperty(default=True, description="Toggle the product info section")

    bpy.utils.register_class(OpenLibraryPathOperator)
    bpy.utils.register_class(AddonPreferences)
    bpy.utils.register_class(TestConnectionOperator)
    bpy.utils.register_class(RenderingOperator)
    bpy.utils.register_class(CreateProductOperator)
    bpy.utils.register_class(RenderingOperatorPanel)
    bpy.utils.register_class(ImportHelperBoxOperator)
    bpy.types.Scene.my_collection = bpy.props.PointerProperty(type=bpy.types.Collection)

    bpy.types.Scene.api_key = StringProperty(name="API Key")
    bpy.types.Scene.member_id = StringProperty(name="Member ID")
    bpy.types.Scene.export_path = bpy.props.StringProperty(
        name="Export Path",
        default="/tmp\\market_renders",
        subtype='DIR_PATH'
    )

    bpy.types.Scene.product_title = StringProperty(name="Title")
    bpy.types.Scene.product_price = StringProperty(name="Price $")
    bpy.types.Scene.product_description = StringProperty(name="Description")
    bpy.types.Scene.geometry_type = bpy.props.EnumProperty(
        items=[
            ('QUADS', 'Polygonal Quads only', ''),
            ('QUADS_TRIS', 'Polygonal Quads/Tris', ''),
            ('TRIS', 'Polygonal Tris only', ''),
            # ... (autres options)
        ],
        name="Geometry"
    )
    bpy.types.Scene.unwrapped_uvs = bpy.props.EnumProperty(
        items=[
            ('YES_NON_OVERLAPPING', 'Yes, non-overlapping', ''),
            ('YES_OVERLAPPING', 'Yes, overlapping', ''),
            ('MIXED', 'Mixed', ''),
            # ... (autres options)
        ],
        name="Unwrapped UVs"
    )
    bpy.types.Scene.is_textured = BoolProperty(name="Textures")
    bpy.types.Scene.is_material = BoolProperty(name="Materials")
    bpy.types.Scene.is_rigged = BoolProperty(name="Rigged")
    bpy.types.Scene.is_animated = BoolProperty(name="Animated")
    bpy.types.Scene.is_uv_mapped = BoolProperty(name="UV Mapped")
    bpy.types.Scene.certification_level = bpy.props.EnumProperty(
        items=[
            ('NONE', 'None', ''),
            ('LITE', 'Lite', ''),
            ('PRO', 'Pro', ''),
        ],
        name="Certification"
    )
    bpy.types.Scene.product_category = StringProperty(name="Category")
    bpy.types.Scene.customer_license = bpy.props.EnumProperty(
        items=[
            ('NO', 'Games, movies, apparel and all normal uses are allowed for this model.', ''),
            ('YES', 'Editorial Uses Only required. Customers allowed include news, education, and organizations that have permission to use the depicted IP.', ''),
        ],
        name="3D Model License for Customers"
    )
    #Partie checkboxes
    bpy.types.Scene.rendering = bpy.props.BoolProperty(
        name="Rendering",
        description="Enable or disable rendering",
        default=False
    )
    
    bpy.types.Scene.turntable = bpy.props.BoolProperty(
        name="Turntable",
        description="Enable or disable turntable rendering",
        default=False
    )
    
    bpy.types.Scene.searchimage = bpy.props.BoolProperty(
        name="Search Image",
        description="Enable or disable search image rendering",
        default=False
    )
    
    bpy.types.Scene.wire = bpy.props.BoolProperty(
        name="Wire",
        description="Enable or disable wire rendering",
        default=False
    )

def unregister():
    bpy.utils.unregister_class(TestConnectionOperator)
    bpy.utils.unregister_class(RenderingOperator)
    bpy.utils.unregister_class(CreateProductOperator)
    bpy.utils.unregister_class(RenderingOperatorPanel)
    bpy.utils.unregister_class(AddonPreferences)
    bpy.utils.unregister_class(ImportHelperBoxOperator)
    bpy.utils.unregister_class(OpenLibraryPathOperator)
    bpy.utils.unregister_class(ImportSceneOperator)
    del bpy.types.Scene.rendering
    del bpy.types.Scene.turntable
    del bpy.types.Scene.searchimage
    del bpy.types.Scene.wire