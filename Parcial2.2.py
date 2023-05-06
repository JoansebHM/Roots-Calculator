import tkinter
from tkinter import font as tkfont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
import numpy as np
import sympy 
import matplotlib.image as mpimg 
from reportlab.pdfgen import canvas as cv
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

ventana = tkinter.Tk()
ventana.geometry('800x900')
ventana.resizable(True,True)
ventana.title('Find the root')
ventana.config()
fuenteTitulo = tkfont.Font(family="Courier New Baltic", size=20)
fuenteNormal = tkfont.Font(family="Courier New Baltic", size=12)
fuentesubtitulos = tkfont.Font(family="Courier New Baltic", size=12, weight='bold')

MainLeftFrame = tkinter.Frame(ventana)
MainLeftFrame.pack(side=tkinter.LEFT)

def plot():
    if(EntradaFuncion.get() != ''):
        formula = EntradaFuncion.get()
        graph(formula)        
    
img = mpimg.imread('./escudo-pascual-bravo_Mesa-de-trabajo-1.jpg')
fig = Figure(figsize=(5, 5))
ax = fig.add_subplot(111)
ax.axhline(0, color='black', lw=1)
ax.axvline(0, color='black', lw=1)
ax.set_title(f'Gráfico', fontdict={'fontsize': 12, 'fontweight': 'bold'})
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.imshow(img,extent=[-10, 10, -10, 10], aspect='auto', alpha=0.3)

canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(side=tkinter.RIGHT, ipady=100, expand=True)
canvas.get_tk_widget().place(x=320,y=60)


def graph(formula):
    x = np.linspace(-500, 500, 10000)
    y = eval(formula)
    ax.clear()
    ax.plot(x, y, color='blue')
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.set_title(f'Gráfico', fontdict={'fontsize': 12, 'fontweight': 'bold'})
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.imshow(img,extent=[-10, 10, -10, 10], aspect='auto', alpha=0.3)
    canvas.draw()

def Resolver():
        if(intch1.get()==1):
            entradaNewton["text"] = encontrarRaices('Newton')
        else:
            entradaNewton["text"] = '...'     
        if(intch2.get()==1):
            entradaSecante["text"] = encontrarRaices2('secante')
        else:
            entradaSecante["text"] = '...'            
        if(intch3.get()==1):
            entradaSteffensen["text"] = encontrarRaices('steffensen')
        else:
            entradaSteffensen["text"] = '...'  
        if(intch4.get()==1):
            entradaTanteo["text"] = encontrarRaices('tanteo')
        else:
            entradaTanteo['text'] = '...'
        if(intch5.get()==1):
            entradaBiseccion['text'] = encontrarRaices2('biseccion')
        else:
            entradaBiseccion['text'] = '...'
        if(intch6.get()==1):
            entradaReglaFalsa['text'] = encontrarRaices2('regla falsa')
        else:
            entradaReglaFalsa['text'] = '...'

def tanteo(x0):
    i = 0
    tolerance=0.1
    max_iterations=5000
    fun = EntradaFuncion.get()
    Fx0 = str(eval(fun, {'x': x0}))
    while i < max_iterations:
        if(abs(eval(Fx0))<=tolerance):
            break
        if(eval(Fx0)>0):
            if(x0 > 0):
                x1 = x0 - 0.002
                x0 = x1
                Fx0 = str(eval(fun, {'x': round(x0,2)}))
                if((abs(eval(Fx0)))<=tolerance):
                    break
            else:
                x1 = x0 + 0.002
                x0 = x1
                Fx0 = str(eval(fun, {'x': round(x0,2)}))
                if(eval(Fx0)<=tolerance):
                    break
        else:
            if (eval(Fx0))>0:
                x1 = x0 - 0.002
                x0 = x1
                Fx0 = str(eval(fun, {'x': round(x0,2)}))
                if(eval(Fx0)<=tolerance):
                    break
            else:
                if (eval(Fx0))<0:
                    x1 = x0 + 0.002
                    x0 = x1
                    Fx0 = str(eval(fun, {'x': round(x0,2)}))
                    if(abs(eval(Fx0))<=tolerance):
                        break
        i += 1
    if(abs(eval(Fx0))<=(tolerance)):
        return round(x0,2), i
    else:
        return None, i      


