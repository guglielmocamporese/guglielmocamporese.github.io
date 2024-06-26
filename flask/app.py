from flask import Flask, render_template, request, redirect, url_for
from firebase import firebase
import os
import json
import sys

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
@app.route('/index.html')
def home():
	return render_template('home.html', base_dir='.', page_title='Bio')

@app.route('/news.html')
def news():
	return render_template('news.html', base_dir='.', page_title='News')

# Puplications
@app.route('/publications.html')
def publications():
	def read_publication_file(pub_path):
		"""
		A publication has the following fields:
			[title, authors, conference(, link, code)]
		"""
		keys = ['title', 'authors', 'conference', 'link', 'code']
		pub = {}
		with open(pub_path, 'r') as f:
			lines = [l.strip() for l in f.readlines() if len(l) > 0]
		if len(lines) == 3:
			del keys[3]
			del keys[3]

		for k, l in zip(keys, lines):
			pub[k] = l
		return pub

	pubs = []
	pubs_basepath = './static/publications'
	filenames = reversed(sorted([f.replace('.txt', '') for f in os.listdir(pubs_basepath) if '.txt' in f]))
	for f in filenames:
		pub_path = os.path.join(pubs_basepath, f'{f}.txt')
		pub = read_publication_file(pub_path)
		pub['number'] = f
		pubs += [pub]
	return render_template('publications.html', base_dir='.', pubs=pubs, page_title='Publications')

@app.route('/extra.html')
def extra():
	return render_template('extra.html', base_dir='.', page_title='Extra')

@app.route('/extras/mosquito.html')
def extra_mosquito():
	return render_template('extras/mosquito.html', base_dir='..', page_title='Computing the Probability of Catching a Mosquito by Hands')

@app.route('/extras/nn_tricks.html')
def extra_nn_tricks():
	return render_template('extras/nn_tricks.html', base_dir='..', page_title='Bag of Tricks for Training Neural Networks')

@app.route('/extras/nn_common_errors.html')
def extra_nn_common_errors():
	return render_template('extras/nn_common_errors.html', base_dir='..', page_title='Common Errors on Training Neural Networks')

@app.route('/extras/fourier.html')
def extra_fourier():
	return render_template('extras/fourier.html', base_dir='..', page_title='Fourier Representation Meets Images')

@app.route('/extras/places.html')
def extra_places():
	return render_template('extras/places.html', base_dir='..', page_title='Places I\'ve Seen So Far')

@app.route('/extras/spotify.html')
def extra_spotify():
	return render_template('extras/spotify.html', base_dir='..', page_title='My Spotify Playlists!')

if __name__ == '__main__':
	app.run(debug=True)