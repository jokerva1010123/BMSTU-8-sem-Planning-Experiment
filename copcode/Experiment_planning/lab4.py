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
                  Model, get_row, get_row_with_s, calculate_b_ockp
import dash_bootstrap_components as dbc
import pandas as pd
import modeller
import dash_table
from math import fabs, sqrt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

columns_table = ['N', 'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6',
                 'x1*x2', 'x1*x3', 'x1*x4', 'x1*x5', 'x1*x6',
                 'x2*x3', 'x2*x4', 'x2*x5', 'x2*x6',
                 'x3*x4', 'x3*x5', 'x3*x6',
                 'x4*x5', 'x4*x6',
                 'x5*x6',
                 'x1*x2*x3', 'x1*x2*x4', 'x1*x2*x5', 'x1*x2*x6',
                 'x1*x3*x4', 'x1*x3*x5', 'x1*x3*x6',
                 'x1*x4*x5', 'x1*x4*x6',
                 'x1*x5*x6',
                 'x2*x3*x4', 'x2*x3*x5', 'x2*x3*x6',
                 'x2*x4*x5', 'x2*x4*x6',
                 'x2*x5*x6',
                 'x3*x4*x5', 'x3*x4*x6',
                 'x3*x5*x6',
                 'x4*x5*x6',
                 'x1*x2*x3*x4', 'x1*x2*x3*x5', 'x1*x2*x3*x6',
                 'x1*x2*x4*x5', 'x1*x2*x4*x6',
                 'x1*x2*x5*x6',
                 'x1*x3*x4*x5', 'x1*x3*x4*x6',
                 'x1*x3*x5*x6',
                 'x1*x4*x5*x6',
                 'x2*x3*x4*x5', 'x2*x3*x4*x6',
                 'x2*x3*x5*x6',
                 'x2*x4*x5*x6',
                 'x3*x4*x5*x6',
                 'x1*x2*x3*x4*x5', 'x1*x2*x3*x4*x6',
                 'x1*x2*x3*x5*x6',
                 'x1*x2*x4*x5*x6',
                 'x1*x3*x4*x5*x6',
                 'x2*x3*x4*x5*x6',
                 'x1*x2*x3*x4*x5*x6',
                 'x1^2 - S', 'x2^2 - S', 'x3^2 - S', 'x4^2 - S', 'x5^2 - S', 'x6^2 - S',
                 'Y', 'Yн', '|Y-Yн|']

count_experiments = 64
count = count_experiments + 2 * 6 + 1
s = sqrt(count_experiments / count)
alpha = sqrt((s * count - count_experiments) / 2)
array_x = []
experim = 0
for i in [1, -1]:
    for j in [1, -1]:
        for k in [1, -1]:
            for l in [1, -1]:
                for m in [1, -1]:
                    for n in [1, -1]:
                        experim += 1
                        array_x.append([experim] + get_row_with_s(i, j, k, l, m, n, s))

