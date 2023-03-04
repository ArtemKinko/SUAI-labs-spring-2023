import math


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
            return ready_data, task_num


def find_t_from_table(table_file_name, x):
    with open(table_file_name) as l_table_file:
        line = [-1, -1]
        while line[0] != x:
            line = [float(param.replace(',', '.')) for param in l_table_file.readline().rsplit()]
        return line[1]


def get_expected_value(x_matrix):
    return sum(x_matrix) / len(x_matrix)


def get_expectation_dispersion(x_matrix):
    exp_estimate = get_expected_value(x_matrix)
    summary = 0
    for x in x_matrix:
        summary += (x - exp_estimate) ** 2
    return summary / (len(x_matrix) - 1)


def get_u_value(x_matrix, y_matrix):
    m_x = get_expected_value(x_matrix)
    m_y = get_expected_value(y_matrix)
    d_x = get_expectation_dispersion(x_matrix)
    d_y = get_expectation_dispersion(y_matrix)

    return (m_x - m_y) / math.sqrt(d_x / len(x_matrix) + d_y / len(y_matrix))


def upload_alpha(alpha_file_name):
    with open(alpha_file_name) as alpha_file:
        return float(alpha_file.readline())


def solve_task():
    data, task = upload_matrix("data.txt", "task.txt")
    print("Массив данных X:", data[0])
    print("Массив данных Y:", data[1])
    exp_values = [get_expected_value(data[0]), get_expected_value(data[1])]
    print("Оценка математического ожидания массива X:", exp_values[0])
    print("Оценка математического ожидания массива Y:", exp_values[1])
    print("---- Проверка гипотез ----")
    print("Пусть нулевая гипотеза - математические ожидания случайных величин равны")
    print("Конкурирующая гипотеза - мат. ожидание с.в. X больше мат. ожидания с.в. Y")
    u_value = get_u_value(data[0], data[1])
    print("Вычисленный показатель согласованности гипотезы u:", u_value)
    alpha = upload_alpha("alpha.txt")
    print("Уровень значимости:", alpha)
    t_function = find_t_from_table("t_function.txt", 1 - 2 * alpha)
    print("Критическая точка:", t_function)
    if u_value > t_function:
        print("Так как u > u_alpha, гипотеза H_0 отвергается,"
              "принимается гипотеза H_1 - мат. ожидание с.в. X больше мат. ожидания с.в. Y")
    else:
        print("Так как u <= u_alpha, гипотеза H_0 принимается - математические ожидания случайных величин равны")


solve_task()
