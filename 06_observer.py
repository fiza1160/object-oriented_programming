from abc import ABC, abstractmethod
import unittest


class Engine(ABC):
    pass


class ObservableEngine(Engine):
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)

    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass


class ShortNotificationPrinter (AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, message):
        self.achievements.add(message['title'])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, message):
        if message not in self.achievements:
            self.achievements.append(message)


class Tests(unittest.TestCase):

    def setUp(self):
        self.short_notifier = ShortNotificationPrinter()
        self.full_notifier = FullNotificationPrinter()

        self.manager = ObservableEngine()
        self.manager.subscribe(self.short_notifier)
        self.manager.subscribe(self.full_notifier)

    def test_one_message(self):
        self.manager.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})

        self.assertEqual(self.short_notifier.achievements,
                         {
                             "Покоритель"
                         }
                         )
        self.assertEqual(self.full_notifier.achievements,
                         [
                             {"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}
                         ]
                         )

    def test_many_message(self):
        self.manager.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
        self.manager.notify({"title": "Ктулху-фхтагн", "text": "Дается при пробуждении Ктулху"})
        self.manager.notify({"title": "Азаза", "text": "Дается когда лень писать"})

        self.assertEqual(self.short_notifier.achievements,
                         {
                             "Покоритель",
                             "Ктулху-фхтагн",
                             "Азаза"
                          }
                         )
        self.assertEqual(self.full_notifier.achievements,
                         [
                             {"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"},
                             {"title": "Ктулху-фхтагн", "text": "Дается при пробуждении Ктулху"},
                             {"title": "Азаза", "text": "Дается когда лень писать"}
                         ]
                         )

    def test_duplicate_message(self):
        self.manager.notify({"title": "Азаза", "text": "Дается когда лень писать"})
        self.manager.notify({"title": "Ктулху-фхтагн", "text": "Дается при пробуждении Ктулху"})
        self.manager.notify({"title": "Азаза", "text": "Дается когда лень писать"})

        self.assertEqual(self.short_notifier.achievements,
                         {
                             "Ктулху-фхтагн",
                             "Азаза"
                         }
                         )
        self.assertEqual(self.full_notifier.achievements,
                         [
                             {"title": "Азаза", "text": "Дается когда лень писать"},
                             {"title": "Ктулху-фхтагн", "text": "Дается при пробуждении Ктулху"}
                         ]
                         )

    def test_delete_subscribe(self):
        self.manager.unsubscribe(self.short_notifier)
        self.manager.unsubscribe(self.full_notifier)

        self.assertEqual(self.manager._ObservableEngine__subscribers, set())


if __name__ == '__main__':
    unittest.main()
