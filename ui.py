# ui.py
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Módulos del proyecto
import procesador_ihq_biomarcadores
import database_manager

# --- Configuración de Estilo Profesional ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#343638", "grid.color": "#4a4d50", 
                                   "figure.facecolor": "#2b2b2b", "text.color": "white",
                                   "xtick.color": "white", "ytick.color": "white",
                                   "axes.labelcolor": "white", "axes.titlecolor": "white"})

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EVARISIS Gestor H.U.V v2.5")
        self.geometry("1280x800")
        self.minsize(1024, 768)

        self.master_df = pd.DataFrame() # DataFrame maestro que sirve como única fuente de verdad

        # --- Layout Principal Adaptable ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Frame de Navegación (Izquierda) ---
        self.nav_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")
        self.nav_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.nav_frame, text="EVARISIS", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 15))

        self.btn_procesar = ctk.CTkButton(self.nav_frame, text="Procesar PDFs", command=self.show_procesar_frame, height=40)
        self.btn_procesar.grid(row=1, column=0, padx=20, pady=15)

        self.btn_visualizar = ctk.CTkButton(self.nav_frame, text="Visualizar Datos", command=self.show_visualizar_frame, height=40)
        self.btn_visualizar.grid(row=2, column=0, padx=20, pady=15)
        
        self.btn_dashboard = ctk.CTkButton(self.nav_frame, text="Dashboard Analítico", command=self.show_dashboard_frame, height=40)
        self.btn_dashboard.grid(row=3, column=0, padx=20, pady=15)
        
        self.theme_switch = ctk.CTkSwitch(self.nav_frame, text="Modo Claro", command=self.change_theme)
        self.theme_switch.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        # --- Contenedor Principal ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # --- Frames de cada vista ---
        self.procesar_frame = self._create_procesar_frame()
        self.visualizar_frame = self._create_visualizar_frame()
        self.dashboard_frame = self._create_dashboard_frame()

        self.show_procesar_frame()

    # --- Lógica de Navegación ---
    def show_frame(self, frame_to_show):
        for frame in [self.procesar_frame, self.visualizar_frame, self.dashboard_frame]:
            frame.grid_forget()
        frame_to_show.grid(row=0, column=0, sticky="nswe")

    def show_procesar_frame(self):
        self.show_frame(self.procesar_frame)

    def show_visualizar_frame(self):
        self.show_frame(self.visualizar_frame)
        self.refresh_data_and_table()

    def show_dashboard_frame(self):
        self.show_frame(self.dashboard_frame)
        self.cargar_dashboard()

    # --- Creación de Vistas ---
    def _create_procesar_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top_frame, text="Módulo de Procesamiento de Informes IHQ", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, sticky="w")
        
        button_frame = ctk.CTkFrame(top_frame)
        button_frame.grid(row=1, column=0, pady=(15,0), sticky="w")

        self.select_files_button = ctk.CTkButton(button_frame, text="Seleccionar Archivos PDF", command=self.select_files, height=35)
        self.select_files_button.pack(side="left", padx=(0, 10))

        self.start_button = ctk.CTkButton(button_frame, text="Iniciar Procesamiento", command=self.start_processing, state="disabled", height=35)
        self.start_button.pack(side="left")

        self.log_textbox = ctk.CTkTextbox(frame, state="disabled", font=("Consolas", 12))
        self.log_textbox.grid(row=1, column=0, sticky="nsew")
        
        self.pdf_files = []
        return frame

    def _create_visualizar_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=3)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Base de Datos de Informes", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        table_frame = ctk.CTkFrame(frame)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_tabla)
        search_entry = ctk.CTkEntry(table_frame, textvariable=self.search_var, placeholder_text="Buscar por N° Petición, Nombre o Apellido...")
        search_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        style = self.setup_treeview_style()
        self.tree = ttk.Treeview(table_frame, show='headings', style="Custom.Treeview")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.tree.bind("<<TreeviewSelect>>", self.mostrar_detalle_registro)
        
        self.detail_frame = ctk.CTkFrame(frame)
        self.detail_frame.grid(row=1, column=1, sticky="nsew")
        self.detail_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.detail_frame, text="Detalles del Registro", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, pady=10, padx=10)
        self.detail_textbox = ctk.CTkTextbox(self.detail_frame, state="disabled", wrap="word", font=("Calibri", 14))
        self.detail_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.detail_frame.grid_rowconfigure(1, weight=1)

        return frame

    def _create_dashboard_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Dashboard de Análisis Estadístico", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        self.kpi_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.kpi_frame.grid(row=1, column=0, sticky="ew", pady=10)
        
        self.dashboard_canvas_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.dashboard_canvas_frame.grid(row=2, column=0, sticky="nsew")

        return frame
        
    # --- Lógica de Funcionalidades ---
    def log_to_widget(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def select_files(self):
        self.pdf_files = filedialog.askopenfilenames(title="Seleccione archivos PDF", filetypes=[("PDF", "*.pdf")])
        if self.pdf_files:
            self.log_to_widget(f"Seleccionados {len(self.pdf_files)} archivos.")
            self.start_button.configure(state="normal")
        else:
            self.log_to_widget("Selección cancelada.")
            self.start_button.configure(state="disabled")

    def start_processing(self):
        if not self.pdf_files:
            messagebox.showwarning("Advertencia", "Por favor, seleccione archivos PDF primero.")
            return
        
        self.start_button.configure(state="disabled")
        self.select_files_button.configure(state="disabled")
        self.log_to_widget("="*50)
        self.log_to_widget("INICIANDO PROCESAMIENTO...")
        
        threading.Thread(target=self.processing_thread, daemon=True).start()

    def processing_thread(self):
        try:
            output_dir = os.path.dirname(self.pdf_files[0])
            num_records = procesador_ihq_biomarcadores.process_ihq_paths(self.pdf_files, output_dir)
            self.log_to_widget(f"PROCESO COMPLETADO. Se guardaron {num_records} registros en la base de datos.")
            messagebox.showinfo("Éxito", f"Proceso finalizado. Se guardaron {num_records} registros.")
        except Exception as e:
            self.log_to_widget(f"ERROR: {e}")
            messagebox.showerror("Error", f"Ocurrió un error durante el procesamiento:\n{e}")
        finally:
            self.start_button.configure(state="normal")
            self.select_files_button.configure(state="normal")

    def refresh_data_and_table(self):
        try:
            database_manager.init_db()
            self.master_df = database_manager.get_all_records_as_dataframe()
            self._populate_treeview(self.master_df)
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los datos: {e}")
    
    def _populate_treeview(self, df_to_display):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if df_to_display.empty: return

        cols_to_show = ["N. peticion (0. Numero de biopsia)", "Primer nombre", "Primer apellido", "Fecha finalizacion (3. Fecha del informe)", "Malignidad", "Organo (1. Muestra enviada a patología)"]
        df_display = df_to_display[cols_to_show]

        self.tree["columns"] = list(df_display.columns)
        for col in df_display.columns:
            self.tree.heading(col, text=col.split('(')[0].strip())
        
        self.tree.tag_configure('oddrow', background='#343638')
        self.tree.tag_configure('evenrow', background='#2a2d2e')
        
        for index, row in df_display.iterrows():
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=list(row), iid=index, tags=(tag,))

    def filter_tabla(self, *args):
        query = self.search_var.get().lower()
        if not query:
            self._populate_treeview(self.master_df)
            return

        df = self.master_df.copy()
        search_cols = ["N. peticion (0. Numero de biopsia)", "Primer nombre", "Primer apellido"]
        for col in search_cols:
            df[col] = df[col].astype(str)

        mask = (df[search_cols[0]].str.lower().str.contains(query, na=False) |
                df[search_cols[1]].str.lower().str.contains(query, na=False) |
                df[search_cols[2]].str.lower().str.contains(query, na=False))
        self._populate_treeview(df[mask])

    def mostrar_detalle_registro(self, event):
        selected_item = self.tree.focus()
        if not selected_item: return
        
        item_index = int(selected_item)
        record = self.master_df.loc[item_index]
        
        self.detail_textbox.configure(state="normal")
        self.detail_textbox.delete("1.0", "end")
        
        details_text = ""
        for key, value in record.items():
            if pd.notna(value) and str(value).strip():
                details_text += f"{key.split('(')[0].strip()}:\n{value}\n{'-'*30}\n"
        
        self.detail_textbox.insert("1.0", details_text)
        self.detail_textbox.configure(state="disabled")

    def cargar_dashboard(self):
        for widget in self.kpi_frame.winfo_children(): widget.destroy()
        for widget in self.dashboard_canvas_frame.winfo_children(): widget.destroy()

        try:
            df = database_manager.get_all_records_as_dataframe()
            if df.empty:
                ctk.CTkLabel(self.dashboard_canvas_frame, text="No hay datos suficientes para generar análisis.").pack(pady=20)
                return

            # --- KPIs ---
            kpi_col = 0
            self._create_kpi_card("Total Informes", f"{len(df)}", kpi_col); kpi_col += 1

            if 'Malignidad' in df.columns and not df['Malignidad'].dropna().empty:
                tasa_malignidad = (df['Malignidad'].value_counts(normalize=True).get('PRESENTE', 0) * 100)
                self._create_kpi_card("Tasa Malignidad", f"{tasa_malignidad:.1f}%", kpi_col); kpi_col += 1
            
            if 'IHQ_KI-67' in df.columns:
                ki_67_series = pd.to_numeric(df['IHQ_KI-67'].str.replace('%', ''), errors='coerce').dropna()
                if not ki_67_series.empty:
                    ki67_avg = ki_67_series.mean()
                    self._create_kpi_card("Ki-67 Promedio", f"{ki67_avg:.1f}%", kpi_col); kpi_col += 1
            
            # --- Gráficos ---
            fig = Figure(figsize=(12, 10), dpi=100)
            fig.subplots_adjust(hspace=0.6, wspace=0.3)
            plot_position = 1
            
            if 'IHQ_KI-67' in df.columns:
                ki_67_series = pd.to_numeric(df['IHQ_KI-67'].str.replace('%', ''), errors='coerce').dropna()
                if not ki_67_series.empty:
                    ax1 = fig.add_subplot(2, 2, plot_position); plot_position += 1
                    sns.histplot(x=ki_67_series, kde=True, ax=ax1, color="#3498db")
                    ax1.set_title('Distribución de Ki-67')

            if 'IHQ_RECEPTOR_ESTROGENO' in df.columns and 'IHQ_RECEPTOR_PROGESTAGENOS' in df.columns:
                df_re_pr = df[['IHQ_RECEPTOR_ESTROGENO', 'IHQ_RECEPTOR_PROGESTAGENOS']].dropna()
                if not df_re_pr.empty:
                    ax2 = fig.add_subplot(2, 2, plot_position); plot_position += 1
                    df['RE_Estado'] = df['IHQ_RECEPTOR_ESTROGENO'].str.contains('POSITIVO', na=False)
                    df['PR_Estado'] = df['IHQ_RECEPTOR_PROGESTAGENOS'].str.contains('POSITIVO', na=False)
                    co_ocurrencia = df.groupby(['RE_Estado', 'PR_Estado']).size().unstack(fill_value=0)
                    all_labels = [False, True]
                    co_ocurrencia = co_ocurrencia.reindex(index=all_labels, columns=all_labels, fill_value=0)
                    co_ocurrencia.index = ['RE Negativo', 'RE Positivo']
                    co_ocurrencia.columns = ['PR Negativo', 'PR Positivo']
                    co_ocurrencia.plot(kind='bar', stacked=True, ax=ax2, colormap='viridis')
                    ax2.set_title('Co-ocurrencia RE y PR')
                    ax2.tick_params(axis='x', rotation=0)

            if 'Organo (1. Muestra enviada a patología)' in df.columns and not df['Organo (1. Muestra enviada a patología)'].dropna().empty:
                ax3 = fig.add_subplot(2, 2, plot_position); plot_position += 1
                top_organos = df['Organo (1. Muestra enviada a patología)'].value_counts().nlargest(5)
                sns.barplot(x=top_organos.index, y=top_organos.values, ax=ax3, palette='rocket')
                ax3.set_title('Top 5 Órganos Analizados')
                ax3.tick_params(axis='x', rotation=45, ha='right')
            
            if 'Fecha finalizacion (3. Fecha del informe)' in df.columns:
                fechas = pd.to_datetime(df['Fecha finalizacion (3. Fecha del informe)'], dayfirst=True, errors='coerce').dropna()
                if not fechas.empty:
                    ax4 = fig.add_subplot(2, 2, plot_position); plot_position += 1
                    informes_mes = fechas.to_frame(name='fecha').set_index('fecha').resample('M').size()
                    informes_mes.plot(kind='line', ax=ax4, marker='o', color='#f1c40f')
                    ax4.set_title('Informes Procesados por Mes')
                    # ▼▼▼ INICIO DE LA CORRECCIÓN ▼▼▼
                    ax4.set(xlabel="Mes") # Usamos .set() que es más robusto
                    # ▲▲▲ FIN DE LA CORRECCIÓN ▲▲▲
            
            if plot_position > 1:
                canvas = FigureCanvasTkAgg(fig, master=self.dashboard_canvas_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
            else:
                 ctk.CTkLabel(self.dashboard_canvas_frame, text="No hay suficientes datos válidos para generar gráficos.").pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error de Dashboard", f"No se pudo generar el dashboard: {e}")
            
    def _create_kpi_card(self, title, value, col):
        self.kpi_frame.grid_columnconfigure(col, weight=1)
        card = ctk.CTkFrame(self.kpi_frame, border_width=1, border_color="#565b5e")
        card.grid(row=0, column=col, sticky="ew", padx=10)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 2))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=22)).pack(pady=(2, 10))

    def setup_treeview_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview", background="#2a2d2e", foreground="white", fieldbackground="#343638", borderwidth=0, rowheight=25)
        style.map('Custom.Treeview', background=[('selected', '#22559b')])
        style.configure("Custom.Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Calibri', 12, 'bold'))
        style.map("Custom.Treeview.Heading", background=[('active', '#343638')])
        return style
        
    def change_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

if __name__ == "__main__":
    app = App()
    app.mainloop()