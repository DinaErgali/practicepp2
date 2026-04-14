# Practice 09 - Game Development with Pygame

## How to Run

Install pygame first:
```
pip install pygame
```

Then run each project:
```
python mickeys_clock/main.py
python music_player/main.py
python moving_ball/main.py
```

## Projects

### 3.1 Mickey's Clock
- Displays current time (minutes and seconds)
- Right hand = minutes, Left hand = seconds
- Uses `pygame.transform.rotate()` to rotate Mickey hand images
- Updates every second

### 3.2 Music Player
- Keyboard controls: P=Play, S=Stop, N=Next, B=Back, Q=Quit
- Add .mp3 or .wav files to `music_player/music/` folder

### 3.3 Moving Ball
- Arrow keys move the red ball 20 pixels per press
- Ball stays within screen boundaries
