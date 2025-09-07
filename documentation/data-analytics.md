# 🩺 Data Analytics Guide

This folder contains scripts to generate data analytics (charts + CSVs) from the **PostgreSQL** database.  
The purpose is to quickly run scripts during/after the trip to provide the medicine team with the data they need.

---

## ⚙️ 1. Setup

1. Pull the `data-analytics` branch
2. Create a new branch `git checkout -b data-analytics-<itemID>`
3. Install Python dependencies (if needed)
4. Write the script

We would need to first write an SQL query to get the relevant table from postgres
```py
def get_patients(conn):
    query = "SELECT gender FROM patients;"
    return pd.read_sql(query, conn)
```

Thereafter, we would connect with the database using `connect_to_db()` from `connection.py` and display/download the relevant materials.

```py
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
```

## 2. Run an Example
```bash
python dataAnalytics/patientsGender.py
```
This will
- Load database credentials from your .env file
- Connect to PostgreSQL
- Query the patients table
- Print out the first 5 rows and a gender breakdown (depending on code logic)

Do note that the database you are connected to should be the updated one with 23 tables in total. If your table happen to be empty, you can insert some dummy values into the table via pgAdmin4 using `SQL` statements

## 3. Push to Github
1. Stage and commit your changes
2. Push your branch `git push origin data-analytics-<itemID>`
3. On GitHub, open a <b>Pull Request (PR)</b>
    - <b>Base branch</b>: data-analytics
    - <b>Compare branch</b>: your `data-analytics-<itemID>`
4. In the PR description, include:
    - what the script does
    - which tables/columns it queries
    - example of expected outputs (CSV/chart names) 


