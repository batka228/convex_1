from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

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

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)

    def cardinality(self):
        x, y = self.p.x, self.p.y
        if x**2 + y**2 == 1:
            return 1
        return 0

    def ind(self):
        return 0


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self

    def cardinality(self):

        card = 0

        xa, ya = self.p.x, self.p.y
        xb, yb = self.q.x, self.q.y

        r = 1
        a = yb - ya
        b = xa - xb
        c = xb * ya - xa * yb

        x0 = -a*c/(a*a+b*b)
        y0 = -b*c/(a*a+b*b)

        if (c*c > r*r*(a*a+b*b)):
            card = 0
        elif (c*c == r*r*(a*a+b*b)):
            if not((x0 < xa and x0 < xb) or (x0 > xa and x0 > xb)):
                card = 1
            else:
                card = 0
        else:
            d = r*r - c*c/(a*a+b*b)
            mult = (d / (a*a+b*b))**0.5
            ax = x0 + b * mult
            bx = x0 - b * mult
            ay = y0 - a * mult
            by = y0 + a * mult
            ccc = 0
            if (xa**2 + ya**2 == 1) \
                and ((xa != ax and ya != ay)
                     or (xa != bx and ya != by)):
                if ((xa-ax)**2 + (ya-ay)**2)**0.5 \
                        < ((xa-bx)**2 + (ya-by)**2)**0.5:
                    if (not((bx < xa and bx < xb) or (bx > xa and bx > xb))
                            and (not((by < ya and by < yb)
                                     or (by > ya and by > yb)))):
                        card = 2
                    else:
                        card = 1
                else:
                    if (not((ax < xa and ax < xb) or (ax > xa and ax > xb))
                            and (not((ay < ya and ay < yb)
                                     or (ay > ya and ay > yb)))):
                        card = 2
                    else:
                        card = 1
                ccc = 1
            elif (xb**2 + yb**2 == 1) \
                    and ((xb != ax and yb != ay) or (xb != bx and yb != by)):
                if ((xb-ax)**2 + (yb-ay)**2)**0.5 \
                        < ((xb-bx)**2 + (yb-by)**2)**0.5:
                    if (not((bx < xa and bx < xb) or (bx > xa and bx > xb))
                            and (not((by < ya and by < yb)
                                     or (by > ya and by > yb)))):
                        card = 2
                    else:
                        card = 1
                else:
                    if (not((ax < xa and ax < xb) or (ax > xa and ax > xb))
                            and (not((ay < ya and ay < yb)
                                     or (ay > ya and ay > yb)))):
                        card = 2
                    else:
                        card = 1
                ccc = 1

            if ((xa**2 + ya**2 == 1 and xb**2 + yb**2 < 1)
                    or (xb**2 + yb**2 == 1
                        and xa**2 + ya**2 < 1)) and not(ccc):
                card = 1
                ccc = 1

            if ((not((ax < xa and ax < xb) or (ax > xa and ax > xb)))
                and (not((ay < ya and ay < yb) or (ay > ya and ay > yb)))
                and (not((bx < xa and bx < xb) or (bx > xa and bx > xb)))
                    and (not((by < ya and by < yb)
                             or (by > ya and by > yb)))) and not(ccc):
                card = 2
            elif (not((ax < xa and ax < xb) or (ax > xa and ax > xb))) \
                    and (not((ay < ya and ay < yb)
                             or (ay > ya and ay > yb))) and not(ccc):
                card = 1
            elif (not((bx < xa and bx < xb) or (bx > xa and bx > xb))
                  and (not((by < ya and by < yb)
                           or (by > ya and by > yb)))) and not(ccc):
                card = 1
            elif not(ccc):
                card = 0

        return 2 * card

    def ind(self):
        return 0


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
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
        self.point = []
        self.point_ = []

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
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

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)
            self.point_.append(t)

        return self

    # вычисление мощности
    def cardinality(self):

        card = 0
        par = 0

        for _ in range(self.points.size()):

            # математика вычисления мощности

            xa, ya = self.points.first().x, self.points.first().y
            xb, yb = self.points.last().x, self.points.last().y

            if xa**2 + ya**2 == 1:
                par += 1

            if xb**2 + yb**2 == 1:
                par += 1

            r = 1
            a = yb - ya
            b = xa - xb
            c = xb * ya - xa * yb

            x0 = -a*c/(a*a+b*b)
            y0 = -b*c/(a*a+b*b)

            if (c*c > r*r*(a*a+b*b)):
                card += 0
            elif (c*c == r*r*(a*a+b*b)):
                if not((x0 < xa and x0 < xb) or (x0 > xa and x0 > xb)):
                    card += 1
                    self.point.append(R2Point(x0, y0))
                else:
                    card += 0
            else:
                d = r*r - c*c/(a*a+b*b)
                mult = (d / (a*a+b*b))**0.5
                ax = x0 + b * mult
                bx = x0 - b * mult
                ay = y0 - a * mult
                by = y0 + a * mult
                ccc = 0
                if (xa**2 + ya**2 == 1) and ((xa != ax and ya != ay)
                                             or (xa != bx and ya != by)):
                    if ((xa-ax)**2 + (ya-ay)**2)**0.5 \
                            < ((xa-bx)**2 + (ya-by)**2)**0.5:
                        if (not((bx < xa and bx < xb) or (bx > xa and bx > xb))
                                and (not((by < ya and by < yb)
                                         or (by > ya and by > yb)))):
                            card += 2
                            self.point.append(R2Point(ax, ay))
                            self.point.append(R2Point(bx, by))
                        else:
                            card += 1
                            self.point.append(R2Point(ax, ay))
                    else:
                        if (not((ax < xa and ax < xb) or (ax > xa and ax > xb))
                                and (not((ay < ya and ay < yb)
                                         or (ay > ya and ay > yb)))):
                            card += 2
                            self.point.append(R2Point(ax, ay))
                            self.point.append(R2Point(bx, by))
                        else:
                            card += 1
                            self.point.append(R2Point(bx, by))
                    ccc = 1
                elif (xb**2 + yb**2 == 1) and ((xb != ax and yb != ay)
                                               or (xb != bx and yb != by)):
                    if ((xb-ax)**2 + (yb-ay)**2)**0.5 \
                            < ((xb-bx)**2 + (yb-by)**2)**0.5:
                        if (not((bx < xa and bx < xb) or (bx > xa and bx > xb))
                                and (not((by < ya and by < yb)
                                         or (by > ya and by > yb)))):
                            card += 2
                            self.point.append(R2Point(ax, ay))
                            self.point.append(R2Point(bx, by))
                        else:
                            card += 1
                            self.point.append(R2Point(ax, ay))
                    else:
                        if (not((ax < xa and ax < xb) or (ax > xa and ax > xb))
                                and (not((ay < ya and ay < yb)
                                         or (ay > ya and ay > yb)))):
                            card += 2
                            self.point.append(R2Point(ax, ay))
                            self.point.append(R2Point(bx, by))
                        else:
                            card += 1
                            self.point.append(R2Point(bx, by))
                    ccc = 1

                if ((xa**2 + ya**2 == 1 and xb**2 + yb**2 < 1)
                        or (xb**2 + yb**2 == 1
                            and xa**2 + ya**2 < 1)) and not(ccc):
                    card += 1
                    if xa**2 + ya**2 == 1:
                        self.point.append(R2Point(xa, ya))
                    elif xb**2 + yb**2 == 1:
                        self.point.append(R2Point(xb, yb))
                    ccc = 1

                if ((not((ax < xa and ax < xb) or (ax > xa and ax > xb)))
                    and (not((ay < ya and ay < yb) or (ay > ya and ay > yb)))
                    and (not((bx < xa and bx < xb) or (bx > xa and bx > xb)))
                        and (not((by < ya and by < yb)
                                 or (by > ya and by > yb)))) and not(ccc):
                    card += 2
                    self.point.append(R2Point(ax, ay))
                    self.point.append(R2Point(bx, by))
                elif (not((ax < xa and ax < xb) or (ax > xa and ax > xb))) \
                        and (not((ay < ya and ay < yb)
                                 or (ay > ya and ay > yb))) and not(ccc):
                    card += 1
                    self.point.append(R2Point(ax, ay))
                elif (not((bx < xa and bx < xb) or (bx > xa and bx > xb))
                        and (not((by < ya and by < yb)
                                 or (by > ya and by > yb)))) and not(ccc):
                    card += 1
                    self.point.append(R2Point(bx, by))
                elif not(ccc):
                    card += 0

            self.points.push_last(self.points.pop_first())
        return int(card - par/2)

    def ind(self):
        for i in range(len(self.point)):
            x, y = self.point[i].x, self.point[i].y
            j = 0
            for _ in range(self.points.size()):
                xa, ya = self.points.first().x, self.points.first().y
                xb, yb = self.points.last().x, self.points.last().y
                if (x-xa)*(yb-ya) == (y-ya)*(xb-xa) \
                        and min(xa, xb) <= x <= max(xa, xb):
                    j += 1
                self.points.push_last(self.points.pop_first())
            if not(j):
                self.point = []
                return 1

        t = self.point_[len(self.point_) - 1]
        for _ in range(self.points.size()):
            if not(t.is_light(self.points.last(), self.points.first())):
                return 1
            self.points.push_last(self.points.pop_first())

        return 0


if __name__ == "__main__":
    f = Void()
    f = f.add(R2Point(0.0, 0.0))
    # print(f.ind())
    f = f.add(R2Point(0.9, 0.9))
    # print(f.ind())
    f = f.add(R2Point(-0.9, 0.9))
    # print(f.ind())
    f = f.add(R2Point(-0.9, -0.9))
    # print(f.ind())
    f = f.add(R2Point(0.9, -0.9))
    # print(f.ind())
    # print(f.cardinality())
    # print(f.ind())
    f = f.add(R2Point(12.0, 12.0))
    # print(f.ind())
    # print(f.cardinality())
    # print(f.ind())
    # f = f.add(R2Point(-12.0, -12.0))
    # print(f.ind())
    # print(f.cardinality())
    # print(f.ind())
    # f = f.add(R2Point(0.0, 1.0))
    # f = f.add(R2Point(0.0, -1.0))
    # f = f.add(R2Point(1.0, 0.0))
    # print(f.ind())
    # print(f.cardinality())
    # print(f.ind())
    # f = f.add(R2Point(-1.0, 0.0))
    # print(f.ind())
    # f = f.add(R2Point(-1.1, 0.0))
    # print(f.cardinality())
