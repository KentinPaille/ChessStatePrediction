import os
import pandas as pd
import re

BASE_DIR = "datasets"

def parse_line(line, category):
    parts = line.strip().split()
    try:
        idx = parts.index('w') if 'w' in parts else parts.index('b')
        fen = " ".join(parts[:idx+1])
    except ValueError:
        fen = " ".join(parts[:6])
    label = None
    line_lower = line.lower()
    if "stalemate" in line_lower:
        label = "draw"
    elif "checkmate" in line_lower:
        label = "checkmate"
    elif "check" in line_lower:
        label = "check"
    elif "nothing" in line_lower:
        label = "ongoing"
    else:
        label = category
    return fen, label

all_fens = []
all_labels = []

for category in os.listdir(BASE_DIR):
    category_path = os.path.join(BASE_DIR, category)
    if not os.path.isdir(category_path):
        continue
    for filename in os.listdir(category_path):
        file_path = os.path.join(category_path, filename)
        if not filename.endswith(".txt"):
            continue
        with open(file_path, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                fen, label = parse_line(line, category)
                all_fens.append(fen)
                all_labels.append(label)

df = pd.DataFrame({"FEN": all_fens, "State": all_labels})
print(df["State"].value_counts())
print(df.head())

df.to_csv("all_fens_labeled.csv", index=False)
print("Fichier global all_fens_labeled.csv créé !")

fens = df["FEN"].values
states = df["State"].values
