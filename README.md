# AI Training Example

This repository contains a small script for training a machine learning model on a CSV dataset.

## Usage

Install dependencies (requires Python 3.11):

```bash
pip install pandas scikit-learn joblib
```

Train a model by providing a CSV file and target column name:

```bash
python train_model.py path/to/data.csv --target label
```

The script splits the data into train/test sets, trains a random forest classifier, prints the test accuracy, and saves the model to `model.joblib` by default.

## White Surface

To display a simple white window using Tkinter:

```bash
python white_surface.py
```
