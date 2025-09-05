# Webpage CSS & Elements Extractor

This project provides Python scripts to extract HTML elements, their classes, and CSS rules (external stylesheets, inline `<style>` blocks, and inline `style` attributes) from a webpage.  
All extracted data is saved into structured Excel files for easy inspection and reuse.

---

## ✨ Features

- Extract **all HTML elements** and their associated classes
- Extract **CSS rules** from:
  - External stylesheets
  - Inline `<style>` blocks
  - Inline element attributes
- Lookup CSS rules for a **single element** or **batch process all elements**
- Extra script to **filter CSS rules** for:
  - Fonts
  - Colors
  - Backgrounds
  - Buttons
- Save results into organized Excel files

---

## 📦 Requirements

- Python **3.10+**
- Install the required packages:

```bash
pip install -r requirements.txt
```

---

# 🚀 Usage

## 1. Extract elements and CSS

Run the main extractor script:

```bash
python clone.py
```

- Enter the target URL
- Choose lookup mode:
- 1 → Lookup CSS rules for a single element (e.g. div, h1, span)
- 2 → Batch lookup for all elements

- Output files:
- Extracted elements → elements_grouped_unique.xlsx
- All CSS rules → css_cloned.xlsx
- Batch lookup results → inside css_lookup_results/

## 2. Filter for Fonts, Colors, and Buttons

- (Optional) Run the fast filter:

```bash
python css_fast_clone.py
```

- Output file: Filtered CSS rules → css_fast_clone.xlsx

---

## Disclaimer & Ethical Use

- This project is created for educational and research purposes only.

- You are solely responsible for how you use this code.

- Do not use it to copy or steal copyrighted designs, assets, or intellectual property.

- Always respect the Terms of Service of the websites you analyze.

- The author(s) of this repository are not liable for any misuse or legal issues arising from the use of this code.

- If you plan to use it in production or for business purposes, consult legal advice regarding web scraping ethics and copyright law.

---

## Contribution

- Contributions are welcome! Feel free to submit issues, bug fixes, or feature suggestions via GitHub Pull Requests.
