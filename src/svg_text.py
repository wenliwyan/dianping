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
    def __init__(self, svg_url):
        logging.debug(f'Start parsing "{os.path.basename(svg_url)}" >>>')
        r = requests.get(svg_url)
        self.soup = BeautifulSoup(r.text, 'html.parser')
        self.font_size = int(re.search(
            r'font-size:(\d+)px', self.soup.style.next_element).group(1))

        id_to_y_limit = {}
        for path in self.soup.defs.children:
            path_id = int(path['id'])
            y_limit = int(path['d'].split()[1])
            id_to_y_limit[path_id] = y_limit

        id_to_text = {}
        for text_path in self.soup.select('text textPath'):
            path_id = int(text_path['xlink:href'][1:])
            text = text_path.text
            id_to_text[path_id] = text

        self.y_limits = sorted(id_to_y_limit.values())
        self.y_limit_to_text = {}
        for path_id in id_to_y_limit:
            y_limit = id_to_y_limit[path_id]
            text = id_to_text[path_id]
            self.y_limit_to_text[y_limit] = text

    def get_text(self, x, y):
        y_limit = self.y_limits[bisect(self.y_limits, y)]
        x_id = x // self.font_size
        return self.y_limit_to_text[y_limit][x_id]
