from flask import Flask, render_template
from app.api.sql_api import sql_api_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.config.update(
    SECRET_KEY="python>java"
)

app.register_blueprint(sql_api_bp, url_prefix='/api/sql')

@app.route('/')
def index():
    return render_template("home.html")

if __name__ == '__main__':
    from app.api.sql_api import test_db
    response = test_db()
    print(response)
    app.run(debug=True)
