from abc import ABC, abstractmethod

from classes.game_instance import GameInstance

class ActionsBloc(ABC):
    def __init__(self, instance : GameInstance, parent=None, children=None):
        self.instance = instance
        self.parent = parent
        self.children = children if children is not None else []
        self.state = "pending"

    def execute(self):
        for child in self.children:
            if child.state == "pending":
                child.execute()
        
        self.update_state('done')

        # Trigger execute function of parent
        if self.parent is not None:
            self.parent.execute()

        print('Fin de la pile action !')

    def update_state(self, state):
        self.state = state

