
### What are Jabberwocky Sentences?

Jabberwocky sentences are syntactically correct, yet composed of invented words (e.g., *the gostak distims the doshes*).

They are useful for studying syntax, morphology, and semantics, and are widely employed in psycholinguistics and neurolinguistics research to investigate syntactic processing independently of semantic influence.

However, Turkish and Ukrainian are understudied languages with limited pseudoword generators that do not follow essential linguistic rules, such as Turkish vowel harmony.

This project seeks to to create additional resources for linguistic research on these languages, with potential for adaptation to other understudied languages.

### The Current Project

Our project aims to create pseudowords and Jabberwocky sentences in Turkish and Ukrainian. 
Script:
1.   Takes user inputs for language, number of pseudowords and Jabberwocky sentences from Python console
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

In order to install them manually:
```
pip install TurkishStemmer
pip install git+https://github.com/ftkurt/python-syllable.git@master 
pip install git+https://github.com/Desklop/Uk_Stemmer 
```

Alternatively, the repository includes the requirements.txt file listing all the dependencies for this specific project.

To install the packages using the requirements.txt file:
```
pip install -r requirements.txt
```

#### How to Run the Script?

After fulfilling all code dependencies, open and run the script in your Python interpreter. 

**Note**: Do not attempt to run it on Google Colab, as the newest Python version used there will not support the code. 

The script can be run in a regular way with any OS but MacOS. 
```
python3 jabberwocky_sentence_generator.py
```


**Note**: Running scripts with a GUI on MacOS within a virtual environment produces an error.\
To avoid this, first install the python.app binary/wxPython:
```
conda install python.app
```
Then, run the script with the following command:
```
pythonw jabberwocky_sentence_generator.py
```

When the script is run, it will ask for inputs from the python console. Those inputs will include:
* language of the jabberwocky sentences
* the number of the pseudowords to be generated
* the number of the sentences to be generated
* the name of the output file

**Language of the jabberwocky sentences**

User must enter one of the languages presented inside the paranthesis as input to choose the language of the jabberwocky sentences. The input is case insensitive. This field also provides a "quit" option to user, if the user wants to quit the program, they can do so by typing "q" to the field. 

```
Enter the language of the Jabberwocky sentences ('Turkish' or 'Ukrainian')(To quit enter 'q'):
```

**Number of pseudowords to be generated**

User must enter an integer value in this field to specify the number of pseudowords they want to generate. The default value is 300.

```
Enter the number of pseudowords to be generated (The default value is 300) (The value entered should be an integer): 
```

**Number of sentences to be generated**

User must enter an integer value in this field to specify the number of Jabberwocky sentences they want to generate. The default value is 5.

```
Enter the number of sentences to be generated (The default value is 5) (The value entered should be an integer):  
```

**Name of the output file**
User must enter a string that would be used as the name of the output file. Output file will be named "[filename].txt".

```
Enter a name for the output file (It will be saved as [filename].txt):
```

**Note:** If a language that does not exist in the program is entered, an error message will appear asking the user to input one of the languages of the program and input field for language will reappear. This process will continue until a language in the program is entered. 

```
You have entered a language that is not currently in the programme. Plase try again!
Enter the language of the Jabberwocky sentences ('Turkish' or 'Ukrainian): 
```

Furthermore, if a non-integer value is entered in the pseudowords or Jabberwocky sentences fields, an error message will appear asking the user to input an integer value. The input field for the non-integer value will reappear, and this process will continue until the user inputs integer values.

```
The value that you have entered is not an integer. Please enter another number!
Enter the number of pseudowords to be generated (The default value is 300) (The value entered should be an integer): 
```
```
The value that you have entered is not an integer. Please enter another number!
Enter the number of pseudowords to be generated (The default value is 5) (The value entered should be an integer): 
```

Upon providing necessary information, the code will generate Jabberwocky sentences in the chosen language and write them to a txt file named according to the user input.

#### The Structure of the Script

The script has a mother class, "Pseudoword_gen", with two daughter classes, "Turkish_jabberwocky" and "Ukrainian_jabberwocky". 

The mother class includes a language-independent function called "probabilities", which is inherited by the daughter classes and can be used for multiple languages. It is independent of language structures, including the alphabet.

Depending on the language entered in the input field, one of the daughter classes will be utilized. The daughter classes are motivated by unique linguistic characteristics of each language, and may differ slightly.

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
6. Update the input field to include the new language as an option.
7. Modify the code to call the appropriate daughter class based on the user's language selection.

*This project was created by Anastasiia Salova and Ecesu Ürker.*
