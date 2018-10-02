from __future__ import unicode_literals

import json

from .common import InfoExtractor
from ..utils import (
    int_or_none,
    parse_iso8601,
    unescapeHTML,
    sanitize_url,
    clean_html,
    get_element_by_attribute,
    js_to_json,
)


class VideofyMeIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.videofy\.me/.+?|p\.videofy\.me/v)/(?P<id>\d+)(&|#|$)'
    IE_NAME = 'videofy.me'

    _TESTS = [{
        'url': 'https://www.videofy.me/v/24582',
        'md5': '1e46140bacdae8959827903cecd054d9',
        'info_dict': {
            'id': '24582',
            'ext': 'mp4',
            'title': 'The VideofyMe app demo!',
            'description': 'This is VideofyMe.',
            'upload_date': '20120607',
            'timestamp': 1339070671,
            'uploader': 'oskarglauser',
            'uploader_id': 7010,
            'view_count': int,
        },
    }, {
    	'url': 'https://www.videofy.me/v/2975905',
        'md5': '79ad4498ab14dec72e815a8f85c7641c',
        'info_dict': {
            'id': '2975905',
            'ext': 'mp4',
            'title': 'But',
            'description': '',
            'upload_date': '20180126',
            'timestamp': 1516931131,
            'uploader': 'iamatlien',
            'uploader_id': 1798214,
            'view_count': int,
        },
    },]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        page = self._download_webpage(url, video_id)

        video_info = json.loads(get_element_by_attribute('type', 'application/ld+json', page))

        meta = self._download_json('https://www.videofy.me/wp-json/wp/v2/posts/%s' % video_id, video_id)
        uploader_id = meta.get('author')
        uploader_name = self._download_json('https://www.videofy.me/wp-json/wp/v2/users/%s' % uploader_id, uploader_id, fatal=False).get('name')   

        return {
            'id': video_id,
            'title': video_info['name'],
            'url': video_info['contentUrl'],
            'thumbnail': video_info.get('thumbnailUrl'),
            'description': clean_html(video_info.get('description')),
            'timestamp': parse_iso8601(video_info.get('uploadDate')),
            'uploader_id': uploader_id,
            'uploader': uploader_name,
            'view_count': int_or_none(video_info.get('interactionCount')),
        }
