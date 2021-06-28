import numpy as np
import tensorflow as tf


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