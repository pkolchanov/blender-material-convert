import random
import bpy
def get_random_color():
    ''' generate rgb using a list comprehension '''
    r, g, b = [random.random() for i in range(3)]
    return r, g, b


def create_material_nodes():
    ''' 
    Selects two random colors diffuse_colors from active material
    and creates cycles material
    '''
    active_material =  bpy.context.selected_objects[0].active_material
    active_material.use_nodes=True
    TreeNodes = active_material.node_tree
    links = TreeNodes.links
    colors = []

    for n in TreeNodes.nodes:
        try:
            colors.append(n.material.diffuse_color)
        except AttributeError as e:
            # print(e)
            pass
                
        TreeNodes.nodes.remove(n)

    while len(colors) < 2:
        colors.append(get_random_color())

    output_material = TreeNodes.nodes.new('ShaderNodeOutputMaterial')
    output_material.location = 542, 60

    shader = TreeNodes.nodes.new('ShaderNodeBsdfGlossy')
    shader.location = 333, 60

    mixer = TreeNodes.nodes.new('ShaderNodeMixRGB')
    mixer.location = 143, 60

    fresnel = TreeNodes.nodes.new('ShaderNodeFresnel')
    fresnel.location = -143, 60


    RGB1, RGB2 = TreeNodes.nodes.new('ShaderNodeRGB'), TreeNodes.nodes.new('ShaderNodeRGB')
    RGB1.location, RGB2.location = (-247, -51), (-56, -107)

    RGB1.outputs[0].default_value = random.choice(colors)[:]+(1,)
    RGB2.outputs[0].default_value =  random.choice(colors)[:]+(1,)
    links.new(RGB1.outputs[0], mixer.inputs[1])
    links.new(RGB2.outputs[0], mixer.inputs[2])

    links.new(fresnel.outputs[0], mixer.inputs[0])
    links.new(mixer.outputs[0], shader.inputs[0])
    links.new(shader.outputs[0], output_material.inputs[0])
    bpy.context.scene.render.engine = 'CYCLES'

class ConvertOperator(bpy.types.Operator):
    bl_idname = "ml.convert_active"
    bl_label = "Convert material from active object"
    bl_description = "Convert material from active object to Cycles redner engine"
    bl_register = True
    bl_undo = True

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        create_material_nodes()
        return {'FINISHED'}

class ConvertPanel(bpy.types.Panel):
    bl_label = "Convert material to Cycles"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        row = layout.row()
        row.operator("ml.convert_active",text='Convert material to Cycles')

def register():
    bpy.utils.register_class(ConvertOperator)
    bpy.utils.register_class(ConvertPanel)


def unregister():
    bpy.utils.unregister_class(ConvertOperator)
    bpy.utils.unregister_class(ConvertPanel)


if __name__ == "__main__":
    register()

