from unittest import TestCase

from src.svg_text import SvgText


class TestSvgText(TestCase):
    def test_get_char(self):
        svg_url = 'http://s3plus.meituan.net/v1' \
                  '/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss' \
                  '/898cb2da6db2b098f9980d7d65d5e7a4.svg'
        svg_text = SvgText(svg_url)
        self.assertEqual('的', svg_text.get_text(224, 314))
