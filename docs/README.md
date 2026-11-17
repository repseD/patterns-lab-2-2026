# Структурная диаграмма

```mermaid
classDiagram
    class BaseMessage {
        <<interface>>
        +render() str
    }

    class Message {
        -_text: str
        +render() str
    }

    class MessageDecorator {
        #_message: BaseMessage
        +render() str
    }

    class HeaderDecorator {
        -_header: str
        +render() str
    }

    class SignatureDecorator {
        -_signature: str
        +render() str
    }

    class DateDecorator {
        -_date: date
        +render() str
    }

    class Base64Decorator {
        +render() str
    }

    class ProtectedMessageProxy {
        -_message: BaseMessage
        -_user: UserContext
        -_policy: AccessPolicy
        +render() str
    }

    class AccessPolicy {
        +is_allowed(user: UserContext) bool
    }

    class UserContext {
        +username: str
        +roles: frozenset
    }

    BaseMessage <.. Message
    BaseMessage <.. MessageDecorator
    BaseMessage <.. ProtectedMessageProxy

    MessageDecorator <-- HeaderDecorator
    MessageDecorator <-- SignatureDecorator
    MessageDecorator <-- DateDecorator
    MessageDecorator <-- Base64Decorator

    MessageDecorator o-- BaseMessage : wraps
    ProtectedMessageProxy o-- BaseMessage : real subject
    ProtectedMessageProxy --> AccessPolicy : uses
    AccessPolicy --> UserContext : checks
```




# Decorator и Proxy: сравнение

Критерий: Decorator / Proxy 
 Назначение:  Добавляет объекту новое поведение / Контролирует доступ к объекту 
 Содержание результата:  Изменяет результат render() / Возвращает результат без изменений 
 Количество обёрток:  Можно вкладывать друг в друга в любом порядке / Обычно один заместитель 
 Кто хранит ссылку:  Декоратор хранит декорируемый BaseMessage / Proxy хранит реальный субъект 
 Логика в проекте:  Формирование текста (заголовок, подпись, дата, Base64) / Проверка AccessPolicy перед вызовом 
 Результат при отказе:  Не применяется / PermissionError 

Итог: у Decorator и Proxy одинаковая структура (оба реализуют BaseMessage и хранят ссылку на другой объект), но разные задачи. Decorator расширяет поведение, а Proxy защищает доступ и не меняет содержимое сообщения.