import os
import requests

def download_model(url, save_path):
    if not os.path.exists('models'):
        os.mkdir('models')
    
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as f:
        f.write(response.content)

# Download Artistic Pre-trained Model
download_model('https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth', './models/ColorizeArtistic_gen.pth')

# Download Stable Pre-trained Model
download_model('https://data.deepai.org/deoldify/ColorizeStable_gen.pth', './models/ColorizeStable_gen.pth')

print("Models downloaded successfully!")
