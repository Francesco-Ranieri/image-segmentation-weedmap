import os

# RAW DATA 
DATA_DIR = os.path.dirname(__file__)
DATASET_PATH = os.path.join(DATA_DIR, '2018-weedMap-dataset-release')
TILES_PATH  = os.path.join(DATASET_PATH, 'Tiles')
SEQUOIA = "Sequoia"
RED_EDGE = "RedEdge"
GROUND_TRUTH = "groundtruth"
GROUND_TRUTH_EXTENSION = "_GroundTruth_color.png"
TILE = "tile"
MASK  = "mask"
DEFAULT_SIZE = (480, 360)

# CHANNELS
B_CHANNEL = "B"
CIR_CHANNEL = "CIR"
G_CHANNEL = "G"
NVDI_CHANNEL = "NDVI"
NVDI_CRAFTED_CHANNEL = "NDVI_crafted"
NIR_CHANNEL = "NIR"
RED_CHANNEL = "R"
RE_CHANNEL = "RE"
RGB_CHANNEL = "RGB" # only for redege sensor !

# PROCESSED DATA
KMEANS = "kmeans"
