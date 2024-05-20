from typing import List
from pynput.mouse import Controller
from classes.inventory_slot import InventorySlot
import time

class Inventory:
    def __init__(self, instance,nbLines,nbColumns,firstSlotKey,dirName,page=1):
        self.instance = instance
        self.page = page
        self.nbLines = nbLines
        self.nbColumns = nbColumns
        self.firstSlotKey = firstSlotKey
        self.slots: List[InventorySlot] = [] 
        self.dirName = dirName
        
        self.initSlots()

    def open(self):
        print('ignore this function')

    def initSlots(self):

        inventory_first_slot = self.firstSlotKey  
        
        slot_distance = 32
        
        for line in range(self.nbLines):
            for column in range(self.nbColumns):
                x = inventory_first_slot[0] + column * slot_distance
                y = inventory_first_slot[1] + line * slot_distance
                position = (x, y)
                
                slot = InventorySlot(position, f"{line+1}_{column+1}", self.dirName )
                self.slots.append(slot)
            
    def move_mouse_over_slots(self):
        mouse = Controller()
        for slot in self.slots:
            x,y = slot.position
            mouse.position = (x+16,y+16)
            time.sleep(0.5)
            
    def refreshAllSlots(self):
        for slot in self.slots:
            slot.refresh()
            
        print( self.getNbSlotByState('item'),' items trouvé' )
            
    def getNbSlotByState(self, state):
        nb = 0
        for slot in self.slots:
            if slot.state == state:
                nb+=1
            
        return nb