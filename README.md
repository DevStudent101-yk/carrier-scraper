# 🚀 Automated Carrier Data Extraction System

> Built by **Muhammad Younas** — AI Automation Engineer & Python Developer  
> First freelance project delivered to a real US logistics client

---

## 📌 What This Project Does

This system automatically scans hundreds of thousands of FMCSA 
carrier records, extracts carrier data from Fenderr, applies 
intelligent filtering, and delivers clean verified results 
in Excel format.

The client needed to find small owner-operator trucking companies 
that are newly registered and actively operating — something that 
would take weeks manually. This system does it in hours.

---

## 📊 Project Results

| Metric | Result |
|---|---|
| MC Numbers Scanned | 700,000+ |
| Valid Carriers Found | 10,000+ |
| Pipeline Steps | 8 |
| Data Lost on Crashes | 0 |

---

## ✅ Filter Conditions Applied

- Carrier status must be **Active**
- Carrier must be **Authorized** for hire
- Must have exactly **1 driver**
- Must have exactly **1 truck**
- MC registration age **3 to 12 months**
- Must have a valid **phone number**

---

## 🔧 How The Pipeline Works
Smart MC Range Generator → Loops through 1,600,000 to 1,800,000
Cloudflare Bypass Engine → CDP session management
Fenderr Web Automation → Playwright browser automation
Intelligent Data Extractor → Extracts all carrier fields
LangChain Data Organizer → Structures raw data
Multi-Condition Filter → Applies all business rules
Auto-Resume Progress System → Never loses progress on crash
Excel and CSV Delivery → Clean client-ready output
---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Playwright | Browser automation |
| BeautifulSoup | HTML parsing |
| Pandas | Data processing |
| LangChain | Data organization |
| openpyxl | Excel export |
| Git | Version control |

---

## 💡 Key Engineering Challenges Solved

### 🛡️ Cloudflare Bot Protection
The target website uses enterprise-level Cloudflare protection 
that blocks all standard automation tools. Solved by connecting 
Python to a real Chrome browser using Chrome DevTools Protocol 
(CDP) making every request look like a real human.

### 🔢 DOT vs MC Number Confusion
The search returns mixed results matching both DOT and MC numbers. 
Built validation logic that only accepts exact MC number matches.

### ⚡ Crash Recovery System
Long runs scanning 700,000+ records can be interrupted at any time. 
Built a progress-saving system that writes position after every 
single MC number — zero data lost on any crash or restart.

### 📊 Deduplication and Merging
Multiple output files created duplicates during long runs. 
Built an automatic merge script that combines all files and 
removes duplicates based on MC number.

---

## 📁 Project Structure
carrier-scraper/
├── src/
│ ├── config.py ← All settings in one place
│ ├── scraper.py ← Playwright + Fenderr automation
│ ├── processor.py ← Data cleaning and filtering
│ ├── exporter.py ← CSV and Excel export
│ └── progress.py ← Resume/save system
├── output/ ← Generated CSV and Excel files
├── logs/ ← Scraper logs
├── merge.py ← Merge multiple output files
├── main.py ← Entry point
└── requirements.txt
---

## ⚙️ How To Run

### 1. Clone the project
```bash
git clone https://github.com/YOUR_USERNAME/carrier-scraper.git
cd carrier-scraper
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Open Chrome with debugging port
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" 
--remote-debugging-port=9222 
--user-data-dir="C:\chrome-debug"
```

### 5. Run the scraper
```bash
python main.py
```

---

## 📬 Contact

**Muhammad Younas**  
AI Automation Engineer & Python Developer  
Available on Fiverr: [text](https://www.fiverr.com/s/DBDmZ2Q)

---

> ⭐ If this project helped you, please give it a star on GitHub!