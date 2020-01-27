from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=["localhost"])

my_analyzer = analyzer('ik_smart')
class ITIndex(Document):
    """计算机工程学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")

    class Index:
        name = 'it_blog'
class artIndex(Document):
    """轮机工程学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")#最新粒度拆分
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")#最粗粒度拆分
    create_date = Date()

    class Index:
        name = 'art_blog'

class cjIndex(Document):
    """财经学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'cj_blog'


class foreignIndex(Document):
    """计算机工程学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'foreign_blog'

class marineIndex(Document):
    """轮机工程学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    create_date = Date()

    class Index:
        name = 'marine_blog'

class msIndex(Document):
    """工商学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'ms_blog'

class mcIndex(Document):
    """音乐学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'mc_blog'

class navIndex(Document):
    """航海学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'nav_blog'

class PEIndex(Document):
    """体育学院文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'PE_blog'

