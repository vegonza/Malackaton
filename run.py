from flask import Flask, render_template,jsonify,request
from app.api.sql_api import sql_api_bp
from app.api.analytics_api import analytics_api_bp
from app.api.bot_detection_api import bot_detection_api_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.config.update(
    SECRET_KEY="python>java"
)

app.register_blueprint(sql_api_bp, url_prefix='/api/sql')
app.register_blueprint(analytics_api_bp, url_prefix="/api/analytics")
app.register_blueprint(bot_detection_api_bp, url_prefix="/api/bot_detection")

@app.route('/')
def index():
    return render_template("home.html")

if __name__ == '__main__':
    from app.api.sql_api import test_db
    response = test_db()
    print(response)
    app.run(debug=True)
