import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# ==============================
# Step 1: Load or Create Dataset
# ==============================
# If you already have a CSV (e.g., "clinic_data.csv"), replace the df below with:
# df = pd.read_csv("clinic_data.csv")

# Example dataset
data = {
    'Patient_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Gender': ['Female', 'Male', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male']
}
df = pd.DataFrame(data)

# ==============================
# Step 2: Prepare Data
# ==============================
gender_counts = df['Gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']

# ==============================
# Step 3: Create Graphs
# ==============================
pie_chart = px.pie(
    gender_counts,
    values='Count',
    names='Gender',
    title='Gender Breakdown of Patients',
    color_discrete_sequence=px.colors.qualitative.Set2
)

bar_chart = px.bar(
    gender_counts,
    x='Gender',
    y='Count',
    text='Count',
    title='Number of Patients by Gender',
    color='Gender',
    color_discrete_sequence=px.colors.qualitative.Set2
)
bar_chart.update_traces(textposition='outside')

# ==============================
# Step 4: Build Dashboard Layout
# ==============================
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Clinic Dashboard: Gender Breakdown', style={'textAlign': 'center'}),

    html.Div([
        html.Div([dcc.Graph(figure=pie_chart)], className='six columns'),
        html.Div([dcc.Graph(figure=bar_chart)], className='six columns'),
    ], className='row'),

    html.Hr(),
    html.Div('This dashboard shows the gender distribution among all registered patients.',
             style={'textAlign': 'center', 'fontStyle': 'italic'})
])

# ==============================
# Step 5: Run App
# ==============================
if __name__ == '__main__':
    app.run_server(debug=True)
