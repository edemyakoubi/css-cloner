import pandas as pd
import os


css_df = pd.read_excel("css_cloned.xlsx")
elements_df = pd.read_excel("elements_grouped_unique.xlsx")

output_folder = "css_lookup_results"
os.makedirs(output_folder, exist_ok=True)

# Loop through each element in sheet 2
for _, row in elements_df.iterrows():
    element = row["Element"]
    classes = str(row["Classes"]).split(", ") if pd.notna(row["Classes"]) else []

    matches = pd.DataFrame()

    # Search for each class in sheet 1
    for cls in classes:
        selector = "." + cls.strip()  # CSS class format
        temp = css_df[css_df["Selector/Element"].str.contains(selector, na=False)]
        if not temp.empty:
            matches = pd.concat([matches, temp])

    # Save if there are matches
    if not matches.empty:
        output_file = os.path.join(output_folder, f"{element}_css_lookup.xlsx")
        matches.to_excel(output_file, index=False)
        print(f"Saved CSS rules for <{element}> to {output_file}")
    else:
        print(f"No CSS rules found for <{element}>")

print("\n Process finished! All results are inside the 'css_lookup_results' folder.")
