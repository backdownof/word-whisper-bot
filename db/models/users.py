from db import models
from db.models import Model

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, func, types, PrimaryKeyConstraint


class User(Model):
    __tablename__ = 'users'
    __table_args__ = {'comment': '[Entity] Пользователи'}

    id = Column(types.BigInteger, nullable=False, primary_key=True, comment="[PK]")
    full_name = Column(types.Text, nullable=True, comment="Полное имя пользователя в Телеграм")
    tg_id = Column(types.BigInteger, nullable=False, comment="ID пользователя в Телеграм")
    tg_nickname = Column(types.Text, nullable=True, server_default="''::text", comment="Имя пользователя в Телеграм")
    word_of_day_subscribed = Column(types.Boolean, nullable=False, server_default="true", comment="Флаг, указывающий на то подписан ли пользователь на слово дня")
    ctime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время создания записи")
    utime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время обновления записи")

    def get_by_tg_id(tg_id):
        return models.DBSession.query(
            User,
        ).filter(
            User.tg_id == tg_id,
        ).first()


class Word(Model):
    __tablename__ = 'words'
    __table_args__ = {'comment': '[Entity] Слова для изучения'}

    id = Column(types.BigInteger, nullable=False, primary_key=True, comment="[PK]")
    word = Column(types.Text, nullable=False, comment="Слово для изучения")
    meaning = Column(types.Text, nullable=False, comment="Значение слова")
    level = Column(types.VARCHAR(10), nullable=True, comment="Уровень сложности слова")
    ctime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время создания записи")

    


class WordTranslation(Model):
    __tablename__ = 'word_translations'
    __table_args__ = {'comment': '[Entity] Переводы слов'}

    id = Column(types.BigInteger, nullable=False, primary_key=True, comment="[PK]")
    word_id = Column(types.BigInteger, ForeignKey('words.id'), nullable=False, comment="[FK]")
    language = Column(types.Text, nullable=False, comment="Язык перевода")
    translation = Column(types.Text, nullable=False, server_default="''::text", comment="Перевод слова")
    ctime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время создания записи")

    word = relationship('Word')


class UserWord(Model):
    __tablename__ = 'user_words'
    __table_args__ = {'comment': '[Entity] Слова пользователя'}

    user_id = Column(types.BigInteger, ForeignKey('users.id'), nullable=False, comment="[FK]")
    word_id = Column(types.BigInteger, ForeignKey('words.id'), nullable=False, comment="[FK]")
    learned = Column(types.Boolean, nullable=True, server_default="false", comment="Слово помечено как выученное")
    list_added = Column(types.Boolean, nullable=True, server_default="false", comment="Слово добавлено в список для изучения")
    ctime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время создания записи")
    utime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время обновления записи")

    PrimaryKeyConstraint(user_id, word_id)

    user = relationship('User')
    word = relationship('Word')


class WordExamples(Model):
    __tablename__ = 'word_examples'
    __table_args__ = {'comment': '[Entity] Примеры применения слова'}

    id = Column(types.BigInteger, nullable=False, primary_key=True, comment="[PK]")
    word_id = Column(types.BigInteger, ForeignKey('words.id'), nullable=False, comment="[FK]")
    example_sentece = Column(types.Text, nullable=False, comment="Пример использования слова в предложении")
    ctime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время создания записи")
    utime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время обновления записи")

    word = relationship('Word', backref='word_examples')


class WordExamplesTranslation(Model):
    __tablename__ = 'word_example_translations'
    __table_args__ = {'comment': '[Entity] Переводы примеров использования слов'}

    id = Column(types.BigInteger, nullable=False, primary_key=True, comment="[PK]")
    word_example_id = Column(types.BigInteger, ForeignKey('word_examples.id'), nullable=False, comment="[FK]")
    language = Column(types.Text, nullable=False, comment="Язык перевода")
    translation = Column(types.Text, nullable=False, server_default="''::text", comment="Перевод примера использования слова")
    ctime = Column(types.DateTime, nullable=False, server_default=func.timezone('UTC', func.now()), comment="Дата и время создания записи")

    word_example = relationship('WordExamples')
