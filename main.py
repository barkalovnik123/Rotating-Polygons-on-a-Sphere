import arcade        # Импортируем модуль arcade для реализации 2D-графики
from logic import *  # Импортируем функции, связанные с математическими преобразованиями

# Устанавливаем константы

# Размер экрана
SCREEN_WIDTH = 600                          # Ширина окна
SCREEN_HEIGHT = 600                         # Высота окна
SCREEN_TITLE = "Sphere projection - rgr"    # Имя окна

timer = 0.0   # Глобальная переменная таймера, которая будет повышаться на 0.01 каждый шаг
# Запрашиваем у пользователя номер теста
number_of_test = int(input("Введите номер теста: "))


def process(vertices, angles):
    """Функция проводит ряд преобразований: поворот, разбиение, проектирование на поверхность
       сферы и центральную проекцию на плоскость. На вход принимает массив исходных вершин
       фигуры vertices и массив, состоящий из трёх углов поворота a, b и c вокруг осей
       Ox, Oy и Oz соответственно"""
    for dot in vertices:  # Перебираем все вершины фигуры, поворачиваем их
        dot[0], dot[1], dot[2] = rotate(dot, angles[0], angles[1], angles[2])

    # Объявляем новый массив, состоящий из вершин многоугольника и точек между ними
    vertices_gotten = find_dots(vertices)

    for dot in vertices_gotten:  # Проецируем каждую точку в новом массиве на сферу
        dot[0], dot[1], dot[2] = projection_on_sphere(dot)

    for dot in vertices_gotten:  # Поиск центральных проекций на плоскость z=-2
        dot[0], dot[1], dot[2] = central_projection_on_surface(dot)

    dots = vertices_gotten  # Для удобства объявляем новый массив, содержащий точки после всех преобразований

    for dot in vertices_gotten:  # В Arcade отрисовка идёт от левого нижнего края (I часть ПДСК)
        dot[0] *= 100            # Чтобы визуализировать более наглядно, увеличиваем координаты
        dot[0] += 300            # точек в 100 раз и центруем их, прибавляя 300
        dot[1] *= 100
        dot[1] += 300

    return vertices_gotten


def on_draw(delta_time):  # Функция, внутри которой производятся все преобразования фигур и их отрисовка
    global timer  # Добавляем глобальную переменную timer в область видимости on_draw

    timer += 0.01  # Увеличиваем значение таймера

    if number_of_test == 7:  # Данное условие реализует выбор номера теста, в каждом из которых
        vertices = [[0, 2, 2], [2, 2, 0], [0, 2, -2], [-2, 2, 0]]  # Объявляются массивы с вершинами фигур
        vertices2 = [[0, 2, 2], [sqrt(3), 2, -1], [-sqrt(3), 2, -1]]
        vertices3 = [[1, 1, 3], [-2, 1, 3], [-2, -1, 3]]
        dots1 = process(vertices, (timer, timer, 0))       # Проводятся их преобразование
        dots2 = process(vertices2, (timer, timer, timer))
        dots3 = process(vertices3, (timer, 5, 5))
        # Объявляется массив, содержащий все обрабатываемые фигуры
        figures = [dots1, dots2, dots3]
    elif number_of_test == 6:
        vertices = [[0, 2, 2], [2, 2, 0], [0, 2, -2], [-2, 2, 0]]     # Объявляются массивы с вершинами фигур
        vertices2 = [[0, 2, 2], [sqrt(3), 2, -1], [-sqrt(3), 2, -1]]
        dots1 = process(vertices, (timer, 0, 0))       # Проводятся их преобразование
        dots2 = process(vertices2, (timer, timer, timer))
        figures = [dots1, dots2]
    elif number_of_test == 5:
        # Объявляются массивы с вершинами фигур
        vertices = [[3, 6, -3], [4.5, 6, 0], [3, 6, 3], [-3, 6, 3], [-4.5, 6, 0], [-3, 6, -3]]
        dots = process(vertices, (timer, timer/2, 0))  # Проводятся их преобразование
        figures = [dots]
    elif number_of_test == 4:
        vertices = [[3, 0, 3], [-3, 0, 3], [-3, 0, 6], [3, 0, 6]]  # Объявляются массивы с вершинами фигур
        dots = process(vertices, (timer, 0, 0))  # Проводятся их преобразование
        figures = [dots]
    elif number_of_test == 3:
        vertices = [[2, 0, 2], [0, 2, 2], [-2, 0, 2], [0, -2, 2]]  # Объявляются массивы с вершинами фигур
        dots = process(vertices, (0, timer, 0))  # Проводятся их преобразование
        figures = [dots]
    elif number_of_test == 2:
        vertices = [[0, 2, 2], [sqrt(3), 2, -1], [-sqrt(3), 2, -1]]  # Объявляются массивы с вершинами фигур
        dots = process(vertices, (0, 0, timer))  # Проводятся их преобразование
        figures = [dots]
    elif number_of_test == 1:
        vertices = [[0, 2, 2], [2, 2, 0], [0, 2, -2], [-2, 2, 0]]  # Объявляются массивы с вершинами фигур
        dots = process(vertices, (timer, 0, 0))  # Проводятся их преобразование
        figures = [dots]

    k = 0   # Вспомогательная переменная k, хранящая то, какую сейчас фигуру мы отрисовываем
    arcade.start_render()
    arcade.draw_circle_filled(300, 300, 232, [255, 255, 255])
    for dots in figures:
        # Последовательный массив цветов фигур, 1 будет отрисована красным, 2 - зелёным, 3 - синим
        c = ([92, 0, 0], [1, 50, 32], [0, 33, 55])[k]
        k += 1
        l = len(dots)  # Для удобства объявляем переменную l - количество отрисовываемых точек
        # Начинаем рендер
        for i in range(l):  # Перебираем все точки в dots, рисуя линии от заданной до следующей
            arcade.draw_line(dots[i][0],    # Ниже с помощью тернарного оператора проверяем является ли точка
                             dots[i][1],    # последней в массиве - в таком случае соединяем её с первой
                             dots[i + 1][0] if i != l - 1 else dots[0][0],
                             dots[i + 1][1] if i != l - 1 else dots[0][1],
                             c,   # Цвет линии, заданный в RGB
                             2)             # Толщина линии


arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)  # Открываем окно
arcade.set_background_color([73, 66, 63])       # Устанавливаем тёмно-серый фон

# Вызываем команду отрисовки каждую 1/80 секунды
arcade.schedule(on_draw, 1/80)

# Запускаем программу
arcade.run()
