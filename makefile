.PHONY: build, install, uninstall

build:
	rm -rf dist/
	poetry build

install:
	pip install dist/backlight*whl

uninstall:
	pip uninstall backlight
