import pytest

from decorators import HeaderDecorator
from messages import Message
from proxies import ProtectedMessageProxy
from security import AccessPolicy, UserContext


def test_proxy_allows_access() -> None:
    message = Message("hello")
    proxy = ProtectedMessageProxy(
        message,
        UserContext.of("alice", "reader"),
        AccessPolicy("reader"),
    )
    assert proxy.render() == "hello"


def test_proxy_denies_access() -> None:
    message = Message("hello")
    proxy = ProtectedMessageProxy(
        message,
        UserContext.of("bob", "guest"),
        AccessPolicy("reader"),
    )
    with pytest.raises(PermissionError):
        proxy.render()


def test_proxy_does_not_change_content() -> None:
    decorated = HeaderDecorator(Message("hello"), "Title")
    proxy = ProtectedMessageProxy(
        decorated,
        UserContext.of("alice", "reader"),
        AccessPolicy("reader"),
    )
    assert proxy.render() == decorated.render()
