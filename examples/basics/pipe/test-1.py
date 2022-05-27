import blenderproc as bproc

import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()



import numpy as np
import bpy
import os
import random


blend_path = "examples/basics/pipe/test-1.blend"
segcolormap_path = "examples/basics/pipe/segmap.json"
output_dir = "examples/basics/pipe/output"

bproc.init()

# load the objects into the scene
objs = bproc.loader.load_blend(blend_path)

# define a light and set its location and energy level
light1 = bproc.types.Light()
light1.set_type("POINT")
light1.set_location([0.0648, -5.10561, 5.54109])
light1.set_energy(1000)

light2 = bproc.types.Light()
light2.set_type("POINT")
light2.set_location([5, -4.83221, 5])
light2.set_energy(1000)

light3 = bproc.types.Light()
light3.set_type("POINT")
light3.set_location([-0.342514 , -3.05966, 7.57489])
light3.set_energy(10.6)
light3.set_color([255, 0, 0])

# define the camera resolution
#bproc.camera.set_resolution(1560, 1040)
bproc.camera.set_resolution(390, 260)
bproc.camera.set_intrinsics_from_blender_params(lens=0.10)

line = [0, -16.671, 4.0742, 1.57, 0, 0]
position, euler_rotation = line[:3], line[3:6]
matrix_world = bproc.math.build_transformation_mat(position, euler_rotation)
bproc.camera.add_camera_pose(matrix_world)

# randomize screw distance and angle

num_variations = 2

for variation in range(0, num_variations):

    bpy.context.view_layer.objects.active = bpy.data.objects['Wrap 2']
    bpy.context.object.modifiers["Screw"].screw_offset = random.uniform(5, 5.3)
    bpy.context.object.modifiers["Screw"].angle = random.uniform(9.4, 9.5)

    data = bproc.renderer.render()

    # Render segmentation masks (per class and per instance)
    #data.update(bproc.renderer.render_segmap(map_by=["instance"], segcolormap_path=segcolormap_path, render_colorspace_size_per_dimension=255 ))
    data.update(bproc.renderer.render_segmap(map_by=["cp_label","instance"]))
    # write the data to a .hdf5 container
    bproc.writer.write_hdf5(os.path.join(output_dir, str(variation)), data)
