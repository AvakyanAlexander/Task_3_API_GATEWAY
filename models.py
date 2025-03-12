from sqlalchemy import (Column,
                        Integer,
                        String,
                        DateTime,
                        LargeBinary,
                        ForeignKey)
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hashed = Column(String)


class Document(Base):
    __tablename__ = 'documents'

    doc_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_data = Column(LargeBinary, nullable=False)


class Contract(Base):
    __tablename__ = 'contract'

    con_id = Column(Integer, primary_key=True, autoincrement=True)
    con_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)


class Сontract_Documentt(Base):
    __tablename__ = "contract_document"

    con_doc_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contract.con_id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.doc_id"), nullable=False)
    date_bind = Column(DateTime, default=datetime.utcnow)
