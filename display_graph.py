from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Circle, Line
from pyglet.graphics import Batch

class Renderer(Window):
    def __init__(self, x_window_size, y_window_size, adj_dict):
        self.x_window_size = x_window_size
        self.y_window_size = y_window_size
        super().__init__(self.x_window_size, self.y_window_size, "Graph")
        self.batch = Batch()
        nodes_arr = []
        for node_pos in adj_dict:
            nodes_arr.append(Circle(node_pos[0], node_pos[1], radius=50, color=(255,255,0), batch=self.batch))

    def on_draw(self):
        self.clear()


if __name__ == "__main__":
    #x = int(input('Size of x? '))
    #y = int(input('Size of y? '))
    x = 1280
    y = 640
    adj_dict = {(10,20): {(20,10): 5}, (20,10): {(10,20): 5}}

    renderer = Renderer(x, y, adj_dict)
    run()
