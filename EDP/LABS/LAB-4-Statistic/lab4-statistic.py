import math
import numpy as np


def upload_matrix(data_file_name, task_file_name):
    with open(data_file_name) as data_file:
        with open(task_file_name) as task_file:
            task_num = int(task_file.readline())
            print("Загружаем данные для варианта №", task_num, "...")
            data = [[], []]
            ready_data = [[], []]
            for _ in range(task_num):
                data[0] = data_file.readline().rsplit()
                data[1] = data_file.readline().rsplit()
            ready_data[0] = [float(x.replace(',', '.')) for x in data[0]]
            ready_data[1] = [float(x.replace(',', '.')) for x in data[1]]
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


def get_needed_matrix(raw_data):
    ready_data = [raw_data[0], raw_data[1], [x ** 2 for x in raw_data[0]], [x ** 3 for x in raw_data[0]],
                  [x ** 4 for x in raw_data[0]], [raw_data[0][i] * raw_data[1][i] for i in range(len(raw_data[0]))],
                  [raw_data[0][i] ** 2 * raw_data[1][i] for i in range(len(raw_data[0]))]]
    return ready_data, [sum(line) for line in ready_data]


def get_coefs(summaries):
    A = np.matrix([[summaries[4], summaries[3], summaries[2]],
                   [summaries[3], summaries[2], summaries[0]],
                   [summaries[2], summaries[0], 5]])
    det_A = int(np.linalg.det(A))
    print("\nМатрица A:")
    print(A)
    print("Определитель |A|:", det_A)

    A0 = np.matrix([[summaries[6], summaries[3], summaries[2]],
                   [summaries[5], summaries[2], summaries[0]],
                   [summaries[1], summaries[0], 5]])
    det_A0 = int(np.linalg.det(A0))
    a0 = round(det_A0 / det_A, 3)
    print("\nМатрица A0:")
    print(A0)
    print("Определитель |A0|:", det_A0)
    print("Коэффициент a0:", a0)

    A1 = np.matrix([[summaries[4], summaries[6], summaries[2]],
                   [summaries[3], summaries[5], summaries[0]],
                   [summaries[2], summaries[1], 5]])
    det_A1 = int(np.linalg.det(A1))
    a1 = round(det_A1 / det_A, 3)
    print("\nМатрица A1:")
    print(A1)
    print("Определитель |A1|:", det_A1)
    print("Коэффициент a1:", a1)

    A2 = np.matrix([[summaries[4], summaries[3], summaries[6]],
                   [summaries[3], summaries[2], summaries[5]],
                   [summaries[2], summaries[0], summaries[1]]])
    det_A2 = int(np.linalg.det(A2))
    a2 = round(det_A2 / det_A, 3)
    print("\nМатрица A2:")
    print(A2)
    print("Определитель |A2|:", det_A2)
    print("Коэффициент a2:", a2)

    return [a0, a1, a2], A


def get_table_dispersion(data, coefs):
    average_y = sum(data[1]) / len(data[1])
    diff_average = [y - average_y for y in data[1]]
    sqr_diff_average = [y ** 2 for y in diff_average]
    sum_sqr_diff_average = sum(sqr_diff_average)

    theoretical_y = [coefs[0] * x ** 2 + coefs[1] * x + coefs[3] for x in data[0]]
    diff_theo = [data[1][i] - theoretical_y[i] for i in range(len(theoretical_y))]
    sqr_diff_theo = [y ** 2 for y in diff_theo]
    sum_sqr_diff_theo = sum(sqr_diff_theo)


def get_f_y_matrix(data):
    left = np.matrix([data[2], data[0], [1, 1, 1, 1, 1]])
    right = np.matrix([[x] for x in data[1]])
    return left, right


def get_table_adequacy(data, theo_coefs, significances):
    y_average = sum(data[1]) / len(data[1])
    theo_y = [round(theo_coefs[0] * significances[0] * x ** 2 +
                    theo_coefs[1] * significances[1] * x +
                    theo_coefs[2] * significances[2], 3) for x in data[0]]
    return [data[0],
            data[1],
            [round(y - y_average, 3) for y in data[1]],
            [round((y - y_average) ** 2, 3) for y in data[1]],
            theo_y,
            [round(data[1][i] - theo_y[i], 3) for i in range(len(data[1]))],
            [round((data[1][i] - theo_y[i]) ** 2, 3) for i in range(len(data[1]))]]


