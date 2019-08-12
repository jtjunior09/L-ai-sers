# L-ai-sers

August 2, 2019

Simple PyGame with an evolving Neural Network.
Dodge lasers using w, a, s, d, or the arrow keys.
Player may loop around the top/bottom edges and if they reach the far left of the screen, they loop around to the right.


Players are rewarded for time lived and how many loops they acheived. 


## Dependencies
- Python 3.7
- PyGame 1.9.6
- NumPy 1.17.0
- SciPy 1.3.0

```
pip install pygame numpy scipy
```

## Running the game
```
python main.py
```

Edit Neural Network / Evolution settings via the variables in `Definitions.py`