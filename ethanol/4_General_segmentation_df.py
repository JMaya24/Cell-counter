import os
import cv2
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
from skimage import io, color, measure, segmentation


def list_png_files(directory):
    png_files = glob.glob(directory + "/*.png")
    return png_files


region = "PCM"
groups = ["H-alc", "H-ctr", "M-alc", "M-ctr"]
subjects = ["04"]
cells = ["Neun"]

for group in groups:
    for subject in subjects:
        results = []  # Move this line here
        
        for cell in cells:
            input_path = f"/Users/juanpablomayaarteaga/Desktop/Inmuno/{region}/{group}/{subject}/{cell}/Threshold/"
            im_list = list_png_files(input_path)

            output_path = os.path.join(input_path, "Segmentation")
            os.makedirs(output_path, exist_ok=True)
        
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
        
        # Generate the output Excel filename
        csv_path = f"/Users/juanpablomayaarteaga/Desktop/Inmuno/{region}/{group}/{subject}"
        output_filename = f"{subject}_{group}_{region}.xlsx"
        output_filepath = os.path.join(csv_path, output_filename)
        
        # Save the dataframe as an Excel file
        df.to_excel(output_filepath, index=False)
        
        print(f"Results saved to {output_filepath}")
