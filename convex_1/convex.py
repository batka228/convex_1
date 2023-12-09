from deq import Deq
from r2point import R2Point


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

        card = 0

        if mode == 0:
            A, B = self.p, self.q
            xa, ya = self.p.x, self.p.y
            xb, yb = self.q.x, self.q.y
        elif mode == 1:
            xa, ya = A.x, A.y
            xb, yb = B.x, B.y

        r = 1
        a = yb - ya
        b = xa - xb
        c = xb * ya - xa * yb

        x0 = -a * c / (a * a + b * b)
        y0 = -b * c / (a * a + b * b)

        if c * c == r * r * (a * a + b * b):
            if not ((x0 < xa and x0 < xb) or (x0 > xa and x0 > xb)):
                card = 1
                self.point_.append([A, B, 1, [R2Point(x0, y0)]])
                if not (R2Point(x0, y0) in self.circle_point):
                    self.circle_point.append(R2Point(x0, y0))
        elif c * c < r * r * (a * a + b * b):
            d = r * r - c * c / (a * a + b * b)
            mult = (d / (a * a + b * b)) ** 0.5
            ax = x0 + b * mult
            bx = x0 - b * mult
            ay = y0 - a * mult
            by = y0 + a * mult
            ccc = 0
            if (xa**2 + ya**2 == 1) and (
                (xa != ax and ya != ay) or (xa != bx and ya != by)
            ):
                if ((xa - ax) ** 2 + (ya - ay) ** 2) ** 0.5 < (
                    (xa - bx) ** 2 + (ya - by) ** 2
                ) ** 0.5:
                    if not (
                        (bx < xa and bx < xb) or (bx > xa and bx > xb)) and (
                        not (
                            (by < ya and by < yb) or (by > ya and by > yb))
                    ):
                        card = 2
                        self.point_.append(
                            [A, B, 2, [R2Point(ax, ay), R2Point(bx, by)]]
                        )
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                    else:
                        card = 1
                        self.point_.append([A, B, 1, [R2Point(ax, ay)]])
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                else:
                    if not (
                        (ax < xa and ax < xb) or (ax > xa and ax > xb)) and (
                        not (
                            (ay < ya and ay < yb) or (ay > ya and ay > yb))
                    ):
                        card = 2
                        self.point_.append(
                            [A, B, 2, [R2Point(ax, ay), R2Point(bx, by)]]
                        )
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                    else:
                        card = 1
                        self.point_.append([A, B, 1, [R2Point(bx, by)]])
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                ccc = 1
            elif (xb**2 + yb**2 == 1) and (
                (xb != ax and yb != ay) or (xb != bx and yb != by)
            ):
                if ((xb - ax) ** 2 + (yb - ay) ** 2) ** 0.5 < (
                    (xb - bx) ** 2 + (yb - by) ** 2
                ) ** 0.5:
                    if not (
                        (bx < xa and bx < xb) or (bx > xa and bx > xb)) and (
                        not (
                            (by < ya and by < yb) or (by > ya and by > yb))
                    ):
                        card = 2
                        self.point_.append(
                            [A, B, 2, [R2Point(ax, ay), R2Point(bx, by)]]
                        )
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                    else:
                        card = 1
                        self.point_.append([A, B, 1, [R2Point(ax, ay)]])
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                else:
                    if not (
                        (ax < xa and ax < xb) or (ax > xa and ax > xb)) and (
                        not (
                            (ay < ya and ay < yb) or (ay > ya and ay > yb))
                    ):
                        card = 2
                        self.point_.append(
                            [A, B, 2, [R2Point(ax, ay), R2Point(bx, by)]]
                        )
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                    else:
                        card = 1
                        self.point_.append([A, B, 1, [R2Point(bx, by)]])
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                ccc = 1

            if (
                (xa**2 + ya**2 == 1 and xb**2 + yb**2 < 1)
                or (xb**2 + yb**2 == 1 and xa**2 + ya**2 < 1)
            ) and not (ccc):
                card = 1
                if xa**2 + ya**2 == 1:
                    self.point_.append([A, B, 1, [R2Point(xa, ya)]])
                    if not (R2Point(xa, ya) in self.circle_point):
                        self.circle_point.append(R2Point(xa, ya))
                elif xb**2 + yb**2 == 1:
                    self.point_.append([A, B, 1, [R2Point(xb, yb)]])
                    if not (R2Point(xb, yb) in self.circle_point):
                        self.circle_point.append(R2Point(xb, yb))
                ccc = 1

            if (
                (not ((ax < xa and ax < xb) or (ax > xa and ax > xb)))
                and (not ((ay < ya and ay < yb) or (ay > ya and ay > yb)))
                and (not ((bx < xa and bx < xb) or (bx > xa and bx > xb)))
                and (not ((by < ya and by < yb) or (by > ya and by > yb)))
            ) and not (ccc):
                card = 2
                self.point_.append([A, B, 2,
                                    [R2Point(ax, ay), R2Point(bx, by)]])
                if not (R2Point(ax, ay) in self.circle_point):
                    self.circle_point.append(R2Point(ax, ay))
                if not (R2Point(bx, by) in self.circle_point):
                    self.circle_point.append(R2Point(bx, by))
            elif (
                (not ((ax < xa and ax < xb) or (ax > xa and ax > xb)))
                and (not ((ay < ya and ay < yb) or (ay > ya and ay > yb)))
                and not (ccc)
            ):
                card = 1
                self.point_.append([A, B, 1, [R2Point(ax, ay)]])
                if not (R2Point(ax, ay) in self.circle_point):
                    self.circle_point.append(R2Point(ax, ay))
            elif (
                not ((bx < xa and bx < xb) or (bx > xa and bx > xb))
                and (not ((by < ya and by < yb) or (by > ya and by > yb)))
            ) and not (ccc):
                card = 1
                self.point_.append([A, B, 1, [R2Point(bx, by)]])
                if not (R2Point(bx, by) in self.circle_point):
                    self.circle_point.append(R2Point(bx, by))

        return 2 * card


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

        xa, ya = A.x, A.y
        xb, yb = B.x, B.y

        r = 1
        a = yb - ya
        b = xa - xb
        c = xb * ya - xa * yb

        x0 = -a * c / (a * a + b * b)
        y0 = -b * c / (a * a + b * b)

        if c * c == r * r * (a * a + b * b):
            if not ((x0 < xa and x0 < xb) or (x0 > xa and x0 > xb)):
                self.point_.append([A, B, 1, [R2Point(x0, y0)]])
                if not (R2Point(x0, y0) in self.circle_point):
                    self.circle_point.append(R2Point(x0, y0))

        elif c * c < r * r * (a * a + b * b):
            d = r * r - c * c / (a * a + b * b)
            mult = (d / (a * a + b * b)) ** 0.5
            ax = x0 + b * mult
            bx = x0 - b * mult
            ay = y0 - a * mult
            by = y0 + a * mult
            ccc = 0
            if (xa**2 + ya**2 == 1) and (
                (xa != ax and ya != ay) or (xa != bx and ya != by)
            ):
                if ((xa - ax) ** 2 + (ya - ay) ** 2) ** 0.5 < (
                    (xa - bx) ** 2 + (ya - by) ** 2
                ) ** 0.5:
                    if not (
                        (bx < xa and bx < xb) or (bx > xa and bx > xb)) and (
                        not (
                            (by < ya and by < yb) or (by > ya and by > yb))
                    ):
                        self.point_.append(
                            [A, B, 2, [R2Point(ax, ay), R2Point(bx, by)]]
                        )
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                    else:
                        self.point_.append([A, B, 1, [R2Point(ax, ay)]])
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                else:
                    if not (
                        (ax < xa and ax < xb) or (ax > xa and ax > xb)) and (
                        not (
                            (ay < ya and ay < yb) or (ay > ya and ay > yb))
                    ):
                        self.point_.append(
                            [A, B, 2, [R2Point(ax, ay), R2Point(bx, by)]]
                        )
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                    else:
                        self.point_.append([A, B, 1, [R2Point(bx, by)]])
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                ccc = 1
            elif (xb**2 + yb**2 == 1) and (
                (xb != ax and yb != ay) or (xb != bx and yb != by)
            ):
                if ((xb - ax) ** 2 + (yb - ay) ** 2) ** 0.5 < (
                    (xb - bx) ** 2 + (yb - by) ** 2
                ) ** 0.5:
                    if not (
                        (bx < xa and bx < xb) or (bx > xa and bx > xb)) and (
                        not (
                            (by < ya and by < yb) or (by > ya and by > yb))
                    ):
                        self.point_.append(
                            [A, B, 2, [R2Point(ax, ay), R2Point(bx, by)]]
                        )
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                    else:
                        self.point_.append([A, B, 1, [R2Point(ax, ay)]])
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                else:
                    if not (
                        (ax < xa and ax < xb) or (ax > xa and ax > xb)) and (
                        not (
                            (ay < ya and ay < yb) or (ay > ya and ay > yb))
                    ):
                        self.point_.append(
                            [A, B, 2, [R2Point(ax, ay), R2Point(bx, by)]]
                        )
                        if not (R2Point(ax, ay) in self.circle_point):
                            self.circle_point.append(R2Point(ax, ay))
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                    else:
                        self.point_.append([A, B, 1, [R2Point(bx, by)]])
                        if not (R2Point(bx, by) in self.circle_point):
                            self.circle_point.append(R2Point(bx, by))
                ccc = 1

            if (
                (xa**2 + ya**2 == 1 and xb**2 + yb**2 < 1)
                or (xb**2 + yb**2 == 1 and xa**2 + ya**2 < 1)
            ) and not (ccc):
                if xa**2 + ya**2 == 1:
                    self.point_.append([A, B, 1, [R2Point(xa, ya)]])
                    if not (R2Point(xa, ya) in self.circle_point):
                        self.circle_point.append(R2Point(xa, ya))
                elif xb**2 + yb**2 == 1:
                    self.point_.append([A, B, 1, [R2Point(xb, yb)]])
                    if not (R2Point(xb, yb) in self.circle_point):
                        self.circle_point.append(R2Point(xb, yb))
                ccc = 1

            if (
                (not ((ax < xa and ax < xb) or (ax > xa and ax > xb)))
                and (not ((ay < ya and ay < yb) or (ay > ya and ay > yb)))
                and (not ((bx < xa and bx < xb) or (bx > xa and bx > xb)))
                and (not ((by < ya and by < yb) or (by > ya and by > yb)))
            ) and not (ccc):
                self.point_.append([A, B, 2,
                                    [R2Point(ax, ay), R2Point(bx, by)]])
                if not (R2Point(ax, ay) in self.circle_point):
                    self.circle_point.append(R2Point(ax, ay))
                if not (R2Point(bx, by) in self.circle_point):
                    self.circle_point.append(R2Point(bx, by))
            elif (
                (not ((ax < xa and ax < xb) or (ax > xa and ax > xb)))
                and (not ((ay < ya and ay < yb) or (ay > ya and ay > yb)))
                and not (ccc)
            ):
                self.point_.append([A, B, 1, [R2Point(ax, ay)]])
                if not (R2Point(ax, ay) in self.circle_point):
                    self.circle_point.append(R2Point(ax, ay))
            elif (
                not ((bx < xa and bx < xb) or (bx > xa and bx > xb))
                and (not ((by < ya and by < yb) or (by > ya and by > yb)))
            ) and not (ccc):
                self.point_.append([A, B, 1, [R2Point(bx, by)]])
                if not (R2Point(bx, by) in self.circle_point):
                    self.circle_point.append(R2Point(bx, by))

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
        lst = []
        i, j = 0, 1
        while i != len(self.circle_point):
            while j != len(self.circle_point):
                if (
                    round(self.circle_point[i].x, 5) ==
                    round(self.circle_point[j].x, 5)
                ) and (
                    round(self.circle_point[i].y, 5) ==
                    round(self.circle_point[j].y, 5)
                ):
                    lst.append(self.circle_point[i])
                j += 1
            i += 1
            j = i + 1
        for q in lst:
            self.circle_point.remove(q)
        return len(self.circle_point)


if __name__ == "__main__":
    f = Void()

    f = f.add(R2Point(0.0, 0.0))
    f = f.add(R2Point(0.9, 0.9))
    f.cardinality()
    f = f.add(R2Point(0.9, -0.9))
    f = f.add(R2Point(-0.9, -0.9))
    f = f.add(R2Point(-0.9, 0.9))
    # f = f.add(R2Point(0.0, 2.0))

    print(f.cardinality())
