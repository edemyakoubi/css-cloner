from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import defaultdict

# 1️⃣ Fetch page
url = "https://quotes.toscrape.com/"
response = requests.get(url).text
soup = BeautifulSoup(response, "lxml")

# 2️⃣ Collect elements and their classes
element_dict = defaultdict(set)  # use set to avoid duplicates

for el in soup.find_all(True):
    tag = el.name
    classes = el.get("class")
    if classes:
        for cls in classes:
            element_dict[tag].add(cls)

# 3️⃣ Prepare rows for Excel
rows = []
for tag, class_set in element_dict.items():
    classes_str = ", ".join(class_set)  # join all classes in one string
    rows.append({"Element": tag, "Classes": classes_str})

# 4️⃣ Save to Excel
df = pd.DataFrame(rows)
df.to_excel("elements_grouped_unique.xlsx", index=False)

print("✅ Saved all elements with unique classes to elements_grouped_unique.xlsx")
