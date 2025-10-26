OUT_FILE = ./data/cucumber_repositories.json

run:
	python -B src/main.py --out $(OUT_FILE)

filter:
	python -B src/filter-repos-by-langs.py ./data/cucumber_repositories_2025-10-26_19-59-35.json -l nodejs java ruby -o ./data/projects_discovery.json