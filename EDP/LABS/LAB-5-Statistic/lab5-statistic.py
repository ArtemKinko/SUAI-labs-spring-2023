import math
import numpy as np


def upload_matrix(data_file_name, task_file_name):
    with open(data_file_name) as data_file:
        with open(task_file_name) as task_file:
            task_num = int(task_file.readline())
            print("Загружаем данные для варианта №", task_num, "...")
            data = [[], [], []]
            ready_data = [[], [], []]
            for _ in range(task_num):
                data[0] = data_file.readline().rsplit()
                data[1] = data_file.readline().rsplit()
                data[2] = data_file.readline().rsplit()
            ready_data[0] = [float(x.replace(',', '.')) for x in data[0]]
            ready_data[1] = [float(x.replace(',', '.')) for x in data[1]]
            ready_data[2] = [float(x.replace(',', '.')) for x in data[2]]
            return ready_data


def get_f_function(f_function_file_name, f1, f2):
    with open(f_function_file_name) as f_function_file:
        line = ""
        for _ in range(f2):
            line = f_function_file.readline().rsplit()
        return float(line[f1 - 1].replace(",", "."))


def get_t_function(t_function_file_name, f):
    with open(t_function_file_name) as t_function_file:
        line = ""
        for _ in range(f):
            line = t_function_file.readline().rsplit()
        return float(line[0].replace(",", "."))


def get_average(x_matrix):
    return round(sum(x_matrix) / len(x_matrix), 3)


def get_centered_data(data_matrix, average_matrix):
    return [[round(data_matrix[0][i] - average_matrix[0], 3) for i in range(len(data_matrix[0]))],
            [round(data_matrix[1][i] - average_matrix[1], 3) for i in range(len(data_matrix[1]))],
            data_matrix[2]]


def get_xt_matrix(data, significance):
    x_array = []
    if significance[0]:
        x_array.append([1, 1, 1, 1, 1, 1])
    if significance[1]:
        x_array.append(data[0])
    if significance[2]:
        x_array.append(data[1])
    return np.matrix(x_array)


def get_xtx_matrix(data, significance):
    x_matrix = get_xt_matrix(data, significance)
    return x_matrix.dot(x_matrix.transpose()).round(2)


def get_inverted_matrix(matrix):
    return np.linalg.inv(matrix).round(4)


def get_xty_matrix(data, significance):
    x_matrix = get_xt_matrix(data, significance)
    y_matrix = np.matrix(data[2]).transpose()
    return x_matrix.dot(y_matrix).round(3)


def get_b_matrix(xtx_matrix, xty_matrix):
    return xtx_matrix.dot(xty_matrix)


def get_y_from_equation(x1, x2, coefs, significance):
    return coefs[0] * int(significance[0]) + coefs[1] * int(significance[1]) * x1 + coefs[2] * int(significance[2]) * x2


def get_dispersion_table(data, coefs, significance):
    y_average = get_average(data[2])

    return [data[0],
            data[1],
            data[2],
            [round(y - y_average, 3) for y in data[2]],
            [round((y - y_average) ** 2, 3) for y in data[2]],
            [round(get_y_from_equation(data[0][i], data[1][i], coefs, significance), 3) for i in
             range(len(data[0]))],
            [round(data[2][i] - get_y_from_equation(data[0][i], data[1][i], coefs, significance), 3) for i in
             range(len(data[0]))],
            [round((data[2][i] - get_y_from_equation(data[0][i], data[1][i], coefs, significance)) ** 2, 3) for i
             in range(len(data[0]))]]


def get_deviation_average(sum_average, denominator):
    return sum_average / denominator


def get_deviation_theo(sum_theo, denominator):
    return sum_theo / denominator


