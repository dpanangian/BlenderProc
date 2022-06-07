import bpy


bpy.context.scene.render.filepath = "C:/Users/danie/Pictures/image.png"
bpy.ops.render.render(write_still = True)