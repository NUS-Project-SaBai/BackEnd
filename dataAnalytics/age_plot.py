import os
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# ==============================
# Step 1: Load or Create Dataset
# ==============================
# If you already have a CSV (e.g., "clinic_data.csv"), replace the df below with:
# df = pd.read_csv("clinic_data.csv")

# Try to load an 'age_range' dataset from common file names in this folder.
# If none is found, fall back to a small example age list. The dataset should
# contain a column named 'Age' (case-insensitive) or a single column of ages.







#
#
#
# Change this to DB connection and query the data when needed
#
#












data_dir = os.path.dirname(__file__)
df = None
for fname in ("age_range.csv", "age_range.xlsx", "ages.csv", "ages.xlsx"):
    path = os.path.join(data_dir, fname)
    if os.path.exists(path):
        try:
            if path.lower().endswith('.csv'):
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path)
            print(f"Loaded age data from: {path}")
            break
        except Exception as e:
            print(f"Failed to read {path}: {e}")

if df is None:
    # No external file found — use an example age column. Replace this with your
    # real dataset or create an 'age_range.csv' file with an 'Age' column.
    df = pd.DataFrame({'Age': [23, 31, 45, 22, 35, 28, 67, 54, 19, 40, 31, 22, 35]})

# Normalize column name to 'Age' if possible (case-insensitive)
age_col = None
for col in df.columns:
    if col.lower() == 'age':
        age_col = col
        break
if age_col is None:
    # If the dataset only contains a single column, assume it's the age column
    if len(df.columns) == 1:
        age_col = df.columns[0]
    else:
        raise ValueError("Could not find an 'Age' column in the dataset. Please provide a file with an 'Age' column.")

# Ensure ages are numeric (coerce errors to NaN and drop them)
df['Age'] = pd.to_numeric(df[age_col], errors='coerce')
df = df.dropna(subset=['Age']).copy()
df['Age'] = df['Age'].astype(int)

# Compute counts per age (exact counts for each integer age in the dataset)
age_counts = df['Age'].value_counts().sort_index().reset_index()
age_counts.columns = ['Age', 'Count']

# Create a bar chart where each integer age has a bar equal to its count
age_bar = px.bar(
    age_counts,
    x='Age',
    y='Count',
    text='Count',
    title='Number of Patients by Exact Age',
    labels={'Age': 'Age (years)', 'Count': 'Number of Patients'},
    color_discrete_sequence=px.colors.qualitative.Pastel
)
age_bar.update_traces(textposition='outside')

# Also create a histogram (binned) view that can show grouped distributions.
age_hist = px.histogram(
    df,
    x='Age',
    nbins=max(5, min(30, int(df['Age'].max() - df['Age'].min()) + 1)),
    title='Age Distribution (Histogram)',
    labels={'Age': 'Age (years)', 'count': 'Number of Patients'},
    color_discrete_sequence=px.colors.sequential.Blues
)

# ==============================
# Step 4: Build Dashboard Layout
# ==============================
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Clinic Dashboard: Age Distribution', style={'textAlign': 'center'}),

    # Two visualizations: exact-count per age (bar) and binned histogram
    html.Div([
        html.Div([dcc.Graph(figure=age_bar)], className='six columns'),
        html.Div([dcc.Graph(figure=age_hist)], className='six columns'),
    ], className='row'),

    html.Hr(),
    html.Div('This dashboard shows the distribution of patient ages. The left chart shows exact counts per age; the right chart is a binned histogram.',
             style={'textAlign': 'center', 'fontStyle': 'italic'})
])

# ==============================
# Step 5: Run App
# ==============================
if __name__ == '__main__':
    app.run_server(debug=True)
