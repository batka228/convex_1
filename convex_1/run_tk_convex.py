#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    tk.draw_oval(R2Point(0.0, 0.0))
    pass


def point_draw(self, tk):
    tk.draw_oval(R2Point(0.0, 0.0))
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_oval(R2Point(0.0, 0.0))
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    tk.draw_oval(R2Point(0.0, 0.0))
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


tk = TkDrawer()
f = Void()
tk.clean()

try:
    while True:
        f = f.add(R2Point())
        tk.clean()
        f.draw(tk)
        print(f"S = {f.area()}, P = {f.perimeter()}")
        print(f"число пересечений {f.cardinality()}\n")
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
