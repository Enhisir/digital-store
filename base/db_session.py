import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Database filename is required.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Setting database connection to  {conn_str}...")
    try:
        engine = sa.create_engine(conn_str, echo=False)
        __factory = orm.sessionmaker(bind=engine)

        from base import __all_models

        SqlAlchemyBase.metadata.create_all(engine)
    except Exception as e:
        print("Database connection failed:")
        print(e)


def create_session() -> Session:
    global __factory
    return __factory()
