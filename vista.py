
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfile

import MMC

class CenteredWindow:
    def __init__(self, master):
        self.master = master
        self.style = ttk.Style(theme='darkly')  # Crea un estilo ttkbootstrap
        self.master.title("Proyecto Mínimos Cuadrados")
        self.master.geometry("750x500")  # Tamaño inicial de la ventana
        self.place_window_center()  # Centra la ventana en la pantalla
        self.master.resizable(False,False)
        # Crea el menú
        self.create_menu()
        self.gif = None
        self.create_cover()
        
        vcmd = (self.master.register(self.validate_numeric_input), '%P')



    def create_cover(self):
        # Fondo animado GIF
        self.canvas = ttk.Canvas(self.master, width=400, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.gif = ttk.PhotoImage(file="cover.GIF")
        self.canvas.create_image(0, 0, anchor="nw", image=self.gif)
        
        # Título del proyecto
        ttk.Label(self.master, text="Proyecto Estadística II", font=("Helvetica", 24),style="warning").place(relx=0.5, rely=0.3, anchor="center")
        # Subtítulo
        ttk.Label(self.master, text="Mínimos Cuadrados (Simple y Multiple)", font=("Helvetica", 16), style="success").place(relx=0.5, rely=0.4, anchor="center")
        
        # ProgressBar
        self.progress = ttk.Progressbar(self.master, mode="indeterminate")
        self.progress.place(relx=0.5, rely=0.6, anchor="center")
        
        # Simular carga
        self.start_loading()
        
    def start_loading(self):
        self.progress.start(5)  # Inicia la animación de ProgressBar con una velocidad de 10
    
    def place_window_center(self):
        """Posiciona la ventana en el centro de la pantalla."""
        self.master.update_idletasks()
        w_height = self.master.winfo_height()
        w_width = self.master.winfo_width()
        s_height = self.master.winfo_screenheight()
        s_width = self.master.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.master.geometry(f'+{xpos}+{ypos}')
        
    def create_menu(self):
        # Crea un menú en la ventana
        menubar = ttk.Menu(self.master)
        
        insert_menu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Insertar en CSV's", menu=insert_menu)
        insert_menu.add_cascade(label="Insertar CSV Simple", command="")
        insert_menu.add_cascade(label="Insertar CSV Multiple", command="")
        
        
        # Crea el menú "Datos"
        data_menu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Regresión Mínimos Cuadrados", menu=data_menu)
        # Crea submenús para el menú "Datos"
        regresion_menu = ttk.Menu(data_menu, tearoff=0)
        data_menu.add_cascade(label="Carga Automática desde Conexión CSV", menu=regresion_menu)
        regresion_menu.add_command(label="Regresión Lineal Simple", command=self.ventana_regresion_simple)
        regresion_menu.add_command(label="Regresión Lineal Múltiple", command=self.ventana_regresion_multiple)
        
        option_menu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=option_menu)
        option_menu.add_cascade(label="Acerca De", command=self.ventana_acerca_de)
        option_menu.add_separator()
        option_menu.add_command(label="Salir", command=self.master.quit)
        
        
        # Establece el menú en la ventana
        self.master.config(menu=menubar)

    def ventana_regresion_simple(self):
        v1 = ttk.Toplevel(self.master, position=(600, 300))
        v1.title("Regresión Simple")
        v1.resizable(False, False)
        v1.geometry("600x650")

        vcmd = (self.master.register(self.validate_numeric_input), '%P')
        
        # Field para ingresar valor
        valor_estimar_label = ttk.Label(v1, text="Valor de x a estimar:")
        valor_estimar_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.valor_estimar_entry = ttk.Entry(v1, validate='key', validatecommand=vcmd)
        self.valor_estimar_entry.grid(row=0, column=1, padx=5, pady=5)

        # Field para ingresar ruta
        archivo_label = ttk.Label(v1, text="Ingrese la ruta del archivo:")
        archivo_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.file_entry = ttk.Entry(v1, width=25)
        self.file_entry.grid(row=1, column=1, padx=5, pady=5)

        # Boton Seleccionar archivo
        ttk.Button(v1, text="Seleccionar archivo", command=self.select_file).grid(row=1, column=2, padx=5, pady=5)

        # Boton Calcular
        ttk.Button(v1, text="Calcular", command=self.calcular_regresion).grid(row=2, column=1, padx=5, pady=5)

        # Scroller Text Field para imprimir un texto
        scroller_label = ttk.Label(v1, text="Detalle de calculos")
        scroller_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.scrolled_text = ttk.ScrolledText(v1, wrap=ttk.WORD, width=80, height=30)
        self.scrolled_text.grid(row=4, column=0, columnspan=3, padx=40, pady=5)

        v1.grab_set()
        
    def ventana_regresion_multiple(self):
        v2 = ttk.Toplevel(self.master, position=(600,300))
        v2.title("Regresión Multiple")
        v2.resizable(False, False)
        v2.geometry("900x700")

        vcmd = (self.master.register(self.validate_numeric_input), '%P')
        
        # Field para ingresar valor
        valor_estimar_label1 = ttk.Label(v2, text="Valor de x1 a estimar:")
        valor_estimar_label1.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        valor_estimar_label2 = ttk.Label(v2, text="Valor de x2 a estimar:")
        valor_estimar_label2.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.valor_estimar_x1 = ttk.Entry(v2, validate='key', validatecommand=vcmd)
        self.valor_estimar_x1.grid(row=0, column=1, padx=5, pady=5)
        
        self.valor_estimar_x2 = ttk.Entry(v2, validate='key', validatecommand=vcmd)
        self.valor_estimar_x2.grid(row=1, column=1, padx=5, pady=5)

        # Field para ingresar ruta
        archivo_label = ttk.Label(v2, text="Ingrese la ruta del archivo:")
        archivo_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.file_entry = ttk.Entry(v2, width=25)
        self.file_entry.grid(row=2, column=1, padx=5, pady=5)

        # Boton Seleccionar archivo
        ttk.Button(v2, text="Seleccionar archivo", command=self.select_file).grid(row=2, column=2, padx=5, pady=5)

        # Boton Calcular
        ttk.Button(v2, text="Calcular", command=self.calcular_multiple).grid(row=3, column=1, padx=5, pady=5)

        # Scroller Text Field para imprimir un texto
        scroller_label = ttk.Label(v2, text="Detalle de calculos")
        scroller_label.grid(row=4, column=4, padx=5, pady=5, sticky="e")

        self.scrolled_text = ttk.ScrolledText(v2, wrap=ttk.WORD, width=130, height=30)
        self.scrolled_text.grid(row=4, column=0, columnspan=3, padx=40, pady=5)

        v2.grab_set()
        
    def validate_numeric_input(self, new_value):
        """Función de validación para permitir solo números"""
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False
    
    def select_file(self):
        file_path = askopenfile(mode="r", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.ruta = file_path.name
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, file_path.name)
                       
    def calcular_regresion(self):
        valor_estimar = self.valor_estimar_entry.get()
        try: 
            valor_estimar = float(valor_estimar)
        except ValueError:
            messagebox.showerror("Error", "Ingrese valor a estima")
        
        if not hasattr(self, 'ruta') or not self.ruta:
            messagebox.showerror("Error", "No se ha seleccionado un archivo")
        elif hasattr(self, 'ruta') or not self.ruta and self.valor_estimar_entry.get() != " ":
            nombre_archivo = MMC.insertar_csv_lineal(self.ruta, valor_estimar)
            if nombre_archivo: 
                self.cargar_resultados(nombre_archivo)
                self.valor_estimar_entry.delete(0, ttk.END)
                self.file_entry.delete(0,ttk.END)

    
    def calcular_multiple(self):
        valor_estimar_x1 = self.valor_estimar_x1.get()
        valor_estimar_x2 = self.valor_estimar_x2.get()
        try:
            valor_estimar_x1 = float(valor_estimar_x1)
            valor_estimar_x2 = float(valor_estimar_x2)
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores a estima")
        
        if not hasattr(self, 'ruta') or not self.ruta:
            messagebox.showerror("Error", "No se ha seleccionado un archivo")
        elif hasattr(self, 'ruta') or not self.ruta and self.valor_estimar_x1.get() != " " and self.valor_estimar_x2.get() != " ":
            nombre_archivo = MMC.insertar_csv_multiple(self.ruta, valor_estimar_x1, valor_estimar_x2)
            if nombre_archivo: 
                self.cargar_resultados(nombre_archivo)
                self.valor_estimar_x1.delete(0, ttk.END)
                self.valor_estimar_x2.delete(0, ttk.END)
                self.file_entry.delete(0,ttk.END)
            
        
    def cargar_resultados(self, nombre_archivo):
        try:
            with open(nombre_archivo, 'r') as archivo:
                contenido = archivo.read()
                self.scrolled_text.delete(1.0, ttk.END)
                self.scrolled_text.insert(ttk.INSERT, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
    
    def ventana_acerca_de(self):
        acerca_de = ttk.Toplevel(self.master, position=(750,300))
        acerca_de.title("Acerca de")
        acerca_de.geometry("400x450")
        
        info = (
            "Desarrolladores:\n"
            "Gerardo Ovando - 9490-21-7\n"
            "Abner Pérez - 9490-17-11829\n"
            "Edvin \n"
            "Curso:\n"
            "Estadística II - Proyecto Final \n\n"
            "Información del Lenguaje:\n"
            "Python 3.12.2\n"
            "Bibliotecas utilizadas:\n"
            "- tkinter\n"
            "- csv\n"
            "- os\n"
            "- datetime\n"
            "- matplotlib\n"
            "- math\n"
            "- ttkbootstrap\n"
            "- statsmodels\n"
            "- numpy\n"
            "- pandas\n"
        )
        
        label_info = ttk.Label(acerca_de, text=info, justify="left", style="info")
        label_info.pack(padx=20, pady=20)
        
        btn_cerrar = ttk.Button(acerca_de, text="Cerrar", command=acerca_de.destroy)
        btn_cerrar.pack(pady=10)
    
    def simple_linear_regression(self):
        self.ventana_regresion_simple()
        

    def multiple_linear_regression(self):
        self.ventana_regresion_multiple

    

def main():
    
    root = ttk.Window(position=(500,300))
    app = CenteredWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
