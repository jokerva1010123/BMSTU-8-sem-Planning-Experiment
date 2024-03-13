import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from model import calculate_reley_param, \
                  calculate_gauss_params, \
                  GenerateRequest, ReleyGenerator, \
                  ProcessRequest, GaussGenerator, \
                  Model
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    external_scripts=[
        'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
    ]
)


app.layout = html.Div(id='main', children=[
    html.H3('Количество заявок'),
    dcc.Input(id='num', value=300, debounce=True, type='number', min=1),

    html.H3('Поступление заявок'),
    html.Span(id='sigma_r', children='Интенсивность'),
    dcc.Input(id='sigma_r_input', debounce=True, value=3, type='text'),

    html.H3('Обработка заявок'),
    html.Span(id='mu', children='Интенсивность'),
    dcc.Input(id='mu_input', debounce=True, value=2, type='text'),
    html.Br(),
    html.Span(id='sigma_n', children='Разброс'),
    dcc.Input(id='sigma_n_input', debounce=True, value=1, type='text'),
    html.Br(),

    html.H3('Расчетная загрузка системы'),
    html.Span(id='load_c', children=''),
    html.H3('Среднее время ожидания'),
    html.Span(id='load_r', children=''),

    dbc.Row(
        [
            dbc.Col(children=
                dcc.Graph(
                    id='graph',
                    figure=go.Figure(data=[go.Scatter(x=[], y=[])])
                ), width={"size": 3})
        ], style={"padding": "3px"}
    ),
    html.Button('Построить график', id='draw', n_clicks=0)
])


@app.callback(
    Output('graph', 'figure'),
    [Input('draw', 'n_clicks'), Input('num', 'value')])
def graphic(n_clicks, clients_number):
    i = 0.01
    dm = 0.3
    mas = []
    res = []
    while i < 0.95:
        mas_i = []
        intensivity_gen = 3
        intensivity_proc = intensivity_gen * i * i * i
        mas.append(i)
        if i < 0.6:
            i += 0.1
        else:
            i += 0.01
        print(i)

        i1, i2, di = intensivity_gen, intensivity_proc, dm
        for j in range(30):
            generator = GenerateRequest(ReleyGenerator(i1), clients_number)
            processor = ProcessRequest(GaussGenerator(i2, di))

            model = Model([generator], [processor])
            result = model.event_mode()
            mas_i.append(result)

        res.append(sum(mas_i) / len(mas_i))
        mas_i.clear()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mas, y=res, mode="lines"))
    fig.update_layout(xaxis_title="Загрузка системы", yaxis_title="Время ожидания")

    return fig


@app.callback(
    [Output('load_c', 'children'), Output('load_r', 'children')],
    [Input('num', 'value'),
     Input('mu_input', 'value'), Input('sigma_n_input', 'value'),
     Input('sigma_r_input', 'value')])
def count_load(clients_number, i1, di1, i2):
    try:
        i1 = float(i1)
        di1 = float(di1)
        i2 = float(i2)
    except TypeError:
        return ['', '']

    if (i1 < 0.0001 or di1 < 0.0001 or i2 < 0.0001):
        return ['', '']

    intensivity_proc, dm = calculate_gauss_params(i1, di1)
    intensivity_gen = calculate_reley_param(i2)

    generator = GenerateRequest(ReleyGenerator(intensivity_gen), clients_number)
    processor = ProcessRequest(GaussGenerator(intensivity_proc, dm))

    model = Model([generator], [processor])
    result = model.event_mode()

    return [intensivity_gen / intensivity_proc, result]


if __name__ == '__main__':
    app.run_server(debug=False)
