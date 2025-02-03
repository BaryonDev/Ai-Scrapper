# 🤖 AI-Powered Web Scraper with Ollama

A sophisticated web scraping tool that combines the power of local AI (using Ollama) with web scraping capabilities to provide intelligent, context-aware information gathering from the internet.

## 🌟 Features

- **🔍 Intelligent Search**: Automatically searches Google for relevant web pages based on user queries
- **🧠 AI-Powered Analysis**: Uses Ollama with the minicpm-v model for intelligent content analysis
- **🌐 Smart Scraping**: Extracts and processes content from multiple websites simultaneously
- **📊 Structured Output**: Organizes scraped data into clean, structured JSON format
- **🎯 Context-Aware**: Provides relevant summaries based on search context
- **💻 User-Friendly Interface**: Clean and responsive web interface for easy interaction
- **🚀 Real-Time Processing**: Shows live progress as content is being scraped and analyzed

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, JavaScript, TailwindCSS
- **AI Model**: Ollama (minicpm-v)
- **Data Processing**: BeautifulSoup4, Requests
- **Output Format**: JSON

## 📋 Prerequisites

- Python 3.8 or higher
- Ollama installed locally
- minicpm-v model downloaded in Ollama

## 🚀 Installation

1. Clone the repository
```bash
git clone https://github.com/BaryonDev/Ai-Scrapper.git
cd ai-web-scraper
```

2. Install required Python packages
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running with minicpm-v model
```bash
ollama serve
ollama pull minicpm-v
```

## 💻 Usage

1. Start the Flask backend:
```bash
python app.py
```

2. Open `index.html` in your web browser

3. Enter your search query in the search box

4. Wait for the results to be processed and displayed

## 📄 Output Format

The scraped data is saved in JSON format:
```json
{
    "url": "https://example.com",
    "query": "search query",
    "analysis": "AI-generated analysis of the content",
    "timestamp": "2025-02-03 08:14:44"
}
```

## 🔧 Configuration

You can modify the following parameters in the code:
- Number of websites to scrape (`num_results` in `search_google`)
- Analysis prompt template (`analyze_content` method)
- Search delay time (`random.uniform(1, 3)` in `scrape_and_analyze`)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚨 Disclaimer

This tool is for educational purposes only. Make sure to follow websites' robots.txt rules and terms of service when scraping content.

## 🙏 Acknowledgments

- Thanks to the Ollama team for providing the AI model
- BeautifulSoup4 for making web scraping easier
- Flask for the lightweight web framework
- All contributors who help improve this project

## 📞 Support

If you have any questions or need help, please:
1. Check the existing issues
2. Create a new issue with a detailed description of your problem
3. Contact the maintainers

---
Made with ❤️ by [Your Name]
