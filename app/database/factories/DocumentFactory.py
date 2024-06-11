import factory
from factory.alchemy import SQLAlchemyModelFactory
from app import db
from app.models import Document

class DocumentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Document
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('file_name')
    path = factory.Faker('file_path')
