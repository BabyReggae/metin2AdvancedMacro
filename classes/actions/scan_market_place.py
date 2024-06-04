import lib.utils as u
from classes.actions.connect import Connect
from classes.actions_bloc import ActionsBloc
from classes.actions.partials.finder.finder_result_crawl_page import FinderResultCrawlPage
from classes.actions.partials.finder.amelio_market import AmelioMarker

class ScanMarketPlace(# `ActionsBloc` is a class that serves as a base class for defining a block of actions
# or a sequence of actions to be executed. In the provided code snippet, `ScanMarketPlace`
# class inherits from `ActionsBloc` and defines a list of child actions to be executed
# sequentially. The `execute` method in `ScanMarketPlace` class is responsible for executing
# these child actions in a specific order.
ActionsBloc):
    def __init__(self, instance,parent=None, children=None):
        super().__init__(instance,parent, children)

        self.children = [
            # Connect( self.instance ),
            # AmelioMarker( self.instance ),
            ActionNameMarketPageItems( self.instance, 'json/shopDictionary.json' )
        ]


    def execute(self):  # Add self parameter here
        self.instance.focus()
        print('start scanShop - main action')
        super().execute()