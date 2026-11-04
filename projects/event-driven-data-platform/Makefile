.PHONY: install test run clean

install:
	pip install -e ".[dev]"

test:
	pytest -q

run:
	python -m event_platform.cli --input sample/orders.jsonl --output build

clean:
	rm -rf build .pytest_cache
