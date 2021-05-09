""" Barebones script. """

import launchpad

lp = launchpad.Device()

@lp.on("ready")
def on_ready():
    print("Connected to Launchpad (I: {0}, O: {1})".format(
        lp.input.name,
        lp.output.name
    ))

if __name__ == "__main__":
    lp.run()
