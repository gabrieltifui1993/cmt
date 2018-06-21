import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('totals.csv', delimiter="|")
classes = df['label'].tolist()
quantities = df['total'].tolist()

plt.bar(classes, quantities, align='center', alpha=0.5)
plt.style.use('fivethirtyeight')

#plt.show()

import plotly
import plotly.graph_objs as go

trace1 = go.Bar(
    x=classes,
    y=quantities,
    name='Uncleared'
)

data = [trace1]

layout = go.Layout(
    autosize=False,
    width=800,
    height=500,
    barmode='group'
)
#fig = go.Figure(data=data, layout=layout)
#plotly.offline.plot(fig)


trace_positive = go.Bar (
    x = ['positive', 'cleared positive'],
    y = [646641, 10739],
    name='positive filtering'
)

trace_negative = go.Bar(
    x = ['negative', 'cleared_negative'],
    y = [604162, 12625],
    name='negative filtering'
)

data = [trace_positive, trace_negative]

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig)

