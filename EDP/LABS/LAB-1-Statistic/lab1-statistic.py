import math

def upload_matrix(matrix_file_name, prob_file_name, var_file_name):
    with open(matrix_file_name) as matrix_file:
        with open(var_file_name) as var_file:
            with open(prob_file_name) as prob_file:
                task_num = int(var_file.readline())
                print("Загружаем данные для варианта №", task_num, "...")
                var_matrix = ""
                prob_matrix = ""
                for _ in range(task_num):
                    var_matrix = matrix_file.readline()
                    prob_matrix = prob_file.readline()
                var_matrix = var_matrix.rsplit()
                prob_matrix = prob_matrix.rsplit()
                return [float(x.replace(',', '.')) for x in var_matrix], float(prob_matrix[0].replace(',', '.')), \
                       float(prob_matrix[1].replace(',', '.'))


def get_expectation_estimate(x_matrix):
    return sum(x_matrix) / len(x_matrix)


def get_expectation_dispersion(x_matrix):
    exp_estimate = get_expectation_estimate(x_matrix)
    summary = 0
    for x in x_matrix:
        summary += (x - exp_estimate) ** 2
    return summary / (len(x_matrix) - 1)


def get_expectation_deviation(x_matrix):
    return math.sqrt(get_expectation_dispersion(x_matrix))


def get_sigma_interval(x_matrix):
    exp_estimate = get_expectation_estimate(x_matrix)
    exp_deviation = get_expectation_deviation(x_matrix)
    return [exp_estimate - 2 * exp_deviation, exp_estimate + 2 * exp_deviation]


def correct_matrix(x_matrix):
    interval = get_sigma_interval(x_matrix)
    return [x for x in x_matrix if interval[0] <= x <= interval[1]]


def find_f_from_table(table_file_name, x):
    with open(table_file_name) as f_table_file:
        print("Значение x для функции Лапласа:", x)
        prev_line = [-1, -1]
        next_line = [-1, -1]
        while x >= next_line[0]:
            prev_line = next_line
            next_line = [float(x.replace(',', '.')) for x in f_table_file.readline().rsplit()]
        if prev_line[0] == x:
            print("Значение функции Лапласа найдено в таблице, оно равно:", prev_line[1])
            return prev_line[1]
        else:
            print("Значение функции Лапласа лежит в диапазоне между", prev_line[1], "и", next_line[1])
            f_function_num = ((x - next_line[0]) / (prev_line[0] - next_line[0])) * prev_line[1] +\
                       ((x - prev_line[0]) / (next_line[0] - prev_line[0])) * next_line[1]
            print("Используем линейную интерполяцию и получаем значение функции Лапласа:", f_function_num)
            return f_function_num


def get_x_for_f_function(exp_epsilon, len_matrix, exp_deviation):
    return exp_epsilon * math.sqrt(len_matrix) / exp_deviation


def get_probability_for_estimate(f_function_number):
    return 2 * f_function_number


def get_estimate_interval(cor_estimate, max_deviation):
    return [cor_estimate - max_deviation, cor_estimate + max_deviation]


def find_l_from_table(table_file_name, x):
    with open(table_file_name) as l_table_file:
        line = [-1, -1]
        while line[0] != x:
            line = [float(param.replace(',', '.')) for param in l_table_file.readline().rsplit()]
        return line[1]


def get_epsilon_from_l_function(deviation, len_matrix, l_function):
    return deviation / math.sqrt(len_matrix) * l_function


def solve_task():
    matrix, beta, epsilon = upload_matrix("data.txt", "probability.txt", "task.txt")
    print("Полученный массив данных:", matrix)
    print("Заданная доверительная вероятность:", beta)
    print("Максимальная вероятная погрешность:", epsilon)
    print('\n\n---------- Получаем оценки характеристик ----------')
    print("Оценка математического ожидания:", get_expectation_estimate(matrix))
    print("Оценка дисперсии:", get_expectation_dispersion(matrix))
    print("Оценка среднего квадратического отклонения:", get_expectation_deviation(matrix))
    print("Полученный двухсигмовый интервал:", get_sigma_interval(matrix))
    corrected_matrix = correct_matrix(matrix)
    print("Вышедшие за интервал элементы:", list(set(matrix).symmetric_difference(set(corrected_matrix))))
    print('\n\n---------- Получаем скорректированные оценки характеристик ----------')
    print("Откорректированный массив данных:", corrected_matrix)

    corrected_estimate = get_expectation_estimate(corrected_matrix)
    corrected_dispersion = get_expectation_dispersion(corrected_matrix)
    corrected_deviation = get_expectation_deviation(corrected_matrix)

    print("Откорректированная оценка математического ожидания:", corrected_estimate)
    print("Откорректированная оценка дисперсии:", corrected_dispersion)
    print("Откорректированая оценка среднего квадратического отклонения:", corrected_deviation)
    print('\n\n---------- Качество оценивания математического ожидания по заданной максимальной вероятной погрешности'
          '----------')
    f_fun_num = find_f_from_table('f_function.txt', get_x_for_f_function(epsilon, len(corrected_matrix),
                                                                         corrected_deviation))
    estimate_interval = get_estimate_interval(corrected_estimate, epsilon)
    print("Получаем доверительный интервал, соответствующий максимальной погрешности eB =", epsilon, ":",
          estimate_interval)
    print("Так, математическое ожидание случайной величины, из которой извлечена исследуемая выборка,"
          " находится в интервале", estimate_interval, "с вероятностью не менее чем",
          get_probability_for_estimate(f_fun_num))

    print('\n\n---------- Качество оценивания математического ожидания по заданной доверительной вероятности'
          '----------')
    print('Доверительная вероятность равна:', beta)
    l_function_num = find_l_from_table('l_function.txt', beta)
    print('Значение функции Стьюдента для заданной вероятности:', l_function_num)
    epsilon = get_epsilon_from_l_function(corrected_deviation, len(corrected_matrix), l_function_num)
    print('Максимальная вероятная погрешность:', epsilon)
    interval = get_estimate_interval(corrected_estimate, epsilon)
    print('Доверительный интервал, соответствующий максимальной вероятной погрешности:',
          interval)
    print('Так, математическое ожидание случайной величины, из которой извлечена исследуемая выборка,'
          'находится с доверительной вероятностью не менее, чем', beta, ' в интервале', interval)


solve_task()
