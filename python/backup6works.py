import shutil
import os
import sys

# Change working directory
os.chdir(sys.path[0])

def find_in_drive(filename, drive_root):
    """ Recursively search for a file in the 'drive' directory and return its path if found. """
    for root, dirs, files in os.walk(drive_root):
        if filename in files:
            return os.path.join(root, filename)
    return None

def backup(src_dir='docs', dst_dir='drive', tolerance=1):
    # Get the paths for the source and destination directories
    src_path = os.path.join(sys.path[0], src_dir)
    dst_path = os.path.join(sys.path[0], dst_dir)
    new_docs_path = os.path.join(dst_path, "new docs")

    # Create 'new docs' directory if it doesn't exist
    if not os.path.exists(new_docs_path):
        os.makedirs(new_docs_path)

    # Function to recursively iterate through the source folder
    for root, dirs, files in os.walk(src_path):
        for file in files:
            # Full path for the current file in docs (source)
            file_path_src = os.path.join(root, file)

            # Reconstruct the relative path from docs (source) to drive (destination)
            relative_path = os.path.relpath(file_path_src, src_path)

            # Check if the file exists anywhere in the drive folder
            file_path_dst = find_in_drive(file, dst_path)

            if file_path_dst:
                # Check if the file in docs was modified more recently than the one in drive
                last_modified_src = os.path.getmtime(file_path_src)
                last_modified_dst = os.path.getmtime(file_path_dst)

                # Only copy if the source file is more than 1 second newer than the destination file
                if last_modified_src > last_modified_dst + tolerance:
                    print("Copying newer version of {}".format(relative_path))
                    shutil.copy2(file_path_src, file_path_dst)  # Copy from docs to drive
                else:
                    print("Not copying {}, drive version is up-to-date.".format(relative_path))
            else:
                # Copy the file to the 'new docs' folder if it doesn't exist anywhere in drive
                print("Copying new file {} to 'new docs'".format(relative_path))
                # Create the directory structure in 'new docs'
                new_file_path = os.path.join(new_docs_path, relative_path)
                if not os.path.exists(os.path.dirname(new_file_path)):
                    os.makedirs(os.path.dirname(new_file_path))
                shutil.copy2(file_path_src, new_file_path)

# Call the function with a tolerance of 1 second
backup()
