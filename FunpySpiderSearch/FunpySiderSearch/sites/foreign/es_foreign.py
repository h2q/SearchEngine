from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer



connections.create_connection(hosts=["localhost"])

my_analyzer = analyzer('ik_smart')


class foreignIndex(Document):
    """计算机工程学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'foreign_blog'


if __name__ == "__main__":

    foreignIndex.init()
