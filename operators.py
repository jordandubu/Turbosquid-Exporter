import bpy, os, subprocess
from .utils import test_connection, setup_wireframe_material, replace_material, render_scene
from .__init__ import ADDON_NAME

class TestConnectionOperator(bpy.types.Operator):
    bl_idname = "object.test_connection"
    bl_label = "Test Connection"

    def execute(self, context):
        api_key = context.scene.api_key
        member_id = context.scene.member_id
        if test_connection(api_key, member_id):
            self.report({'INFO'}, "Connection succeeded")
        else:
            self.report({'ERROR'}, "Connection failed")
        return {'FINISHED'}

class RenderingOperator(bpy.types.Operator):
    bl_idname = "object.rendering_operator"
    bl_label = "RENDER"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_scene = bpy.context.window.scene
        collection = context.scene.my_collection
        export_path = context.scene.export_path

        imported_scenes = []  # Étape 1: Liste pour conserver les scènes importées

        if collection is None:
            self.report({'ERROR'}, "No collection selected")
            return {'CANCELLED'}

        dir_path = os.path.dirname(os.path.realpath(__file__))
        blend_file_name = context.scene.render_scene
        blend_file_path = os.path.join(context.preferences.addons[ADDON_NAME].preferences.library_path, blend_file_name)

        with bpy.data.libraries.load(blend_file_path) as (data_from, _):
            all_scene_names = data_from.scenes

        num_scenes = len(all_scene_names)

        for index, scene_name in enumerate(all_scene_names):
            new_scene = bpy.data.scenes.get(scene_name)

            if new_scene is None:
                with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
                    data_to.scenes = [scene_name]
                new_scene = bpy.data.scenes.get(scene_name)
                if new_scene is None:
                    self.report({'ERROR'}, f"Scene '{scene_name}' not found")
                    return {'CANCELLED'}

                imported_scenes.append(new_scene)  # Ajoutez la nouvelle scène à la liste

            bpy.context.window.scene = new_scene

            # Importer la collection
            if collection.name not in new_scene.collection.children:
                new_scene.collection.children.link(collection)

            if scene_name == "wire":
                render_scene(new_scene, scene_name, export_path, shading_type='SOLID')
            else:
                render_scene(new_scene, scene_name, export_path)

            wm = context.window_manager
            wm.progress_begin(0, num_scenes)
            wm.progress_update(index)
            wm.progress_end()

        # Étape 2 : Supprimez toutes les scènes importées
        for scene in imported_scenes:
            bpy.data.scenes.remove(scene)

        # Étape 3 : Réglez la scène actuelle sur la scène d'origine
        bpy.context.window.scene = current_scene
        return {'FINISHED'}


class ImportSceneOperator(bpy.types.Operator):
    """Import all scenes from a specified .blend file and link a specified collection to each imported scene"""
    bl_idname = "scene.import_scene"
    bl_label = "Import Selected Scene"

    def execute(self, context):
        scene_name = context.scene.render_scene
        collection_name = context.scene.my_collection

        if not scene_name:
            self.report({'WARNING'}, "No scene file specified")
            return {'CANCELLED'}

        if not collection_name:
            self.report({'WARNING'}, "No collection specified")
            return {'CANCELLED'}

        blend_file_path = os.path.join(context.preferences.addons[ADDON_NAME].preferences.library_path, scene_name)

        if not os.path.exists(blend_file_path):
            self.report({'ERROR'}, f"File not found: {blend_file_path}")
            return {'CANCELLED'}

        with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
            data_to.scenes = data_from.scenes
            data_to.objects = data_from.objects

        for imported_scene_name in data_to.scenes:
            imported_scene = bpy.data.scenes[imported_scene_name]
            bpy.context.window.scene = imported_scene

            # Liez la collection spécifiée comme instance de collection
            if collection_name in bpy.data.collections:
                collection = bpy.data.collections[collection_name]
                instance = bpy.data.objects.new(name=collection.name + "_instance", object_data=None)
                instance.instance_type = 'COLLECTION'
                instance.instance_collection = collection
                imported_scene.collection.objects.link(instance)
            else:
                self.report({'WARNING'}, f"Collection '{collection_name}' not found")

        self.report({'INFO'}, f"Imported scenes from {blend_file_path}")
        return {'FINISHED'}




class ImportHelperBoxOperator(bpy.types.Operator):
    bl_idname = "object.import_helper_box"
    bl_label = "Import Helper Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        blend_file_name = context.scene.render_scene  # ceci est seulement le nom du fichier
        blend_file_path = os.path.join(context.preferences.addons[ADDON_NAME].preferences.library_path, blend_file_name)
        
        with bpy.data.libraries.load(blend_file_path, link=True) as (data_from, data_to):  # Notez que 'link' est à True
            # Importer la collection "helperbox" si elle est disponible
            if "helperbox" in data_from.collections:
                data_to.collections = ["helperbox"]

        if not data_to.collections:
            self.report({'ERROR'}, "Collection 'helperbox' not found in the .blend file!")
            return {'CANCELLED'}

        # Créer une instance de la collection "helperbox" dans la scène courante
        instance = bpy.data.objects.new("helperbox_instance", object_data=None)
        instance.instance_type = 'COLLECTION'
        instance.instance_collection = data_to.collections[0]
        context.scene.collection.objects.link(instance)

        return {'FINISHED'}





class CreateProductOperator(bpy.types.Operator):
    bl_idname = "object.create_product"
    bl_label = "Create Product"

    def execute(self, context):
        for ob in context.selected_objects:
            print(ob)
        return {'FINISHED'}

class OpenLibraryPathOperator(bpy.types.Operator):
    bl_idname = "object.open_library_path"
    bl_label = "Open Library Path"
    bl_description = "Open the library path in the file explorer"
    
    def execute(self, context):
        library_path = context.preferences.addons[ADDON_NAME].preferences.library_path
        path = bpy.path.abspath(library_path)

        
        if os.path.exists(path):
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', path])
            elif sys.platform == 'linux':  # Linux
                subprocess.run(['xdg-open', path])
            else:
                self.report({'WARNING'}, "Could not open the directory")
                return {'CANCELLED'}


        else:
            self.report({'WARNING'}, "Path does not exist")
            return {'CANCELLED'}

        return {'FINISHED'}