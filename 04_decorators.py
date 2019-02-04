from abc import ABC
import unittest


class Hero(ABC):
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        effects = []
        now_effect = self
        while type(now_effect) != Hero:
            if str(now_effect) in ['Berserk', 'Blessing']:
                effects.append(str(now_effect))
            now_effect = now_effect.base
        effects.reverse()
        return effects

    def get_negative_effects(self):
        effects = []
        now_effect = self
        while type(now_effect) != Hero:
            if str(now_effect) in ['Weakness', 'EvilEye', 'Curse']:
                effects.append(str(now_effect))
            now_effect = now_effect.base
        effects.reverse()
        return effects

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

        self.stats = base.stats
        self.positive_effects = base.positive_effects
        self.negative_effects = base.negative_effects

    def get_stats(self):
        stats = self.stats.copy()
        all_effects = self.get_positive_effects() + self.get_negative_effects()
        count_effects = {}

        for effect in all_effects:
            if effect not in count_effects:
                count_effects[effect] = 0
            count_effects[effect] += 1

        for effect, count in count_effects.items():
            if effect == 'Berserk':
                stats = Berserk.apply_effect(stats, count)
            if effect == 'Blessing':
                stats = Blessing.apply_effect(stats, count)
            if effect == 'Weakness':
                stats = Weakness.apply_effect(stats, count)
            if effect == 'EvilEye':
                stats = EvilEye.apply_effect(stats, count)
            if effect == 'Curse':
                stats = Curse.apply_effect(stats, count)

        return stats


class AbstractPositive(AbstractEffect):
    def __init__(self, base):
        super().__init__(base)


class AbstractNegative(AbstractEffect):
    def __init__(self, base):
        super().__init__(base)


class Berserk(AbstractPositive):

    def __str__(self):
        return 'Berserk'

    @staticmethod
    def apply_effect(stats, multiplier):
        stats['HP'] += (50 * multiplier)

        stats['Strength'] += (7 * multiplier)
        stats['Endurance'] += (7 * multiplier)
        stats['Agility'] += (7 * multiplier)
        stats['Luck'] += (7 * multiplier)

        stats['Perception'] -= (3 * multiplier)
        stats['Charisma'] -= (3 * multiplier)
        stats['Intelligence'] -= (3 * multiplier)

        return stats


class Blessing(AbstractPositive):
    def __str__(self):
        return 'Blessing'

    @staticmethod
    def apply_effect(stats, multiplier):

        stats['Strength'] += (2 * multiplier)
        stats['Endurance'] += (2 * multiplier)
        stats['Agility'] += (2 * multiplier)
        stats['Luck'] += (2 * multiplier)
        stats['Perception'] += (2 * multiplier)
        stats['Charisma'] += (2 * multiplier)
        stats['Intelligence'] += (2 * multiplier)

        return stats


class Weakness(AbstractNegative):
    def __str__(self):
        return 'Weakness'

    @staticmethod
    def apply_effect(stats, multiplier):

        stats['Strength'] -= (4 * multiplier)
        stats['Endurance'] -= (4 * multiplier)
        stats['Agility'] -= (4 * multiplier)

        return stats


class EvilEye(AbstractNegative):
    def __str__(self):
        return 'EvilEye'

    @staticmethod
    def apply_effect(stats, multiplier):
        stats['Luck'] -= (10 * multiplier)

        return stats


class Curse(AbstractNegative):
    def __str__(self):
        return 'Curse'

    @staticmethod
    def apply_effect(stats, multiplier):
        stats['Strength'] -= (2 * multiplier)
        stats['Endurance'] -= (2 * multiplier)
        stats['Agility'] -= (2 * multiplier)
        stats['Luck'] -= (2 * multiplier)
        stats['Perception'] -= (2 * multiplier)
        stats['Charisma'] -= (2 * multiplier)
        stats['Intelligence'] -= (2 * multiplier)

        return stats


