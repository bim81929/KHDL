from keras.applications.densenet import layers
from tensorflow import keras

def load_model(shape):
    model = keras.Sequential([
        layers.Dense(64, activation="relu"),
        layers.Dense(64, activation="relu"),
        layers.Dense(1)
    ])
    model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])

    model.build(input_shape=(shape))
    model.load_weights("./weights.h5")
    return model

