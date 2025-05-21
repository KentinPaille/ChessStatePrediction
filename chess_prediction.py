import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input
from tensorflow.keras.utils import to_categorical

def fen_to_onehot(fen):
    piece_list = ['p', 'n', 'b', 'r', 'q', 'k', 'P', 'N', 'B', 'R', 'Q', 'K']
    piece_to_idx = {p: i for i, p in enumerate(piece_list)}
    board, *_ = fen.split()
    rows = board.split('/')
    onehot = np.zeros((8, 8, 13), dtype=np.int8)
    for i, row in enumerate(rows):
        col = 0
        for char in row:
            if char.isdigit():
                col += int(char)
            else:
                idx = piece_to_idx[char]
                onehot[i, col, idx] = 1
                col += 1
    return onehot

df = pd.read_csv("all_fens_labeled.csv")
print("Dataset loaded:", df.shape)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["State"].values)
num_classes = len(label_encoder.classes_)
y_cat = to_categorical(y, num_classes=num_classes)

print("Encodage des FEN (one-hot spatial)...")
X = np.array([fen_to_onehot(fen) for fen in df["FEN"].values])

X_train, X_test, y_train, y_test = train_test_split(
    X, y_cat, test_size=0.2, stratify=y, random_state=42
)

model = Sequential([
    Input(shape=(8, 8, 13)),
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(
    X_train, y_train,
    epochs=3,
    batch_size=32,
    validation_split=0.1,
    verbose=2
)

loss, acc = model.evaluate(X_test, y_test, verbose=2)
print(f"Test accuracy: {acc:.3f}")

def predict_fen(fen):
    x = np.array([fen_to_onehot(fen)])
    pred = model.predict(x)
    class_idx = np.argmax(pred)
    return label_encoder.inverse_transform([class_idx])[0]

example_fen = "8/1k6/2r5/3Q4/8/8/8/4K3 b"
print("Example FEN:", example_fen)
print("Predicted state:", predict_fen(example_fen))