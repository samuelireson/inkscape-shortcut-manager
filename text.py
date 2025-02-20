import os
import tempfile
import subprocess
from evdev import UInput, ecodes as e

def text():
    f = tempfile.NamedTemporaryFile(
        mode='w+',
        delete=False,
        suffix='.typ'
    )
    f.write('$$')
    f.close()

    subprocess.run([
        'kitty', 'nvim', f.name
    ])

    with open (f.name, 'r') as c:
        content = """
        #set page(height: auto, width: auto, margin: 0cm, fill: none)
        #set text(size: 12pt)
        #show math.equation: set text(font: "STIX Two Math")

        """ + c.read().strip()

    os.remove(f.name)

    m = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    m.write(content)
    m.close()

    cwd = tempfile.gettempdir()
    subprocess.run(
        ['typst', 'compile', '--format', 'svg', m.name],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    svg_path = m.name + ".svg"

    with open(svg_path, 'r') as svg:
        subprocess.run(
            ['wl-copy'],
            stdin=svg
        )

    os.remove(svg_path)

    ui = UInput()
    ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 1)
    ui.write(e.EV_KEY, e.KEY_V, 1)
    ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)
    ui.write(e.EV_KEY, e.KEY_V, 0)
    ui.syn()


