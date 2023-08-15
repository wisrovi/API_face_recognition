from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FingerprintEntry(Base):
    """
    FingerprintEntry model
    """

    __tablename__ = "fingerprint_entries"

    id = Column(Integer, primary_key=True)
    fingerprint = Column(String(length=4096), nullable=False)
    company = Column(String(length=255), nullable=False)
    group = Column(String(length=255), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "company",
            "group",
            "fingerprint",
            name="_company_group_fingerprint_uc",
        ),
    )
