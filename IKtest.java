
 
import java.io.IOException;
import java.io.StringReader;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.wltea.analyzer.lucene.IKAnalyzer; 
public class IKtest {	
	public static void main(String[] args) throws IOException {		
		String text="软件工程搜索引擎中文分词测试";		//创建分词对象		
		Analyzer anal=new IKAnalyzer(true);				
		StringReader reader=new StringReader(text);		//分词		
		TokenStream ts=anal.tokenStream("", reader);		
		CharTermAttribute term=ts.getAttribute(CharTermAttribute.class);		//遍历分词数据		
		while(ts.incrementToken()){			
			System.out.print(term.toString()+"|");		
		}		
		reader.close();		
		System.out.println();	
	} 
}

