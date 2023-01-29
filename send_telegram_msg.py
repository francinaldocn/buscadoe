"""Load dependencies."""
import telepot


def send_message(token: str, receive_id: int, message: str) -> None:
    """
    Send a chat message to Telegram.

        Parameters:
            token (str): Telegran Bot Token
            receive_id (str): Telegram Bot Receive ID
            message (str): Message to send
        Returns: None
    """
    # Telegram Bot
    bot = telepot.Bot(token)

    # Send message to Telegram
    bot.sendMessage(receive_id, message, parse_mode="html")
