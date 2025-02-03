from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import json
from langchain_community.llms import Ollama
from fake_useragent import UserAgent
import time
import random
from flask_cors import CORS
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class AiWebScraper:
    def __init__(self):
        try:
            self.llm = Ollama(model="minicpm-v", base_url="http://localhost:11434")
            self.ua = UserAgent()
            logger.info("Successfully initialized Ollama with minicpm-v model")
        except Exception as e:
            logger.error(f"Error initializing Ollama: {str(e)}")
            raise
        
    def search_google(self, query, num_results=10):
        logger.info(f"Starting Google search for query: {query}")
        
        # Multiple User-Agent strings for better reliability
        headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            },
            {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }
        ]
        
        search_results = []
        
        try:
            # Try different search URL formats
            search_urls = [
                f"https://www.google.com/search?q={query}&num={num_results}",
                f"https://www.google.com/search?q={query}&num={num_results}&hl=id"
            ]
            
            for search_url in search_urls:
                for headers in headers_list:
                    try:
                        logger.info(f"Trying search URL: {search_url}")
                        response = requests.get(search_url, headers=headers, timeout=10)
                        response.raise_for_status()
                        
                        soup = BeautifulSoup(response.text, 'html.parser')
                        logger.info("Successfully fetched search results page")
                        
                        # Try multiple selectors for finding results
                        selectors = [
                            ('div', {'class': 'g'}),
                            ('div', {'class': 'rc'}),
                            ('div', {'class': 'yuRUbf'}),
                            ('div', {'class': 'tF2Cxc'})
                        ]
                        
                        for tag, attrs in selectors:
                            results = soup.find_all(tag, attrs)
                            if results:
                                logger.info(f"Found results using selector: {tag}, {attrs}")
                                for result in results:
                                    # Try different ways to find URLs
                                    url = None
                                    if result.find('a'):
                                        url = result.find('a').get('href')
                                    elif result.find('cite'):
                                        url = result.find('cite').text
                                    
                                    if url and url.startswith('http') and not url.startswith(('https://google.com', 'https://www.google.com')):
                                        if url not in search_results:  # Avoid duplicates
                                            search_results.append(url)
                                            logger.info(f"Found URL: {url}")
                                            if len(search_results) >= num_results:
                                                break
                                
                                if search_results:
                                    break
                        
                        if search_results:
                            break
                            
                    except requests.RequestException as e:
                        logger.warning(f"Request failed for URL {search_url}: {str(e)}")
                        continue
                    
                if search_results:
                    break
            
            logger.info(f"Found {len(search_results)} unique search results")
            return search_results[:num_results]
            
        except Exception as e:
            logger.error(f"Error in search: {str(e)}")
            return []

    def scrape_content(self, url):
        logger.info(f"Scraping content from URL: {url}")
        headers = {'User-Agent': self.ua.random}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe']):
                element.decompose()
                
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            logger.info(f"Successfully scraped content from {url} (length: {len(text)})")
            return text
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return ""

    def analyze_content(self, text, query):
        logger.info(f"Analyzing content for query: {query}")
        prompt = f"""
        Berikut adalah teks tentang {query}. 
        Tolong berikan ringkasan yang informatif dalam bahasa Indonesia.
        Fokuskan pada fakta penting dan informasi utama.
        
        Teks untuk dianalisis: {text[:2000]}
        
        Berikan ringkasan dalam format yang terstruktur:
        1. Informasi Utama
        2. Detail Penting
        3. Kesimpulan
        """
        
        try:
            logger.info("Sending prompt to Ollama")
            response = self.llm(prompt)
            logger.info("Received response from Ollama")
            return response
        except Exception as e:
            logger.error(f"Error in analysis: {str(e)}")
            return ""

    def scrape_and_analyze(self, query):
        logger.info(f"Starting scrape and analyze process for query: {query}")
        results = []
        urls = self.search_google(query)
        
        if not urls:
            logger.warning("No URLs found in search results")
            return results
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing URL {i}/{len(urls)}: {url}")
            time.sleep(random.uniform(1, 3))
            
            content = self.scrape_content(url)
            if content:
                logger.info(f"Content scraped successfully, length: {len(content)}")
                analysis = self.analyze_content(content, query)
                
                if analysis:
                    logger.info("Analysis completed successfully")
                    result = {
                        "url": url,
                        "query": query,
                        "analysis": analysis,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    results.append(result)
                else:
                    logger.warning(f"No analysis result for URL: {url}")
            
            # Save intermediate results after each successful analysis
            if results:
                with open(f"hasil_scraping_{query.replace(' ', '_')}_temp.json", 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Completed processing with {len(results)} results")
        return results

try:
    logger.info("Initializing AiWebScraper")
    scraper = AiWebScraper()
except Exception as e:
    logger.error(f"Failed to initialize AiWebScraper: {str(e)}")
    exit(1)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        logger.error("No query provided in request")
        return jsonify({"error": "No query provided"}), 400
    
    try:
        logger.info(f"Processing scrape request for query: {query}")
        results = scraper.scrape_and_analyze(query)
        
        if not results:
            logger.warning("No results found for query")
            return jsonify({
                "status": "success",
                "results": [],
                "message": "No results found"
            })
        
        filename = f"hasil_scraping_{query.replace(' ', '_')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Successfully saved results to {filename}")
        return jsonify({
            "status": "success",
            "results": results,
            "filename": filename
        })
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)