# Import
import bpy
import os
from bpy.props import *
from bpy.types import Panel, Operator, Menu
from bpy.utils import previews
from bpy.types import WindowManager
from . import addon_updater_ops

preview_collections = {}

class PBRMaterialPanel(bpy.types.Panel):
    bl_label = "PBR Materials"
    bl_idname = "pbr_previews"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    
    def draw_header(self, context):
        settings = context.scene.pbr_material_settings
        layout = self.layout
        layout.prop(settings, 'enabled', text='')
    
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'CYCLES' and context.active_object.material_slots.data.active_material

    # Panel
    def draw(self, context):
        addon_updater_ops.check_for_update_background(context)
        settings = context.scene.pbr_material_settings
        layout = self.layout
        scn = bpy.context.scene
        layout.enabled = settings.enabled

        # Category
        col = layout.column(align=True)
        row = col.row(align=True)
        row.alignment = 'CENTER'
        row.prop(settings, 'category', text="Category", expand=True)
        
        if settings.category == 'd':
            # Dielectrics
            material_name = context.scene.thumbs_mats_dielectrics
            thumbs = "thumbs_mats_dielectrics"   
        else:
            # Metals
            material_name = context.scene.thumbs_mats_metals
            thumbs = "thumbs_mats_metals"

        # Previews
        row = col.row()
        row.template_icon_view(scn, thumbs, show_labels=True)

        # Material Name
        row = col.row(align=True)
        row.alignment = 'CENTER'
        row.label(material_name)

        # Updater
        addon_updater_ops.update_notice_box_ui(self, context)


###############################################################################################################################à


# Add Material
def add_material(self, context):
    settings = context.scene.pbr_material_settings
    path = os.path.join(os.path.dirname(__file__), "blends" + os.sep + "dielectrics.blend")

    if settings.category == 'd':
        node_name = context.scene.thumbs_mats_dielectrics
        if node_name in ("Fire", "Grass", "Hair", "Leaf", "Paper", "Particles", "Transparent", "Velvet"):
            with bpy.data.libraries.load(path, False) as (data_from, data_to):
                if not node_name in bpy.data.node_groups:
                    data_to.node_groups = [node_name]
    else:
        node_name = context.scene.thumbs_mats_metals

    active_mat = bpy.context.active_object.active_material

    # Output
    active_mat.use_nodes = True
    active_mat.node_tree.nodes.clear()    
    preview_type = active_mat.preview_render_type
    output = active_mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    output.location = (200, 0)

    # Dielectrics
    if node_name=="Dielectric":
        princi = principled(node_name, active_mat, output)
        princi.inputs[7].default_value = (0)
    elif node_name=="Acrylic Paint Black":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.05, 0.05, 0.05, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0)
    elif node_name=="Acrylic Paint White":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0)
    elif node_name=="Asphalt New":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.02, 0.02, 0.02, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.55)
    elif node_name=="Asphalt Old":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.12, 0.12, 0.12, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.55)
    elif node_name=="Brick":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.231, 0.148, 0.109, 1)
        princi.inputs[5].default_value = (0.55)
        princi.inputs[7].default_value = (0.78)
    elif node_name=="Car Paint":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0, 0.083, 0.457, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.25)
        princi.inputs[12].default_value = (1)
    elif node_name=="Ceramic":
        princi = principled(node_name, active_mat, output)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 0.898, 0.716, 1)
        princi.inputs[0].default_value = (0.6, 0.6, 0.6, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.6, 0.6, 0.6, 1)
        princi.inputs[5].default_value = (0.525)
        princi.inputs[7].default_value = (0)
    elif node_name=="Cloth":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.065, 0.08, 0.254, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.8)
        princi.inputs[10].default_value = (5)
        princi.inputs[11].default_value = (0.5)
    elif node_name=="Concrete":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.235, 0.231, 0.201, 1)
        princi.inputs[5].default_value = (1.163)
        princi.inputs[7].default_value = (0.74)
    elif node_name=="Light":
        emission = active_mat.node_tree.nodes.new("ShaderNodeEmission")
        blackbody = active_mat.node_tree.nodes.new("ShaderNodeBlackbody")
        blackbody.location = (-200, 0)
        blackbody.inputs[0].default_value = (3000)
        active_mat.node_tree.links.new(blackbody.outputs[0], emission.inputs[0])
        active_mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    elif node_name=="Mud":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.349, 0.25, 0.167, 1)
        princi.inputs[5].default_value = (2.225)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Plaster":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.66, 0.66, 0.66, 1)
        princi.inputs[5].default_value = (0.438)
        princi.inputs[7].default_value = (0.86)
    elif node_name=="Plastic":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.448, 0.013, 0.007, 1)
        princi.inputs[5].default_value = (0.375)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Rock":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.33, 0.33, 0.33, 1)
        princi.inputs[5].default_value = (0.588)
        princi.inputs[7].default_value = (0.81)
    elif node_name=="Rubber":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.047, 0.047, 0.047, 1)
        princi.inputs[5].default_value = (0.375)
        princi.inputs[7].default_value = (0.79)
    elif node_name=="Rust":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.187, 0.027, 0.004, 1)
        princi.inputs[5].default_value = (0.475)
        princi.inputs[7].default_value = (0.82)
    elif node_name=="Sand":
        princi = principled(node_name, active_mat, output)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 1, 1, 1)
        princi.inputs[0].default_value = (0.47, 0.367, 0.166, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.47, 0.367, 0.166, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.8)
        princi.inputs[10].default_value = (1)
        princi.inputs[11].default_value = (0)
    elif node_name=="Skin":
        princi = principled(node_name, active_mat, output)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 0, 0, 1)
        princi.inputs[0].default_value = (0.604, 0.326, 0.261, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.604, 0.326, 0.261, 1)
        princi.inputs[5].default_value = (0.375)
        princi.inputs[7].default_value = (0.5)
    elif node_name=="Snow":
        princi = principled(node_name, active_mat, output)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 0.97, 0.95, 1)
        princi.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.8, 0.8, 0.8, 1)
        princi.inputs[5].default_value = (1.25)
        princi.inputs[7].default_value = (0.5)
    elif node_name=="Wax":
        princi = principled(node_name, active_mat, output)
        color = rgb(princi, active_mat)
        color.outputs[0].default_value = (1, 0.397, 0.16, 1)
        princi.inputs[0].default_value = (0.263, 0.084, 0.222, 1)
        princi.inputs[1].default_value = (1)
        princi.inputs[3].default_value = (0.263, 0.084, 0.222, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.3)
    elif node_name=="Wood":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.61, 0.398, 0.228, 1)
        princi.inputs[5].default_value = (0.5)
        princi.inputs[7].default_value = (0.68)

    # Translucent and Volume
    if node_name in ("Grass", "Hair", "Leaf", "Paper", "Transparent", "Velvet"):
        groupnode(node_name, active_mat, output)
    elif node_name in ("Fire", "Particles"):
        group = active_mat.node_tree.nodes.new("ShaderNodeGroup")
        group.node_tree = bpy.data.node_groups[node_name]
        active_mat.node_tree.links.new(group.outputs[0], output.inputs[1])

    # Metals
    if node_name=="Aluminium":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.815, 0.831, 0.839, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Brass":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.956, 0.791, 0.305, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Bronze":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.973, 0.429, 0.15, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Chromium":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.262, 0.258, 0.283, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Cobalt":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.392, 0.386, 0.361, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Copper":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.973, 0.356, 0.246, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Gallium":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.479, 0.604, 0.578, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Gold":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.973, 0.539, 0.109, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Iron":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.552, 0.571, 0.571, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Lead":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.591, 0.591, 0.591, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Mercury":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.584, 0.571, 0.571, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0)
    elif node_name=="Molybdenum":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.429, 0.445, 0.361, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Nickel":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.392, 0.323, 0.235, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Pewter":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.515, 0.456, 0.392, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Platinum":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.429, 0.381, 0.314, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Pot":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.815, 0.831, 0.839, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.3)
        princi.inputs[8].default_value = (1)
    elif node_name=="Rhodium":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.468, 0.381, 0.392, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Silver":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.93, 0.913, 0.831, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Tin":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.776, 0.776, 0.776, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Titanium":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.262, 0.209, 0.165, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Tungsten":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.319, 0.319, 0.309, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Vanadium":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.407, 0.451, 0.429, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    elif node_name=="Zinc":
        princi = principled(node_name, active_mat, output)
        princi.inputs[0].default_value = (0.591, 0.546, 0.462, 1)
        princi.inputs[4].default_value = (1)
        princi.inputs[7].default_value = (0.1)
    
    # Hack to refresh the preview
    active_mat.preview_render_type = preview_type


