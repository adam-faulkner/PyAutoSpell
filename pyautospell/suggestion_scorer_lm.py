from kenlm import LanguageModel
from pyautospell.suggestion_scorer import SuggestionScorer
from pyautospell.simple_tokenizer import SimpleTokenizer
import editdistance
import math

class SuggestionScorerLM(SuggestionScorer):

    def __init__(self, tokenizer, lm ):
        self.tokenizer = SimpleTokenizer()#tokenizer
        self.lm = LanguageModel(lm)

    def __get_context_tokens(self, prevwords, endwords):
        '''
        :param prevwords: list of Word objects
        :param endwords:  list of Word objects
        :return:
        '''
        vals = ["<s>", "<s>", "</s>", "</s>"]
        if (len(prevwords) > 1):
            vals[0] = prevwords[len(prevwords) - 2].word
        if (len(prevwords) > 0):
            vals[1] = prevwords[len(prevwords) - 1].word
        if (len(endwords) > 0):
            vals[2] = endwords[0].word
        if (len(endwords) > 1):
            vals[3] = endwords[1].word
        return vals

    def candidate_scoring(self, misspelllist, sentence):
        for idx, missed in enumerate(misspelllist):
            #TODO: if (self.filter_misspelling(next_misspelling, sentence))
             # misspelling_iter.remove();
             #  continue;
            #prevwords and endwords are lists of Word objects
            prevwords = self.tokenizer.tokenize(sentence[: missed.begin])
            endwords = self.tokenizer.tokenize(sentence[missed.end+1:])

            ppv = ""
            pv = ""
            nv =""
            nnv =""

            if (len(prevwords) > 1):
                ppv = prevwords[len(prevwords)- 2].word
            if (len(prevwords) > 0):
                pv = prevwords[len(prevwords) - 1].word
            if (len(endwords) > 0):
                nv = endwords[0].word
            if (len(endwords) > 1):
                nnv = endwords[1].word

            #first word?
            if not prevwords:
                pv= ""
                ppv = ""

            suggestions = missed.suggestions
            feature_map =  dict(zip(range(len(suggestions)), [[] for i in range(len(suggestions) )]))

            for sugg_indx, suggestion in enumerate(suggestions):
                features = [0,0]
                text = suggestion.text
                words = self.tokenizer.tokenize(text) #a list of Word objects
                head = words[0].word
                tail = words[len(words) - 1].word
                #Feature 1: language model feature
                if (self.lm != None):
                    head_prob = self.lm.score(" ".join([ppv, pv, head]))
                    tail_prob = self.lm.score(" ".join([tail, nv, nnv]))
                    head_plus_tail = math.exp(head_prob + tail_prob)
                    head_plus_tail = math.exp(head_prob + tail_prob) * suggestion.apriori
                    #feature_index+=1
                    feature_map[sugg_indx].append(head_plus_tail)
                    feature_map[sugg_indx] = head_plus_tail

            #rank-order the suggestions according to n-gram probability and add to Misspelling
            rank_ordered_suggs = list(reversed(self.__rank_suggestions(feature_map)))
            missed.suggestions= [suggestions[t[0]] for t in rank_ordered_suggs]
            #TODO: Feature 2: Edit distance
            #sim = 1.0 - (editdistance.eval(missed.word, text)/len(missed.word))
            #print("leven ", sim)
            #features[1] = sim
            #feature_map[sugg_indx].append(sim)

            #TODO: Feature 3: Frequency
            #if (len(words) == 1):
            #   // features[featureIndex + +] = um.getFrequencyStrictly(head);
            #else
            #// features[featureIndex + +] = Math.sqrt(um.getFrequencyStrictly(head)
            #                                      // * um.getFrequencyStrictly(tail));
            #featureVal[i] = features;
             #_featureSize = featureIndex;
            #}
            #X = feature_map[sugg_indx] #np.asarray(feature_map[sugg_indx])

            #
            #normalized = preprocessing.normalize(X, norm='l2')
            #normalized= [float(i)/sum(X) for i in X]#normalize(X,  axis=0).ravel()
            #preprocessing.normalize(X, norm='l2')

            #print("normed ", normalized)
            #feature_map[sugg_indx] = normalized
            #print("feature map vals after norming ",feature_map)
             #feature_index += 1


    def score_suggestion(self, suggestion , sentence):
        '''
        :param suggestion:
        :param sentence:
        :return:
        '''
        misspelling = suggestion.misspelling
        prevwords = self.tokenizer.tokenize(sentence[0 : misspelling.begin])
        endwords = self.tokenizer.tokenize(sentence[misspelling.end : len(sentence )- 1])
        vals = self.__get_context_tokens(prevwords, endwords)
        text = suggestion.text
        words = self.tokenizer.tokenize(text)
        prob = self.__obtain_prob(words, vals)
        apriori = suggestion.apriori
        totalprob = prob * apriori
        return totalprob

    def __rank_suggestions(self, feature_map):
        as_ls = feature_map.items()
        return sorted(as_ls, key = lambda tup: tup[1])

    def __obtain_prob(self, words, vals):
        head_prob = float("nan")
        tail_prob = float("nan")
        prob = float("nan")
        ppv = vals[0].word
        pv = vals[1].word
        nv = vals[2].word
        nnv = vals[3].word
        head = words[0].word
        tail = words[len(words) - 1].word
        if (len(words) == 2):
            head_prob = self.lm.score(pv +head+tail)
            tail_prob = self.lm.score(head+ tail+ nv)
        else:
            head_prob = self.lm.score(ppv+pv+head)
            tail_prob = self.lm.score(tail + nv +nnv)
        prob = math.exp(head_prob + tail_prob)
        return prob
