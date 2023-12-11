import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import glob
import czifile
import tifffile

# Path to the directory containing CZI images
input_path = "/Users/juanpablomayaarteaga/Desktop/Confocal_MOR/Mor_S3_DG/Otro_formato/"

# Output directory for TIFF images
output_path = f"{input_path}TIF/"
os.makedirs(output_path, exist_ok=True)



# DEF

def list_czi_images(directory):
    czi_images = glob.glob(directory + "/*.czi")
    return czi_images





# List all CZI images in the input directory
im_list = list_czi_images(input_path)
print(im_list)



"""
# Loop through each CZI image
for image_path in im_list:
    # Open the CZI file
    with czifile.CziFile(image_path) as czi:
        # Get the pixel data as a numpy array
        data = czi.asarray()
        
        # Print the shape of the image
        print(f"Image {image_path} shape:", data.shape)

"""

# Loop through each CZI image
for image_path in im_list:
    # Open the CZI file
    with czifile.CziFile(image_path) as czi:
        # Get the pixel data as a numpy array
        data = czi.asarray()
        

        # Select the desired channel (assuming the channel dimension is the second dimension)
        #channel_data = data[0, 0, 0, :, :, 0]
        #channel_data = data[0, 0, 0, 0, :, :, :, :]
        channel_data = data[:, :, :, :]

        # Perform maximum projection along the desired axis
        maximum_projection = np.max(channel_data, axis=0)

        # Get the base filename of the CZI image
        base_filename = os.path.splitext(os.path.basename(image_path))[0]

        # Create the output filename for the TIFF image
        output_filename = os.path.join(output_path, base_filename + ".tif")

        # Save the maximum projection as a TIFF file
        tifffile.imwrite(output_filename, maximum_projection)

        # Display the maximum projection using Matplotlib
        plt.imshow(maximum_projection, cmap='gray')
        plt.show()
        
        


