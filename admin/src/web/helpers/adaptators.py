import base64
import io
from PIL import Image
import qrcode
from werkzeug.utils import secure_filename
import os
import base64
import hashlib

# Resize profile image
def image_resize(file, size=250):
    img = Image.open(file)
    img_size = img.size
    img_ratio = size/img_size[0]
    img.thumbnail((img_size[0]*img_ratio, img_size[1]*img_ratio), Image.ANTIALIAS)
    img_ratio = img.width / img.height
    img = img.resize((int(size*img_ratio), int(size*img_ratio)))
    return image_to_bytes(img)

def image_to_bytes(image):
    stream = io.BytesIO()
    image.save(stream, format='PNG')
    return stream.getvalue()

# QR
def generate_qr(url):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=3,
                       border=2)

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    return base64.b64encode(image_to_bytes(img)) #img


def upload_file(file, id_cuota, id_socio):
    '''Persistencia de archivo en el FS, retorna el PATH donde se guardó el
    archivo, únicamente si este no estaba vacío. En caso contrario, retorna None'''
    
    if file:
      ext = file.filename.split('.')[1]
      filename = hashlib.sha256(f"{id_cuota}-{id_socio}".encode()).hexdigest()
      filename = secure_filename(filename)
      PATH = os.path.join("public", "images", "comprobantes", f"{filename}.{ext}")
      TOTAL_PATH = os.path.join(os.getcwd(), PATH)

      file.save(TOTAL_PATH)
       
      return PATH 

    return None