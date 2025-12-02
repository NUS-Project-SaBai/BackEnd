import os
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Try to load medicine dispensed counts from the DB. Fall back to example data.
from dataAnalytics.connection import connect_to_db

# SQL to aggregate dispensed quantity per medicine. Adjust column/table names if your
# schema differs. This sums `quantity_changed` from `medication_review` for reviews
# with status 'APPROVED' (i.e., dispensed). If your project uses a different
# column to indicate dispensed quantity, modify the SQL accordingly.
MEDICINE_SQL = """
SELECT m.medicine_name,
       COALESCE(SUM(mr.quantity_changed), 0) AS total_dispensed,
       COUNT(mr.id) AS times_reviewed
FROM medication_review mr
LEFT JOIN medication m ON mr.medicine = m.id
WHERE mr.order_status = 'APPROVED'
GROUP BY m.medicine_name
ORDER BY total_dispensed DESC
LIMIT 50;
"""


def load_medicine_data():
    df = None
    conn = connect_to_db()
    if conn:
        try:
            df = pd.read_sql_query(MEDICINE_SQL, conn)
            if df.empty:
                print("No rows returned from medicine query; falling back to sample data.")
        except Exception as e:
            print(f"Error querying medicine data: {e}")
        finally:
            try:
                conn.close()
            except Exception:
                pass

    if df is None or df.empty:
        # Fallback sample data (medicine_name, total_dispensed)
        df = pd.DataFrame({
            'medicine_name': [
                'Paracetamol 500mg',
                'Amoxicillin 500mg',
                'Cough Syrup 100ml',
                'Ibuprofen 200mg',
                'Metformin 500mg'
            ],
            'total_dispensed': [124, 98, 76, 64, 55],
            'times_reviewed': [60, 50, 42, 39, 28]
        })
        print("Using fallback sample medicine data.")

    # Normalize names and ensure numeric
    df['medicine_name'] = df['medicine_name'].astype(str)
    df['total_dispensed'] = pd.to_numeric(df['total_dispensed'], errors='coerce').fillna(0).astype(int)
    return df


# Build charts
medicine_df = load_medicine_data()

# If there are many distinct medicine names, horizontal bar is easier to read
medicine_bar = px.bar(
    medicine_df.sort_values('total_dispensed', ascending=True),
    x='total_dispensed',
    y='medicine_name',
    orientation='h',
    text='total_dispensed',
    title='Top Medicines by Units Dispensed',
    labels={'total_dispensed': 'Units Dispensed', 'medicine_name': 'Medicine'},
    color_discrete_sequence=px.colors.qualitative.Set3
)
medicine_bar.update_traces(textposition='outside')
medicine_bar.update_layout(margin={'l': 200})

# Also produce a simple vertical bar for the top N names (if desired)
medicine_bar_vertical = px.bar(
    medicine_df.sort_values('total_dispensed', ascending=False).head(20),
    x='medicine_name',
    y='total_dispensed',
    text='total_dispensed',
    title='Top 20 Medicines by Units Dispensed',
    labels={'total_dispensed': 'Units Dispensed', 'medicine_name': 'Medicine'},
    color_discrete_sequence=px.colors.qualitative.Set2
)
medicine_bar_vertical.update_traces(textposition='outside')
medicine_bar_vertical.update_layout(xaxis_tickangle=-45)

# Build a minimal Dash app layout (similar to `age_plot.py`)
app = Dash(__name__)
app.layout = html.Div([
    html.H1('Pharmacy Dashboard: Most Dispensed Medicines', style={'textAlign': 'center'}),

    html.Div([
        html.Div([dcc.Graph(figure=medicine_bar)], className='six columns'),
        html.Div([dcc.Graph(figure=medicine_bar_vertical)], className='six columns'),
    ], className='row'),

    html.Hr(),
    html.Div('This dashboard shows the most commonly dispensed medicines. Data is aggregated from medication_review (approved reviews).',
             style={'textAlign': 'center', 'fontStyle': 'italic'})
])


if __name__ == '__main__':
    app.run_server(debug=True)
