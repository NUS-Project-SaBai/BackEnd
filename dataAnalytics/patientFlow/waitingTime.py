from connection import connect_to_db
import pandas as pd
import matplotlib.pyplot as plt

def getTimeDifference(conn):
    query = """
    SELECT 
        v.id AS visit_id,
        v.date AS visit_date,
        c.id AS consult_id,
        c.date AS consult_date,
        p.village_prefix,
        p.id AS patient_id
    FROM 
        visits v
    JOIN 
        consults c ON v.id = c.visit_id
    JOIN
        patients p ON v.patient_id = p.id;
"""  # SQL statement
    return pd.read_sql(query, conn)

if __name__ == "__main__":
    conn = connect_to_db()

    if conn:
        combined_data = getTimeDifference(conn)

        combined_data['visit_date'] = combined_data['visit_date'] + pd.Timedelta(hours=7)
        combined_data['consult_date'] = combined_data['consult_date'] + pd.Timedelta(hours=7)

        combined_data['time_difference'] = combined_data['consult_date'] - combined_data['visit_date']
        combined_data = combined_data.sort_values(by='patient_id').reset_index(drop=True)
        combined_data['time_difference_hours'] = combined_data['time_difference'].dt.total_seconds() / 3600
        combined_data['day'] = combined_data['visit_date'].dt.date
        average_waiting_time_daily = combined_data.groupby('day')['time_difference_hours'].mean().reset_index()
        average_waiting_time_daily.rename(columns={'time_difference_hours': 'average_waiting_time_hours'}, inplace=True)

        plt.figure(figsize=(10, 6))
        plt.plot(average_waiting_time_daily['day'], average_waiting_time_daily['average_waiting_time_hours'], marker='o', color='blue')
        plt.title("Average Waiting Time (Hours) Per Day")
        plt.xlabel("Day")
        plt.ylabel("Average Waiting Time (Hours)")
        plt.grid(axis='y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("average_waiting_time_daily.png")
        plt.show()

        combined_data['hour'] = combined_data['visit_date'].dt.hour
        hourly_waiting_time = combined_data.groupby(['day', 'village_prefix', 'hour'])['time_difference_hours'].mean().reset_index()
        for (day, prefix), data in hourly_waiting_time.groupby(['day', 'village_prefix']):
            plt.figure(figsize=(10, 6))
            plt.plot(data['hour'], data['time_difference_hours'], marker='o', color='blue', label=f"{prefix} - {day}")
            plt.title(f"Hourly Average Waiting Time on {day} - Clinic {prefix}")
            plt.xlabel("Hour of the Day")
            plt.ylabel("Average Waiting Time (Hours)")
            plt.xticks(range(7, 19))
            plt.grid(axis='y')
            plt.tight_layout()
            plt.savefig(f"hourly_waiting_time_{prefix}_{day}.png")
            plt.show()
        
        combined_data['day'] = combined_data['visit_date'].dt.date

        # Group by village_prefix and day to calculate daily average waiting time
        daily_waiting_time = combined_data.groupby(['village_prefix', 'day'])['time_difference_hours'].mean().reset_index()

        # **Plot: PC Daily Bar Chart**
        pc_data = daily_waiting_time[daily_waiting_time['village_prefix'] == 'PC']

        plt.figure(figsize=(10, 6))
        bars = plt.bar(pc_data['day'].astype(str), pc_data['time_difference_hours'], color='blue', edgecolor='black', alpha=0.7)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, round(height, 2),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.title("Daily Average Waiting Time - Clinic PC")
        plt.xlabel("Day")
        plt.ylabel("Average Waiting Time (Hours)")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("daily_waiting_time_PC_bar.png")
        plt.show()

        # **Plot: SV Daily Bar Chart**
        sv_data = daily_waiting_time[daily_waiting_time['village_prefix'] == 'SV']

        plt.figure(figsize=(10, 6))
        bars = plt.bar(sv_data['day'].astype(str), sv_data['time_difference_hours'], color='green', edgecolor='black', alpha=0.7)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, round(height, 2),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')


        plt.title("Daily Average Waiting Time - Clinic SV")
        plt.xlabel("Day")
        plt.ylabel("Average Waiting Time (Hours)")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("daily_waiting_time_SV_bar.png")
        plt.show()

        # **Plot: Overall Average Waiting Time Across Village Prefixes**
        overall_waiting_time = combined_data.groupby('village_prefix')['time_difference_hours'].mean().reset_index()

        plt.figure(figsize=(8, 6))
        bars = plt.bar(overall_waiting_time['village_prefix'], overall_waiting_time['time_difference_hours'],
                color=['blue', 'green', 'orange', 'purple', 'red'], edgecolor='black', alpha=0.7)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, round(height, 2),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.title("Overall Average Waiting Time Across Village Prefixes")
        plt.xlabel("Village Prefix")
        plt.ylabel("Average Waiting Time (Hours)")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("overall_waiting_time_village_prefix_bar.png")
        plt.show()
        conn.close()
