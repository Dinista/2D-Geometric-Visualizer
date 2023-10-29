import tkinter as tk
import math
import sys
import os

from time import sleep

from tkinter import messagebox

import threading
##############################################################################################################
LARGURA = 1000
ALTURA = 580
ESPACAMENTOVERTICAL = ALTURA*0.10
ESPACAMENTOHORIZONTAL = LARGURA*0.135
OFFSETVERTICAL = ALTURA*0.20
OFFSETHORIZONTAL = LARGURA*0.17

##############################################################################################################
image = 0
poly = 3
click_fun = 1
click_stage = 0
ovais = []
lista_pontos = []
##############################################################################################################
def button_poly():
    btn_select.configure(relief='raised')
    btn_circle.configure(relief='raised')
    btn_transla.configure(relief='raised')
    btn_poly.configure(relief='sunken')
    global click_fun
    global lista_pontos
    global click_stage
    click_fun = "poly"
    click_stage = 0
    list_pontos_reset()

def button_select():
    btn_select.configure(relief='sunken')
    btn_circle.configure(relief='raised')
    btn_transla.configure(relief='raised')
    btn_poly.configure(relief='raised')
    global click_fun
    global lista_pontos
    global click_stage
    click_stage = 0
    click_fun = "select"
    list_pontos_reset()

def button_circle():
    btn_select.configure(relief='raised')
    btn_circle.configure(relief='sunken')
    btn_transla.configure(relief='raised')
    btn_poly.configure(relief='raised')
    global click_fun
    global lista_pontos
    global click_stage
    click_stage = 0
    click_fun = "circle"
    list_pontos_reset()

def button_transla():
    btn_select.configure(relief='raised')
    btn_circle.configure(relief='raised')
    btn_transla.configure(relief='sunken')
    btn_poly.configure(relief='raised')
    global click_fun
    global lista_pontos
    global click_stage
    click_stage = 0
    click_fun = "mover"
    list_pontos_reset()

##############################################################################################################
def motion(event):
    x, y = event.x, event.y
    mouseXY.configure(text= 'X = {} | Y = {}'.format(x,y))

def stage_reset():
    global click_stage
    click_stage = 0

def delete_ovais():
    global ovais
    while len(ovais) > 0:
        can.delete(ovais[0])
        ovais.pop(0)

def list_pontos_reset():
    global lista_pontos
    lista_pontos.clear()

##############################################################################################################
def click(event):
    if  click_stage == 0:
        delete_ovais()
        stage_reset()
    if click_fun == "poly":
        create_poly(event)
    elif click_fun == "select":
        select(event)
    elif click_fun == "circle":
        create_circle(event)
    elif click_fun == "mover":
        mover(event)

def motion_root(event):
    lista = listbox.get(0, tk.END)
    selecionados  = listbox.curselection()
    for i in  range(0,len(lista)):
        if listbox.get(tk.ACTIVE) == listbox.get(i):
            can.itemconfig(listbox.get(i), width = 2)
        else:
            can.itemconfig(listbox.get(i), width = 0, outline="black")
    for i in range(0, len(selecionados)):
        can.itemconfig(listbox.get(selecionados[i]), width = 2)
##############################################################################################################

def centroid(vertexes):
    _x_list = []
    _y_list = []
    for k in range(len(vertexes)):
        if k%2 == 0:
            _x_list.append(vertexes[k])
        else:
            _y_list.append(vertexes[k])

    _len = len(vertexes)/2
    _x = sum(_x_list) / _len
    _y = sum(_y_list) / _len
    return _x, _y


def button_plus():
    global poly
    poly += 1
    polyLabel.configure(text=poly)

def button_minus():
    global poly
    if poly > 2:
        poly -= 1
        polyLabel.configure(text=poly)

def button_clear():
    can.delete("all")
    listbox.delete(0,tk.END)

def button_delete():
    cur = listbox.curselection()
    for i in range(len(cur)-1,-1,-1):
        can.delete(listbox.get(cur[i]))
        listbox.delete(cur[i])

def button_rotacao():
    id = listbox.get(tk.ACTIVE)
    cord = can.coords(id)
    aux = []
    angle = int(rotate.get())
    x = []
    y = []
    center_x, center_y = centroid(cord)
    for i in range(0, len(cord), 2):
        x.append(cord[i])
    for i in range(1, len(cord), 2):
        y.append(cord[i])
    for i in range (len(x)):
        x[i] -= center_x
        y[i] -= center_y
        aux.append(x[i] * math.cos(math.radians(angle)) - y[i] * math.sin(math.radians(angle)))
        aux.append(x[i] * math.sin(math.radians(angle)) + y[i] * math.cos(math.radians(angle)))
    for t in range(len(aux)):
        if t%2 == 0:
            aux[t] += center_x
        else: aux[t] += center_y

    can.coords(id, aux)


