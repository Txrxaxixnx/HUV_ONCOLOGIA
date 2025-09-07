# Procesadores por tipo de informe (Prototipos)

Este directorio contiene prototipos de procesadores específicos por tipo de informe.

- `autopsy_processor.py`: reglas y patrones específicos para Autopsias.
- `ihq_processor.py`: reglas y patrones específicos para Inmunohistoquímica.

Notas importantes:
- La extracción estable sigue centralizada en `data_extraction.extract_huv_data` usando `huv_constants.PATTERNS_HUV`.
- Estos módulos sirven de base para la futura modularización: separar `PATTERNS_BASE` (comunes) y especializaciones por tipo.
- Si vas a añadir un tipo nuevo, consulta `analisis/13_processors.md` para convenciones, flujo y riesgos.
