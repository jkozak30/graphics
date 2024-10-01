test: face.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py gallery.mdl

clean:
	rm *pyc *out parsetab.py imgs/*.png

clear:
	rm *pyc *out parsetab.py *ppm

convert:
	convert imgs/*.png -delay 1.7 imgs/animation.gif
