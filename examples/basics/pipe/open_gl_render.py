import bpy


my_areas = bpy.context.workspace.screens[0].areas
my_shading = 'SOLID'  # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'

for area in my_areas:
    for space in area.spaces:
        if space.type == 'VIEW_3D':
            for shading in ['SOLID', 'MATERIAL']:
                bpy.context.scene.render.filepath = "C:/Users/danie/Pictures/image_"+shading+".png"
                space.shading.type = shading
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                bpy.ops.render.opengl(write_still=True)