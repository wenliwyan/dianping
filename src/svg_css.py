import logging
import os
import re

import requests

from src.svg_text import SvgText


class SvgCss:
    """
    Parser for .css file, which maps class name to background-image pixels, and
    to text subsequently
    """
    def __init__(self, css_url):
        logging.debug(f'Start parsing css file '
                      f'"{os.path.basename(css_url)}" >>>')
        self.css_text = requests.get(css_url).text

        """example: svgmtsi[class^="scb"]{width: 14px;height: 
        30px;margin-top: -9px;background-image: url( 
        //s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91 
        /svgtextcss/898cb2da6db2b098f9980d7d65d5e7a4.svg);background-repeat: 
        no-repeat;display: inline-block;vertical-align: middle;}
        """
        svg_file_pattern = (
            r'svgmtsi\[class\^="(.*?)"].*?background-image: url\((.*?)\)')
        matched = re.search(svg_file_pattern, self.css_text)

        class_prefix = matched.group(1)
        logging.debug(f'svgmtsi class prefix: {class_prefix}')

        svg_url = 'http:' + matched.group(2)
        logging.debug(f'Found dependant svg link: {svg_url}')
        svg_text = SvgText(svg_url)

        # example:          .scbifa{background:-224.0px -314.0px;}
        class_pattern = (r'\.(%s\w+){background:-(\d+)\.0px -(\d+)\.0px;}' %
                         class_prefix)
        self.class_to_text = {}
        for class_name, x, y in re.findall(class_pattern, self.css_text):
            text = svg_text.get_text(int(x), int(y))
            self.class_to_text[class_name] = text

    def get_text(self, class_name):
        return self.class_to_text[class_name]
