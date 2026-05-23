from flask_frozen import Freezer
from app import app

CONFIG = {
	#'FREEZER_BASE_URL': './',
	'FREEZER_STATIC_IGNORE': ['*.pdf', '*.JPG', '*.css', '*.js', '*.png'],
	# 'FREEZER_DESTINATION': '../static',
    'FREEZER_DESTINATION': '../docs',
    'FREEZER_DESTINATION_IGNORE': [],
    'FREEZER_BASE_URL': 'https://guglielmocamporese.github.io/',
}

app.config.update(**CONFIG)


freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()