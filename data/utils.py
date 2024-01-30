import os
from data.constants import *


def remove_files_with_extension(folder_path, extension_to_remove):
    """
    Removes all files with the given extension in the given folder.
    """
    
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(extension_to_remove):
                file_path = os.path.join(subdir, file)
                try:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")


def load_data_path(root_path=TILES_PATH):
    """
    Returns a list of tuples (image_path, label_path) for the dataset.
    """
    
    data = {}
    
    drone_dirs = os.listdir(root_path)
    drone_dirs.sort()
    for drone_dir in drone_dirs:
        data[drone_dir] = {}
        image_dirs = os.listdir(os.path.join(TILES_PATH, drone_dir))
        image_dirs.sort()
        for image_dir in image_dirs:
            data[drone_dir][image_dir] = {}
            sub_dirs = os.listdir(os.path.join(TILES_PATH, drone_dir, image_dir))
            sub_dirs.sort()
            for sub_dir in sub_dirs:
                
                dir_path = os.path.join(TILES_PATH, drone_dir, image_dir, sub_dir)
                
                if sub_dir == GROUND_TRUTH:    
                    gt_imgs = [os.path.join(dir_path, path) for path in os.listdir(dir_path) if GROUND_TRUTH_EXTENSION in path]
                    data[drone_dir][image_dir][GROUND_TRUTH] = gt_imgs
                
                elif sub_dir == TILE:
                    if drone_dir == SEQUOIA:
                        dir_path = os.path.join(dir_path, SEQUIOA_CHANNEL)
                    elif drone_dir == RED_EDGE:
                        dir_path = os.path.join(dir_path, RED_EDGE_CHANNEL)
                    tile_imgs = [os.path.join(dir_path, path) for path in os.listdir(dir_path)]
                    data[drone_dir][image_dir][TILE] = tile_imgs
                    
                elif sub_dir == MASK:
                    mask_imgs = [os.path.join(dir_path, path) for path in os.listdir(dir_path)]
                    data[drone_dir][image_dir][MASK] = mask_imgs

    return data                  


# remove_files_with_extension(TILES_PATH, BLACKLIST)
# load_data_path()