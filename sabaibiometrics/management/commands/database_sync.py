from django.core.management.base import BaseCommand
from dotenv import load_dotenv
import os
from django.db import connections
import subprocess
from datetime import datetime

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        load_dotenv()
        if not self.checkRequiredEnv():
            return
        
        menu = '''  
        dump_local - dump local database (public schema only) into /dumps
        dump_remote - dump remote database (public schema only) into /dumps
        verify - check if local and remote database are the same
        restore - restore to a database from a dump. Please ensure that if you're restoring the local database from a remote database, it should be cleaned first.
        drop - removes public schema from a database. This command won't do it for you but it will tell you what to run.
        '''

        print(menu)
        user_input = input()

        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        dumps_dir = os.path.join(project_root, "dumps")

        #TODO: data validation for input file path.
        if user_input == "dump_local":
            file_name = self.ts()+"_local.sql"
            self.create_dump("default", os.path.join(dumps_dir, file_name))
        elif user_input == "dump_remote":
            file_name = self.ts()+"_remote"
            path = os.path.join(dumps_dir, file_name)
            self.create_dump("remote", path + ".sql")
            self.clean_dump(path + ".sql", path +"_cleaned.sql")
        elif user_input == "verify":
            self.verify_all_tables()
        elif user_input == "drop":
            self.drop()
        elif user_input == "restore":
            print("Input which database to restore to (you are overwriting this database) remote/default")
            db = input()
            if (db != "remote") & (db != "default"):
                print("Invalid input. Exiting")
                return
            print("Input the file name of the dump")
            path = input()
            self.restore_dump(db, os.path.join(dumps_dir, path))
        else:
            print("Invalid input. Exiting")

    def ts(self):
        return datetime.now().strftime("%d_%m_%Y_%H%M%S")

    def create_dump(self, connection_alias, output_file):
        """
        Dump a database schema to a SQL file.
        
        Args:
            connection_alias: 'default' or 'remote'
            output_file: Path where the dump file should be saved
        """
        import pdb;pdb.set_trace()
        db_settings = connections[connection_alias].settings_dict
        
        connection_url = (
            f"postgresql://{db_settings['USER']}:{db_settings['PASSWORD']}"
            f"@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"
        )
        
        print(f"Dumping {connection_alias} database to {output_file}...")
        subprocess.run([
            os.getenv("PG_SCRIPTS_PATH") + "pg_dump.exe",
            "--schema=public",
            "--no-owner",
            "--no-privileges",
            "--file", output_file,
            connection_url
        ], check=True)
        print(f"Dump complete: {output_file}")

    # TODO: consider shifting to pg 17 for development? then we can erase this function
    def clean_dump(self, input_file, output_file):

        """
        Solves pg17-15 incompatibility issues.
        
        Args:
            input_file: Path to the original dump file
            output_file: Path where the cleaned dump should be saved
        """
        pg17_params = [
            'transaction_timeout',
        ]
        
        print(f"Cleaning dump file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as infile:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    if not any(param in line for param in pg17_params):
                        outfile.write(line)
        print(f"Cleaned dump saved to: {output_file}")


    def restore_dump(self, connection_alias, dump_file):
        """
        Restore a SQL dump file to a database.
        
        Args:
            connection_alias: Django connection alias ('default', 'remote', etc.)
            dump_file: Path to the SQL dump file to restore
        """
        db_settings = connections[connection_alias].settings_dict
        
        connection_url = (
            f"postgresql://{db_settings['USER']}:{db_settings['PASSWORD']}"
            f"@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"
        )
        
        print(f"Restoring {dump_file} into {connection_alias} database...")
        subprocess.run([
            os.getenv("PG_SCRIPTS_PATH") + "psql.exe",
            "--dbname", connection_url,
            "--file", dump_file,
            "--quiet"
        ], check=True)
        print("Restore complete.")

    def drop(self):
        print("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        print("I don't want anyone to randomly use this lol")

    def checkRequiredEnv(self):

        """
        Checks if the required variables in .env file are present. If this is true, program quits immediately.

        """
        required = ["LIVE_POSTGRES_DATABASE_URL", "POSTGRES_NAME", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT"]
        for req in required:
            if os.getenv(req) == "":
                print(req, " is missing. Check your .env file and run the command again. Exiting")
                return False
        if os.getenv("OFFLINE") == "True":
            return True
        else:
            print("Offline needs to be set to True in the .env file. Exiting.")
        return False
    
    # TODO: check these 2 functions.
    def verify_all_tables(self):
        """
        Verify ALL data for ALL tables in the public schema.
        Performs complete data integrity check.
        """
        from django.db import connections
        import time
        
        remote_conn = connections["remote"]
        
        # Get all tables
        with remote_conn.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """)
            tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n{'='*80}")
        print(f"COMPLETE DATA VERIFICATION")
        print(f"{'='*80}")
        print(f"Verifying ALL data in {len(tables)} tables...")
        print(f"This will check every row in every table.\n")
        
        start_time = time.time()
        results = {}
        
        for i, table in enumerate(tables, 1):
            print(f"\n[{i}/{len(tables)}] Processing table: {table}")
            try:
                result = self.verify_table_data(table)
                results[table] = result
            except Exception as e:
                print(f"\nError checking {table}: {e}")
                import traceback
                traceback.print_exc()
                results[table] = False
        
        elapsed = time.time() - start_time
        
        # Summary
        print("\n" + "=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for v in results.values() if v)
        failed = len(results) - passed
        
        print(f"Total tables: {len(results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        
        if failed > 0:
            print(f"\nFAILED TABLES:")
            for table, result in results.items():
                if not result:
                    print(f"  - {table}")
            print(f"\nDATABASE SYNC VERIFICATION FAILED")
            return False
        else:
            print(f"\nALL TABLES VERIFIED - DATABASES ARE IDENTICAL")
            return True
    
    def verify_table_data(self, table_name):
        """
        Verify that ALL data in a specific table matches between remote and local.
        
        Args:
            table_name: Name of the table to check
        """
        from django.db import connections
        
        remote_conn = connections["remote"]
        local_conn = connections["default"]
        
        print(f"\nVerifying ALL data for table: {table_name}")
        print("=" * 80)
        
        # Get primary key column(s)
        with remote_conn.cursor() as cursor:
            cursor.execute("""
                SELECT a.attname
                FROM pg_index i
                JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                WHERE i.indrelid = %s::regclass AND i.indisprimary
                ORDER BY a.attnum
            """, [f'public.{table_name}'])
            pk_columns = [row[0] for row in cursor.fetchall()]
        
        if pk_columns:
            print(f"Primary key: {', '.join(pk_columns)}")
            order_by = f"ORDER BY {', '.join(pk_columns)}"
        else:
            print("No primary key found. Results may be unordered.")
            order_by = ""
        
        # Get row count
        with remote_conn.cursor() as cursor:
            cursor.execute(f'SELECT COUNT(*) FROM public."{table_name}"')
            total_rows = cursor.fetchone()[0]
        
        print(f"Total rows to check: {total_rows}")
        
        # Get ALL data from both databases
        query = f'SELECT * FROM public."{table_name}" {order_by}'
        
        print("Fetching remote data...")
        with remote_conn.cursor() as cursor:
            cursor.execute(query)
            remote_columns = [desc[0] for desc in cursor.description]
            remote_rows = cursor.fetchall()
        
        print("Fetching local data...")
        with local_conn.cursor() as cursor:
            cursor.execute(query)
            local_columns = [desc[0] for desc in cursor.description]
            local_rows = cursor.fetchall()
        
        # Check schema matches
        if remote_columns != local_columns:
            print(f"Schema mismatch!")
            print(f"Remote columns: {remote_columns}")
            print(f"Local columns: {local_columns}")
            return False
        
        print("Comparing data...")
        
        # Convert to sets of tuples for comparison
        # Use string representation to handle different data types
        remote_set = {tuple(str(v) if v is not None else None for v in row) for row in remote_rows}
        local_set = {tuple(str(v) if v is not None else None for v in row) for row in local_rows}
        
        # Find differences
        only_remote = remote_set - local_set
        only_local = local_set - remote_set
        
        if only_remote or only_local:
            print(f"\nData mismatch found!")
            if only_remote:
                print(f"Rows only in remote: {len(only_remote)}")
                print(f"First 5 examples:")
                for i, row in enumerate(list(only_remote)[:5]):
                    print(f"{dict(zip(remote_columns, row))}")
            if only_local:
                print(f"Rows only in local: {len(only_local)}")
                print(f"First 5 examples:")
                for i, row in enumerate(list(only_local)[:5]):
                    print(f"{dict(zip(local_columns, row))}")
            return False
        
        print(f"\nAll {total_rows} rows match perfectly!")
        return True