def find_coefs(data, significance):
    print("\nНайдем функцию регрессии в виде алгебраического полинома: y = " + ("b0" if significance[0] else "")
          + (" + b1 * x1" if significance[1] else "") + (" + b2 * x2" if significance[2] else ""))
    x1_average = get_average(data[0])
    x2_average = get_average(data[1])
    if significance[1]:
        print("Среднее значение фактора x1:", x1_average)
    if significance[2]:
        print("Среднее значение фактора x2:", x2_average)
    data = get_centered_data(data, [x1_average, x2_average])
    print("Производим центрирование данных:")
    if significance[1]:
        print("Массив x1*:", data[0])
    if significance[2]:
        print("Массив x2*:", data[1])
    print("Массив y:", data[2])
    print("Для вычисления оценок коэффициентов регрессии решим уравнение B ̃ = (Ẋ^T * Ẋ)^(-1) (Ẋ^T * Y)")
    print("\nМатрица (Ẋ^T * Ẋ):")
    xtx_matrix = get_xtx_matrix(data, significance)
    print(xtx_matrix)
    inv_xtx_matrix = get_inverted_matrix(xtx_matrix)
    print("\nОбратная для этой матрица:")
    print(inv_xtx_matrix)
    print("\nМатрица (Ẋ^T * Y):")
    xty_matrix = get_xty_matrix(data, significance)
    print(xty_matrix)
    b_matrix = get_b_matrix(inv_xtx_matrix, xty_matrix)
    print("\nОценка вектора коэффициентов регрессии:")
    print(b_matrix)
    corrected_b_matrix = []

    j = 0
    titles = ["+", "ẋ1 + ", "ẋ2"]
    print("\nПолучаем уравнение: ", end="")
    for i in range(len(significance)):
        if significance[i]:
            corrected_b_matrix.append(b_matrix.item(j))
            print(round(b_matrix.item(j), 3), titles[i], end=" ")
            j += 1
        else:
            corrected_b_matrix.append(0)
    print("")

    print("\n---- Проверка адекватности уравнения")
    print("Составляем расчетную таблицу:")
    dispersion_table = get_dispersion_table(data, corrected_b_matrix, significance)
    titles = ["x1_i", "x2_i", "y_i", "y_i - y^-", "(y_i - y^-)^2", "y~_i", "y_i - y~_i", "(y_i - y~_i)^2"]
    sum_average_dispersion = sum(dispersion_table[4])
    sum_theo_dispersion = sum(dispersion_table[7])
    for i in range(len(titles)):
        print(titles[i], dispersion_table[i], ("- сумма:" + str(sum_average_dispersion) if i == 4 else ""),
              ("- сумма:" + str(sum_theo_dispersion) if i == 7 else ""))
    f2 = 5 - (sum([(int(significance[i])) if i == 0 else 0 for i in range(len(significance))]))
    deviation = get_deviation_average(sum_average_dispersion, 5)
    deviation1 = get_deviation_theo(sum_theo_dispersion, f2)
    significance_value = deviation / deviation1
    print("Оценка отклонения sigma^2:", deviation)
    print("Оценка отклонения sigma1^2:", deviation1)
    print("Значение показателя согласованности:", significance_value)
    f_function = get_f_function("f_function.txt", 5, f2)
    print("Критическое значение показателя согласованности:", f_function)
    if significance_value > f_function:
        print("Так как значение показателя согласованности больше значения показателя F, "
              "нулевая гипотеза об адекватности функции регрессии, принимается")
    else:
        print("Так как значение показателя согласованности меньше значения показателя F, "
              "нулевая гипотеза об адекватности функции регрессии, принимается")

    print("\n---- Селекция факторов")
    diag_matrix = [inv_xtx_matrix.item(i, i) for i in range(len(inv_xtx_matrix))]
    diag_matrix = [deviation1 * x for x in diag_matrix]
    print("Элементы главной диагонали корреляционной матрицы:", diag_matrix)
    sigmas = [math.sqrt(x) for x in diag_matrix]
    print("Оценки средних квадратичных отклонений:", sigmas)
    t_function_a = [abs(b_matrix[i][0]) / sigmas[i] for i in range(len(sigmas))]
    print("Соответствующие показатели согласованности:", t_function_a)
    t_function = get_t_function("t_function.txt", 3)
    print("Критическое значение показателя согласованности при уровне значимости alpha=0,05 степени свободы f = 3:",
          t_function)

    new_significance = []
    titles = ["ẋ0", "ẋ1", "ẋ2"]
    j = 0
    for i in range(3):
        if not significance[i]:
            new_significance.append(False)
        else:
            new_significance.append(t_function_a[j] > t_function)
            if t_function_a[j] > t_function:
                print("Фактор", titles[i], "является значимым")
            else:
                print("Фактор", titles[i], "является не значимым")
            j += 1

    print("\n---- Пересчет регрессионного выражения")
    if new_significance.count(False) == 0 or new_significance == significance:
        print("Все факторы значимы, пересчет не требуется")
        return
    else:
        if new_significance.count(True) == 0:
            print("Все коэффициенты не значимы. Пересчет невозможен")
            return
        print("Пересчет")
        find_coefs(data, new_significance)


def solve_task():
    data = upload_matrix("data.txt", "task.txt")
    print("Массив x1:", data[0])
    print("Массив x2:", data[1])
    print("Массив y:", data[2])
    significance = [True, True, True]
    find_coefs(data, significance)


solve_task()
