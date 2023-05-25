# Simpsons Episodes Web Scraping Pipeline

This repository is used to update my Simpsons tv episode data on Kaggle. Please see about.md for the datacard used on Kaggle.

Using GitHub Actions, the generator file is run on the first of every month (or on push for testing). If there is new data available the Kaggle dataset is updated via the Kaggle API. The generator relies on scraping Wikipedia and IMDB data as well as using The Movie Database API. GitHub Secrets are used to maintain API access tokens.

# Important Files

- simpsons-generator.py: Constructs simpsons episode data and determines if new episodes are avaiable. If new episodes are available, save dataset to data folder and update Kaggle.
- data/dataset-metadata.json: Contains Kaggle dataset path for API update.
- simpsons-tv-data-generator.ipynb: Notebook with code used for data construction. Used for testing purposes.
- simpsons-performance-with-r-sql.r: R notebook used for simple analysis

[Kaggle Dataset](https://www.kaggle.com/datasets/jonbown/simpsons-episodes-2016)
