import random
from typing import Callable


class Vector:
    x: float = 0
    y: float = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({round(self.x, 4)}, {round(self.y, 4)})'

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        return Vector(x, y)

    def __rmul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x, y)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x, y)


def func_r(v: Vector) -> float:
    return (1 - v.x) ** 2 + 100 * ((v.y - v.x ** 2) ** 2)


def exploring(p0: Vector,
              h1: float,
              h2: float,
              func: Callable) -> Vector:
    if func(p0 + Vector(h1, 0)) < func(p0):
        p1 = p0 + Vector(h1, 0)
    elif func(p0 - Vector(h1, 0)) < func(p0):
        p1 = p0 - Vector(h1, 0)
    else:
        p1 = p0

    if func(p1 + Vector(0, h2)) < func(p1):
        p2 = p1 + Vector(0, h2)
    elif func(p1 - Vector(0, h2)) < func(p1):
        p2 = p1 - Vector(0, h2)
    else:
        p2 = p1

    return p2


def sample(x1: Vector,
           x2: Vector,
           gamma: float = 2) -> Vector:
    return x1 + gamma * (x2 - x1)


def hook_jeeves(func,
                point_0: Vector,
                h1: float = 1.0,
                h2: float = 1.0,
                h_min: float = 1e-10,
                alpha: float = 0.5,
                gamma: float = 2.0,
                iters: int = 5000,
                ) -> (Vector, int):

    global i

    point_exploring = point_0

    for i in range(iters):

        point_1 = exploring(point_exploring, h1, h2, func)

        if func(point_1) < func(point_0):
            point_exploring = sample(point_0, point_1, gamma)
            point_0 = point_1
        else:
            if h1 < h_min and h2 < h_min:
                break
            else:
                if h1 > h_min:
                    h1 = h1 * alpha
                if h2 > h_min:
                    h2 = h2 * alpha
                point_exploring = point_0

    return point_0, i


print('\n\t\t ~ Реализация метода Хука-Дживса ~ ')
print('_'*60)

yn = int(input('\nЗадать начальную точку самостоятельно? да-1 нет-0\t->\t'))

if yn == 1:
    a, b = map(int, input('\n\tВведите координаты начальной точки через пробел: ').split())
    point = Vector(a, b)
else:
    point = Vector(random.randint(-10, 10), random.randint(-10, 10))

min_point, iteration = hook_jeeves(func=func_r,
                                   point_0=point)

if iteration is not None:
    print('\n\tАлгоритм выполняется ...\n')
    print('_'*60)
    print('Алгоритм выполнился', iteration, 'раз')
    print('Минимум функции в точке (x, y) = ', min_point)
    print('Значение функции F(x, y) = ', round(func_r(min_point), 6))
    print('_'*60)
