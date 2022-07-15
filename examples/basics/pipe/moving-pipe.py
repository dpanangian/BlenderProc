import blenderproc as bproc
import time

import numpy as np
import bpy
import os
import random



blend_path = "examples/basics/pipe/moving_pipe_continuous_long_test.blend"
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
bproc.camera.set_resolution(1560, 1040)
#bproc.camera.set_resolution(390, 260)
bproc.camera.set_intrinsics_from_blender_params(lens=0.10)

line = [0, -16.671, 4.0742, 1.57, 0, 0]
position, euler_rotation = line[:3], line[3:6]
matrix_world = bproc.math.build_transformation_mat(position, euler_rotation)
bproc.camera.add_camera_pose(matrix_world)

#render-settings
my_areas = bpy.context.workspace.screens[0].areas
my_shading = 'SOLID'  # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'

for area in my_areas:
    for space in area.spaces:
        if space.type == 'VIEW_3D':
                space.shading.type = my_shading
                area.spaces[0].region_3d.view_perspective = 'CAMERA'

#put ovjects into collection
pipe_objects = ["Pipe", "Wrap 1", "Wrap 2", "Wrap dalem"]

#get z positions
positions = {obj:bpy.data.objects[obj].location.z for obj in pipe_objects}
num_images  = 0
num_variations = 100

for variation in range(0, num_variations):
    
    #inititate locations
    for obj in pipe_objects:
        bpy.data.objects[obj].location.z = positions[obj] - 0.4
    
    #randomize gaps
    bpy.context.view_layer.objects.active = bpy.data.objects['Wrap 2']
    bpy.context.object.modifiers["Screw"].screw_offset = random.uniform(5, 5.3)
    bpy.context.object.modifiers["Screw"].angle = random.uniform(9.4, 9.5)
    
    #move the pipe up and render
    move_by= 0.2
    frames = 4
    for frame in range(frames):
        for obj in pipe_objects:
            bpy.data.objects[obj].location.z = bpy.data.objects[obj].location.z + move_by
        
    
        #start = time.time()
        #data = bproc.renderer.render()
        #end = time.time()
        #print("Elapsed Time: ", end - start)
        # Render segmentation masks (per class and per instance)
        #bpy.ops.image.save_as(save_as_render=True, copy=True, filepath="//viewport-"+str(variation)+".png", show_multiview=False, use_multiview=False)
        #data.update(bproc.renderer.render_segmap(map_by=["instance"], segcolormap_path=segcolormap_path, render_colorspace_size_per_dimension=255 ))
        if not os.path.exists("C:\\Users\\danie\\Documents\\My Projects\\BlenderProc-dpana\\examples\\basics\\pipe\\output\\" + str(num_images) + ".png"):
            data =bproc.renderer.render_segmap(map_by=["cp_label","instance"])
            # write the data to a .hdf5 container
            bproc.writer.write_hdf5(os.path.join(output_dir, str(num_images)), data)
            
            #render    
            bpy.context.scene.render.filepath = "C:\\Users\\danie\\Documents\\My Projects\\BlenderProc-dpana\\examples\\basics\\pipe\\output\\" + str(num_images) + ".png"
            bpy.ops.render.opengl(write_still=True)
        
        
        num_images += 1
        print(num_images / (num_variations*frames))

