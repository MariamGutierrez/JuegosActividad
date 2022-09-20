from machine import Pin, I2C, ADC
from time import sleep_ms, sleep
from ssd1306 import SSD1306_I2C
import random

#cambiar los pines

pinboton=26
pinejeX=12
pinejey=13
pinSCL=22
pinSDA=23


ancho = 128
alto = 64

tamañoX=25
tamañoY=12
matriz=[]
for i in range(tamañoX):
  matriz.append([])
  for j in range(tamañoY):
    matriz[i].append(0)
print(matriz)

ejex= ADC(Pin(pinejeX))
ejex.atten(ADC.ATTN_11DB)
ejex.width(ADC.WIDTH_12BIT)

boton=Pin(pinboton,Pin.IN,Pin.PULL_UP)

ejey=ADC(Pin(pinejey))
ejey.atten(ADC.ATTN_11DB)
ejey.width(ADC.WIDTH_12BIT)

i2c = I2C(0, scl=Pin(pinSCL), sda=Pin(pinSDA))
oled = SSD1306_I2C(ancho, alto, i2c)

cubito=[[tamañoX-1,5]]

cubo=[[tamañoX-2,5],[tamañoX-2,6],[tamañoX-1,6],[tamañoX-1,5]]
ele=[[tamañoX-2,5],[tamañoX-1,5],[tamañoX-2,6],[tamañoX-2,7]]
eleI=[[tamañoX-2,6],[tamañoX-1,6],[tamañoX-2,4],[tamañoX-2,5]]
rayo=[[tamañoX-2,6],[tamañoX-2,7],[tamañoX-1,6],[tamañoX-1,5]]
rayoI=[[tamañoX-2,5],[tamañoX-2,4],[tamañoX-1,6],[tamañoX-1,5]]
te=[[tamañoX-2,6],[tamañoX-1,6],[tamañoX-2,5],[tamañoX-2,7]]
linea=[[tamañoX-1,5],[tamañoX-1,4],[tamañoX-1,6],[tamañoX-1,7]]

oled.rect(0,0,126,61,1)

def display():
  for i in range(len(matriz)):
    for j in range(len(matriz[0])):
      if matriz[i][j]==1:
        x=(i*5)+1
        y=(j*5)+1
        oled.rect(x,y,4,4,1)
      else:
        x=(i*5)+1
        y=(j*5)+1
        oled.rect(x,y,4,4,0)
  
def validar_Obstaculo_Izquierda(cordX,cordY):
  try:
    if matriz[cordX-1][cordY]!=1 and cordX!=0:
      return True
  except:
    return False
  return False
def validar_Obstaculo_Derecha(cordX,cordY):
  try:
    if matriz[cordX+1][cordY]!=1:
      return True
  except:
    return False
  return False
def validar_Obstaculo_Arriba(cordX,cordY):
  try:
    if matriz[cordX][cordY-1]!=1 and cordY!=0:
      return True
  except:
    return False
  return False
def validar_Obstaculo_Abajo(cordX,cordY):
  try:
    if matriz[cordX][cordY+1]!=1:
      return True
  except:
    return False
  return False

def mover_Izquierda(coordenadaX, coordenadaY):
  matriz[coordenadaX][coordenadaY]=0
  matriz[coordenadaX-1][coordenadaY]=1
  return int(coordenadaX-1)
def mover_Derecha(coordenadaX, coordenadaY):
  matriz[coordenadaX][coordenadaY]=0
  matriz[coordenadaX+1][coordenadaY]=1
  return int(coordenadaX+1)
def mover_Arriba(coordenadaX, coordenadaY):
  matriz[coordenadaX][coordenadaY]=0
  matriz[coordenadaX][coordenadaY-1]=1
  return int(coordenadaY-1)
def mover_Abajo(coordenadaX, coordenadaY):
  matriz[coordenadaX][coordenadaY]=0
  matriz[coordenadaX][coordenadaY+1]=1
  return int(coordenadaY+1)

