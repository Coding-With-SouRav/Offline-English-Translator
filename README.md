# English Translator Application

This Python application is a GUI-based translator tool that converts English text into multiple languages using Google Translate API. The application features a modern, user-friendly interface with several advanced functionalities.

## Key Features

1. **Multi-language Support**: Supports translation to 107 different languages including Bengali, Hindi, Spanish, French, Chinese, and many more.

2. **Auto-completion**: Provides word suggestions as you type English text, with words loaded from JSON files organized by first letter.

3. **Responsive UI**: Features a collapsible sidebar for language selection and adjustable text areas.

4. **Persistent Settings**: Saves window geometry and state between sessions using a configuration file.

5. **Cross-platform Compatibility**: Works on Windows and other platforms with proper icon handling.

## Technical Implementation

- **GUI Framework**: Built with `ttkbootstrap` for modern themed widgets
- **Translation Engine**: Uses `deep_translator` with Google Translate API
- **Text Handling**: Implements scrollable text areas with smart padding
- **Word Suggestions**: Loads words from JSON files in the "words" folder
- **Configuration**: Uses configparser to save/restore application state

## Usage

1. Type English text in the input area
2. Select target language from the sidebar
3. Click "Translate" or press Enter to get translation
4. Use arrow keys to navigate word suggestions
5. Toggle sidebar with the ☰ button

The application handles large texts by splitting them into chunks and provides smooth scrolling for both input and output areas.
## Demo Images

<img width="943" height="936" alt="Screenshot 2025-09-09 182227" src="https://github.com/user-attachments/assets/32970e3c-3f2f-4947-8c6d-531df1968623" />
<img width="944" height="938" alt="Screenshot 2025-09-09 182315" src="https://github.com/user-attachments/assets/5905b77a-0202-44e3-9009-98ad8bf38643" />
<img width="938" height="934" alt="Screenshot 2025-09-09 182359" src="https://github.com/user-attachments/assets/69c68c30-05d4-438d-96d2-f33fcf688bd8" />
