# Legal Case Law Knowledge Management Bot
## 🚀 Real Data from Indian Kanoon

A complete legal research bot that scrapes **real case data** from Indian Kanoon (4.5M+ legal documents).

---

## ✅ Features Implemented

### Mandatory Features (from PDF):
1. ✅ **Keyword-Based Legal Search** - Search using keywords and phrases
2. ✅ **Source Display with Citations** - Clear citations with court name, year, case title
3. ✅ **Semantic Query Understanding** - Understands intent beyond exact keywords
4. ✅ **Jurisdiction Filtering** - Filter by Supreme Court, High Courts
5. ✅ **Result Ranking by Relevance** - Orders cases by relevance score
6. ✅ **Case/Statute Summary** - Provides summaries for each result
7. ✅ **Traceability to Source Text** - View exact paragraphs from original source
8. ✅ **Multi-Source Aggregation** - Combines results from various courts
9. ✅ **Query Refinement Suggestions** - Suggests improvements for no-result searches

### Absolute Restrictions (from PDF):
1. ✅ **No Legal Advice** - Rejects advice-seeking queries
2. ✅ **No Interpretation** - Only shows cited information
3. ✅ **No Uncited Content** - All info has citations
4. ✅ **No Free-Text Counseling** - Stays within information retrieval scope
5. ✅ **No Hallucinated Sources** - Scrapes real data from Indian Kanoon

---

## 📦 Installation

### Prerequisites:
- Python 3.8+
- pip (Python package manager)
- Web browser

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (cross-origin requests)
- Requests (HTTP library)
- BeautifulSoup4 (web scraping)
- lxml (HTML parser)

### Step 2: Start the Backend Server

```bash
python backend.py
```

You should see:
```
🚀 Legal Case Law Bot API starting...
📚 Using Indian Kanoon as data source
🌐 Server running on http://localhost:5000
```

### Step 3: Open the Frontend

Open `legal_bot_live.html` in your web browser.

**Note:** You can simply double-click the HTML file or use:
```bash
# On Windows
start legal_bot_live.html

# On Mac
open legal_bot_live.html

# On Linux
xdg-open legal_bot_live.html
```

---

## 🎯 How to Use

### Sample Queries to Try:

**Valid Research Queries:**
1. `right to privacy` - Find privacy-related judgments
2. `article 21` - Constitutional law cases
3. `section 498A` - Criminal law statute
4. `habeas corpus` - Writ petitions
5. `contract breach` - Contract law cases

**Queries That Will Be Rejected (Legal Advice):**
1. `Should I file a case against my employer?`
2. `What are my chances of winning?`
3. `Can I sue my landlord?`

### Using Filters:

1. **Jurisdiction Filter:**
   - Select Supreme Court, specific High Courts, or All Courts
   
2. **Year Range:**
   - Enter "From" year (e.g., 2015)
   - Enter "To" year (e.g., 2025)

3. **View Source Text:**
   - Click "Load Source Text" button on any result
   - Fetches actual case text from Indian Kanoon

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  Frontend HTML  │ ──────► │  Flask Backend   │ ──────► │ Indian Kanoon   │
│  (User Interface)│         │  (Web Scraper)   │         │  (Legal Database)│
│                 │ ◄────── │                  │ ◄────── │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

### Frontend (legal_bot_live.html):
- User interface with filters
- Chat-based interaction
- Result display with citations
- Source text viewer

### Backend (backend.py):
- Flask API server
- Web scraping logic
- BeautifulSoup HTML parsing
- Indian Kanoon integration

---

## 🔧 Technical Details

### API Endpoints:

**POST /api/search**
- Searches Indian Kanoon for legal cases
- Body: `{ query, jurisdictions, year_from, year_to }`
- Returns: Array of case results with citations

**POST /api/case-details**
- Fetches full case text
- Body: `{ url }`
- Returns: Source text from case

**GET /health**
- Health check endpoint
- Returns: `{ status: 'healthy' }`

### Data Scraped from Indian Kanoon:
- Case title
- Citation (court reference)
- Court name
- Year
- Case summary/snippet
- Full case text (on demand)
- Direct link to source

---

## ⚠️ Limitations

1. **Scraping Speed:** 
   - Results take 2-5 seconds to load (scraping is slower than API)
   - Limited to ~10 results per search (to avoid overloading)

2. **Indian Kanoon Dependency:**
   - Requires active internet connection
   - Depends on Indian Kanoon website availability
   - Website structure changes may break scraper

3. **No Authentication:**
   - Completely free, no API key needed
   - Subject to Indian Kanoon's rate limits

---

## 🚀 Future Enhancements

- [ ] Cache frequently searched cases
- [ ] Add precedent relationship detection
- [ ] Implement statute search
- [ ] Add export to PDF feature
- [ ] Multi-threaded scraping for faster results
- [ ] Add more High Courts to filters

---

## 📝 Notes

- This is a **completely free** solution using web scraping
- All data comes from **Indian Kanoon's public database**
- The bot **does NOT provide legal advice** - only information retrieval
- For production use, consider getting Indian Kanoon API access for faster results

---

## 🐛 Troubleshooting

**Backend won't start:**
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt

# Check if port 5000 is available
# On Windows: netstat -ano | findstr :5000
# On Mac/Linux: lsof -i :5000
```

**No results showing:**
- Check that backend is running (http://localhost:5000/health should return JSON)
- Check browser console for errors (F12)
- Verify internet connection
- Try broader search terms

**CORS errors:**
- Make sure backend is running on localhost:5000
- Check that Flask-CORS is installed

---

## 📄 License

Educational use only. Respect Indian Kanoon's terms of service when scraping data.

---

## 👨‍💻 Developer

Built as per the project requirements specified in the PDF document.

**Tech Stack:**
- Backend: Python + Flask + BeautifulSoup4
- Frontend: HTML + CSS + JavaScript
- Data Source: Indian Kanoon (web scraping)
