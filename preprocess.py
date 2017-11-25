#remove users "@"----done
#remove hyderlinks ---done
#remove hashtags unless it is the one we are searching for !!!!NOT DONE!!!!
import nltk
import re,string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *

def stem_words(text):
	stemmer=PorterStemmer()	
	word_tokens = word_tokenize(text)
	filtered_sentence=[stemmer.stem(words) for words in word_tokens]
	ret=""
	for w in filtered_sentence:
		ret=ret+w+" "
	return ret
	
def strip_links(text):
	link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*\s*)')
	links         = re.sub(link_regex,'', text) 
	return links

def strip_all_usernames(text):
	username_regex = re.compile('\B@([\w*\.*:*]+\s*)')
	username       = re.sub(username_regex,'',text)
	return username
   
def strip_all_hashtags(text):
	hashtag_regex = re.compile('\B#([\w*]+\s*)')
	hashtag	  = re.sub(hashtag_regex,'',text)
	return hashtag

def remove_stopwords(text):
	stop_words = set(stopwords.words('english'))
	word_tokens = word_tokenize(text)
	filtered_sentence = [w for w in word_tokens if not w in stop_words]
	ret=""
	for w in filtered_sentence:
		ret=ret+w+" "
	return ret
	
def preprocess(text):
	return strip_all_usernames(strip_all_hashtags(strip_links(text)))
#test="#GiveMeYourFuture https://t.co/QFKyP5ot95RT @tommyfromspace: Fri 8th sept @Tunnel267 @Space_The_Band #London #GiveMeYourFuture https://t.co/TLeqpQSTso https://t.co/VTWgMZ2b4nRT @jayaprimatour: So, kota mana yang akan Traveler kunjungi untuk menikmati musim gugur tahun ini ? #Kyoto #Montreal #Seoul #London #Berli…Luck and wishes to Weibang M on set today for @LittleLifeUK - have fun and enjoy all x #SetLife #photography #london #movies #action #film #london #londonprestige #kowloon #kowloonkillers #cinema #director… https://t.co/MBpN3mwfjv https://t.co/nuPqUFG8xh Your last opportunity to hear Big Ben's bongs before it goes silent until 2021 #London  https://t.co/u3F475FXovA NIGHT IN LONDON #indie #romantic #City #London"
#print (preprocess(test))
# @[\w*\d*_*]+(\.*)[\w*\d*_*]*

stem_words("Human machine interface for lab abc computer applications")
