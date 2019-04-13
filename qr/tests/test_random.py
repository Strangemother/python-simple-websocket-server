import unittest
import rand

class TestRandom(unittest.TestCase):

    def test_gen_16(self):

        res = rand.gen_16()
        assert len(res) == 16
        assert rand.gen_16() != rand.gen_16()

    def test_rand_str(self):

        res1 = rand.rand_str()
        assert len(res1) == 10

        res2 = rand.rand_str(20)
        assert len(res2) == 20

        res3 = rand.rand_str()

        assert len(set([res1, res2, res3])) == 3
