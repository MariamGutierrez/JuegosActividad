from machine import Pin, I2C, ADC
from time import sleep_ms, sleep
from ssd1306 import SSD1306_I2C 
import random

ancho = 128
alto = 64

pinboton=26
pinejeX=13
pinejey=12
pinSCL=22
pinSDA=23

ejex= ADC(Pin(pinejeX))
ejex.atten(ADC.ATTN_11DB)
ejex.width(ADC.WIDTH_12BIT)

boton=Pin(pinboton,Pin.IN,Pin.PULL_UP)

ejey=ADC(Pin(pinejey))
ejey.atten(ADC.ATTN_11DB)
ejey.width(ADC.WIDTH_12BIT)

i2c = I2C(0, scl=Pin(pinSCL), sda=Pin(pinSDA))
oled = SSD1306_I2C(ancho, alto, i2c)

xActual=12
yActual=5

oled.rect(0,0,126,61,1)

class cuerpo:
  def __init__(self, oled):
    self.x = 4
    self.y = 4
    self.oled = oled
  
  def dibujar(self):
    oled.pixel(self.x, self.y, 0) 
  
  def mover (self):
    if ejex.read()<1000:
      self.x -= 1
    elif ejex.read()>4000:
      self.x += 1
    elif ejey.read()<1000:
      self.y -= 1
    elif ejey.read()>4000:
      self.y += 1


class comidita:
  def __init__(self, oled):
    self.x = random.randrange (11)*10
    self.y = random.randrange (5)*10
    self.oled = oled
  
  def dibujar(self):
    oled.pixel(self.x, self.y, 0)

  def mas_comidita(self):
    self.x = random.randrange (11)*10
    self.y = random.randrange (5)*10


def refrescar (oled):
  oled.fill(1)
  comida.dibujar()
  for i in range(len(serpiente)):
    serpiente[i].dibujar()
  oled.show()
  
def seguir_cabeza():
  for i in range (len(serpiente)- 1):
    serpiente[len(serpiente)-i-1].x = serpiente[len(serpiente)-i-2].x
    serpiente[len(serpiente)-i-1].y = serpiente[len(serpiente)-i-2].y

def main ():
  global serpiente, comida
  comida = comidita(oled)
  serpiente = [cuerpo (oled)]
  run = True
  while run:
    if boton.value() == 0:
      run = False

    serpiente[0].mover()
    refrescar(oled)
    
    if serpiente[0].x == comida.x and serpiente[0].y == comida.y:
      comida.mas_comidita()
      serpiente.append(cuerpo(oled))
    if serpiente[0].x >= 128:
      oled.text("Game Over :(",30, 12, 0)
      run = False
    elif serpiente[0].x < 0:
      oled.text("Game Over :(",30, 12, 0)
      run = False
    if serpiente[0].y >= 61:
      oled.text("Game Over :(",30, 12, 0)
      run = False
    elif serpiente[0].y < 0:
      oled.text("Game Over :(",30, 12, 0)
      run = False
    seguir_cabeza()


while True:
  main()
  oled.show()
  sleep(0.3)