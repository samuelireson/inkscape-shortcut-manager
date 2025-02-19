import os
import tempfile
import subprocess

def open_editor(filename):
    subprocess.run([
        'kitty', 'nvim', filename
    ])

def text():
    f = tempfile.NamedTemporaryFile(
        mode='w+',
        delete=False,
        suffix='.typ'
    )
    f.write('$$')
    f.close()

    open_editor(f.name)

    with open (f.name, 'r') as c:
        content = """
        #set page(height: auto, width: auto, margin: 0cm)
        #set text(size: 12pt)

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

def main():
    text()

if __name__ == '__main__':
    main()
