# 'create_engine' actual connection pipe banata hai database tak.
from sqlalchemy import create_engine

# Ye imports classes aur database session banane ke liye tool hain.
# (Note: tumhare code me 'declarative_baseform' typo tha, sirf 'declarative_base' hota hai)
from sqlalchemy.orm import declarative_base, sessionmaker 

# Yahan hum apni upar banayi hui setting file se object import kar rahe hain
from src.utils.settings import settings


# STEP 1: ENGINE BANANA (The Train Engine)
# create_engine ko humne wo URL de diya jo settings ne .env se uthaya tha.
# Ye engine ab PostgreSQL se direct baatchit karne ke liye taiyar hai.
engine = create_engine(url=settings.DB_CONNECTION)

# STEP 2: SESSION BANANA (The Ticket Counter)
# SessionMaker ek factory hai jo "database sessions" banayegi. 
# Jaise database me query chalani ho, toh pehle session (ticket) lena padta hai.
# bind=engine ka matlab hai ki har session is particular engine (database) se juda hoga.
LocalSession = sessionmaker(bind=engine)

# STEP 3: BASE CLASS BANANA (The Blueprint)
# Ye ekdum tumhare Java ke '@Entity' jaisa hai. 
# Aage chalkar hum jitne bhi table banayenge (User, Task), wo sab is 'Base' class se judenge.
Base = declarative_base()


# STEP 4: DATABASE SESSION DENE WALA FUNCTION
# Ye function FastAPI me Dependency Injection ka kaam karta hai.
def get_db():
    db = LocalSession() # Ek naya connection (session) khola
    try:
        yield db # Request aane par connection FastAPI ko de diya
    finally:
        db.close() # Request khatam hote hi connection safely close kar diya (Bohot important!)