def button_escala():
    id = listbox.get(tk.ACTIVE)
    cord  = can.coords(id)
    x = []
    y = []
    for i in range(0,len(cord),2):
        x.append(cord[i])
    for i in range(1,len(cord),2):
        y.append(cord[i])
    center = [(max(x)+min(x))/2,(max(y) + min(y))/2]
    can.scale(id, center[0], center[1], escala.get(), escala.get())

def button_zoom_extent():
    id = listbox.get(tk.ACTIVE)
    cord = can.coords(id)
    x = []
    y = []
    for i in range(0, len(cord), 2):
        x.append(cord[i])
    for i in range(1, len(cord), 2):
        y.append(cord[i])
    center = [(max(x) + min(x)) / 2, (max(y) + min(y)) / 2]
    can.move(tk.ALL, LARGURA*0.35 - center[0], ALTURA*0.35 - center[1])

    a = LARGURA*0.7/(max(x) - min(x))
    b = ALTURA*0.7/(max(y) - min(y))
    if a > b:
        z = b
    else:
        z = a

    objetos = listbox.get(0, tk.END)

    for j in range(0, len(objetos)):
        id = objetos[j]
        cord = can.coords(id)
        x = []
        y = []
        for i in range(0, len(cord), 2):
            x.append(cord[i])
        for i in range(1, len(cord), 2):
            y.append(cord[i])
        center = [(max(x) + min(x)) / 2, (max(y) + min(y)) / 2]
        can.scale(id, LARGURA*0.35, ALTURA*0.35, z, z)


def button_zoom():
    objetos = listbox.get(0,tk.END)
    for j in range(0,len(objetos)):
        print(j)
        id = objetos[j]
        print(id)
        cord = can.coords(id)
        print(cord)
        x = []
        y = []
        i = 0
        for i in range(0, len(cord), 2):
            x.append(cord[i])
        for i in range(1, len(cord), 2):
            y.append(cord[i])
        center = [(max(x) + min(x)) / 2, (max(y) + min(y)) / 2]
        can.scale(id, LARGURA*0.35, ALTURA*0.35, zoom.get(), zoom.get())

##############################################################################################################

def select(event):
    id = can.find_closest(event.x, event.y)
    for i in range(listbox.size()):
        if id == listbox.get(i):
            listbox.activate(i)
            listbox.see(i)

def create_poly(event):
    global ovais
    global click_stage
    lista_pontos.append([event.x, event.y])
    ovais.append(can.create_oval(event.x + 4, event.y, event.x, event.y + 4, fill='black') )
    click_stage += 1
    if click_stage == poly:
        delete_ovais()
        listbox.insert(tk.END, [can.create_polygon(lista_pontos, fill="white", outline="black")])
        list_pontos_reset()
        stage_reset()

def create_circle(event):
    global ovais
    global click_stage
    lista_pontos.append([event.x, event.y])
    ovais.append(can.create_oval(event.x + 4, event.y, event.x, event.y + 4, fill='black'))
    click_stage += 1
    aux = []
    if click_stage == 2:
        x1 = lista_pontos[0][0]
        y1 = lista_pontos[0][1]
        x2 = lista_pontos[1][0]
        y2 = lista_pontos[1][1]
        r = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)/2
        middleX = (x1+x2)/2
        middleY = (y1+y2)/2
        print(r)
        pontos = get_points(r, 1000)
        for x in pontos:
            new_x = x[0] + middleX
            new_y = x[1] + middleY
            t = (new_x, new_y)
            aux.append(t)
        delete_ovais()
        listbox.insert(tk.END, [can.create_polygon(aux, fill = "white", outline="black", outlineoffset = 90)])
        list_pontos_reset()
        stage_reset()

def get_points(radius, number_of_points):
    radians_between_each_point = 2*math.pi/number_of_points
    list_of_points = []
    for p in range(0, number_of_points):
        list_of_points.append( (radius*math.cos(p*radians_between_each_point),radius*math.sin(p*radians_between_each_point)) )
    return list_of_points