# Principled
def principled(node_name, active_mat, output):
    principled = active_mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    principled.name = node_name
    active_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    return principled

# RGB
def rgb(principled, active_mat):
    rgbnode = active_mat.node_tree.nodes.new("ShaderNodeRGB")
    rgbnode.location = (-200, 0)
    active_mat.node_tree.links.new(rgbnode.outputs[0], principled.inputs[2])
    return rgbnode

# Group
def groupnode(node_name, active_mat, output):
    group = active_mat.node_tree.nodes.new("ShaderNodeGroup")
    group.node_tree = bpy.data.node_groups[node_name]
    active_mat.node_tree.links.new(group.outputs[0], output.inputs[0])


# Generate Previews
def generate_previews(metals):
    if metals:
        previews = preview_collections["pbr_materials_metals"]
    else:
        previews = preview_collections["pbr_materials_dielectrics"]
    image_location = previews.images_location
    enum_items = []    
    # Generate the thumbnails
    for i, image in enumerate(os.listdir(image_location)):
        filepath = os.path.join(image_location, image)
        thumb = previews.load(filepath, filepath, 'IMAGE')
        enum_items.append((image, image, "", thumb.icon_id, i))
    enum_items.sort()
    return enum_items


###################################################################################################################


# Register
def register():
    previews_mat_metals = bpy.utils.previews.new()
    previews_mat_dielectrics = bpy.utils.previews.new()

    previews_mat_metals.images_location = os.path.join(os.path.dirname(__file__), "thumbs/m")
    previews_mat_dielectrics.images_location = os.path.join(os.path.dirname(__file__), "thumbs/d")

    preview_collections['pbr_materials_metals'] = previews_mat_metals
    preview_collections['pbr_materials_dielectrics'] = previews_mat_dielectrics

    # Previews Dielectrics and Metals
    bpy.types.Scene.thumbs_mats_metals = bpy.props.EnumProperty(
        items=generate_previews(True),
        description="Choose the material you want to use",
        update=add_material,
        default='Gold'
    )
    bpy.types.Scene.thumbs_mats_dielectrics = bpy.props.EnumProperty(
        items=generate_previews(False),
        description="Choose the material you want to use",
        update=add_material,
        default='Dielectric'
    )

# Unregister
def unregister():
    for preview in preview_collections.values():
        bpy.utils.previews.remove(preview)
    preview_collections.clear()

    del bpy.types.Scene.thumbs_mats_metals
    del bpy.types.Scene.thumbs_mats_dielectrics
