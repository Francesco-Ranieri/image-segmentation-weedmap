import os
import re
import numpy as np
from data.constants import *
from common import get_distinct_files_name_in_dir, search_files_in_dir
from PIL import Image, ImageFilter

def create_directory(directory_path:str):
  os.makedirs(directory_path, exist_ok=True)

def split_image(image, num_splits, file_name, save_result):
    
    """
    Splits the given image into patches.
    Args:
        image: The image to split.
        num_splits: The number of splits.
        file_name: The name of the file to save.
        save_results: Whether to save the results.
    Returns:
        The patches.
    Raises:
        ValueError: If the number of splits is less than or equal to 1.
    """
    
    print(file_name)
    print(f'- Split image into: {num_splits}')

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

            if save_result:
                directory_name = os.path.join('pre_process', 'patches')
                create_directory(directory_name)
                patch.save(os.path.join(directory_name, f'{file_name}_{patch_index}.png'), format='png')
        return patches

    except Exception as e:
        print("Error:", e)
        return None


def sharp_image_pil(image, file_name, save_result=True, sharpen_strength=2):
    
    """
    Sharpens the given image.
    Args:
        image: The image to sharpen.
        file_name: The name of the file to save.
        save_results: Whether to save the results.
        sharpen_strength: The number of times to apply the filter.
    Returns:
        The sharpened image.
    """
    
    print(f'- Sharp image: {file_name} with strength: {sharpen_strength}')
    try:
        for _ in range(sharpen_strength):
            image = image.filter(ImageFilter.SHARPEN)

        if save_result:
            directory_name = os.path.join('pre_process', 'sharp')
            create_directory(directory_name)
            image.save(f'{directory_name}/{file_name}.png', format='png')

        return image

    except Exception as e:
        print(f"Error while processing image: {e}")
        return None


def enlarge_image(image, file_name, save_result):
  
  """
    Enlarges the given image.
    Args:
        image: The image to enlarge.
        file_name: The name of the file to save.
        save_results: Whether to save the results.
    Returns:
        The enlarged image.
    """ 
    
  print(f'- Enlarge image: {file_name}')
  try:
    # Set the new size for the enlarged image
    height_coeff = width_coeff = 3
    new_width = image.width * width_coeff
    new_height = image.height * height_coeff

    # Resize the image to the new size
    enlarged_image = image.resize((new_width, new_height), Image.LANCZOS)

    if save_result:
      directory_name = os.path.join('pre_process', 'enlarged_images')
      create_directory(directory_name)
      enlarged_image.save(os.path.join(directory_name, f'{file_name}.png'), format='png')
    return enlarged_image

  except Exception as e:
    print(f'Error while processing image: {e}')
    return None



def assemble_patch(folder_path, num_splits:int = 2, save_results:bool = True):
    
    """
    Assembles the patches from the given directory.
    Args:
        folder_path: The directory containing the patches.
        num_splits: The number of splits.
        save_results: Whether to save the results.
    Returns:
        The assembled patches.
    Raises:
        ValueError: If the number of splits is less than or equal to 1.
    """
    assembled_patches = []

    patch_to_assemble = get_distinct_files_name_in_dir('predictions')

    for patch in patch_to_assemble:
      patches = []
      for index in range(0, num_splits*2):
        file_name = search_files_in_dir(folder_path, f'{patch}_{index}_2')[0]
        image = Image.open(file_name)
        print(file_name)
        patches.append(image)

      assembled_image = _assemble_patch(patches, num_splits)
      assembled_patches.append(assembled_image)

      if save_results:
        patch_name = re.search(r'\d{2,}', file_name).group(0)
        directory_name = 'frames_predictions'
        create_directory(directory_name)
        save_path = os.path.join(directory_name, f"{patch_name}.png")
        assembled_image.save(save_path)


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


def reassemble_orthomosaic(dir_path,
                           file_name:str ='orthomosaic.png',
                           rows: int = 13):
    """
    Reassembles the orthomosaic from the given directory.

    Args:
        dir_path (_type_): _description_
        rows (int, optional): _description_. Defaults to 13.

    Raises:
        Exception: _description_
    """
    
    image_paths = os.listdir(dir_path)
    image_paths.sort()

    images = [Image.open(os.path.join(dir_path, image_path)) for image_path in image_paths]

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

    combined_image.save(file_name)
    

def convert_to_black_and_white(image, save_results, threshold, file_name="black_and_white"):
    
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

        if save_results:
          directory_name = os.path.join('post_process', 'black_and_white')
          create_directory(directory_name)
          path = os.path.join(directory_name, f'{file_name}.png')
          bw_threshold.save(path, format='png')

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