import unittest


class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, type):
        self.type = type


class EventSet:
    def __init__(self, value):
        self.value = value


class NullHandler:
    def __init__(self, successor=None):
        self. __successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if self.event_is_correct_type(event):
            res = self.handle_event(obj, event)
            return res
        else:
            return super().handle(obj, event)

    @staticmethod
    def event_is_correct_type(event):
        if isinstance(event, EventSet):
            if isinstance(event.value, int):
                return True
        elif isinstance(event, EventGet):
            if event.type == int:
                return True
        else:
            raise TypeError

        return False

    @staticmethod
    def handle_event(obj, event):
        if isinstance(event, EventSet):
            obj.integer_field = event.value
            return obj.integer_field
        if isinstance(event, EventGet):
            return obj.integer_field
        else:
            raise ValueError


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if self.event_is_correct_type(event):
            res = self.handle_event(obj, event)
            return res
        else:
            return super().handle(obj, event)

    @staticmethod
    def event_is_correct_type(event):
        if isinstance(event, EventSet):
            if isinstance(event.value, float):
                return True
        elif isinstance(event, EventGet):
            if event.type == float:
                return True
        else:
            raise TypeError

        return False

    @staticmethod
    def handle_event(obj, event):
        if isinstance(event, EventSet):
            obj.float_field = event.value
            return obj.float_field
        if isinstance(event, EventGet):
            return obj.float_field
        else:
            raise ValueError


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if self.event_is_correct_type(event):
            res = self.handle_event(obj, event)
            return res
        else:
            return super().handle(obj, event)

    @staticmethod
    def event_is_correct_type(event):
        if isinstance(event, EventSet):
            if isinstance(event.value, str):
                return True
        elif isinstance(event, EventGet):
            if event.type == str:
                return True
        else:
            raise TypeError

        return False

    @staticmethod
    def handle_event(obj, event):
        if isinstance(event, EventSet):
            obj.string_field = event.value
            return obj.string_field
        if isinstance(event, EventGet):
            return obj.string_field
        else:
            raise ValueError


class Chain:
    def __init__(self):
        self.handlers = IntHandler(FloatHandler(StrHandler(NullHandler())))

    def handle(self, obj, event):
        return self.handlers.handle(obj, event)


class Tests(unittest.TestCase):

    def test_get_after_init(self):
        obj = SomeObject()
        with self.subTest(case="get int after init"):
            self.assertEqual(Chain().handle(obj, EventGet(int)), 0)

        with self.subTest(case="get str after init"):
            self.assertEqual(Chain().handle(obj, EventGet(str)), "")

        with self.subTest(case="get float after init"):
            self.assertEqual(Chain().handle(obj, EventGet(float)), 0.0)

        with self.subTest(case="event type must be EventGet or EventSet"):
            self.assertRaises(
                TypeError,
                Chain().handle,
                obj,
                None
            )

            self.assertRaises(
                TypeError,
                Chain().handle,
                obj,
                []
            )

            self.assertRaises(
                TypeError,
                Chain().handle,
                obj,
                "None"
            )

    def test_set(self):
        with self.subTest(case="set int"):
            obj = SomeObject()
            self.assertEqual(Chain().handle(obj, EventSet(1)), 1)

        with self.subTest(case="set str"):
            obj = SomeObject()
            self.assertEqual(Chain().handle(obj, EventSet("str")), "str")

        with self.subTest(case="set float"):
            obj = SomeObject()
            self.assertEqual(Chain().handle(obj, EventSet(1.1)), 1.1)

        with self.subTest(case="event type must be EventGet or EventSet"):
            self.assertRaises(
                TypeError,
                Chain().handle,
                obj,
                None
            )

            self.assertRaises(
                TypeError,
                Chain().handle,
                obj,
                []
            )

            self.assertRaises(
                TypeError,
                Chain().handle,
                obj,
                "None"
            )

    def test_get_after_set(self):
        with self.subTest(case="get int after set int"):
            obj = SomeObject()
            self.assertEqual(Chain().handle(obj, EventSet(18)), 18)
            self.assertEqual(Chain().handle(obj, EventGet(int)), 18)

        with self.subTest(case="get str after set str"):
            obj = SomeObject()
            self.assertEqual(Chain().handle(obj, EventSet("azaza")), "azaza")
            self.assertEqual(Chain().handle(obj, EventGet(str)), "azaza")

        with self.subTest(case="get float after set float"):
            obj = SomeObject()
            self.assertEqual(Chain().handle(obj, EventSet(12.7)), 12.7)
            self.assertEqual(Chain().handle(obj, EventGet(float)), 12.7)


