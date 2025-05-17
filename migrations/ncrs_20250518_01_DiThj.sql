-- Create the tables for the GitHub and Discord metadata (First Tables in Database!)
-- depends: 


CREATE TABLE "github" (
	"id" serial NOT NULL UNIQUE,
	"repository" varchar(255) NOT NULL,
	"issue_id" int NOT NULL UNIQUE,
	"author" varchar(255) NOT NULL,
	PRIMARY KEY("id")
);

COMMENT ON TABLE github IS 'Table used for storing GitHub metadata. Internal ID same as Discord table';


CREATE TABLE "discord" (
	"id" serial NOT NULL UNIQUE,
	"guild_id" int NOT NULL,
	"forum_id" int NOT NULL,
	"thread_id" int NOT NULL,
	"author_id" int NOT NULL,
	PRIMARY KEY("id")
);

COMMENT ON TABLE discord IS 'Table used for storing Discord metadata. Internal ID same as GitHub table';


ALTER TABLE "discord"
ADD FOREIGN KEY("id") REFERENCES "github"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;