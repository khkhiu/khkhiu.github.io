name: Deploy Sphinx to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install sphinx furo ghp-import

      - name: Build HTML
        run: |
          cd docs
          make html

      - name: Deploy to GitHub Pages
        run: |
          ghp-import -n -p -f docs/build/html
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
