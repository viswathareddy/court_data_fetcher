import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CourtAIBot:
    def __init__(self):
        self.case_type_info = {
            'WP(C)': {
                'full_name': 'Writ Petition (Civil)',
                'description': 'A constitutional remedy for violation of fundamental rights',
                'typical_duration': '6-18 months',
                'success_rate': 'High for clear violations',
                'key_insights': [
                    'Article 226 of Constitution',
                    'Violation of fundamental rights',
                    'Quick disposal possible',
                    'Can be filed against state/authorities'
                ]
            },
            'CRL.A': {
                'full_name': 'Criminal Appeal',
                'description': 'Appeal against criminal conviction or acquittal',
                'typical_duration': '2-5 years',
                'success_rate': 'Moderate',
                'key_insights': [
                    'Section 374 of CrPC',
                    'Against conviction/acquittal',
                    'Requires legal representation',
                    'Evidence review important'
                ]
            },
            'CIVIL': {
                'full_name': 'Civil Suit',
                'description': 'Dispute resolution for civil matters',
                'typical_duration': '3-7 years',
                'success_rate': 'Varies by case strength',
                'key_insights': [
                    'Property, contract, family disputes',
                    'Evidence and documentation crucial',
                    'Mediation possible',
                    'Cost-benefit analysis important'
                ]
            },
            'CRL.M.C': {
                'full_name': 'Criminal Miscellaneous Case',
                'description': 'Interim relief in criminal matters',
                'typical_duration': '3-12 months',
                'success_rate': 'High for interim relief',
                'key_insights': [
                    'Bail, stay, quashing petitions',
                    'Interim relief possible',
                    'Quick disposal',
                    'Strategic timing important'
                ]
            }
        }
    
    def analyze_case(self, case_data: Dict) -> Dict:
        """Analyze case data and provide AI insights"""
        try:
            case_type = case_data.get('case_title', '').split()[0]
            case_info = self.case_type_info.get(case_type, {})
            
            # Calculate case age
            filing_date = case_data.get('filing_date', '')
            case_age = self._calculate_case_age(filing_date)
            
            # Analyze next hearing
            next_hearing = case_data.get('next_hearing', '')
            hearing_analysis = self._analyze_hearing_schedule(next_hearing)
            
            # Generate insights
            insights = self._generate_insights(case_data, case_info, case_age)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(case_data, case_info, case_age)
            
            return {
                'case_analysis': {
                    'case_type_info': case_info,
                    'case_age': case_age,
                    'hearing_analysis': hearing_analysis,
                    'insights': insights,
                    'recommendations': recommendations
                },
                'ai_summary': self._generate_ai_summary(case_data, insights, recommendations)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing case: {e}")
            return {'error': 'Unable to analyze case at this time'}
    
    def _calculate_case_age(self, filing_date: str) -> Dict:
        """Calculate case age and timeline analysis"""
        try:
            if filing_date and filing_date != 'Information not available':
                filing_dt = datetime.strptime(filing_date, '%Y-%m-%d')
                current_dt = datetime.now()
                age_days = (current_dt - filing_dt).days
                age_years = age_days / 365.25
                
                if age_years < 1:
                    status = "New Case"
                    description = "Case is relatively new and likely in early stages"
                elif age_years < 3:
                    status = "Active Case"
                    description = "Case is in active litigation phase"
                elif age_years < 5:
                    status = "Mature Case"
                    description = "Case has been ongoing for some time"
                else:
                    status = "Long-pending Case"
                    description = "Case has been pending for an extended period"
                
                return {
                    'age_days': age_days,
                    'age_years': round(age_years, 1),
                    'status': status,
                    'description': description
                }
            else:
                return {
                    'age_days': 'Unknown',
                    'age_years': 'Unknown',
                    'status': 'Unknown',
                    'description': 'Filing date not available'
                }
        except Exception as e:
            logger.error(f"Error calculating case age: {e}")
            return {
                'age_days': 'Error',
                'age_years': 'Error',
                'status': 'Error',
                'description': 'Unable to calculate case age'
            }
    
    def _analyze_hearing_schedule(self, next_hearing: str) -> Dict:
        """Analyze next hearing schedule"""
        try:
            if next_hearing and next_hearing != 'Information not available':
                hearing_dt = datetime.strptime(next_hearing, '%Y-%m-%d')
                current_dt = datetime.now()
                days_until_hearing = (hearing_dt - current_dt).days
                
                if days_until_hearing < 0:
                    status = "Overdue"
                    urgency = "High"
                    description = "Hearing date has passed"
                elif days_until_hearing <= 7:
                    status = "Imminent"
                    urgency = "High"
                    description = "Hearing is very soon"
                elif days_until_hearing <= 30:
                    status = "Upcoming"
                    urgency = "Medium"
                    description = "Hearing is within a month"
                else:
                    status = "Scheduled"
                    urgency = "Low"
                    description = "Hearing is scheduled for later"
                
                return {
                    'days_until_hearing': days_until_hearing,
                    'status': status,
                    'urgency': urgency,
                    'description': description
                }
            else:
                return {
                    'days_until_hearing': 'Unknown',
                    'status': 'Unknown',
                    'urgency': 'Unknown',
                    'description': 'Next hearing not scheduled'
                }
        except Exception as e:
            logger.error(f"Error analyzing hearing schedule: {e}")
            return {
                'days_until_hearing': 'Error',
                'status': 'Error',
                'urgency': 'Error',
                'description': 'Unable to analyze hearing schedule'
            }
    
    def _generate_insights(self, case_data: Dict, case_info: Dict, case_age: Dict) -> List[str]:
        """Generate AI insights about the case"""
        insights = []
        
        # Case type insights
        if case_info:
            insights.append(f"This is a {case_info.get('full_name', 'court case')} - {case_info.get('description', '')}")
            insights.append(f"Typical duration: {case_info.get('typical_duration', 'Unknown')}")
            insights.append(f"Success rate: {case_info.get('success_rate', 'Unknown')}")
        
        # Case age insights
        if case_age.get('status') != 'Unknown':
            insights.append(f"Case status: {case_age['status']} ({case_age['description']})")
            if case_age.get('age_years') != 'Unknown':
                insights.append(f"Case age: {case_age['age_years']} years")
        
        # Hearing insights
        if case_data.get('next_hearing'):
            insights.append(f"Next hearing: {case_data['next_hearing']}")
        
        # Parties analysis
        parties = case_data.get('parties', '')
        if 'vs.' in parties or 'v.' in parties:
            insights.append("This appears to be an adversarial proceeding")
        
        # Legal insights based on case type
        case_type = case_data.get('case_title', '').split()[0]
        if case_type == 'WP(C)':
            insights.append("Fundamental rights violation alleged")
            insights.append("Constitutional remedy sought")
        elif case_type == 'CRL.A':
            insights.append("Criminal conviction/acquittal under appeal")
            insights.append("Evidence and legal arguments crucial")
        elif case_type == 'CIVIL':
            insights.append("Civil dispute resolution")
            insights.append("Documentation and evidence important")
        elif case_type == 'CRL.M.C':
            insights.append("Interim relief in criminal matter")
            insights.append("Quick disposal possible")
        
        return insights
    
    def _generate_recommendations(self, case_data: Dict, case_info: Dict, case_age: Dict) -> List[str]:
        """Generate AI recommendations"""
        recommendations = []
        
        # General recommendations
        recommendations.append("Consider consulting with a legal expert")
        recommendations.append("Review all case documents thoroughly")
        
        # Case-specific recommendations
        case_type = case_data.get('case_title', '').split()[0]
        if case_type == 'WP(C)':
            recommendations.append("Focus on fundamental rights violation")
            recommendations.append("Prepare strong constitutional arguments")
        elif case_type == 'CRL.A':
            recommendations.append("Review evidence and legal precedents")
            recommendations.append("Consider alternative dispute resolution")
        elif case_type == 'CIVIL':
            recommendations.append("Gather all relevant documents")
            recommendations.append("Consider mediation if appropriate")
        elif case_type == 'CRL.M.C':
            recommendations.append("Prepare for quick hearing")
            recommendations.append("Focus on interim relief arguments")
        
        # Age-based recommendations
        if case_age.get('age_years') != 'Unknown':
            age = case_age['age_years']
            if age > 5:
                recommendations.append("Consider case status review")
                recommendations.append("Check for any procedural delays")
            elif age > 3:
                recommendations.append("Monitor case progress closely")
                recommendations.append("Prepare for potential settlement")
        
        return recommendations
    
    def _generate_ai_summary(self, case_data: Dict, insights: List[str], recommendations: List[str]) -> str:
        """Generate a comprehensive AI summary"""
        summary = f"🤖 **AI Case Analysis Summary**\n\n"
        
        summary += f"**Case Overview:**\n"
        summary += f"• {case_data.get('case_title', 'Unknown case')}\n"
        summary += f"• Parties: {case_data.get('parties', 'Unknown')}\n"
        summary += f"• Filed: {case_data.get('filing_date', 'Unknown')}\n"
        summary += f"• Next Hearing: {case_data.get('next_hearing', 'Not scheduled')}\n\n"
        
        summary += f"**Key Insights:**\n"
        for insight in insights[:5]:  # Limit to top 5 insights
            summary += f"• {insight}\n"
        
        summary += f"\n**AI Recommendations:**\n"
        for rec in recommendations[:3]:  # Limit to top 3 recommendations
            summary += f"• {rec}\n"
        
        summary += f"\n*This analysis is provided by AI and should not replace legal advice.*"
        
        return summary
    
    def answer_question(self, question: str, case_data: Dict) -> str:
        """Answer specific questions about the case"""
        question_lower = question.lower()
        
        if 'what' in question_lower and 'case' in question_lower:
            return f"This is a {case_data.get('case_title', 'court case')} involving {case_data.get('parties', 'the parties')}."
        
        elif 'when' in question_lower and 'filed' in question_lower:
            return f"The case was filed on {case_data.get('filing_date', 'an unknown date')}."
        
        elif 'next' in question_lower and 'hearing' in question_lower:
            return f"The next hearing is scheduled for {case_data.get('next_hearing', 'an unknown date')}."
        
        elif 'how' in question_lower and 'long' in question_lower:
            case_age = self._calculate_case_age(case_data.get('filing_date', ''))
            if case_age.get('age_years') != 'Unknown':
                return f"The case has been ongoing for {case_age['age_years']} years ({case_age['status']})."
            else:
                return "The case duration is unknown due to missing filing date."
        
        elif 'advice' in question_lower or 'recommend' in question_lower:
            recommendations = self._generate_recommendations(case_data, {}, {})
            return f"Based on the case details, I recommend: {'; '.join(recommendations[:3])}"
        
        else:
            return "I can help you with questions about case details, timeline, legal implications, and recommendations. Please ask a specific question about the case."

# Global AI bot instance
ai_bot = CourtAIBot() 