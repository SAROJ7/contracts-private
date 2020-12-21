from ..sicx import sICX
from tbears.libs.scoretest.score_test_case import ScoreTestCase


class TestsICX(ScoreTestCase):

    def setUp(self):
        super().setUp()
        self.score = self.get_score_instance(sICX, self.test_account1)

    def test_hello(self):
        self.assertEqual(self.score.hello(), "Hello")
