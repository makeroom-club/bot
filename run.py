import os
import sys

from dotenv import load_dotenv

from bot import bot


def main():
    load_dotenv()
    token = os.environ.get('TOKEN')

    if not token:
        return 'You must set a token as env var TOKEN or in a .env file.'

    bot.run(token)


if __name__ == '__main__':
    sys.exit(main())
