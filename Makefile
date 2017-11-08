run:
	./serve -k

compile:
	browserify src/index.js -o static/index.js -t [ babelify --presets [ es2015 react ] ]

minify:
	browserify src/index.js -t [ babelify --presets [ es2015 react ] ] -i reactstrap-tether | uglifyjs static/index.js
