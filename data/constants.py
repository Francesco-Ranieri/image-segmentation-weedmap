import os

# RAW DATA 
# ------------------------
DATA_DIR = os.path.dirname(__file__)
DATASET_PATH = os.path.join(DATA_DIR, '2018-weedMap-dataset-release')
TILES_PATH  = os.path.join(DATASET_PATH, 'Tiles')
SEQUOIA = "Sequoia"
SEQUIOA_CHANNEL = "NDVI"
RED_EDGE = "RedEdge"
RED_EDGE_CHANNEL = "RGB"
GROUND_TRUTH = "groundtruth"
GROUND_TRUTH_EXTENSION = "_GroundTruth_color.png"
TILE = "tile"
MASK  = "mask"
DEFAULT_SIZE = (480, 360)
# ------------------------


# PROCESSED DATA
# ------------------------
KMEANS = "kmeans"
# ...
# ------------------------