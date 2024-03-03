import pyglet

window = pyglet.window.Window(width=1280, height=720, caption="Graph")
window.set_location(x=400, y=200)
star = pyglet.shapes.Star(100,100,7,3,5, color=(50,225,30))
circle = pyglet.shapes.Circle(x=700, y=150, radius=10, color=(50, 225, 30))

@window.event
def on_draw() -> None:
    window.clear()
    circle.draw()
    star.draw()

def display():
    pyglet.app.run()

if __name__ == "__main__":
    display()
