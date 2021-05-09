"""

Create a checkered pattern across the device's lights.
You may view how this looks at `/resources/light_py.jpg`.

"""

import launchpad

lp = launchpad.Device()

@lp.on("ready")
def on_ready():
    for x in range(8):
        for y in range(8):
            if x % 2 == y % 2:
                lp.light(x, y)

if __name__ == "__main__":
    lp.run()
