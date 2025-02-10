import os
import torch
from deoldify.visualize import *

# Check if GPU is available
if torch.cuda.is_available():
    device = torch.device('cuda')
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use GPU if available
    print("Using GPU for DeOldify.")
else:
    device = torch.device('cpu')
    print("CUDA not available. Using CPU for DeOldify, which may be slower.")

# Initialize the colorizer
colorizer = get_image_colorizer(artistic=True)  # No gen_file_path

def colorize_image(filepath, result_folder):
    result_filename = "colorized_" + os.path.basename(filepath)
    result_filepath = os.path.join(result_folder, result_filename)

    # Perform colorization
    colorizer.plot_transformed_image(filepath, render_factor=35, results_dir=result_folder)

    return result_filename
