CREATE EXTENSION pg_turso CASCADE;
CREATE OR REPLACE FUNCTION turso_token() RETURNS text LANGUAGE SQL AS $$ SELECT 'secret-token'; $$;
CREATE OR REPLACE FUNCTION turso_url() RETURNS text LANGUAGE SQL AS $$ SELECT 'https://test-tristenharr.turso.io/'; $$;
