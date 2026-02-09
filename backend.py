from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

class IndianKanoonScraper:
    """Scraper for Indian Kanoon legal database"""
    
    BASE_URL = "https://indiankanoon.org"
    SEARCH_URL = f"{BASE_URL}/search/"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_cases(self, query, jurisdiction=None, year_from=None, year_to=None):
        """
        Search Indian Kanoon for legal cases
        
        Args:
            query: Search query string
            jurisdiction: Filter by court (e.g., "Supreme Court")
            year_from: Start year for filtering
            year_to: End year for filtering
        
        Returns:
            List of case dictionaries
        """
        try:
            # Build search URL
            search_query = quote_plus(query)
            search_url = f"{self.SEARCH_URL}?formInput={search_query}"
            
            # Add jurisdiction filter if specified
            if jurisdiction:
                if "Supreme Court" in jurisdiction:
                    search_url += "&courtList=supreme-court"
                elif "High Court" in jurisdiction:
                    court_code = jurisdiction.lower().replace(" high court", "").replace(" ", "-")
                    search_url += f"&courtList={court_code}"
            
            # Add year filters
            if year_from:
                search_url += f"&fromYear={year_from}"
            if year_to:
                search_url += f"&toYear={year_to}"
            
            # Make request
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # Parse results
            soup = BeautifulSoup(response.content, 'html.parser')
            cases = self._parse_search_results(soup)
            
            return cases
            
        except Exception as e:
            print(f"Error searching Indian Kanoon: {e}")
            return []
    
    def _parse_search_results(self, soup):
        """Parse search results page and extract case information"""
        cases = []
        
        # Find all result divs
        result_divs = soup.find_all('div', class_='result')
        
        for div in result_divs[:10]:  # Limit to first 10 results
            try:
                case = {}
                
                # Extract title and link
                title_tag = div.find('a', class_='cite_tag')
                if title_tag:
                    case['title'] = title_tag.get_text(strip=True)
                    case['url'] = self.BASE_URL + title_tag.get('href', '')
                    case['id'] = title_tag.get('href', '').split('/')[-2] if '/' in title_tag.get('href', '') else ''
                
                # Extract citation
                cite_tag = div.find('div', class_='cite')
                if cite_tag:
                    case['citation'] = cite_tag.get_text(strip=True)
                
                # Extract summary/snippet
                snippet = div.find('div', class_='result_doc_head')
                if snippet:
                    case['summary'] = snippet.get_text(strip=True)[:300] + "..."
                
                # Extract court and year from citation or title
                case['court'] = self._extract_court(case.get('citation', '') + ' ' + case.get('title', ''))
                case['year'] = self._extract_year(case.get('citation', '') + ' ' + case.get('title', ''))
                
                # Set jurisdiction
                if 'Supreme Court' in case['court']:
                    case['jurisdiction'] = 'Supreme Court'
                elif 'High Court' in case['court']:
                    case['jurisdiction'] = case['court']
                else:
                    case['jurisdiction'] = 'Other Courts'
                
                # Type is always judgment from search
                case['type'] = 'judgment'
                
                cases.append(case)
                
            except Exception as e:
                print(f"Error parsing result: {e}")
                continue
        
        return cases
    
    def get_case_details(self, case_url):
        """Fetch full case details including source text"""
        try:
            response = self.session.get(case_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract case text
            doc_div = soup.find('div', class_='doc')
            if doc_div:
                # Get first few paragraphs as source text
                paragraphs = doc_div.find_all('p')[:5]
                source_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                return source_text
            
            return "Source text not available"
            
        except Exception as e:
            print(f"Error fetching case details: {e}")
            return "Error fetching source text"
    
    def _extract_court(self, text):
        """Extract court name from text"""
        courts = [
            'Supreme Court',
            'Delhi High Court',
            'Bombay High Court',
            'Madras High Court',
            'Calcutta High Court',
            'Karnataka High Court',
            'Kerala High Court',
            'Allahabad High Court',
            'Gujarat High Court'
        ]
        
        for court in courts:
            if court.lower() in text.lower():
                return court
        
        # Try to extract "XYZ High Court" pattern
        match = re.search(r'(\w+\s+High Court)', text, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return 'Unknown Court'
    
    def _extract_year(self, text):
        """Extract year from citation or text"""
        # Look for year in format (YYYY) or YYYY
        match = re.search(r'\((\d{4})\)|\b(\d{4})\b', text)
        if match:
            year = match.group(1) or match.group(2)
            year = int(year)
            # Validate year is reasonable (between 1950-2025)
            if 1950 <= year <= 2025:
                return year
        return 2024  # Default year

# Initialize scraper
scraper = IndianKanoonScraper()

@app.route('/api/search', methods=['POST'])
def search():
    """API endpoint for searching legal cases"""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Get filters
        jurisdictions = data.get('jurisdictions', [])
        year_from = data.get('year_from')
        year_to = data.get('year_to')
        
        # Search with first jurisdiction if provided
        jurisdiction = jurisdictions[0] if jurisdictions else None
        
        # Perform search
        results = scraper.search_cases(
            query=query,
            jurisdiction=jurisdiction,
            year_from=year_from,
            year_to=year_to
        )
        
        # Add relevance scores (simple keyword matching)
        query_words = set(query.lower().split())
        for result in results:
            score = 0
            title_lower = result.get('title', '').lower()
            summary_lower = result.get('summary', '').lower()
            
            for word in query_words:
                if word in title_lower:
                    score += 10
                if word in summary_lower:
                    score += 5
            
            # Recency bonus
            if result.get('year', 0) >= 2020:
                score += 5
            elif result.get('year', 0) >= 2015:
                score += 3
            
            result['relevanceScore'] = score
        
        # Sort by relevance
        results.sort(key=lambda x: x.get('relevanceScore', 0), reverse=True)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/case-details', methods=['POST'])
def case_details():
    """API endpoint for fetching full case details"""
    try:
        data = request.json
        case_url = data.get('url', '')
        
        if not case_url:
            return jsonify({'error': 'URL is required'}), 400
        
        source_text = scraper.get_case_details(case_url)
        
        return jsonify({
            'success': True,
            'sourceText': source_text
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Legal Bot API'})

if __name__ == '__main__':
    print("🚀 Legal Case Law Bot API starting...")
    print("📚 Using Indian Kanoon as data source")
    print("🌐 Server running on http://localhost:5000")
    app.run(debug=True, port=5000)
