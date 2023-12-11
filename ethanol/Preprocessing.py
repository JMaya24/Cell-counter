import os
import numpy as np
import matplotlib.pyplot as plt
import glob
from skimage import io, exposure, filters, morphology, feature, measure, segmentation, restoration, color
import cv2
import pandas as pd


def list_png_files(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files


# Parameters
region = "PCM"
groups = ["H-alc", "H-ctr", "M-alc", "M-ctr"]
subjects = ["04", "06", "07", "03", "23", "47", "24", "43", "85", "46", "87"]
cells = ["Neun"]

#"GFAP", "Iba", 

results = []

for group in groups:
    for subject in subjects:
        for cell in cells:
            input_path = f"/Users/juanpablomayaarteaga/Desktop/Inmuno/{region}/{group}/{subject}/{cell}"
            im_list = list_png_files(input_path)
            
            for im in im_list:
                image = io.imread(im)
    
                # Non-local Means Denoising
                denoised_image = restoration.denoise_nl_means(image, patch_size=5, patch_distance=7, h=0.1)
                
                denoised_path = os.path.join(input_path, "Denoised")
                os.makedirs(denoised_path, exist_ok=True)
    
                plt.imshow(denoised_image, cmap='gray')
                plt.axis('off')
                plt.savefig(os.path.join(denoised_path, f"{os.path.splitext(os.path.basename(im))[0]}_denoised.png"),
                            bbox_inches="tight", pad_inches=0, format="png", dpi=1200)
                plt.close()
        
            thresholding_path = os.path.join(input_path, "Thresholding")
            os.makedirs(thresholding_path, exist_ok=True)
    
            for im in im_list:
                image = io.imread(im)
    
                # Apply Sauvola thresholding
                window_size = 51  # Adjust this value according to the size of your cells
                thresholded_image = filters.threshold_sauvola(image, window_size)
    
                # Convert thresholded image to binary
                binary_image = image > thresholded_image
    
                # Save the thresholded image
                output_filename = os.path.splitext(os.path.basename(im))[0] + "_thresholded.png"
                output_filepath = os.path.join(thresholding_path, output_filename)
                io.imsave(output_filepath, binary_image.astype(np.uint8) * 255)
    
            segmantation_path = os.path.join(input_path, "Segmentation")
            os.makedirs(segmantation_path, exist_ok=True)
    
            for im in im_list:
                image = io.imread(im)
    
                if image.shape[2] == 4:
                    # Extract only RGB channels and discard the alpha channel
                    image = image[:, :, :3]
    
                # Convert image to grayscale
                image_gray = color.rgb2gray(image)
    
                # Convert image to binary
                binary_image = (image_gray > 0).astype(np.uint8)  # Adjust the threshold value as needed
    
                # Morphological operations to remove small noise - opening
                kernel = np.ones((3, 3), np.uint8)
                opening = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=1)
    
                # Perform connected component labeling
                labeled_image = measure.label(opening)
    
                # Measure properties of labeled regions
                regions = measure.regionprops(labeled_image)
    
                # Count objects and their areas
                num_objects = len(regions)
                areas = [region.area for region in regions]
                total_area = sum(areas)
                max_area = max(areas)
    
                # Calculate density (total area / cell number)
                density = total_area / num_objects
    
                # Convert area from pixels to microns
                conversion_factor = 850.19 / 512
                areas = [area * conversion_factor for area in areas]
                total_area = total_area * conversion_factor
                max_area = max_area * conversion_factor
    
                # Extract the slice name from the image filename
                slice_name = os.path.splitext(os.path.basename(im))[0].split("_")[0]
    
                # Store the results in a dictionary
                result = {
                    "subject": subject,
                    "group": group,
                    "region": region,
                    "cell": cell,
                    "slice": slice_name,
                    "cell_number": num_objects,
                    "total_area": total_area,
                    "max_area": max_area,
                    "density": density
                }
                results.append(result)

# Create a dataframe from the results
df = pd.DataFrame(results)

output_path = f"/Users/juanpablomayaarteaga/Desktop/Inmuno/{region}"
os.makedirs(output_path, exist_ok=True)

for group in groups:
    for subject in subjects:
        output_filename = f"{subject}_{group}_{region}.xlsx"
        output_filepath = os.path.join(output_path, group, output_filename)
    
        # Filter the dataframe based on group and subject
        filtered_df = df[(df["group"] == group) & (df["subject"] == subject)]
    
        # Save the filtered dataframe as an Excel file
        filtered_df.to_excel(output_filepath, index=False)
        print(f"Results for {subject}_{group} saved to {output_filepath}")
