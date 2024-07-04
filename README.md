# Regex Bot

This bot is designed to assist with the creation, management, and execution of regular expressions. Whether you're a beginner or an expert, this bot provides an intuitive interface to add, delete, and test regular expressions with ease. You can also manage flags and switch between different languages for a more customized experience.

## Features

- Add, delete, and list regular expressions
- Apply regular expressions to text
- Manage flags for regular expressions
- Multi-language support

## Commands

- /start - Start interacting with the bot
- /help - Get information on how to use the bot
- /lang - Change the language of the bot
- /add_pattern - Add a new regular expression
- /delete_pattern - Delete an existing regular expression
- /add_flag - Add a flag to a regular expression
- /pattern_list - List all your regular expressions
- /parse - Execute a regular expression on a text

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/regex_bot.git
   cd regex_bot
   ```
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your bot token:
   ```
   TELEGRAM=your_bot_token
   ```

## Usage

1. Run the bot:
   ```
   python main.py
   ```
2. Start interacting with the bot on Telegram.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any issues or questions, please contact the creator @lixelv.
