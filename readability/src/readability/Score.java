package readability;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import features.Document;

public class Score {
	public static double getFleschReadingEaseScore(String url){
		Document document = new Document();
		document.setDocument(getHtmlContent(url));
		return 206.835-0.846*document.wl-1.015*document.sl;
	}
	
	public static double getFleschKincaidReadingGradeLevel(String url){
		Document document = new Document();
		document.setDocument(getHtmlContent(url));
		return 0.39*document.sl+11.8*document.spw-15.59;
	}
	
	public static double getFogIndex(String url){
		Document document = new Document();
		document.setDocument(getHtmlContent(url));
		return 0.4*(document.sl + document.lw_ditr);
	}
	
	public static double getSmogRgl(String url){
		Document document = new Document();
		document.setDocument(getHtmlContent(url));
		return 3+Math.sqrt(document.lw);
	}
	
    private static String getHtmlContent(String htmlurl) {  
        URL url;  
        String temp;  
        StringBuffer sb = new StringBuffer();  
        try {  
            url = new URL(htmlurl);  
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            while ((temp = in.readLine()) != null) {  
                sb.append(temp);  
            }  
            in.close();  
        } catch (final MalformedURLException me) {
            me.getMessage();  
        } catch (final IOException e) {  
            e.printStackTrace();  
        }  
        return delHTMLTag(sb.toString());  
    }
    
    public static String delHTMLTag(String htmlStr){ 
        String regEx_script="<script[^>]*?>[\\s\\S]*?<\\/script>"; 
        String regEx_style="<style[^>]*?>[\\s\\S]*?<\\/style>";
        String regEx_html="<[^>]+>";
        
        Pattern p_script=Pattern.compile(regEx_script,Pattern.CASE_INSENSITIVE); 
        Matcher m_script=p_script.matcher(htmlStr); 
        htmlStr=m_script.replaceAll("");
        
        Pattern p_style=Pattern.compile(regEx_style,Pattern.CASE_INSENSITIVE); 
        Matcher m_style=p_style.matcher(htmlStr); 
        htmlStr=m_style.replaceAll("");
        
        Pattern p_html=Pattern.compile(regEx_html,Pattern.CASE_INSENSITIVE); 
        Matcher m_html=p_html.matcher(htmlStr); 
        htmlStr=m_html.replaceAll("");

       return htmlStr.trim();
    } 
    
    public static void main(String[] args) {
		String url = "http://priceonomics.com/extract-text-and-calculate-the-reading-level-of/";
		System.out.println(Score.getFogIndex(url));
	}
}
