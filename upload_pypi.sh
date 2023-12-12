git pull
rm -rf dist/
poetry build
twine upload dist/*

