import math
import mido
import asyncio
import logging
from types import MethodType

from .macro import MacroManager
from .message import Message
from .exceptions import DeviceNotFound, InvalidCoordinate

log = logging.getLogger(__name__)

def find_midi_devices():
    """ Find the I/O devices for the Launchpad. """
    devices = [None, None]

    for device in mido.get_input_names():
        if "Launchpad" in device:
            devices[0] = device
    
    for device in mido.get_output_names():
        if "Launchpad" in device:
            devices[1] = device

    if None in devices:
        raise DeviceNotFound("No Launchpad was found.")

    return (
        mido.open_input(devices[0]),
        mido.open_output(devices[1], autoreset=True)
    )

def translate_coordinate(x, y):
    """ Translate from x/y coordinates to MIDI, decimal coordinates. """
    if not 0 <= x <= 8 or not 0 <= y <= 8:
        raise InvalidCoordinate(f"Invalid coordinates were provided: {x}, {y}")

    return (0x10 * y) + x

def translate_key(key):
    """ Translate from MIDI coordinates to x/y coordinates. """
    vertical = math.floor(key / 16)
    horizontal = key - (vertical * 16)

    return horizontal, vertical

def do_send(self, message_type, data):
    message_types = {
        "control_change": ["control", "value"],
        "note_on": ["note", "velocity"],
        "note_off": ["note", "velocity"]
    }

    kwargs = {}
    for idx in range(len(data)):
        kwargs[message_types[message_type][idx]] = data[idx]

    message = mido.Message(message_type, **kwargs)
    return self.send(message)

class Device:
    def __init__(self, loop=None):
        # Set up MIDI I/O
        self.input, self.output = find_midi_devices()
        self.loop = loop if loop else asyncio.get_event_loop()

        self.output.do_send = MethodType(do_send, self.output)

        # Define macro manager
        self.macro = MacroManager(self, self.loop)

        callback = lambda *_, **__: None
        self.methods = {
            "click": callback,
            "release": callback,
            "ready": callback,
            "stop": callback
        }

    def on(self, method):
        """ Allows the user to implement callbacks. """
        def _on(func, *args):
            self.methods[method] = func
            log.debug("Updated callback for '{0}' to function {1}".format(method, func))

        return _on

    def make_stream(self):
        """ Make async stream for the MIDI device. """
        queue = asyncio.Queue()

        def callback(message):
            self.loop.call_soon_threadsafe(queue.put_nowait, message)

        async def stream():
            while True:
                yield await queue.get()

        return callback, stream()

    async def process_messages(self):
        """ Process the incoming MIDI messages. """
        cb, stream = self.make_stream()
        self.input.callback = cb

        self.output.reset()
        self.methods["ready"]()

        log.debug("Readied the device")

        async for message in stream:
            data = Message(message)
            x, y = translate_key(data.key)

            log.debug("Received key event: {0}, {1} [Pressed: {2}]".format(x, y, data.clicked))

            if data.clicked:
                if self.macro.is_bound(x, y):
                    await self.macro.click(x, y)

                self.methods["click"](x, y)
            else:
                self.methods["release"](x, y)

    def light(self, x, y, on=True, colour=0x3E):
        """ Set Launchpad lights. """
        method_type = "note_on" if on else "note_off"
        self.output.do_send(
            method_type, [
                translate_coordinate(x, y),
                colour
            ]
        )

    def run(self):
        """ Run the processing loop, and handle shutdown. """
        try:
            self.loop.run_until_complete(self.process_messages())
        except KeyboardInterrupt:
            log.debug("Caught an interrupt, shutting down cleanly...")

            def shutdown_exception_handler(loop, context):
                if "exception" not in context \
                or not isinstance(context["exception"], asyncio.CancelledError):
                    self.loop.default_exception_handler(context)
            self.loop.set_exception_handler(shutdown_exception_handler)

            tasks = asyncio.gather(*asyncio.Task.all_tasks(loop=self.loop), loop=self.loop, return_exceptions=True)
            tasks.add_done_callback(lambda t: self.loop.stop())
            tasks.cancel()

            while not tasks.done() and not self.loop.is_closed():
                self.loop.run_forever()

        finally:
            self.shutdown()

            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()

            log.debug("Closed the event loop")

    def shutdown(self):
        """ Shut down the MIDI I/O cleanly. """
        self.output.do_send("control_change", [0x00, 0x00])

        self.input.close()
        self.output.close()
