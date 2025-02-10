import torch
from deoldify.visualize import *

# Set device to CPU
device = torch.device('cpu')

# Load the colorizer model
colorizer = get_image_colorizer(artistic=True)

# Modify the load function to force CPU usage
colorizer.learn.model.load_state_dict(
    torch.load('path/to/ColorizeArtistic_gen.pth', map_location=device)
)

# Colorize an image
colorizer.plot_transformed_image('C:/Users/lenovo/Desktop/web/photo hi.jpg', render_factor=45, figsize=(20,20))
