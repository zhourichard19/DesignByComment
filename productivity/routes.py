from productivity import app

@app.route('/')
@app.route('/home')
def home_page():
    return "hello world"