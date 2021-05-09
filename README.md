# Launchpad

Library to interact with the lights and buttons of a Launchpad device. Currently only tested with a Launchpad Mini 1.

## Install
`python3 -m pip install git+https://github.com/ramadan8/Launchpad`

## Usage
At its most basic, a project using this library may look like the following.
```python
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
```
Giving the following output.
```bash
C:\Launchpad\examples>py basic.py
Connected to Launchpad (I: Launchpad Mini 0, O: Launchpad Mini 1)
```
You may find more of these examples in the `/examples/` directory.