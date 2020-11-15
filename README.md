# Description

WildFireNet is a linear neural network which uses weather and satelitte data to form accurate predictions on the probability of there being a wildfire in any given location in the USA.

# Structure
Data: Contains datasets used for training and predicting
Preprocess: clean.py - combines and cleans datasets, predict.py - creates dataset to prediction features, transform.py - turns clean dataset into features
Results: Contains notebook showing resulting predictions
Train: Contains notebook where model is trained

# Results
Results can be viewed in results/Results. Here you can enter a location in the USA and data and the model's prediction will be returned.

# Future
In the future WildFireNet will reduce the radius of space it considers to form more precise predictions. Use geo-spatial data with convolutional neural networks. Scale to a global level.
