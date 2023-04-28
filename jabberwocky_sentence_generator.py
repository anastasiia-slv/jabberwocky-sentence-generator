# -*- coding: utf-8 -*-
"""Jabberwocky Sentence Generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SVF3ATpyaBIucCyXG0jN59oCETEUPabM
"""
import ukrsyllab #syllabificator for Ukrainian

from syllable import Encoder #this function separates Turkish words into syllables
import re, random
from TurkishStemmer import TurkishStemmer #this function stems Turkish words 
from uk_stemmer import UkStemmer #this function stems Ukrainian words
from ast import literal_eval
from psychopy import gui

class Pseudoword_gen():
    
  """
  A class that generates pseudowords and Jabberwocky sentences depending on the 
  sound probabilities in a language determined by the words in a given database.

    ...

    Attributes
    ----------
    filename : str
        name of the database that has the existing words in a language
    n_words : int, optional
        number of the pseudowords to be generated, the default value is 300
    n_sent : int, optional
        number of Jabberwocky sentences to be generated, the default value is 5

    Methods
    -------
    probabilities(syllables):
        creates a dictionary that contains the probabilities of 
        different syllables following each other, and calculates the probability 
        of different syllables occuring as the first syllable, it requires a 
        list of lists that contains the syllables of words in the language
  
  """
  
  def __init__(self, filename, n_words, n_sent):

    """
    Constructs all the necessary attributes for the Pseudoword_gen object, opens
    and reads the database that has the existing words and stores them in a 
    variable

        Parameters
        ----------
        filename : str
            name of the database that has the existing words in a language
        n_words : int
            number of the pseudowords to be generated, the default value is 300
        n_sent : int
            number of Jabberwocky sentences to be generated, the default value 
            is 5
    """
    file = open(filename, "r", encoding="utf8")
    self.words = file.read().split("\n")
    self.n_words = n_words #number of words to generate
    self.n_sent = n_sent #number of sentences to generate

  def probabilities(self, syllables):
    """
    Creates a probability dictionary that contains the probabilities of different 
    syllables following each other, and calculates the probability of different 
    syllables occuring as the first syllable, it requires a list of lists that
    contains the syllables of words in the language

        Parameters
        ----------
        syllables : list
            a list of lists that contains syllables of different words in a 
            language

        Returns
        -------
        sound_prob : dict
            a dictionary that contains all probabilities regarding the 
            probability of a syllable following another one, keys are syllables
            and values are a list of probabilities
        in_m : dict
            a dictionary that contains the probability of different syllables
            being the initial syllable the keys are syllables and values are
            the probabilities
    """
    sound_prob = {} #an empty dictionary to store syllables and the possibilities of another syllable following them
    in_m = {} #an empty dictionary to store initial syllables of words and their possibility to appear in the first syllable
    for s in syllables:
      i = 0 #index value
      if len(s) != 1: #if the word has only one syllable, it is not going to be added to the probability
        if s[i] not in in_m: #if the first syllable is not in the database add it in the database
          in_m[s[i]] = 1/(len(self.stems)) #divided by the len to normalize the values
        else:
          in_m[s[i]] += 1/(len(self.stems))#if it is in the database increase the possibility
        while i < (len(s) - 1): #while the index is still in the bound of the word
          b = s[i] #taking two consequative syllables from the word
          n = s[i+1]
          if n != "": #in the cases where we have two syllables following each other, (the initial syllable is not the last syllable of the word)
            if b in sound_prob: #if the first syllable is in the database of syllables
              if n in sound_prob: #if the second one is in the database as well
                bInd = list(sound_prob).index(n) #find the index of the second syllable
                sound_prob[b][bInd] = int(sound_prob[b][bInd]) + 1 #and manipulate the probability value in the row of b that has the index of the following syllable
              else:
                probs = len(sound_prob) * "0" #if the second syllable does not exist in the dataset, we need to add it to the matrix and it needs a value row full of 0's (because its frequency with other sounds is 0)
                sound_prob[n] = list(probs) 
                for x in sound_prob: sound_prob[x].append(0) #every row of the matrix should be appended with 0 because the new sound that is added is also added as a new column that has never occured with the other sounds before
                sound_prob[b][-1] = 1 #the last entry of the probability of b should be altered to 1 because the new added sound appeared after that so +1 occurence
            else:
              probs = len(sound_prob) * "0" #if b does not exist in the dataset we should add it
              sound_prob[b] = list(probs)
              for x in sound_prob: sound_prob[x].append(0)
              if n in sound_prob:
                bInd = list(sound_prob).index(n)
                sound_prob[b][bInd] = int(sound_prob[b][bInd]) + 1
              else:
                sound_prob[n] = list(probs)
                sound_prob[n].append(0)
                for x in sound_prob: sound_prob[x].append(0)
                sound_prob[b][-1] = 1
          i += 1
    for v in sound_prob.values(): #to turn every value in the dictionary to float
      for n in range(len(v)):
        v[n] = float(v[n])/len(sound_prob.keys()) #normalize the probabilities
    return sound_prob, in_m

