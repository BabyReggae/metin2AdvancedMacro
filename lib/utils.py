from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter,ImageEnhance, ImageChops
import time
from time import sleep
from pynput.mouse import Button, Controller, Listener
import glob

import difflib

import pytesseract

import numpy as np
import pyscreenshot as ImageGrab
import cv2
import json
from types import SimpleNamespace

import pyautogui
import json

def askUserQuestion(question: str, answer_type: type):
    while True:
        user_input = input(question + ' ')
        
        if answer_type == int:
            try:
                return int(user_input)
            except ValueError:
                print("Please enter a valid integer.")
        elif answer_type == str:
            return user_input
        else:
            raise ValueError("Unsupported answer type. Supported types are 'str' and 'int'.")


def clearImgNoise( src_path, dest_path, inverse_noiseRange = ((160,150,140),(255,255,255)) ):
    extractedImg = Image.open( src_path )
    extractedImg = extractedImg.convert("RGBA")
    pixdata = extractedImg.load()
    imgsize = extractedImg.size

    fontAverageRangeColor = inverse_noiseRange

    for pX in range( imgsize[0] ):
        for pY in range( imgsize[1] ):
            colorVal = extractedImg.getpixel( (pX ,pY) )
            if isPixelColorContainedInRange(  fontAverageRangeColor[0], fontAverageRangeColor[1], colorVal ) == False:
                pixdata[pX, pY] = (0, 0, 0, 255)

    extractedImg.save( dest_path )

def cropFromPosition(position, width, height, imgName, debug=False):
    # Get coordinates for the cropped area
    left = position[0]
    top = position[1]
    right = left + width
    bottom = top + height

    # Grab the screen area
    im = ImageGrab.grab(bbox=(left, top, right, bottom), backend="mss", childprocess=False)
    im.save(imgName)

    if debug:
        im.show()

    return im

def parseCoord(position):
    # Load coordinates from JSON
    with open('lib/conf/conf.json') as confile:
        conf = json.load(confile)
    
    # Initialize dictionary to store coordinates with position added
    coords = {}
    
    # Iterate through each coordinate in the JSON, add position to it, and store with key name
    for key, coord in conf["coordinates"].items():
        coords[key] = (coord[0] + position[0], coord[1] + position[1])
    
    return coords

def add_new_coordinate(d):
    new_key = input("Enter the new key for the tuple: ")

    # Load coordinates from JSON
    with open('lib/conf/conf.json') as confile:
        conf = json.load(confile)
    
    # Add the new coordinate to the dictionary
    conf["coordinates"][new_key] = d
    
    # Write the updated JSON back to the file
    with open('lib/conf/conf.json', 'w') as confile:
        json.dump(conf, confile, indent=4)

    print(f"New coordinate '{new_key}' added successfully.")

def listFile( path ):
        res = glob.glob(  path + "*")
        for i in range(len(res)):
                res[i] = res[i].replace("\\" , "/")
        return res

def on_click(x, y, button, pressed):
    global clickPos
        
    if not pressed:
        clickPos = (x,y)
        return False      
# Collect events until released

def screenInstance( instancePositions, configWidth = 800, configHeight = 600 ):
    im = ImageGrab.grab( 
        bbox=( instancePositions[0],  instancePositions[1],  instancePositions[0] + configWidth,  instancePositions[1] + configHeight), 
        backend="mss",
        childprocess=False)
    im.save("ancor/metin.png")
    sleep(0.1)

def getNextClickPos():
    with Listener(on_click=on_click) as listener:
        listener.join()
        return clickPos

def moveTo( coord ):
    mouse = Controller()
    mouse.position = (coord[0],coord[1])

def moveToCoord( coord ):
    mouse = Controller()
    mouse.position = (coord['x'],coord['y'])

def moveThenClick( mouseBtn, coord, delay = 0.5 ):
    mouse = Controller()
    mouse.position = (coord[0],coord[1])
    time.sleep(delay)
    mouse.click( Button[mouseBtn],1)
    time.sleep(0.1)

def moveThenClickCoord( mouseBtn, coord ):
    mouse = Controller()
    mouse.position = (coord["x"],coord["y"])
    time.sleep(0.05)
    mouse.click( Button[mouseBtn],1)
    time.sleep(0.1)

