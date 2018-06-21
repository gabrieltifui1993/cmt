from nltk import FreqDist, TweetTokenizer

tweet = "Criptomoneda este cea mai sigura metoda de plata. Plata prin criptomonede nu doar ca este sigura dar ofera si anonimitate"

t_word_tokenizer = TweetTokenizer()

words = t_word_tokenizer.tokenize(tweet)
words=[word.lower() for word in words if word.isalpha()]

allWordDist = FreqDist(word.lower() for word in words)

print(allWordDist.most_common(1000))