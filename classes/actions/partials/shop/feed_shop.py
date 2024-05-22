from classes.actions_bloc import ActionsBloc
import lib.utils as u
import virtualKeyboardEvents as VK_event

class FeedShop(ActionsBloc):
    
    def __init__(self, instance, price, parent=None, children=None):
        super().__init__(instance, parent, children)
        self.price = price
    
    def execute(self):
        print(f'Remplissage du shop : {self.price} yangs / item ')
        
        for slot in self.instance.inventory.slots:
            if slot.state == "item":
                u.moveThenClick("left", ( slot.position[0] + 16, slot.position[1] + 16 ))
                
                for shop_slot in self.instance.shop.slots:
                    if shop_slot.state == "void" or shop_slot.state == "unknown":
                        u.moveThenClick("left", ( shop_slot.position[0] + 16, shop_slot.position[1] + 16 ) )
                        
                        VK_event.Write(str(self.price))
                        VK_event.UseKey('Enter')
                        
                        shop_slot.state = "item"
                        break

        u.moveThenClick("left", self.instance.coord['CONFIRM_SHOP_ANCOR'])

        super().execute()