def isPixelColorContainedInRange( begRangeRGB , endRangeRGB, auditedRGB ):
    isContained = True
    for ind in range(3):
        if( auditedRGB[ind] < begRangeRGB[ind] or auditedRGB[ind] > endRangeRGB[ind] ):
            return False

    return isContained

def findFirstPixePosInImgOnColor(im, boxRangeX, boxRangeY,targetColor ):
    for pX in range( boxRangeX ):
        for pY in range( boxRangeY ):
            color = im.getpixel( (pX ,pY) )
            if color == targetColor :
                return [pX,pY]
##replace outter circle by (0,0,0)
def mask_circle_solid(pil_img, background_color, blur_radius, offset=0):
    background = Image.new(pil_img.mode, pil_img.size, background_color)

    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    return Image.composite(pil_img, background, mask)
# maybe try to create ^pixcel map to Optimize like image.load() ? 
def getListOfPixelPosByColor(im, boxRangeX, boxRangeY, targetColor, blurArea ):
    targetColorBegRange = [ x - blurArea for x in targetColor]
    targetColorEndRange = [ x + blurArea for x in targetColor]
    imData = []
    for pX in range( boxRangeX ):
        for pY in range( boxRangeY ):
            colorVal = im.getpixel( (pX ,pY) )
            if isPixelColorContainedInRange( targetColorBegRange, targetColorEndRange, colorVal ) == False:
                continue

            imData.append( (pX ,pY) )
            # if colorVal in imData:
            #     oldVal = imData[colorVal]
            #     imData[colorVal] = oldVal+1
            # else :
            #     imData[ colorVal ] = 1

    return imData

def get_img_dimensions(path):
    favicon_img = Image.open(path)
    width, height = favicon_img.size
    return width, height

################ IMG IN IMG // IMG TO TEXT // TEXT TO PRICE -- TODO LOAD GLOBAL VAR BY ENV VAR ( create .env )



# CONFIG
LTC_IMG_PATH = ['ancor/refs/items/leftTopItemBorder.png','ancor/refs/items/leftTopItemBorder2.png','ancor/refs/items/leftTopItemBorder3.png','ancor/refs/items/leftTopItemBorder4.png']
RTC_IMG_PATH =  ['ancor/refs/items/rightTopItemBorder.png','ancor/refs/items/rightTopItemBorder2.png','ancor/refs/items/rightTopItemBorder3.png','ancor/refs/items/rightTopItemBorder4.png']

GIDP_IMG_PATH = 'img/guessedItemDesription.png'
EIN_IMG_PATH = 'img/extractedItemName.png'

PRICING_JSON_PATH = 'json/items_pricing.json'
# -- tesseract config
pytesseract.pytesseract.tesseract_cmd = r'D:\Web_game_solo\OCR\tesseract'

# FUNCTIONS
def getItemList( jsonFilePath = PRICING_JSON_PATH ):
    input_file = open ( jsonFilePath )
    itemsData = json.load(input_file)

    itemList = []
    for index, item in enumerate(itemsData):
        itemList.append( item )

    return itemList , itemsData

def contrast( val , img ):
    #image brightness enhancer
    enhancer = ImageEnhance.Contrast(img)

    factor = val #gives original image
    im_output = enhancer.enhance(factor)
    return im_output

def getImgPosInImg( large_img_path , small_img_path , method = cv2.TM_SQDIFF_NORMED, debug = False ):
    # Read the images from the file
    large_image = cv2.imread(large_img_path)
    small_image = cv2.imread(small_img_path)
    result = cv2.matchTemplate(small_image, large_image, method)
    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc
    # print( MPx,MPy )
    if debug :
        # - - - DEBUG  Step 2: Get the size of the template. This is the same size as the match.
        trows,tcols = small_image.shape[:2]
        # Step 3: Draw the rectangle on large_image
        cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
        # Display the original image with the rectangle around the match.
        cv2.imshow('output',large_image)
        # The image is only displayed if we call this
        cv2.waitKey(0)

    return [MPx,MPy]

