import tkinter as tk
import requests
import threading
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

m = tk.Tk()
m.title('Postman')

# =========================== LABELS ===========================

Label(m, text='URL', width=14, anchor='e').grid(row=0,column=0)
Label(m, text='CONCURRENCIA', width=14, anchor='e').grid(row=1,column=0)
Label(m, text='SOLICITUDES', width=14, anchor='e').grid(row=2,column=0)
Label(m, text='ARCHIVO', width=14, anchor='e').grid(row=3,column=0)
Label(m, text='TIMEOUT (MINS)', width=14, anchor='e').grid(row=4,column=0)
Label(m, text='ESTADO', width=14, anchor='e').grid(row=5,column=0)
Label(m, text='RESUMEN', width=14, anchor='e').grid(row=6,column=0)

# =========================== INPUTS ===========================

dir = Entry(m,width=63)
dir.insert(tk.END,'http://35.209.204.71:8080/api/tweet')
dir.grid(row=0,column=1, columnspan=2)
concurrencia = Spinbox(m,from_=1,to=2147483647, width=61)
concurrencia.grid(row=1,column=1, columnspan=2)
solicitudes = Spinbox(m,from_=1,to=2147483647, width=61)
solicitudes.grid(row=2,column=1, columnspan=2)
archivo = Entry(m,width=50)
archivo.insert(tk.END,'/Users/dennis/Documents/Python_postman/example.txt')
archivo.grid(row=3,column=1)
timeout = Spinbox(m,from_=1,to=2147483647, width=61)
timeout.grid(row=4,column=1, columnspan=2)
estado = Entry(m,width=50)
estado.insert(tk.END,'ESPERA')
estado.grid(row=5,column=1)
resumen = Text(m, width=62,height=6,borderwidth=2, relief="groove")
resumen.grid(row=7, column=1)

# =========================== OPEN FILE ===========================

def openFile():
    m.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (('text files','*.txt'),('all files','*.*')))
    archivo.insert(0,m.filename)

button = tk.Button(m,text='Buscar', width=9, command=openFile)
button.grid(row=3,column=2)

# =========================== GET REQUEST ===========================

def make_get_request():
    resumen.insert(tk.END,'Resumen de ejecucion:\n\n')
    resumen.insert(tk.END,'Tiempo de Inicio: ')
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    resumen.insert(tk.END,current_time)
    resumen.insert(tk.END,'\n')
    for l in range(int(concurrencia.get())):
        x = threading.Thread(target=threaded_request)
        x.start()
    resumen.insert(tk.END,'\n')
    resumen.insert(tk.END,'\n')
    resumen.insert(tk.END,'Tiempo de finalizado:')
    now2 = datetime.now()
    current_time2 = now2.strftime('%H:%M:%S')
    resumen.insert(tk.END,current_time2)
    resumen.insert(tk.END,'\n')

def threaded_request():
    file = open(archivo.get(), 'r')
    list = file.readlines()
    requests_count = int(solicitudes.get())
    while requests_count >0:
        for l in list:
            splitted_list = l.split(';')
            usr = (splitted_list[0].split('&')[0]).split('=')[1]
            nom = (splitted_list[1].split('&')[0]).split('=')[1]
            txt = splitted_list[2].split('=')[1]
            txt_without_hashtag = (txt.replace("#", "")).replace('\n','')
            hashtag = txt.split('#', maxsplit=1)[-1].split(maxsplit=1)[0]
            PARAMS = {'usr':usr,'nom':nom,'txt':txt,'tag':hashtag}
            URL = dir.get()
            r = requests.get(url = URL,params=PARAMS)
            resumen.insert(tk.END,r.json())
            requests_count = requests_count-1
        #resumen.insert(tk.END,'usr='+usr+'\nnom='+nom+'\ntxt='+txt_without_hashtag+'\ntag='+hashtag+'\n\n')

exec_button = Button(m,text='Ejecutar', width=9, command=make_get_request)
exec_button.grid(row=5,column=2)

m.mainloop()
