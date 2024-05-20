from classes.actions_bloc import ActionsBloc
from classes.game_instance import GameInstance
import lib.utils as u
import virtualKeyboardEvents as VK_event

class InitShop(ActionsBloc):
    
    def __init__(self, instance : GameInstance, shopName : str, parent=None):
        super().__init__(instance, parent, children=None)
        
        self.shopName = shopName
    
    def execute(self):
        print(f'Ouverture du shop : "{self.shopName}"')
        
        u.moveThenClick("right", self.instance.coord['SHORTCUT_1'], 1 )
        VK_event.Write( self.shopName )
        VK_event.UseKey('Enter')
        
        self.instance.initShop()
        
        super().execute()
