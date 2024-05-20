import lib.utils as u
from classes.actions_bloc import ActionsBloc

class AmelioMarker(ActionsBloc):
    def __init__(self, instance,parent=None, children=None):
        super().__init__(instance,parent, children)


    def execute(self):  # Add self parameter here
        u.moveThenClick("right", self.instance.coord['SHORTCUT_1'] )
        u.moveThenClick("left", self.instance.coord['FINDER_MAIN_MENU'] )
        u.moveThenClick("left", self.instance.coord['FINDER_AMELIO_MENU'] )
        u.moveThenClick("left", self.instance.coord['FINDER_SEARCH'] )

        super().execute()