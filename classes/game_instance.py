from classes.inventory import Inventory
import lib.utils as u
import pyscreenshot as ImageGrab

class GameInstance:
    def __init__(self, position, state):
        self.position = position
        self.resolution = {'width': 800, 'height': 600}
        self.state = state
        self.coord = u.parseCoord(position)

    def focus(self):
        u.moveThenClick("left", self.position)
    
    def getRelativeDistanceFromClick(self):
        click_pos = u.getNextClickPos()
        return (click_pos[0] - self.position[0], click_pos[1] - self.position[1])
    
    def saveScreen(self, img_path="ancor/metin.png"):
        im = ImageGrab.grab(
            bbox=(
                self.position[0],
                self.position[1],
                self.position[0] + self.resolution['width'],
                self.position[1] + self.resolution['height']
            ),
            backend="mss",
            childprocess=False
        )
        im.save(img_path)

    def initInventory(self):
        self.inventory = Inventory( self, 9,5,self.coord['INVENTORY_FIRST_SLOT_ANCOR'], 'inventory_slots' )
        self.inventory.refreshAllSlots()

    def initShop(self):
        self.shop = Inventory( self, 8,5, self.coord['SHOP_FIRST_SLOT_ANCOR'], 'shop_slots' )