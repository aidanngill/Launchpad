""" Run async functions from the press of a button. """

import launchpad

lp = launchpad.Device()

async def do_macro():
    print("Running a macro!")

@lp.on("ready")
def on_ready():
    lp.macro.set(0, 0, do_macro)

if __name__ == "__main__":
    lp.run()
