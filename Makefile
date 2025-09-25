.PHONY: reqs

# Export a clean requirements.txt from uv
reqs:
	uv export --no-hashes --format requirements-txt > requirements.txt
