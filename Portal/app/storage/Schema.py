#TODO move consts into separate Consts package

def init_schema(app, storage):
    db = storage.db 
    mc = db.mapped_column
    MP = db.Mapped

    class Users(db.Model):
        id      : MP[int]       = mc(primary_key=True)
        name    : MP[str]       = mc( db.String(30) ) 
        password: MP[str]       = mc( )
        email   : MP[str]       = mc( db.String(60) ) 
        is_admin: MP[bool]      = mc(default=False) 

    class GraphCredentials(db.Model):
        id      : MP[int]       = mc(primary_key=True)
        user_id : MP[int]       = mc( db.ForeignKey('users.id') )
        name    : MP[str]       = mc( db.String(60) )
        airtable_api_key                 : MP[str] = mc( db.String(60) )
        airtable_base_id                 : MP[str] = mc( db.String(60) )
        airtable_states_table_id         : MP[str] = mc( db.String(60) )
        airtable_states_table_view_id    : MP[str] = mc( db.String(60) )
        airtable_transitions_table_id    : MP[str] = mc( db.String(60) )
        airtable_transition_table_view_id: MP[str] = mc( db.String(60) )
        airtable_forms_table_id          : MP[str] = mc( db.String(60) )
        airtable_forms_table_view_id     : MP[str] = mc( db.String(60) )
        airtable_config_table_id         : MP[str] = mc( db.String(60) )
        airtable_config_table_view_id    : MP[str] = mc( db.String(60) )

    with app.app_context():
        db.create_all()
        #storage.InsertDefaults()

    from collections    import namedtuple

    schema = namedtuple('schema', 'users graph_cred')
    return schema(users=Users,
                  graph_cred=GraphCredentials)

