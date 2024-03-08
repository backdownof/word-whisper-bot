import os
import asyncio
import logging

from views.middlewares.antispam import ThrottlingMiddleware
from views.middlewares.middleware import MessageMiddleware
from views import user

from dotenv import load_dotenv
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

load_dotenv()

logger = logging.getLogger(__name__)

ENV = os.getenv('SERVER_SOFTWARE')

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')
WEBAPP_PATH = os.getenv('WEBAPP_PATH')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_webhook(WEBHOOK_URL, certificate=types.FSInputFile('/opt/homebrew/etc/ssl/certs/self-signed.pem'))
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning('Shutting down..')

    await bot.delete_webhook()

    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

    logging.warning('Bye!')


# def prod_main():
#     storage = RedisStorage.from_url('redis://localhost:6379/0')

#     bot_settings = {"parse_mode": "HTML"}
#     bot = Bot(token=BOT_TOKEN, **bot_settings)

#     dp = Dispatcher(storage=MemoryStorage())
#     dp.message.filter(F.chat.type == "private")
#     dp.startup.register(on_startup)
#     dp.shutdown.register(on_shutdown)

#     ignore_middleware_router = Router()
#     ignore_middleware_router.include_router(character.router)

#     app_router = Router()
#     app_router.include_router(location.router)
#     app_router.include_router(fight.router)
#     app_router.include_router(inventory.router)
#     app_router.include_router(shop.router)
#     app_router.include_router(auction_house.router)
#     app_router.include_router(npc.router)
#     app_router.include_router(quests.router)
#     app_router.include_router(mail.router)
#     app_router.include_router(bank.router)
#     app_router.include_router(items.router)
#     app_router.include_router(fight_settings.router)
#     app_router.include_router(character_details.router)
#     app_router.include_router(arena.router)
#     app_router.include_router(gathering.router)

#     app_router.message.middleware(MessageMiddleware())
#     app_router.callback_query.middleware(MessageMiddleware())

#     dp.include_router(app_router)
#     dp.include_router(ignore_middleware_router)

#     dp.message.outer_middleware(ThrottlingMiddleware(storage))

#     app = web.Application()

#     SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBAPP_PATH)

#     setup_application(app, dp, bot=bot)

#     try:
#         web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
#     except Exception as ex:
#         logger.error(f"[Exception] {ex}", exc_info=True)
#     finally:
#         app.shutdown()


async def local_main():
    bot = Bot(token=BOT_TOKEN)

    storage = RedisStorage.from_url(f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0')

    try:
        dp = Dispatcher(storage=MemoryStorage())
        # TODO: allow only private chats
        # dp.message.filter(F.chat.type == "private")

        app_router = Router()
        app_router.include_router(user.router)

        app_router.message.middleware(MessageMiddleware())
        app_router.callback_query.middleware(MessageMiddleware())

        dp.include_router(app_router)

        dp.message.outer_middleware(ThrottlingMiddleware(storage))

        await bot.delete_webhook(drop_pending_updates=True)

        logger.info("Bot has started succesfully")
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(f"Exception: {ex}", exc_info=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(local_main())

    # if ENV.startswith('dev'):
    #     prod_main()
    # else:
    #     asyncio.run(local_main())
