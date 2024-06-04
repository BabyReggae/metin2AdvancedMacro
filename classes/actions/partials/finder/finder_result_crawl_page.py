from classes.actions_bloc import ActionsBloc
import classes.services.market_service as market_service

class ActionNameMarketPageItems(ActionsBloc):
    def __init__(self, instance, alphabet_path, parent=None, children=None, pageWith = 500,pageHeight = 250 ):
        super().__init__(instance, parent, children)
        #TODO deleguate this function to global service ( refacto utils )
        self.letter_mapping = market_service.load_json( alphabet_path )
        self.pageWith = pageWith
        self.pageHeight = pageHeight

    def execute(self):
        
        page_items = market_service.getPageItemsAsArray( self.instance.coord['FINDER_RESULT_WINDOW_ANCOR'], self.pageWith, self.pageHeight, self.letter_mapping )
            
        #TODO perform action on each page items - 
        
        super().execute()