def check_agreement(new_data, coefs, significance):
    print("\n\n---- Проверяем адекватность регрессионной зависимости экспериментальным данным")
    titles_adequacy = ["x_i\t\t\t\t", "y_i\t\t\t\t", "y_i - y^*\t\t", "(y_i - y^*)^2\t", "y~_i\t\t\t", "y_i - y~_i\t\t",
                       "(y_i - y~_i)^2\t"]
    table_adequacy = get_table_adequacy(new_data, coefs, significance)
    table_adequacy_sums = [sum(table_adequacy[3]), sum(table_adequacy[6])]
    print("Расчетная таблица:")
    for i in range(len(table_adequacy)):
        print(titles_adequacy[i], table_adequacy[i])
        if i == 3:
            print("Сумма квадратов разности значения y и оценки мат. ожидания - ", table_adequacy_sums[0])
        if i == 6:
            print("Сумма квадратов разности значения y и значений полученной функции - ", table_adequacy_sums[1])
    dispersion = table_adequacy_sums[0] / 4
    dispersion_1 = table_adequacy_sums[1] / 2
    print("Вычисляем оценку дисперсий sigma^2:", dispersion)
    print("Вычисляем оценку дисперсий sigma^2_1:", dispersion_1)
    agreement_coef = dispersion / dispersion_1
    print("Значение показателя согласованности:", agreement_coef)
    f_function = get_f_function("f_function.txt", 4, 2)
    print("Критическое значение показателя согласованности при уровне значимости alpha=0.01 и степенях свободы: f1 = 4,"
          "f2 = 2:", f_function)
    if agreement_coef > f_function:
        print("Так как показатель согласованности больше критической точки распределения Фишера,"
              "нулевая гипотеза H0 о соответствии функции регрессии экспериментальным данным принимается")
    else:
        print("Так как показатель согласованности меньше критической точки распределения Фишера,"
              "нулевая гипотеза H0 о соответствии функции регрессии экспериментальным данным отклоняется")
    return dispersion_1


def solve_task():
    data = upload_matrix("data.txt", "task.txt")
    print("Значения X:", data[0])
    print("Значения Y:", data[1])
    print("Необходимо построить уравнение регрессии y = f(x) в предположении,"
          "что оно является алгебраическим полиномом второй степени")
    print("Пусть y = a0 * f0(x) + a1 * f1(x) + a2 * f2(x), где \n"
          "f0(x) = x^2, f1(x) = x, f2(x) = 1")
    new_data, summary = get_needed_matrix(data)
    print("\n\n---- Расчетная таблица для скалярного расчета:")
    titles = ["x_i\t\t\t", "y_i\t\t\t", "x^2_i\t\t", "x^3_i\t\t", "x^4_i\t\t", "y_i * x_i\t", "y_i * x^2_i\t"]
    for i in range(len(new_data)):
        print(titles[i], new_data[i], "\t- сумма:", summary[i])
    coefs, a_matrix = get_coefs(summary)
    print(coefs)
    print("\nФункция, полученная с помощью скалярного расчета, принимает вид:")
    print(coefs[0], "* x^2 +", coefs[1], "* x +", coefs[2])

    print("\n---- Произведем расчеты в матричной форме")
    print("Решим уравнение A<3> = (F^T[3;5] F[5;3])^-1 F^T[3;5] Y<5>")
    print("\nВычисляем обратную матрицу для (F^T F)^-1 для матрицы:")
    print(a_matrix)
    print("\nОбратная матрица:")
    inv_a_matrix = np.linalg.inv(a_matrix)
    print(inv_a_matrix)
    print("Вычисляем матрицу в правой части уравнения - F^T_[5;3] Y<5>:")
    left_matrix, right_matrix = get_f_y_matrix(new_data)
    print("\nF^T_[5;3]:")
    print(left_matrix)
    print("\nY<5>:")
    print(right_matrix)
    print("\nПолученная правая часть уравнения:")
    total_matrix = left_matrix.dot(right_matrix)
    print(total_matrix)
    print("\nПолучим оценки коэффициенты регрессии путем перемножения обратной матрицы с полученной:")
    coefs_matrix = [round(float(x[0]), 3) for x in inv_a_matrix.dot(total_matrix)]
    print("\nФункция, полученная с помощью скалярного расчета, принимает вид:")
    print(coefs_matrix[0], "* x^2 +", coefs_matrix[1], "* x +", coefs_matrix[2])

    dispersion_1 = check_agreement(new_data, coefs, [1, 1, 1])

    print("\n\n---- Проверяем значимость коэффициентов регрессии.")
    diag_matrix = [inv_a_matrix.item(0, 0), inv_a_matrix.item(1, 1), inv_a_matrix.item(2, 2)]
    print("Элементы главной диагонали обратной матрицы:", diag_matrix)
    print("Перемножим sigma^2_1 на элементы диагонали и получим дисперсии коэффициентов регрессии:")
    diag_matrix = [dispersion_1 * x for x in diag_matrix]
    print(diag_matrix)
    sigmas_matrix = [math.sqrt(x) for x in diag_matrix]
    print("Соответствующие средние квадратичные отклонения:", sigmas_matrix)
    t_function_a = [abs(coefs[i]) / sigmas_matrix[i] for i in range(len(sigmas_matrix))]
    print("Находим наблюдаемые значения показателя:", t_function_a)
    t_function = get_t_function("t_function.txt", 2)
    print("Критическое значение показателя согласованности при уровне значимости alpha=0,01 степени свободы f = 2:",
          t_function)
    print("Сравниваем полученные показатели с критическим значением:\n")
    significance = [x > t_function for x in t_function_a]
    for i in range(len(significance)):
        print("Коэффициент a" + str(i) + " является", ("значимым" if significance[i] else "незначимым"))
    print("Исключая, незначимые коэффициенты получим уравнение:")
    print((str(coefs[0]) + " * x^2" if significance[0] == 1 else "") +
          (" + " + str(coefs[1]) + " * x" if significance[1] == 1 else "") +
          (" + " + str(coefs[2]) if significance[2] == 1 else ""))

    print("\n\n---- Повторно проверим адекватность для нового уравнения")
    check_agreement(new_data, coefs, significance)


solve_task()
