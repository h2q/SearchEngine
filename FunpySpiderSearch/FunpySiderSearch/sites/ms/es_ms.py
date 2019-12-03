from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer



connections.create_connection(hosts=["localhost"])

my_analyzer = analyzer('ik_smart')


class msIndex(Document):
    """工商学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'ms_blog'


if __name__ == "__main__":

    msIndex.init()
