from ExpenseLog_Website import create_app
from flask_bootstrap import Bootstrap

app = create_app()
bootstrap = Bootstrap(app)

if __name__ =='__main__':
    app.run(debug=True)