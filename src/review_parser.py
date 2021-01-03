import logging
import re

import requests
from bs4 import BeautifulSoup

from src.svg_css import SvgCss


class ReviewParser:
    def __init__(self):
        """example: <link rel="stylesheet" type="text/css" 
        href="//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91
        /svgtextcss/fbf48635df260f2a46cadd5a2d064522.css">
        """
        self.css_url_regex = re.compile('^//s3plus.meituan.net')
        self.parsed_css = {}

    def _extract(self, content_div, css_mapper):
        paragraph = ''

        for content in content_div.contents:
            if isinstance(content, str):
                # bs4.element.NavigableString
                text = str(content)
            elif content.name == 'svgmtsi':
                # svg class
                class_name = content['class'][0]
                text = css_mapper.get_text(class_name)
            else:
                # <img class="emoji-img" src="">文字</img>
                text = f'[{content["class"][0]} {content["src"]}]'
                if (len(content.contents) > 2 or
                        (len(content.contents) == 1 and
                         str(content.contents[0]).strip())):
                    logging.debug(f'Recursively parsing nested div: '
                                  f'{len(content.contents)} parts')
                    text += self._extract(content, css_mapper)
            paragraph += text

        return paragraph.strip()

    def extract_review(self, review_text):
        soup = BeautifulSoup(review_text, 'html.parser')

        css_tag = soup.find(href=self.css_url_regex)
        css_url = 'http:' + css_tag['href']

        logging.debug(f'Found dependant css link: {css_url}')
        if css_url not in self.parsed_css:
            self.parsed_css[css_url] = SvgCss(css_url)

        review_paragraph = self._extract(
            soup.select('.review-content .review-words')[0],
            self.parsed_css[css_url])

        return review_paragraph

    def request_and_extract(self, review_url, http_headers):
        r = requests.get(review_url, headers=http_headers)
        if r.status_code != 200:
            logging.warning(f'{r.status_code} {r.reason}')
        return self.extract_review(r.text)


if __name__ == '__main__':
    from glob import glob

    logging.basicConfig(level=logging.DEBUG)
    review_parser = ReviewParser()

    for filepath in glob('data/review_*.html'):
        logging.info(f'Start processing review page "{filepath}" ...')
        with open(filepath) as f:
            html_text = f.read()
            review_result = review_parser.extract_review(html_text)
            logging.info(f'Parsed result: \n{review_result}\n{"=" * 10}')
