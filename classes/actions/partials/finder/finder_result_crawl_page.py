import lib.utils as u
from classes.actions_bloc import ActionsBloc
from PIL import Image
import datetime
import os
import json

class FinderResultCrawlPage(ActionsBloc):
    def __init__(self, instance, parent=None, children=None):
        super().__init__(instance, parent, children)
        self.letter_mapping = self.load_letter_mapping()

    def load_letter_mapping(self):
        with open('json/shopDictionary.json', 'r') as f:
            return json.load(f)

    def execute(self):
        pageWidth = 500
        pageHeight = 250
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        cropped_image_path = f"cropped_image_{timestamp}.png"
        resultPageIm = u.cropFromPosition(
            self.instance.coord['FINDER_RESULT_WINDOW_ANCOR'],
            pageWidth,
            pageHeight,
            cropped_image_path,
            False
        )

        rows_data = []

        collumsNames = ['nom', 'vendeur', 'nb', 'won', 'yang']
        row_height = pageHeight / 10

        for row in range(10):
            top = int(row * row_height)
            bottom = int((row + 1) * row_height)

            LineImg = resultPageIm.crop((0, top + 6, pageWidth, bottom - 7))
            cleanedLineImg = u.clearImgNoise(LineImg)

            sentence = self.extract_and_parse_letters(cleanedLineImg)
            rows_data.append(sentence)
            print(sentence)

        super().execute()

    def extract_and_parse_letters(self, img):
        img = img.convert('L')
        pixels = img.load()
        width, height = img.size

        letter_start = None
        letter_image = None
        letter_folder = 'img/letterLabel'
        os.makedirs(letter_folder, exist_ok=True)

        sentence = []
        word = []
        consecutive_black_columns = 0
        #the min number of black collumn separating shop collumn
        black_column_threshold = 8

        for x in range(width):
            column_has_white = any(pixels[x, y] > 0 for y in range(height))

            if column_has_white:
                consecutive_black_columns = 0
                if letter_start is None:
                    letter_start = x
                    letter_image = Image.new('L', (width, height))
                for y in range(height):
                    if pixels[x, y] > 0:
                        letter_image.putpixel((x - letter_start, y), 255)
            else:
                consecutive_black_columns += 1
                if letter_start is not None:
                    letter_name = self.get_letter_name(letter_image.crop((0, 0, x - letter_start, height)))
                    letter_path = os.path.join(letter_folder, f"{letter_name}.png")
                    if not os.path.exists(letter_path):
                        letter_image.crop((0, 0, x - letter_start, height)).save(letter_path)
                    letter_char = self.letter_mapping.get(letter_name, '?')
                    word.append(letter_char)
                    letter_start = None
                    letter_image = None

                if consecutive_black_columns >= black_column_threshold and len(word) > 0:
                    sentence.append(''.join(word))
                    word = []

        if letter_start is not None:
            letter_name = self.get_letter_name(letter_image.crop((0, 0, x - letter_start, height)))
            letter_path = os.path.join(letter_folder, f"{letter_name}.png")
            if not os.path.exists(letter_path):
                letter_image.crop((0, 0, x - letter_start, height)).save(letter_path)
            letter_char = self.letter_mapping.get(letter_name, '?')
            word.append(letter_char)

        if word:
            sentence.append(''.join(word))

        return ' // '.join(sentence)

    def get_letter_name(self, letter_img):
        width, height = letter_img.size
        pixels = letter_img.load()
        name_parts = []

        for x in range(width):
            white_pixel_count = sum(1 for y in range(height) if pixels[x, y] > 0)
            first_white_pixel_index = next((y for y in range(height) if pixels[x, y] > 0), -1)
            name_parts.append(f"{first_white_pixel_index}{white_pixel_count}")

        return ''.join(name_parts)
