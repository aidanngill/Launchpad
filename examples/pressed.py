""" Print out whenever a key is pressed/released. """

import launchpad

lp = launchpad.Device()

@lp.on("click")
def on_click(x, y):
    print(f"Key ({x}, {y}) was pressed")

@lp.on("release")
def on_release(x, y):
    print(f"Key ({x}, {y}) was released")

if __name__ == "__main__":
    lp.run()
