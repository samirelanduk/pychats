import random

class MarkovGenerator:
    """Something which can generate a Markov message"""

    def __init__(self, markov_entities):
        self.markov_entities = markov_entities

        self.initial_distribution = [entity.markov_words[0] for entity in self.markov_entities
         if len(entity.markov_words) > 1 and entity.can_use]



    def generate_message(self):
        """Generate a message using Markov chains, based on exisiting messages"""
        message = []
        message.append(self.get_first_word())
        message.append(self.get_second_word(message[0]))

        while message[-1] != None:
            message.append(self.get_next_word(message[-2:]))

        return " ".join(message[:-1])



    def get_first_word(self):
        """Get the first work in a Markov sentence"""
        if len(self.initial_distribution) != 0:
            return random.choice(self.initial_distribution)



    def get_second_word(self, first_word):
        """Get the second word in a Markov sentence"""
        possibles = []
        for entity in [x for x in self.markov_entities
         if len(x.markov_words) > 0 and x.can_use]:
            i = 0
            for word in entity.markov_words[:-1]:
                if word == first_word:
                    possibles.append(entity.markov_words[i+1])
                i += 1

        return random.choice(possibles)



    def get_next_word(self, current_words):
        """Get the next word in a Markov sentence"""
        #Build up a list of possible next words
        possibles = []


        #Try and get a next word based on current two words
        for entity in [x for x in self.markov_entities
         if len(x.markov_words) > 0 and x.can_use]:
            i = 0
            for word in entity.markov_words[:-2]:
                if word == current_words[0] and entity.markov_words[i+1] == current_words[1]:
                    possibles.append(entity.markov_words[i+2])
                i += 1


        #If not possibele, get one based on most recent word only
        if len(possibles) == 0:
            for entity in [x for x in self.markov_entities
             if len(x.markov_words) > 0 and x.can_use]:
                i = 0
                for word in entity.markov_words[:-1]:
                    if word == current_words[1]:
                        possibles.append(entity.markov_words[i+1])
                    i += 1


        #Return a random possible word
        return random.choice(possibles)



class MarkovEntity:
    """Something which provides the text for a MarkovGenerator"""

    def __init__(self, text, can_use):
        #This will do for now
        self.markov_words = text.replace("\n", " ").split(" ") + [None]
        self.markov_words = [word for word in self.markov_words if word != ""]

        self.can_use = can_use
