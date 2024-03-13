import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from model import calculate_b, \
                  convert_factor_to_value, \
                  calculate_reley_param, \
                  calculate_gauss_params, \
                  GenerateRequest, ReleyGenerator, \
                  ProcessRequest, GaussGenerator, \
                  Model, get_row
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
from math import fabs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

columns_table = ['x0', 'x1', 'x2', 'x3', 'x1*x2', 'x1*x3', 'x2*x3',
                 'x1*x2*x3', 'Y', 'Yл', 'Yчн', '|Y-Yл|', '|Y-Yчн|']
array_x = []
for i in [1, -1]:
    for j in [1, -1]:
        for k in [1, -1]:
            array_x.append(get_row([i, j, k], 3))

df = pd.DataFrame(array_x, columns=columns_table)
df.reset_index()

count_experiments = 8
n_add = 0


app.layout = html.Div(id='main', children=[
    dbc.Row(
        [
            dbc.Col(children=html.H6("Интенсивность поступления"), width={"size": 2, "offset": 1}),
            dbc.Col(children=html.H6("Интенсивность обработки"), width={"size": 2}),
            dbc.Col(children=html.H6("Разброс интенсивности обработки"), width={"size": 2}),
            dbc.Col(children=html.H6("Количество заявок"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='clients', debounce=True, value=100, type='number'), width=2),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("Минимум"), width=1),
            dbc.Col(children=dcc.Input(id='rel_min', debounce=True, value=1, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='norm_min', debounce=True, value=15, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='norm_d_min', debounce=True, value=5, type='text'), width={"size": 2}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("Максимум"), width=1),
            dbc.Col(children=dcc.Input(id='rel_max', debounce=True, value=10, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='norm_max', debounce=True, value=25, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='norm_d_max', debounce=True, value=10, type='text'), width={"size": 2}),
            dbc.Col(children=html.Button('Построить', id='table', n_clicks=0))
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("X1"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x1_new', debounce=True, value=0, type='text'), width={"size": 2}),
            dbc.Col(children=html.H6("X2"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x2_new', debounce=True, value=0, type='text'), width={"size": 2}),
            dbc.Col(children=html.H6("X3"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x3_new', debounce=True, value=0, type='text'), width={"size": 2}),
            dbc.Col(children=html.Button('Добавить точку', id='add_point', n_clicks=0))
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=
            dash_table.DataTable(
                id='table_exp',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records')), width={"size": 10, "offset": 1})
        ], style={"padding": "3px"}
    ),
    html.H3('Линейная модель: '),
    html.Span(id='line', children=''),
    html.H3('Частично-нелинейная модель'),
    html.Span(id='no_line', children=''),
])


@app.callback(
    [Output('table_exp', 'columns'), Output('table_exp', 'data'),
     Output('line', 'children'), Output('no_line', 'children')],
    [Input('table', 'n_clicks'), Input('add_point', 'n_clicks')],
    [State('clients', 'value'), State('rel_min', 'value'), State('rel_max', 'value'),
     State('norm_min', 'value'), State('norm_max', 'value'),
     State('norm_d_min', 'value'), State('norm_d_max', 'value'),
     State('x1_new', 'value'), State('x2_new', 'value'),
     State('x3_new', 'value')])
def graphic(table_clicks, add_clicks, clients_number, rel_min, rel_max,
            norm_min, norm_max, norm_d_min, norm_d_max, x1_new, x2_new, x3_new):
    global df, n_add

    if (add_clicks > n_add):
        n_add = add_clicks
        x1_new = float(x1_new)
        x2_new = float(x2_new)
        x3_new = float(x3_new)
        array_x.append(get_row([x1_new, x2_new, x3_new], 3))

    rel_min = float(rel_min)
    rel_max = float(rel_max)
    norm_min = float(norm_min)
    norm_max = float(norm_max)
    norm_d_min = float(norm_d_min)
    norm_d_max = float(norm_d_max)

    i = 0
    for row in array_x:
        rel = convert_factor_to_value(float(rel_min), float(rel_max), row[1])
        norm = convert_factor_to_value(float(norm_min), float(norm_max), row[2])
        norm_d = convert_factor_to_value(float(norm_d_min), float(norm_d_max), row[3])

        c_rel = calculate_reley_param(rel)
        c_norm, c_norm_d = calculate_gauss_params(norm, norm_d)

        generator = GenerateRequest(ReleyGenerator(c_rel), clients_number)
        processor = ProcessRequest(GaussGenerator(c_norm, c_norm_d))

        model = Model([generator], [processor])
        result = model.event_mode()
        array_x[i][8] = round(result, 5)
        i += 1

    b0 = calculate_b(0, 1, [array_x[i][0] for i in range(count_experiments)],
                     [array_x[i][8] for i in range(count_experiments)],
                     count_experiments)

    b1 = calculate_b(rel_min, rel_max,
                     [array_x[i][1] for i in range(count_experiments)],
                     [array_x[i][8] for i in range(count_experiments)],
                     count_experiments)

    b2 = calculate_b(norm_min, norm_max,
                     [array_x[i][2] for i in range(count_experiments)],
                     [array_x[i][8] for i in range(count_experiments)],
                     count_experiments)

    b3 = calculate_b(norm_d_min, norm_d_max,
                     [array_x[i][3] for i in range(count_experiments)],
                     [array_x[i][8] for i in range(count_experiments)],
                     count_experiments)

    b12 = calculate_b(rel_min * norm_min, rel_max * norm_max,
                      [array_x[i][4] for i in range(count_experiments)],
                      [array_x[i][8] for i in range(count_experiments)],
                      count_experiments)

    b13 = calculate_b(rel_min * norm_d_min, rel_max * norm_d_max,
                      [array_x[i][5] for i in range(count_experiments)],
                      [array_x[i][8] for i in range(count_experiments)],
                      count_experiments)

    b23 = calculate_b(norm_d_min * norm_min, norm_d_max * norm_max,
                      [array_x[i][6] for i in range(count_experiments)],
                      [array_x[i][8] for i in range(count_experiments)],
                      count_experiments)

    b123 = calculate_b(rel_min * norm_d_min * norm_min,
                       rel_max * norm_d_max * norm_max,
                       [array_x[i][7] for i in range(count_experiments)],
                       [array_x[i][8] for i in range(count_experiments)],
                       count_experiments)

    line = f"y={round(b0, 5)}+({round(b1, 5)})*x1+({round(b2, 5)})*x2+({round(b3, 5)})*x3"
    no_line = f"y={round(b0, 5)}+({round(b1, 5)})*x1+({round(b2, 5)})*x2+({round(b3, 5)})*x3+ \
                  ({round(b12, 5)})*x1*x2+({round(b13, 5)})*x1*x3+({round(b23, 5)})*x2*x3+({round(b123, 5)})*x1*x2*x3"

    i = 0
    for row in array_x:
        x1 = array_x[i][1]
        x2 = array_x[i][2]
        x3 = array_x[i][3]
        array_x[i][9] = round(fabs(b0 + b1 * x1 + b2 * x2 + b3 * x3), 5)
        array_x[i][11] = round(fabs(array_x[i][9] - array_x[i][8]), 5)
        array_x[i][10] = round(fabs(b0 + b1 * x1 + b2 * x2 + b3 * x3 + b12 * x1 * x2 + b23 * x2 * x3 + b13 * x1 * x3 + b123 * x1 * x2 * x3), 5)
        array_x[i][12] = round(fabs(array_x[i][10] - array_x[i][8]), 5)
        i += 1
    df = pd.DataFrame(array_x, columns=columns_table)

    return [[{"name": i, "id": i} for i in df.columns], df.to_dict('records'), line, no_line]


if __name__ == '__main__':
    app.run_server(debug=False)
