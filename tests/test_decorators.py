import base64
from datetime import date

from decorators import (
    Base64Decorator,
    DateDecorator,
    HeaderDecorator,
    SignatureDecorator,
)
from messages import Message


def test_header_decorator() -> None:
    message = HeaderDecorator(Message("hello"), "Title")
    assert message.render() == "Title\nhello"


def test_signature_decorator() -> None:
    message = SignatureDecorator(Message("hello"), "-- Alice")
    assert message.render() == "hello\n-- Alice"


def test_date_decorator() -> None:
    message = DateDecorator(Message("hello"), date(2026, 1, 15))
    assert message.render() == "hello\n2026-01-15"


def test_base64_decorator() -> None:
    message = Base64Decorator(Message("hello"))
    expected = base64.b64encode(b"hello").decode("utf-8")
    assert message.render() == expected


def test_decorators_combination() -> None:
    message = Base64Decorator(
        SignatureDecorator(
            DateDecorator(HeaderDecorator(Message("hello"), "Title"), date(2026, 1, 15)),
            "-- Alice",
        )
    )
    expected_text = "Title\nhello\n2026-01-15\n-- Alice"
    assert message.render() == base64.b64encode(expected_text.encode()).decode("utf-8")


def test_decorator_order_matters() -> None:
    first = DateDecorator(SignatureDecorator(Message("hello"), "-- Alice"), date(2026, 1, 15))
    second = SignatureDecorator(DateDecorator(Message("hello"), date(2026, 1, 15)), "-- Alice")

    assert first.render() == "hello\n-- Alice\n2026-01-15"
    assert second.render() == "hello\n2026-01-15\n-- Alice"
