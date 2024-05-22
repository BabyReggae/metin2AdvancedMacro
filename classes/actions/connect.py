import lib.utils as u
from classes.actions_bloc import ActionsBloc

class Connect(ActionsBloc):

    def __init__(self, instance,parent=None, children=None):
        super().__init__(instance,parent, children)

    def execute(self):
        print('Connexion au compte (30secondes)')
        self.instance.focus()
        u.moveThenClick("left", self.instance.coord['SERV_EUW'] )
        u.moveThenClick("left", self.instance.coord['SELECT_CH1'], 2 )
        u.moveThenClick("left", self.instance.coord['SERVER_OK'], 2 )
        u.moveThenClick("left", self.instance.coord['START'], 10 )
        u.moveThenClick("left", self.instance.coord['FENETREDEMERDEAULOAD'], 20 )
        super().execute()