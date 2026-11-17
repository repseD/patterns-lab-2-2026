import base64
from datetime import date

from interfaces import BaseMessage


class MessageDecorator(BaseMessage):
    def __init__(self, message: BaseMessage) -> None:
        self._message = message

    def render(self) -> str:
        return self._message.render()


class HeaderDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, header: str) -> None:
        super().__init__(message)
        self._header = header

    def render(self) -> str:
        return f"{self._header}\n{self._message.render()}"


class SignatureDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, signature: str) -> None:
        super().__init__(message)
        self._signature = signature

    def render(self) -> str:
        return f"{self._message.render()}\n{self._signature}"


class DateDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, current_date: date | None = None) -> None:
        super().__init__(message)
        self._date = current_date or date.today()

    def render(self) -> str:
        return f"{self._message.render()}\n{self._date.isoformat()}"


class Base64Decorator(MessageDecorator):
    def render(self) -> str:
        text = self._message.render()
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")
