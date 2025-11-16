# Kaizen Team Bot

## Setup
1. Copy `config.py.example` to `config.py`
2. Fill in your bot token and user IDs in `config.py`:
   - `TOKEN`: Your bot token from @BotFather
   - `ADMIN_ID`: Your Telegram user ID (get it from @userinfobot)
   - `OPERATORS_IDS`: List of operator user IDs
   - `EDITORS_IDS`: List of editor user IDs
   - `VISITORS_IDS`: List of visitor user IDs
3. Run: `pip install -r requirements.txt`
4. Run: `python main.py`

## Development
This project uses modular MVC architecture with separate Models, Services, and Handlers.
