#!/usr/bin/env python2.7
"""
Generates the list for http://meta.stackexchange.com/a/224922
"""

import ConfigParser
import collections
import os.path
import sys
import urllib


def main(own_path):
    own_dir = os.path.dirname(own_path)
    
    config = ConfigParser.RawConfigParser()
    with open(os.path.join(own_dir, 'torrents.config'), 'rt') as f:
        config.readfp(f)

    torrent_btihs = config.sections()
    for torrent_btih in torrent_btihs:
        torrent_info = {
            option: config.get(torrent_btih, option)
            for option in config.options(torrent_btih)
        }

        comments = [
            line.strip() for line
            in torrent_info.get('comments', '').split('\n')
            if line.strip()]

        name = torrent_info['name']

        year_month, _, rest = (name
            .replace(' Stack Exchange Data Dump', '')
            .partition(' '))
        year, month_precise = year_month.split('-')

        month_friendly = {
            '01Jan': 'January',
            '02Feb': 'February',
            '03Mar': 'March',
            '04Apr': 'April',
            '05May': 'May',
            '06Jun': 'June',
            '07Jul': 'July',
            '08Aug': 'August',
            '09Sep': 'September',
            '10Oct': 'October',
            '11Nov': 'November',
            '12Dec': 'December',
        }[month_precise]

        post_name = month_friendly + ' ' + year
        if rest:
            post_name += ' ' + rest

        if comments:
            annotation = ' (' + '; '.join(comments) + ')'
        else:
            annotation = ''

        link = (
            'http://mgnt.ca/#' +
            'magnet:?' +
            'xt=urn:btih:' + torrent_btih +
            '&dn=' + urllib.quote_plus(name) +
            '&tr=udp://tracker.openbittorrent.com:80' + 
            '&tr=udp://tracker.publicbt.com:80')

        print (
            '<sub><sup>`{btih}`</sup></sub> [{name}]({link}){annotation}  '
        ).format(
            btih=torrent_btih,
            name=post_name,
            link=link,
            annotation=annotation
        )



if __name__ == '__main__':
    sys.exit(main(*sys.argv))
