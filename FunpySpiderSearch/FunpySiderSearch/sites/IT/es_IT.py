from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer    #导入CustomAnalyzer类

connections.create_connection(hosts=["localhost"])
my_analyzer = analyzer('ik_smart')

class CustomAnalyzer(_CustomAnalyzer):                                      # 自定义CustomAnalyzer类，来重写CustomAnalyzer类
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])  # 实例化重写的CustomAnalyzer类传入分词器和大小写转，将大写转换成小写

class ITIndex(Document):
    """计算机工程学院文章类型"""
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")
    class Index:
        name = 'it_blog'


def gen_suggest(index, info_tuple):
    # 根据字符串生成搜索建议数组
    """
    此函数主要用于,连接elasticsearch(搜索引擎)，使用ik_max_word分词器，将传入的字符串进行分词，返回分词后的结果
    此函数需要两个参数：
    第一个参数：要调用elasticsearch(搜索引擎)分词的索引index，一般是（索引操作类._doc_type.index）
    第二个参数：是一个元组，元祖的元素也是元组，元素元祖里有两个值一个是要分词的字符串，第二个是分词的权重，多个分词传多个元祖如下
    书写格式：
    gen_suggest(lagouType._doc_type.index, (('字符串', 10),('字符串', 8)))
    """
    es = connections.create_connection(ITIndex._doc_type.using)       # 连接elasticsearch(搜索引擎)，使用操作搜索引擎的类下面的_doc_type.using连接
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串，
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    # 返回分词后的列表，里面是字典，
    # 如：[{'input': ['录音', '广告'], 'weight': 10}, {'input': ['新能源', '汽车',], 'weight': 8}]
    return suggests

if __name__ == "__main__":

    ITIndex.init()
