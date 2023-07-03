import asyncio
import datetime
import logging
import uvicorn

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from injector import Injector
from fastapi import FastAPI

from application.routers import MessageRouter
from logic.message_processor import MessageProcessor
from logic.bot.tg_bot import ILSSBot
from settings import Settings


class App:

    def __init__(self, container):
        self.container = Injector(container)
        self.app = FastAPI()
        self.loop = asyncio.get_event_loop()
        self.server = self.init_server(self.loop)
        self.bot = self.container.get(ILSSBot)
        self.settings = self.container.get(Settings)
        self.message_router = self.container.get(MessageRouter)
        self.message_processor = self.container.get(MessageProcessor)
        self._scheduler = AsyncIOScheduler({'event_loop': self.loop})

    def start(self):

        self.add_routes()
        self.add_jobs()

        try:
            logging.info(f'Start application')
            tasks = asyncio.gather(
                self.server.serve(),
                self.bot.dp.start_polling()
            )
            self.loop.run_until_complete(tasks)

            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        except Exception:
            logging.error('Unexpected error')
        finally:
            self.loop.close()

    def init_server(self, loop):
        config = uvicorn.Config(app=self.app,
                                loop=loop,
                                host='0.0.0.0')

        return uvicorn.Server(config)

    def add_routes(self):
        self.app.add_api_route(
            '/load_all_message_history',
            self.message_router.load_all_messages_to_bd,
            methods=['POST']
        )
        self.app.add_api_route(
            '/load_unread_messages',
            self.message_router.load_unread_messages_to_bd,
            methods=['POST']
        )

    def add_jobs(self):
        self._scheduler.add_job(
            self.message_processor.process_unread_messages,
            trigger='cron',
            second=self.settings.load_schedule_second,
            minute=self.settings.load_schedule_minute,
            hour=self.settings.load_schedule_hour,
            day_of_week=self.settings.load_schedule_day_of_week,
            timezone='Asia/Tomsk'
        )
