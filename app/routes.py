from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .scraper import fetch_case_details
from .ai_bot import ai_bot
from .models import QueryLog
from . import db
import json
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    result = None
    ai_analysis = None
    if request.method == 'POST':
        case_type = request.form.get('case_type', '').strip()
        case_number = request.form.get('case_number', '').strip()
        filing_year = request.form.get('filing_year', '').strip()

        # Validate inputs
        if not case_type or not case_number or not filing_year:
            flash('All fields are required', 'danger')
            return render_template('index.html')

        # Log the query attempt
        query_log = QueryLog(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year,
            timestamp=datetime.utcnow(),
            status='pending'
        )
        db.session.add(query_log)
        db.session.commit()

        try:
            # Call scraper function
            result, error = fetch_case_details(case_type, case_number, filing_year)
            
            # Update log with result
            query_log.status = 'success' if result else 'error'
            query_log.raw_response = json.dumps({
                'result': result,
                'error': error
            }, default=str)
            db.session.commit()

            if error:
                flash(error, 'danger')
                return render_template('index.html')
            
            # Get AI analysis if case found
            if result:
                ai_analysis = ai_bot.analyze_case(result)
            
            flash('Case details retrieved successfully!', 'success')
            return render_template('results.html', result=result, ai_analysis=ai_analysis)
            
        except Exception as e:
            # Update log with error
            query_log.status = 'error'
            query_log.raw_response = json.dumps({'error': str(e)}, default=str)
            db.session.commit()
            
            flash(f'An unexpected error occurred: {str(e)}', 'danger')
            return render_template('index.html')
    
    return render_template('index.html')

@main.route('/download/<path:pdf_url>')
def download_pdf(pdf_url):
    """Download PDF from the court website"""
    try:
        import requests
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()
        
        from flask import send_file
        from io import BytesIO
        
        # Create a file-like object from the response content
        pdf_content = BytesIO(response.content)
        pdf_content.seek(0)
        
        return send_file(
            pdf_content,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'court_order_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    except Exception as e:
        flash(f'Error downloading PDF: {str(e)}', 'danger')
        return redirect(url_for('main.index'))

@main.route('/history')
def query_history():
    """Show query history"""
    logs = QueryLog.query.order_by(QueryLog.timestamp.desc()).limit(50).all()
    return render_template('history.html', logs=logs)

@main.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for AJAX searches"""
    data = request.get_json()
    case_type = data.get('case_type', '').strip()
    case_number = data.get('case_number', '').strip()
    filing_year = data.get('filing_year', '').strip()

    if not case_type or not case_number or not filing_year:
        return jsonify({'error': 'All fields are required'}), 400

    result, error = fetch_case_details(case_type, case_number, filing_year)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Get AI analysis
    ai_analysis = ai_bot.analyze_case(result) if result else None
    
    return jsonify({'result': result, 'ai_analysis': ai_analysis})

@main.route('/api/ask', methods=['POST'])
def ask_ai():
    """API endpoint for asking AI questions about cases"""
    data = request.get_json()
    question = data.get('question', '').strip()
    case_data = data.get('case_data', {})

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    try:
        answer = ai_bot.answer_question(question, case_data)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': f'Error processing question: {str(e)}'}), 500

@main.route('/api/analyze', methods=['POST'])
def analyze_case():
    """API endpoint for AI case analysis"""
    data = request.get_json()
    case_data = data.get('case_data', {})

    if not case_data:
        return jsonify({'error': 'Case data is required'}), 400

    try:
        analysis = ai_bot.analyze_case(case_data)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': f'Error analyzing case: {str(e)}'}), 500
