import pyscreenshot as ImageGrab
from PIL import Image
import lib.utils as u

class InventorySlot:
    def __init__(self, position, name, dirName, state="unknown", img=None ):
        self.position = position
        self.dirName = dirName
        
        self.state = state
        self.img = img
        self.name = name

    def refresh(self):
        x, y = self.position
        box = (x+5, y+5, x + 27, y + 27)
        img = ImageGrab.grab(bbox=box)
        
        # img.save(f"img/{self.dirName}/{self.name}.png")
        
        void_img_path = "img/config/void_inventory_slot.png"
        void_img = Image.open(void_img_path)
        
        if u.compare_images( img, void_img):
            self.state = "void"
        else:
            self.state = "item"