def biseccion(a, b):
    tol = 0.1
    fun = EntradaFuncion.get()
    Fxa = str(eval(fun, {'x': a}))
    Fxb = str(eval(fun, {'x': b}))
    if eval(Fxa)*eval(Fxb) > 0:
        return None, 0
    m = (a + b) / 2
    Fxm = str(eval(fun, {'x': m}))
    count = 0
    while count <= 500:
        if eval(Fxa)*eval(Fxm) < 0:
            b = m
        else:
            a = m
        m = (a + b) / 2
        Fxm = str(eval(fun, {'x': m}))        
        count += 1
        if abs(eval(Fxm)) <= tol:
            return round(m,2), count
    return None, count


def ReglaFalsa(a,b):
    fun = EntradaFuncion.get()
    Fxa = str(eval(fun, {'x': a}))
    Fxb = str(eval(fun, {'x': b}))
    if(eval(Fxa) == eval(Fxb)):
        return None, 0
    m= a - (eval(Fxa)*(b-a))/(eval(Fxb)-eval(Fxa))
    Fxm = str(eval(fun, {'x': m}))
    MargenError = 0.0001
    if(eval(Fxa) * eval(Fxb) > 0):
        return None, 0
    if(abs(eval(Fxm)<= MargenError)):     
        return round(m,2), 1
    else:
        counter=0
        while(counter<= 500):
            counter = counter+1
            if(abs(eval(Fxm)) <= MargenError):
                return round(m,2), counter
                break
            else:
                if((eval(Fxa)*eval(Fxb))<0):
                    b=m
                    Fxb = str(eval(fun, {'x': b}))
                else:
                    a=m
                    Fxa = str(eval(fun, {'x': a}))
                if(abs(eval(Fxm))<=MargenError):
                    return round(m,2), counter
                    break
                m= a - (eval(Fxa)*(b-a))/(eval(Fxb)-eval(Fxa))
                Fxm = str(eval(fun, {'x': m}))
        return None, counter

    
def NewtonRaphson(x0):
    if(EntradaDerivada.get()=='Derivada...'):
        messagebox.showinfo(message="Debes ingresar la derivada", title="Invalid input") 
        return 'exit'
    def fp(x):
        fun = EntradaDerivada.get()
        derivada = str(eval(fun, {'x': x}))
        return eval(derivada)   
    counter = 0
    max_iter = 100
    fun = EntradaFuncion.get()
    fx0 = str(eval(fun, {'x': x0}))
    while counter <= max_iter:
        if(x0 == 0):
            counter +=1
            if(abs(eval(fx0)) <= 0.00001):
                return round(x0,2), counter
                break  
        p = eval(fx0)
        pp = fp(x0)
        if(pp==0):
            return None,0
        x1 = x0 - ((p)/(pp))
        fx1 = str(eval(fun, {'x': x1}))
        if(abs(eval(fx1)) <= 0.00001):
            return round(x1,2), counter
            break
        else:
            x0 = x1
            fx0 = str(eval(fun, {'x': x0}))
    return None, counter

def steffensen( x0 ):
    max_iter=500
    counter = 0
    x1 = x0
    Fun = EntradaFuncion.get()
    Fx0 = str(eval(Fun, {'x': x0}))
    while counter <= max_iter:
        Fdeno = str(eval(Fun, {'x': (x0 + eval(Fx0))}))
        denominador = (eval(Fdeno) - eval(Fx0))
        if denominador == 0:
            break
        else:
            x1 = x0 - eval(Fx0)**2 / denominador
        x0 = x1
        Fx0 = str(eval(Fun, {'x': x0}))
        counter += 1
    if(abs(eval(Fx0)) <= 0.1):
        return round(x0,2), counter
    else:
        return None, counter
