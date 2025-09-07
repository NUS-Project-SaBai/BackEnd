from connection import connect_to_db
import pandas as pd

def get_patients(conn):
    query = "SELECT gender FROM patients;"  # SQL statement
    return pd.read_sql(query, conn)

if __name__ == "__main__":
    conn = connect_to_db()

    if conn:
        df_patients = get_patients(conn)
        print(df_patients.head())

        gender_counts = df_patients["gender"].value_counts()
        # this prints a gender breakdown table
        print("\nGender breakdown:")
        print(gender_counts) 

        conn.close()
