# Analisis: `procesador_ihq.py` / `procesador_ihq_biomarcadores.py`

## Rol en v2.5
- `procesador_ihq.py` mantiene las reglas especificas para informes IHQ (datos base de 55 columnas).
- `procesador_ihq_biomarcadores.py` expande esas reglas con biomarcadores, estudios solicitados y persistencia en SQLite.

## Flujo principal
1. Recibe texto normalizado desde `ocr_processing.pdf_to_text_enhanced`.
2. `_iter_reports` segmenta el PDF en bloques por codigo IHQ###### (maneja variantes OCR).
3. `procesador_ihq.extract_ihq_data` extrae campos base (identificacion, servicios, organos, descripciones).
4. `procesador_ihq.map_to_excel_format` arma las 55 columnas historicas.
5. `_extract_biomarkers` agrega HER2, Ki-67, RE, RP, PD-L1, P16 y estudios solicitados con heuristicas tolerantes a errores.
6. `database_manager.save_records` escribe el diccionario final en SQLite (evitando duplicados).

## Heuristicas destacadas
- Limpieza de tokens (IHQ######, estudios solicitados, nombres de marcadores).
- Normalizacion de porcentajes y estados (positivo/negativo) para RE/RP, Ki-67.
- Soporte para TPS/CPS en PD-L1 y correcciones comunes (PL6 -> P16, etc.).

## Salida
- Diccionario con columnas base + columnas IHQ_* adicionales.
- Orden de columnas preservado para compatibilidad con analitica y posibles exportaciones.

## Interaccion con otros modulos
- Usa `ocr_processing` para obtener texto, `database_manager` para persistir y `huv_constants` para valores por defecto.
- El dashboard lee directamente las columnas agregadas por este procesador.

## Mejoras pendientes
- Parametrizar el conjunto de biomarcadores para habilitar ampliaciones sin editar regex.
- Registrar metadatos de calidad (por ejemplo, confianza OCR) para analisis posteriores.
- Integrar pruebas unitarias que verifiquen cada biomarcador con PDFs sintenticos.
