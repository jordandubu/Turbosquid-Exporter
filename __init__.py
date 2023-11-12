bl_info = {
    "name": "Turbosquid Exporter",
    "description": "Create renders, generate description",
    "author": "Jordan Dubu - Doyorn",
    "version": (1, 1),
    "blender": (3, 6, 5),
    "location": "View3D > Tool Shelf > Turbosquid Tab",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

from . import properties
ADDON_NAME = bl_info["name"]

def register():
    properties.register()

def unregister():
    properties.unregister()

if __name__ == "__main__":
    register()