def MetodoSecante(a,b):
    def fp(a,b):
        Fun = EntradaFuncion.get()
        Fxa = str(eval(Fun, {'x': a}))
        Fxb = str(eval(Fun, {'x': b}))
        if eval(Fxa) == eval(Fxb):
            return None
        denom = eval(Fxa) - eval(Fxb)
        if denom == 0:
            return None
        return a - (eval(Fxa)*(a-b)/denom)
    
    Fun = EntradaFuncion.get()
    c = fp(a,b)
    if c is None:
        return None,0
    Fxc = str(eval(Fun, {'x': float(c)}))
    Fxa = str(eval(Fun, {'x': a}))
    Fxb = str(eval(Fun, {'x': b}))
    cont=0
    while cont <= 500:
        cont += 1
        if abs(eval(Fxc)) <= 0.001:
            return round(c,2),cont
        elif eval(Fxa) * eval(Fxb) < 0:
            b = c
            c = fp(a,b)
            if c is None:
                return None, cont
            Fxc = str(eval(Fun, {'x': float(c)}))
            Fxb = str(eval(Fun, {'x': b}))
        else:
            a = c
            c = fp(a,b)
            if c is None:
                return None, cont
            Fxa = str(eval(Fun, {'x': a}))
            Fxc = str(eval(Fun, {'x': float(c)}))
    return None, cont


def encontrarRaices(metodo):
    a = -10
    raices = []
    iteraciones= []
    while a <= 10:
        if metodo == 'steffensen':
            resul, count = steffensen(a)
        elif metodo == 'tanteo':
            resul, count = tanteo(a)
        elif metodo == 'Newton':
             resul, count = NewtonRaphson(a)
             if(resul=='exit'):
                 break
        if(resul == None):
            iteraciones.append(count)
            a = a + 0.5
        else:
            raices.append(resul)
            iteraciones.append(count)
            if(resul in raices):
                a = a + 0.5
                
    numeros_sin_repetidos = []
    for numero in raices:
        numero_redondeado = round(numero, 2)
        if not any(round(num, 2) == numero_redondeado for num in numeros_sin_repetidos):
            numeros_sin_repetidos.append(numero)
    if iteraciones:
        TotalIteraciones = sum(iteraciones)
        return f'{sorted(numeros_sin_repetidos)} => {round(TotalIteraciones, 2)} Iteraciones'
    else:
        return 'No se encontraron raíces para este método.'


def encontrarRaices2(metodo):
    a = -10
    b = -9
    raices = []
    iteraciones = []
    while a <= 10:
        if metodo == 'biseccion':
            resul, count = biseccion(a, b)
        elif metodo == 'regla falsa':
            resul, count = ReglaFalsa(a, b)
        elif metodo == 'secante':
            resul, count = MetodoSecante(a, b)
        if resul == None:
            iteraciones.append(count)
            a = a + 0.5
            b += 0.5
        else:
            raices.append(resul)
            iteraciones.append(count)
            if resul in raices:
                a = a + 0.5
                b += 0.5
                
    numeros_sin_repetidos = []
    for numero in raices:
        numero_redondeado = round(numero, 2)
        if not any(round(num, 2) == numero_redondeado for num in numeros_sin_repetidos):
            numeros_sin_repetidos.append(numero)
    if iteraciones:
        Totaliteraciones = sum(iteraciones) 
        return f'{sorted(numeros_sin_repetidos)} => {round(Totaliteraciones, 2)} Iteraciones'
    else:
        return 'No se encontraron raíces para este método.'


lblIngreseFuncion = tkinter.Label(MainLeftFrame, text='Ingrese La funcion')
lblIngreseFuncion.config(font=fuenteTitulo)
EntradaFuncion = tkinter.Entry(MainLeftFrame, border=5)
EntradaFuncion.config(font=fuenteNormal)
EntradaDerivada = tkinter.Entry(MainLeftFrame, border=4)
EntradaDerivada.config(font=fuenteNormal)
lblIngreseFuncion.pack()
EntradaFuncion.pack(pady=10)


def calcular_derivada():
    funcion = EntradaFuncion.get()
    x = sympy.symbols('x')
    expresion = sympy.sympify(funcion)
    derivada = sympy.diff(expresion, x)
    EntradaDerivada.delete(0, 'end') 
    EntradaDerivada.insert(0, str(derivada))


