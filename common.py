import os
import re
import shutil
import numpy as np
from constants import *
from PIL import Image, ImageFilter


def extract_image_name(image_path:str):
  image_name = image_path.split("\\")[-1]
  return re.search(r'\d+', image_name).group(0)


def extract_patch_name(image_path:str):
  return re.search(r'\d+_\d+_\d+', image_path).group(0)


def search_files_in_dir(directory, sub_string):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if sub_string in file:
                matching_files.append(os.path.join(root, file))
    return matching_files


def is_image_total_black(image):
    img_array = np.array(image)
    return not np.any(img_array != 0)


def get_distinct_files_name_in_dir(directory):
  dist_file_names = set()
  file_names = os.listdir(directory)

  for file_name in file_names:
    dist_file_names.add(extract_image_name(file_name))
  return dist_file_names


def get_blacklist_files():
  return ['.ipynb_checkpoints']


def delete_experiment_files(experiment_path=None):

  # Check if the experiment path is empty
  if not experiment_path:
      raise ValueError("Error: 'experiment_path' must not be empty")

  # Prompt the user for confirmation
  # confirmation = input(f"Are you sure you want to delete the directory '{experiment_path}'? (yes/no): ")

  # Check the user's input
  # if confirmation.lower() == "yes" or confirmation.lower() == "":
  shutil.rmtree(experiment_path)
  print("Deletion cancelled.")