def mover(event):
    id = listbox.get(tk.ACTIVE)
    cord  = can.coords(id)
    x = []
    y = []
    for i in range(0,len(cord),2):
        x.append(cord[i])
    for i in range(1,len(cord),2):
        y.append(cord[i])
    center = [(max(x)+min(x))/2,(max(y) + min(y))/2]
    can.move(id,event.x - center[0], event.y - center[1])
##############################################################################################################

root = tk.Tk()
root.title('Sistema de visualização')
root.resizable(width=False, height=False)
root.geometry("%dx%d" % (LARGURA, ALTURA))
root.configure(bg='light grey')

base_folder = os.path.dirname(__file__)
icon_path = os.path.join(base_folder, 'Img/unnamed.ico')

root.iconbitmap(icon_path)

##############################################################################################################
def quit(self):
    self.destroy()


def ajuda(op):
    ajuda = tk.Tk()
    ajuda.resizable()
    ajuda.geometry( '%dx%d+%d+%d' % (300, 300, 350, 80))
    ajuda.configure(bg='light grey')

    ajuda_can = tk.Canvas(ajuda, bg='light grey', height = 250, width= 300, highlightthickness= 0,
              highlightbackground="black")

    ajuda_can.place( x = 3, y = -1)
    ajuda_can.pack()

    if op == "Desenhos":
        ajuda.title('Desenhos')
        ajuda_can.create_text(150, 125, text = "• Para realizar os desenhos com pontos, você deve\n   selecionar "
                                            "o botão polígono e definir o número\n   de pontos "
                                            "que ele terá (exemplos):\n       - 4 pontos: Quadrado\n       - 3 pontos: Triângulo\n       - 2 pontos: Reta\n   "
                                             "Selecionando a quatidade de pontos, você pode\n   criar qualquer polígono. Basta, com o mouse\n   "
                                             "(botão esquerdo), criar os pontos na tela.\n\n"
                                             "• Para fazer um círculo, é necessário selecionar\n   "
                                             "o botão Círculo, e definir com o mouse\n  (botão esquerdo) o tamanho, no canvas.")

    if op == "Seleção":
        ajuda.title('Seleção')
        ajuda_can.create_text(150, 125, text = "• O botão 'Select' serve para escolher, na tela e\n   com o mouse (botão esquerdo), o desenho \n   que você deseja operar.\n\n"
                                            "• Quando uma forma está selecionada, o contorno\n   da mesma fica mais grosso.\n   "
                                             "Assim é possível diferenciar qual desenho está \n   selecionado e qual não está. \n   ")

    if op == "Deletar":
        ajuda.title('Deletar')
        ajuda_can.create_text(150, 125, text = "• O botão 'Deletar' permite excluir uma forma\n   geométrica que está no canvas.\n\n   "
                                            "   - Primeiro você deve selecionar a forma,\n      para depois deletá-la.\n\n      - A forma precisa estar selecionada"
                                            "\n      na caixa de seleção 'Formas.'")

    if op == "Translação":
        ajuda.title('Translação')
        ajuda_can.create_text(150, 125, text = "    • O botão 'Translação' moverá o desenho\n       selecionado para a posição clicada no canvas. \n\n   "
                                            "    - Primeiro selecione a forma geométrica.\n\n"
                                            "      - Clique no botão 'Translação'.\n\n"
                                            "      - Clique no lugar que deseja mover seu objeto'.\n\n"
                                            "       Dessa forma é possível diferenciar qual desenho\n       está selecionado e qual não está. \n   ")


    if op == "Formas":
        ajuda.title('Formas')
        ajuda_can.create_text(150, 125, text = "• A caixa de seleção 'Formas' serve para selecionar\n   um dos desenhos contidos no canvas.\n\n"
                                            "• Os rótulos de cada desenho, são seus identificadores.\n\n"
                                            "• Quando uma forma/desenho está selecionada, \n   o contorno da mesma fica mais grosso.\n   "
                                             "Dessa forma é possível diferenciar qual desenho\n   está selecionado e qual não está. \n   ")


    botao_ajuda = tk.Button(ajuda, text='Fechar', width=int(LARGURA * 0.01), command = lambda: quit(ajuda))
    botao_ajuda.place(x=250, y=350)
    botao_ajuda.pack()

