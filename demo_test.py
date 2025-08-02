#!/usr/bin/env python3
"""
Demo test script to show example case data
"""

def test_demo_cases():
    """Test all demo cases and show their output"""
    from app.scraper import fetch_case_details
    
    demo_cases = [
        ("WP(C)", "1234", "2024"),
        ("CRL.A", "5678", "2023"),
        ("CIVIL", "9999", "2022"),
        ("CRL.M.C", "4321", "2021")
    ]
    
    print("🎯 Demo Case Examples")
    print("=" * 50)
    
    for case_type, case_number, filing_year in demo_cases:
        print(f"\n📋 Testing: {case_type} {case_number}/{filing_year}")
        print("-" * 30)
        
        result, error = fetch_case_details(case_type, case_number, filing_year)
        
        if result:
            print("✅ Case Found!")
            print(f"   Title: {result['case_title']}")
            print(f"   Parties: {result['parties']}")
            print(f"   Filing Date: {result['filing_date']}")
            print(f"   Next Hearing: {result['next_hearing']}")
            print(f"   Latest Order: {result['latest_order']['date']}")
            print(f"   PDF URL: {result['latest_order']['pdf_url']}")
        else:
            print(f"❌ Error: {error}")
    
    print("\n" + "=" * 50)
    print("🌐 Try these cases in your web application!")
    print("   Go to: http://127.0.0.1:5000")

if __name__ == "__main__":
    test_demo_cases() 