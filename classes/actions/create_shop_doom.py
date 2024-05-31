from classes.actions.connect import Connect
from classes.actions.partials.inventory.init_inventory import InitInventory
from classes.actions.partials.shop.feed_shop import FeedShop
from classes.actions.partials.shop.init_shop import InitShop
from classes.game_instance import GameInstance
import lib.utils as u
from classes.actions_bloc import ActionsBloc

class CreateShopDoom(ActionsBloc):
    
    def __init__(self, instance : GameInstance, shopName, price, parent=None, children=None):
        super().__init__(instance, parent, children)
        
        self.shopName = shopName
        self.price = price
        

        self.children = [
            Connect(self.instance),
            InitInventory(self.instance)
            ,InitShop(self.instance, shopName)
            ,FeedShop(self.instance, self.price)
            # ,Test(self.instance)
        ]
        
        
    
    def execute(self):
        print('Requis : ')
        print('1 - Avoir des "Paquets" sur le Raccourci "1"')
        self.instance.focus()
        print(f'Début de la création du shop: {self.shopName} with price: {self.price}')
        super().execute()

