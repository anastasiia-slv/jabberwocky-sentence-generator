
### What are Jabberwocky Sentences?

Jabberwocky sentences are syntactically correct, yet composed of invented words (e.g., *the gostak distims the doshes*).

They are useful for studying syntax, morphology, and semantics, and are widely employed in psycholinguistics and neurolinguistics research to investigate syntactic processing independently of semantic influence.

However, Turkish and Ukrainian are understudied languages with limited pseudoword generators that do not follow essential linguistic rules, such as Turkish vowel harmony.

This project seeks to to create additional resources for linguistic research on these languages, with potential for adaptation to other understudied languages.

### The Current Project

Our project aims to create pseudowords and Jabberwocky sentences in Turkish and Ukrainian. 
Script:
1.   Uses GUI to take user inputs for language, number of pseudowords and Jabberwocky sentences
2.   Takes dataset of existing words in selected language
3. Cleans up words from inflectional affixes
4. Separates words into natural morphemes
5. Calculates probability of each morpheme following another and appearing as initial morpheme
6. Constructs pseudowords based on appearance probabilities and user input
7. Assigns pseudowords into syntactic categories and adds affixes based on language rules
8. Forms user-specified number of Jabberwocky sentences based on language's word order rules
9. Writes Jabberwocky sentences into file named language_Jabberwockysent.txt.

#### How Does the Script Work?

#### Dependencies

Recommended Python version: 3.8. Compatible with up to version 3.10, but newer versions may not support necessary libraries.

The script requires the following libraries to run: PsychoPy, TurkishStemmer| https://github.com/otuncelli/turkish-stemmer-python, Syllable Encoder (for Turkish)| https://github.com/ftkurt/python-syllable, Uk_Stemmer|https://github.com/Desklop/Uk_Stemmer, ukrsyllab.py (provided in the current repository), re, random, and ast. 

#### How to Run the Script?

After fulfilling all code dependencies, open and run the script in your Python interpreter. 

Note: Do not attempt to run it on Google Colab, as the newest Python version used there will not support the code. Running the script will display a window as shown below:

<img width="477" alt="1" src="https://user-images.githubusercontent.com/126243859/235170272-9363755d-e82c-4376-adfe-1037fe603e52.png">

In this pop-up window, three sets of information is required from the user:

**Language**

The script presents a multiple choice area for selecting language to generate Jabberwocky sentences. User can click the area and choose desired language from available options, which currently include only Turkish and Ukrainian.

<img width="478" alt="2" src="https://user-images.githubusercontent.com/126243859/235171181-75d7eeba-d580-4c6a-b1b9-9e7223cd3cd4.png">

**Number of pseudowords to be generated**

User must enter an integer value in this field to specify the number of pseudowords they want to generate. The default value is 300.

**Number of sentences to be generated**

User must enter an integer value in this field to specify the number of Jabberwocky sentences they want to generate. The default value is 5.

**Note:** If a non-integer value is entered in the pseudowords or Jabberwocky sentences fields, an error message will appear asking the user to input an integer value. The initial pop-up window for user preferences will reappear, and this process will continue until the user inputs integer values.

<img width="480" alt="3" src="https://user-images.githubusercontent.com/126243859/235171264-b044e412-9bbf-4f30-844a-f9546faf30b0.png">

<img width="367" alt="4" src="https://user-images.githubusercontent.com/126243859/235171302-089e2fd0-8a7d-46b2-b119-808b3ff82825.png">

Upon providing necessary information, the code will generate Jabberwocky sentences in the chosen language and write them to a txt file named "language_Jabberwockysent.txt".

#### The Structure of the Script

The script has a mother class, "Pseudoword_gen", with two daughter classes, "Turkish_jabberwocky" and "Ukrainian_jabberwocky". 

The mother class includes a language-independent function called "probabilities", which is inherited by the daughter classes and can be used for multiple languages. It is independent of language structures, including the alphabet.

Depending on the language chosen in the initial pop-up window, one of the daughter classes will be utilized. The daughter classes are motivated by unique linguistic characteristics of each language, and may differ slightly.

| <sup>The Pseudoword_gen <br>Class</sup> |  | <sup>Turkish_jabberwocky <br>Class</sup> |  | <sup>Ukrainian_jabberwocky <br>Class</sup> |  |
|---|---|---|---|---|---|
| <sup>*probabilities*</sup> | <sup>creates a probability dictionary that shows the probability of different syllables appearing after one another, as well as the probability of different syllables occurring as the first syllable.</sup> | <sup>*syllabification*</sup>| <sup>separates Turkish stems into syllables</sup> | <sup>*syllabification*</sup> | <sup>takes a list of Ukrainian stems, separates them into syllables, and stores them in a list of lists</sup> |
|  |  | <sup>*vowel_harmony*</sup>| <sup>changes syllables according to the rules of Turkish vowel harmony</sup> | <sup>*normalization*</sup>| <sup>takes a list of pseudostems, eliminates repeated syllables, redundant vowels, and consonants; randomly assigns suffixes to pseudostems, resulting in the creation of morphologically recognizable pseudowords</sup> |
|  |  | <sup>*categorize*</sup> | <sup>assigns Turkish pseudowords to random syntactical categories and adds suffixes according to the category</sup> | <sup>*categorize*</sup> | <sup>categorizes a list of words into distinct syntactical categories and adds them to the dictionary</sup> |
|  |  | <sup>*sent_generator*</sup> | <sup>creates Jabberwocky sentences in Turkish by placing pseudowords with suffixes according to their syntactical category, following the word order rules of Turkish</sup> | <sup>*sent_generator*</sup> | <sup>uses the dictionary with syntactical categories as keys and words as values to randomly select words from each category and form sentences in Ukrainian word order (it also takes gender coordination into account during the selection process)</sup> |
|  |  |<sup>*run*</sup> | <sup>calls the functions inside the class in a particular order. It creates pseudowords according to the probabilities of syllables and creates Jabberwocky sentences</sup> | <sup>*run*</sup> | <sup>executes the functions in the class in a particular order to create pseudowords and Jabberwocky sentences in Ukrainian</sup> |

### How to extend a project?

The project can easily be extended to accommodate different tasks, such as adding more syntactic categories or incorporating negation into the grammatical structure.

To extend the project to new languages:

1. Add a new daughter class inheriting the Pseudoword_gen mother class.
2. Prepare a dataset of existing words in the language.
3. Implement syllabification function based on the language's phonological rules.
4. Implement a function that assigns pseudowords into syntactic categories and adds affixes based on the language's grammar rules.
5. Implement Jabberwocky sentences creation function based on the language's word order rules.\
Optional:
6. Update the GUI to include the new language as an option.
7. Modify the code to call the appropriate daughter class based on the user's language selection.

*This project was created by Anastasiia Salova and Ecesu Ürker.*
