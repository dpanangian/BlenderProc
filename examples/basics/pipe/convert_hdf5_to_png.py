import h5py
import numpy as np
import glob
import pathlib
from PIL import Image
import matplotlib.pyplot as plt
import sys
import io

def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    import matplotlib as mpl
    import numpy as np
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)

input_dir= sys.argv[1]
output_dir = sys.argv[2]

print(input_dir)

print(output_dir)
for file in glob.glob(input_dir+'/*/*.hdf5'):
    
    p = pathlib.Path(file)
    name = p.parent.name
    hdf = h5py.File(file,'r')

    input_array = np.array(hdf["colors"]) 
    label_array = np.array(hdf["cp_label_segmaps"])
    img_input = Image.fromarray(input_array, 'RGB')
    input_dir= output_dir+"/data/"
    label_dir= output_dir+"/label/"
    pathlib.Path(input_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(label_dir).mkdir(parents=True, exist_ok=True)
    img_input.save(input_dir+name+".png", "png")
    plt.axis('off')
    colors = [(128,0,0), (0,0,128), (0,0,0), (0,0,128), (0,0,128)] # This example uses the 8-bit RGB
    ### Call the function make_cmap which returns your colormap
    cmap = make_cmap(colors, bit=True)
    plt.imshow(label_array,cmap=cmap, vmin=0, vmax=len(colors)-1)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,bbox_inches='tight',pad_inches = 0, dpi=300)
    buf.seek(0)
    img = Image.open(buf)
    img = img.resize((1560,1040))
    img.save(pathlib.Path(label_dir) / (name+".png"), 'png')