class Turkish_jabberwocky(Pseudoword_gen):
  """
  A daughter class of Pseudoword_gen that generates pseudowords and Jabberwocky 
  sentences that are following the sound regularities and grammatical structure
  of Turkish.
    ...

    Attributes
    ----------
    filename : str
        name of the database that has the existing words in Turkish
    n_words : int, optional
        number of the pseudowords to be generated, the default value is 300
    n_sent : int, optional
        number of Jabberwocky sentences to be generated, the default value is 5

    Methods
    -------
    probabilities(syllables):
        creates a probability dictionary that contains the probabilities of 
        different syllables following each other, and calculates the probability 
        of different syllables occuring as the first syllable, it requires a 
        list of lists that contains the syllables of words in the language
    syllabification(stem):
        takes a list of Turkish stems and separates them into their syllables 
        and stores them in a list of lists
    vowel_harmony(m1, m2):
        takes two consequative syllables and changes the second one according to
        the rules of Turkish vowel harmony
    categorize(pwords):
        takes a list of words and then assigns them into random syntactical 
        categories, adds suffixes according to their categories and stores them 
        in a dictionary
    sent_generator(pdic):
        takes a dictionary that has different syntactical categories as keys and 
        words as values, and picks random words from each category and forms 
        sentences according to the word order of Turkish
    run():
        runs the functions in the class in an order to create pseudowords and 
        Jabberwocky sentences in Turkish
  """
  def __init__(self, filename, n_words, n_sent):
    """
    Constructs all the necessary attributes for the Turkish_jabberwocky object, 
    opens and reads the database that has the existing words and stores them in 
    a variable. Furthermore, it removes any inflectional suffix from the words
    and stores the stems in a list.

        Parameters
        ----------
        filename : str
            name of the database that has the existing words in a language
        n_words : int
            number of the pseudowords to be generated, the default value is 300
        n_sent : int
            number of Jabberwocky sentences to be generated, the default value 
            is 5
    """
    super().__init__(filename, n_words=300, n_sent=5)

    self.stems = [] #The empty list that will be appended with stems
    for w in self.words[:50000]: #We are only taking a slice, because the actual database has more than 300.000 words that it takes a lot of time to run.
      w = TurkishStemmer().stem(w) #Getting the stems of Turkish words 
      if w in self.words and len(w) != 1 and w.lower() == w: #These two conditions are added because in the database there are proper names that are mostly Arabic that we would like to avoid and there are some one letter words that are not actual words in Turkish, i.e., "a"
        if w not in self.stems:#To avoid appending the same words
          self.stems.append(w)

  def syllabification(self, stems):
    """
    Takes a list of Turkish stems and separates them into their syllables and 
    stores them in a list of lists

        Parameters
        ----------
        stems : list
            a list that contains stems in Turkish

        Returns
        -------
        syllables : list
            a list of lists that contain syllables of different words
    """
    syllables = [] #An empty list to store the words that are separated into syllables
    encoder = Encoder(lang="tr") #Initializing the function for syllable separation in Turkish
    for word in stems:
      word = word.strip()
      morphemes = encoder.tokenize(word).split() #Separating the words into their syllables
      syllables.append(morphemes) #Store the list of syllables of a word in another list
    return syllables

  def vowel_harmony(self, m1, m2): #It changes syllables of the words according to the vowel harmony of Turkish
    """
    Takes two consequative syllables and changes the second one according to the 
    rules of Turkish vowel harmony

        Parameters
        ----------
        m1 : str
            a string that contains a Turkish syllable
        m2 : str
            a string that contains a Turkish syllable that follows m1 in a word

        Returns
        -------
        m2 : str
            a string that contains modified version of argument m2 according to
            the rules of vowel harmony
    """
    if re.search("[aı]", m1):
        m2 = re.sub("e|i|o|u|ö|ü","a", m2)
    elif re.search("[ei]", m1):
        m2 = re.sub("a|ı|o|u|ö|ü","e", m2)
    elif re.search("[ou]", m1):
        m2 = re.sub("e|i|ı|o|ö|ü","a", m2)
    elif re.search("[öü]", m1):
        m2 = re.sub("a|i|ı|o|ö|u","e", m2)
    return m2

  def categorize(self, pwords):
    """
    Takes a list of words and then assigns them into random syntactical 
    categories, adds suffixes according to their categories and stores them in a 
    dictionary

        Parameters
        ----------
        pwords : list
            a list of Turkish pseudowords

        Returns
        -------
        categories : dict
            a dictionary which has syntactical categories as the keys and 
            pseudowords that are assigned to a syntactical category and added
            suffixes according to the category
    """
    categories = {"SUBJECT": [],
                "PREDICATE": [],
                "ATTRIBUTE":[],
                "OBJECT": [],
                "ADVERBIAL MODIFIER": []} #a dictionary to place words randomly into different syntactical categories
    for w in pwords:
      c = random.choice(list(categories.keys())) #randomly assigning words to different categories
      if c == "PREDICATE": #to add appropriate suffixes for predicates (past tense suffix)
        if re.search("[aeıioöuü]$", w): #following the suffix rules of Turkish
          if re.search("[aıou]$", w): #following the vowel harmony rules of Turkish
            w = w + "dı"
          else:
            w = w + "di"
        else:
          if re.search("[fstkçşhp]$", w):
            if re.search("[aıou]", w):
              w = w + "tı"
            else:
              w = w + "ti"
          else:
            if re.search("[aıou]", w):
              w = w + "dı"
            else:
              w = w + "di"
      elif c == "OBJECT":
        if re.search("[aeıioöuü]$", w):
          if re.search("[aıou]$", w):
            w = w + "yı"
          else:
            w = w + "yi"
        else:
          if re.search("p$", w):
            if re.search("[aıou]", w):
              w = re.sub("p$", "bı", w)
            else:
              w = re.sub("p$", "bi", w)
          elif re.search("ç$", w):
            if re.search("[aıou]", w):
              w = re.sub("ç$", "cı", w)
            else:
              w = re.sub("ç$", "ci", w)
          elif re.search("t$", w):
            if re.search("[aıou]", w):
              w = re.sub("t$",  "tı", w)
            else:
              w = re.sub("t$",  "ti", w)
          elif re.search("k$", w):
            if re.search("[aıou]", w):
              w = re.sub("k$",  "ğı", w)
            else:
              w = re.sub("k$",  "ği", w)
          else:
            if re.search("[aıou]", w):
              w = w + "ı"
            else:
              w = w + "i"
      elif c == "ADVERBIAL MODIFIER":
        if re.search("[fstkçşhp]$", w):
          w = w + "ç"
        else:
          w = w + "c"
        if re.search("[aıou]", w):
          w = w + "a"
        else:
          w = w + "e"
      categories[c].append(w)
    return categories
  
  def sent_generator(self, pdic):
      """
      Takes a dictionary that has different syntactical categories as keys and 
      words as values, and picks random words from each category and forms 
      Jabberwocky sentences according to the word order of Turkish

        Parameters
        ----------
        pdic : dict
            a dictionary that has syntactical categories as the keys and lists
            of pseudowords that are assigned to that category as values

        Returns
        -------
        sent : str
            a Jabberwocky sentence that includes Turkish pseudowords from 
            different syntactical categories in the order of Turkish word order
      """
      subj = random.choice(list(pdic["SUBJECT"])) #picking random pseudowords from each syntactical category
      pred = random.choice(list(pdic["PREDICATE"]))
      attr = random.choice(list(pdic["ATTRIBUTE"]))
      obje = random.choice(list(pdic["OBJECT"]))
      adve = random.choice(list(pdic["ADVERBIAL MODIFIER"]))
      sent_str = random.choice(["sent_str1", "sent_str2"]) #Turkish allows for 2 different word orders, randomly picking one
      if sent_str == "sent_str1":
        sent = subj + " " + attr + " " + obje + " " + adve + " " + pred + ".\n"
      else:
        sent = subj + " " + adve + " " + attr + " " + obje + " " + pred + ".\n"
      return sent.capitalize()
    
  def run(self):
    """
    Runs the functions in the class in an order to create pseudowords and 
    Jabberwocky sentences in Turkish

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    syllable = self.syllabification(self.stems) #To split words into syllables
    dict_prob, in_morph = self.probabilities(syllable) #To calculate the possibility of syllables following each other
    p_words = [] #an empty list to store generated pseudowords
    j = 0 #the number of generated pseudowords
    while j < self.n_words:
      pword = [] #an empty list to store the syllables that will be used in generating the pseudoword
      i = 0 #length of the pseudoword
      plen = 7 #the average word length in Turkish is 7, this value is picked because of that
      while i < plen:
        if pword == []: #initial syllables are picked from the dictionary that stores initial syllables 
          sound = random.choices(list(in_morph.keys()), weights=in_morph.values())[0]
          i += len(sound) #increase the length of the word by the picked sound
        else:
            if sum(dict_prob[pword[-1]]) != 0: #this condition is necessary, because certain syllables in Turkish only appear in the end of words which means the possibility of these syllables being followed by a syllable is 0 but they are still in the database because they follow a syllable
              sound = random.choices(list(dict_prob.keys()), weights=dict_prob[pword[-1]])[0]
              i += len(sound)
            else:
              i = plen #if a syllable that usually appears in the end of a word is picked, the word should end not elaborate 
        pword.append(sound) #add the picked sound to the word
      m = 1
      while m < len(pword): #to modify the syllables according to the rules of vowel harmony
        pword[m] = self.vowel_harmony(pword[m-1], pword[m])
        m += 1
      pword = "".join(pword)
      if not re.search("\w*[aeıioöuü][aeıioöuü]\w*", pword) and pword not in p_words: #in Turkish two vowels do not appear together, this condition is to check for this
        p_words.append(pword)
      j += 1

    word_categories = self.categorize(p_words) #to assign random syntactic categories to the pseudowords
    p_sentences = [] #an empty list to store generated sentences
    for i in range(self.n_sent):
      p_sentences.append(self.sent_generator(word_categories))
    return p_sentences

class Ukrainian_jabberwocky(Pseudoword_gen):
  """
  A daughter class of Pseudoword_gen that generates pseudowords and Jabberwocky 
  sentences that are following the sound regularities and grammatical structure
  of the Ukrainian language.
    ...

    Attributes
    ----------
    filename : str
        name of the database that has the existing words in Ukrainian
    n_words : int, optional
        number of the pseudowords to be generated, the default value is 300
    n_sent : int, optional
        number of Jabberwocky sentences to be generated, the default value is 5

    Methods
    ---------
    probabilities(syllables):
        creates a probability dictionary that contains the probabilities of 
        different syllables following each other, and calculates the probability 
        of different syllables occuring as the first syllable, it requires a 
        list of lists that contains the syllables of words in the language
    syllabification(stems):
        takes a list of Ukrainian stems and separates them into their syllables 
        and stores them in a list of lists
    normalization(p_list):
        takes a list of pseudostems and normalizes them to form refined pseudowords
        by eliminating repeated syllables, redundant vowels, and consonants. 
        the primary function is to randomly assign suffixes to the pseudostems, 
        resulting in the creation of morphologically recognizable pseudowords
    categorize(dataset):
        categorizes a list of words into distinct syntactical categories, 
        adding them to the dictionary
    sent_generator(dic):
        takes the dictionary with syntactical categories as keys 
        and words as values to randomly select words from each category 
        and form sentences in Ukrainian word order. gender coordination is 
        taken into account during the selection process
    run():
        runs the functions in the class in an order to create pseudowords and 
        Jabberwocky sentences in Ukrainian
  """
  def __init__(self, filename, n_words, n_sent):
    """
    Constructs all the necessary attributes for the Ukrainian_jabberwocky object, 
    opens and reads the database that has the existing words and stores them in 
    a variable. Furthermore, it removes any inflectional suffix from the words
    and stores the stems in a list.

        Parameters
        ----------
        filename : str
            name of the database that has the existing words in a language
        n_words : int
            number of the pseudowords to be generated, the default value is 300
        n_sent : int
            number of Jabberwocky sentences to be generated, the default value 
            is 5
    """
    super().__init__(filename, n_words, n_sent)

    self.stems = [] #the empty list that will be appended with stems
    for w in self.words[:50000]: #only taking a portion of the database because the full database contains over 300,000 words, which takes a significant amount of time to run
      w = re.sub("\w'\w", "", w) #remove apostrophe words
      w = re.sub("\w-\w", "", w) #remove hyphenated words
      stemmer = UkStemmer() 
      w = stemmer.stem_word(w) #stem the words from the dataset
      if w in self.words and len(w) > 1 and w.lower() == w: #two conditions have been included to remove any proper names and one-letter words
        if w not in self.stems: #avoid appending the same words
          self.stems.append(w) #append the stems list with unique lower-case two(or more)-syllable stems 

  def syllabification (self, stems):
    """
      Takes a list of Ukrainian stems and separates them into their syllables and 
      stores them in a list of lists.

          Parameters
          ----------
          stems : list
              a list that contains stems in Ukrainian

          Returns
          -------
          syllables : list
              a list of lists that contain syllables of different words
      """
    syllables = [] #an empty list to store the words that are separated into syllables
    for word in stems:
      morphemes = ukrsyllab.split_word(word) #separating the words into their syllables
      syllables.append(morphemes) #store the list of syllables of a word in another list
    return syllables

  def normalization (self, p_list):
    """
       Takes a list of pseudostems, eliminates repeated syllables, redundant vowels, 
       and consonants; randomly assigns suffixes to pseudostems, resulting in the 
       creation of morphologically recognizable pseudowords.

          Parameters
          ----------
          p_list : list
              a list that contains pseudostems in Ukrainian

          Returns
          -------
          p_words : list
              a list that contains refined morphologically recognizable pseudowords
      """
    global p_words
    p_words = []
    suffixes = ['о-таки', 'о-то','но','цька','ий','ик','ник','івник','льник','иво','аль','ень','ець','ість','тель','иця','иня','ння','іння','ання','яння','ення','иння','еня','ечок','ечка','ечко','ичок','ичка','енко','енько','исько','ище','івка','овка','ок','ир','ист','изм','ір','іст','ізм','яти','ати','іти']
    ending = ['б', 'в', 'г', 'ґ', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    for instance in p_list: 
        if (list(filter(instance.endswith, ending))): #if the ending of the pseudostem matches any ending of the 'ending' list, it gets a random suffix from the 'suffixes' list     
          norm = instance + random.choice(suffixes)
          if norm not in p_words: #pseudowords list gets appended with the unique pseudoword
            p_words.append(norm)
    p_words = re.sub(r'(.+?)\1+', r'\1', str(p_words))
    p_words = literal_eval(str(p_words))
    return p_words  

  def categorize (self, dataset): 
    """
      Categorizes a list of words into distinct syntactical categories. 
      Initially, subjects and adverbial modifiers are stored in the dictionary, 
      while predicates, attributes, and objects are stored in separate lists 
      for later inflection. Then, the lists are passed to the functions with 
      the main function. 

          Parameters
          ----------
          dataset : list
              a list of Ukrainian pseudowords

          Returns
          -------
          uk_pos : dict
              a dictionary which has syntactical categories as the keys and 
              pseudowords that are assigned to a syntactical category
      """
    uk_pos = {"SUBJECT": [],
              "PREDICATE": [],
              "ATTRIBUTE":[],
              "OBJECT": [],
              "ADVERBIAL MODIFIER": []} #a dictionary to place words into different syntactical categories
    
    #suffix lists, by which functions within the sentence are implied
    subj_suff = ['ик','ник','івник','льник','иво','аль','ень','ець','ість','тель','иця','иня','ння','іння','ання','яння','ення','иння','еня','ечок','ечка','ечко','ичок','ичка','енко','исько','ище','івка','овка','ок','ир','ист','изм','ір','іст','ізм']
    pred_suff = ['ти']
    attr_suff = ['ий']
    mod_suff = ['-таки', '-то', 'но', 'ацька' ]

    pr = []
    attr = []
    obj = []

    for word in dataset: #iterate though the dataset
        if any(word.endswith(s) for s in subj_suff): #iterate through the suffix list
              uk_pos["SUBJECT"].append(word) #if there's a match, add pseudowords in the nominative case to the dictionary -- subjects
              obj.append(word) #if there's a match, add pseudowords in the nominative case to the specific list to later be inflected -- objects 
        elif any(word.endswith(mod) for mod in mod_suff): 
              uk_pos["ADVERBIAL MODIFIER"].append(word) #if there's a match, add pseudowords in the nominative case to the dictionary -- adverbial modifiers
        elif any(word.endswith(p) for p in pred_suff): 
              pr.append(word) #if there's a match, add pseudowords in the nominative case to the specific list to later be inflected -- predicates
        elif any(word.endswith(at) for at in attr_suff):
              attr.append(word) #if there's a match, add pseudowords in the nominative case to the specific list to later be inflected -- attributes

    def infl_dict(infl_suff, inf_suff, lst, dict_key): 
       """
      Inflects the lists of predicates and attributes for accusative 
      and adds them to the dictionary.

          Parameters
          ----------
          infl_suff : list
              a list of inflectional suffixes
          inf_suff: str
              a suffix in infinitive/nominative case to be inflected
          lst: list
              a list of a certain morphological category to be inflected
          dict_key: list
              a dictionary key to be appended with the pseudowords

          Returns
          -------
          None
      """
       for st in lst: #iterate though the list
          for af in infl_suff: #iterate through the nominative suffix list
            ret = re.sub(inf_suff, af, st) #substitute the ending in the nominative case with the ending in the accusative
            uk_pos[dict_key].append(ret) 

    infl_dict(infl_suff=['в','ла', 'ло'], inf_suff = 'ти', lst=pr, dict_key="PREDICATE")
    infl_dict(infl_suff=['ої','ого'], inf_suff = 'ий', lst=attr, dict_key="ATTRIBUTE")

    def infl_dict_obj (gendered_suffix, inflection): 
        """
      Inflects the list of objects for accusative based on gendered noun 
      inflection rules, which depend on the hardness or softness of the 
      ending consonant, and adds them to the dictionary.

          Parameters
          ----------
          gendered_suffix: list
              a list of gendered inflectional suffixes
          inflection: str
              a suffix in infinitive/nominative case to be inflected
          
          Returns
          -------
          None
      """
        for ob in obj: #iterate though the list
          if any(ob.endswith(s) for s in gendered_suffix): #iterate through the gendered nominative suffix list
            if ob[-1] in ['м', 'р', 'к', 'т']: #nouns ending with suffixes from the list, and with these letters specifically, get another letter added
              ob = ob + inflection
            elif ob[-1] in ['ь']: #other nouns that match change the last letter 
              ob = ob[:-1] + inflection
            elif ob[-1] in ['я']:
              ob = ob[:-1] + inflection
            elif ob[-1] in ['а']:
              ob = ob[:-1] + inflection
            elif ob[-1] in ['о', 'е']:
              ob = ob[:-1] + inflection
            uk_pos["OBJECT"].append(ob)

    infl_dict_obj(gendered_suffix=['ик','ник','івник','льник','ок','ир','ист','изм', 'ір', 'іст', 'ізм'], inflection = 'а') #masculine nouns that end in a hard consonant
    infl_dict_obj(gendered_suffix= ['аль', 'ень' 'тель', 'ець'], inflection = 'я') #masculine nouns that end in a soft consonant
    infl_dict_obj(gendered_suffix=['иця','иня','ння','іння','ання','яння','иння'], inflection = 'і') #feminine nouns that end in a soft consonant
    infl_dict_obj(gendered_suffix=['ичка', 'івка', 'овка'], inflection = 'и') #feminine nouns that end in a hard consonant
    infl_dict_obj(gendered_suffix=['иво', 'ечко', 'енко', 'исько','ище'], inflection = 'а') #neutral nouns
    return uk_pos

  def sent_generator(self, dic): #generate sentences with the dictionary values, based on the dictionary keys
    """
        Takes the dictionary with syntactical categories as keys 
        and words as values to randomly select words from each category 
        and form sentences in Ukrainian word order. Gender coordination is 
        taken into account during the selection process.

          Parameters
          ----------
          dic : dict
              a dictionary that has syntactical categories as the keys and lists
              of pseudowords that are assigned to that category as values

          Returns
          -------
          sent : str
              a Jabberwocky sentence that includes Ukrainian pseudowords from 
              different syntactical categories in Ukrainian word order
    """
    subj = random.choice(list(dic["SUBJECT"])) #pick a random value
    pred = random.choice(list(dic["PREDICATE"]))
    attr = random.choice(list(dic["ATTRIBUTE"]))
    obje = random.choice(list(dic["OBJECT"]))
    adve = random.choice(list(dic["ADVERBIAL MODIFIER"]))

    if re.search('[ое]$', subj): #coordinate subject and predicate by gender
        while not re.search('ло$', pred): #if a chosen subject matches a certain pattern, a predicate must match a specific pattern too -- if it doesn't, a different value is being chosen until the conditions are satisfied.
          pred = random.choice(list(dic["PREDICATE"]))     
    elif re.search('[аяь]$', subj):
        while not re.search('ла$', pred):
          pred = random.choice(list(dic["PREDICATE"]))
    elif re.search('[кмстр]$', subj):
        while not re.search('в$', pred):
          pred = random.choice(list(dic["PREDICATE"]))
      
    if re.search('[иі]$', obje): #coordinate attribute and object by gender
        while not re.search('ої$', attr): #if a chosen object matches a certain pattern, an attribute must match a specific pattern too -- if it doesn't, a different value is being chosen until the conditions are satisfied.
          attr = random.choice(list(dic["ATTRIBUTE"]))
    elif re.search('[ая]$', obje): 
        while not re.search('ого$', attr):
          attr = random.choice(list(dic["ATTRIBUTE"]))     

    sent_str = random.choice(["sent_str1", "sent_str2",  "sent_str3"]) #create random sentences using a randomly chosen structure, natural to the ukrainian syntax
    if sent_str == "sent_str1":
      sent = subj + " " + pred + " " + attr + " " + obje + " " + adve + ".\n"
    elif sent_str == "sent_str2":
      sent = adve + " " + subj + " " + pred + " " + attr + " " + obje + ".\n"
    else: 
      sent = attr + " " + obje + " " + pred + " " + subj + " " + adve + ".\n"
    sent = sent.capitalize()
    return sent

  def run(self):
      """
      Runs the functions in the class in an order to create pseudowords and 
      Jabberwocky sentences in Ukrainian

          Parameters
          ----------
          None

          Returns
          -------
          None
      """  
      syllable = self.syllabification(self.stems)
      dict_prob, in_morph = self.probabilities(syllable)
      
      pre_p_words = [] 
      j=0
      while j < self.n_words: #create pseudostems
        pword = []
        i = 0
        plen = 5
        while i < plen:
         if pword == []:
           sound = random.choices(list(in_morph.keys()), weights=in_morph.values())[0]
           i += len(sound)
         else:
            if sum(dict_prob[pword[-1]]) != 0:
              sound = random.choices(list(dict_prob.keys()), weights=dict_prob[pword[-1]])[0]
              i += len(sound)
            else:
              i = plen
         pword.append(sound)
        pword = "".join(pword)
        pre_p_words.append(pword)
        p_words = self.normalization(pre_p_words) #run function to normalize the stems
        j += 1

      word_categories = self.categorize(p_words)#run function to sort the parts of the sentences into the dictionary
      p_sentences = []
      for i in range(self.n_sent):
        p_sentences.append(self.sent_generator(word_categories)) #run function to create sentences
      return p_sentences
  
#The code that opens up the GUI  
dlg = gui.Dlg(title= "Jabberwocky Generator") #The title of the window
dlg.addField("Language", choices=["Turkish", "Ukrainian"]) #Language options
dlg.addField("Number of pseudowords to be generated", 300) #The number of pseudowords to be generated (default is 300)
dlg.addField("Number of sentences to be generated", 5) #The number of jabberwocky sentences to be generated (default is 5)
Udata = dlg.show() #To obtain GUI data as a list
while type(Udata[1]) != int or type(Udata[2]) != int: #If a non-integer value is entered the GUI will appear until the integer values are entered
    err_dlg = gui.Dlg(title='error message')
    err_dlg.addText("Please enter an integer to the number of pseudoword and sentence fields")
    err_dlg.show()
    dlg = gui.Dlg(title= "Jabberwocky Generator")
    dlg.addField("Language", choices=["Turkish", "Ukrainian"])
    dlg.addField("Number of pseudowords to be generated", 300)
    dlg.addField("Number of sentences to be generated", 5)
    Udata = dlg.show()
    
if Udata[0] == "Ukrainian": #If Ukrainian is selected 
    j_sent = Ukrainian_jabberwocky("uk_UA.csv", int(Udata[1]), int(Udata[2])).run()
elif Udata[0] == "Turkish": #If Turkish is selected
    j_sent = Turkish_jabberwocky("tr_TR.csv", Udata[1], Udata[2]).run()
    
f_name = Udata[0] + "_Jabberwockysent.txt" #To write down the obtained sentences
f = open(f_name, "w", encoding="utf-8")
for s in j_sent:
    f.write(s)
f.close()