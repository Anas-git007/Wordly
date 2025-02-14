# Wordly - A Fun Word Guessing Game  

**Wordly** is a word-guessing game built with Python and Pygame. The game challenges players to guess a hidden word, providing color-coded feedback for correct and misplaced letters. It also features background music and sound effects for a more engaging experience.  

## Features  
- Fetches a random word using an **API** 🖥️  
- Validates user-entered words using another **API** 🌍  
- **Color-coded feedback** (like Wordle) for correct/misplaced letters 🎨  
- **Background music and sound effects** for a better experience 🎵  
- **Interactive UI** built with Pygame 🕹️  

## How It Works  
1. The game fetches a random word from an API.  
2. The player enters a word, which is validated against an API to check if it's real.  
3. The game provides feedback with colored tiles:  
   - 🟩 Green: Correct letter in the correct position  
   - 🟨 Yellow: Correct letter in the wrong position  
4. If the player wins or loses, a sound effect is played.  

## APIs Used  
- **Random Word Fetching**: `https://api.datamuse.com/words`  
- **Word Validation**: `https://api.dictionaryapi.dev/api/v2/entries/en/`  

## Contributing  
Feel free to fork the repository and submit pull requests!  
