# Description
## The Problem
Between 1972 and 2018 California has seen a 5-fold increase in it’s annual burned area. As the climate crisis deepens, wildfires are expected increase further and with it must come preventative action. Wildfires are notoriously hard to predict with a vast array of differing indicators from wind speed to soil moisture. 

## Our Solution
WildFireNet is a deep artificial neural network which uses weather and satelitte data to foresee the likelihood of a wildfire starting, and remaining active, 7 days after the given date at which the climate evaluation is made, or 30 days after the date at which the climate evaluation is made.

# Structure
- `data`: Contains datasets used for training and predicting

- `preprocess`: `clean.py` combines and cleans datasets, `predict.py` creates dataset to prediction features, and `transform.py` turns clean dataset into features

- `results`: Contains notebook showing predictions resulting from the preliminary model, as described in the `roadmap.pdf` file.

- `train`: Contains the notebook in which the preliminary model was trained (Note: The model was trained using smaller versions of the datasets which can found here: https://drive.google.com/drive/folders/1G8R_xnjWk9WEXvx_hwYQT3rgDVywe1lW?usp=sharing) 

# Video

https://youtu.be/xcbF_KvtFnk

# Results
Results can be viewed by consulting the files found in `results`. Here you can enter a location in the USA, in addition to other relevant data attributes (said attributes may be found in the training notebook) and the model's prediction will be returned.

# Future
The future developments this model will likely be subject to may be found in the `roadmap.pdf` file.
