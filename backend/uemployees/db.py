from neomodel import config


def init_db():
    config.DATABASE_URL = 'bolt://neo4j:@neo4j:7687'
    config.AUTO_INSTALL_LABELS = True
