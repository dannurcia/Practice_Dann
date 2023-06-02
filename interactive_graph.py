import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Define data
classifiers = ['Fraccionamiento', 'Identificación de ruta', 'Incrementos', 'Motivo del ROS', 'Vínculos', 'Promedio']
f1_scores = [0.57, 0.84, 0.73, 0.63, 0.0, 0.55]

# Create bar chart with Matplotlib
fig, ax = plt.subplots(figsize=(10,6))
ax.barh(classifiers, f1_scores)
ax.set_xlabel('F1-Score')
ax.set_ylabel('Clasificador')
ax.set_title('Rendimiento de Clasificadores')

# Create interactive bar chart with Plotly
fig = go.Figure(go.Bar(
            x=f1_scores,
            y=classifiers,
            orientation='h'))

fig.update_layout(
    title='Rendimiento de Clasificadores',
    xaxis_title='F1-Score',
    yaxis_title='Clasificador')

fig.show()
