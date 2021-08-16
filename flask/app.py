from flask import Flask, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('home.html', base_dir='.')

@app.route('/news.html')
def news():
    return render_template('news.html', base_dir='.')

@app.route('/publications.html')
def publications():
    return render_template('publications.html', base_dir='.')

# Extras
@app.route('/extra.html')
def extra():
    return render_template('extra.html', base_dir='.')

@app.route('/extras/mosquito.html')
def extra_mosquito():
    return render_template('extras/mosquito.html', base_dir='..')

@app.route('/extras/nn_tricks.html')
def extra_nn_tricks():
    return render_template('extras/nn_tricks.html', base_dir='..')

@app.route('/extras/nn_common_errors.html')
def extra_nn_common_errors():
    return render_template('extras/nn_common_errors.html', base_dir='..')

if __name__ == '__main__':
	app.run(debug=True)