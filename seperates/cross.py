import pandas as pd

# Load your sheets
css_df = pd.read_excel("css_cloned.xlsx")  # CSS rules
elements_df = pd.read_excel("elements_grouped_unique.xlsx")  # Elements + classes

# Ask user for element
element_choice = input("Enter the element you want (e.g. div, h1, span): ").strip()

# Get the row for that element
row = elements_df[elements_df["Element"] == element_choice]

if row.empty:
    print(f"Element '{element_choice}' not found.")
else:
    # Extract its classes
    classes = row["Classes"].iloc[0].split(", ")
    print(f"Classes for {element_choice}: {classes}")

    # Collect matching CSS rules
    matches = pd.DataFrame()
    for cls in classes:
        selector = "." + cls  # CSS class format
        temp = css_df[css_df["Selector/Element"].str.contains(selector, na=False)]
        if not temp.empty:
            matches = pd.concat([matches, temp])

    if matches.empty:
        print("❌ No CSS rules found for this element.")
    else:
        print("✅ Matching CSS rules found:")
        print(matches)

        # Save results
        output_file = f"{element_choice}_css_lookup.xlsx"
        matches.to_excel(output_file, index=False)
        print(f"💾 Saved to {output_file}")


import pandas as pd


def lookup_element_css(
    element_choice,
    css_file="css_cloned.xlsx",
    elements_file="elements_grouped_unique.xlsx",
):
    # Load your sheets
    css_df = pd.read_excel(css_file)  # CSS rules
    elements_df = pd.read_excel(elements_file)  # Elements + classes

    element_choice = element_choice.strip()

    # Get the row for that element
    row = elements_df[elements_df["Element"] == element_choice]

    if row.empty:
        print(f"❌ Element '{element_choice}' not found.")
        return None

    # Extract its classes
    classes = row["Classes"].iloc[0].split(", ")
    print(f"🔎 Classes for {element_choice}: {classes}")

    # Collect matching CSS rules
    matches = pd.DataFrame()
    for cls in classes:
        selector = "." + cls  # CSS class format
        temp = css_df[css_df["Selector/Element"].str.contains(selector, na=False)]
        if not temp.empty:
            matches = pd.concat([matches, temp], ignore_index=True)

    if matches.empty:
        print("❌ No CSS rules found for this element.")
        return pd.DataFrame()  # return empty DataFrame

    print("✅ Matching CSS rules found:")
    print(matches)

    # Save results
    output_file = f"{element_choice}_css_lookup.xlsx"
    matches.to_excel(output_file, index=False)
    print(f"💾 Saved to {output_file}")

    return matches
