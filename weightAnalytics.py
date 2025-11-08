from connection import connect_to_db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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
        print("\nWeight Distribution")
        print("\nValue Counts")
        print(df_vitals["weight"].value_counts().sort_index(ascending=False))
        print("Median: ", df_vitals["weight"].median())
        print("\nDescription")
        print(df_vitals["weight"].describe())
        plt.hist(df_vitals["weight"], bins=25, edgecolor='black')
        plt.xlabel("Weight")
        plt.ylabel("Frequency")
        plt.title("Distribution of weight of patients")
        plt.xticks(np.arange(0, 820, 50))
        print("There seems to be an anomaly at around 800 kgs and 200 kgs")
        print("### There is clustering between 40-70 kgs. It is unknown if the anomalies of the lower weights below 10 are legitimate or are due to masses of infants.") 
        plt.figure(figsize=(8,2))
        sns.boxplot(x=df_vitals[df_vitals["weight"] > 0]["weight"])
        plt.title("Boxplot of weight distribution of patients")
        plt.show()
        print("0 and the value around 200 and 800 are probably wrongly keyed values")

        print("\nFinal Analysis")
        print("The distribution of weight ranges from 0 to 820, with a median of 41.6 and a mean of 41.0. However, the values 0.0, and over 200 are treated as anomalies. There is a clustering between 0-75, showing that this is the most common weights of the patients.")


        conn.close()

