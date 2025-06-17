# ♟️ ChessAI - Chess Game State Detection

This project provides tools to generate, label, and parse chess positions (in FEN format) for building machine learning or deep learning models to detect the current state of a chess game: `ongoing`, `check`, `checkmate`, or `draw`.

---

## 📁 Project Structure

```
├── utils/
    └── chess_generate.py         # Generate labeled random legal FEN positions
    └── determine_state.py        # Aggregate and label FENs from text datasets
    └── parse_chess_state.py      # Convert FENs to one-hot encoded 3D arrays
├── chessai.ipynb             # Notebook for testing, visualization, and experimentation
├── datasets/                 # Folder containing text-based FENs by category
```

---

## ⚙️ Scripts Overview

### `chess_generate.py`

- Generates random legal FEN positions for different game states.
- Creates a labeled dataset (`custom_chess_states.csv`).

**Run it:**
```bash
python chess_generate.py
```

---

### `determine_state.py`

- Scans the `datasets/` folder for `.txt` files inside subfolders named after categories.
- Extracts FENs and infers their game state labels (`check`, `checkmate`, `draw`, `ongoing`).
- Saves all data into `all_fens_labeled.csv`.

**Expected `datasets/` structure:**
```
datasets/
  ├── check/
  │   └── 10_pieces.txt
  |   └── 20_pieces.txt
  |   └── many_pieces.txt
  ├── checkmate/
  │   └── 10_pieces.txt
  |   └── 20_pieces.txt
  |   └── many_pieces.txt
  ├── draw/
  │   └── 10_pieces.txt
  |   └── 20_pieces.txt
  |   └── many_pieces.txt
  └── ongoing/
      └── 10_pieces.txt
      └── 20_pieces.txt
      └── many_pieces.txt
```

---

### `parse_chess_state.py`

- Converts a FEN string into a one-hot encoded tensor of shape `(8, 8, 13)` (12 pieces + empty square).
- Includes batch and parallel processing utilities.

**Key functions:**
- `fen_to_onehot(fen)`
- `batch_fens_to_arrays(fens)`
- `parallel_batch_fens_to_arrays(fens, workers=4)`

---

### `chessai.ipynb`

A Jupyter notebook for:
- Data exploration and visualization
- FEN to tensor transformation
- Integration with machine learning pipelines

---

## 📦 Dependencies

- `python-chess`
- `pandas`
- `numpy`

**Installation:**
```bash
pip install python-chess pandas numpy
```

---

## 👥 Authors

- William Stoops
- Kentin Paille
Developed as part of a master’s degree team project.
