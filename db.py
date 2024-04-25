from sqlmodel import create_engine, SQLModel, Session

DATABASE_SQL = 'postgresql://postgres:postgres@localhost:5432/postgres'

engine = create_engine(DATABASE_SQL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session