-- connect to the correct db 
-- this name is determined in the docker-compose file
\connect supportsConnect_database

-- Clean up
DROP SCHEMA IF EXISTS NewsCollectorInfo CASCADE;

-- Create schema
CREATE SCHEMA NewsCollectorInfo;

-- Create user-defined data type with constraints for URLs 
CREATE DOMAIN URL AS VARCHAR(250);

-- create enumeration type of types of articles and media outlets
CREATE TYPE TYPEOFARTICLE AS ENUM ('Opinion', 'News');

CREATE TABLE NewsCollectorInfo.PublicNewsAPISources (
	id 					INT 			GENERATED ALWAYS AS IDENTITY,
	name 				VARCHAR(50) 	NOT NULL,
	endpoint_URL		URL 			NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE NewsCollectorInfo.ArticleContent (
	id 					INT 			GENERATED ALWAYS AS IDENTITY,
	content 			TEXT,
	PRIMARY KEY(id)
);

CREATE TABLE NewsCollectorInfo.MediaOutlets (
	id 					INT 			GENERATED ALWAYS AS IDENTITY,
	name				VARCHAR(50)		NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE NewsCollectorInfo.Topics (
	id					INT 			GENERATED ALWAYS AS IDENTITY,
	name				VARCHAR(100) 	NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE NewsCollectorInfo.ArticleSummary (
	id 					INT 			GENERATED ALWAYS AS IDENTITY,
	who					VARCHAR(250),
	what				VARCHAR(250),
	when_				VARCHAR(250),
	where_				VARCHAR(250),
	why					VARCHAR(250),
	how					VARCHAR(250),
	PRIMARY KEY(id)
);

-- timestamptz is short for timestamp with timezone
CREATE TABLE NewsCollectorInfo.Articles (
	id 					INT 			GENERATED ALWAYS AS IDENTITY,
	created_at			TIMESTAMPTZ 	NOT NULL DEFAULT NOW(),
	title 				VARCHAR(250)	NOT NULL, 
	web_content_url		URL,
	api_content_url		URL,
	article_type 		TYPEOFARTICLE 	NOT NULL,
	publication_date 	TIMESTAMP 		NOT NULL, 
	author				VARCHAR(50),
	text_summary		INT,
	media_outlet_id	 	INT    			NOT NULL,
	content_id			INT,
	PRIMARY KEY(id),
	CONSTRAINT foreign_key_content 		FOREIGN KEY(content_id) 	 REFERENCES NewsCollectorInfo.ArticleContent(id),
	CONSTRAINT foreign_key_media_outlet FOREIGN KEY(media_outlet_id) REFERENCES NewsCollectorInfo.MediaOutlets(id),
	CONSTRAINT foreign_key_summary		FOREIGN KEY(text_summary) REFERENCES NewsCollectorInfo.ArticleSummary(id)
);

CREATE TABLE NewsCollectorInfo.TopicOfArticle (
	id					INT 			GENERATED ALWAYS AS IDENTITY,
	topic_id			INT 			NOT NULL,
	article_id			INT 			NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT foreign_key_topic 		FOREIGN KEY(topic_id)				REFERENCES NewsCollectorInfo.Topics(id),
	CONSTRAINT foreign_key_article		FOREIGN KEY(article_id)				REFERENCES NewsCollectorInfo.Articles(id)
);


-- USER TABLES - this should be in a different schema, but just put it here for the meantime
CREATE TABLE NewsCollectorInfo.User (
	id 					VARCHAR(100) 			NOT NULL, 
	PRIMARY KEY(id)
);

CREATE TABLE NewsCollectorInfo.UserConfiguration (
	id 					INT 			GENERATED ALWAYS AS IDENTITY,
	config_name 		VARCHAR(100)	NOT NULL,
	usr_id				VARCHAR(100)	NOT NULL, 
	PRIMARY KEY(id),
	CONSTRAINT foreign_key_user			FOREIGN KEY(usr_id)			REFERENCES NewsCollectorInfo.User(id)
);	

-- By enforcing the primary key as such, you make sure that can't select the same 
-- config option for a given saved user config
CREATE TABLE NewsCollectorInfo.TopicConfiguration (
	id 					INT 			GENERATED ALWAYS AS IDENTITY,
	usr_config_id		INT 			NOT NULL, 
	topic_id 			INT 			NOT NULL,
	topic_name 			VARCHAR(100)	NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT foreign_key_usr_config 	FOREIGN KEY(usr_config_id) 	REFERENCES NewsCollectorInfo.UserConfiguration(id),
	CONSTRAINT foreign_key_topic		FOREIGN KEY(topic_id)		REFERENCES NewsCollectorInfo.Topics(id)
);