class TestCheckEventsType(unittest.TestCase):

    def setUp(self):
        self.get_int = EventGet(int)
        self.get_str = EventGet(str)
        self.get_float = EventGet(float)

        self.set_int = EventSet(18)
        self.set_str = EventSet("kurly")
        self.set_float = EventSet(13.777)

    def test_check_event_type_int_handler(self):
        int_handler = IntHandler()
        with self.subTest(case='if type(event) is EventGet and event.type is int expected True'):
            self.assertEqual(
                int_handler.event_is_correct_type(self.get_int),
                True
            )

        with self.subTest(case='if type(event) is EventGet and event.type is str expected False'):
            self.assertEqual(
                int_handler.event_is_correct_type(self.get_str),
                False
            )

        with self.subTest(case='if type(event) is EventGet and event.type is float expected False'):
            self.assertEqual(
                int_handler.event_is_correct_type(self.get_float),
                False
            )

        with self.subTest(case='if type(event) is EventSet and event.type is int expected True'):
            self.assertEqual(
                int_handler.event_is_correct_type(self.set_int),
                True
            )

        with self.subTest(case='if type(event) is EventSet and event.type is str expected False'):
            self.assertEqual(
                int_handler.event_is_correct_type(self.set_str),
                False
            )

        with self.subTest(case='if type(event) is EventSet and event.type is float expected False'):
            self.assertEqual(
                int_handler.event_is_correct_type(self.set_float),
                False
            )

        with self.subTest(case='event type must be EventGet or EventSet'):
            self.assertRaises(
                TypeError,
                int_handler.event_is_correct_type,
                None
            )
            self.assertRaises(
                TypeError,
                int_handler.event_is_correct_type,
                'str'
            )
            self.assertRaises(
                TypeError,
                int_handler.event_is_correct_type,
                1111
            )

    def test_check_event_type_str_handler(self):
        str_handler = StrHandler()
        with self.subTest(case='if type(event) is EventGet and event.type is int expected False'):
            self.assertEqual(
                str_handler.event_is_correct_type(self.get_int),
                False
            )

        with self.subTest(case='if type(event) is EventGet and event.type is str expected True'):
            self.assertEqual(
                str_handler.event_is_correct_type(self.get_str),
                True
            )

        with self.subTest(case='if type(event) is EventGet and event.type is float expected False'):
            self.assertEqual(
                str_handler.event_is_correct_type(self.get_float),
                False
            )

        with self.subTest(case='if type(event) is EventSet and event.type is int expected False'):
            self.assertEqual(
                str_handler.event_is_correct_type(self.set_int),
                False
            )

        with self.subTest(case='if type(event) is EventSet and event.type is str expected True'):
            self.assertEqual(
                str_handler.event_is_correct_type(self.set_str),
                True
            )

        with self.subTest(case='if type(event) is EventSet and event.type is float expected False'):
            self.assertEqual(
                str_handler.event_is_correct_type(self.set_float),
                False
            )

        with self.subTest(case='event type must be EventGet or EventSet'):
            self.assertRaises(
                TypeError,
                str_handler.event_is_correct_type,
                None
            )

            self.assertRaises(
                TypeError,
                str_handler.event_is_correct_type,
                'str'
            )
            self.assertRaises(
                TypeError,
                str_handler.event_is_correct_type,
                1111
            )

    def test_check_event_type_float_handler(self):
        float_handler = FloatHandler()
        with self.subTest(case='if type(event) is EventGet and event.type is int expected False'):
            self.assertEqual(
                float_handler.event_is_correct_type(self.get_int),
                False
            )

        with self.subTest(case='if type(event) is EventGet and event.type is str expected False'):
            self.assertEqual(
                float_handler.event_is_correct_type(self.get_str),
                False
            )

        with self.subTest(case='if type(event) is EventGet and event.type is float expected True'):
            self.assertEqual(
                float_handler.event_is_correct_type(self.get_float),
                True
            )

        with self.subTest(case='if type(event) is EventSet and event.type is int expected False'):
            self.assertEqual(
                float_handler.event_is_correct_type(self.set_int),
                False
            )

        with self.subTest(case='if type(event) is EventSet and event.type is str expected False'):
            self.assertEqual(
                float_handler.event_is_correct_type(self.set_str),
                False
            )

        with self.subTest(case='if type(event) is EventSet and event.type is float expected True'):
            self.assertEqual(
                float_handler.event_is_correct_type(self.set_float),
                True
            )

        with self.subTest(case='event type must be EventGet or EventSet'):
            self.assertRaises(
                TypeError,
                float_handler.event_is_correct_type,
                None
            )

            self.assertRaises(
                TypeError,
                float_handler.event_is_correct_type,
                'str'
            )
            self.assertRaises(
                TypeError,
                float_handler.event_is_correct_type,
                1111
            )
