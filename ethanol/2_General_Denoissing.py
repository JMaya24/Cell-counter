import os
import numpy as np
import matplotlib.pyplot as plt
import glob
from skimage import io, restoration
import time

def list_png_files(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files

region = "PCM"
groups = ["H-alc"]
subjects = ["04"]
cells = ["Neun"]

start_time = time.time()  # Start measuring time

for group in groups:
    for subject in subjects:
        for cell in cells:
            input_path = f"/Users/juanpablomayaarteaga/Desktop/Inmuno/{region}/{group}/{subject}/{cell}"
            im_list = list_png_files(input_path)
            denoised_images = []

            for im in im_list:
                image = io.imread(im)
                denoised_image = restoration.denoise_nl_means(image, patch_size=5, patch_distance=7, h=0.1)
                denoised_images.append(denoised_image)

            denoised_path = os.path.join(input_path, "Denoised")
            os.makedirs(denoised_path, exist_ok=True)

            for i, im in enumerate(im_list):
                denoised_image = denoised_images[i]
                plt.imshow(denoised_image, cmap='gray')
                plt.axis('off')
                plt.savefig(
                    os.path.join(denoised_path, f"{os.path.splitext(os.path.basename(im))[0]}_denoised.png"),
                    bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                plt.close()

end_time = time.time()  # Stop measuring time
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")
