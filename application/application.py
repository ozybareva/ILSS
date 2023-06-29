import asyncio
import logging
import uvicorn

from injector import Injector
from fastapi import FastAPI
from logic.bot.tg_bot import ILSSBot


class App:

    def __init__(self, container):
        self.container = Injector(container)
        self.app = FastAPI()
        self.loop = asyncio.get_event_loop()
        self.server = self.init_server(self.loop)
        self.bot = self.container.get(ILSSBot)

    def init_server(self, loop):
        config = uvicorn.Config(app=self.app,
                                loop=loop,
                                host='0.0.0.0')

        return uvicorn.Server(config)

    def start(self):
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
