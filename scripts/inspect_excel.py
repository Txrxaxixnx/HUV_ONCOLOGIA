#!/usr/bin/env python3
import json
from pathlib import Path
import pandas as pd

def main():
    p1 = Path('EJEMPLO DE LO QUE TENGO.xlsx')
    p2 = Path('BD_JULIO PARA ENSAYO IA.xlsx')
    out = {}
    if p1.exists():
        try:
            df1 = pd.read_excel(p1)
            out['ejemplo_columns'] = list(map(str, df1.columns))
            out['ejemplo_first_row'] = df1.iloc[0].astype(str).to_dict() if len(df1)>0 else {}
        except Exception as e:
            out['ejemplo_error'] = str(e)
    else:
        out['ejemplo_error'] = 'missing'

    if p2.exists():
        try:
            df2 = pd.read_excel(p2, header=1)
            out['bdjulio_columns'] = list(map(str, df2.columns))
            out['bdjulio_ncols'] = len(df2.columns)
        except Exception as e:
            out['bdjulio_error'] = str(e)
    else:
        out['bdjulio_error'] = 'missing'

    print(json.dumps(out, ensure_ascii=False))

if __name__ == '__main__':
    main()

