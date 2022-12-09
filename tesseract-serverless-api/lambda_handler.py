#import cv2
import json
import base64
from PIL import Image, ImageFilter
import pytesseract
    
def ocr(img,oem=None,psm=None, lang=None):

  config='--oem {} --psm {} -l {}'.format(oem,psm,lang)
  
  ocr_text = pytesseract.image_to_string(img, config=config).strip()
  
  return ocr_text
      
def lambda_handler(event, context):
    
    # Extract content from json body
    body_image64 = event['image64']
    oem = event["tess_params"]["oem"]
    psm = event["tess_params"]["psm"]
    lang = event["tess_params"]["lang"]
    use_pil = event["usepil"]
    
    # Decode & save image to /tmp
    with open("/tmp/saved_img.png", "wb") as f:
      f.write(base64.b64decode(body_image64))
    
    # # Read the image with cv2
    # image = cv2.imread("/tmp/saved_img.png")
    # # Convert to grayscale
    # gr_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if use_pil:
      # open image
      im = Image.open("/tmp/saved_img.png")
      # preprocessing
      gr_image = im.convert('L')# grayscale
      gr_image = gr_image.filter(ImageFilter.MedianFilter()) 
      
      # Ocr
      ocr_text = ocr(gr_image,oem=oem,psm=psm,lang=lang)
    else:
      # Ocr
      ocr_text = ocr("/tmp/saved_img.png",oem=oem,psm=psm,lang=lang)
    
    # # Write grayscale image to /tmp
    # cv2.imwrite("/tmp/gr_image.png", gr_image)
    # # Encode the grayscale image
    # with open("/tmp/gr_image.png", "rb") as imageFile:
    #   gr_image = base64.b64encode(imageFile.read())
    #   encoded_img = gr_image.decode("utf-8")
    
    # Return the result data in json format
    event["ocr_text"] = ocr_text
    del event["image64"]
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
