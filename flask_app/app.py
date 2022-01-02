import random
from flask import Flask, render_template, request
from tensorflow.keras.datasets import boston_housing
import house_prices
    
(train_data, train_targets), (test_data, test_targets) = (
    boston_housing.load_data()
)

mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std
test_data -= mean
test_data /= std

model = house_prices.load_model(test_data.shape)
predictions = model.predict(test_data)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    app.logger.warning(request.form.get("id"))
    id = request.form.get("id", "undefined")

    if id == "undefined" or id == "" or int(id) >= test_data.shape[0]:
        return render_template("predictions.html", id=0, price=predictions[0])
    
    return render_template("predictions.html", id=id, price=predictions[int(id)])
