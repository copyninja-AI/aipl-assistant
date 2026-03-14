import io
import zipfile
import os

def create_zip_buffer(folder_path):
    """
    Creates a zip file in-memory from a local folder.
    Note: For a real cloud app, you'd generate file contents dynamically,
    rather than relying on pre-existing local files.
    """
    # Create an in-memory buffer to store the zip file
    zip_buffer = io.BytesIO()

    # Write the zip file to the buffer
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Walk through the directory and add files to the zip
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Ensure the path in the zip file is relative to the base folder
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname)

    # Crucial step: rewind the buffer to the beginning so st.download_button can read it
    zip_buffer.seek(0)
    return zip_buffer