array_x.append([experim + 1] + get_row_with_s(alpha, 0, 0, 0, 0, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(-alpha, 0, 0, 0, 0, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, alpha, 0, 0, 0, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, -alpha, 0, 0, 0, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, alpha, 0, 0, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, -alpha, 0, 0, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, 0, alpha, 0, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, 0, -alpha, 0, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, 0, 0, alpha, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, 0, 0, -alpha, 0, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, 0, 0, 0, alpha, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, 0, 0, 0, -alpha, s))
experim += 1
array_x.append([experim + 1] + get_row_with_s(0, 0, 0, 0, 0, 0, s))
experim += 1

tmax = 300
df = pd.DataFrame(array_x, columns=columns_table)
df.reset_index()

n_add = 0


app.layout = html.Div(id='main', children=[
    dbc.Row(
        [
            dbc.Col(children=html.H6("Интенсивность поступления 1"), width={"size": 2, "offset": 1}),
            dbc.Col(children=html.H6("Интенсивность поступления 2"), width={"size": 2}),
            dbc.Col(children=html.H6("Интенсивность обработки тип 1"), width={"size": 2}),
            dbc.Col(children=html.H6("Разброс интенсивности обработки тип 1"), width={"size": 2}),
            dbc.Col(children=html.H6("Количество заявок"), width={"size": 1}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("Минимум"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='rel_min1', debounce=True, value=1, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='rel_min2', debounce=True, value=1, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='norm_min1', debounce=True, value=17, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='norm_d_min1', debounce=True, value=5, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='clients', debounce=True, value=100, type='number'), width=2),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("Максимум"), width=1),
            dbc.Col(children=dcc.Input(id='rel_max1', debounce=True, value=10, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='rel_max2', debounce=True, value=10, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='norm_max1', debounce=True, value=20, type='text'), width={"size": 2}),
            dbc.Col(children=dcc.Input(id='norm_d_max1', debounce=True, value=10, type='text'), width={"size": 2})
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("Интенсивность обработки тип 2"), width={"size": 2,  "offset": 5}),
            dbc.Col(children=html.H6("Разброс интенсивности обработки тип 2"), width={"size": 2}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("Минимум"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='norm_min2', debounce=True, value=17, type='text'), width={"size": 2,  "offset": 4}),
            dbc.Col(children=dcc.Input(id='norm_d_min2', debounce=True, value=5, type='text'), width={"size": 2}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("Максимум"), width=1),
            dbc.Col(children=dcc.Input(id='norm_max2', debounce=True, value=20, type='text'), width={"size": 2,  "offset": 4}),
            dbc.Col(children=dcc.Input(id='norm_d_max2', debounce=True, value=10, type='text'), width={"size": 2}),
            dbc.Col(children=html.Button('Построить', id='table', n_clicks=0))
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("X1"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x1_new', debounce=True, value=0, type='text'), width={"size": 2}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("X2"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x2_new', debounce=True, value=0, type='text'), width={"size": 2}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("X3"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x3_new', debounce=True, value=0, type='text'), width={"size": 2}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("X4"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x4_new', debounce=True, value=0, type='text'), width={"size": 2}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("X5"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x5_new', debounce=True, value=0, type='text'), width={"size": 2}),
        ], style={"padding": "3px"}
    ),
    dbc.Row(
        [
            dbc.Col(children=html.H6("X6"), width={"size": 1}),
            dbc.Col(children=dcc.Input(id='x6_new', debounce=True, value=0, type='text'), width={"size": 2}),
            dbc.Col(children=html.Button('Добавить точку', id='add_point', n_clicks=0))
        ], style={"padding": "3px"}
    ),

    html.H3('ОЦКП'),
    dbc.Row(
        [
            dbc.Col(children=
            dash_table.DataTable(
                id='table_exp',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records')), width={"size": 10, "offset": 1})
        ], style={"padding": "3px"}
    ),

    html.H3('Частично-нелинейная модель'),
    html.Span(id='no_line', children=''),
])


@app.callback(
    [Output('table_exp', 'columns'), Output('table_exp', 'data'),
     Output('no_line', 'children')],
    [Input('table', 'n_clicks'), Input('add_point', 'n_clicks')],
    [State('clients', 'value'), State('rel_min1', 'value'), State('rel_max1', 'value'),
     State('rel_min2', 'value'), State('rel_max2', 'value'),
     State('norm_min1', 'value'), State('norm_max1', 'value'),
     State('norm_d_min1', 'value'), State('norm_d_max1', 'value'),
     State('norm_min2', 'value'), State('norm_max2', 'value'),
     State('norm_d_min2', 'value'), State('norm_d_max2', 'value'),
     State('x1_new', 'value'), State('x2_new', 'value'),
     State('x3_new', 'value'), State('x4_new', 'value'),
     State('x5_new', 'value'), State('x6_new', 'value')])
def graphic(table_clicks, add_clicks, clients_number, rel_min1, rel_max1,
            rel_min2, rel_max2, norm_min1, norm_max1,
            norm_d_min1, norm_d_max1, norm_min2, norm_max2,
            norm_d_min2, norm_d_max2, x1_new, x2_new, x3_new, x4_new, x5_new, x6_new):
    global df, n_add, experim

    for i in range(experim):
        array_x[i] = array_x[i][1:]

    if (add_clicks > n_add):
        n_add = add_clicks
        x1_new = float(x1_new)
        x2_new = float(x2_new)
        x3_new = float(x3_new)
        x4_new = float(x4_new)
        x5_new = float(x4_new)
        x6_new = float(x4_new)
        experim += 1
        array_x.append(get_row([x1_new, x2_new, x3_new, x4_new, x5_new, x6_new], 6))

    f1_b = float(rel_min1)
    f1_e = float(rel_max1)
    f2_b = float(rel_min2)
    f2_e = float(rel_max2)
    f3_b = float(norm_min1)
    f3_e = float(norm_max1)
    f4_b = float(norm_d_min1)
    f4_e = float(norm_d_max1)
    f5_b = float(norm_min2)
    f5_e = float(norm_max2)
    f6_b = float(norm_d_min2)
    f6_e = float(norm_d_max2)

    r = True if 2 * (f1_b + f1_e + f2_b + f2_e) / (f3_b + f3_e + f5_b + f5_e) > 0.8 else False

    i = 0
    for row in array_x:
        rel1 = convert_factor_to_value(float(rel_min1), float(rel_max1), row[1])
        rel2 = convert_factor_to_value(float(rel_min2), float(rel_max2), row[2])
        norm1 = convert_factor_to_value(float(norm_min1), float(norm_max1), row[3])
        norm_d1 = convert_factor_to_value(float(norm_d_min1), float(norm_d_max1), row[4])
        norm2 = convert_factor_to_value(float(norm_min2), float(norm_max2), row[5])
        norm_d2 = convert_factor_to_value(float(norm_d_min2), float(norm_d_max2), row[6])

        c_rel1 = calculate_reley_param(rel1)
        c_rel2 = calculate_reley_param(rel2)
        c_norm1, c_norm_d1 = calculate_gauss_params(norm1, norm_d1)
        c_norm2, c_norm_d2 = calculate_gauss_params(norm2, norm_d2)

        model = modeller.Model([c_rel1, c_rel2], [c_norm1, c_norm2], [c_norm_d1, c_norm_d2], 2, 1, 0)

        avg_queue_size, avg_queue_time, processed_requests = model.time_based_modellingg(tmax, 0.001)
        print(i)
        array_x[i][70] = round(avg_queue_time, 5)
        i += 1

    b0 = calculate_b_ockp(0, 1,
                   [array_x[i][0] for i in range(count)],
                   [array_x[i][70] for i in range(count)],
                   count)

    b1 = calculate_b_ockp(f1_b, f1_e,
                   [array_x[i][1] for i in range(count)],
                   [array_x[i][70] for i in range(count)],
                   count)

    b2 = calculate_b_ockp(f2_b, f2_e,
                   [array_x[i][2] for i in range(count)],
                   [array_x[i][70] for i in range(count)],
                   count)

    b3 = calculate_b_ockp(f3_b, f3_e,
                   [array_x[i][3] for i in range(count)],
                   [array_x[i][70] for i in range(count)],
                   count)

    b4 = calculate_b_ockp(f4_b, f4_e,
                   [array_x[i][4] for i in range(count)],
                   [array_x[i][70] for i in range(count)],
                   count)

    b5 = calculate_b_ockp(f5_b, f5_e,
                   [array_x[i][5] for i in range(count)],
                   [array_x[i][70] for i in range(count)],
                   count)

    b6 = calculate_b_ockp(f6_b, f6_e,
                   [array_x[i][6] for i in range(count)],
                   [array_x[i][70] for i in range(count)],
                   count)

    b12 = calculate_b_ockp(f1_b * f2_b, f1_e * f2_e,
                    [array_x[i][7] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b13 = calculate_b_ockp(f1_b * f3_b, f1_e * f3_e,
                    [array_x[i][8] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b14 = calculate_b_ockp(f1_b * f4_b, f1_e * f4_e,
                    [array_x[i][9] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b15 = calculate_b_ockp(f1_b * f5_b, f1_e * f5_e,
                    [array_x[i][10] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b16 = calculate_b_ockp(f1_b * f6_b, f1_e * f6_e,
                    [array_x[i][11] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b23 = calculate_b(f2_b * f3_b, f2_e * f3_e,
                    [array_x[i][12] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b24 = calculate_b_ockp(f2_b * f4_b, f2_e * f4_e,
                    [array_x[i][13] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b25 = calculate_b_ockp(f2_b * f5_b, f2_e * f5_e,
                    [array_x[i][14] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b26 = calculate_b_ockp(f2_b * f6_b, f2_e * f6_e,
                    [array_x[i][15] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b34 = calculate_b_ockp(f3_b * f4_b, f3_e * f4_e,
                    [array_x[i][16] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b35 = calculate_b_ockp(f3_b * f5_b, f3_e * f5_e,
                    [array_x[i][17] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b36 = calculate_b_ockp(f3_b * f6_b, f3_e * f6_e,
                    [array_x[i][18] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b45 = calculate_b_ockp(f4_b * f5_b, f4_e * f5_e,
                    [array_x[i][19] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b46 = calculate_b_ockp(f4_b * f6_b, f4_e * f6_e,
                    [array_x[i][20] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b56 = calculate_b_ockp(f5_b * f6_b, f5_e * f6_e,
                    [array_x[i][21] for i in range(count)],
                    [array_x[i][70] for i in range(count)],
                    count)

    b123 = calculate_b_ockp(f1_b * f2_b * f3_b, f1_e * f2_e * f3_e,
                     [array_x[i][22] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b124 = calculate_b_ockp(f1_b * f2_b * f4_b, f1_e * f2_e * f4_e,
                     [array_x[i][23] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b125 = calculate_b_ockp(f1_b * f2_b * f5_b, f1_e * f2_e * f5_e,
                     [array_x[i][24] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b126 = calculate_b_ockp(f1_b * f2_b * f6_b, f1_e * f2_e * f6_e,
                     [array_x[i][25] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b134 = calculate_b_ockp(f1_b * f3_b * f4_b, f1_e * f3_e * f4_e,
                     [array_x[i][26] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b135 = calculate_b_ockp(f1_b * f3_b * f5_b, f1_e * f3_e * f5_e,
                     [array_x[i][27] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b136 = calculate_b_ockp(f1_b * f3_b * f6_b, f1_e * f3_e * f6_e,
                     [array_x[i][28] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b145 = calculate_b_ockp(f1_b * f4_b * f5_b, f1_e * f4_e * f5_e,
                     [array_x[i][29] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b146 = calculate_b_ockp(f1_b * f4_b * f6_b, f1_e * f4_e * f6_e,
                     [array_x[i][30] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b156 = calculate_b_ockp(f1_b * f5_b * f6_b, f1_e * f5_e * f6_e,
                     [array_x[i][31] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b234 = calculate_b_ockp(f2_b * f3_b * f4_b, f2_e * f3_e * f4_e,
                     [array_x[i][32] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b235 = calculate_b_ockp(f2_b * f3_b * f5_b, f2_e * f3_e * f5_e,
                     [array_x[i][33] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b236 = calculate_b_ockp(f2_b * f3_b * f6_b, f2_e * f3_e * f6_e,
                     [array_x[i][34] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b245 = calculate_b_ockp(f2_b * f4_b * f5_b, f2_e * f4_e * f5_e,
                     [array_x[i][35] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b246 = calculate_b_ockp(f2_b * f4_b * f6_b, f2_e * f4_e * f6_e,
                     [array_x[i][36] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b256 = calculate_b_ockp(f2_b * f5_b * f6_b, f2_e * f5_e * f6_e,
                     [array_x[i][37] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b345 = calculate_b_ockp(f3_b * f4_b * f5_b, f3_e * f4_e * f5_e,
                     [array_x[i][38] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b346 = calculate_b_ockp(f3_b * f4_b * f6_b, f3_e * f4_e * f6_e,
                     [array_x[i][39] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b356 = calculate_b_ockp(f3_b * f5_b * f6_b, f3_e * f5_e * f6_e,
                     [array_x[i][40] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b456 = calculate_b_ockp(f4_b * f5_b * f6_b, f4_e * f5_e * f6_e,
                     [array_x[i][41] for i in range(count)],
                     [array_x[i][70] for i in range(count)],
                     count)

    b1234 = calculate_b_ockp(f1_b * f2_b * f3_b * f4_b, f1_e * f2_e * f3_e * f4_e,
                      [array_x[i][42] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1235 = calculate_b_ockp(f1_b * f2_b * f3_b * f5_b, f1_e * f2_e * f3_e * f5_e,
                      [array_x[i][43] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1236 = calculate_b_ockp(f1_b * f2_b * f3_b * f6_b, f1_e * f2_e * f3_e * f6_e,
                      [array_x[i][44] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1245 = calculate_b_ockp(f1_b * f2_b * f4_b * f5_b, f1_e * f2_e * f4_e * f5_e,
                      [array_x[i][45] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1246 = calculate_b_ockp(f1_b * f2_b * f4_b * f6_b, f1_e * f2_e * f4_e * f6_e,
                      [array_x[i][46] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1256 = calculate_b_ockp(f1_b * f2_b * f5_b * f6_b, f1_e * f2_e * f5_e * f6_e,
                      [array_x[i][47] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1345 = calculate_b_ockp(f1_b * f3_b * f4_b * f5_b, f1_e * f3_e * f4_e * f5_e,
                      [array_x[i][48] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1346 = calculate_b_ockp(f1_b * f3_b * f4_b * f6_b, f1_e * f3_e * f4_e * f6_e,
                      [array_x[i][49] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1356 = calculate_b_ockp(f1_b * f3_b * f5_b * f6_b, f1_e * f3_e * f5_e * f6_e,
                      [array_x[i][50] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b1456 = calculate_b_ockp(f1_b * f4_b * f5_b * f6_b, f1_e * f4_e * f5_e * f6_e,
                      [array_x[i][51] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b2345 = calculate_b_ockp(f2_b * f3_b * f4_b * f5_b, f2_e * f3_e * f4_e * f5_e,
                      [array_x[i][52] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b2346 = calculate_b_ockp(f2_b * f3_b * f4_b * f6_b, f2_e * f3_e * f4_e * f6_e,
                      [array_x[i][53] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b2356 = calculate_b_ockp(f2_b * f3_b * f5_b * f6_b, f2_e * f3_e * f5_e * f6_e,
                      [array_x[i][54] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b2456 = calculate_b_ockp(f2_b * f4_b * f5_b * f6_b, f2_e * f4_e * f5_e * f6_e,
                      [array_x[i][55] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b3456 = calculate_b_ockp(f3_b * f4_b * f5_b * f6_b, f3_e * f4_e * f5_e * f6_e,
                      [array_x[i][56] for i in range(count)],
                      [array_x[i][70] for i in range(count)],
                      count)

    b12345 = calculate_b_ockp(f1_b * f2_b * f3_b * f4_b * f5_b, f1_e * f2_e * f3_e * f4_e * f5_e,
                       [array_x[i][57] for i in range(count)],
                       [array_x[i][70] for i in range(count)],
                       count)

    b12346 = calculate_b_ockp(f1_b * f2_b * f3_b * f4_b * f6_b, f1_e * f2_e * f3_e * f4_e * f6_e,
                       [array_x[i][58] for i in range(count)],
                       [array_x[i][70] for i in range(count)],
                       count)

    b12356 = calculate_b_ockp(f1_b * f2_b * f3_b * f5_b * f6_b, f1_e * f2_e * f3_e * f5_e * f6_e,
                       [array_x[i][59] for i in range(count)],
                       [array_x[i][70] for i in range(count)],
                       count)

    b12456 = calculate_b_ockp(f1_b * f2_b * f4_b * f5_b * f6_b, f1_e * f2_e * f4_e * f5_e * f6_e,
                       [array_x[i][60] for i in range(count)],
                       [array_x[i][70] for i in range(count)],
                       count)

    b13456 = calculate_b_ockp(f1_b * f3_b * f4_b * f5_b * f6_b, f1_e * f3_e * f4_e * f5_e * f6_e,
                       [array_x[i][61] for i in range(count)],
                       [array_x[i][70] for i in range(count)],
                       count)

    b23456 = calculate_b_ockp(f2_b * f3_b * f4_b * f5_b * f6_b, f2_e * f3_e * f4_e * f5_e * f6_e,
                       [array_x[i][62] for i in range(count)],
                       [array_x[i][70] for i in range(count)],
                       count)

    b123456 = calculate_b_ockp(f1_b * f2_b * f3_b * f4_b * f5_b * f6_b, f1_e * f2_e * f3_e * f4_e * f5_e * f6_e,
                        [array_x[i][63] for i in range(count)],
                        [array_x[i][70] for i in range(count)],
                        count)

    b11 = calculate_b_ockp(0, 1,
                        [array_x[i][64] for i in range(count)],
                        [array_x[i][70] for i in range(count)],
                        count)


    b22 = calculate_b_ockp(0, 1,
                        [array_x[i][65] for i in range(count)],
                        [array_x[i][70] for i in range(count)],
                        count)

    b33 = calculate_b_ockp(0, 1,
                        [array_x[i][66] for i in range(count)],
                        [array_x[i][70] for i in range(count)],
                        count)

    b44 = calculate_b_ockp(0, 1,
                        [array_x[i][67] for i in range(count)],
                        [array_x[i][70] for i in range(count)],
                        count)

    b55 = calculate_b_ockp(0, 1,
                        [array_x[i][68] for i in range(count)],
                        [array_x[i][70] for i in range(count)],
                        count)

    b66 = calculate_b_ockp(0, 1,
                        [array_x[i][69] for i in range(count)],
                        [array_x[i][70] for i in range(count)],
                        count)

    b0 = b0 - (b11+b22+b33+b44+b55+b66) * s
    no_line = f"y={round(b0, 5)}+({round(b1, 5)})*x1+({round(b2, 5)})*x2+({round(b3, 5)})*x3+({round(b4, 5)})*x4+({round(b5, 5)})*x5+({round(b6, 5)})*x6+\
                  ({round(b12, 5)})*x1*x2+({round(b13, 5)})*x1*x3+({round(b14, 5)})*x1*x4+({round(b15, 5)})*x1*x5+({round(b16, 5)})*x1*x6+\
                  ({round(b23, 5)})*x2*x3+({round(b24, 5)})*x2*x4+({round(b25, 5)})*x2*x5+({round(b26, 5)})*x2*x6+\
                  ({round(b34, 5)})*x3*x4+({round(b35, 5)})*x3*x5+({round(b36, 5)})*x3*x6+\
                  ({round(b45, 5)})*x4*x5+({round(b46, 5)})*x4*x6+\
                  ({round(b56, 5)})*x5*x6+\
                  ({round(b123, 5)})*x1*x2*x3+({round(b124, 5)})*x1*x2*x4+({round(b125, 5)})*x1*x2*x5+({round(b126, 5)})*x1*x2*x6+\
                  ({round(b134, 5)})*x1*x3*x4+({round(b135, 5)})*x1*x3*x5+({round(b136, 5)})*x1*x3*x6+\
                  ({round(b145, 5)})*x1*x4*x5+({round(b146, 5)})*x1*x4*x6+\
                  ({round(b156, 5)})*x1*x5*x6+\
                  ({round(b234, 5)})*x2*x3*x4+({round(b235, 5)})*x2*x3*x5+({round(b236, 5)})*x2*x3*x6+\
                  ({round(b245, 5)})*x2*x4*x5+({round(b246, 5)})*x2*x4*x6+\
                  ({round(b256, 5)})*x2*x5*x6+\
                  ({round(b345, 5)})*x3*x4*x5+({round(b346, 5)})*x3*x4*x6+\
                  ({round(b356, 5)})*x3*x5*x6+\
                  ({round(b456, 5)})*x4*x5*x6+\
                  ({round(b1234, 5)})*x1*x2*x3*x4+({round(b1235, 5)})*x1*x2*x3*x5+({round(b1236, 5)})*x1*x2*x3*x6+\
                  ({round(b1245, 5)})*x1*x2*x4*x5+({round(b1246, 5)})*x1*x2*x4*x6+\
                  ({round(b1256, 5)})*x1*x2*x5*x6+\
                  ({round(b1345, 5)})*x1*x3*x4*x5+({round(b1346, 5)})*x1*x3*x4*x6+\
                  ({round(b1356, 5)})*x1*x3*x5*x6+\
                  ({round(b1456, 5)})*x1*x4*x5*x6+\
                  ({round(b2345, 5)})*x2*x3*x4*x5+({round(b2346, 5)})*x2*x3*x4*x6+\
                  ({round(b2356, 5)})*x2*x3*x5*x6+\
                  ({round(b2456, 5)})*x2*x4*x5*x6+\
                  ({round(b3456, 5)})*x3*x4*x5*x6+\
                  ({round(b12345, 5)})*x1*x2*x3*x4*x5+({round(b12346, 5)})*x1*x2*x3*x4*x6+\
                  ({round(b12356, 5)})*x1*x2*x3*x5*x6+\
                  ({round(b12456, 5)})*x1*x2*x4*x5*x6+\
                  ({round(b13456, 5)})*x1*x3*x4*x5*x6+\
                  ({round(b23456, 5)})*x2*x3*x4*x5*x6+\
                  ({round(b123456, 5)})*x1*x2*x3*x4*x5*x6+\
                  ({round(b11 if b11 > 0 else -b11, 5)})*(x1^2-s)+\
                  ({round(b22 if b22 > 0 else -b22, 5)})*(x2^2-s)+\
                  ({round(b33 if not r else (-b33 if b33 > 0 else b33), 5)})*(x3^2-s)+\
                  ({round(b44, 5)})*(x4^2-s)+\
                  ({round(b55 if not r else (-b55 if b55 > 0 else b55), 5)})*(x5^2-s)+\
                  ({round(b66, 5)})*(x6^2-s)"

    i = 0
    for row in array_x:
        x1 = array_x[i][1]
        x2 = array_x[i][2]
        x3 = array_x[i][3]
        x4 = array_x[i][4]
        x5 = array_x[i][5]
        x6 = array_x[i][6]
        array_x[i][71] = round(fabs(b0 + b1 * x1 + b2 * x2 + b3 * x3 + b4 * x4 + b5 * x5 + b6 * x6 + \
                                    b12 * x1 * x2 + b13 * x1 * x3 + b14 * x1 * x4 + b15 * x1 * x5 + b16 * x1 * x6 + \
                                    b23 * x2 * x3 + b24 * x2 * x4 + b25 * x2 * x5 + b26 * x2 * x6+\
                                    b34 * x3 * x4 + b35 * x3 * x5 + b36 * x3 * x6 + \
                                    b45 * x4 * x5 + b46 * x4 * x6 + \
                                    b56 * x5 * x6 + \
                                    b123 * x1 * x2 * x3 + b124 * x1 * x2 * x4 + b125 * x1 * x2 * x5+ b126 * x1 * x2 * x6 + \
                                    b134 * x1 * x3 * x4 + b135 * x1 * x3 * x5 + b136 * x1 * x3 * x6 + \
                                    b145 * x1 * x4 * x5 + b146 * x1 * x4 * x6 + \
                                    b156 * x1 * x5 * x6 + \
                                    b234 * x2 * x3 * x4 + b235 * x2 * x3 * x5 + b236 * x2 * x3 * x6 + \
                                    b245 * x2 * x4 * x5 + b246 * x2 * x4 * x6 + \
                                    b256 * x2 * x5 * x6 + \
                                    b345 * x3 * x4 * x5 + b346 * x3 * x4 * x6 + \
                                    b356 * x3 * x5 * x6 + \
                                    b456 * x4 * x5 * x6 + \
                                    b1234 * x1 * x2 * x3 * x4 + b1235 * x1 * x2 * x3 * x5 + b1236 * x1 * x2 * x3 * x6+\
                                    b1245 * x1 * x2 * x4 * x5 + b1246 * x1 * x2 * x4 * x6 + \
                                    b1256 * x1 * x2 * x5 * x6 + \
                                    b1345 * x1 * x3 * x4 * x5 + b1346 * x1 * x3 * x4 * x6 + \
                                    b1356 * x1 * x3 * x5 * x6 + \
                                    b1456 * x1 * x4 * x5 * x6 + \
                                    b2345 * x2 * x3 * x4 * x5 + b2346 * x2 * x3 * x4 * x6 + \
                                    b2356 * x2 * x3 * x5 * x6 + \
                                    b2456 * x2 * x4 * x5 * x6 + \
                                    b3456 * x3 * x4 * x5 * x6 + \
                                    b12345 * x1 * x2 * x3 * x4 * x5 + b12346 * x1 * x2 * x3 * x4 * x6 + \
                                    b12356 * x1 * x2 * x3 * x5 * x6 + \
                                    b12456 * x1 * x2 * x4 * x5 * x6 + \
                                    b13456 * x1 * x3 * x4 * x5 * x6 + \
                                    b23456 * x2 * x3 * x4 * x5 * x6 + \
                                    b123456 * x1 * x2 * x3 * x4 * x5 * x6 + \
                                    b11 * (x1*x1 - s) + \
                                    b22 * (x2*x2 - s) + \
                                    b33 * (x3*x3 - s) + \
                                    b44 * (x4*x4 - s) + \
                                    b55 * (x5*x5 - s) + \
                                    b66 * (x6*x6 - s)), 5)
        array_x[i][72] = round(fabs(array_x[i][70] - array_x[i][71]), 5)
        i += 1

    for i in range(experim):
        array_x[i] = [i+1] + array_x[i]
    df = pd.DataFrame(array_x, columns=columns_table)

    return [[{"name": i, "id": i} for i in df.columns], df.to_dict('records'), no_line]


if __name__ == '__main__':
    app.run_server(debug=False)
