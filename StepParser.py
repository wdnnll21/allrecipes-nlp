from RecipeGrabber import GrabFromRemote
from RecipeX import Recipe, Action
import spacy
from VerbMap import verbMap

nlp = spacy.load('en_core_web_sm')

rec = GrabFromRemote("https://www.allrecipes.com/recipe/242362")

def basicActions(recipe):
    for step in recipe.directions:
        for sentence in step:
            a = nlp(sentence)
            for word in a:
                if word.dep_ == "ROOT":
                    if word.pos_ == "VERB":
                        ActionMaker(a)
                    else:
                        reclaimSentence(sentence)
                        break
        """elif word.dep_ == "conj" and word.pos_ == "VERB":
          print(word.text)"""

def reclaimSentence(sentence):
    sentence = "I " + sentence.lower()
    a = nlp(sentence)
    for word in a:
        if word.dep_ == "ROOT" and word.pos_ == "VERB":
            ActionMaker(a[1:])

def ActionMaker(sentence):
    acts = []
    for word in sentence:
        if word.tag_ in ["VBP","VB"] and word.text not in ["is","are"]:
            verb = word.text
            classify = verbClassify(verb)
            items = []
            preps = []
            for sub in word.subtree:
                if sub.dep_ == "dobj" and sub.head.text == word.text:
                    items.append(sub.text)
                    items.extend([x.text for x in sub.conjuncts])
                if sub.dep_ in ["prep","mark"] and (sub.head.text == word.text or sub.head.text in items):
                    preps.append([x.text for x in sub.subtree])
            acts.append((verb,classify,items,preps))
    return acts
        
def verbClassify(verb):
    for category in verbMap:
        if verb.lower() in verbMap[category]:
            return category
    print("Not Recognized",verb)
    return "Prepare"

basicActions(rec)