import json
import logging
import re

import requests
from bs4 import BeautifulSoup

from src.review_parser import ReviewParser


class ReviewSummary:
    def __init__(self, headers):
        """ headers need to include User-Agent, Cookie, and etc. in order to
        access review contents, otherwise, the response would be 302 redirect,
         403 forbidden, or 200 but verification required.
        """
        self.headers = headers
        self.review_parser = ReviewParser()

    def get_all_review_urls(self, url):
        review_url_pattern = r'href="(http://www.dianping.com/review/\d+)"'
        all_review_urls = []
        cur_page_url = url

        while True:
            r = requests.get(cur_page_url, headers=self.headers)
            review_urls = re.findall(review_url_pattern, r.text)
            logging.info(f'Found {len(review_urls)} reviews >>>')
            all_review_urls.extend(review_urls)

            soup = BeautifulSoup(r.text, 'html.parser')
            divs = soup.select('.page-next')
            if not divs:
                break
            cur_page_url = url + divs[0]['href']
            logging.info('Go to next page ...')

        return all_review_urls

    def extract_all_reviews(self, url, write_to_file=True):
        all_reviews = {}

        for review_url in self.get_all_review_urls(url):
            logging.debug(f'Start processing review url {review_url} >>>')
            review_paragraph = self.review_parser.request_and_extract(
                review_url, http_headers)
            logging.info(f'Parsed result: \n{review_paragraph}\n{"=" * 10}')
            all_reviews[review_url] = review_paragraph

        if write_to_file:
            with open('data/all_reviews.json', 'w', encoding='utf8') as fp:
                json.dump(all_reviews, fp, indent=2, ensure_ascii=False)

        return all_reviews


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    http_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/14.0.2 Safari/605.1.15',
        'Referer': 'Referer: http://www.dianping.com/member/1209753740',
        'Cookie': '_lxsdk_s=176c6b45ea4-054-519-822%7C%7C49; '
                  'Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1609651897; '
                  'Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1609570843; '
                  '_lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; '
                  'cy=1; cye=shanghai; aburl=1; '
                  'dper=c3e04a8a5ba92acbb4a0492322f362f5164a94156e98901d4df2140386005fc79a620033a1bff2308ddf2da033728c387c9cda1bbd5af693245c2a886991a0679de5426983dde9b5527e660aef5bd090849ae51388ed6eb716d33fc30d365b1b; '
                  'dplet=79d3026b4b4516453ec1cf203d99b6da; '
                  'll=7fd06e815b796be3df069dec7836c3df; '
                  'ua=%E8%B5%84%E6%B7%B1%E5%9B%BD%E9%99%85%E5%90%83%E8%B4%A7; '
                  'SIGN="NzYzYTU4ZDExNzc4NmMxZDNhMDU0YjJmZDY1ZWRjN2I="; '
                  'currentTimestamp="MTYwOTU3Mjk2MTI4MQ=="; '
                  'redir="aHR0cHM6Ly93d3cuZGlhbnBpbmcuY29tL21lbWJlci8xMjA5NzUzNzQwL3Jldmlld3M="; '
                  'thirdtoken=cc55293a-9415-4b40-95a4-0d0717398ca1; '
                  '_dp.ac.v=5b3fce92-9137-4d6a-81bd-41e9f37da6fd; '
                  'ctu=02624345f19d5eba35c43facb51645d5762ecbc932d67b72b4ba2f0d8a3091df; '
                  'fspop=test; _hc.v=5301a11e-2c8a-6cc0-8358-72fabeb3687b.1609569836; '
                  '_lxsdk=176c1d69c627a-0580b311564d388-48193201-13c680-176c1d69c63c8; '
                  '_lxsdk_cuid=176c1d69c627a-0580b311564d388-48193201-13c680-176c1d69c63c8 '
    }
    summary = ReviewSummary(http_headers)
    summary.extract_all_reviews(
        'http://www.dianping.com/member/1209753740/reviews', )
