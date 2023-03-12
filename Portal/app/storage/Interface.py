from flask_sqlalchemy   import SQLAlchemy
from .Schema            import init_schema
from .Models            import User, GraphCredentials


class Storage():
    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
        self.db = SQLAlchemy()
        self.db.init_app(app)

        self.schema = init_schema(app, self)

    def GetUser(self, key, value) -> User:
        users_t = self.schema.users
        db = self.db
        usr = self.db.session.scalars(
                  db.select(users_t)\
                  .where(getattr(users_t, key, 'id') == value)\
                  ).first()
        if not usr:
            return None
        return User(
            id=usr.id,
            name=usr.name,
            email=usr.email,
            password=usr.password,
            is_admin=usr.is_admin,
        )

    def CreateUser(self, user) -> None:
        user_schema = self.schema.users(
            **self.__CleanModel(user)
        )
        self.db.session.add(user_schema)
        self.db.session.commit()
        user.id = user_schema.id
        return user

    def CreateGraph(self, graph) -> None:
        graph_schema = self.schema.graph_cred(
            **self.__CleanModel(graph)
        )
        self.db.session.add(graph_schema)
        self.db.session.commit()
        graph.id = graph_schema.id
        return graph

    def InsertDefaults(self):
        admin = User(
            name='porko',
            email='porkonoir@tutamail.com',
            password='',
        )

    def __CleanModel(self, model) -> dict:
        v = vars(model)
        v.pop('id')
        return v

