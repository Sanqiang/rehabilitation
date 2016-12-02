package features;

import java.util.StringTokenizer;

public class Document {
	
	private String sents;
	
	public double spw, wl, sl, lw, lw_ditr;
	
	public int cnt_word, cnt_syl, cnt_sent = 1;

	
	public void setDocument(String sents) {
		this.sents = sents;
		process();
	}
	
	public void	process() {
		StringTokenizer tokenizer = new StringTokenizer(this.sents);
		String token = null;
		
		while (tokenizer.hasMoreTokens()) {
			token = tokenizer.nextToken();
			if (Word.isSentenceEnd(token)) {
				++cnt_sent;
			}else{
				int cnt_word_syl = Word.countSyllables(token);
				cnt_syl += cnt_word_syl;
				if(cnt_syl >= 3){
					++lw;
				}
				++cnt_word;
			}
		}
		
		spw = cnt_syl / cnt_word;
		wl = spw * 100;
		sl = cnt_word / cnt_sent;
		lw_ditr = lw / cnt_word;
	}
}
