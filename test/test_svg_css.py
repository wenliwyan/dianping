from unittest import TestCase

from src.svg_css import SvgCss


class TestSvgCss(TestCase):
    def test_get_text(self):
        css_url = 'http://s3plus.meituan.net/v1' \
                  '/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss' \
                  '/fbf48635df260f2a46cadd5a2d064522.css '
        svg_css = SvgCss(css_url)
        self.assertEqual('的', svg_css.get_text('scbifa'))
