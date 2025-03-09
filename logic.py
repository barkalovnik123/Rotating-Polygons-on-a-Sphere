from math import cos, sin, sqrt  # импортируем необходимые функции из math


def rotate(vector, a=0, b=0, c=0):
    """Последовательно вращает векторы из массива vector вокруг осей OX(угол a), OY(угол b), OZ(угол c)"""
    new_vector = [None, None, None]
    # Изменение x-координаты
    new_vector[0] = vector[0] * cos(b) * cos(c) - vector[1] * sin(c) * cos(b) + vector[2] * sin(b)
    # Изменение y-координаты
    new_vector[1] = vector[0] * (sin(a) * sin(b) * cos(c) + sin(c) * cos(a))
    new_vector[1] += vector[1] * (-sin(a) * sin(b) * sin(c) + cos(a) * cos(c))
    new_vector[1] += vector[2] * -sin(a) * cos(b)
    # Изменение Z-координаты
    new_vector[2] = vector[0] * (sin(a) * sin(c) - sin(b) * cos(a) * cos(c))
    new_vector[2] += vector[1] * (sin(a) * cos(c) + sin(b) * sin(c) * cos(a))
    new_vector[2] += vector[2] * cos(a) * cos(b)
    # Возвращаем полученный вектор
    return new_vector


def find_dots(vectors, n=15):
    """возвращает массив из (n+1)*len(vectors) равноудалённых точек,
    принадлежащих отрезкам между данными точками"""
    new_dots = []
    # данное выражение помогает создать двумерный массив размера Nx2 вида [(0,1),(1,2)...(n-1,n),(n,0)]
    for i in [(k, k+1) if k < len(vectors)-1 else (k, 0) for k in range(len(vectors))]:
        for n in range(16):
            lm = n / (16-n)
            new_dots.append([
                (vectors[i[0]][j] + lm * vectors[i[1]][j]) / (lm + 1) for j in range(3)
            ])
    return new_dots


def projection_on_sphere(dot, r=1):
    """Возвращает вектор длины r, сонаправленный данному"""
    new_dot = dot.copy()
    k = r / sqrt(dot[0] ** 2 + dot[1] ** 2 + dot[2] ** 2)
    new_dot[0], new_dot[1], new_dot[2] = dot[0] * k, dot[1] * k, dot[2] * k
    return new_dot


def orthogonal_projection_on_surface(dot, A=0, B=0, C=1, D=2):
    """Возвращает проекцию на плоскость, заданную уравнением
    Ax+By+Cz+D=0, если не указаны коэффициенты, то на плоскость z=-2"""
    new_dot = dot.copy()
    t = (D + A * dot[0] + B * dot[1] + C * dot[2]) / (A * A + B * B + C * C)
    new_dot[0] += A * t
    new_dot[1] += B * t
    new_dot[2] += C * t
    return new_dot

def central_projection_on_surface(dot, center=[0, 0, 2], A=0, B=0, C=1, D=2):
    """Возвращает центральную проекцию на плоскость, заданную уравнением
        Ax+By+Cz+D=0, если не указаны коэффициенты, то на плоскость z=-2, считая
        центром точку center"""
    # Рассчитаем координаты направляющего вектора прямой для уравнения
    # (x-x0)/p=(y-y0)/q=(z-z0)/m
    p = center[0] - dot[0]
    q = center[1] - dot[1]
    m = center[2] - dot[2]
    # Объявим координаты точки, как x0, y0, z0
    x0, y0, z0 = dot
    # Из уравнения плоскости Ax+By+Cz+D=0, куда мы подставим правые части параметрических уравнений
    # x=x0+pt; y=y0+qt; z=z0+mt, найдём t = (-D-Cz0-By0-Ax0)/(Ap+Bq+Cm)
    t = (-D-C*z0-B*y0-A*x0)/(A*p+B*q+C*m)
    return [
        x0+p*t,
        y0+q*t,
        z0+m*t
    ]
