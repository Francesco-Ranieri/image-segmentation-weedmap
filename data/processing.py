import os
import re
import numpy as np
from data.constants import *
from common import get_distinct_files_name_in_dir, search_files_in_dir
from PIL import Image, ImageFilter


def split_image(image, num_splits, save_path):
    
    """
    Splits the given image into patches.
    """
    file_name = os.path.splitext(os.path.basename(save_path))[0]
    print(f'- Split image {file_name} into: {num_splits}')

    try:
        width, height = image.size
        patch_width = width // num_splits
        patch_height = height // num_splits
        patches = []

        for i in range(num_splits * num_splits):
            row_index = i // num_splits
            col_index = i % num_splits
            patch_index = i + 1
            print(f'    Split: {patch_index}')

            left = col_index * patch_width
            upper = row_index * patch_height
            right = left + patch_width
            lower = upper + patch_height

            patch = image.crop((left, upper, right, lower))
            patches.append(patch)

            if save_path:
                
                folder = os.path.dirname(save_path)
                folder = os.path.join(folder, 'patches')
                _save_path = os.path.join(folder, file_name)
                os.makedirs(folder, exist_ok=True)
                
                patch.save(f'{_save_path}_{patch_index}.png', format='png')
                
        return patches

    except Exception as e:
        print("Error:", e)
        return None


def sharp_image_pil(image, save_path:str, sharpen_strength=2):
    
    """
    Sharpens the given image.
    """
    file_name = os.path.basename(save_path)
    print(f'- Sharp image: {file_name} with strength: {sharpen_strength}')
    try:
        for _ in range(sharpen_strength):
            image = image.filter(ImageFilter.SHARPEN)

        if save_path:
            
            folder = os.path.dirname(save_path)
            folder = os.path.join(folder, 'sharp')
            save_path = os.path.join(folder, file_name)
            
            os.makedirs(folder, exist_ok=True)
            
            image.save(f'{save_path}.png', format='png')

        return image

    except Exception as e:
        print(f"Error while processing image: {e}")
        return None


def enlarge_image(image, save_path:str):
  
  """
    Enlarges the given image.
    """ 
    
  file_name = os.path.basename(save_path)
  print(f'- Enlarge image: {file_name}')
  try:
    # Set the new size for the enlarged image
    height_coeff = width_coeff = 3
    new_width = image.width * width_coeff
    new_height = image.height * height_coeff

    # Resize the image to the new size
    enlarged_image = image.resize((new_width, new_height), Image.LANCZOS)

    if save_path:
        
      folder = os.path.dirname(save_path)
      folder = os.path.join(folder, 'enlarged')
      save_path = os.path.join(folder, file_name)
      
      os.makedirs(folder, exist_ok=True)
      enlarged_image.save(f'{save_path}.png', format='png')
    return enlarged_image

  except Exception as e:
    print(f'Error while processing image: {e}')
    return None



def assemble_patch(patch_dir, num_splits:int = 2, save_path:str='frames_predictions', prediction_dir = 'predictions'):
    
    """
    Assembles the patches from the given directory.
    """
    
    assembled_patches = []

    patch_to_assemble = get_distinct_files_name_in_dir(prediction_dir)

    for patch in patch_to_assemble:
      patches = []
      for index in range(0, num_splits*2):
        file_name = search_files_in_dir(patch_dir, f'{patch}_{index}_2')[0]
        image = Image.open(file_name)
        print(file_name)
        patches.append(image)

      assembled_image = _assemble_patch(patches, num_splits)
      assembled_patches.append(assembled_image)

      if save_path:
        
        os.makedirs(save_path, exist_ok=True)
        
        _save_path = os.path.join(save_path, f"{patch}.png")
        assembled_image.save(_save_path)


    return assembled_patches


def _assemble_patch(patches, num_splits):
    
    """
    Assembles the given patches into a single image.
    Args:
        patches: The patches to assemble.
        num_splits: The number of splits.
    Returns:
        The assembled image.
    Raises:
        ValueError: If the patches are empty.
        ValueError: If the number of splits is less than or equal to 1.
    """
    
    if not patches:
        raise ValueError("Error: 'patches' must not be empty")

    if num_splits <= 1:
        raise ValueError("Error: 'num_splits' should be greater than 1")

    # Get the dimensions of the first patch
    patch_width, patch_height = patches[0].size
    width = patch_width * num_splits
    height = patch_height * num_splits

    # Create a new blank image to assemble patches
    assembled_image = Image.new('RGB', (width, height))

    for i in range(num_splits * num_splits):
        row_index = i // num_splits
        col_index = i % num_splits

        left = col_index * patch_width
        upper = row_index * patch_height
        right = left + patch_width
        lower = upper + patch_height

        patch = patches[i]
        assembled_image.paste(patch, (left, upper, right, lower))

    return assembled_image


def reassemble_orthomosaic(patch_dir,
                           save_path:str,
                           rows: int = 13):
    """
    Reassembles the orthomosaic from the given directory.
    """
    
    image_paths = os.listdir(patch_dir)
    image_paths.sort()

    images = [Image.open(os.path.join(patch_dir, image_path)) for image_path in image_paths]

    # Assicurati che il numero di immagini sia un multiplo del numero di immagini per riga
    if len(images) % rows != 0:
        raise Exception(f"Number of images not multiple of {rows}")

    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)

    combined_image = Image.new('RGB', (max_width * rows, int(len(images)/rows)*max_height))

    x_offset = 0
    y_offset = 0

    for img in images:
        combined_image.paste(img, (x_offset, y_offset))
        x_offset += img.width

        if x_offset >= combined_image.width:
            x_offset = 0
            y_offset += img.height

    if save_path:
        folder = os.path.dirname(save_path)
        os.makedirs(folder, exist_ok=True)
        combined_image.save(save_path)


def convert_to_black_and_white(image, threshold, file_name = None):
    
    """
    Converts an image to black and white.
    Args:
        image: The image to convert.
        file_name: The name of the file to save.
        save_results: Whether to save the results.
        threshold: The threshold to use to convert the image.
    Returns:
        The converted image.
    """
    
    try:
        bw_img = image.convert("L")

        # Apply a threshold to convert to pure black and white
        bw_threshold = bw_img.point(lambda p: 0 if p < threshold else 255, '1')

        if file_name:
            folder = os.path.dirname(file_name)
            os.makedirs(folder, exist_ok=True)
            bw_threshold.save(f"{file_name}.png", format='png')

        return bw_threshold

    except Exception as e:
        print("Error:", e)
        return None
    

def resize_image(new_size=DEFAULT_SIZE, file_path=None, image=None):
    
    """
    Resizes the given image.
    Args:
        file_path: The path of the image to resize.
        new_size: The new size of the image.
    Returns:
        The resized image.
    """
    
    # Open the image if not already opened
    assert file_path or image, "Either file_path or image must be specified"
    
    if not image:
        image = Image.open(file_path)

    # Resize the image
    resized_image = image.resize(new_size)

    # Return the resized image
    return resized_image