def DerivadaNewton():
    if intch1.get()==1:
        EntradaDerivada.pack(before=Marcoseleccion)
        calcular_derivada()
    else:
        EntradaDerivada.pack_forget()
        EntradaDerivada.delete(0,'end')



intch1 = tkinter.IntVar()
intch2 = tkinter.IntVar()
intch3 = tkinter.IntVar()
intch4 = tkinter.IntVar()
intch5 = tkinter.IntVar()
intch6 = tkinter.IntVar()


Marcoseleccion = tkinter.LabelFrame(MainLeftFrame, text='Metodos', font=fuentesubtitulos)
Marcoseleccion.pack( pady=15, padx=15)
Frameizquierdo = tkinter.Frame(Marcoseleccion)
FrameDerecho = tkinter.Frame(Marcoseleccion)
chbtnNewton = tkinter.Checkbutton(Frameizquierdo, text='Newton Raphson', font=fuenteNormal, variable=intch1, command=DerivadaNewton)
chbtnNewton.pack(anchor='w', side='top')
chbtnSecante = tkinter.Checkbutton(Frameizquierdo, text='Secante', font=fuenteNormal, variable=intch2)
chbtnSecante.pack(anchor='w', side='top')
chbtnSteffenson = tkinter.Checkbutton(Frameizquierdo, text='Steffensen',font=fuenteNormal, variable=intch3)
chbtnSteffenson.pack(anchor='w', side='top')
chbtnTaneo = tkinter.Checkbutton(FrameDerecho, text='Tanteo', font=fuenteNormal, variable=intch4)
chbtnTaneo.pack(anchor='w',  side='top')
chbtnBiseccion = tkinter.Checkbutton(FrameDerecho, text='Biseccion', font=fuenteNormal, variable=intch5)
chbtnBiseccion.pack(anchor='w',  side='top')
chbtnReglaFalsa = tkinter.Checkbutton(FrameDerecho, text='Regla Falsa',font=fuenteNormal, variable=intch6)
chbtnReglaFalsa.pack(anchor='w', side='top')

Frameizquierdo.pack(side=tkinter.LEFT, padx=5)
FrameDerecho.pack(side=tkinter.RIGHT)

btnVerificar = tkinter.Button(MainLeftFrame, text="Resolver", font=fuenteNormal, command=Resolver)
btnVerificar.pack()


marcoNewton = tkinter.LabelFrame(MainLeftFrame, text="Newton Raphson", font=fuentesubtitulos)
marcoNewton.pack(padx=15, pady=15)
entradaNewton = tkinter.Label(marcoNewton, 
                border=4,
                width=30,
                font=fuenteNormal,
                text=f'...',
                anchor='w'
                )

marcoSecante = tkinter.LabelFrame(MainLeftFrame, text="Secante", font=fuentesubtitulos)
marcoSecante.pack(padx=15, pady=15)
entradaSecante = tkinter.Label(marcoSecante, 
                border=4,
                width=30,
                font=fuenteNormal,
                text=f'...',
                anchor='w'

                )


marcoSteffensen = tkinter.LabelFrame(MainLeftFrame, text="Steffensen", font=fuentesubtitulos)
marcoSteffensen.pack(padx=15, pady=15)
entradaSteffensen = tkinter.Label(marcoSteffensen, 
                border=4,
                width=30,
                font=fuenteNormal,
                text=f'...',
                anchor='w'
                )

marcoTanteo = tkinter.LabelFrame(MainLeftFrame, text="Tanteo", font=fuentesubtitulos)
marcoTanteo.pack(padx=20, pady=15)
entradaTanteo = tkinter.Label(marcoTanteo, 
                border=4,
                width=30,
                font=fuenteNormal,
                text=f'...',
                anchor='w'
                )

marcoBiseccion = tkinter.LabelFrame(MainLeftFrame, text="Biseccion", font=fuentesubtitulos)
marcoBiseccion.pack(padx=15, pady=15)
entradaBiseccion = tkinter.Label(marcoBiseccion, 
                border=4,
                width=30,
                font=fuenteNormal,
                text=f'...',
                anchor='w'
                )

