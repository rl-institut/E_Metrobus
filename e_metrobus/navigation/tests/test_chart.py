
from django.test import TestCase, tag
from e_metrobus.navigation.chart import get_rounding


@tag("chart")
class ChartTestCase(TestCase):
    def test_rounding(self):
        self.assertEqual(get_rounding(10.4), 0)

        self.assertEqual(get_rounding(1.5), 1)
        self.assertEqual(get_rounding(0.5), 1)

        self.assertEqual(get_rounding(0.54), 2)
        self.assertEqual(get_rounding(0.522), 2)
        self.assertEqual(get_rounding(0.04), 2)
        self.assertEqual(get_rounding(0.003296), 4)
