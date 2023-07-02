import logging
from fastapi.responses import JSONResponse
from logic.message_processor import MessageProcessor


class MessageRouter:

    def __init__(self, message_processor: MessageProcessor) -> None:
        self.message_processor = message_processor

    async def load_all_messages_to_bd(
            self
    ):
        try:
            await self.message_processor.process_all_messages()
            return JSONResponse({'Status': 'Success'})
        except Exception as exc:
            logging.error(f'Error {exc}')
            return JSONResponse({'Status': 'Error'})

    async def load_unread_messages_to_bd(
            self
    ):
        try:
            await self.message_processor.process_unread_messages()
            return JSONResponse({'Status': 'Success'})
        except Exception as exc:
            logging.error(f'Error {exc}')
            return JSONResponse({'Status': 'Error'})
