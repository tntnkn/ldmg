class MaxDmgLoader():
    from .src import Loader

    def __init():
        pass

    def Load(self,
             AIRTABLE_API_KEY, 
             AIRTABLE_BASE_ID,
             AIRTABLE_STATES_TABLE_ID,
             AIRTABLE_STATES_TABLE_MAIN_VIEW_ID,
             AIRTABLE_TRANSITIONS_TABLE_ID,
             AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID,
             AIRTABLE_FORMS_TABLE_ID,
             AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID,
             AIRTABLE_CONFIG_TABLE_ID,
             AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID
        ):
        loader = MaxDmgLoader.Loader()
        loader.load(
            AIRTABLE_API_KEY, 
            AIRTABLE_BASE_ID,
            AIRTABLE_STATES_TABLE_ID,
            AIRTABLE_STATES_TABLE_MAIN_VIEW_ID,
            AIRTABLE_TRANSITIONS_TABLE_ID,
            AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID,
            AIRTABLE_FORMS_TABLE_ID,
            AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID,
            AIRTABLE_CONFIG_TABLE_ID,
            AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID
        ) 

        return {
            'graph'         : loader.graph,
            'forms'         : loader.forms,
            'docs'          : loader.docs
        }

    def LoadFromConfig(self, config):
        return self.Load(**(vars(config)))

