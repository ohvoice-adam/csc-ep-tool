import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# Load data from JSON files
def load_data():
    with open('data/polling_places.json', 'r') as f:
        polling_places = json.load(f)
    with open('data/reports.json', 'r') as f:
        reports = json.load(f)
    return polling_places, reports

def save_reports(reports):
    with open('data/reports.json', 'w') as f:
        json.dump(reports, f, indent=2)

# Mock authentication
MOCK_USERS = {
    'admin': 'demo'
}

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('polling_places_list'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in MOCK_USERS and MOCK_USERS[username] == password:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('polling_places_list'))
        else:
            flash('Invalid credentials. Try admin/demo', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/polling-places')
@login_required
def polling_places_list():
    polling_places, reports = load_data()

    # Get filter parameters
    county_filter = request.args.get('county', '')
    risk_min = request.args.get('risk_min', 0, type=int)
    risk_max = request.args.get('risk_max', 100, type=int)
    sort_by = request.args.get('sort', 'risk_score')
    sort_order = request.args.get('order', 'desc')

    # Filter polling places
    filtered_places = polling_places

    if county_filter:
        filtered_places = [p for p in filtered_places if p['county'] == county_filter]

    filtered_places = [p for p in filtered_places if risk_min <= p['risk_score'] <= risk_max]

    # Sort polling places
    reverse = (sort_order == 'desc')
    if sort_by in ['risk_score', 'total_voters', 'multi_state_registrations', 'recent_registrations', 'purged_voters']:
        filtered_places.sort(key=lambda x: x[sort_by], reverse=reverse)
    elif sort_by == 'name':
        filtered_places.sort(key=lambda x: x['name'], reverse=reverse)
    elif sort_by == 'county':
        filtered_places.sort(key=lambda x: x['county'], reverse=reverse)

    # Count reports for each polling place
    report_counts = {}
    for report in reports:
        pp_id = report['polling_place_id']
        report_counts[pp_id] = report_counts.get(pp_id, 0) + 1

    # Add report counts to polling places
    for place in filtered_places:
        place['report_count'] = report_counts.get(place['id'], 0)

    # Get unique counties for filter dropdown
    counties = sorted(set(p['county'] for p in polling_places))

    return render_template('polling_places_list.html',
                         polling_places=filtered_places,
                         counties=counties,
                         current_county=county_filter,
                         current_risk_min=risk_min,
                         current_risk_max=risk_max,
                         current_sort=sort_by,
                         current_order=sort_order)


@app.route('/polling-places/<place_id>')
@login_required
def polling_place_detail(place_id):
    polling_places, reports = load_data()

    # Find the polling place
    place = next((p for p in polling_places if p['id'] == place_id), None)
    if not place:
        flash('Polling place not found', 'error')
        return redirect(url_for('polling_places_list'))

    # Get reports for this polling place
    place_reports = [r for r in reports if r['polling_place_id'] == place_id]
    place_reports.sort(key=lambda x: x['timestamp'], reverse=True)

    return render_template('polling_place_detail.html',
                         place=place,
                         reports=place_reports)


@app.route('/map')
@login_required
def map_view():
    return render_template('map.html')


@app.route('/report', methods=['GET', 'POST'])
@login_required
def submit_report():
    polling_places, reports = load_data()

    if request.method == 'POST':
        # Generate new report ID
        report_id = f"rpt-{len(reports) + 1:03d}"

        new_report = {
            'id': report_id,
            'polling_place_id': request.form.get('polling_place_id'),
            'reporter_name': request.form.get('reporter_name'),
            'reporter_email': request.form.get('reporter_email'),
            'reporter_phone': request.form.get('reporter_phone', ''),
            'issue_type': request.form.get('issue_type'),
            'description': request.form.get('description'),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'status': 'reported'
        }

        reports.append(new_report)
        save_reports(reports)

        flash('Report submitted successfully!', 'success')
        return redirect(url_for('polling_place_detail', place_id=new_report['polling_place_id']))

    # GET request - show form
    preselected_place_id = request.args.get('polling_place_id', '')
    return render_template('report_form.html',
                         polling_places=polling_places,
                         preselected_place_id=preselected_place_id)


# API endpoints for map
@app.route('/api/polling-places')
@login_required
def api_polling_places():
    polling_places, reports = load_data()

    # Count reports for each polling place
    report_counts = {}
    for report in reports:
        pp_id = report['polling_place_id']
        report_counts[pp_id] = report_counts.get(pp_id, 0) + 1

    # Add report counts
    for place in polling_places:
        place['report_count'] = report_counts.get(place['id'], 0)

    return jsonify(polling_places)


@app.route('/api/reports')
@login_required
def api_reports():
    _, reports = load_data()
    return jsonify(reports)


@app.route('/health')
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
