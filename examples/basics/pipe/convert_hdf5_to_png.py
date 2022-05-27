import h5py
import numpy as np
import glob
import pathlib
from PIL import Image
import matplotlib.pyplot as plt
import sys

input_dir= sys.argv[0]
output_dir = sys.argv[1]


for file in glob.glob(input_dir+'/*/*.hdf5'):
    
    p = pathlib.Path(file)
    name = p.parent.name
    hdf = h5py.File(file,'r')

    input_array = np.array(hdf["colors"]) 
    label_array = np.array(hdf["cp_label_segmaps"])
    img_input = Image.fromarray(input_array, 'RGB')
    input_dir= output_dir+"/data/"+name+".png"
    label_dir= output_dir+"label/"+name+".npy"
    pathlib.Path(input_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(label_dir).mkdir(parents=True, exist_ok=True)
    img_input.save(input_dir, "png")
    np.save(label_dir, label_array)

