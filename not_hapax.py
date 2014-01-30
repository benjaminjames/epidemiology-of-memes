from unigram import Unigram, db

the_words = Unigram.query.filter(Unigram.times_occurred > 1).all()
hapax = Unigram.query.filter(Unigram.times_occurred == 1).count()
the = Unigram.query.filter(Unigram.id == 'the').first().times_occurred

types = len(the_words)
tokens = 0

for word in sorted(the_words):
    tokens += word.times_occurred
    print('{}'.format(word))

summary = '\n{:,} types and {:,} tokens, with {:,} hapax unigrams ({:.2%} of the corpora). "the" was {:.2%} of the corpora.'
form = (types, tokens, hapax, hapax / tokens, the / tokens)
print(summary.format(*form))
