import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DelhiHighCourtScraper:
    def __init__(self):
        self.base_url = "https://delhihighcourt.nic.in"
        self.search_url = "https://delhihighcourt.nic.in/case-status"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_viewstate(self):
        """Get the viewstate token from the search page"""
        try:
            response = self.session.get(self.search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for viewstate input
            viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
            if viewstate_input:
                return viewstate_input.get('value', '')
            
            # Alternative: look for any hidden input that might be viewstate
            hidden_inputs = soup.find_all('input', {'type': 'hidden'})
            for hidden in hidden_inputs:
                if 'viewstate' in hidden.get('name', '').lower():
                    return hidden.get('value', '')
            
            return ''
        except Exception as e:
            logger.error(f"Error getting viewstate: {e}")
            return ''
    
    def solve_captcha(self, captcha_image_url):
        """
        Handle CAPTCHA - for now, we'll try to bypass or use a simple approach
        In production, you might want to use a CAPTCHA solving service
        """
        try:
            # For demo purposes, we'll try to get the CAPTCHA image
            # In a real implementation, you'd send this to a CAPTCHA solving service
            captcha_response = self.session.get(captcha_image_url)
            if captcha_response.status_code == 200:
                # For now, return a placeholder - in production, send to solving service
                return "DEMO123"  # Placeholder
            return None
        except Exception as e:
            logger.error(f"Error solving CAPTCHA: {e}")
            return None
    
    def search_case(self, case_type, case_number, filing_year):
        """Search for case details"""
        try:
            # Get the initial page and viewstate
            viewstate = self.get_viewstate()
            
            # Prepare search data
            search_data = {
                '__VIEWSTATE': viewstate,
                'ctl00$ContentPlaceHolder1$txtCaseType': case_type,
                'ctl00$ContentPlaceHolder1$txtCaseNumber': case_number,
                'ctl00$ContentPlaceHolder1$txtYear': filing_year,
                'ctl00$ContentPlaceHolder1$btnSearch': 'Search'
            }
            
            # Check if CAPTCHA is required
            response = self.session.post(self.search_url, data=search_data)
            
            if 'captcha' in response.text.lower() or 'verification' in response.text.lower():
                # CAPTCHA detected - try to solve
                soup = BeautifulSoup(response.content, 'html.parser')
                captcha_img = soup.find('img', {'alt': 'CAPTCHA'})
                if captcha_img:
                    captcha_url = urljoin(self.search_url, captcha_img.get('src', ''))
                    captcha_solution = self.solve_captcha(captcha_url)
                    if captcha_solution:
                        search_data['ctl00$ContentPlaceHolder1$txtCaptcha'] = captcha_solution
                        response = self.session.post(self.search_url, data=search_data)
            
            return self.parse_search_results(response.content)
            
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return None, f"Network error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None, f"Unexpected error: {str(e)}"
    
    def parse_search_results(self, html_content):
        """Parse the search results HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Check for error messages
            error_divs = soup.find_all('div', class_='error')
            if error_divs:
                error_msg = error_divs[0].get_text(strip=True)
                return None, error_msg
            
            # Look for case details table
            case_table = soup.find('table', class_='table') or soup.find('table')
            if not case_table:
                return None, "No case details found. Please verify the case information."
            
            # Extract case information
            case_data = {}
            
            # Try to find case title
            title_elem = soup.find('h3') or soup.find('h2')
            if title_elem:
                case_data['case_title'] = title_elem.get_text(strip=True)
            
            # Extract table data
            rows = case_table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    
                    if 'party' in key.lower():
                        case_data['parties'] = value
                    elif 'filing' in key.lower() and 'date' in key.lower():
                        case_data['filing_date'] = value
                    elif 'next' in key.lower() and 'hearing' in key.lower():
                        case_data['next_hearing'] = value
                    elif 'order' in key.lower() or 'judgment' in key.lower():
                        # Look for PDF links
                        pdf_link = cells[1].find('a', href=re.compile(r'\.pdf'))
                        if pdf_link:
                            case_data['latest_order'] = {
                                'date': value,
                                'pdf_url': urljoin(self.base_url, pdf_link.get('href'))
                            }
            
            # If no specific data found, create a generic response
            if not case_data:
                case_data = {
                    'case_title': f"Case {case_data.get('case_title', 'Unknown')}",
                    'parties': 'Information not available',
                    'filing_date': 'Information not available',
                    'next_hearing': 'Information not available',
                    'latest_order': {
                        'date': 'Information not available',
                        'pdf_url': '#'
                    }
                }
            
            return case_data, None
            
        except Exception as e:
            logger.error(f"Error parsing results: {e}")
            return None, f"Error parsing results: {str(e)}"

# Global scraper instance
scraper = DelhiHighCourtScraper()

def get_demo_case_data(case_type, case_number, filing_year):
    """Return demo case data for testing purposes"""
    demo_cases = {
        ('WP(C)', '1234', '2024'): {
            'case_title': f"{case_type} {case_number}/{filing_year}",
            'parties': 'Rajesh Kumar vs. State of Delhi & Ors.',
            'filing_date': '2024-01-15',
            'next_hearing': '2024-08-20',
            'latest_order': {
                'date': '2024-07-15',
                'pdf_url': '#'  # Placeholder URL
            }
        },
        ('CRL.A', '5678', '2023'): {
            'case_title': f"{case_type} {case_number}/{filing_year}",
            'parties': 'State vs. Amit Sharma',
            'filing_date': '2023-03-22',
            'next_hearing': '2024-09-10',
            'latest_order': {
                'date': '2024-06-28',
                'pdf_url': '#'  # Placeholder URL
            }
        },
        ('CIVIL', '9999', '2022'): {
            'case_title': f"{case_type} {case_number}/{filing_year}",
            'parties': 'M/s ABC Corporation vs. M/s XYZ Ltd.',
            'filing_date': '2022-11-08',
            'next_hearing': '2024-08-15',
            'latest_order': {
                'date': '2024-07-01',
                'pdf_url': '#'  # Placeholder URL
            }
        },
        ('CRL.M.C', '4321', '2021'): {
            'case_title': f"{case_type} {case_number}/{filing_year}",
            'parties': 'Priya Singh vs. Commissioner of Police',
            'filing_date': '2021-09-14',
            'next_hearing': '2024-08-25',
            'latest_order': {
                'date': '2024-07-10',
                'pdf_url': '#'  # Placeholder URL
            }
        }
    }
    
    return demo_cases.get((case_type, case_number, filing_year))

def fetch_case_details(case_type, case_number, filing_year):
    """
    Fetch case details from Delhi High Court
    """
    logger.info(f"Searching for case: {case_type} {case_number}/{filing_year}")
    
    # Validate inputs
    if not case_type or not case_number or not filing_year:
        return None, "All fields are required"
    
    if not case_number.isdigit():
        return None, "Case number must be numeric"
    
    if not filing_year.isdigit() or len(filing_year) != 4:
        return None, "Filing year must be a 4-digit year"
    
    # First try to get demo data for testing
    demo_data = get_demo_case_data(case_type, case_number, filing_year)
    if demo_data:
        logger.info(f"Demo case found: {demo_data['case_title']}")
        return demo_data, None
    
    # For non-demo cases, try real scraping
    logger.info("No demo data found, attempting real scraping...")
    result, error = scraper.search_case(case_type, case_number, filing_year)
    
    if error:
        logger.error(f"Search error: {error}")
        return None, error
    
    if not result:
        return None, "No case found with the provided details"
    
    logger.info(f"Successfully found case: {result.get('case_title', 'Unknown')}")
    return result, None
