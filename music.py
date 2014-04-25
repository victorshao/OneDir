import pyglet
class start:
    def __init__(self):
        song = pyglet.media.load('start.wav')
        song.play()
        pyglet.app.run()
class exit:
    def __init__(self):
        song = pyglet.media.load('exit.wav')
        song.play()
        pyglet.app.run()