from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from routes.auth import auth_bp
import os

# Get absolute paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

# Health check (JSON API)
@app.route('/api/health')
def api_health():
    return jsonify({'message': 'GEN GRADE Backend is running!'})

# HTML page routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/mycourses')
def mycourses():
    return render_template('mycourses.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/career')
def career():
    return render_template('career.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/lesson')
def lesson():
    return render_template('lesson.html')

# Fallback for static files (CSS, JS, fonts)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Template folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")
    app.run(debug=True, port=port, use_reloader=False)
