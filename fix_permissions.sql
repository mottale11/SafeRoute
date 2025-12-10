-- Run this as the postgres superuser to grant permissions to saferoute_user
-- Connect as postgres user and run these commands:

-- Grant schema usage
GRANT USAGE ON SCHEMA public TO saferoute_user;

-- Grant create privileges
GRANT CREATE ON SCHEMA public TO saferoute_user;

-- Grant all privileges on database
GRANT ALL PRIVILEGES ON DATABASE saferoute_db TO saferoute_user;

-- Grant all privileges on all tables (for existing and future tables)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO saferoute_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO saferoute_user;

-- If tables already exist, grant privileges on them
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO saferoute_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO saferoute_user;

