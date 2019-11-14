#%%
import re
import pyarabic.araby as araby
#%%
# from py4j.java_gateway import JavaGateway

# gateway = JavaGateway.launch_gateway(classpath='farasa_segmenter/FarasaSegmenterJar.jar')
# farasa = gateway.jvm.com.qcri.farasa.segmenter.Farasa()
regex_url = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
regex_mention = r'@[\w\d]+'
regex_email = r'\S+@\S+'
redundant_punct_pattern = r'([!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ【»؛\s+«–…‘]{2,})'



def remove_elongation(word):
	"""
    :param word:  the input word to remove elongation
    :return: delongated word
    """
	regex_tatweel = r'(\w)\1{2,}'
	# loop over the number of times the regex matched the word
	for index_ in range(len(re.findall(regex_tatweel, word))):
		if re.search(regex_tatweel, word):
			elongation_found = re.search(regex_tatweel, word)
			elongation_replacement = elongation_found.group()[0]
			elongation_pattern = elongation_found.group()
			word = re.sub(elongation_pattern, elongation_replacement, word, flags=re.MULTILINE)
		else:
			break
	return word


def tokenize_arabic_words(line_input):
	tokenized_line_input = list()
	tokens = line_input.split()
	for token in tokens:
		if token.startswith('و') or token.startswith('ل') or token.startswith('ب') or token.startswith('ف'):
			token_split = list(farasa.segmentLine(token))
			token_ = token_split[0].split('+')
			if token_[0] in ['و', 'ل', 'ب', 'ف']:
				while token_[0] in ['و', 'ل', 'ب', 'ف'] and len(token_) > 2:
					token_[-2:] = [''.join(token_[-2:])]
				token_ = ' '.join(token_)
			else:
				token_ = ''.join(token_)
			tokenized_line_input.append(token_)
		else:
			tokenized_line_input.append(token)
	return ' '.join(tokenized_line_input)


def remove_redundant_punct(text):
	text_ = text
	result = re.search(redundant_punct_pattern, text)
	dif = 0
	while result:
		sub = result.group()
		sub = sorted(set(sub), key=sub.index)
		sub = ' ' + ''.join(list(sub)) + ' '
		text = ''.join((text[:result.span()[0]+dif], sub, text[result.span()[1]+dif:]))
		text_ = ''.join((text_[:result.span()[0]], text_[result.span()[1]:])).strip()
		dif = abs(len(text) - len(text_))
		result = re.search(redundant_punct_pattern, text_)
	text = re.sub(r'\s+', ' ', text)
	return text.strip()


def preprocess(text):
	text=str(text)
	processing_tweet = araby.strip_tashkeel(text)
	processing_tweet = re.sub(r'\d+\/[ء-ي]+\/\d+\]', '', processing_tweet)
	processing_tweet = re.sub(r'\d+([,\d]+)?', '[رقم]', processing_tweet)
	processing_tweet = re.sub('ـ', '', processing_tweet)
	processing_tweet = re.sub(regex_url, '[رابط]', processing_tweet)
	processing_tweet = re.sub(regex_email, '[بريد إلكتروني]', processing_tweet)
	processing_tweet = re.sub(regex_mention, '[مستخدم]', processing_tweet)
	processing_tweet = re.sub('…', r'\.', processing_tweet).strip()
	processing_tweet = remove_redundant_punct(processing_tweet)

	processing_tweet = re.sub(r'\[ رقم \]|\[رقم \]|\[ رقم\]', ' [رقم] ', processing_tweet)
	processing_tweet = re.sub(r'\[ رابط \]|\[ رابط\]|\[رابط \]', ' [رابط] ', processing_tweet)
	processing_tweet = re.sub(r'\[ بريد إلكتروني \]|\[ بريد إلكتروني\]|\[بريد إلكتروني \]', ' [بريد إلكتروني] ', processing_tweet)
	processing_tweet = re.sub(r'\[ مستخدم \]|\[ مستخدم\]|\[مستخدم \]', ' [مستخدم] ', processing_tweet)

	processing_tweet = remove_elongation(processing_tweet)
	# processing_tweet = tokenize_arabic_words(processing_tweet)
	return processing_tweet.strip()
