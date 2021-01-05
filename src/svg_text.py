import logging
import os
import re
from bisect import bisect

import requests
from bs4 import BeautifulSoup


class SvgText:
    """
    Parser for .svg file, which maps pixel location (x, y) to text
    """
    def __init__(self, file_content):
        self.soup = BeautifulSoup(file_content, 'html.parser')
        self.font_size = int(re.search(
            r'font-size:(\d+)px', self.soup.style.next_element).group(1))

        if self.soup.defs:
            self.y_limit_to_text = self._parse_v1()
        else:
            self.y_limit_to_text = self._parse_v2()

        self.y_limits = sorted(self.y_limit_to_text)

    @classmethod
    def from_local_file(cls, filepath):
        logging.debug(f'Read local file: "{os.path.basename(filepath)}" >>>')
        with open(filepath) as f:
            return cls(f.read())

    @classmethod
    def from_web_url(cls, url):
        logging.debug(f'Request from web: "{os.path.basename(url)}" >>>')
        r = requests.get(url)
        return cls(r.text)

    def _parse_v1(self):
        # example: <defs><path id="1" d="M0 46 H600"/>...</defs>
        id_to_y_limit = {}
        for path in self.soup.defs.children:
            path_id = int(path['id'])
            y_limit = int(path['d'].split()[1])
            id_to_y_limit[path_id] = y_limit

        # example: <textPath xlink:href="#1" textLength="532">朽...</textPath>
        id_to_text = {}
        for text_path in self.soup.select('textPath'):
            path_id = int(text_path['xlink:href'][1:])
            text = text_path.text
            id_to_text[path_id] = text

        y_limit_to_text = {}
        for path_id in id_to_y_limit:
            y_limit = id_to_y_limit[path_id]
            text = id_to_text[path_id]
            y_limit_to_text[y_limit] = text

        return y_limit_to_text

    def _parse_v2(self):
        # example: <text x="0" y="44">续...</text>
        y_limit_to_text = {}
        for tag in self.soup.find_all('text'):
            y_limit = int(tag['y'])
            text = tag.text
            y_limit_to_text[y_limit] = text
        return y_limit_to_text

    def get_text(self, x, y):
        y_limit = self.y_limits[bisect(self.y_limits, y)]
        x_id = x // self.font_size
        return self.y_limit_to_text[y_limit][x_id]