def Limite_Izquierda(objeto,linea):
  limite=-1
  for i in range(len(objeto)):
    if objeto[i][1]==linea and (objeto[i][0]<limite or limite==-1):
      limite=objeto[i][0]
  return limite
def Limite_Derecha(objeto,linea):
  limite=-1
  for i in range(len(objeto)):
    if objeto[i][1]==linea and (objeto[i][0]>limite or limite==-1):
      limite=objeto[i][0]
  return limite
def Limite_Arriba(objeto,linea):
  limite=-1
  for i in range(len(objeto)):
    if objeto[i][0]==linea and (objeto[i][1]<limite or limite==-1):
      limite=objeto[i][1]
  return limite
def Limite_Abajo(objeto,linea):
  limite=-1
  for i in range(len(objeto)):
    if objeto[i][0]==linea and (objeto[i][1]>limite or limite==-1):
      limite=objeto[i][1]
  return limite

def validar_Obstaculo_Objeto_Izquierda(objeto):
  for i in range(len(matriz[0])):
    Limite=Limite_Izquierda(objeto,i)
    if Limite!=-1 and validar_Obstaculo_Izquierda(Limite,i)==False:
      return False
  return True
def validar_Obstaculo_Objeto_Derecha(objeto):
  for i in range(len(matriz[0])):
    Limite=Limite_Derecha(objeto,i)
    if Limite!=-1 and validar_Obstaculo_Derecha(Limite,i)==False:
      return False
  return True
def validar_Obstaculo_Objeto_Arriba(objeto):
  for i in range(len(matriz)):
    Limite=Limite_Arriba(objeto,i)
    if Limite!=-1 and validar_Obstaculo_Arriba(i,Limite)==False:
      return False
  return True
def validar_Obstaculo_Objeto_Abajo(objeto):
  for i in range(len(matriz)):
    Limite=Limite_Abajo(objeto,i)
    if Limite!=-1 and validar_Obstaculo_Abajo(i,Limite)==False:
      return False
  return True

def mover_Objeto_Izquierda(objeto):
  for i in range(len(objeto)):
    objeto[i][0]=mover_Izquierda(objeto[i][0],objeto[i][1])
def mover_Objeto_Derecha(objeto):
  for i in range(len(objeto)):
    objeto[i][0]=mover_Derecha(objeto[i][0],objeto[i][1])
def mover_Objeto_Arriba(objeto):
  for i in range(len(objeto)):
    objeto[i][1]=mover_Arriba(objeto[i][0],objeto[i][1])
def mover_Objeto_Abajo(objeto):
  for i in range(len(objeto)):
    objeto[i][1]=mover_Abajo(objeto[i][0],objeto[i][1])

def imprimir_objeto(objeto,valor):
  for i in range(len(objeto)):
    matriz[objeto[i][0]][objeto[i][1]]=valor
def bajar_todo(lineaD):
  for i in range(lineaD+1,len(matriz)):
    for j in range(len(matriz[i])):
      if matriz[i][j]==1:
        mover_Izquierda(i,j)
