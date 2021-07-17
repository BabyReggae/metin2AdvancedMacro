from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter
import time
from pynput.mouse import Button, Controller, Listener
import glob

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
def getNextClickPos():
    with Listener(on_click=on_click) as listener:
        listener.join()
        return clickPos

def moveTo( coord ):
    mouse = Controller()
    mouse.position = (coord[0],coord[1])

def moveThenClick( mouseBtn, coord ):
    mouse = Controller()
    mouse.position = (coord[0],coord[1])
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


