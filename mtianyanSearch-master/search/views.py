import pickle
from django.shortcuts import render
import json

from django.utils.datastructures import OrderedSet
from django.views.generic.base import View
from django.http import HttpResponse
from datetime import datetime
import redis
from elasticsearch import Elasticsearch
from django.views.generic.base import RedirectView
from search.models import ITIndex,artIndex,cjIndex,foreignIndex,marineIndex,msIndex,mcIndex,navIndex,PEIndex

client = Elasticsearch(hosts=["localhost"])

redis_cli = redis.StrictRedis()


class IndexView(View):

    @staticmethod
    def get(request):
        topn_search_clean = []
        topn_search = redis_cli.zrevrangebyscore(
            "search_keywords_set", "+inf", "-inf", start=0, num=5)
        for topn_key in topn_search:
            topn_key = str(topn_key, encoding="utf-8")
            topn_search_clean.append(topn_key)
        topn_search = topn_search_clean
        return render(request, "index.html", {"topn_search": topn_search})


class SearchSuggest(View):

    @staticmethod
    def get(request):
        key_words = request.GET.get('s', '')
        current_type = request.GET.get('s_type', '')

        if current_type == "it":
            return_suggest_list = []
            if key_words:
                s = ITIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        if current_type == "art":
            return_suggest_list = []
            if key_words:
                s = artIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        if current_type == "marine":
            return_suggest_list = []
            if key_words:
                s = marineIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        if current_type == "cj":
            return_suggest_list = []
            if key_words:
                s = cjIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        if current_type == "foreign":
            return_suggest_list = []
            if key_words:
                s = foreignIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        if current_type == "ms":
            return_suggest_list = []
            if key_words:
                s = msIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        if current_type == "mc":
            return_suggest_list = []
            if key_words:
                s = mcIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        if current_type == "nav":
            return_suggest_list = []
            if key_words:
                s = navIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        if current_type == "PE":
            return_suggest_list = []
            if key_words:
                s = PEIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:5]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")

class SearchView(View):

    def get(self, request):
        key_words = request.GET.get("q", "")

        # 通用部分
        # 实现搜索关键词keyword加1操作
        redis_cli.zincrby("search_keywords_set", key_words)
        #获取topn关键字
        # topn_search_clean = []
        # topn_search = redis_cli.zrevrangebyscore(
        #     "search_keywords_set", "+inf", "-inf", start=0, num=5)
        # for topn_key in topn_search:
        #     topn_key = str(topn_key, encoding="utf-8")
        #     topn_search_clean.append(topn_key)
        # topn_search = topn_search_clean
        # 当前要获取第几页的数据
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except BaseException:
            page = 1
        response = []
        start_time = datetime.now()
        s_type = request.GET.get("s_type", "")
        if s_type == "it":
            response = client.search(
                index="it_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "marine":
            response = client.search(
                index="marine_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "cj":
            response = client.search(
                index="cj_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "ms":
            response = client.search(
                index="ms_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "mc":
            response = client.search(
                index="mc_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "nav":
            response = client.search(
                index="nav_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "PE":
            response = client.search(
                index="pe_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "foreign":
            response = client.search(
                index="foreign_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "art":
            response = client.search(
                index="art_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )
        elif s_type == "_all":
            response = client.search(
                index="_all",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    } ,
                    "sort": [
                        {
                            "_score":{
                                "order": "desc"
                            },
                            "crawl_time": {
                                "order": "desc",
                              #  "ignore_unmapped": "true"
                            }
                        }
                    ]
                }
            )

        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()

        # 计算机工程学院的具体的信息
        hit_list = []
        error_nums = 0
        if s_type == "it":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "计算机工程学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "marine":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "轮机工程学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "art":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "美术学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "foreign":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "外国语学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "cj":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "财经学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "ms":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "工商学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "mc":
                    for hit in response["hits"]["hits"]:
                        hit_dict = {}
                        try:
                            if "title" in hit["highlight"]:
                                hit_dict["title"] = "".join(hit["highlight"]["title"])
                            else:
                                hit_dict["title"] = hit["_source"]["title"]
                            if "content" in hit["highlight"]:
                                hit_dict["content"] = "".join(
                                    hit["highlight"]["content"])
                            else:
                                hit_dict["content"] = hit["_source"]["content"][:200]

                            hit_dict["url"] = hit["_source"]["url"]
                            hit_dict["score"] = hit["_score"]
                            hit_dict["source_site"] = "音乐学院"
                            hit_list.append(hit_dict)
                        except:
                            error_nums = error_nums + 1
        elif s_type == "nav":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "航海学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "PE":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "体育学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "_all":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]

                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "所有学院"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1

        total_nums = int(response["hits"]["total"])

        # 计算出总页数
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,

                                               "s_type": s_type,

                                               })


favicon_view = RedirectView.as_view(
    url='#', permanent=True)