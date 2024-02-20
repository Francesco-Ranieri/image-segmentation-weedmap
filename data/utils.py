import os
from enum import Enum
from PIL import Image
from data.processing import convert_to_black_and_white
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


class DroneEnum(Enum):
    RED_EDGE = RED_EDGE
    SEQUOIA = SEQUOIA



def load_data_path(root_path=TILES_PATH,                     
                   drone_to_load: list[DroneEnum] = [DroneEnum.RED_EDGE, DroneEnum.SEQUOIA],):
    """
    Returns a list of tuples (image_path, label_path) for the dataset.
    """
    
    data = {}
    
    drone_dirs = os.listdir(root_path)
    drone_dirs.sort()
    for drone_dir in drone_dirs:
        if DroneEnum(drone_dir) in drone_to_load:     
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
                        data[drone_dir][image_dir][TILE] = {}
                        channel_dirs = os.listdir(dir_path)
                        
                        for channel in  channel_dirs:
                            channel_path = os.path.join(dir_path, channel)
                            tile_imgs = [os.path.join(channel_path, path) for path in os.listdir(channel_path)]
                            data[drone_dir][image_dir][TILE][channel] = tile_imgs

                    elif sub_dir == MASK:
                        mask_imgs = [os.path.join(dir_path, path) for path in os.listdir(dir_path)]
                        data[drone_dir][image_dir][MASK] = mask_imgs

    return data                  


def load_split_data(target_channel=NVDI_CHANNEL, 
                    drone_to_load: list[DroneEnum] = [DroneEnum.RED_EDGE, DroneEnum.SEQUOIA],
                    test_image=['003', '005'],
                    open_image=False):

    data = load_data_path(drone_to_load=drone_to_load)
    
    train_tiles = {}
    train_gt = {}
    test_tiles = {}
    test_gt = {}
    
    for drone, images in data.items():
                
        print('Drone:', drone)
            
        train_tiles[drone] = {}
        train_gt[drone] = {}
        test_tiles[drone] = {}
        test_gt[drone] = {}  

        for image, image_data in images.items():
            tiles = image_data[TILE][target_channel]
            gts = image_data[GROUND_TRUTH]
            print('     Image:', image)
            
            if image in test_image:  
                test_tiles[drone][image] = []
                test_gt[drone][image] = [] 
                if open_image:
                    test_tiles[drone][image].extend([Image.open(tile) for tile in tiles])
                    test_gt[drone][image].extend([convert_to_black_and_white(Image.open(gt), threshold=128) for gt in gts])
                else:
                    test_tiles[drone][image].extend([tile for tile in tiles])
                    test_gt[drone][image].extend([gt for gt in gts])
                    
            else:
                train_tiles[drone][image] = []
                train_gt[drone][image] = []
                
                if open_image:
                    train_tiles[drone][image].extend([Image.open(tile) for tile in tiles])
                    train_gt[drone][image].extend([convert_to_black_and_white(Image.open(gt), threshold=128) for gt in gts])
                else:
                    train_tiles[drone][image].extend([tile for tile in tiles])
                    train_gt[drone][image].extend([gt for gt in gts])

    return train_tiles, train_gt, test_tiles, test_gt

