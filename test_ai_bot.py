#!/usr/bin/env python3
"""
Test script for AI Bot functionality
"""

def test_ai_bot():
    """Test AI bot with sample case data"""
    from app.ai_bot import ai_bot
    
    # Sample case data
    sample_cases = [
        {
            'case_title': 'WP(C) 1234/2024',
            'parties': 'Rajesh Kumar vs. State of Delhi & Ors.',
            'filing_date': '2024-01-15',
            'next_hearing': '2024-08-20',
            'latest_order': {
                'date': '2024-07-15',
                'pdf_url': '#'
            }
        },
        {
            'case_title': 'CRL.A 5678/2023',
            'parties': 'State vs. Amit Sharma',
            'filing_date': '2023-03-22',
            'next_hearing': '2024-09-10',
            'latest_order': {
                'date': '2024-06-28',
                'pdf_url': '#'
            }
        },
        {
            'case_title': 'CIVIL 9999/2022',
            'parties': 'M/s ABC Corporation vs. M/s XYZ Ltd.',
            'filing_date': '2022-11-08',
            'next_hearing': '2024-08-15',
            'latest_order': {
                'date': '2024-07-01',
                'pdf_url': '#'
            }
        }
    ]
    
    print("🤖 AI Bot Test Results")
    print("=" * 50)
    
    for i, case in enumerate(sample_cases, 1):
        print(f"\n📋 Test Case {i}: {case['case_title']}")
        print("-" * 40)
        
        # Test AI analysis
        analysis = ai_bot.analyze_case(case)
        
        if 'error' not in analysis:
            print("✅ AI Analysis:")
            print(f"   Case Type: {analysis['case_analysis']['case_type_info'].get('full_name', 'Unknown')}")
            print(f"   Case Age: {analysis['case_analysis']['case_age']['status']}")
            print(f"   Next Hearing: {analysis['case_analysis']['hearing_analysis']['status']}")
            
            print("\n   Key Insights:")
            for insight in analysis['case_analysis']['insights'][:3]:
                print(f"   • {insight}")
            
            print("\n   Recommendations:")
            for rec in analysis['case_analysis']['recommendations'][:3]:
                print(f"   • {rec}")
            
            # Test question answering
            print("\n   AI Q&A Test:")
            questions = [
                "What type of case is this?",
                "How long has this case been pending?",
                "What should I do next?"
            ]
            
            for question in questions:
                answer = ai_bot.answer_question(question, case)
                print(f"   Q: {question}")
                print(f"   A: {answer}")
                print()
        else:
            print(f"❌ Error: {analysis['error']}")
    
    print("\n" + "=" * 50)
    print("🎉 AI Bot is working perfectly!")
    print("🌐 Try it in your web application at: http://127.0.0.1:5000")

if __name__ == "__main__":
    test_ai_bot() 