"""
Utils for dealing with arxiv API and related processing
"""

import time
import logging
import urllib.request
import feedparser
from collections import OrderedDict

logger = logging.getLogger(__name__)

def get_response(search_query=None, start_index=0, id_list=None):
    """ pings arxiv.org API to fetch papers by query or by list of IDs """
    base_url = 'http://export.arxiv.org/api/query?'

    if id_list is not None:
        # id_list can be a string or list of strings
        if isinstance(id_list, list):
            id_list = ','.join(id_list)
        url_str = f"{base_url}id_list={id_list}"
    elif search_query is not None:
        url_str = f"{base_url}search_query={search_query}&sortBy=lastUpdatedDate&start={start_index}&max_results=100"
    else:
        raise ValueError("Must provide either search_query or id_list")

    logger.debug(f"Searching arxiv for {url_str}")
    with urllib.request.urlopen(url_str) as url:
        response = url.read()

    if url.status != 200:
        logger.error(f"arxiv did not return status 200 response")
    return response

def encode_feedparser_dict(d):
    """ helper function to strip feedparser objects using a deep copy """
    if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
        return {k: encode_feedparser_dict(d[k]) for k in d.keys()}
    elif isinstance(d, list):
        return [encode_feedparser_dict(k) for k in d]
    else:
        return d

def parse_arxiv_url(url):
    """
    examples is http://arxiv.org/abs/1512.08756v2
    we want to extract the raw id (1512.08756) and the version (2)
    """
    ix = url.rfind('/')
    assert ix >= 0, 'bad url: ' + url
    idv = url[ix+1:] # extract just the id (and the version)
    parts = idv.split('v')
    assert len(parts) == 2, 'error splitting id and version in idv string: ' + idv
    return idv, parts[0], int(parts[1])

def parse_response(response):

    out = []
    parse = feedparser.parse(response)
    for e in parse.entries:
        j = encode_feedparser_dict(e)
        # extract / parse id information
        idv, rawid, version = parse_arxiv_url(j['id'])
        j['_idv']= idv
        j['_id'] = rawid
        j['_version'] = version
        j['_time'] = time.mktime(j['updated_parsed'])
        j['_time_str'] = time.strftime('%b %d %Y', j['updated_parsed'])
        # delete apparently spurious and redundant information
        del j['summary_detail']
        del j['title_detail']
        out.append(j)

    return out

def filter_latest_version(idvs):
    """
    for each idv filter the list down to only the most recent version
    """

    pid_to_v = OrderedDict()
    for idv in idvs:
        pid, v = idv.split('v')
        pid_to_v[pid] = max(int(v), pid_to_v.get(pid, 0))

    filt = [f"{pid}v{v}" for pid, v in pid_to_v.items()]
    return filt
