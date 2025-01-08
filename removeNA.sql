DO $$
DECLARE
	r RECORD;
	update_query TEXT;

BEGIN
	FOR r IN
		select column_name 
		from information_schema.columns
			where table_name = 'SIdata'
	
	LOOP
		update_query:=format('
			UPDATE "SIdata"
			SET %I = CASE
						WHEN %I = ''N/a'' OR %I = ''NA'' OR %I = ''N/A'' OR %I = ''n/a'' THEN NULL
						ELSE %I
					END;', 
					r.column_name, r.column_name, r.column_name, r.column_name, r.column_name, r.column_name);
		EXECUTE update_query;
	END LOOP;
END$$;
	