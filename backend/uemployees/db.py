import time
import os

from neomodel import (
    config,
    db,
    clear_neo4j_database
)


def init_db():
    config.DATABASE_URL = 'bolt://neo4j:@neo4j:7687'

    # waiting until neo4j initialized
    time.sleep(40)

    # clear db
    clear_neo4j_database(db)
    for constraint in db.cypher_query("CALL db.constraints")[0]:
        db.cypher_query(f'DROP CONSTRAINT {constraint[0]};')

    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_file = os.path.join(base_dir, 'db_data.txt')

    with open(db_file, 'r') as db_data:
        raw_queries = db_data.readlines()
        clear_queries = [query.replace('\n', '') for query in raw_queries]
        queries = list(filter(len, clear_queries))
        current_query = ''
        for query in queries:
            if query[-1] != ';':
                current_query += f' {query}'
            else:
                current_query = query if not current_query else f'{current_query} {query}'
                db.cypher_query(current_query)
                current_query = ''