marcoReglaFalsa = tkinter.LabelFrame(MainLeftFrame, text="Regla Falsa", font=fuentesubtitulos)
marcoReglaFalsa.pack(padx=15, pady=15)
entradaReglaFalsa = tkinter.Label(marcoReglaFalsa, 
                border=4,
                width=30,
                font=fuenteNormal,
                text=f'...',
                anchor='w'
                )
def generar_Reporte():
    Rtan = entradaTanteo['text']
    RBi = entradaBiseccion['text']
    Rreg = entradaReglaFalsa['text']
    Rsec = entradaSecante['text']
    Rnew = entradaNewton['text']
    Rste = entradaSteffensen['text']
    textoReporte.configure(state='normal')
    textoReporte.delete('1.0', 'end')
    textoReporte.insert('1.0',f'Metodo        |  Raices encontradas |  Iteraciones\n')
    textoReporte.insert('2.0',f'---------------------------------------\n')
    textoReporte.insert('3.0',f'Tanteo        |  {Rtan}\n')
    textoReporte.insert('4.0',f'Biseccion     |  {RBi}\n')
    textoReporte.insert('5.0',f'Regla Falsa   |  {Rreg}\n')
    textoReporte.insert('6.0',f'Secante       |  {Rsec}\n')
    textoReporte.insert('7.0',f'Newton Raphson|  {Rnew}\n')
    textoReporte.insert('8.0',f'Steffensen    |  {Rste}\n')
    textoReporte.configure(state='disable')


def generar_PDF():
    try:
        if not os.path.exists('Reportes'):
            os.makedirs('Reportes')
        ruta = os.path.join('Reportes','Reporte.pdf')
        doc = cv.Canvas(ruta,pagesize=A4)
        doc.setFont('Helvetica', 12)
        Rtan = entradaTanteo['text']
        RBi = entradaBiseccion['text']
        Rreg = entradaReglaFalsa['text']
        Rsec = entradaSecante['text']
        Rnew = entradaNewton['text']
        Rste = entradaSteffensen['text']
        doc.drawString(72,265,       f'Metodo             |     Raices        |      Iteraciones')
        doc.drawString(72,(265-20),  f'----------------------------------------------------------------')
        doc.drawString(72,(265-40),  f'Tanteo -> {Rtan}')
        doc.drawString(72,(265 - 60),f'Biseccion -> {RBi}')
        doc.drawString(72,(265 - 80),f'Regla Falsa -> {Rreg}')
        doc.drawString(72,(265 - 100),f'Secante -> {Rsec}')
        doc.drawString(72,(265 - 120),f'Newton Raphson -> {Rnew}')
        doc.drawString(72,(265 - 140),f'Steffensen -> {Rste}')
        formula = EntradaFuncion.get()
        graph(formula)
        ax.figure.savefig('mi_grafico.png')
        with open('mi_grafico.png','rb') as f:
            img = ImageReader(f)
        doc.drawImage(img,50,320,width=500, height=500)
        os.remove('mi_grafico.png')
        doc.save()
    except Exception:
        messagebox.showerror("Error", f"Ha ocurrido un error, debes generar el grafico\ny generar el reporte")



btngraficar = tkinter.Button(ventana, text="Graficar", font=fuenteNormal, command=plot, width=43, bg='steel blue', fg='White', border=3)
btngraficar.pack()
btngraficar.place(x=370,y=30)
btngenerarReporte = tkinter.Button(ventana, text="Generar Reporte", font=fuenteNormal, width=20, bg='steel blue', fg='White', border=3, command=generar_Reporte)
btngenerarReporte.pack()
btngenerarReporte.place(x=370,y=610)
textoReporte = tkinter.Text(ventana, width=50, height=10, border=3)
textoReporte.pack()
textoReporte.place(x=370, y=650)
btnGuardarReporte = tkinter.Button(ventana, text='Guardar', font=fuenteNormal,width=10, bg='steel blue', fg='White', border=3, command=generar_PDF)
btnGuardarReporte.pack()
btnGuardarReporte.place(x=650,y=610)

entradaNewton.pack()
entradaSecante.pack()
entradaSteffensen.pack()
entradaTanteo.pack()
entradaBiseccion.pack()
entradaReglaFalsa.pack()

ventana.mainloop()