def jirar_piesa(piesa,numpiesa):
  
  if numpiesa==0:
    print("intentaste jirar un cubo XD")
  elif (numpiesa==1 or numpiesa==2 or numpiesa==6) and piesa[0][0]-2>0:
    try:
      nouse=matriz[0][piesa[0][1]+2]
    except:
      return 0
    for i in range (1, len(piesa)):
      tempopiesa=getObjeto(piesa)
      matriz[piesa[i][0]][piesa[i][1]]=0

      if (tempopiesa[i][0]!=tempopiesa[0][0]) and (tempopiesa[i][1]!=tempopiesa[0][1]):
        if (tempopiesa[i][0]>tempopiesa[0][0] and tempopiesa[i][1]>tempopiesa[0][1]) or (tempopiesa[i][0]<tempopiesa[0][0] and tempopiesa[i][1]<tempopiesa[0][1]):
          piesa[i][0]=tempopiesa[0][0]-(tempopiesa[i][0]-tempopiesa[0][0])
        else:
          piesa[i][1]=tempopiesa[0][1]-(tempopiesa[i][1]-tempopiesa[0][1])
      else:
        if tempopiesa[i][0]!=tempopiesa[0][0]:
          piesa[i][0]=tempopiesa[0][0]
        else:

          piesa[i][0]=tempopiesa[0][0]+int(tempopiesa[0][1]-tempopiesa[i][1])
        if tempopiesa[i][1]!=tempopiesa[0][1]:
          piesa[i][1]=tempopiesa[0][1]
        else:
          piesa[i][1]=tempopiesa[0][1]-(tempopiesa[0][0]-tempopiesa[i][0])
      matriz[piesa[i][0]][piesa[i][1]]=1  
  elif (numpiesa==3 or numpiesa==4 or numpiesa==5) and piesa[0][0]-1>0:  
    try:
      nouse=matriz[0][piesa[0][1]+1]
    except:
      return 0
    for i in range (1, len(piesa)):
      tempopiesa=getObjeto(piesa)
      matriz[piesa[i][0]][piesa[i][1]]=0

      if (tempopiesa[i][0]!=tempopiesa[0][0]) and (tempopiesa[i][1]!=tempopiesa[0][1]):
        if (tempopiesa[i][0]>tempopiesa[0][0] and tempopiesa[i][1]>tempopiesa[0][1]) or (tempopiesa[i][0]<tempopiesa[0][0] and tempopiesa[i][1]<tempopiesa[0][1]):
          piesa[i][0]=tempopiesa[0][0]-(tempopiesa[i][0]-tempopiesa[0][0])
        else:
          piesa[i][1]=tempopiesa[0][1]-(tempopiesa[i][1]-tempopiesa[0][1])
      else:
        if tempopiesa[i][0]!=tempopiesa[0][0]:
          piesa[i][0]=tempopiesa[0][0]
        else:
          piesa[i][0]=tempopiesa[0][0]+int(tempopiesa[0][1]-tempopiesa[i][1])
        if tempopiesa[i][1]!=tempopiesa[0][1]:
          piesa[i][1]=tempopiesa[0][1]
        else:
          piesa[i][1]=tempopiesa[0][1]-(tempopiesa[0][0]-tempopiesa[i][0])
      matriz[piesa[i][0]][piesa[i][1]]=1 


def getObjeto(Objeto):
  lel=[]
  for i in range(len(Objeto)):
    lel.append([])
    for j in range(len(Objeto[0])):
      lel[i].append(Objeto[i][j])
  return lel

while True:

  for i in range(len(matriz)):
    point=True
    while point==True:
      for j in range(len(matriz[i])):
        if matriz[i][j]==0:
          point=False
      if point==True:
        for j in range(len(matriz[i])):
          matriz[i][j]=0
        bajar_todo(i)
      
  contador=0

  NumPiesa=random.randint(0, 6)

  if NumPiesa==0:
    piesa=getObjeto(cubo)
  elif NumPiesa==1:
    piesa=getObjeto(ele)
  elif NumPiesa==2:
    piesa=getObjeto(eleI)
  elif NumPiesa==3:
    piesa=getObjeto(rayo)
  elif NumPiesa==4:
    piesa=getObjeto(rayoI)
  elif NumPiesa==5:
    piesa=getObjeto(te)
  else:
    piesa=getObjeto(linea)

  reset=False

  while reset==False:

    velocidad=0.7

    if boton.value()==0:
      jirar_piesa(piesa,NumPiesa)

    imprimir_objeto(piesa,1)

    if contador==4 or ejex.read()>4000:
      contador=0
      if validar_Obstaculo_Objeto_Izquierda(piesa)==True:
        mover_Objeto_Izquierda(piesa)
      else:
        reset=True

    if ejey.read()>4000 and validar_Obstaculo_Objeto_Arriba(piesa)==True:
      mover_Objeto_Arriba(piesa)
    if ejey.read()<1000 and validar_Obstaculo_Objeto_Abajo(piesa)==True:
      mover_Objeto_Abajo(piesa)

    display()

    contador=contador+1

    oled.show()
    sleep(0.1)