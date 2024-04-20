import kaggle

kaggle.api.authenticate()
# kaggle.api.dataset_download_files('shubhambathwal/flight-price-prediction', path='.', unzip=True)
# kaggle.api.dataset_metadata('shubhambathwal/flight-price-prediction', path='.')
# print(kaggle.api.dataset_list_files('shubhambathwal/flight-price-prediction').files)
# pip install urllib3==1.26.15

ds = kaggle.api.dataset_list(search='put option 2024')
print(ds)
