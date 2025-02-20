from text import text
import pywayland
import pywayland.client as wl

class Manager():
    def __init__(self, inkscape_id):
        self.id = inkscape_id
        self.display = wl.display.Display()

def main():
    text()

if __name__ == '__main__':
    main()
