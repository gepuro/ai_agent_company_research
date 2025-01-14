\c cr

CREATE TABLE "users" (
  "user_id" serial PRIMARY KEY,
  "email" varchar(512) NOT NULL DEFAULT '',
  "hashed_password" varchar(512) NOT NULL DEFAULT '',
  "is_deleted" boolean NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX "idx_email" ON "users" ("email");
CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE set_updated_at();


-- 1,1000012160153,01,1,2018-04-02,2015-10-05,"釧路検察審査会",,101,"北海道","釧路市","柏木町４－７",,01,206,0850824,,,,,,,2015-10-05,1,"Kushiro Committee for the Inquest of Prosecution","Hokkaido","4-7, Kashiwagicho, Kushiro shi",,"クシロケンサツシンサカイ",0
-- 2,1000013050386,01,1,2018-04-02,2015-10-05,"伊達簡易裁判所",,101,"北海道","伊達市","末永町４７－１０",,01,233,0520021,,,,,,,2015-10-05,1,"Date Summary Court","Hokkaido","47-10, Suenagacho, Date shi",,"ダテカンイサイバンショ",0
CREATE TABLE "houjin_bangou" (
  "corporate_number" varchar(13) PRIMARY KEY,
  "company_name" varchar(512) NOT NULL DEFAULT '',
  "concatenation_address" varchar(512) NOT NULL DEFAULT '',
  "prefecture_name" varchar(16) NOT NULL DEFAULT '',
  "city_name" varchar(32) NOT NULL DEFAULT '',
  "town_name" varchar(32) NOT NULL DEFAULT '',
  "address_number" varchar(128) NOT NULL DEFAULT '',
  "lat" varchar(16) NOT NULL DEFAULT '',
  "lon" varchar(16) NOT NULL DEFAULT '',
  "post_code" varchar(16) NOT NULL DEFAULT '',
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "corporate_site" (
  "corporate_number" varchar(13) PRIMARY KEY,
  "url" varchar(512) NOT NULL DEFAULT '',
  "domain" varchar(128) NOT NULL DEFAULT '',
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "cache_url" (
  "url" varchar(512) PRIMARY KEY,
  "response" text NOT NULL DEFAULT '',
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "cache_gemini" (
  "prompt_hash" varchar(512) PRIMARY KEY,
  "model" varchar(512) NOT NULL DEFAULT '',
  "response" text NOT NULL DEFAULT '',
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "cache_google" (
  "search_word" varchar(512) PRIMARY KEY,
  "response" text NOT NULL DEFAULT '',
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "cache_company" (
  "corporate_number" varchar(13) PRIMARY KEY,
  "response" text NOT NULL DEFAULT '',
  "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
