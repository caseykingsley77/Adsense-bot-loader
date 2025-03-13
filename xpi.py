import os
import zipfile

# Define the folder to compress
folder_to_compress = "auth_extension"
output_file = "auth.xpi"

# Create the ZIP file
with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(folder_to_compress):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, folder_to_compress)
            zipf.write(file_path, arcname)

print(f"Created {output_file} successfully!")