validate:
	python3 tools/validate_book.py

build:
	python3 tools/build_book.py

epub: build
	@echo "EPUB built in build/book.epub"

pdf: build
	@echo "PDF built in build/book.pdf"

all: validate build
