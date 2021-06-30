import pickle
import numpy as np
import tensorflow as tf


FEATURE_ENCODING_PATH = '../datasets/autoria/feature_encoding.pkl'

# All images first resized to 'mid_size' without distortions
MID_SIZE = (250, 380)
# than resized to 'final_size' with distortions
FINAL_SIZE = (128, 128)


def process_image(path):
    """Return image in format ready to feed into model"""
    img = tf.keras.preprocessing.image.load_img(path, color_mode='grayscale')
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.keras.preprocessing.image.smart_resize(img, MID_SIZE)
    img = tf.image.resize(img, FINAL_SIZE)
    img = img.numpy() / 255
    img = np.expand_dims(img, 0)
    
    return img


def encode_features(**features):
    """
    Return encoded features.

    Example of 'data' kwargs:
    data = {
        'brand' : 'BMW',
        'fuel_type' : 'petrol',
        'transmission_type' : 'automatic',
        'mileage_kkm' : 145,
        'year_made' : 2010,
        'engine_size' : 4.4,
    }
    """

    with open(FEATURE_ENCODING_PATH, 'rb') as f:
        encoding = pickle.load(f)

    for f, val in features.items():
        val = val.lower() if isinstance(val, str) else val
        if f in encoding:
            features[f] = encoding[f].transform([val])
    return [list(features.values())]