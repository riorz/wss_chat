from blessed import Terminal
from collections import namedtuple

Pos = namedtuple('Pos', ['x', 'y'])


class Display:
    def __init__(self):
        self.term = term = Terminal()
        self.width = term.width
        self.height = term.height
        self.input_cursor = Pos(0, 0)
        self.output_cursor = Pos(3, 0)
        self.input_box = Pos(term.width, 1)
        self.output_box = Pos(term.width, term.height - 2)

    def clear(self):
        print(self.term.clear)
        with self.term.location(0, self.input_box.y + 1):
            print('=' * self.term.width, end='')

    def print(self, message, wait_input=True):
        print(self.term.move(self.output_cursor.x, self.output_cursor.y) + message)
        self.output_cursor = Pos(self.output_cursor.x + 1, self.output_cursor.y)
        if wait_input:
            self.wait_input()

    def wait_input(self):
        with self.term.location(self.width, self.input_cursor.y + 1):
            print(self.term.clear_bol)
        print(self.term.move(self.input_cursor.x, self.input_cursor.y))