class MyTest(unittest.TestCase):
    def test_berserk(self):
        hero = Hero()
        hero_with_effect = Berserk(hero)
        stats_with_effect = hero_with_effect.get_stats()
        expected_stats = {
            "HP": 178,
            "MP": 42,
            "SP": 100,
            "Strength": 22,
            "Perception": 1,
            "Endurance": 15,
            "Charisma": -1,
            "Intelligence": 0,
            "Agility": 15,
            "Luck": 8
        }
        self.assertEqual(stats_with_effect, expected_stats)

    def test_blessing(self):
        hero = Hero()
        hero_with_effect = Blessing(hero)
        stats_with_effect = hero_with_effect.get_stats()
        expected_stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,
            "Strength": 17,
            "Perception": 6,
            "Endurance": 10,
            "Charisma": 4,
            "Intelligence": 5,
            "Agility": 10,
            "Luck": 3
        }
        self.assertEqual(stats_with_effect, expected_stats)

    def test_weakness(self):
        hero = Hero()
        hero_with_effect = Weakness(hero)
        stats_with_effect = hero_with_effect.get_stats()
        expected_stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,
            "Strength": 11,
            "Perception": 4,
            "Endurance": 4,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 4,
            "Luck": 1
        }
        self.assertEqual(stats_with_effect, expected_stats)

    def test_evileye(self):
        hero = Hero()
        hero_with_effect = EvilEye(hero)
        stats_with_effect = hero_with_effect.get_stats()
        expected_stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,
            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": -9
        }
        self.assertEqual(stats_with_effect, expected_stats)

    def test_curse(self):
        hero = Hero()
        hero_with_effect = Curse(hero)
        stats_with_effect = hero_with_effect.get_stats()
        expected_stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,
            "Strength": 13,
            "Perception": 2,
            "Endurance": 6,
            "Charisma": 0,
            "Intelligence": 1,
            "Agility": 6,
            "Luck": -1
        }
        self.assertEqual(stats_with_effect, expected_stats)

    def test_three_berserk(self):
        hero = Hero()
        hero_with_effect_1 = Berserk(hero)
        hero_with_effect_2 = Berserk(hero_with_effect_1)
        hero_with_effect_3 = Berserk(hero_with_effect_2)
        stats_with_effect = hero_with_effect_3.get_stats()
        expected_stats = {
            "HP": 278,
            "MP": 42,
            "SP": 100,
            "Strength": 36,
            "Perception": -5,
            "Endurance": 29,
            "Charisma": -7,
            "Intelligence": -6,
            "Agility": 29,
            "Luck": 22
        }
        self.assertEqual(stats_with_effect, expected_stats)

    def test_three_blessing(self):
        hero = Hero()
        hero_with_effect_1 = Blessing(hero)
        hero_with_effect_2 = Blessing(hero_with_effect_1)
        hero_with_effect_3 = Blessing(hero_with_effect_2)
        stats_with_effect = hero_with_effect_3.get_stats()
        expected_stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,
            "Strength": 21,
            "Perception": 10,
            "Endurance": 14,
            "Charisma": 8,
            "Intelligence": 9,
            "Agility": 14,
            "Luck": 7
        }
        self.assertEqual(stats_with_effect, expected_stats)

    def test_different_effects(self):
        hero = Hero()
        hero_with_effect_1 = Berserk(hero)
        hero_with_effect_2 = Blessing(hero_with_effect_1)
        hero_with_effect_3 = EvilEye(hero_with_effect_2)
        stats_with_effect = hero_with_effect_3.get_stats()
        expected_stats = {
            "HP": 178,
            "MP": 42,
            "SP": 100,
            "Strength": 24,
            "Perception": 3,
            "Endurance": 17,
            "Charisma": 1,
            "Intelligence": 2,
            "Agility": 17,
            "Luck": 0
        }
        self.assertEqual(stats_with_effect, expected_stats)

    def test_berserk_blessing(self):
        hero = Hero()
        hero = Berserk(hero)
        hero = Blessing(hero)
        hero = Berserk(hero)
        hero = Blessing(hero)
        stats = hero.get_stats()
        expected_stats = {
            "HP": 228,
            "MP": 42,
            "SP": 100,
            "Strength": 33,
            "Perception": 2,
            "Endurance": 26,
            "Charisma": 0,
            "Intelligence": 1,
            "Agility": 26,
            "Luck": 19
        }
        self.assertEqual(stats, expected_stats)

    def test_get_positive_effects(self):
        hero = Hero()
        hero_with_effect_1 = Berserk(hero)
        hero_with_effect_2 = Blessing(hero_with_effect_1)
        hero_with_effect_3 = EvilEye(hero_with_effect_2)
        hero_with_effect_4 = Weakness(hero_with_effect_3)
        hero_with_effect_5 = Curse(hero_with_effect_4)

        positive_effects = hero_with_effect_5.get_positive_effects()
        expected_effects = ['Berserk', 'Blessing']
        self.assertEqual(positive_effects, expected_effects)

    def test_get_negative_effects(self):
        hero = Hero()
        hero_with_effect_1 = Berserk(hero)
        hero_with_effect_2 = Blessing(hero_with_effect_1)
        hero_with_effect_3 = EvilEye(hero_with_effect_2)
        hero_with_effect_4 = Weakness(hero_with_effect_3)
        hero_with_effect_5 = Curse(hero_with_effect_4)

        negative_effects = hero_with_effect_5.get_negative_effects()
        expected_effects = ['EvilEye', 'Weakness', 'Curse']
        self.assertEqual(negative_effects, expected_effects)

    def test_remove_effects(self):
        hero = Hero()
        hero_with_effect_1 = EvilEye(hero)
        hero_with_effect_2 = Weakness(hero_with_effect_1)
        hero_with_effect_3 = Curse(hero_with_effect_2)

        hero_with_effect_3.base = hero_with_effect_3.base.base
        negative_effects = hero_with_effect_3.get_negative_effects()
        expected_effects = ['EvilEye', 'Curse']
        self.assertEqual(negative_effects, expected_effects)

    def test_remove_all_effects(self):
        hero = Hero()
        hero = Berserk(hero)
        hero = Blessing(hero)
        hero = EvilEye(hero)
        hero = Weakness(hero)
        hero = Curse(hero)

        while type(hero) != Hero:
            hero = hero.base

        stats = hero.get_stats()
        expected_stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,
            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }
        self.assertEqual(stats, expected_stats)


if __name__ == '__main__':
    unittest.main()
