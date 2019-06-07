import asyncio
from blessed import Terminal
from dataclasses import dataclass


@dataclass
class Pos:
    x: int
    y: int


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
        self.output_cursor += 1
        if wait_input:
            self.wait_input()

    def wait_input(self):
        with self.term.location(self.width, self.input_cursor.y + 1):
            print(self.term.clear_bol)
        print(self.term.move(self.input_cursor.x, self.input_cursor.y))


class AsyncPrompt:
    """ A non-blocking prompt
        Ref: https://stackoverflow.com/questions/35223896/listen-to-keypress-with-asyncio
    """
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.q = asyncio.Queue(loop=self.loop)
        self.loop.add_reader(sys.stdin, self.got_input)

    def got_input(self):
        asyncio.ensure_future(self.q.put(sys.stdin.readline()), loop=self.loop)

    async def __call__(self, msg, end='\n', flush=False):
        print(msg, end=end, flush=flush)
        return (await self.q.get()).rstrip('\n')