My_Menu =  tk.Menu(root)
ajudamenu = tk.Menu(root, tearoff = 0)
My_Menu.add_cascade(label = 'Ajuda', menu = ajudamenu)
ajudamenu.add_command(label="Seleção", command = lambda: ajuda('Seleção'))
ajudamenu.add_command(label="Desenhos", command = lambda: ajuda('Desenhos'))
ajudamenu.add_command(label="Deletar", command = lambda: ajuda('Deletar'))
ajudamenu.add_separator()
ajudamenu.add_command(label="Translação", command = lambda: ajuda('Translação'))
ajudamenu.add_command(label="Formas", command = lambda: ajuda('Formas'))
ajudamenu.add_separator()
ajudamenu.add_command(label="Sair", command = lambda: quit(root))


root.config(menu = My_Menu)

##############################################################################################################


btn_select = tk.Button(root, text='Select', width=int(LARGURA*0.01), command = button_select)
btn_select.pack()
btn_select.place(x = LARGURA*0.03, y= OFFSETVERTICAL + 0*ESPACAMENTOVERTICAL)

btn_poly = tk.Button(root, text='Polígono', width= int(LARGURA*0.01), command = button_poly)
btn_poly.pack()
btn_poly.place(x = LARGURA*0.03, y= OFFSETVERTICAL + 1*ESPACAMENTOVERTICAL)

btn_circle = tk.Button(root, text='Círculo', width=int(LARGURA*0.01), command = button_circle)
btn_circle.pack()
btn_circle.place(x = LARGURA*0.03, y= OFFSETVERTICAL + 2.8*ESPACAMENTOVERTICAL)

btn_delete = tk.Button(root, text='Deletar', width= int(LARGURA*0.01), command = button_delete)
btn_delete.pack()
btn_delete.place(x = LARGURA*0.03, y = OFFSETVERTICAL + 3.8*ESPACAMENTOVERTICAL)

btn_plus = tk.Button(root, text='⯅', width= 1, height = 0, font = 'Arial, 7 bold', command = button_plus, borderwidth = 1, relief = 'ridge')
btn_plus.pack()
btn_plus.place(x = LARGURA*0.03, y = OFFSETVERTICAL + 1.85*ESPACAMENTOVERTICAL)

btn_minus = tk.Button(root, text ='⯆', font = ('Arial, 7 bold'),  height = 0, width = 1, command = button_minus, borderwidth = 1, relief = 'ridge')
btn_minus.pack()
btn_minus.place(x = LARGURA*0.03, y = OFFSETVERTICAL + 2.15*ESPACAMENTOVERTICAL)


##############################################################################################################


btn_clear = tk.Button(root, text='Clear', width=int(LARGURA*0.015), command=button_clear)
btn_clear.pack()
btn_clear.place(x = OFFSETHORIZONTAL + 0*ESPACAMENTOHORIZONTAL, y = ALTURA*0.09)

btn_rotacao = tk.Button(root, text='Rotação', width=int(LARGURA*0.015), command = button_rotacao)
btn_rotacao.pack()
btn_rotacao.place(x = OFFSETHORIZONTAL + 1*ESPACAMENTOHORIZONTAL, y = ALTURA*0.09)

btn_escala = tk.Button(root, text='Mudança de Escala', width= int(LARGURA*0.015), command = button_escala)
btn_escala.pack()
btn_escala.place(x = OFFSETHORIZONTAL + 2*ESPACAMENTOHORIZONTAL, y = ALTURA*0.09)

btn_zoom_extent = tk.Button(root, text='Zoom extent', width= int(LARGURA*0.015), command = button_zoom_extent)
btn_zoom_extent.pack()
btn_zoom_extent.place(x = OFFSETHORIZONTAL + 3*ESPACAMENTOHORIZONTAL, y = ALTURA*0.0001)

btn_zoom = tk.Button(root, text='Zoom', width= int(LARGURA*0.015), command = button_zoom)
btn_zoom.pack()
btn_zoom.place(x = OFFSETHORIZONTAL + 3*ESPACAMENTOHORIZONTAL, y = ALTURA*0.09)

btn_transla = tk.Button(root, text='Translação', width= int(LARGURA*0.015), command= button_transla)
btn_transla.pack()
btn_transla.place(x = OFFSETHORIZONTAL + 4*ESPACAMENTOHORIZONTAL, y = ALTURA*0.09)

##############################################################################################################

text_rotacao = tk.Label(root, text= "Ângulo:", font = "Arial 8", bg = 'light grey')
text_rotacao.pack()
text_rotacao.place(x = OFFSETHORIZONTAL + 1*ESPACAMENTOHORIZONTAL, y = ALTURA*0.05)

