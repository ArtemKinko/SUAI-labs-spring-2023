import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


def upload_matrix(data_file_name, task_file_name, significance_file_name):
    with open(data_file_name) as data_file:
        with open(significance_file_name) as significance_file:
            with open(task_file_name) as task_file:
                task_num = int(task_file.readline())
                print("Загружаем данные для варианта №", task_num, "...")
                data = [[], []]
                ready_data = [[], []]
                for _ in range(task_num):
                    data[0] = data_file.readline().rsplit()
                    data[1] = data_file.readline().rsplit()
                ready_data[0] = [[float(data[0][i][:-1].replace(',', '.')),
                                  float(data[0][i + 1].replace(',', '.'))] for i in range(0, len(data[0]), 2)]
                ready_data[1] = [float(x.replace(',', '.')) for x in data[1]]
                signif = float(significance_file.readline().rsplit()[0])
                for _ in range(task_num % 2):
                    signif = float(significance_file.readline().rsplit()[0])
                return ready_data, signif


def get_probabilities(counters):
    sum_num = sum(counters)
    print("Общее количество экспериментов:", sum_num)
    return [x / sum_num for x in counters]


def show_hist(intervals, probabs):
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot()
    for i in range(len(probabs)):
        difference = intervals[i][1] - intervals[i][0]
        medium = intervals[i][0] + difference / 2
        ax.bar(medium, probabs[i], difference, facecolor="#0288D1")
    ax.grid()


def get_first_moment(intervals, probabilities):
    return sum([(intervals[i][0] + (intervals[i][1] - intervals[i][0]) / 2) * probabilities[i]
                for i in range(len(probabilities))])


def get_second_moment(intervals, probabilities):
    return sum([(intervals[i][0] + (intervals[i][1] - intervals[i][0]) / 2) ** 2 * probabilities[i]
                for i in range(len(probabilities))])


def get_dispersion(intervals, probabilities):
    first_moment = get_first_moment(intervals, probabilities)
    second_moment = get_second_moment(intervals, probabilities)
    return second_moment - first_moment ** 2


def get_probability_normal_interval_edges(intervals, average, deviation):
    edges = []
    probabilities = []
    for interval in intervals:
        for i in range(2):
            if interval[i] not in edges:
                edges.append(interval[i])
                probabilities.append(round(1 / deviation / math.sqrt(2 * math.pi) *
                                     math.e ** (-1 / 2 * ((interval[i] - average) / deviation) ** 2), 3))
    return edges, probabilities


def show_normal_graph(edges, probabilities, average, deviation):
    x = np.array(edges)
    y = np.array(probabilities)
    plt.scatter(x, y, color="black", label="Плотность распределения (границы)")

    x_acc = np.linspace(edges[0], edges[-1], 1000)
    y_acc = 1 / deviation / math.sqrt(2 * math.pi) * math.e ** (-1 / 2 * ((x_acc - average) / deviation) ** 2)
    plt.plot(x_acc, y_acc, color="red", label="Плотность распределения (точная)")
    plt.legend()

    plt.show()


def normal_probability(x, average, deviation):
    return 1 / deviation / math.sqrt(2 * math.pi) * math.e ** (-1 / 2 * ((x - average) / deviation) ** 2)


def get_theoretical_probabilities(intervals, average, deviation):
    probabilities = []
    for interval in intervals:
        probabilities.append(round(integrate.quad(normal_probability, interval[0], interval[1],
                                                  args=(average, deviation))[0], 3))
    return probabilities


def get_quad_difference_theoretical_empirical(theoretical, empirical):
    return [(theoretical[i] - empirical[i]) ** 2 for i in range(len(empirical))]


def get_u_parts(num_experiments, theoretical, empirical):
    difference = get_quad_difference_theoretical_empirical(theoretical, empirical)
    return [num_experiments * difference[i] / theoretical[i] for i in range(len(empirical))]


def get_u_function(f, significance, u_function_file):
    with open(u_function_file) as u_file:
        u_function = ["", ""]
        for _ in range(f):
            u_function = u_file.readline().rsplit()
        if significance == 0.025:
            return float(u_function[0].replace(",", "."))
        else:
            return float(u_function[1].replace(",", "."))


def solve_task():
    data_matrix, significance = upload_matrix("data.txt", "task.txt", "significance.txt")
    print("Загруженные интервалы:", data_matrix[0])
    print("Соответствующие количества попаданий:", data_matrix[1])
    probabilities = get_probabilities(data_matrix[1])
    print("Соответствующие частоты:", probabilities)
    show_hist(data_matrix[0], probabilities)
    print("\n\n---- Поиск теоретической плотности нормального распределения ----")
    first_moment = get_first_moment(data_matrix[0], probabilities)
    print("Оценка математического ожидания:", first_moment)
    second_moment = get_second_moment(data_matrix[0], probabilities)
    print("Второй начальный момент:", second_moment)
    dispersion = get_dispersion(data_matrix[0], probabilities)
    print("Оценка дисперсии:", dispersion)
    deviation = math.sqrt(dispersion)
    print("Соответственно, параметры нормального распределения: m =", first_moment, "; sigma =", deviation)
    normal_edges, normal_probabilities = get_probability_normal_interval_edges(data_matrix[0], first_moment, deviation)
    print("Границы интервалов:", normal_edges)
    print("Соответствующие значения плотности распределения нормального закона:", normal_probabilities)
    print("\n\n---- Проверка гипотезы о нормальном распределении ----")
    print("Интервалы:", data_matrix[0])
    theoretical_probabilities = get_theoretical_probabilities(data_matrix[0], first_moment, deviation)
    print(theoretical_probabilities)
    print("Эмпирические вероятности:", probabilities)
    print("Теоретические вероятности:", theoretical_probabilities)
    quad_difference_theoretical_empirical = get_quad_difference_theoretical_empirical(theoretical_probabilities,
                                                                                      probabilities)
    print("Квадраты разностей:", quad_difference_theoretical_empirical)
    u_parts = get_u_parts(sum(data_matrix[1]), theoretical_probabilities, probabilities)
    print("Слагаемые показателя согласованности:", u_parts)
    u = sum(u_parts)
    print("Значение показателя согласованности гипотезы:", u)
    print("Уровень значимости:", significance)
    u_real = get_u_function(len(probabilities) - 3, significance, "u_function.txt")
    print("Соответствующая  критическая граница:", u_real)
    if u <= u_real:
        print("Так как значение согласованности гипотезы меньше или равно критической границе, соответствующей"
              "заданному уровню значимости, гипотеза о нормальном распредлении случайной величины принимается")
    else:
        print("Так как значение согласованности гипотезы больше критической границы, соответствующей"
              "заданному уровню значимости, гипотеза о нормальном распределении случайной величины отвергается")

    show_normal_graph(normal_edges, normal_probabilities, first_moment, deviation)


solve_task()
