import pickle

import redis

__author__ = 'mtianyan'
__date__ = '2018/8/20 08:05'

import re
import hashlib

redis_cli = redis.StrictRedis()


def get_md5(url):

    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):

    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def extract_num_include_dot(text):

    text_num = text.replace(',', '')
    try:
        nums = int(text_num)
    except:
        nums = -1
    return nums


def real_time_count(key, init):
    if redis_cli.get(key):
        count = pickle.loads(redis_cli.get(key))
        count = count + 1
        count = pickle.dumps(count)
        redis_cli.set(key, count)
    else:
        count = pickle.dumps(init)
        redis_cli.set(key, count)


if __name__ == "__main__":
    print(get_md5("http://cec.jmu.edu.cn/".encode("utf-8")))
