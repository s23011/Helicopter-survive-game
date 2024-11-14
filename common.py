#標準モジュール
import os
from typing import Tuple
import json
#インストールのモジュール
import pygame
from pygame import Rect 
from pygame import Surface

FOLDER_PATH = ''

#Vecter
class Vecter2():
    def __init__(self,x,y):
        self.x=x
        self.y=y
    # def __init__(self,xy:Tuple=(0,0)):
    #     self.x=xy[0]
    #     self.y=xy[1]
    
    def str(self):
        return f'{self.x,self.y}'
    def tuple(self):
        return (self.x,self.y)

class Vecter3(Vecter2):
    def __init__(self,x=0.0,y=0.0,z=0.0):
        super().__init__(x,y)
        self.z=z

    def __init__(self,xyz:Tuple=(0,0,0)):
        self.x=xyz[0]
        self.y=xyz[1]
        self.z=xyz[2]

    def str(self):
        return f'{self.x,self.y,self.z}'
    def tuple(self):
        return (self.x,self.y,self.y)

#UI
class Window():
    def __init__(self,window_caption,window_size:Vecter2):
        self.caption = window_caption
        self.size = window_size
        self.center = Vecter2(self.size.x / 2,self.size.y / 2)

        pygame.init()
        pygame.display.set_caption(window_caption)
        self.surface = pygame.display.set_mode(window_size.tuple())

class Panel:
    def __init__(self,size:Tuple[int,int],center:Tuple[int,int],background_col = (255,255,255),side_color = (0,0,0),side_width = 4):
        self.rect = Rect(0,0,size[0],size[1])
        self.rect.center = (center[0],center[1])
        self.inner_rect = self.rect.inflate(-side_width*2,-side_width*2)

        self.backgroud_col = background_col  
        self.side_color = side_color  

    def draw(self, surface:Surface):
        pygame.draw.rect(surface, self.side_color, self.rect, 0)
        pygame.draw.rect(surface, self.backgroud_col, self.inner_rect, 0)

class Label():    
    def __init__(self,font_size,font_color:Tuple[int,int,int],center:Tuple[int,int]):
        self.font_size = font_size
        self.font_color = font_color
        self.center = Vecter2(center[0],center[1])
        self.font = pygame.font.SysFont(None,font_size)
        self.text = ''

    def draw(self,surface:Surface):
        img = self.font.render(self.text,True,self.font_color)
        x = self.center.x - img.get_width() / 2
        y = self.center.y - img.get_height() / 2
        surface.blit(img, (x, y))

    def Clear(self,window:Surface):
        self.text = ''
        self.draw(window)
    
#Method
def load_image(filename, colorkey = None):
    filename = os.path.join(FOLDER_PATH,filename)
    try:
        image = pygame.image.load(filename)
    except(pygame.error):
        print ("Cannot load image:",filename)
        raise(SystemExit)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image

def write_json(filename,data):
    filename =filename + '.json'
    filepath = os.path.join(FOLDER_PATH,filename)

    with open(filepath,'w') as file_obj:
        json.dump(data,file_obj)
        print(f'write json:{filepath}\n     data{data}')

def read_json(filename):
    filename =filename + '.json'
    filepath = os.path.join(FOLDER_PATH,filename)

    try:
        with open(filepath) as file_obj:
            data = json.load(file_obj)

            print(f'read json:{filepath}\n      data:{data}')
            return data
        
    except FileNotFoundError:
        print(f'read json not found:{filepath}')
        return []