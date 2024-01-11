import utils
from game import Juego

if __name__ == "__main__":
    resolution = utils.load_resolution_from_csv()
    if resolution:
        Juego(resolution).run()
    else:
        Juego().run()