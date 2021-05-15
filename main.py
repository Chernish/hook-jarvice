# Импортируем необходимые библиотеки и зависимости
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

# Дефолтные параметры
b = np.array([-8, 8]).T

# Тестовая модель
def three_hump_camel(x):
    f = 2 * x[0] ** 2 - 1.05 * x[0] ** 4 + x[0] ** 6 / 6 + x[0] * x[1] + x[1] ** 2
    return f

# Метод Хука-Джарвиса
def hooke_jeeves(function, x0, d, d_min):
    n = x0.size
    e = np.eye(n) * d
    x = x0
    fx = function(x)
    num_iterations = 0
    result_step_iterations = []

    while e[1, 1] > d_min:
        current_position = x
        for i in range(0, n):
            z = current_position + e[:, i]
            y = function(z)
            num_iterations += 1
            if y < fx:
                current_position = z
                fx = y
                if num_iterations % 10 == 0:
                    step_iterations = [x]
                    # result_step_iterations.append(step_iterations)
            else:
                z = current_position - e[:, i]
                y = function(z)
                num_iterations += 1
                if y < fx:
                    current_position = z
                    fx = y
                if num_iterations % 10 == 0:
                    step_iterations = [x]
                    # result_step_iterations.append(step_iterations)

        if np.all(current_position == x):
            e = e * 0.5

        else:
            x1 = current_position + (current_position - x)
            f1 = function(x1)
            num_iterations += 1
            x = current_position
            if num_iterations % 10 == 0:
                step_iterations = [x]
                # result_step_iterations.append(step_iterations)
            if f1 < fx:
                x = x1
                fx = f1
                for i in range(0, n):
                    z = x1 - e[:, i]
                    y = function(z)
                    num_iterations += 1
                    if y < f1:
                        x = z
                        fx = y
                    if num_iterations % 10 == 0:
                        step_iterations = [x]
                        # result_step_iterations.append(step_iterations)

    return x


# Функция для отрисовки полученных данных
def plot_function_3D(function, a, b, style, title):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    x = np.linspace(a, b, 30)
    y = x

    X, Y = np.meshgrid(x, y)
    Z = function([X, Y])

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=style, edgecolor="none")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    plt.show()





if __name__ == '__main__':
    # Делаем вызов функций
    # print(hooke_jeeves(three_hump_camel, b, 1, 0.0002))
    hooke_jeeves_result = hooke_jeeves(three_hump_camel, b, 1, 0.05)
    print(hooke_jeeves_result)
    # print(hooke_jeeves_result[0])
    plot_function_3D(three_hump_camel, hooke_jeeves_result[0], hooke_jeeves_result[1], "viridis", "Three Hump Camel")
