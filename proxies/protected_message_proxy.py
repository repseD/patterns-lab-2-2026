from interfaces import BaseMessage
from security import AccessPolicy, UserContext


class ProtectedMessageProxy(BaseMessage):
    def __init__(
        self,
        message: BaseMessage,
        user: UserContext,
        policy: AccessPolicy,
    ) -> None:
        self._message = message
        self._user = user
        self._policy = policy

    def render(self) -> str:
        if not self._policy.is_allowed(self._user):
            raise PermissionError(
                f"Пользователь {self._user.username} не имеет доступа к сообщению"
            )
        return self._message.render()
