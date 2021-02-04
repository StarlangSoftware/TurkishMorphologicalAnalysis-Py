For Developers
============

You can also see [Cython](https://github.com/starlangsoftware/TurkishMorphologicalAnalysis-Cy), [Java](https://github.com/starlangsoftware/TurkishMorphologicalAnalysis), [C++](https://github.com/starlangsoftware/TurkishMorphologicalAnalysis-CPP), or [C#](https://github.com/starlangsoftware/TurkishMorphologicalAnalysis-CS) repository.

## Requirements

* [Python 3.7 or higher](#python)
* [Git](#git)

### Python 

To check if you have a compatible version of Python installed, use the following command:

    python -V
    
You can find the latest version of Python [here](https://www.python.org/downloads/).

### Git

Install the [latest version of Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Download Code

In order to work on code, create a fork from GitHub page. 
Use Git for cloning the code to your local or below line for Ubuntu:

	git clone <your-fork-git-link>

A directory called DataStructure will be created. Or you can use below link for exploring the code:

	git clone https://github.com/starlangsoftware/TurkishMorphologicalAnalysis-Py.git

## Open project with Pycharm IDE

Steps for opening the cloned project:

* Start IDE
* Select **File | Open** from main menu
* Choose `DataStructure-PY` file
* Select open as project option

Detailed Description
============

+ [Creating FsmMorphologicalAnalyzer](#creating-fsmmorphologicalanalyzer)
+ [Word level morphological analysis](#word-level-morphological-analysis)
+ [Sentence level morphological analysis](#sentence-level-morphological-analysis)

## Creating FsmMorphologicalAnalyzer 

FsmMorphologicalAnalyzer provides Turkish morphological analysis. This class can be created as follows:

    fsm = FsmMorphologicalAnalyzer()
    
This generates a new `TxtDictionary` type dictionary from [`turkish_dictionary.txt`](https://github.com/olcaytaner/Dictionary/tree/master/src/main/resources) with fixed cache size 100000 and by using [`turkish_finite_state_machine.xml`](https://github.com/olcaytaner/MorphologicalAnalysis/tree/master/src/main/resources). 

Creating a morphological analyzer with different cache size, dictionary or finite state machine is also possible. 
* With different cache size, 

        fsm = FsmMorphologicalAnalyzer(50000);   

* Using a different dictionary,

        fsm = FsmMorphologicalAnalyzer("my_turkish_dictionary.txt");   

* Specifying both finite state machine and dictionary, 

        fsm = FsmMorphologicalAnalyzer("fsm.xml", "my_turkish_dictionary.txt") ;      
    
* Giving finite state machine and cache size with creating `TxtDictionary` object, 
        
        dictionary = TxtDictionary("my_turkish_dictionary.txt");
        fsm = FsmMorphologicalAnalyzer("fsm.xml", dictionary, 50000) ;
    
* With different finite state machine and creating `TxtDictionary` object,
       
        dictionary = TxtDictionary("my_turkish_dictionary.txt", "my_turkish_misspelled.txt");
        fsm = FsmMorphologicalAnalyzer("fsm.xml", dictionary);

## Word level morphological analysis

For morphological analysis,  `morphologicalAnalysis(String word)` method of `FsmMorphologicalAnalyzer` is used. This returns `FsmParseList` object. 


    fsm = FsmMorphologicalAnalyzer()
    word = "yarına"
    fsmParseList = fsm.morphologicalAnalysis(word)
    for i in range(fsmParseList.size()):
      	print(fsmParseList.getFsmParse(i).transitionList())
    
      
Output

    yar+NOUN+A3SG+P2SG+DAT
    yar+NOUN+A3SG+P3SG+DAT
    yarı+NOUN+A3SG+P2SG+DAT
    yarın+NOUN+A3SG+PNON+DAT
    
From `FsmParseList`, a single `FsmParse` can be obtained as follows:

    parse = fsmParseList.getFsmParse(0)
    print(parse.transitionList())  
    
Output    
    
    yar+NOUN+A3SG+P2SG+DAT
    
## Sentence level morphological analysis
`morphologicalAnalysis(Sentence sentence)` method of `FsmMorphologicalAnalyzer` is used. This returns `FsmParseList[]` object. 

    fsm = FsmMorphologicalAnalyzer()
    sentence = Sentence("Yarın doktora gidecekler")
    parseLists = fsm.morphologicalAnalysis(sentence)
    for i in range(len(parseLists)):
        for j in range(parseLists[i].size()):
            parse = parseLists[i].getFsmParse(j)
            print(parse.transitionList())
        print("-----------------")
    
Output
    
    -----------------
    yar+NOUN+A3SG+P2SG+NOM
    yar+NOUN+A3SG+PNON+GEN
    yar+VERB+POS+IMP+A2PL
    yarı+NOUN+A3SG+P2SG+NOM
    yarın+NOUN+A3SG+PNON+NOM
    -----------------
    doktor+NOUN+A3SG+PNON+DAT
    doktora+NOUN+A3SG+PNON+NOM
    -----------------
    git+VERB+POS+FUT+A3PL
    git+VERB+POS^DB+NOUN+FUTPART+A3PL+PNON+NOM
