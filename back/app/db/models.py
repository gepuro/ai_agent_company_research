from re import I
from typing import Tuple

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.traversals import COMPARE_FAILED

from app.db import session


class User(session.Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    organization_id = Column(Integer)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())


# CREATE TABLE "houjin_bangou" (
#   "corporate_number" varchar(13) PRIMARY KEY,
#   "company_name" varchar(512) NOT NULL DEFAULT '',
#   "concatenation_address" varchar(512) NOT NULL DEFAULT '',
#   "prefecture_name" varchar(16) NOT NULL DEFAULT '',
#   "city_name" varchar(32) NOT NULL DEFAULT '',
#   "town_name" varchar(32) NOT NULL DEFAULT '',
#   "address_number" varchar(128) NOT NULL DEFAULT '',
#   "lat" varchar(16) NOT NULL DEFAULT '',
#   "lon" varchar(16) NOT NULL DEFAULT '',
#   "post_code" varchar(16) NOT NULL DEFAULT '',
#   "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
# )
class HoujinBangou(session.Base):
    __tablename__ = "houjin_bangou"
    corporate_number = Column(String, primary_key=True)
    company_name = Column(String, nullable=False, default="")
    concatenation_address = Column(String, nullable=False, default="")
    prefecture_name = Column(String, nullable=False, default="")
    city_name = Column(String, nullable=False, default="")
    town_name = Column(String, nullable=False, default="")
    address_number = Column(String, nullable=False, default="")
    lat = Column(String, nullable=False, default="")
    lon = Column(String, nullable=False, default="")
    post_code = Column(String, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())


# CREATE TABLE "corporate_site" (
#   "corporate_number" varchar(13) PRIMARY KEY,
#   "url" varchar(512) NOT NULL DEFAULT '',
#   "domain" varchar(128) NOT NULL DEFAULT '',
#   "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
# )
class CorporateSite(session.Base):
    __tablename__ = "corporate_site"
    corporate_number = Column(String, primary_key=True)
    url = Column(String, nullable=False, default="")
    domain = Column(String, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())


# CREATE TABLE "cache_url" (
#   "url" varchar(512) PRIMARY KEY,
#   "response" text NOT NULL DEFAULT '',
#   "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
# )
class CacheUrl(session.Base):
    __tablename__ = "cache_url"
    url = Column(String, primary_key=True)
    response = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())


# CREATE TABLE "cache_gemini" (
#   "url" varchar(512) PRIMARY KEY,
#   "model" varchar(512) NOT NULL DEFAULT '',
#   "response" text NOT NULL DEFAULT '',
#   "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
# )
class CacheGemini(session.Base):
    __tablename__ = "cache_gemini"
    prompt_hash = Column(String, primary_key=True)
    model = Column(String, nullable=False, default="")
    response = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())


# CREATE TABLE "cache_google" (
#   "search_word" varchar(512) PRIMARY KEY,
#   "response" text NOT NULL DEFAULT '',
#   "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
# )
class CacheGoogle(session.Base):
    __tablename__ = "cache_google"
    search_word = Column(String, primary_key=True)
    response = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())


# CREATE TABLE "cache_company" (
#   "corporate_number" varchar(13) PRIMARY KEY,
#   "response" text NOT NULL DEFAULT '',
#   "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
# )
class CacheCompany(session.Base):
    __tablename__ = "cache_company"
    corporate_number = Column(String, primary_key=True)
    response = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=current_timestamp())
