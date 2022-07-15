import blenderproc as bproc
import time
import numpy as np
import bpy
import os
import random
random.seed(11)



blend_path = "examples/basics/pipe/alu_pipe_2.blend"
output_dir = "examples/basics/pipe/output"

bproc.init()

# load the objects into the scene
objs = bproc.loader.load_blend(blend_path)


# define a light and set its location and energy level
light1 = bproc.types.Light()
light1.set_type("POINT")
light1.set_location([5.01691, 4.14938, 5.34748])
light1.set_energy(100)

light2 = bproc.types.Light()
light2.set_type("POINT")
light2.set_location([6.33304, -5.44624 , 5.34748])
light2.set_energy(100)


# define the camera resolution
bproc.camera.set_resolution(1560, 1040)
#bproc.camera.set_resolution(390, 260)
bproc.camera.set_intrinsics_from_blender_params(lens=0.185)

line = [0, -16.671, 4.0742, 1.57, 0, 0]
position, euler_rotation = line[:3], line[3:6]
matrix_world = bproc.math.build_transformation_mat(position, euler_rotation)
bproc.camera.add_camera_pose(matrix_world)

pipe_objects = ["Plane.002", "Curve.001"]
#get z positions
positions = {obj:bpy.data.objects[obj].location.z for obj in pipe_objects}

num_variations = 3

for variation in range(0, num_variations):

    bpy.context.view_layer.objects.active = bpy.data.objects['Curve.001']
    bpy.context.object.scale[0] = random.uniform(11, 15)
    bpy.data.objects["Curve.001"].location.z = random.uniform(3, 3.8)
    bpy.data.objects["Curve.001"].location.x = random.uniform(-0.35, 0.35)
    
    data = bproc.renderer.render()
        #end = time.time()
        #print("Elapsed Time: ", end - start)
        # Render segmentation masks (per class and per instance)
        #bpy.ops.image.save_as(save_as_render=True, copy=True, filepath="//viewport-"+str(variation)+".png", show_multiview=False, use_multiview=False)
        #data.update(bproc.renderer.render_segmap(map_by=["instance"], segcolormap_path=segcolormap_path, render_colorspace_size_per_dimension=255 ))
    data.update(bproc.renderer.render_segmap(map_by=["cp_label","instance"]))
        # write the data to a .hdf5 container
    bproc.writer.write_hdf5(os.path.join(output_dir, str(variation)), data)

    my_areas = bpy.context.workspace.screens[0].areas
    shadings = ['SOLID', 'MATERIAL']  # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'
    for shading in shadings:
        for area in my_areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                        space.shading.type = shading
                        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        
        
        if not os.path.exists(f"C:\\Users\\danie\\Documents\\My Projects\\BlenderProc-dpana\\examples\\basics\\pipe\\output\\{shading.lower()}\\" + str(variation) + ".png"):
            #data =bproc.renderer.render_segmap(map_by=["cp_label","instance"])
            # write the data to a .hdf5 container
            #bproc.writer.write_hdf5(os.path.join(output_dir, str(num_images)), data)
            
            #render    
            bpy.context.scene.render.filepath = f"C:\\Users\\danie\\Documents\\My Projects\\BlenderProc-dpana\\examples\\basics\\pipe\\output\\{shading.lower()}\\" + str(variation) + ".png"
            bpy.ops.render.opengl(write_still=True)
