import os
import sys
import numpy as np
import tensorflow as tf

sys.path.append(os.path.abspath(os.path.join('..', 'img_inpaint')))
import app

from tensorflow import keras
from .pconv import PConv2D
from tensorflow.keras.models import model_from_json
from PIL import Image



json_file = open('modelRunner/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json, custom_objects={'PConv2D':PConv2D})
loaded_model.load_weights("modelRunner/model.h5")


def clean_input_dir():
    # clean the input sub-dir in static
    filelist = [f for f in os.listdir("static/input/")]
    for f in filelist:
        os.remove(os.path.join("static/input/", f))
    return

def rgba_to_rgb(image1, image2, color=(255, 255, 255)):
    image1.load()
    image2.load()
    background1, background2 = (Image.new('RGB', image1.size, color), 
                                        Image.new('RGB', image2.size, color))
    background1.paste(image1, mask=image1.split()[3])
    background2.paste(image2, mask=image2.split()[3])
    return (background1.save('static/input/mi_new.jpg', 'JPEG', quality=80),
            background2.save('static/input/m_new.jpg', 'JPEG', quality=80))

def imginp(masked_image, mask):
    masked_img = Image.open(masked_image)
    mask = Image.open(mask)
    # convert rgba to rgb -- Need to add a check for those images which 
    # either don't have an alpha channel OR have partial data in alpha channel
    rgba_to_rgb(masked_img, mask)

    mi_new = Image.open('static/input/mi_new.jpg')
    m_new = Image.open('static/input/m_new.jpg')

    mi_new = mi_new.resize((32,32))
    m_new = m_new.resize((32,32))
    mi_r = np.array(mi_new)
    m_r = np.array(m_new)

    inp = [mi_r.reshape((1,) + mi_r.shape), m_r.reshape((1,) + m_r.shape)]
    val = loaded_model.predict(inp)
    pred_img = val.reshape(val.shape[1:])
    fimg = Image.fromarray(pred_img, 'RGB')

    clean_input_dir()
    return fimg.save("static/output/image.jpg", 'JPEG', quality=80)



if __name__ == "__main__":
    app.make_static_dir()
    imginp("modelRunner/masked_image.png", "modelRunner/mask.png")
