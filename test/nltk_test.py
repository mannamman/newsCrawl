import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 


def test_fun(word_tokens :str):
    stops = set(stopwords.words('english'))
    result = []
    for word in word_tokens: 
        if word not in stops: 
            result.append(word) 
    return_str = " ".join(result)
    print(return_str)
context = u"Family is not an important thing. It's everything."
word_tokens = word_tokenize(context)
test_fun(word_tokens)