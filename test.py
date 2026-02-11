import pandas as pd
import json

df = pd.read_excel("listf.xlsx")

# Keep only needed columns
df = df[["psno", "subdivision", "psname","area"]]

data = df.to_dict(orient="records")

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
