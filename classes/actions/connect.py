import lib.utils as u
from classes.actions_bloc import ActionsBloc

class Connect(ActionsBloc):

    def __init__(self, instance,parent=None, children=None):
        super().__init__(instance,parent, children)

    def execute(self):
        print('Connexion au compte')
        self.instance.focus()
        u.moveThenClick("left", self.instance.coord['SERV_EUW'] )
        u.moveThenClick("left", self.instance.coord['SELECT_CH1'], 1 )
        u.moveThenClick("left", self.instance.coord['SERVER_OK'], 1 )
        u.moveThenClick("left", self.instance.coord['START'], 6 )
        u.moveThenClick("left", self.instance.coord['FENETREDEMERDEAULOAD'], 15 )
        super().execute()