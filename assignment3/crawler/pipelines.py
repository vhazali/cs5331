import logging, datetime
from database.models import *
from scrapy import signals
from items import *
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)

class URLPipeline(object):
    def __init__(self, settings):
        self.database = settings.get('DATABASE')
        self.sessions={}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def create_engine(self):
        engine = create_engine(URL(**self.database), poolclass=NullPool)
        return engine

    def create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    def create_session(self, engine):
        session = sessionmaker(bind=engine)()
        return session

    def spider_opened(self, spider):
        engine = self.create_engine()
        self.create_tables(engine)
        session = self.create_session(engine)
        self.sessions[spider] = session

    def spider_closed(self, spider):
        session = self.sessions.pop(spider)
        session.close()

    def process_item(self, item, spider):

        # Only process if it's a URLItem
        if not isinstance(item, URLItem):
            return item

        session = self.sessions[spider]
        url = Links(**item)
        logger.info("processing url {}".format(url))

        # Check if already in database
        exists = session.query(Links).filter_by(url=item['url']).first() is not None
        if exists:
            logger.info('Url {} is already in db'.format(url))
            return

        try:
            session.add(url)
            session.commit()
            logger.info('Url {} stored in db'.format(url))
        except:
            logger.warning('Failed to add url {} to db'.format(url))
            session.rollback()
            raise

        return item

class FormPipeline(object):
    def __init__(self, settings):
        self.database = settings.get('DATABASE')
        self.sessions={}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def create_engine(self):
        engine = create_engine(URL(**self.database), poolclass=NullPool)
        return engine

    def create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    def create_session(self, engine):
        session = sessionmaker(bind=engine)()
        return session

    def spider_opened(self, spider):
        engine = self.create_engine()
        self.create_tables(engine)
        session = self.create_session(engine)
        self.sessions[spider] = session

    def spider_closed(self, spider):
        session = self.sessions.pop(spider)
        session.close()

    def process_item(self, item, spider):

        # Only process if it's a FormItem
        if not isinstance(item, FormItem):
            return item

        session = self.sessions[spider]
        form = Forms(**item)
        logger.info("processing form {}".format(form))

        # Check if already in database
        exists = session.query(Forms).filter_by(url=item['url'], id_attr=item['id_attr']).first() is not None
        if exists:
            logger.info('Form {} is already in db'.format(form))
            return

        try:
            session.add(form)
            session.commit()
            logger.info('Form {} stored in db'.format(form))
        except:
            logger.warning('Failed to add form {} to db'.format(form))
            session.rollback()
            raise

        return item

class InputPipeline(object):
    def __init__(self, settings):
        self.database = settings.get('DATABASE')
        self.sessions={}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def create_engine(self):
        engine = create_engine(URL(**self.database), poolclass=NullPool)
        return engine

    def create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    def create_session(self, engine):
        session = sessionmaker(bind=engine)()
        return session

    def spider_opened(self, spider):
        engine = self.create_engine()
        self.create_tables(engine)
        session = self.create_session(engine)
        self.sessions[spider] = session

    def spider_closed(self, spider):
        session = self.sessions.pop(spider)
        session.close()

    def process_item(self, item, spider):

        # Only process if it's a InputItem
        if not isinstance(item, InputItem):
            return item

        session = self.sessions[spider]
        form_input = Inputs(**item)
        logger.info("processing form input {}".format(form_input))

        # Check if already in database
        exists = session.query(Inputs).filter_by(complete=item['complete']).first() is not None
        if exists:
            logger.info('Input {} is already in db'.format(form_input))
            return

        try:
            session.add(form_input)
            session.commit()
            logger.info('Input {} stored in db'.format(form_input))
        except:
            logger.warning('Failed to add input {} to db'.format(form_input))
            session.rollback()
            raise

        return item