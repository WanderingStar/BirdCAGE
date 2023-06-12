from flask import Flask, render_template, redirect, url_for
import requests
from datetime import datetime, date
import os
from calendar import monthrange

app = Flask(__name__)

API_SERVER_URL = os.environ.get('API_SERVER_URL', 'http://192.168.1.75:7006')
WEBUI_PORT = os.environ.get('WEBUI_PORT', '7009')
TITLE_TEXT = os.environ.get('TITLE_TEXT', '')
TITLE_LINK = os.environ.get('TITLE_LINK', '')
URL_PREFIX = os.environ.get('URL_PREFIX', '')


@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', api_server_url=API_SERVER_URL, today=today, title_text=TITLE_TEXT,
                           title_link=TITLE_LINK, url_prefix=URL_PREFIX)


@app.route('/detections/by_hour/<date>/<int:hour>')
def show_detections_by_hour(date, hour):
    return render_template('detections_by_hour.html', date=date, api_server_url=API_SERVER_URL, hour=hour)


@app.route('/detections/by_common_name/<common_name>/<date>', defaults={'end_date': None})
@app.route('/detections/by_common_name/<common_name>/<date>/<end_date>')
def show_detections_by_common_name(common_name, date, end_date):
    return render_template('detections_by_name.html', api_server_url=API_SERVER_URL, common_name=common_name, date=date, end_date=end_date)


@app.route('/daily_summary/<date>')
def daily_summary(date):
    return render_template('daily_summary.html', date=date, api_server_url=API_SERVER_URL)


@app.route('/stream_settings', methods=['GET'])
def streams():
    return render_template('stream_settings.html', api_server_url=API_SERVER_URL)


@app.route('/preferences', methods=['GET'])
def preferences():
    user_id = 0
    response = requests.get(f"{API_SERVER_URL}/api/preferences/{user_id}")
    current_preferences = response.json()
    return render_template('preferences.html', api_server_url=API_SERVER_URL, current_preferences=current_preferences)


@app.route('/detections/detection/<int:detection_id>')
def show_detection_details(detection_id):
    return render_template('detection_details.html', detection_id=detection_id, api_server_url=API_SERVER_URL)


@app.route('/birdsoftheweek')
def birds_of_the_week():
    return render_template('birdsoftheweek.html', api_server_url=API_SERVER_URL)


@app.route('/detection_filters')
def detection_filters():
    return render_template('detection_filters.html', api_server_url=API_SERVER_URL)


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", api_server_url=API_SERVER_URL)


@app.route('/notification_settings', methods=['GET'])
def notification_settings():
    return render_template('notifications_settings.html', api_server_url=API_SERVER_URL)


@app.route('/weekly_report/', defaults={'week': None})
@app.route('/weekly_report/<week>')
def weekly_report(week):
    if not week:
        today = date.today()
        year, week_number, _ = today.isocalendar()
        week = f"{year}-W{week_number}"

        # Redirect to the URL with the current week
        return redirect(url_for('weekly_report', week=week))

    return render_template('weekly_report.html', week=week, api_server_url=API_SERVER_URL, url_prefix=URL_PREFIX)


@app.route('/monthly_report/', defaults={'month': None})
@app.route('/monthly_report/<month>')
def monthly_report(month):
    if not month:
        today = date.today()
        year = today.year
        month_number = today.month
        month = f"{year}-{month_number:02d}"

        # Redirect to the URL with the current month
        return redirect(url_for('monthly_report', month=month))

    return render_template('monthly_report.html', month=month, api_server_url=API_SERVER_URL, url_prefix=URL_PREFIX)


@app.route('/annual_report/', defaults={'year': None})
@app.route('/annual_report/<int:year>')
def annual_report(year):
    if not year:
        today = date.today()
        year = today.year
        # Redirect to the URL with the current year
        return redirect(url_for('annual_report', year=year))

    return render_template('annual_report.html', year=year, api_server_url=API_SERVER_URL, url_prefix=URL_PREFIX)


@app.route('/app_health', methods=['GET'])
def app_health_task_health():
    return render_template('app_health.html', api_server_url=API_SERVER_URL)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(WEBUI_PORT))
