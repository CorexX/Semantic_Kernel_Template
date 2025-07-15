from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

# Create the SQLAlchemy Base
Base = declarative_base()

# Create the MetaData object
metadata = Base.metadata

# Import all ORM models to ensure they are registered with the Base
from models.orm import foundry_agent, handoff_rule

# Example engine creation (update the URL as needed)
# Replace 'sqlite:///example.db' with your actual database URL
engine = create_engine("sqlite:///vita.db", echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
