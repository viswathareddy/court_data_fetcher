# Court Data Fetcher & Mini-Dashboard

A comprehensive web application for fetching and displaying case details from the Delhi High Court, enhanced with **AI-powered case analysis and legal insights**. This application provides a user-friendly interface to search for court cases, view case details, download PDF orders, maintain search history, and get intelligent analysis from an AI bot.

## 🎯 Objective

Build a small web app that lets users choose a Case Type and Case Number for the Delhi High Court, then fetches and displays the case metadata, latest orders/judgments, and provides **AI-powered analysis and recommendations**.

## 🏛️ Target Court

**Delhi High Court** (https://delhihighcourt.nic.in/)

The application is specifically designed to work with the Delhi High Court's case status portal, handling view-state tokens and CAPTCHA challenges.

## ✨ Features

### Core Functionality
- **Case Search**: Search for cases using Case Type, Case Number, and Filing Year
- **Case Details Display**: View comprehensive case information including parties, filing date, next hearing, and latest orders
- **PDF Download**: Download court orders and judgments directly from the application
- **Search History**: Track all search attempts with detailed logging
- **Error Handling**: User-friendly error messages for invalid inputs or network issues

### 🤖 **AI-Powered Features** (NEW!)
- **AI Case Analysis**: Intelligent analysis of case details and legal implications
- **Timeline Analysis**: Track case progress, age, and hearing schedules
- **Legal Insights**: Provide context about case types and procedures
- **Smart Recommendations**: AI-generated suggestions for next steps
- **Interactive Q&A**: Ask questions about cases and get intelligent responses
- **Case Type Intelligence**: Detailed information about different case types (WP(C), CRL.A, CIVIL, CRL.M.C)

### Technical Features
- **CAPTCHA Handling**: Automatic CAPTCHA detection and handling strategies
- **View-State Management**: Proper handling of ASP.NET view-state tokens
- **Database Logging**: SQLite database to log all queries and responses
- **Responsive UI**: Modern, mobile-friendly interface built with Bootstrap 5
- **API Endpoints**: RESTful API for programmatic access
- **AI Integration**: Local AI bot for case analysis and legal insights

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Web Scraping**: Requests, BeautifulSoup4
- **AI/ML**: Custom AI bot with legal knowledge base
- **Icons**: Font Awesome 6

## 📋 Requirements

### Functional Requirements
1. **UI** - Simple form with dropdown/inputs for Case Type, Case Number, Filing Year
2. **Backend** - Programmatically request the court site, bypass view-state tokens/CAPTCHA
3. **Storage** - Log each query & raw response in SQLite database
4. **Display** - Render parsed details nicely; allow downloading linked PDFs
5. **Error Handling** - User-friendly messages for invalid cases or site downtime
6. **🤖 AI Analysis** - Provide intelligent insights and recommendations about cases

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd court_data_fetcher
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///court_data.db
```

### Sample Configuration
```env
FLASK_ENV=development
SECRET_KEY=change_this_secret_key_in_production
DATABASE_URL=sqlite:///court_data.db
DEBUG=True
```

## 📖 Usage

### Basic Search
1. Navigate to the home page
2. Enter the Case Type (e.g., WP(C), CRL.A, CIVIL)
3. Enter the Case Number (numeric only)
4. Enter the Filing Year (4-digit year)
5. Click "Fetch Case Details"

### 🤖 **AI Features**
- **Case Analysis**: View AI-generated insights about case type, timeline, and legal implications
- **Smart Recommendations**: Get AI suggestions for next steps and legal strategies
- **Interactive Q&A**: Ask questions like:
  - "What type of case is this?"
  - "How long has this case been pending?"
  - "What should I do next?"
  - "What are the legal implications?"
- **Timeline Analysis**: See case age, status, and hearing urgency
- **Legal Context**: Understand case types, typical durations, and success rates

### Advanced Features
- **Search History**: View all previous searches at `/history`
- **PDF Downloads**: Click download buttons to save court orders
- **Print Details**: Use the print button to save case details as PDF
- **AI Chat**: Interactive chat interface for case-related questions

## 🔍 CAPTCHA Strategy

The application implements several strategies to handle CAPTCHA challenges:

1. **Detection**: Automatically detects when CAPTCHA is required
2. **Bypass Attempts**: Tries to bypass CAPTCHA using session management
3. **Placeholder Solution**: Currently uses a demo solution (in production, integrate with CAPTCHA solving service)
4. **Error Handling**: Graceful fallback when CAPTCHA cannot be solved

### Production CAPTCHA Solutions
For production deployment, consider:
- **2captcha API**: Commercial CAPTCHA solving service
- **Anti-CAPTCHA**: Alternative CAPTCHA solving service
- **Manual Token Field**: Allow users to manually solve CAPTCHA
- **Court API**: If available, use official court APIs

## 🤖 **AI Bot Capabilities**

### Case Analysis
- **Case Type Intelligence**: Detailed information about WP(C), CRL.A, CIVIL, CRL.M.C
- **Timeline Analysis**: Calculate case age, status, and hearing urgency
- **Legal Insights**: Provide context about legal procedures and implications
- **Success Rate Analysis**: Estimate case success probability based on type

### Smart Recommendations
- **Next Steps**: Suggest appropriate actions based on case status
- **Legal Strategy**: Recommend legal approaches based on case type
- **Documentation**: Suggest important documents to gather
- **Timeline Management**: Advise on hearing preparation and deadlines

### Interactive Q&A
- **Natural Language**: Ask questions in plain English
- **Context-Aware**: Responses based on specific case details
- **Legal Guidance**: Provide legal context and explanations
- **Procedural Advice**: Guide users through legal processes

## 🗄️ Database Schema

### QueryLog Table
```sql
CREATE TABLE query_log (
    id INTEGER PRIMARY KEY,
    case_type VARCHAR(50),
    case_number VARCHAR(50),
    filing_year VARCHAR(10),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_response TEXT,
    status VARCHAR(20)
);
```

## 🔒 Security Considerations

- **No Hard-coded Secrets**: All sensitive data stored in environment variables
- **Input Validation**: Client and server-side validation for all inputs
- **SQL Injection Protection**: Using SQLAlchemy ORM for safe database operations
- **XSS Protection**: Proper HTML escaping in templates
- **CSRF Protection**: Flask-WTF integration ready

## 🧪 Testing

### Manual Testing
1. Test with valid case numbers
2. Test with invalid inputs
3. Test network error scenarios
4. Test PDF download functionality
5. **Test AI features**: Ask questions and verify responses

### Sample Test Cases
```python
# Valid case
Case Type: WP(C)
Case Number: 1234
Filing Year: 2024

# Invalid inputs
Case Type: 123 (should fail)
Case Number: ABC (should fail)
Filing Year: 202 (should fail)
```

### AI Bot Testing
```python
# Test AI analysis
python test_ai_bot.py

# Test demo cases
python demo_test.py
```

## 🚀 Deployment

### Local Development
```bash
python run.py
```

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure reverse proxy (Nginx, Apache)
4. Set up SSL certificates
5. Configure database for production

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

## 📊 API Endpoints

### REST API
- `GET /` - Main search page
- `POST /` - Submit case search
- `GET /history` - View search history
- `GET /download/<pdf_url>` - Download PDF
- `POST /api/search` - API endpoint for AJAX searches
- **`POST /api/ask`** - Ask AI questions about cases
- **`POST /api/analyze`** - Get AI case analysis

### API Response Format
```json
{
  "result": {
    "case_title": "WP(C) 1234/2024",
    "parties": "Petitioner vs Respondent",
    "filing_date": "2024-01-15",
    "next_hearing": "2024-08-20",
    "latest_order": {
      "date": "2024-07-15",
      "pdf_url": "https://delhihighcourt.nic.in/orders/..."
    }
  },
  "ai_analysis": {
    "case_analysis": {
      "case_type_info": {...},
      "case_age": {...},
      "hearing_analysis": {...},
      "insights": [...],
      "recommendations": [...]
    },
    "ai_summary": "..."
  },
  "error": null
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Template Not Found Error**
   - Ensure templates are in the correct directory
   - Check template folder configuration in `app/__init__.py`

2. **Database Errors**
   - Run database initialization: `python init_db.py`

3. **Scraping Errors**
   - Check internet connectivity
   - Verify Delhi High Court website is accessible
   - Check for CAPTCHA requirements

4. **PDF Download Issues**
   - Verify PDF URLs are accessible
   - Check file permissions for downloads

5. **AI Bot Issues**
   - Check AI bot dependencies: `pip install openai python-dotenv`
   - Test AI functionality: `python test_ai_bot.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

## 🔮 Future Enhancements

- [ ] **Advanced AI**: Integration with OpenAI GPT for more sophisticated analysis
- [ ] **Multi-Court Support**: Extend to other High Courts and District Courts
- [ ] **Real-time Updates**: Live case status updates and notifications
- [ ] **Document Analysis**: AI-powered analysis of court orders and judgments
- [ ] **Predictive Analytics**: Predict case outcomes and timelines
- [ ] **Mobile App**: Native mobile application
- [ ] **Voice Interface**: Voice-based case queries and analysis
- [ ] **Legal Research**: Integration with legal databases and precedents

---

**Built with ❤️ using Flask, Bootstrap**