def extractItemNameAsImg( mousePos, screenArea , resultImgPath, debug = False, iter = 0 ):
    im = ImageGrab.grab( bbox=( mousePos['x']-screenArea, mousePos['y']-screenArea, mousePos['x']+screenArea, mousePos['y']+screenArea), backend="mss",childprocess=False )  # X1,Y1,X2,Y2
    im.save(GIDP_IMG_PATH)

    tlBorder = getImgPosInImg( GIDP_IMG_PATH, LTC_IMG_PATH[iter], debug = debug )
    trBorder = getImgPosInImg( GIDP_IMG_PATH, RTC_IMG_PATH[iter], debug = debug )
    # print( tlBorder,  trBorder )
    cropped = Image.open( GIDP_IMG_PATH )
    # Setting the points for cropped image'test shop

    
    left = tlBorder[0]+20
    right = trBorder[0]-20

    top = tlBorder[1] +15 
    bottom = tlBorder[1] + 25
    # Cropped image of above dimension
    # (It will not change original image)

    if debug :
        print('imgSize before ' , cropped.size )
        print('left : ' ,left ,'top : ' ,top ,'right : ' ,right ,'bottom : ' ,bottom)

    cropped = cropped.crop((left, top, right, bottom)) 

    if debug :
        print('imgSize after ' , cropped.size )
    # # Shows the image in image viewer
    # cropped.show()

    try:
        cropped.save(resultImgPath)
    except:
        print('could not saved cropped img')
        return None

    # im = im.crop((tlBorder[0], tlBorder[1]+ 5, trBorder[0], trBorder[1] +5  ))
    return cropped  

def getItemPriceByParsingMousePosImg( mousePos, nearRange = 220, fontAverageRangeColor = ((180,180,180),(255,255,255)), debug = False, iter = 0 ):

    moveToCoord( mousePos )
    sleep( 0.5 )

    nearRange = 220
    extractedImg = extractItemNameAsImg( mousePos, nearRange, EIN_IMG_PATH, debug = debug, iter = iter  )
    # try :
    #     extractedImg.save("img/tmpState.png")
    # except :
    #     print( 'imgSat' ,  extractedImg )
    
    if( extractedImg == None ):
        return None
        
    extractedImg = extractedImg.convert("RGBA")
    pixdata = extractedImg.load()
    imgsize = extractedImg.size

    for pX in range( imgsize[0] ):
        for pY in range( imgsize[1] ):
            colorVal = extractedImg.getpixel( (pX ,pY) )
            if isPixelColorContainedInRange(  fontAverageRangeColor[0], fontAverageRangeColor[1], colorVal ) == False:
                pixdata[pX, pY] = (0, 0, 0, 255)

    extractedImg.save( EIN_IMG_PATH )
    extractedText = pytesseract.image_to_string( EIN_IMG_PATH )
    parsedExtractedText = extractedText.strip()

    itemsList, itemData = getItemList()
    match = difflib.get_close_matches( parsedExtractedText , itemsList)

    if debug :
        print("extracted text => ",  parsedExtractedText  )
        print( "item => " , itemData )
        print( "match => ", match , len(match) )

    if len(match) == 0: 
        return None

    pricingData = itemData[match[0]] if itemData.get(match[0]) else None

    return pricingData

def get_screen_resolution():
    return pyautogui.size()

def compare_images(img1, img2):
        diff = ImageChops.difference(img1, img2)
        if diff.getbbox() is None:
            return True
        return False

def image_to_integer(image_path):
    #TODO test this aswell
    # https://stackoverflow.com/questions/75959720/how-to-extract-number-from-an-image

    # Open the image file
    img = Image.open(image_path)

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=0123456789')

    # Remove any non-digit characters
    text = ''.join(filter(str.isdigit, text))

    # Convert the text to an integer
    if text:
        return int(text)
    else:
        raise ValueError("No digits found in the image")

# # getImgPosInImg( 'img/guessedItemDesription.png', "ancor/refs/items/leftTopItemBorder.png", method=cv2.TM_SQDIFF_NORMED ,  debug=True )

# getImgPosInImg( 'img/guessedItemDesription.png', "ancor/refs/items/rightTopItemBorder4.png", method=cv2.TM_SQDIFF_NORMED ,  debug=True )
# extractedText = pytesseract.image_to_string( 'img/extractedItemName.png' )
# parsedExtractedText = extractedText.strip()

# print( parsedExtractedText , extractedText )

