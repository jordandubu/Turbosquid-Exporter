import requests
import bpy
import os


# Un nouvel opérateur pour tester la connexion à TurboSquid
def test_connection(api_key, member_id):
    url = "https://api.turbosquid.com/api/drafts"  # Remplacez par l'URL correcte de l'API
    headers = {
        "Accept": "application/vnd.api+json; com.turbosquid.api.version=1",
        "Authorization": f"Token {api_key}"
    }
    # Paramètres supplémentaires si nécessaire
    params = {
        "filter": {
            "member_id": member_id  # Utilisez le member_id passé en paramètre
        }
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return True
        else:
            print(f"Error {response.status_code}: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False
    
def setup_wireframe_material():
    """Crée un matériau wireframe et le retourne."""
    mat = bpy.data.materials.new(name="Wireframe_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    for node in nodes:
        nodes.remove(node)
    
    wire_shader = nodes.new(type="ShaderNodeBsdfDiffuse")
    wire_shader.location = (0,0)

    wireframe = nodes.new(type="ShaderNodeWireframe")
    wireframe.location = (-200,0)

    material_output = nodes.new(type="ShaderNodeOutputMaterial")
    material_output.location = (400,0)

    mat.node_tree.links.new(wire_shader.inputs[0], wireframe.outputs[0])
    mat.node_tree.links.new(material_output.inputs["Surface"], wire_shader.outputs["BSDF"])
    
    return mat


def replace_material(object, old_material, new_material):
    ob = object
    om = bpy.data.materials[old_material]
    nm = bpy.data.materials[new_material]
    for s in ob.material_slots:
        if s.material.name == old_material:
            s.material = nm


def render_scene(scene, scene_name, export_path, shading_type='RENDERED'):
    scene_export_path = os.path.join(export_path, scene_name)

    if not os.path.exists(scene_export_path):
        os.makedirs(scene_export_path)

    scene.render.image_settings.file_format = 'PNG'
    scene.render.use_file_extension = True
    scene.render.filepath = os.path.join(scene_export_path, scene_name)

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            original_shading_type = space.shading.type
            original_overlay_settings = {
                "show_wireframes": space.overlay.show_wireframes,
                "show_color_type": space.shading.color_type,
                "show_floor": space.overlay.show_floor,
                "show_axis_x": space.overlay.show_axis_x,
                "show_axis_y": space.overlay.show_axis_y,
                "show_axis_z": space.overlay.show_axis_z,
                "show_cursor": space.overlay.show_cursor,
                "show_outline_selected": space.overlay.show_outline_selected,
                "show_text": space.overlay.show_text,
                "show_object_origins": space.overlay.show_object_origins,
                "show_extra": space.overlay.show_extras
            }

            if shading_type != 'RENDERED':
                space.shading.type = shading_type
                if shading_type == 'SOLID':
                    bpy.ops.object.select_all(action='DESELECT')
                    space.overlay.show_wireframes = True
                    space.shading.color_type = 'THEME'
                    space.shading.wireframe_color_type = 'THEME'
                    space.overlay.show_floor = False
                    space.overlay.show_axis_x = False
                    space.overlay.show_axis_y = False
                    space.overlay.show_axis_z = False
                    space.overlay.show_cursor = False
                    space.overlay.show_outline_selected = False
                    space.overlay.show_text = False
                    space.overlay.show_object_origins = False
                    space.overlay.show_extras = False
                bpy.ops.view3d.view_camera()
                bpy.ops.render.opengl(animation=True)
                break
            else:
                bpy.ops.render.render('EXEC_DEFAULT', animation=True)

    space.shading.type = original_shading_type
    space.overlay.show_wireframes = original_overlay_settings["show_wireframes"]
    space.shading.color_type = original_overlay_settings["show_color_type"]
    space.overlay.show_floor = original_overlay_settings["show_floor"]
    space.overlay.show_axis_x = original_overlay_settings["show_axis_x"]
    space.overlay.show_axis_y = original_overlay_settings["show_axis_y"]
    space.overlay.show_axis_z = original_overlay_settings["show_axis_z"]
    space.overlay.show_cursor = original_overlay_settings["show_cursor"]
    space.overlay.show_outline_selected = original_overlay_settings["show_outline_selected"]
    space.overlay.show_text = original_overlay_settings["show_text"]
    space.overlay.show_object_origins = original_overlay_settings["show_object_origins"]
    space.overlay.show_extras = original_overlay_settings["show_extra"]