from decorators import (
    Base64Decorator,
    DateDecorator,
    HeaderDecorator,
    SignatureDecorator,
)
from messages import Message
from proxies import ProtectedMessageProxy
from security import AccessPolicy, UserContext


def main() -> None:
    message = Message("С Днём Рождения!")

    decorated = SignatureDecorator(
        DateDecorator(HeaderDecorator(message, "Поздравление")),
        "-- Алиса",
    )

    print("Цепочка декораторов:")
    print(decorated.render())

    print("\nТа же цепочка в Base64:")
    print(Base64Decorator(decorated).render())

    policy = AccessPolicy("reader")
    allowed_user = UserContext.of("alice", "reader")
    denied_user = UserContext.of("bob", "guest")

    print("\nДоступ разрешён:")
    print(ProtectedMessageProxy(decorated, allowed_user, policy).render())

    print("\nДоступ запрещён:")
    try:
        ProtectedMessageProxy(decorated, denied_user, policy).render()
    except PermissionError as error:
        print(error)


if __name__ == "__main__":
    main()
