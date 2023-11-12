import bpy
class RenderingOperatorPanel(bpy.types.Panel):
    bl_label = "Turbosquid Exporter"
    bl_idname = "OBJECT_PT_turbosquid_exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Section Rendering
        box = layout.box()
        col = box.column()
        col.prop(scene, "show_rendering_section", text="Rendering", icon='TRIA_DOWN' if scene.show_rendering_section else 'TRIA_RIGHT', emboss=False)

        if scene.show_rendering_section:
            # Les autres éléments restent inchangés
            col.label(text="Collection to render:")
            col.prop(scene, "my_collection", text="")
            col.label(text="Export Path:")
            col.prop(scene, "export_path", text="")
            
            col.label(text="Render scene:")
            # Création d'une nouvelle ligne
            row = col.row()
            
            # Ajout du bouton avec l'icône "CUBE"
            row.operator("object.import_helper_box", text="", icon='CUBE')
            row.operator("object.open_library_path", icon='FILE_FOLDER', text="")

            # Ajout de la propriété "render_scene" à la même ligne
            row.prop(context.scene, "render_scene", text="")
            col.operator("object.rendering_operator")

        # Section Register
        box = layout.box()
        col = box.column()
        col.prop(scene, "show_register_section", text="Register", icon='TRIA_DOWN' if scene.show_register_section else 'TRIA_RIGHT', emboss=False)

        if scene.show_register_section:
            col.label(text="api_key:")
            col.prop(scene, "api_key", text="")
            col.label(text="member_id:")
            col.prop(scene, "member_id", text="")
            col.operator("object.test_connection")

        # Section Product Info
        box = layout.box()
        col = box.column()
        col.prop(scene, "show_product_info_section", text="Publish", icon='TRIA_DOWN' if scene.show_product_info_section else 'TRIA_RIGHT', emboss=False)

        if scene.show_product_info_section:

            col.prop(scene, "product_title", text="Title")

            col.prop(scene, "product_price", text="Price ($)")
            #col.label(text="Description: AUTO GENERATED")

            #col.template_text(scene, "product_description", "", text="")

            col.label(text="Geometry type:")
            col.prop(scene, "geometry_type", text="")

            col.label(text="Unwrapped uvs:")
            col.prop(scene, "unwrapped_uvs", text="")
            row = col.row()
            row2 = col.row()
            row3 = col.row()
            row.prop(scene, "is_textured")
            row.prop(scene, "is_material")
            row2.prop(scene, "is_rigged")
            row2.prop(scene, "is_animated")
            row3.prop(scene, "is_uv_mapped")
            col.label(text="Certification level:")
            col.prop(scene, "certification_level", text="")
            col.label(text="Product category:")
            col.prop(scene, "product_category", text="")
            col.label(text="3D Model License for Customers:")
            col.prop(scene, "customer_license", text="")

            col.operator("object.create_product")

