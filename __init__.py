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


bl_info = {
    "name": "3D Market Exporter",
    "description": "Create renders, generate description",
    "author": "Jordan Dubu - Doyorn",
    "version": (1, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Tool Shelf > Turbosquid Tab",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

from . import properties
ADDON_NAME = "Turbosquid Exporter"

def register():
    properties.register()

def unregister():
    properties.unregister()

if __name__ == "__main__":
    register()
