.PHONY: test test-preprocess test-module2 clean

VENV = .venv
PYTHON = $(VENV)/bin/python

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -p "test_*.py"

test-preprocess:
	PYTHONPATH=src $(PYTHON) -m unittest tests/test_preprocess.py

test-module2:
	PYTHONPATH=src $(PYTHON) -m unittest tests/test_fingerprint.py

test-module3:
	PYTHONPATH=src $(PYTHON) -m unittest tests/test_vocal_match.py

test-module4:
	PYTHONPATH=src $(PYTHON) -m unittest tests/test_recognize.py

# Pour installer les dépendances rapidement si besoin
install:
	$(PYTHON) -m pip install -r requirements.txt

# Nettoyage des caches Python
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
