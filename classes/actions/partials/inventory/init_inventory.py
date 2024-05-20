from classes.actions_bloc import ActionsBloc
from classes.game_instance import GameInstance
import lib.utils as u
import virtualKeyboardEvents as VK_event

class InitInventory(ActionsBloc):
    
    def __init__(self, instance : GameInstance, parent=None, children=None):
        super().__init__(instance, parent,children)
        
    
    def execute(self):
        print(f'Ouverture & Scan inventaire')
        
        VK_event.UseKey('i')
        self.instance.initInventory()
        
        super().execute()