text_obj = tk.Label(root, text= "Formas:", font = "Arial 8", bg = 'light grey')
text_obj.pack()
text_obj.place(x= LARGURA*0.86, y = ALTURA*0.07)

text_escala = tk.Label(root, text= "Escala:", font = "Arial 8", bg = 'light grey')
text_escala.pack()
text_escala.place(x = OFFSETHORIZONTAL + 2*ESPACAMENTOHORIZONTAL, y = ALTURA*0.05)

text_zoom = tk.Label(root, text= "Escala:", font = "Arial 8", bg = 'light grey')
text_zoom.pack()
text_zoom.place(x = OFFSETHORIZONTAL + 3*ESPACAMENTOHORIZONTAL, y = ALTURA*0.05)

text_poly = tk.Label(root, text= "Quantidade de pontos:", font = "Arial 8", bg = 'light grey')
text_poly.pack()
text_poly.place(x = LARGURA*0.03, y= OFFSETVERTICAL + 1.50*ESPACAMENTOVERTICAL)

polyLabel = tk.Label(root, text = poly)
polyLabel.place(x = LARGURA*0.05, y= OFFSETVERTICAL + 1.95*ESPACAMENTOVERTICAL)

mouseXY = tk.Label(root, text=[-1,-1])
mouseXY.place(x = LARGURA*0.03, y = ALTURA*0.9)

listbox = tk.Listbox(root, selectmode=tk.EXTENDED)
listbox.pack()
listbox.place(x= LARGURA*0.86, y = ALTURA*0.1)


##############################################################################################################
rotate = tk.Entry(root)
rotate.pack
rotate.place(x = OFFSETHORIZONTAL + 1.32*ESPACAMENTOHORIZONTAL, y = ALTURA*0.05, width= LARGURA*0.07)
rotate.insert(0, 30)


escala = tk.Entry(root)
escala.pack
escala.place(x = OFFSETHORIZONTAL + 2.32*ESPACAMENTOHORIZONTAL, y = ALTURA*0.05, width= LARGURA*0.07)
escala.insert(0, 1.5)


zoom = tk.Entry(root)
zoom.pack
zoom.place(x = OFFSETHORIZONTAL + 3.32*ESPACAMENTOHORIZONTAL, y = ALTURA*0.05, width= LARGURA*0.07)
zoom.insert(0, 1.5)

##############################################################################################################

base_folder = os.path.dirname(__file__)
image_path = os.path.join(base_folder, 'Img/3d-shape.png')
photo = tk.PhotoImage(file=image_path)

image = tk.Label(root, image = photo, bg= 'light grey')
image.place(x = 30, y = 15)


image_path2 = os.path.join(base_folder, 'Img/Cursor-Select-icon.png')
photo1 = tk.PhotoImage(file=image_path2)

image1 = tk.Label(root, image = photo1, bg= 'light grey')
image1.place(x = LARGURA*0.12, y= OFFSETVERTICAL + 0.08*ESPACAMENTOVERTICAL)

image_path3 = os.path.join(base_folder, 'Img/draw_a_polygon_.png')
photo2 = tk.PhotoImage(file=image_path3)

image2 = tk.Label(root, image = photo2, bg= 'light grey')
image2.place(x = LARGURA*0.12, y= OFFSETVERTICAL + 1.05*ESPACAMENTOVERTICAL)

image_path4 = os.path.join(base_folder, 'Img/08-512.png')
photo3 = tk.PhotoImage(file = image_path4)

image3 = tk.Label(root, image = photo3, bg= 'light grey')
image3.place(x = LARGURA*0.12, y= OFFSETVERTICAL + 2.85*ESPACAMENTOVERTICAL)

image_path5 = os.path.join(base_folder, 'Img/img_89283.png')
photo4 = tk.PhotoImage(file = image_path5)

image4 = tk.Label(root, image = photo4, bg= 'light grey')
image4.place(x = LARGURA*0.12, y= OFFSETVERTICAL + 3.85*ESPACAMENTOVERTICAL)

##############################################################################################################

can = tk.Canvas(root, bg='white', height = ALTURA*0.7, width = LARGURA*0.7, highlightthickness= 1, highlightbackground="black")
can.pack()
can.place(x = LARGURA*0.15, y = ALTURA*0.15)


can.bind('<Motion>', motion)
can.bind('<1>', click)

root.bind('<Motion>', motion_root)

can.itemconfig(listbox.get(tk.ACTIVE), fill = "white")
can.itemconfig(listbox.get(tk.ACTIVE), fill = "yellow")

root.mainloop()