
from connection import connect_to_db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



###### Consults Table
def get_consults(conn):
    query = "SELECT * FROM consults;"  # SQL statement
    return pd.read_sql(query, conn)

####### Vitals Table
def get_vitals(conn):
    query = "SELECT * FROM vitals;"  # SQL statement
    print("Vitals Table")
    return pd.read_sql(query, conn)



if __name__ == "__main__":
    conn = connect_to_db()

    if conn:
        # Vitals
        df_vitals = get_vitals(conn)

        print("Analysis of Height Distribution")
        print("\nMin height:")
        print(df_vitals["height"].min())
        print("\nValue Counts")
        print(df_vitals["height"].value_counts())

        df_vitals["height"].sort_values()
        df_vitals["height"].isnull().sum()
        print("\nIgnoring the 0.0, the minimum height is 10.0 cm and the maximum height is 171.0 cm")
        print("\nDescription")
        print(df_vitals["height"].describe())
        data = df_vitals[df_vitals["height"] > 0]["height"]
        print("Graphs are drawn after filtering out height = 0")

        plt.hist(data, bins=25, edgecolor='black')
        plt.xlabel("Height")
        plt.ylabel("Frequency")
        plt.title("Distribution of height of patients")
        plt.xticks(np.arange(0, 175, 10))
        print("We can see that there is clustering between 110 cm to 160 cm")
        print("The anomalies of 70-90 cm is probably due a patient who is a child")

        plt.figure(figsize=(8,2))
        sns.boxplot(x=data)
        plt.title("Boxplot of height distribution of patients")
        plt.xticks(np.arange(0, 200, 10))
       

        print("Final analysis of weight distribution")
        print("The distrubution of height ranges from 0cm to 181 cm, with a few anomalies observed from 0cm to 70 cm. Some low values are explained by taking the height of children, however, these values seem too low for the height of children hence is concluded to be inaccurate key-ins. There is a clusterig of data between 120cm-160cm, with a median of 146cm, and a mean of 139cm.")
        print("Limitations of analysis: Height value was not filled in for 13 values, hence the analysis might be slightly inaccurate.")

        plt.show()


        conn.close()

