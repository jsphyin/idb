run:
	./serve -k

compile:
	browserify src/index.js -o static/index.js -t [ babelify --presets [ es2015 react ] ]

minify:
	browserify src/index.js -t [ babelify --presets [ es2015 react ] ] -i reactstrap-tether | uglifyjs -o static/index.js

test:
	(export SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:boardgamers@127.0.0.1:3306/proddata; python tests.py)
	python selenium_tests.py
