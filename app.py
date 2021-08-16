from models import (Book, engine,
                    session, Base)

if __name__ == '__main__':
    Base.metadata.create_all(engine)