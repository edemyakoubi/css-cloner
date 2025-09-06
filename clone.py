from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import defaultdict
import re
import os


def extract_elements_to_excel(url, output_file="elements_grouped_unique.xlsx"):
    # Fetch page
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")

    # Collect elements and their classes
    element_dict = defaultdict(set)  # avoid duplicates
    for el in soup.find_all(True):
        tag = el.name
        classes = el.get("class")
        if classes:
            for cls in classes:
                element_dict[tag].add(cls)
        else:
            element_dict[tag].add("")  # add empty string if no class

    # Prepare rows for Excel
    rows = []
    for tag, class_set in element_dict.items():
        classes_str = ", ".join(filter(None, class_set))  # ignore empty strings
        rows.append({"Element": tag, "Classes": classes_str})

    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False)

    print(f" Saved elements with unique classes to {output_file}")


def extract_css_to_excel(url, output_file="css_cloned.xlsx"):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")

    data = []

    # External CSS
    for css in soup.find_all("link", rel="stylesheet"):
        href = css.get("href")
        if href:
            css_url = requests.compat.urljoin(url, href)
            r = requests.get(css_url)
            css_text = r.text

            # Extract all blocks of selector + rules
            blocks = re.findall(r"([^{]+){([^}]+)}", css_text)
            for selector, rules in blocks:
                selector = selector.strip()
                for rule in rules.split(";"):
                    rule = rule.strip()
                    if ":" in rule:
                        prop, val = rule.split(":", 1)
                        data.append(
                            ["External", selector, prop.strip(), val.strip(), ""]
                        )
    # Inline <style> blocks
    for style in soup.find_all("style"):
        css_text = style.text
        blocks = re.findall(r"([^{]+){([^}]+)}", css_text)
        for selector, rules in blocks:
            selector = selector.strip()
            for rule in rules.split(";"):
                rule = rule.strip()
                if ":" in rule:
                    prop, val = rule.split(":", 1)
                    data.append(
                        ["Inline Block", selector, prop.strip(), val.strip(), ""]
                    )

    # Inline style attributes
    for tag in soup.find_all(style=True):
        if tag.get("class"):
            selector = tag.name + "/" + "." + ".".join(tag["class"])
        else:
            selector = tag.name

        style_content = tag["style"].split(";")
        for rule in style_content:
            rule = rule.strip()
            if ":" in rule:
                prop, val = rule.split(":", 1)
                data.append(
                    ["Inline Attribute", selector, prop.strip(), val.strip(), ""]
                )

    # Save to Excel
    df = pd.DataFrame(
        data, columns=["Source Type", "Selector/Element", "Property", "Value", "Notes"]
    )
    df.to_excel(output_file, index=False)

    print(f"CSS saved into {output_file}")


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
        print(f"Element '{element_choice}' not found.")
        return None

    # Extract its classes
    classes = row["Classes"].iloc[0].split(", ")
    print(f"Classes for {element_choice}: {classes}")

    # Collect matching CSS rules
    matches = pd.DataFrame()
    for cls in classes:
        if cls:  # skip empty
            selector = "." + cls
            temp = css_df[
                css_df["Selector/Element"].str.contains(selector, na=False, regex=False)
            ]
            if not temp.empty:
                matches = pd.concat([matches, temp], ignore_index=True)

    # 2. Also search by tag name itself
    temp2 = css_df[
        css_df["Selector/Element"].str.contains(element_choice, na=False, regex=False)
    ]
    if not temp2.empty:
        matches = pd.concat([matches, temp2], ignore_index=True)

    if matches.empty:
        print("No CSS rules found for this element.")
        return pd.DataFrame()  # return empty DataFrame

    print("Matching CSS rules found:")
    print(matches)

    # Save results
    output_file = f"{element_choice}_css_lookup.xlsx"
    matches.to_excel(output_file, index=False)
    print(f"Saved to {output_file}")

    return matches


def batch_lookup_css(
    css_file="css_cloned.xlsx",
    elements_file="elements_grouped_unique.xlsx",
    output_folder="css_lookup_results",
):
    # Load the sheets
    css_df = pd.read_excel(css_file)
    elements_df = pd.read_excel(elements_file)

    os.makedirs(output_folder, exist_ok=True)

    # Loop elements
    for _, row in elements_df.iterrows():
        element = row["Element"]
        classes = str(row["Classes"]).split(", ") if pd.notna(row["Classes"]) else []

        matches = pd.DataFrame()

        # Search for each class in CSS sheet
        for cls in classes:
            selector = "." + cls.strip()
            temp = css_df[
                css_df["Selector/Element"].str.contains(selector, na=False, regex=False)
            ]
            if not temp.empty:
                matches = pd.concat([matches, temp], ignore_index=True)

        # Save matches if found
        if not matches.empty:
            output_file = os.path.join(output_folder, f"{element}_css_lookup.xlsx")
            matches.to_excel(output_file, index=False)
            print(f" Saved CSS rules for <{element}> to {output_file}")
        else:
            print(f" No CSS rules found for <{element}>")

    print(f"\n Process finished! All results are inside the '{output_folder}' folder.")


def main():
    print("--Webpage CSS & Elements Extractor--")
    url = input("Enter the URL of the webpage: ").strip()
    # 1st step
    extract_elements_to_excel(url)
    # 2nd step
    extract_css_to_excel(url)

    # Choose lookup mode
    print("\n Choose CSS lookup mode:")
    print("1. Lookup a single element")
    print("2. Batch lookup for all elements")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        element_choice = input(
            "Enter the element you want (e.g., div, h1, span): "
        ).strip()
        lookup_element_css(element_choice)
    elif choice == "2":
        batch_lookup_css()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
