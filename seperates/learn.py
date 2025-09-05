from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://quotes.toscrape.com/"
response = requests.get(url).text
soup = BeautifulSoup(response, "lxml")

data = []

import re

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
                    data.append(["External", selector, prop.strip(), val.strip(), ""])


import re

for style in soup.find_all("style"):
    css_text = style.text
    blocks = re.findall(r"([^{]+){([^}]+)}", css_text)
    for selector, rules in blocks:
        selector = selector.strip()
        for rule in rules.split(";"):
            rule = rule.strip()
            if ":" in rule:
                prop, val = rule.split(":", 1)
                data.append(["Inline Block", selector, prop.strip(), val.strip(), ""])

for tag in soup.find_all(style=True):
    if tag.get("class"):
        selector = tag.name + "/" + "." + ".".join(tag["class"])
    else:
        selector = tag.name

    # Now split style rules
    style_content = tag["style"].split(";")
    for rule in style_content:
        rule = rule.strip()
        if ":" in rule:
            prop, val = rule.split(":", 1)
            data.append(["Inline Attribute", selector, prop.strip(), val.strip(), ""])


df = pd.DataFrame(
    data, columns=["Source Type", "Selector/Element", "Property", "Value", "Notes"]
)
df.to_excel("css_cloned.xlsx", index=False)


print("✅ CSS saved into css_cloned.xlsx")
