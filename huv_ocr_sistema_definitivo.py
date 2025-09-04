#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Punto de entrada principal para el sistema OCR del HUV."""

import tkinter as tk

from ui import HUVOCRSystem


def main() -> None:
    """Inicializa la interfaz y arranca el sistema."""
    root = tk.Tk()
    HUVOCRSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
