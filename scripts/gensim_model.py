# for topic modelling
from gensim import corpora
from gensim.models import ldamodel
from itertools import chain
import spacy
from collections import Counter

def build_the_model(data):
    # loading the model
    nlp = spacy.load("en_core_web_sm")
    # remove ner function to speed up the processing
    nlp.disable_pipes('ner')

    def crop_full_text(text):
        words = text.split()
        first_150 = ' '.join(words[0:150])
        return first_150

    def get_lemmas(text):
        '''
    This function takes in a string, and returns only noun lemmas
    '''
        doc = nlp(text)
        pt = [token.lemma_.lower() for token in doc if
           (len(token.lemma_) > 1 and token.pos_ == "NOUN" and not token.is_stop)]
        return pt


    def drop_high_frequency_words(lemmas):
        for word in high_freq_words.keys():
            if word in lemmas:
                lemmas = [x for x in lemmas if x != word]
                return lemmas


    # shorten the full text for spead
    data['lemmas'] = data['clean_text'].apply(crop_full_text)

    # getting lemmas
    
    data.loc[:,'lemmas'] = data['lemmas'].apply(get_lemmas)

    # Getting the corpus length 
    docs_length=len(data['lemmas'])

    # # calculate in how many documents a word appeared
    counts_word_percentage = Counter(chain(*[set(x) for x in data['lemmas']]))

    # # calculate in what % of all articles a word appears
    counts_word_percentage = {key:(value/docs_length)*100 for (key,value) in counts_word_percentage.items()}

    # # get words with high frequency
    high_freq_words = {key:value for (key,value) in counts_word_percentage.items() if value>25}

    data.loc[:,'lemmas'] = data['lemmas'].apply(drop_high_frequency_words)
    
    #Replace None lemmas
    data.loc[:,'lemmas'] = data['lemmas'].apply(lambda d: d if isinstance(d, list) else [])
    
    # Defining dictionary and corpus with Gensim
    dictionary = corpora.Dictionary(data['lemmas'])
    corpus = [dictionary.doc2bow(text) for text in data['lemmas']]

    # Building topics model using LDA
    lda_model = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=22, alpha='auto', eval_every=5)

    topics =  lda_model.show_topics()

    # Assign most likely topic to the data point

    def get_most_likely_label(lemmas):
        bow = dictionary.doc2bow(lemmas)
        output = lda_model.get_document_topics(bow, minimum_probability=0.000001)
        topics = sorted(output,key=lambda x:x[1],reverse=True)
        return topics[0][0]


    data['gensim_topic'] = data['lemmas'].apply(get_most_likely_label)

    return topics, data






    