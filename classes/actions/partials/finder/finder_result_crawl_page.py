import lib.utils as u
from classes.actions_bloc import ActionsBloc
from PIL import Image
import pytesseract
import datetime

class FinderResultCrawlPage(ActionsBloc):
    def __init__(self, instance,parent=None, children=None):
        super().__init__(instance,parent, children)
        # -- tesseract config
        pytesseract.pytesseract.tesseract_cmd = r'D:\Web_game_solo\OCR\tesseract'

    def execute(self):
        pageWidth = 500
        pageHeight = 250
        resultPageIm = u.cropFromPosition( 
            self.instance.coord['FINDER_RESULT_WINDOW_ANCOR'],
            pageWidth,
            pageHeight,
            f"cropped_image_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png",
            False
        )

        rows_data = []

        # Define column percentages and row height  # Column names
        collumsNames = ['nom', 'vendeur', 'nb', 'won', 'yang']
        col_percentages = [0.35, 0.25, 0.05, 0.20, 0.15]
        row_height = pageHeight / 10  # Assuming 10 rows per page

        # Calculate column widths in pixels
        col_widths = [int(pageWidth * p) for p in col_percentages]

        # Iterate over each row
        for row in range(10):
            # Calculate top and bottom coordinates for the row
            row_data = {}
            top = int(row * row_height)
            bottom = int((row + 1) * row_height)

            # Iterate over each column
            for col, width in enumerate(col_widths):
                # Calculate left and right coordinates for the column
                left = sum(col_widths[:col])  # Left coordinate
                right = left + width  # Right coordinate

                # Crop the column from the resultPageIm
                column_img = resultPageIm.crop((left+6, top+5, right-6, bottom-5))
                img_name = f"img/finder/{collumsNames[col]}_{row}.png"

                # Save the column image
                column_img.save(img_name)

                # Perform text extraction
                extracted_text = pytesseract.image_to_string(column_img, lang='eng')

                # Store extracted text in row_data
                row_data[collumsNames[col]] = extracted_text.strip()

            rows_data.append(row_data)

        # Perform clicks for pagination
        # u.moveThenClick("left", self.instance.coord['FINDER_RESULT_PAGE_SECOND'])
        # u.moveThenClick("left", self.instance.coord['FINDER_RESULT_PAGE_THIRD'])
        # u.moveThenClick("left", self.instance.coord['FINDER_RESULT_PAGE_FOURTH'])
        # u.moveThenClick("left", self.instance.coord['FINDER_RESULT_PAGE_FIFTH'])
        # u.moveThenClick("left", self.instance.coord['FINDER_RESULT_NEXT_PAGES'])
        print(rows_data)

        super().execute()

# # Example usage
# # Assuming you have instantiated the instance of FinderResultCrawlPage
# finder_result_crawl_page = FinderResultCrawlPage(instance, parent, children)
# finder_result_crawl_page.execute()
