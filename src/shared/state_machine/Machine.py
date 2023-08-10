from typing import Union, List, Tuple
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FingerprintEntry(Base):
    """
    Represents a fingerprint entry in the database.
    """
    __tablename__ = 'fingerprint_entries'

    id = Column(Integer, primary_key=True)
    fingerprint = Column(String)
    company = Column(String)
    group = Column(String)

class FingerprintDatabase:
    """
    Provides methods for interacting with a fingerprint database.
    """
    def __init__(self, host: str, user: str, password: str, database: str):
        """
        Initializes a new instance of FingerprintDatabase.

        :param host (str): The database host.
        :param user (str): The database user.
        :param password (str): The database password.
        :param database (str): The name of the database.
        """
        self.db_url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        """
        A context manager that provides a session scope for database operations.
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def save_fingerprints(self, fingerprints: Union[str, List[str]], company: str, group: str) -> Union[int, List[int]]:
        """
        Saves fingerprints to the database.

        :param fingerprints (Union[str, List[str]]): A single fingerprint or a list of fingerprints.
        :param company (str): The company name.
        :param group (str): The group name.
        :return (Union[int, List[int]]): The ID of the inserted record or a list of IDs for multiple inserts.
        """
        with self.session_scope() as session:
            if isinstance(fingerprints, str):
                fingerprints = [fingerprints]
            
            inserted_ids = []
            for fingerprint in fingerprints:
                new_entry = FingerprintEntry(fingerprint=fingerprint, company=company, group=group)
                session.add(new_entry)
                session.flush()
                inserted_ids.append(new_entry.id)
            
            if len(inserted_ids) == 1:
                return inserted_ids[0]
            else:
                return inserted_ids

    def read_fingerprints(self, company: str, group: str) -> Tuple[List[str], List[int]]:
        """
        Reads fingerprints from the database.

        :param company (str): The company name.
        :param group (str): The group name.
        :return (Tuple[List[str], List[int]]): A tuple containing a list of fingerprints and a list of table IDs.
        """
        with self.session_scope() as session:
            filtered_entries = session.query(FingerprintEntry).filter_by(company=company, group=group).all()
            
            table_ids = [entry.id for entry in filtered_entries]
            fingerprints = [entry.fingerprint for entry in filtered_entries]
            
            return fingerprints, table_ids



# Example usage
if __name__ == "__main__":
    fingerprint_db = FingerprintDatabase(host="localhost", user="your_user", password="your_password", database="your_database")
    
    # Example data for Company A
    company_a_fingerprints = ["fingerprint1", "fingerprint2", "fingerprint3"]
    company_a_group = "Group A"
    
    inserted_id_a = fingerprint_db.save_fingerprints(company_a_fingerprints, "Company A", company_a_group)
    print("Inserted IDs for Company A:", inserted_id_a)
    
    # Example data for Company B
    company_b_fingerprints = ["fingerprint4", "fingerprint5"]
    company_b_group = "Group B"
    
    inserted_id_b = fingerprint_db.save_fingerprints(company_b_fingerprints, "Company B", company_b_group)
    print("Inserted IDs for Company B:", inserted_id_b)
    
    fingerprints_a, table_ids_a = fingerprint_db.read_fingerprints("Company A", company_a_group)
    print("Fingerprints for Company A:", fingerprints_a)
    print("Table IDs for Company A:", table_ids_a)
    
    fingerprints_b, table_ids_b = fingerprint_db.read_fingerprints("Company B", company_b_group)
    print("Fingerprints for Company B:", fingerprints_b)
    print("Table IDs for Company B:", table_ids_b)

