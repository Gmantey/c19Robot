import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import hardwareDB as dataBase


# db = dataBase.connect()
# cursor = db[0]

# id = 1


X = deque(maxlen=25)
X.append(1)
Y = deque(maxlen=25)
Y.append(1)


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    X.append(X[-1]+1)
    data = dataBase.get_last("temp", X[-1])

    if (len(data) == 0):
        y_data = Y[-1]
    else:
        y_data = data[0][0]
    Y.append(y_data)

    print(X)
    print(Y)

    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y), max(Y)]),)}


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
