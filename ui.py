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

# =========================
# Tema oscuro y paleta EVARISIS Gestor HUV
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT   = "#2b6cb0"  # azul HUV
BG       = "#0f1115"  # fondo app
SURFACE  = "#171a21"  # tarjetas / paneles
TEXT     = "#e9ecef"  # texto principal
MUTED    = "#a9b1bb"  # texto secundario

# Estilo visual para seaborn/mpl dentro de Tk
sns.set_theme(
    style="darkgrid",
    rc={
        "axes.facecolor": "#343638",
        "grid.color": "#4a4d50",
        "figure.facecolor": "#2b2b2b",
        "text.color": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "axes.labelcolor": "white",
        "axes.titlecolor": "white",
    },
)

# Módulos del proyecto
import procesador_ihq_biomarcadores
import database_manager


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---------- Ventana principal ----------
        self.title("EVARISIS Gestor HUV")
        self.geometry("1400x860")
        self.minsize(1200, 780)
        self.configure(fg_color=BG)

        self.master_df = pd.DataFrame()  # DataFrame maestro (fuente única de verdad)

        # Grid maestro: fila 0 header, fila 1 contenido, fila 2 status
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # ---------- Header (hero) ----------
        self.header = ctk.CTkFrame(self, height=72, fg_color=SURFACE, corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_propagate(False)

        self.h_title = ctk.CTkLabel(
            self.header,
            text="EVARISIS Gestor HUV",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT,
        )
        self.h_title.grid(row=0, column=0, padx=20, pady=18, sticky="w")

        self.h_meta = ctk.CTkLabel(
            self.header,
            text="Oncología • IHQ",
            font=ctk.CTkFont(size=14),
            text_color=MUTED,
        )
        self.h_meta.grid(row=0, column=1, padx=20, pady=18, sticky="e")

        # ---------- Panel lateral ----------
        self.nav_frame = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color=SURFACE)
        self.nav_frame.grid(row=1, column=0, sticky="nswe")
        self.nav_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.nav_frame,
            text="EVARISIS Gestor HUV",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT,
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(26, 12), sticky="w")

        self.btn_procesar = ctk.CTkButton(
            self.nav_frame, text="Procesar PDFs", command=self.show_procesar_frame, height=40
        )
        self.btn_procesar.grid(row=1, column=0, padx=20, pady=12, sticky="ew")

        self.btn_visualizar = ctk.CTkButton(
            self.nav_frame, text="Visualizar Datos", command=self.show_visualizar_frame, height=40
        )
        self.btn_visualizar.grid(row=2, column=0, padx=20, pady=12, sticky="ew")

        self.btn_dashboard = ctk.CTkButton(
            self.nav_frame, text="Dashboard Analítico", command=self.show_dashboard_frame, height=40
        )
        self.btn_dashboard.grid(row=3, column=0, padx=20, pady=12, sticky="ew")

        self.theme_switch = ctk.CTkSwitch(self.nav_frame, text="Modo Claro", command=self.change_theme)
        self.theme_switch.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        # ---------- Contenido ----------
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color=BG)
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=0)
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Fila de KPI cards globales
        self.kpi_row = ctk.CTkFrame(self.content, fg_color=BG)
        self.kpi_row.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))
        for i in range(4):
            self.kpi_row.grid_columnconfigure(i, weight=1)

        self.kpi_total = self._kpi_card(self.kpi_row, "Total informes", "0")
        self.kpi_total.grid(row=0, column=0, padx=8, pady=6, sticky="nsew")

        self.kpi_malig = self._kpi_card(self.kpi_row, "Malignidad (%)", "0.0%")
        self.kpi_malig.grid(row=0, column=1, padx=8, pady=6, sticky="nsew")

        self.kpi_ultimo = self._kpi_card(self.kpi_row, "Último ingreso", "—")
        self.kpi_ultimo.grid(row=0, column=2, padx=8, pady=6, sticky="nsew")

        self.kpi_tiempo = self._kpi_card(self.kpi_row, "Tiempo de proceso", "—")
        self.kpi_tiempo.grid(row=0, column=3, padx=8, pady=6, sticky="nsew")

        # Contenedor de vistas debajo de los KPIs
        self.views_container = ctk.CTkFrame(self.content, fg_color="transparent")
        self.views_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(6, 12))
        self.views_container.grid_columnconfigure(0, weight=1)
        self.views_container.grid_rowconfigure(0, weight=1)

        # ---------- Status bar ----------
        self.status = ctk.CTkLabel(self, text="Listo.", text_color=MUTED, anchor="w")
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 8))

        # ---------- Vistas ----------
        self.procesar_frame = self._create_procesar_frame()
        self.visualizar_frame = self._create_visualizar_frame()
        self.dashboard_frame = self._create_dashboard_frame()

        # Vista inicial
        self.show_procesar_frame()

    # =========================
    # Helpers UI (KPI y Status)
    # =========================
    def _kpi_card(self, parent, title, value_text):
        card = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=14)
        title_lbl = ctk.CTkLabel(card, text=title, text_color=MUTED, font=ctk.CTkFont(size=12))
        title_lbl.pack(anchor="w", padx=14, pady=(12, 2))
        value_lbl = ctk.CTkLabel(card, text=value_text, text_color=TEXT, font=ctk.CTkFont(size=26, weight="bold"))
        value_lbl.pack(anchor="w", padx=14, pady=(0, 12))
        card.value_lbl = value_lbl
        return card

    def _render_kpis(self, df):
        if df is None or df.empty:
            self.kpi_total.value_lbl.configure(text="0")
            self.kpi_malig.value_lbl.configure(text="0.0%")
            self.kpi_ultimo.value_lbl.configure(text="—")
            return

        total = len(df)

        # Malignidad: "PRESENTE"
        mal_col = "Malignidad" if "Malignidad" in df.columns else None
        malignos = int(df[mal_col].astype(str).str.upper().eq("PRESENTE").sum()) if mal_col else 0
        pct = (malignos / total * 100) if total else 0.0

        # Último ingreso: fecha finalización > informe > ingreso
        fecha_cols = [
            "Fecha finalizacion (3. Fecha del informe)",
            "Fecha de informe",
            "Fecha de ingreso",
        ]
        fecha_encontrada = None
        for c in fecha_cols:
            if c in df.columns:
                try:
                    fecha_encontrada = (pd.to_datetime(df[c], dayfirst=True, errors="coerce")).max()
                    if pd.notna(fecha_encontrada):
                        break
                except Exception:
                    pass
        ultimo_txt = "—" if (fecha_encontrada is None or pd.isna(fecha_encontrada)) else fecha_encontrada.strftime("%d/%m/%Y")

        self.kpi_total.value_lbl.configure(text=f"{total:,}".replace(",", "."))
        self.kpi_malig.value_lbl.configure(text=f"{pct:.1f}%")
        self.kpi_ultimo.value_lbl.configure(text=ultimo_txt)

    def set_status(self, text):
        try:
            self.status.configure(text=text)
            self.status.update_idletasks()
        except Exception:
            pass

    # =========================
    # Navegación
    # =========================
    def show_frame(self, frame_to_show):
        for frame in [self.procesar_frame, self.visualizar_frame, self.dashboard_frame]:
            frame.grid_forget()
        frame_to_show.grid(row=0, column=0, sticky="nswe")

    def show_procesar_frame(self):
        self.show_frame(self.procesar_frame)
        self.set_status("Listo para procesar PDFs.")

    def show_visualizar_frame(self):
        self.show_frame(self.visualizar_frame)
        self.refresh_data_and_table()
        self.set_status("Visualizando datos de la base.")

    def show_dashboard_frame(self):
        self.show_frame(self.dashboard_frame)
        self.cargar_dashboard()
        self.set_status("Dashboard actualizado.")

    # =========================
    # Creación de Vistas
    # =========================
    def _create_procesar_frame(self):
        frame = ctk.CTkFrame(self.views_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top_frame,
            text="Módulo de Procesamiento de Informes IHQ",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        button_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=(15, 0), sticky="w")

        self.select_files_button = ctk.CTkButton(
            button_frame, text="Seleccionar Archivos PDF", command=self.select_files, height=35
        )
        self.select_files_button.pack(side="left", padx=(0, 10))

        self.start_button = ctk.CTkButton(
            button_frame, text="Iniciar Procesamiento", command=self.start_processing, state="disabled", height=35
        )
        self.start_button.pack(side="left")

        self.log_textbox = ctk.CTkTextbox(frame, state="disabled", font=("Consolas", 12))
        self.log_textbox.grid(row=1, column=0, sticky="nsew")

        self.pdf_files = []
        return frame

    def _create_visualizar_frame(self):
        frame = ctk.CTkFrame(self.views_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=3)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text="Base de Datos de Informes", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        table_frame = ctk.CTkFrame(frame, fg_color="transparent")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_tabla)
        search_entry = ctk.CTkEntry(
            table_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por N° Petición, Nombre o Apellido...",
        )
        search_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        style = self.setup_treeview_style()
        self.tree = ttk.Treeview(table_frame, show="headings", style="Custom.Treeview")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.tree.bind("<<TreeviewSelect>>", self.mostrar_detalle_registro)

        self.detail_frame = ctk.CTkFrame(frame, fg_color=SURFACE)
        self.detail_frame.grid(row=1, column=1, sticky="nsew")
        self.detail_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.detail_frame, text="Detalles del Registro", font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=10, padx=10)
        self.detail_textbox = ctk.CTkTextbox(self.detail_frame, state="disabled", wrap="word", font=("Calibri", 14))
        self.detail_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.detail_frame.grid_rowconfigure(1, weight=1)

        return frame

    def _create_dashboard_frame(self):
        frame = ctk.CTkFrame(self.views_container, fg_color="transparent")
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text="Dashboard de Análisis Estadístico", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.kpi_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.kpi_frame.grid(row=1, column=0, sticky="ew", pady=10)

        self.dashboard_canvas_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.dashboard_canvas_frame.grid(row=2, column=0, sticky="nsew")

        return frame

    # =========================
    # Funcionalidad
    # =========================
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
            self.set_status(f"{len(self.pdf_files)} archivos listos.")
        else:
            self.log_to_widget("Selección cancelada.")
            self.start_button.configure(state="disabled")
            self.set_status("Selección cancelada.")

    def start_processing(self):
        if not self.pdf_files:
            messagebox.showwarning("Advertencia", "Por favor, seleccione archivos PDF primero.")
            return

        self.start_button.configure(state="disabled")
        self.select_files_button.configure(state="disabled")
        self.log_to_widget("=" * 50)
        self.log_to_widget("INICIANDO PROCESAMIENTO...")
        self.set_status("Procesando… esto puede tardar según el tamaño de los PDFs.")

        threading.Thread(target=self.processing_thread, daemon=True).start()

    def processing_thread(self):
        try:
            output_dir = os.path.dirname(self.pdf_files[0])
            num_records = procesador_ihq_biomarcadores.process_ihq_paths(self.pdf_files, output_dir)
            self.log_to_widget(f"PROCESO COMPLETADO. Se guardaron {num_records} registros en la base de datos.")
            messagebox.showinfo("Éxito", f"Proceso finalizado. Se guardaron {num_records} registros.")
            self.set_status("Completado ✔  |  " + datetime.now().strftime("%d/%m/%Y %H:%M"))
        except Exception as e:
            self.log_to_widget(f"ERROR: {e}")
            messagebox.showerror("Error", f"Ocurrió un error durante el procesamiento:\n{e}")
            self.set_status("Error en el procesamiento.")
        finally:
            self.start_button.configure(state="normal")
            self.select_files_button.configure(state="normal")

    def refresh_data_and_table(self):
        try:
            database_manager.init_db()
            self.master_df = database_manager.get_all_records_as_dataframe()
            self._populate_treeview(self.master_df)
            self._render_kpis(self.master_df)
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los datos: {e}")
            self.set_status("Error al cargar datos.")

    def _populate_treeview(self, df_to_display):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if df_to_display.empty:
            return

        cols_to_show = [
            "N. peticion (0. Numero de biopsia)",
            "Primer nombre",
            "Primer apellido",
            "Fecha finalizacion (3. Fecha del informe)",
            "Malignidad",
            "Organo (1. Muestra enviada a patología)",
        ]
        df_display = df_to_display[[c for c in cols_to_show if c in df_to_display.columns]].copy()

        self.tree["columns"] = list(df_display.columns)
        for col in df_display.columns:
            header = col.split("(")[0].strip()
            # Ordenamiento al clic
            self.tree.heading(col, text=header, command=lambda c=col: self._sort_treeview(c, False))
            # Auto-ancho (acorde a datos y encabezado, con límites)
            try:
                max_len = max(df_display[col].astype(str).str.len().max(), len(header))
            except Exception:
                max_len = len(header)
            width = max(120, min(280, int(max_len * 7)))
            self.tree.column(col, width=width, anchor="w", stretch=True)

        # Filas cebra
        self.tree.tag_configure("oddrow", background="#2a2d2e")
        self.tree.tag_configure("evenrow", background="#232629")

        for idx, (_, row) in enumerate(df_display.iterrows()):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=list(row), iid=idx, tags=(tag,))

        # Actualizar KPIs en base a lo mostrado
        try:
            self._render_kpis(df_display)
        except Exception:
            pass

    def _sort_treeview(self, col, reverse):
        items = self.tree.get_children("")
        data = [(self.tree.set(it, col), it) for it in items]

        from datetime import datetime as _dt

        def _key(v):
            s = str(v).strip()
            # número
            try:
                return float(s.replace(",", "."))
            except Exception:
                pass
            # fecha
            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
                try:
                    return _dt.strptime(s, fmt)
                except Exception:
                    pass
            return s.lower()

        data.sort(key=lambda x: _key(x[0]), reverse=reverse)

        for idx, (_, item) in enumerate(data):
            self.tree.move(item, "", idx)

        self.tree.heading(col, command=lambda: self._sort_treeview(col, not reverse))

    def filter_tabla(self, *args):
        query = self.search_var.get().lower()
        if not query:
            self._populate_treeview(self.master_df)
            return

        df = self.master_df.copy()
        search_cols = ["N. peticion (0. Numero de biopsia)", "Primer nombre", "Primer apellido"]
        for col in search_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)
        mask = False
        if search_cols[0] in df.columns:
            mask = df[search_cols[0]].str.lower().str.contains(query, na=False)
        if search_cols[1] in df.columns:
            mask |= df[search_cols[1]].str.lower().str.contains(query, na=False)
        if search_cols[2] in df.columns:
            mask |= df[search_cols[2]].str.lower().str.contains(query, na=False)
        self._populate_treeview(df[mask])

    def mostrar_detalle_registro(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        item_index = int(selected_item)
        if item_index not in self.master_df.index:
            return
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
        for widget in self.kpi_frame.winfo_children():
            widget.destroy()
        for widget in self.dashboard_canvas_frame.winfo_children():
            widget.destroy()

        try:
            df = database_manager.get_all_records_as_dataframe()
            if df.empty:
                ctk.CTkLabel(self.dashboard_canvas_frame, text="No hay datos suficientes para generar análisis.").pack(
                    pady=20
                )
                return

            # --- KPIs del dashboard ---
            kpi_col = 0
            self._create_kpi_card("Total Informes", f"{len(df)}", kpi_col)
            kpi_col += 1

            if "Malignidad" in df.columns and not df["Malignidad"].dropna().empty:
                tasa_malignidad = df["Malignidad"].astype(str).str.upper().eq("PRESENTE").mean() * 100
                self._create_kpi_card("Tasa Malignidad", f"{tasa_malignidad:.1f}%", kpi_col)
                kpi_col += 1

            if "IHQ_KI-67" in df.columns:
                ki_67_series = pd.to_numeric(df["IHQ_KI-67"].astype(str).str.replace("%", ""), errors="coerce").dropna()
                if not ki_67_series.empty:
                    ki67_avg = ki_67_series.mean()
                    self._create_kpi_card("Ki-67 Promedio", f"{ki67_avg:.1f}%", kpi_col)
                    kpi_col += 1

            # --- Gráficos ---
            fig = Figure(figsize=(12, 10), dpi=100)
            fig.subplots_adjust(hspace=0.6, wspace=0.3)
            plot_position = 1

            if "IHQ_KI-67" in df.columns:
                ki_67_series = pd.to_numeric(df["IHQ_KI-67"].astype(str).str.replace("%", ""), errors="coerce").dropna()
                if not ki_67_series.empty:
                    ax1 = fig.add_subplot(2, 2, plot_position)
                    plot_position += 1
                    import matplotlib.pyplot as plt  # para estilos por defecto
                    # hist con kde usando seaborn
                    import seaborn as _sns  # no shadow the global
                    _sns.histplot(x=ki_67_series, kde=True, ax=ax1)
                    ax1.set_title("Distribución de Ki-67")

            if "IHQ_RECEPTOR_ESTROGENO" in df.columns and "IHQ_RECEPTOR_PROGESTAGENOS" in df.columns:
                df_re_pr = df[["IHQ_RECEPTOR_ESTROGENO", "IHQ_RECEPTOR_PROGESTAGENOS"]].dropna()
                if not df_re_pr.empty:
                    ax2 = fig.add_subplot(2, 2, plot_position)
                    plot_position += 1
                    df["RE_Estado"] = df["IHQ_RECEPTOR_ESTROGENO"].astype(str).str.contains("POSITIVO", na=False)
                    df["PR_Estado"] = df["IHQ_RECEPTOR_PROGESTAGENOS"].astype(str).str.contains("POSITIVO", na=False)
                    co_ocurrencia = df.groupby(["RE_Estado", "PR_Estado"]).size().unstack(fill_value=0)
                    all_labels = [False, True]
                    co_ocurrencia = co_ocurrencia.reindex(index=all_labels, columns=all_labels, fill_value=0)
                    co_ocurrencia.index = ["RE Negativo", "RE Positivo"]
                    co_ocurrencia.columns = ["PR Negativo", "PR Positivo"]
                    co_ocurrencia.plot(kind="bar", stacked=True, ax=ax2)
                    ax2.set_title("Co-ocurrencia RE y PR")
                    ax2.tick_params(axis="x", rotation=0)

            if "Organo (1. Muestra enviada a patología)" in df.columns and not df[
                "Organo (1. Muestra enviada a patología)"
            ].dropna().empty:
                ax3 = fig.add_subplot(2, 2, plot_position)
                plot_position += 1
                top_organos = df["Organo (1. Muestra enviada a patología)"].value_counts().nlargest(5)
                import seaborn as _sns2
                _sns2.barplot(x=top_organos.index, y=top_organos.values, ax=ax3)
                ax3.set_title("Top 5 Órganos Analizados")
                ax3.tick_params(axis="x", rotation=45)
                for lbl in ax3.get_xticklabels():
                    lbl.set_horizontalalignment("right")

            if "Fecha finalizacion (3. Fecha del informe)" in df.columns:
                fechas = pd.to_datetime(df["Fecha finalizacion (3. Fecha del informe)"], dayfirst=True, errors="coerce").dropna()
                if not fechas.empty:
                    ax4 = fig.add_subplot(2, 2, plot_position)
                    plot_position += 1
                    informes_mes = fechas.to_frame(name="fecha").set_index("fecha").resample("M").size()
                    informes_mes.plot(kind="line", ax=ax4, marker="o")
                    ax4.set_title("Informes Procesados por Mes")
                    ax4.set(xlabel="Mes")  # más robusto que set_xlabel aislado

            if plot_position > 1:
                canvas = FigureCanvasTkAgg(fig, master=self.dashboard_canvas_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
            else:
                ctk.CTkLabel(
                    self.dashboard_canvas_frame, text="No hay suficientes datos válidos para generar gráficos."
                ).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error de Dashboard", f"No se pudo generar el dashboard: {e}")

    def _create_kpi_card(self, title, value, col):
        self.kpi_frame.grid_columnconfigure(col, weight=1)
        card = ctk.CTkFrame(self.kpi_frame, border_width=1, border_color="#565b5e")
        card.grid(row=0, column=col, sticky="ew", padx=10)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 2))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=22)).pack(pady=(2, 10))

    # =========================
    # Estilo de tabla (Treeview)
    # =========================
    def setup_treeview_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")  # look & feel moderno y estable en Windows

        # Cuerpo de la tabla
        style.configure(
            "Custom.Treeview",
            background="#1f2124",
            fieldbackground="#1f2124",
            foreground="#e9ecef",
            rowheight=30,
            borderwidth=0,
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#2b6cb0")],
            foreground=[("selected", "white")],
        )

        # Encabezados
        style.configure(
            "Custom.Treeview.Heading",
            background="#262a2e",
            foreground="#e9ecef",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
        )
        style.map("Custom.Treeview.Heading", background=[("active", "#2d3136")])
        return style

    # =========================
    # Tema claro/oscuro
    # =========================
    def change_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Light")
            self.set_status("Tema claro activado.")
        else:
            ctk.set_appearance_mode("Dark")
            self.set_status("Tema oscuro activado.")


if __name__ == "__main__":
    app = App()
    app.mainloop()