from connection import connect_to_db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



###### Consults Table
def get_patients(conn):
    query = "SELECT * FROM patients;"  # SQL statement
    return pd.read_sql(query, conn)




if __name__ == "__main__":
    conn = connect_to_db()

    if conn:
        # Vitals
        patients_df = get_patients(conn)

        print("Total Patients: ", patients_df["id"].count())
        print("BS2 Card Frequency: ", patients_df[patients_df["bs2"] == "Yes"]["bs2"].count())
        print("SaBai Card Frequency: ", patients_df[patients_df["sabai"] == "Yes"]["sabai"].count())
        print("Poor Card Frequency: ", patients_df[patients_df["poor"] == "Yes"]["poor"].count())



        conn.close()

