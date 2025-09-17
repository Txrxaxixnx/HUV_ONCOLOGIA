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
import numpy as np

from calendario import CalendarioInteligente
from huv_web_automation import automatizar_entrega_resultados, Credenciales

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

        try:
            from ttkbootstrap import Style as TBStyle
            self._tbstyle = TBStyle(theme="darkly")  # puedes usar otro tema si prefieres
        except Exception as e:
            self._tbstyle = None
            print(f"[WARN] ttkbootstrap no inicializado ({e}). Usando ttk estándar.")

        self._init_treeview_style()
        
        # ---------- Ventana principal ----------
        self.title("EVARISIS Gestor HUV")
        self.state('zoomed')       # Y añadimos esta, ¡listo el pollo!
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

        self.btn_webauto = ctk.CTkButton(
            self.nav_frame, text="Automatizar BD Web", command=self.open_web_auto_modal, height=40
        )
        self.btn_webauto.grid(row=4, column=0, padx=20, pady=12, sticky="ew")

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
        self.after(10, self.state, 'zoomed')


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
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=0)  # sidebar
        frame.grid_columnconfigure(1, weight=1)  # main area

        # Sidebar de filtros (colapsable)
        self.db_filters = {
            "fecha_desde": ctk.StringVar(value=""),
            "fecha_hasta": ctk.StringVar(value=""),
            "servicio": ctk.StringVar(value=""),
            "malignidad": ctk.StringVar(value=""),
            "responsable": ctk.StringVar(value=""),
        }
        self.db_sidebar_collapsed = True
        self.db_sidebar = ctk.CTkFrame(frame, fg_color=SURFACE, corner_radius=12, width=280)
        self.db_sidebar.grid_rowconfigure(10, weight=1)

        ctk.CTkLabel(self.db_sidebar, text="Filtros", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=14, pady=(12, 6), sticky="w")
        ctk.CTkLabel(self.db_sidebar, text="Fecha desde (dd/mm/aaaa)").grid(row=1, column=0, padx=14, pady=(6, 2), sticky="w")
        ctk.CTkEntry(self.db_sidebar, textvariable=self.db_filters["fecha_desde"]).grid(row=2, column=0, padx=14, pady=(0, 6), sticky="ew")
        ctk.CTkLabel(self.db_sidebar, text="Fecha hasta (dd/mm/aaaa)").grid(row=3, column=0, padx=14, pady=(6, 2), sticky="w")
        ctk.CTkEntry(self.db_sidebar, textvariable=self.db_filters["fecha_hasta"]).grid(row=4, column=0, padx=14, pady=(0, 6), sticky="ew")
        ctk.CTkLabel(self.db_sidebar, text="Servicio").grid(row=5, column=0, padx=14, pady=(10, 2), sticky="w")
        self.cmb_servicio = ctk.CTkComboBox(self.db_sidebar, values=[], variable=self.db_filters["servicio"])
        self.cmb_servicio.grid(row=6, column=0, padx=14, pady=(0, 6), sticky="ew")
        ctk.CTkLabel(self.db_sidebar, text="Malignidad").grid(row=7, column=0, padx=14, pady=(10, 2), sticky="w")
        self.cmb_malig = ctk.CTkComboBox(self.db_sidebar, values=["", "PRESENTE", "AUSENTE"], variable=self.db_filters["malignidad"])
        self.cmb_malig.grid(row=8, column=0, padx=14, pady=(0, 6), sticky="ew")
        ctk.CTkLabel(self.db_sidebar, text="Responsable").grid(row=9, column=0, padx=14, pady=(10, 2), sticky="w")
        self.cmb_resp = ctk.CTkComboBox(self.db_sidebar, values=[], variable=self.db_filters["responsable"])
        self.cmb_resp.grid(row=10, column=0, padx=14, pady=(0, 6), sticky="ew")
        btns = ctk.CTkFrame(self.db_sidebar, fg_color="transparent")
        btns.grid(row=11, column=0, padx=14, pady=(12, 14), sticky="ew")
        ctk.CTkButton(btns, text="Refrescar", command=self._refresh_dashboard).pack(side="left", expand=True, fill="x")
        ctk.CTkButton(btns, text="Limpiar", command=self._clear_filters).pack(side="left", expand=True, fill="x", padx=(8,0))

        # Área principal con toolbar + pestañas
        main = ctk.CTkFrame(frame, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        toolbar = ctk.CTkFrame(main, fg_color=BG)
        toolbar.grid(row=0, column=0, sticky="ew", padx=2, pady=(2, 6))
        self.btn_toggle_sidebar = ctk.CTkButton(toolbar, text="≡ Mostrar filtros", width=140, command=self._toggle_db_sidebar)
        self.btn_toggle_sidebar.pack(side="left", padx=(6, 8), pady=4)
        ctk.CTkButton(toolbar, text="Filtros…", width=100, command=self._open_filters_sheet).pack(side="left", padx=(0, 8), pady=4)

        self.tabs = ttk.Notebook(main)
        self.tabs.grid(row=1, column=0, sticky="nsew")

        self.tab_overview   = ctk.CTkFrame(self.tabs, fg_color="transparent")
        self.tab_biomarkers = ctk.CTkFrame(self.tabs, fg_color="transparent")
        self.tab_times      = ctk.CTkFrame(self.tabs, fg_color="transparent")
        self.tab_quality    = ctk.CTkFrame(self.tabs, fg_color="transparent")
        self.tab_compare    = ctk.CTkFrame(self.tabs, fg_color="transparent")

        for t in [self.tab_overview, self.tab_biomarkers, self.tab_times, self.tab_quality, self.tab_compare]:
            t.grid_columnconfigure(0, weight=1)
            t.grid_columnconfigure(1, weight=1)

        self.tabs.add(self.tab_overview,   text="Overview")
        self.tabs.add(self.tab_biomarkers, text="Biomarcadores")
        self.tabs.add(self.tab_times,      text="Tiempos")
        self.tabs.add(self.tab_quality,    text="Calidad")
        self.tabs.add(self.tab_compare,    text="Comparador")

        self._dash_canvases = []
        # Sidebar iniciará colapsado (no grid)
        return frame


    # ---------- Helpers Dashboard ----------

    def _clear_filters(self):
        for k in self.db_filters:
            self.db_filters[k].set("")
        self._refresh_dashboard()

    def _refresh_dashboard(self):
        try:
            self.set_status("Actualizando dashboard…")
            self.cargar_dashboard()
        finally:
            self.set_status("Dashboard actualizado.")

    def _get_filtered_df(self, df):
        dff = df.copy()
        fd = self.db_filters["fecha_desde"].get().strip()
        fh = self.db_filters["fecha_hasta"].get().strip()
        if fd:
            d0 = pd.to_datetime(fd, dayfirst=True, errors="coerce")
            if pd.notna(d0):
                dff = dff[dff["_fecha_informe"] >= d0]
        if fh:
            d1 = pd.to_datetime(fh, dayfirst=True, errors="coerce")
            if pd.notna(d1):
                dff = dff[dff["_fecha_informe"] <= d1]

        srv = self.db_filters["servicio"].get().strip()
        if srv:
            dff = dff[dff.get("Servicio", "").astype(str).eq(srv)]
        mal = self.db_filters["malignidad"].get().strip()
        if mal:
            dff = dff[dff.get("Malignidad", "").astype(str).str.upper().eq(mal)]
        rsp = self.db_filters["responsable"].get().strip()
        if rsp:
            dff = dff[dff.get("Usuario finalizacion", "").astype(str).eq(rsp)]
        return dff

    def _clear_dash_area(self):
        # Desmonta los canvases previos para liberar memoria
        for cv in getattr(self, "_dash_canvases", []):
            try:
                cv.get_tk_widget().destroy()
            except Exception:
                pass
        self._dash_canvases = []

        # Limpia frames hijos en cada pestaña
        for tab in [self.tab_overview, self.tab_biomarkers, self.tab_times, self.tab_quality, self.tab_compare]:
            for child in tab.grid_slaves():
                child.destroy()

    def _chart_in(self, tab, row, col, render_fn, title, dff):
        card = ctk.CTkFrame(tab, fg_color=SURFACE, corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        tab.grid_rowconfigure(row, weight=1)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(header, text=title, text_color=TEXT, font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="⛶ Pantalla completa", width=150,
                      command=lambda: self._open_fullscreen_figure(render_fn, title, dff)).pack(side="right")

        try:
            fig = render_fn()
            if fig is None:
                ctk.CTkLabel(card, text="(sin datos)", text_color=MUTED).pack(padx=10, pady=10)
                return
            canvas = FigureCanvasTkAgg(fig, master=card)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.pack(fill="both", expand=True, padx=8, pady=8)
            widget.bind("<Double-Button-1>", lambda e: self._open_fullscreen_figure(render_fn, title, dff))
            self._dash_canvases.append(canvas)
        except Exception as e:
            ctk.CTkLabel(card, text=f"Error: {e}", text_color=MUTED).pack(padx=10, pady=10)

    def _toggle_db_sidebar(self):
        # Muestra/oculta el sidebar, ajusta texto del botón y grid
        if self.db_sidebar_collapsed:
            self.db_sidebar.grid(row=0, column=0, sticky="ns", padx=(0, 12), pady=6)
            self.btn_toggle_sidebar.configure(text="✕ Ocultar filtros")
        else:
            self.db_sidebar.grid_forget()
            self.btn_toggle_sidebar.configure(text="≡ Mostrar filtros")
        self.db_sidebar_collapsed = not self.db_sidebar_collapsed

    def _open_filters_sheet(self):
        # Modal de filtros (para no robar ancho)
        top = ctk.CTkToplevel(self)
        top.title("Filtros")
        top.geometry("420x420")
        top.grab_set()
        wrap = ctk.CTkFrame(top, fg_color=BG)
        wrap.pack(fill="both", expand=True, padx=12, pady=12)

        def row(lbl, widget):
            r = ctk.CTkFrame(wrap, fg_color="transparent"); r.pack(fill="x", pady=6)
            ctk.CTkLabel(r, text=lbl, width=160, anchor="w").pack(side="left")
            widget.pack(in_=r, side="left", fill="x", expand=True)

        e1 = ctk.CTkEntry(wrap, textvariable=self.db_filters["fecha_desde"])
        e2 = ctk.CTkEntry(wrap, textvariable=self.db_filters["fecha_hasta"])
        cb1 = ctk.CTkComboBox(wrap, values=self.cmb_servicio.cget("values"), variable=self.db_filters["servicio"])
        cb2 = ctk.CTkComboBox(wrap, values=self.cmb_malig.cget("values"), variable=self.db_filters["malignidad"])
        cb3 = ctk.CTkComboBox(wrap, values=self.cmb_resp.cget("values"), variable=self.db_filters["responsable"])

        row("Fecha desde (dd/mm/aaaa)", e1)
        row("Fecha hasta (dd/mm/aaaa)", e2)
        row("Servicio", cb1)
        row("Malignidad", cb2)
        row("Responsable", cb3)

        btns = ctk.CTkFrame(wrap, fg_color="transparent"); btns.pack(fill="x", pady=(10,0))
        ctk.CTkButton(btns, text="Aplicar", command=lambda:(self._refresh_dashboard(), top.destroy())).pack(side="left", expand=True, fill="x", padx=(0,6))
        ctk.CTkButton(btns, text="Limpiar", command=self._clear_filters).pack(side="left", expand=True, fill="x", padx=(6,0))

    def _open_fullscreen_figure(self, render_fn, title, dff):
        # Ventana a pantalla completa con inspector lateral
        fs = ctk.CTkToplevel(self)
        fs.title(title)
        try:
            fs.state('zoomed')
        except Exception:
            pass
        fs.configure(fg_color=BG)
        fs.grid_rowconfigure(0, weight=1)
        fs.grid_columnconfigure(0, weight=1)
        fs.grid_columnconfigure(1, weight=0)

        # Área de gráfico
        graph_area = ctk.CTkFrame(fs, fg_color=SURFACE, corner_radius=12)
        graph_area.grid(row=0, column=0, sticky="nsew", padx=(10,6), pady=10)
        fig = render_fn()
        if fig is None:
            ctk.CTkLabel(graph_area, text="(sin datos)", text_color=MUTED).pack(padx=12, pady=12)
        else:
            canv = FigureCanvasTkAgg(fig, master=graph_area)
            canv.draw()
            canv.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Inspector lateral
        insp = ctk.CTkFrame(fs, fg_color=SURFACE, corner_radius=12, width=300)
        insp.grid(row=0, column=1, sticky="ns", padx=(6,10), pady=10)
        ctk.CTkLabel(insp, text="Inspector", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=12, pady=(12,6))
        self._build_inspector(insp, title, dff)

        # Barra superior simple (cerrar)
        topbar = ctk.CTkFrame(graph_area, fg_color="transparent")
        topbar.pack(fill="x", padx=10, pady=(10,0))
        ctk.CTkLabel(topbar, text=title, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        ctk.CTkButton(topbar, text="Cerrar", width=80, command=fs.destroy).pack(side="right")

    def _build_inspector(self, parent, title, dff):
        # Datos generales
        n = len(dff)
        fmin = pd.to_datetime(dff.get("_fecha_informe"), errors="coerce").min()
        fmax = pd.to_datetime(dff.get("_fecha_informe"), errors="coerce").max()
        rng = f"{fmin:%d/%m/%Y} – {fmax:%d/%m/%Y}" if pd.notna(fmin) and pd.notna(fmax) else "—"

        def row(k, v):
            r = ctk.CTkFrame(parent, fg_color="transparent"); r.pack(fill="x", padx=12, pady=4)
            ctk.CTkLabel(r, text=k, text_color=MUTED).pack(side="left")
            ctk.CTkLabel(r, text=v, text_color=TEXT).pack(side="right")

        row("Registros filtrados", f"{n:,}".replace(",", "."))
        row("Rango de fechas", rng)

        # Secciones condicionales útiles
        if "Malignidad" in dff.columns:
            ser = dff["Malignidad"].astype(str).str.upper().value_counts()
            box = ctk.CTkFrame(parent, fg_color=BG, corner_radius=10); box.pack(fill="x", padx=12, pady=(10,4))
            ctk.CTkLabel(box, text="Malignidad", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8,2))
            for k,v in ser.items():
                rowtxt = ctk.CTkFrame(box, fg_color="transparent"); rowtxt.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(rowtxt, text=f"{k}").pack(side="left")
                ctk.CTkLabel(rowtxt, text=str(v)).pack(side="right")

        if "Organo (1. Muestra enviada a patología)" in dff.columns:
            top_org = dff["Organo (1. Muestra enviada a patología)"].astype(str).replace({"": "No especificado"}).value_counts().head(8)
        elif "IHQ_ORGANO" in dff.columns:
            top_org = dff["IHQ_ORGANO"].astype(str).replace({"": "No especificado"}).value_counts().head(8)
        else:
            top_org = None

        if top_org is not None and not top_org.empty:
            box2 = ctk.CTkFrame(parent, fg_color=BG, corner_radius=10); box2.pack(fill="x", padx=12, pady=(10,12))
            ctk.CTkLabel(box2, text="Top Órganos", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8,2))
            for k,v in top_org.items():
                rowtxt = ctk.CTkFrame(box2, fg_color="transparent"); rowtxt.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(rowtxt, text=f"{k}").pack(side="left")
                ctk.CTkLabel(rowtxt, text=str(v)).pack(side="right")

    # ---------- Renderers: Overview ----------

    def _g_line_informes_por_mes(self, df):
        if df.empty or df["_fecha_informe"].isna().all():
            return None
        ser = df.dropna(subset=["_fecha_informe"]).set_index("_fecha_informe").resample("MS").size()
        fig = Figure(figsize=(5.6, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(ser.index, ser.values, marker="o")
        ax.set_title("Informes por mes")
        ax.set_xlabel("Mes")
        ax.set_ylabel("Conteo")
        fig.tight_layout()
        return fig

    def _g_pie_malignidad(self, df):
        if "Malignidad" not in df.columns or df.empty:
            return None
        ser = df["Malignidad"].astype(str).str.upper().replace({"": "DESCONOCIDO"}).value_counts()
        if ser.empty: return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(ser.values, labels=ser.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Distribución de Malignidad")
        fig.tight_layout()
        return fig

    def _g_bar_top_servicio(self, df, top=12):
        if "Servicio" not in df.columns or df.empty:
            return None
        ser = df["Servicio"].astype(str).value_counts().head(top)
        if ser.empty: return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(ser.index, ser.values)
        ax.set_title(f"Top Servicios (n={ser.sum()})")
        ax.set_ylabel("Informes")
        ax.tick_params(axis="x", rotation=30, labelsize=8)
        fig.tight_layout()
        return fig

    def _g_bar_top_organo(self, df, top=12):
        # soporta tanto columna Excel como IHQ_ORGANO
        col = "Organo (1. Muestra enviada a patología)" if "Organo (1. Muestra enviada a patología)" in df.columns else ("IHQ_ORGANO" if "IHQ_ORGANO" in df.columns else None)
        if not col: return None
        ser = df[col].astype(str).replace({"": "No especificado"}).value_counts().head(top)
        if ser.empty: return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(ser.index, ser.values)
        ax.set_title("Top Órganos")
        ax.set_ylabel("Informes")
        ax.tick_params(axis="x", rotation=30, labelsize=8)
        fig.tight_layout()
        return fig

    # ---------- Renderers: Biomarcadores ----------

    def _g_hist_ki67(self, df):
        col = "IHQ_KI-67" if "IHQ_KI-67" in df.columns else None
        if not col: return None
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if s.empty: return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.hist(s.values, bins=12)
        ax.set_title("Ki-67 (%)")
        ax.set_xlabel("%")
        ax.set_ylabel("Frecuencia")
        fig.tight_layout()
        return fig

    def _g_bar_her2(self, df):
        col = "IHQ_HER2" if "IHQ_HER2" in df.columns else None
        if not col: return None
        order = ["0", "1+", "2+", "3+", "NEGATIVO", "POSITIVO"]
        ser = df[col].astype(str).str.upper().value_counts()
        ser = ser.reindex(order, fill_value=0) if any(k in ser.index for k in order) else ser
        if ser.sum() == 0: return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        ax.bar(ser.index, ser.values)
        ax.set_title("HER2 (score)")
        ax.set_ylabel("Informes")
        fig.tight_layout()
        return fig

    def _g_bar_re_rp(self, df):
        cols = [c for c in ["IHQ_RECEPTOR_ESTROGENO", "IHQ_RECEPTOR_PROGESTAGENOS"] if c in df.columns]
        if not cols: return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        data = []
        labels = []
        for c in cols:
            ser = df[c].astype(str).str.upper().replace({"": "ND"}).value_counts()
            data.append(ser)
            labels.append(c.replace("IHQ_", ""))
        # Normaliza categorías
        cats = sorted(set().union(*[d.index for d in data]))
        mat = np.array([[d.get(k, 0) for k in cats] for d in data])
        for i, row in enumerate(mat):
            ax.bar(np.arange(len(cats))+i*0.35, row, width=0.35, label=labels[i])
        ax.set_xticks(np.arange(len(cats))+0.35/2)
        ax.set_xticklabels(cats, rotation=0)
        ax.set_title("RE / RP (estado)")
        ax.legend()
        fig.tight_layout()
        return fig

    def _g_bar_pdl1(self, df):
        # intenta TPS o CPS
        for col in ["IHQ_PDL-1", "IHQ_PDL1_TPS", "IHQ_PDL1_CPS"]:
            if col in df.columns:
                s = df[col].astype(str)
                break
        else:
            return None
        ser = s.replace({"": "ND"}).value_counts()
        if ser.empty: return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        ax.bar(ser.index, ser.values)
        ax.set_title("PD-L1")
        ax.set_ylabel("Informes")
        ax.tick_params(axis="x", rotation=0)
        fig.tight_layout()
        return fig

    # ---------- Renderers: Tiempos ----------

    def _g_box_tiempo_proceso(self, df):
        f_ing = pd.to_datetime(df.get("Fecha de ingreso (2. Fecha de la muestra)", ""), dayfirst=True, errors="coerce")
        f_inf = pd.to_datetime(df.get("Fecha finalizacion (3. Fecha del informe)", df.get("Fecha de informe", "")), dayfirst=True, errors="coerce")
        dias = (f_inf - f_ing).dt.days.dropna()
        if dias.empty: return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        ax.boxplot(dias.values, vert=True)
        ax.set_title("Tiempo de proceso (días)")
        fig.tight_layout()
        return fig

    def _g_line_throughput_semana(self, df):
        if df.empty or df["_fecha_informe"].isna().all(): return None
        ser = df.dropna(subset=["_fecha_informe"]).set_index("_fecha_informe").resample("W-MON").size()
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        ax.plot(ser.index, ser.values, marker="o")
        ax.set_title("Throughput semanal")
        ax.set_xlabel("Semana")
        ax.set_ylabel("Informes")
        fig.tight_layout()
        return fig

    def _g_scatter_edad_ki67(self, df):
        if "Edad" not in df.columns: return None
        x = pd.to_numeric(df["Edad"], errors="coerce")
        y = pd.to_numeric(df.get("IHQ_KI-67", pd.Series(np.nan, index=df.index)), errors="coerce")
        m = x.notna() & y.notna()
        if not m.any(): return None
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        ax.scatter(x[m], y[m], alpha=0.6)
        ax.set_title("Edad vs Ki-67")
        ax.set_xlabel("Edad")
        ax.set_ylabel("Ki-67 (%)")
        fig.tight_layout()
        return fig

    # ---------- Renderers: Calidad ----------

    def _g_bar_missingness(self, df):
        cols = [
            "Servicio", "Malignidad", "Usuario finalizacion",
            "Organo (1. Muestra enviada a patología)", "IHQ_HER2", "IHQ_KI-67"
        ]
        present = [c for c in cols if c in df.columns]
        if not present: return None
        miss = df[present].isna().mean().sort_values(ascending=False)
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        ax.bar(miss.index, (miss.values*100.0))
        ax.set_title("Campos vacíos (%)")
        ax.set_ylabel("% vacío")
        ax.tick_params(axis="x", rotation=25)
        fig.tight_layout()
        return fig

    def _g_bar_top_responsables(self, df, top=10):
        col = "Usuario finalizacion"
        if col not in df.columns: return None
        ser = df[col].astype(str).value_counts().head(top)
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        ax.bar(ser.index, ser.values)
        ax.set_title("Productividad por responsable (Top)")
        ax.set_ylabel("Informes")
        ax.tick_params(axis="x", rotation=25)
        fig.tight_layout()
        return fig

    def _g_bar_largos_texto(self, df):
        col = "Descripcion Diagnostico (5,6,7 Tipo histológico, subtipo histológico, margenes tumorales)"
        if col not in df.columns: return None
        s = df[col].astype(str).str.len()
        bins = [0, 50, 150, 300, 600, 1200, np.inf]
        ser = pd.cut(s, bins=bins, labels=["<50", "50–150", "150–300", "300–600", "600–1200", "1200+"], include_lowest=True).value_counts().sort_index()
        fig = Figure(figsize=(5.6, 3.2), dpi=100); ax = fig.add_subplot(111)
        ax.bar(ser.index.astype(str), ser.values)
        ax.set_title("Longitud del diagnóstico (bins)")
        ax.set_ylabel("Informes")
        fig.tight_layout()
        return fig

    # ---------- Comparador parametrizable ----------

    def _build_comparator(self, tab, df):
        # Controles
        ctrl = ctk.CTkFrame(tab, fg_color="transparent")
        ctrl.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,0), sticky="ew")

        dims = [c for c in ["Servicio", "Usuario finalizacion", "Malignidad", "Organo (1. Muestra enviada a patología)"] if c in df.columns]
        mets = [c for c in ["IHQ_KI-67"] if c in df.columns]  # se pueden añadir más numéricas

        self._compare_controls["dim"] = ctk.StringVar(value=dims[0] if dims else "")
        self._compare_controls["agg"] = ctk.StringVar(value="conteo")
        self._compare_controls["met"] = ctk.StringVar(value=mets[0] if mets else "")

        row = ctk.CTkFrame(ctrl, fg_color=SURFACE, corner_radius=12)
        row.pack(fill="x", padx=4, pady=4)
        ctk.CTkLabel(row, text="Dimensión:").pack(side="left", padx=6)
        ctk.CTkComboBox(row, values=dims or [""], variable=self._compare_controls["dim"]).pack(side="left", padx=6)
        ctk.CTkLabel(row, text="Agregador:").pack(side="left", padx=6)
        ctk.CTkComboBox(row, values=["conteo", "promedio"], variable=self._compare_controls["agg"]).pack(side="left", padx=6)
        ctk.CTkLabel(row, text="Métrica:").pack(side="left", padx=6)
        ctk.CTkComboBox(row, values=mets or [""], variable=self._compare_controls["met"]).pack(side="left", padx=6)
        ctk.CTkButton(row, text="Aplicar", command=lambda: self._chart_in(tab, 1, 0, lambda: self._g_compare(df),)).pack(side="left", padx=10)

        # Gráfico inicial
        self._chart_in(tab, 1, 0, lambda: self._g_compare(df))

    def _g_compare(self, df):
        dim = self._compare_controls["dim"].get()
        agg = self._compare_controls["agg"].get()
        met = self._compare_controls["met"].get()
        if not dim or df.empty: return None

        fig = Figure(figsize=(11.6, 3.2), dpi=100); ax = fig.add_subplot(111)

        if agg == "conteo":
            ser = df[dim].astype(str).value_counts()
            ax.bar(ser.index, ser.values)
            ax.set_title(f"Conteo por {dim}")
            ax.tick_params(axis="x", rotation=25)
        else:
            if not met or met not in df.columns:
                return None
            s = pd.to_numeric(df[met], errors="coerce")
            grp = df.assign(_metric=s).groupby(dim)["_metric"].mean().dropna()
            ax.bar(grp.index, grp.values)
            ax.set_title(f"Promedio de {met} por {dim}")
            ax.tick_params(axis="x", rotation=25)

        fig.tight_layout()
        return fig

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
        # 1) Preparar DF y combos de filtros
        df = self.master_df.copy()
        if df is None or df.empty:
            self._render_kpis(df)
            self._clear_dash_area()
            return

        # Normaliza fechas (varias columnas posibles)
        df["_fecha_informe"] = pd.to_datetime(
            df.get("Fecha finalizacion (3. Fecha del informe)", df.get("Fecha de informe", df.get("Fecha de ingreso", ""))),
            dayfirst=True, errors="coerce"
        )

        # Llenar combos dinámicos (servicios / responsables)
        srv_vals = sorted([s for s in df.get("Servicio", pd.Series(dtype=str)).dropna().astype(str).unique() if s.strip()])
        rsp_vals = sorted([s for s in df.get("Usuario finalizacion", pd.Series(dtype=str)).dropna().astype(str).unique() if s.strip()])
        self.cmb_servicio.configure(values=[""] + srv_vals)
        self.cmb_resp.configure(values=[""] + rsp_vals)

        # 2) Render de KPIs básicos
        self._render_kpis(df)

        # 3) Limpiar canvases anteriores y pintar
        self._clear_dash_area()

        # Filtros iniciales (los que estén llenos)
        dff = self._get_filtered_df(df)

        # 4) PINTAR: OVERVIEW (4 gráficos)
        self._chart_in(self.tab_overview, 0, 0, lambda: self._g_line_informes_por_mes(dff), "Informes por mes", dff)
        self._chart_in(self.tab_overview, 0, 1, lambda: self._g_pie_malignidad(dff), "Distribución de Malignidad", dff)
        self._chart_in(self.tab_overview, 1, 0, lambda: self._g_bar_top_servicio(dff), "Top Servicios", dff)
        self._chart_in(self.tab_overview, 1, 1, lambda: self._g_bar_top_organo(dff), "Top Órganos", dff)

        # 5) PINTAR: BIOMARCADORES
        self._chart_in(self.tab_biomarkers, 0, 0, lambda: self._g_hist_ki67(dff), "Ki-67 (%)", dff)
        self._chart_in(self.tab_biomarkers, 0, 1, lambda: self._g_bar_her2(dff), "HER2 (score)", dff)
        self._chart_in(self.tab_biomarkers, 1, 0, lambda: self._g_bar_re_rp(dff), "RE / RP (estado)", dff)
        self._chart_in(self.tab_biomarkers, 1, 1, lambda: self._g_bar_pdl1(dff), "PD-L1", dff)

        # 6) PINTAR: TIEMPOS
        self._chart_in(self.tab_times, 0, 0, lambda: self._g_box_tiempo_proceso(dff), "Tiempo de proceso (días)", dff)
        self._chart_in(self.tab_times, 0, 1, lambda: self._g_line_throughput_semana(dff), "Throughput semanal", dff)
        self._chart_in(self.tab_times, 1, 0, lambda: self._g_scatter_edad_ki67(dff), "Edad vs Ki-67", dff)

        # 7) PINTAR: CALIDAD
        self._chart_in(self.tab_quality, 0, 0, lambda: self._g_bar_missingness(dff), "Campos vacíos (%)", dff)
        self._chart_in(self.tab_quality, 0, 1, lambda: self._g_bar_top_responsables(dff), "Productividad por responsable", dff)
        self._chart_in(self.tab_quality, 1, 0, lambda: self._g_bar_largos_texto(dff), "Longitud del diagnóstico", dff)

        # 8) PINTAR: COMPARADOR
        self._build_comparator(self.tab_compare, dff)


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
    # ---------- Automatización Web (modal + ejecución) ----------

    def open_web_auto_modal(self):
        top = ctk.CTkToplevel(self)
        top.title("Automatizar Entrega de Resultados")
        top.geometry("460x360")
        top.grab_set()

        top.transient(self)
        try:
            top.lift(); top.focus_force()
        except Exception:
            pass
        
        # Campos
        frm = ctk.CTkFrame(top, fg_color=SURFACE, corner_radius=12)
        frm.pack(fill="both", expand=True, padx=12, pady=12)

        # Usuario / Clave
        ctk.CTkLabel(frm, text="Usuario").grid(row=0, column=0, padx=10, pady=(12,6), sticky="w")
        user_var = ctk.StringVar(value="12345")
        ctk.CTkEntry(frm, textvariable=user_var).grid(row=0, column=1, padx=10, pady=(12,6), sticky="ew")

        ctk.CTkLabel(frm, text="Contraseña").grid(row=1, column=0, padx=10, pady=6, sticky="w")
        pass_var = ctk.StringVar(value="CONSULTA1")
        ctk.CTkEntry(frm, textvariable=pass_var, show="•").grid(row=1, column=1, padx=10, pady=6, sticky="ew")

        # Criterio
        ctk.CTkLabel(frm, text="Buscar por").grid(row=2, column=0, padx=10, pady=6, sticky="w")
        criterio_var = ctk.StringVar(value="Fecha de Ingreso")
        ctk.CTkComboBox(frm, values=["Fecha de Ingreso", "Fecha de Finalizacion", "Rango de Peticion", "Datos del Paciente"], variable=criterio_var).grid(row=2, column=1, padx=10, pady=6, sticky="ew")

        # Fechas
        fi_var = ctk.StringVar(value="")
        ff_var = ctk.StringVar(value="")

        def pick_fi():
            sel = CalendarioInteligente.seleccionar_fecha(parent=top, locale='es_CO', codigo_pais_festivos='CO')
            if sel:
                fi_var.set(sel.strftime("%d/%m/%Y"))
            # RE-ADQUIRIR MODAL Y TRAER AL FRENTE
            try:
                top.deiconify()
                # truco para traer al frente en Windows
                top.attributes("-topmost", True); top.attributes("-topmost", False)
                top.lift(); top.focus_force(); top.grab_set()
            except Exception:
                pass

        def pick_ff():
            sel = CalendarioInteligente.seleccionar_fecha(parent=top, locale='es_CO', codigo_pais_festivos='CO')
            if sel:
                ff_var.set(sel.strftime("%d/%m/%Y"))
            # RE-ADQUIRIR MODAL Y TRAER AL FRENTE
            try:
                top.deiconify()
                top.attributes("-topmost", True); top.attributes("-topmost", False)
                top.lift(); top.focus_force(); top.grab_set()
            except Exception:
                pass

        ctk.CTkLabel(frm, text="Fecha inicial").grid(row=3, column=0, padx=10, pady=6, sticky="w")
        row_fi = ctk.CTkFrame(frm, fg_color="transparent"); row_fi.grid(row=3, column=1, padx=10, pady=6, sticky="ew")
        ctk.CTkEntry(row_fi, textvariable=fi_var).pack(side="left", fill="x", expand=True, padx=(0,6))
        ctk.CTkButton(row_fi, text="Elegir…", width=80, command=pick_fi).pack(side="left")

        ctk.CTkLabel(frm, text="Fecha final").grid(row=4, column=0, padx=10, pady=6, sticky="w")
        row_ff = ctk.CTkFrame(frm, fg_color="transparent"); row_ff.grid(row=4, column=1, padx=10, pady=6, sticky="ew")
        ctk.CTkEntry(row_ff, textvariable=ff_var).pack(side="left", fill="x", expand=True, padx=(0,6))
        ctk.CTkButton(row_ff, text="Elegir…", width=80, command=pick_ff).pack(side="left")

        # Botones
        btns = ctk.CTkFrame(frm, fg_color="transparent"); btns.grid(row=5, column=0, columnspan=2, pady=(12,8), sticky="ew")
        ctk.CTkButton(btns, text="Cancelar", command=top.destroy).pack(side="right", padx=6)
        def go():
            top.destroy()
            self._start_web_automation(
                fi_var.get().strip(), ff_var.get().strip(),
                user_var.get().strip(), pass_var.get().strip(),
                criterio_var.get().strip()
            )
        ctk.CTkButton(btns, text="Iniciar", command=go).pack(side="right", padx=6)

        # grid conf
        frm.grid_columnconfigure(1, weight=1)

    def _start_web_automation(self, fi, ff, user, pwd, criterio):
        if not fi or not ff:
            messagebox.showwarning("Fechas requeridas", "Debe seleccionar fecha inicial y final.")
            return
        self.set_status("Automatizando Entrega de resultados…")
        t = threading.Thread(target=self._run_web_automation, args=(fi, ff, user, pwd, criterio), daemon=True)
        t.start()

    def _run_web_automation(self, fi, ff, user, pwd, criterio):
        try:
            ok = automatizar_entrega_resultados(
                fecha_inicial_ddmmaa=fi,
                fecha_final_ddmmaa=ff,
                cred=Credenciales(usuario=user, clave=pwd),
                criterio=criterio,
                headless=False,
                log_cb=self._log_auto
            )
            if ok:
                self.set_status("Consulta web completada. Revise resultados en el navegador.")
                messagebox.showinfo("Automatización", "Consulta completada en el portal.")
            else:
                self.set_status("Automatización: sin resultado.")
        except Exception as e:
            self.set_status(f"Error en automatización: {e}")
            messagebox.showerror("Automatización", f"Ocurrió un error:\n{e}")

    def _log_auto(self, msg: str):
        try:
            # Si está visible el textbox de logs de Procesar, úsalo; si no, status.
            if hasattr(self, "log_textbox") and str(self.log_textbox.winfo_exists()) == "1":
                self.log_textbox.configure(state="normal")
                self.log_textbox.insert("end", f"[AUTO] {msg}\n")
                self.log_textbox.configure(state="disabled")
                self.log_textbox.see("end")
            else:
                self.set_status(msg)
        except Exception:
            self.set_status(msg)

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

    def _init_treeview_style(self):
        """
        Define el estilo 'Custom.Treeview' y su heading. Usa colores por defecto si no existen constantes.
        """
        try:
            from tkinter import ttk as _ttk
            s = _ttk.Style()

            # Fallbacks por si no tienes BG/SURFACE/TEXT/ACCENT definidos
            bg      = globals().get("BG", "#1a1b1e")
            surface = globals().get("SURFACE", "#23262b")
            text    = globals().get("TEXT", "#eaeaea")
            accent  = globals().get("ACCENT", "#2f8bfd")

            s.configure(
                "Custom.Treeview",
                background=bg,
                fieldbackground=bg,
                foreground=text,
                rowheight=26,
                borderwidth=0,
            )
            s.map(
                "Custom.Treeview",
                background=[("selected", accent)],
                foreground=[("selected", "white")],
            )
            s.configure(
                "Custom.Treeview.Heading",
                background=surface,
                foreground=text,
                relief="flat",
                padding=6,
            )
        except Exception as e:
            print(f"[WARN] No se pudo configurar Custom.Treeview: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()