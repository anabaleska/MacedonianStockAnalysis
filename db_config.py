from sqlalchemy import create_engine


def get_database_connection():
    DATABASE_URL = "postgresql+psycopg2://postgres:anaiman@localhost:5432/msa_data"
    engine = create_engine(DATABASE_URL)
    return engine