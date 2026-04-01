from PIL import Image
import numpy as np

def score_image(path):
    img = Image.open(path)
    arr = np.array(img)
    return arr.mean() + arr.std()
