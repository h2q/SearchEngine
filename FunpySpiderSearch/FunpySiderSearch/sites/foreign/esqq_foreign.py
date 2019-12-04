from elasticsearch import Elasticsearch
es = Elasticsearch('localhost:9200')
mappings_settings = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "pinyin_analyzer": {
                        "type": "custom",
                        "tokenizer": "ik_max_word",
                        "filter": ["pinyin_filter"]
                    }
                },
                "filter": {
                    "pinyin_filter": {
                        "type": "pinyin",
                        "keep_first_letter": "true",
                        "keep_full_pinyin": "true",
                        "keep_joined_full_pinyin": "true",
                        "keep_none_chinese_in_joined_full_pinyin": "true",
                        "keep_original": "true",
                        "remove_duplicated_term": "true"
                    }
                }
            }
        }
    },
    "mappings": {
        "doc": {
            "properties": {
                "suggest": {
                "max_input_length": 50,
                 "analyzer":"pinyin_analyzer",
                 "search_analyzer":"ik_max_word",
               "preserve_position_increments": "true",
               "type": "completion",
               "preserve_separators": "true"
             },
        "url_object_id": {
            "type": "keyword",

        },
        "create_date": {
            "type": "date"
        },
        "title": {
             "analyzer":"pinyin_analyzer",
           "search_analyzer":"ik_max_word",
            "type": "text"
        },
        "content": {
             "analyzer":"pinyin_analyzer",
           "search_analyzer":"ik_max_word",
            "type": "text"
        },
        "url": {
            "type": "keyword"
        },
         "crawl_time":
             {
                 "type":"date"
             }
    }

}
            }
        }

res = es.indices.create(index = 'foreign_blog',body =mappings_settings)