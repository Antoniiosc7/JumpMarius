import os
import pandas as pd
import pygame

BASE_IMG_PATH = 'recursos/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def save_resolution_to_csv(resolution):
    current_data = load_config_from_csv()
    current_data['Width'], current_data['Height'] = resolution
    save_config_to_csv(current_data)

def load_resolution_from_csv():
    try:
        config_df = pd.read_csv('config.csv')
        resolution = (config_df['Width'].iloc[0], config_df['Height'].iloc[0])
        print("Resolution loaded:", resolution)
        return resolution
    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError, ValueError):
        return None

def save_selected_character_to_csv(selected_character):
    current_data = load_config_from_csv()
    current_data['Character'] = selected_character
    save_config_to_csv(current_data)

def load_selected_character_from_csv():
    try:
        config_df = pd.read_csv('config.csv')
        selected_character = config_df['Character'].iloc[0]
        return selected_character
    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError, ValueError):
        return "Character1"  # Valor predeterminado si no se encuentra en el archivo o hay un error

def save_config_to_csv(data):
    config_df = pd.DataFrame(data)
    config_df.to_csv('config.csv', index=False)

def load_config_from_csv():
    try:
        config_df = pd.read_csv('config.csv')
        return config_df.to_dict(orient='list')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return {'Width': [], 'Height': [], 'Character': []}
    
def load_and_scale_background(game):
    # Obtener la resolución del archivo CSV
    resolution = load_resolution_from_csv()

    # Cargar y escalar la imagen de fondo
    background = pygame.image.load("recursos/Clouds7.png").convert()

    if resolution:
        background = pygame.transform.scale(background, resolution)

    return background
def get_available_levels():
    map_folder = "mapas"
    if os.path.exists(map_folder):
        return [file[:-5] for file in os.listdir(map_folder) if file.endswith(".json")]
    else:
        return []

# Añade esta función para actualizar el nivel seleccionado en el archivo config.csv
def save_selected_level_to_csv(selected_level):
    current_data = load_config_from_csv()
    current_data['Nivel'] = selected_level
    save_config_to_csv(current_data)

# Añade esta función para cargar el nivel seleccionado desde el archivo config.csv
def load_selected_level_from_csv():
    try:
        config_df = pd.read_csv('config.csv')
        if 'Nivel' in config_df.columns:
            selected_level = config_df['Nivel'].iloc[0]
            return selected_level
        else:
            print("La columna 'Nivel' no está presente en el archivo CSV.")
            return None
    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError, ValueError):
        return None
def load_selected_character_from_csv():
    try:
        config_df = pd.read_csv('config.csv')
        if 'Character' in config_df.columns:
            selected_character = config_df['Character'].iloc[0]
            return selected_character
        else:
            print("La columna 'Nivel' no está presente en el archivo CSV.")
            return None
    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError, ValueError):
        return None
class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]