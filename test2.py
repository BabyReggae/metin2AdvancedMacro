import cv2
import pytesseract
from pytesseract import Output
import pandas as pd
import lib.utils as u
from PIL import Image, ImageDraw, ImageFilter,ImageEnhance


import re

def parse_item_digit(item_str):
    # Define regular expression patterns
    pattern1 = r'(?P<nb>\d+)\s(?P<won>\d+)\s(?P<yang>\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?)$'
    pattern2 = r'(?P<nb>\d+)\s(?P<won>\d+)\s(?P<yang>\d+)$'
    pattern3 = r'(?P<nb>\d+)\s(?P<won>\d+)\s(?P<yang>(?:\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?|\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?\s)+)$'

    # Try matching each pattern
    match = re.match(pattern1, item_str)
    if match:
        nb = int(match.group('nb'))
        won = int(match.group('won')) # Convert to int directly
        yang = int(float(match.group('yang').replace(',', '').replace('.', ''))) # Convert to int
        return {'nb': nb, 'won': won, 'yang': yang}

    match = re.match(pattern2, item_str)
    if match:
        nb = int(match.group('nb'))
        won = int(match.group('won')) # Convert to int directly
        yang = int(match.group('yang')) # Convert to int directly
        return {'nb': nb, 'won': won, 'yang': yang}

    match = re.match(pattern3, item_str)
    if match:
        nb = int(match.group('nb'))
        won = int(match.group('won')) # Convert to int directly
        yang_str = match.group('yang')
        yang = sum(int(float(num.replace(',', '').replace('.', ''))) for num in yang_str.split())
        return {'nb': nb, 'won': won, 'yang': yang}

    print('Error on : ' + item_str)
    return None


def parse_item_alpha(item_str):
    # First pattern
    pattern1 = r'(?P<name>[+\w\s]+)\s(?P<seller>[^\s"]+)'
    
    # Second pattern

    # Match the first pattern
    match = re.match(pattern1, item_str)

    if match:
        # Extract matched groups
        name = match.group('name')
        seller = match.group('seller').strip()  # Remove leading and trailing space
        
        return {'name': name, 'seller': seller}

    else:
        print('Error on : ' + item_str )
        return None

def create_array_of_dicts(alpha, digit):
    # Split the string into lines and filter out empty lines
    lines_a = [line.strip() for line in alpha.split('\n') if line.strip()]
    lines_d = [line.strip() for line in digit.split('\n') if line.strip()]

    # Check if number of lines match
    if len(lines_a) != len(lines_d):
        print("Number of lines in alpha and digit don't match.")
        return []

    # Parse each line
    result = []
    for alpha_line, digit_line in zip(lines_a, lines_d):
        alpha_dict = parse_item_alpha(alpha_line)
        digit_dict = parse_item_digit(digit_line)
        
        if alpha_dict and digit_dict:
            merged_dict = {**alpha_dict, **digit_dict}
            result.append(merged_dict)
        else:
            print(f'Error on merge-lines: {alpha_line}, {digit_line}')
            result.append(None)

    return result


pytesseract.pytesseract.tesseract_cmd = r'D:\Web_game_solo\OCR\tesseract'


u.clearImgNoise( "cropped_image_2024-05-11_15-43-18.png", "cropped_image_3.png" )

img = cv2.imread("cropped_image_3.png")

img = cv2.resize(
    img, 
    (int(img.shape[1] + (img.shape[1] * .49)), int(img.shape[0] + (img.shape[0] * .9))),
    interpolation=cv2.INTER_AREA
)

img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
custom_config = r'-l fra --oem 3 --psm 6'
custom_config_digits = r'-l fra --oem 3 --psm 6 -c tessedit_char_whitelist=0123456789\  '

alphaDigitImg = img_rgb[:, :440, :]  # 280 pixels width for alphaDigits
digitsImg = img_rgb[:, 440:, :]  # 220 pixels width for digits

alphaDigits = pytesseract.image_to_string(alphaDigitImg, config=custom_config)
digits = pytesseract.image_to_string(digitsImg, config=custom_config_digits)
print( alphaDigits, digits )

res = create_array_of_dicts( alphaDigits.strip(), digits.strip() )

for item in res:
    print(item)

