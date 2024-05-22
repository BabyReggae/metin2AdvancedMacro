class Shop:
    def __init__(self, instance, shopPos):
        self.instance = instance
        self.shopPos = shopPos
        self.nbLines = 8
        self.nbColumns = 5
        self.slots = {}

    def initSlots(self):
        # Check if the shop inventory is detected in the image
        shopInvPos = u.getImgPosInImg('ancor/metin.png', 'ancor/voidShop.png')
        if shopInvPos == [0, 0]:
            print('Shop not found in instance')
            return False

        # Initialize the grid with slot positions
        for x in range(self.nbColumns):
            self.slots[x] = {}
            for y in range(self.nbLines):
                self.slots[x][y] = {
                    'x': self.shopPos[0] + (32 * x) + 15,
                    'y': self.shopPos[1] + (32 * y) + 15
                }
        
        return True