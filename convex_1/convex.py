from deq import Deq
from r2point import R2Point
import math


class Figure:
    """Абстрактная фигура"""

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p
        self.point_ = []
        self.circle_point = []

    def add(self, q):
        return (
            self if self.p == q else Segment(self.p,
                                             q,
                                             self.point_,
                                             self.circle_point)
        )

    def cardinality(self):
        x, y = self.p.x, self.p.y
        if x**2 + y**2 == 1:
            return 1
        return 0


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, lst, circle_point):
        self.p, self.q = p, q
        self.point_ = lst
        self.circle_point = circle_point

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            self.cardinality(self.p, r, mode=1)
            self.cardinality(self.q, r, mode=1)
            return Polygon(self.p, self.q, r, self.point_, self.circle_point)
        elif self.q.is_inside(self.p, r):
            self.point_.pop()
            self.cardinality(self.p, r, mode=1)
            return Segment(self.p, r, self.point_, self.circle_point)
        elif self.p.is_inside(r, self.q):
            self.point_.pop()
            self.cardinality(r, self.q, mode=1)
            return Segment(r, self.q, self.point_, self.circle_point)
        else:
            return self

    def cardinality(self, A=None, B=None, mode=0):

        if mode == 0:
            A, B = self.p, self.q
            x1, y1 = self.p.x, self.p.y
            x2, y2 = self.q.x, self.q.y
        elif mode == 1:
            x1, y1 = A.x, A.y
            x2, y2 = B.x, B.y

        a = y2 - y1
        b = x1 - x2
        c = x2 * y1 - x1 * y2

        discriminant = (a**2 + b**2) - c**2
        if discriminant < 0:
            return 0
        else:
            x_1 = round(
                (-a * c + b * math.sqrt(discriminant)) / (a**2 + b**2), 5
            )
            y_1 = round(
                (-b * c - a * math.sqrt(discriminant)) / (a**2 + b**2), 5
            )
            x_2 = round(
                (-a * c - b * math.sqrt(discriminant)) / (a**2 + b**2), 5
            )
            y_2 = round(
                (-b * c + a * math.sqrt(discriminant)) / (a**2 + b**2), 5
            )

            q, d = 0, 0
            points = []
            if min(x1, x2) <= x_1 <= max(x1, x2) and min(
                y1, y2
            ) <= y_1 <= max(y1, y2):
                points.append((x_1, y_1))
                q = 1
                if not (R2Point(x_1, y_1) in self.circle_point):
                    self.circle_point.append(R2Point(x_1, y_1))
            if min(x1, x2) <= x_2 <= max(x1, x2) and min(
                y1, y2
            ) <= y_2 <= max(y1, y2):
                if (x_2, y_2) not in points:
                    points.append((x_2, y_2))
                    d = 1
                    if not (
                        R2Point(x_2, y_2) in self.circle_point
                    ):
                        self.circle_point.append(
                            R2Point(x_2, y_2)
                        )

            if q == 1 and d == 1:
                self.point_.append(
                    [
                        A,
                        B,
                        2,
                        [
                            R2Point(x_1, y_1),
                            R2Point(x_2, y_2),
                        ],
                    ]
                )
            elif q == 1:
                self.point_.append(
                    [A, B, 1, [R2Point(x_1, y_1)]]
                )
            elif d == 1:
                self.point_.append(
                    [A, B, 1, [R2Point(x_2, y_2)]]
                )

            return len(points) * 2


class Polygon(Figure):
    """Многоугольник"""

    def __init__(self, a, b, c, lst, circle_point):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self.point_ = lst
        self.circle_point = circle_point

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for _ in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            self.search_del(self.points.first(), self.points.last())

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                self.search_del(self.points.first(), p)
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                self.search_del(self.points.last(), p)
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first())
            self._perimeter += t.dist(self.points.last())

            self.card(t, self.points.first())
            self.card(t, self.points.last())

            self.points.push_first(t)

        return self

    # точки пересечения заданного ребра
    def card(self, A, B):

        x1, y1 = A.x, A.y
        x2, y2 = B.x, B.y

        a = y2 - y1
        b = x1 - x2
        c = x2 * y1 - x1 * y2

        discriminant = (a**2 + b**2) - c**2
        if discriminant < 0:
            return self
        else:
            x_1 = round(
                (-a * c + b * math.sqrt(discriminant)) / (a**2 + b**2), 5
            )
            y_1 = round(
                (-b * c - a * math.sqrt(discriminant)) / (a**2 + b**2), 5
            )
            x_2 = round(
                (-a * c - b * math.sqrt(discriminant)) / (a**2 + b**2), 5
            )
            y_2 = round(
                (-b * c + a * math.sqrt(discriminant)) / (a**2 + b**2), 5
            )

            q, d = 0, 0
            points = []
            if min(x1, x2) <= x_1 <= max(x1, x2) and min(
                y1, y2
            ) <= y_1 <= max(y1, y2):
                points.append((x_1, y_1))
                q = 1
                if not (R2Point(x_1, y_1) in self.circle_point):
                    self.circle_point.append(R2Point(x_1, y_1))
            if min(x1, x2) <= x_2 <= max(x1, x2) and min(
                y1, y2
            ) <= y_2 <= max(y1, y2):
                if (x_2, y_2) not in points:
                    points.append((x_2, y_2))
                    d = 1
                    if not (
                        R2Point(x_2, y_2) in self.circle_point
                    ):
                        self.circle_point.append(
                            R2Point(x_2, y_2)
                        )

            if q == 1 and d == 1:
                self.point_.append(
                    [
                        A,
                        B,
                        2,
                        [
                            R2Point(x_1, y_1),
                            R2Point(x_2, y_2),
                        ],
                    ]
                )
            elif q == 1:
                self.point_.append(
                    [A, B, 1, [R2Point(x_1, y_1)]]
                )
            elif d == 1:
                self.point_.append(
                    [A, B, 1, [R2Point(x_2, y_2)]]
                )

            return self

    def search_del(self, p, d):
        for i in range(len(self.point_)):
            if (p == self.point_[i][0] and d == self.point_[i][1]) or (
                d == self.point_[i][0] and p == self.point_[i][1]
            ):
                q = self.point_.pop(i)
                for k in range(q[2]):
                    if q[3][k] in self.circle_point:
                        self.circle_point.remove(q[3][k])
                break
        return self

    def cardinality(self):
        return len(self.circle_point)
