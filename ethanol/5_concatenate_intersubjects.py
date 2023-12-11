import os
import pandas as pd

region = "Crus"
sexs = ["M-", "H-"]
groups = ["alc", "ctr"]
subjects = ["03", "04", "06", "07", "23", "24", "35", "43", "46","47","49", "51", "85", "87"]
# subjects = ["04", "06", "07"] 

output_path = "/Users/juanpablomayaarteaga/Desktop/Inmuno/" + region + "/"
concatenated_df = pd.DataFrame()

for sex in sexs:
    for group in groups:
        for subject in subjects:
            excel_path = os.path.join(output_path, sex + group, subject)
            if not os.path.exists(excel_path):
                continue  # Skip if the directory doesn't exist
           
            # Iterate over the Excel files in the directory
            for file in os.listdir(excel_path):
                if file.endswith(".xlsx"):
                    # Read the Excel file
                    df = pd.read_excel(os.path.join(excel_path, file))
                    
                    concatenated_df = concatenated_df.append(df, ignore_index=True)
                   
if len(concatenated_df) > 0:
    # Save the concatenated DataFrame to a CSV file
    output_file = os.path.join(output_path, f"{region}.csv")
    concatenated_df.to_csv(output_file, index=False)
    # Print the path and file name of the CSV file produced
    print("CSV file saved:")
    print(output_file)
    # Display the contents of the concatenated DataFrame
    print(concatenated_df)
else:
    print("No Excel files found in the directories.")
