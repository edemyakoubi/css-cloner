# Run after clone.py

import pandas as pd


css_df = pd.read_excel("css_cloned.xlsx")

keywords = ["font", "color", "bg", "background", "button", "btn"]


filtered_rows = []

for i, row in css_df.iterrows():
    prop = str(row["Property"]).lower()
    selector = str(row["Selector/Element"]).lower()
    for kw in keywords:
        if kw in prop or kw in selector:
            filtered_rows.append(row)
            break

filtered_df = pd.DataFrame(filtered_rows)
filtered_df.to_excel("css_fast_clone.xlsx", index=False)
print(f"{len(filtered_rows)} rows found. Saved to css_fonts_colors.xlsx")
