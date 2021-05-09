import asyncio
import logging

from .exceptions import NoMacroBound

log = logging.getLogger(__name__)

class MacroManager:
    def __init__(self, launchpad, loop):
        self.launchpad = launchpad
        self.loop = loop

        self.binds = [[None for _ in range(9)] for _ in range(8)]

    async def run(self, x, y):
        log.debug("Started running the function {0}".format(self.binds[y][x]))
        
        self.launchpad.light(x, y, colour=0xF)
        await self.binds[y][x]()
        self.launchpad.light(x, y)

    def set(self, x, y, func):
        self.binds[y][x] = func
        self.launchpad.light(x, y)

    def sidebar(self, y, func):
        self.binds[y][-1] = func
        self.launchpad.light(8, y, colour=0x38)

    async def click(self, x, y):
        if not self.is_bound(x, y):
            raise NoMacroBound("No macro was found for that coordinate.")

        asyncio.create_task(self.run(x, y))

    def is_bound(self, x, y):
        return self.binds[y][x] is not None
