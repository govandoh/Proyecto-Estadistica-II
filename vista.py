
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfile
import MMC

class CenteredWindow:
    def __init__(self, master):
        self.master = master
        self.style = ttk.Style(theme='darkly')  # Crea un estilo ttkbootstrap
        self.master.title("Ventana centrada")
        self.master.geometry("750x500")  # Tamaño inicial de la ventana
        self.place_window_center()  # Centra la ventana en la pantalla
        # Crea el menú
        self.create_menu()
        self.gif = None
        self.create_cover()

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
        
        # Crea el menú "Datos"
        data_menu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Regresión Mínimos Cuadrados", menu=data_menu)
        # Crea submenús para el menú "Datos"
        regresion_menu = ttk.Menu(data_menu, tearoff=0)
        data_menu.add_cascade(label="Carga Automática desde Conexión CSV", menu=regresion_menu)
        regresion_menu.add_command(label="Regresión Lineal Simple", command=self.ventana_regresion_simple)
        regresion_menu.add_separator()
        regresion_menu.add_command(label="Regresión Lineal Múltiple", command=self.multiple_linear_regression)
        data_menu.add_separator()
        data_menu.add_command(label="Carga Manual", command=self.manual_data_entry)
        
        option_menu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=option_menu)
        option_menu.add_cascade(label="Acerca De")
        option_menu.add_separator()
        option_menu.add_command(label="Salir", command=self.master.quit)
        
        
        # Establece el menú en la ventana
        self.master.config(menu=menubar)

    def ventana_regresion_simple(self):
        v1 = ttk.Toplevel(self.master, position=(600,300), minsize=(500,250))
        v1.title("Regresión Simple")
        v1.resizable(False, False)
        v1.geometry("500x250")
        
        # Etiqueta y entrada para ingresar el valor a estimar
        valor_estimar_label = ttk.Label(v1, text="Ingrese el valor a estimar:")
        valor_estimar_label.pack(pady=5)
        
        self.valor_estimar_entry = ttk.Entry(v1)
        self.valor_estimar_entry.pack(pady=5)
        
        # Etiqueta y entrada para cargar la ruta del archivo
        archivo_label = ttk.Label(v1, text="Seleccione el archivo CSV:")
        archivo_label.pack(pady=5)
        
        self.file_entry = ttk.Entry(v1, width=50)
        self.file_entry.pack(pady=5)
        
        ttk.Button(v1, text="Seleccionar archivo", command=self.select_file).pack(pady=5)
        ttk.Button(v1, text="Calcular", command=self.calcular_regresion).pack(pady=5)
    
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
            MMC.insertar_csv_lineal(self.ruta, valor_estimar)
        
            
    
    def simple_linear_regression(self):
        self.ventana_regresion_simple()
        print("Regresión Lineal Simple")

    def multiple_linear_regression(self):
        # Lógica para la regresión lineal múltiple
        print("Regresión Lineal Múltiple")

    def manual_data_entry(self):
        # Aquí puedes implementar la lógica para abrir una segunda ventana para la inserción manual de datos
        print("Abrir ventana para inserción manual de datos")



def main():
    
    root = ttk.Window(position=(500,300))
    app = CenteredWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
