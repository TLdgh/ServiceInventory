DO $$ 
DECLARE
    r RECORD;
	dropfr TEXT;
	
BEGIN
    -- Loop through columns matching the pattern '%\_fr'
    FOR r IN 
        SELECT column_name
        FROM information_schema.columns
        WHERE column_name LIKE '%\_fr' ESCAPE '\'
        AND table_name = 'SIdata'
    LOOP
        -- Dynamically drop each column
        dropfr:=format('ALTER TABLE public."SIdata" DROP COLUMN IF EXISTS %I;', r.column_name);
		EXECUTE dropfr;
    END LOOP;
END $$;