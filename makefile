.PHONY: run
run:
	(. ./sigpro/venv/bin/activate; python3 ./sigpro/sigpro.py)

.PHONY: createvenv
createvenv:
	python3 -m venv ./sigpro/venv
	(. ./sigpro/venv/bin/activate; python3 -m pip install -r requirements.txt)

.PHONY: build
build:
	python3 -m build

.PHONY: clean
clean:
	trash -f dist/ sigpro.egg-info/ ./sigpro/__pycache__/
