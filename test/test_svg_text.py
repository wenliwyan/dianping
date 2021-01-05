from unittest import TestCase

from src.svg_text import SvgText


class TestSvgText(TestCase):
    def test_from_local_file(self):
        svg_text = SvgText.from_local_file(
            'data/898cb2da6db2b098f9980d7d65d5e7a4.svg')
        self.assertEqual(14, svg_text.font_size)

    def test_from_web_url(self):
        svg_url = 'http://s3plus.meituan.net/v1' \
                  '/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss' \
                  '/898cb2da6db2b098f9980d7d65d5e7a4.svg'
        svg_text = SvgText.from_web_url(svg_url)
        self.assertEqual(14, svg_text.font_size)

    def test_parse_v1(self):
        svg_text = SvgText.from_local_file(
            'data/898cb2da6db2b098f9980d7d65d5e7a4.svg')
        self.assertEqual(80, len(svg_text.y_limits))

    def test_parse_v2(self):
        svg_text = SvgText.from_local_file(
            'data/e313e383a6965b5461fccef15b5796ea.svg')
        self.assertEqual(60, len(svg_text.y_limits))

    def test_get_text(self):
        svg_url = 'http://s3plus.meituan.net/v1' \
                  '/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss' \
                  '/898cb2da6db2b098f9980d7d65d5e7a4.svg'
        svg_text = SvgText.from_web_url(svg_url)
        self.assertEqual('的', svg_text.get_text(224, 314))
