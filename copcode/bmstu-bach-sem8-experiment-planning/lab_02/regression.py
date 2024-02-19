def get_coeffs(matrix, results, coeff_num):
    coeffs = []
    for i in range(coeff_num):
        c = 0
        for j in range(len(results)):
            c += matrix[j][i] * results[j]
        coeffs.append(c / len(results))
    return coeffs

def build_equation(coeffs, x_s):
    eq = "{:.2f}".format(coeffs[0])
    for i in range(1, len(coeffs)):
        if coeffs[i] >= 0:
            eq += " + {:.2f}{:s}".format(coeffs[i], x_s[i - 1])
        else:
            eq += " - {:.2f}{:s}".format(abs(coeffs[i]), x_s[i - 1])
    return eq

def get_result(coeffs, x_s, args):
    res = coeffs[0]
    for i in range(1, len(coeffs)):
        additive = coeffs[i]
        x = x_s[i - 1]

        while x != "":
            if x[0] == 'x':
                x = x[1:]
            else:
                additive *= args[int(x[0]) - 1]
                x = x[1:]

        res += additive
    return res

def get_matrix(num_exp, results):
    matrix = []
    for i in range(num_exp):
        matrix.append([1])
    
    for i in range(num_exp):
        if i % 2 == 1:
            matrix[i].append(1)
        else:
            matrix[i].append(-1)

        if i % 4 >= 2:
            matrix[i].append(1)
        else:
            matrix[i].append(-1)

        if i % 8 >= 4:
            matrix[i].append(1)
        else:
            matrix[i].append(-1)
        
        matrix[i].append(matrix[i][1] * matrix[i][2])
        matrix[i].append(matrix[i][1] * matrix[i][3])
        matrix[i].append(matrix[i][2] * matrix[i][3])
        matrix[i].append(matrix[i][1] * matrix[i][2] * matrix[i][3])

        matrix[i].append(results[i])

    lin_coeffs = get_coeffs(matrix, results, 4)
    # lin_coeffs = get_coeffs(matrix, results, 3)
    nonlin_coeffs = get_coeffs(matrix, results, 8)
    # nonlin_coeffs = get_coeffs(matrix, results, 4)

    # print(build_equation(lin_coeffs, ['x1', 'x2', 'x3']))
    # print(build_norm_equation(lin_coeffs, ['x1', 'x2']))
    # print(build_equation(nonlin_coeffs, ['x1', 'x2', 'x3', 'x1x2', 'x1x3', 'x2x3', 'x1x2x3']))
    # print(build_norm_equation(nonlin_coeffs, ['x1', 'x2', 'x1x2']))

    for i in range(num_exp):
        matrix[i].append(get_result(lin_coeffs, ['x1', 'x2', 'x3'], matrix[i][1:4]))
        matrix[i].append(get_result(nonlin_coeffs, ['x1', 'x2', 'x3', 'x1x2', 'x1x3', 'x2x3', 'x1x2x3'], matrix[i][1:4]))
        matrix[i].append(abs(matrix[i][9] - matrix[i][8]))
        matrix[i].append(abs(matrix[i][10] - matrix[i][8]))
        # matrix[i].append(get_result(lin_coeffs, ['x1', 'x2'], matrix[i][1:3]))
        # matrix[i].append(get_result(nonlin_coeffs, ['x1', 'x2', 'x1x2'], matrix[i][1:3]))
        # matrix[i].append(abs(matrix[i][5] - matrix[i][4]))
        # matrix[i].append(abs(matrix[i][6] - matrix[i][4]))
        # print(matrix[i])
    return matrix, lin_coeffs, nonlin_coeffs

def get_natural_coeffs(coeffs, x_mins, x_maxs, linear=True):
    if linear:
        nat_coeffs = [coeffs[0]]
        for i in range(1, len(coeffs)):
            nat_coeffs.append(2 * coeffs[i] / (x_maxs[i - 1] - x_mins[i - 1]))
            nat_coeffs[0] -= coeffs[i] * (x_mins[i - 1] + x_maxs[i - 1]) / (x_maxs[i - 1] - x_mins[i - 1])
        return nat_coeffs
    
    centers = [(x_mins[i] + x_maxs[i]) / 2 for i in range(len(x_mins))]
    centers.insert(0, 0)
    deltas = [(x_maxs[i] - x_mins[i]) / 2 for i in range(len(x_mins))]
    deltas.insert(0, 0)
    ratios = [centers[i] / deltas[i] for i in range(1, len(centers))]
    ratios.insert(0, 0)
    
    nat_coeffs = [
        coeffs[0] - sum([coeffs[i] * ratios[i] for i in range(len(centers))])
                    + coeffs[4] * ratios[1] * ratios[2] + coeffs[5] * ratios[1] * ratios[3] 
                    + coeffs[6] * ratios[2] * ratios[3] - coeffs[7] * ratios[1] * ratios[2] * ratios[3],
        (coeffs[1] - coeffs[4] * ratios[2] - coeffs[5] * ratios[3] + coeffs[7] * ratios[2] * ratios[3]) / deltas[1],
        (coeffs[2] - coeffs[4] * ratios[1] - coeffs[6] * ratios[3] + coeffs[7] * ratios[1] * ratios[3]) / deltas[2],
        (coeffs[3] - coeffs[5] * ratios[1] - coeffs[6] * ratios[2] + coeffs[7] * ratios[1] * ratios[2]) / deltas[3],
        (coeffs[4] - coeffs[7] * centers[3] / deltas[3]) / deltas[1] / deltas[2],
        (coeffs[5] - coeffs[7] * centers[2] / deltas[2]) / deltas[1] / deltas[3],
        (coeffs[6] - coeffs[7] * centers[1] / deltas[1]) / deltas[2] / deltas[3],
        coeffs[7] / deltas[1] / deltas[2] / deltas[3]
    ]
    return nat_coeffs

# matrix, lin_coeffs, nonlin_coeffs = get_matrix(4, [6, 3, 4, 7])
# print(get_result(lin_coeffs, ['x1', 'x2'], [0, 0]))
# print(get_result(nonlin_coeffs, ['x1', 'x2', 'x1x2'], [0, 0]))

# get_matrix(4, [45, 40, 35, 32])