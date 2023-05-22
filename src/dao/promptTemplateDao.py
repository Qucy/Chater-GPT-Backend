# create table prompt_template (
#     id integer primary key autoincrement,
#     name text not null,
#     description text not null,
#     system_prompt text not null,
#     user_prompt text not null,
#     few_shots text not null,
#     created_at datetime not null,
#     updated_at datetime not null
# );

# create a base class PromptTemplate mapping to prompt_template table
# create a data access object PromptTemplateDao for prompt_template table in sqlite database
# use slqalchemy to access sqlite database

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PromptTemplate(Base):
    __tablename__ = 'prompt_template'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    system_prompt = Column(Text, nullable=False)
    user_prompt = Column(Text, nullable=False)
    few_shots = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class PromptTemplateDao:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        self.session = sessionmaker(bind=self.engine)()

    def get_all(self):
        return self.session.query(PromptTemplate).all()

    def get_by_id(self, id):
        return self.session.query(PromptTemplate).filter_by(id=id).first()

    def get_by_name(self, name):
        return self.session.query(PromptTemplate).filter_by(name=name).first()

    def insert(self, prompt_template):
        self.session.add(prompt_template)
        self.session.commit()

    def update(self, prompt_template):
        self.session.merge(prompt_template)
        self.session.commit()

    def delete(self, id):
        prompt_template = self.get_by_id(id)
        self.session.delete(prompt_template)
        self.session.commit()

    def close(self):
        self.session.close()