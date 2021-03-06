from RecipeGrabber import GrabFromRemote
from RecipeX import Recipe, Action
import spacy
import re
from VerbMap import verbMap,toolMap,aprimary

nlp = spacy.load('en_core_web_sm')

#rec = GrabFromRemote("https://www.allrecipes.com/recipe/278271/air-fryer-stuffed-mushrooms/")

class Phrase(object):
    def __init__(self,verb):
        self.verb = verb
        self.typ = ""
        self.objects = []
        self.preps = []
        self.tools = []
        self.ingrs = []

    def __str__(self):
        return "Method: " + str(self.verb) + "; Type: " + self.typ + "; Tools: " + str(self.tools) + "; Ingredients: " + str(self.ingrs) +"\n\t"+self.getStep()

    def getStep(self):
        objects = ", ".join([str(x) for x in self.objects])
        preptext = []
        for a in self.preps:
            for b in a:
                if b not in preptext:
                    preptext.append(b)
        preps = " ".join([str(x) for x in preptext])
        return str(self.verb) + " " +  objects + " " + preps

class Sentence(object):
    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)
        self.phrases = []
        self.sentenceChecker()

    def reclaimSentence(self):
        sentence = "I " + self.text.lower()
        a = nlp(sentence)
        for word in a:
            if word.dep_ == "ROOT" and word.pos_ == "VERB":
                return a[1:]
        return a

    def sentenceChecker(self):
        structures = {}
        a = self.doc
        for word in a:
            if word.dep_ == "ROOT":
                if word.tag_ in ["VBP","VB"]:
                    structures[word.lower_] = Phrase(word)
                    structures[word.lower_].typ = verbClassify(word.lower_)
                    for conj in word.conjuncts:
                        structures[conj.lower_] = Phrase(conj)
                        structures[conj.lower_].typ = verbClassify(conj.lower_)
                else:
                    a = self.reclaimSentence()
                    for wordb in a:
                        if wordb.dep_ == "ROOT":
                            structures[wordb.lower_] = Phrase(wordb)
                            structures[wordb.lower_].typ = verbClassify(wordb.lower_)
                            for conj in word.conjuncts:
                                structures[conj.lower_] = Phrase(conj)
                                structures[conj.lower_].typ = verbClassify(conj.lower_)
                    break
            #elif word.pos_ == "VERB" and word.dep_ != "conj":
            #    structures[word.lemma_] = Phrase(word)
        for word in a:
            if word.dep_ == "dobj":
                if word.head.lower_ in structures:
                    structures[word.head.lower_].objects.append(word)
                    if len(word.conjuncts) > 0:
                        structures[word.head.lower_].objects.extend(word.conjuncts)
            elif word.dep_ == "prep":
                head = word.head
                while head.tag_ not in ["VBP","VB"] and head.dep_ != "ROOT":
                    head = head.head
                if head.lower_ in structures:
                    structures[head.lower_].preps.append([x for x in word.subtree])
        self.doc = a
        self.phrases = list(structures.values())

        for phrase in self.phrases:
            if len(phrase.objects) == 0 and len(phrase.tools) == 0 and len(phrase.preps) == 0:
                self.phrases.remove(phrase)
            elif phrase.verb.lower_ in ["have","is","was","are","can"]:
                self.phrases.remove(phrase)
        

def basicActions(recipe):
    basic = []
    DiscoverDescriptor(recipe)
    for step in recipe.directions:
        sbreak = []
        for sentence in step:
            sbreak.append(Sentence(sentence))
        basic.append(sbreak)          

    return basic

def ActionMachine(recipe):
    basic = basicActions(recipe)
    tools = []
    actionList = []
    for step in basic:
        for sentence in step:
            for act in sentence.phrases:
                actionList.append(act)
                if act.typ == "Prepare":
                    for tool in toolMap:
                        if act.verb.text in toolMap[tool]:
                            act.tools.append(tool)
                            tools.append(tool)
                    for word in act.objects:
                        if any([word.lower_ in x.ingredient for x in recipe.ingredients]):
                            act.ingrs.append(word.lower_)
                        else:
                            act.tools.append(word.lower_)
                            tools.append(word.lower_)
                elif act.typ == "Cook":
                    for tool in toolMap:
                        if act.verb.text in toolMap[tool]:
                            act.tools.append(tool)
                            tools.append(tool)
                    for word in act.objects:
                        if any([word.lower_ in x.ingredient for x in recipe.ingredients]):
                            act.ingrs.append(word.lower_)
                        else:
                            act.tools.append(word.lower_)
                            tools.append(word.lower_)
                elif act.typ == "Combine":
                    for word in act.objects:
                        if any([word.lower_ in x.ingredient for x in recipe.ingredients]):
                            act.ingrs.append(word.lower_)
                        else:
                            act.tools.append(word.lower_)
                            tools.append(word.lower_)
                for prepphrase in act.preps:
                        if prepphrase[0].text in ["in","with","into","onto","from"]:
                            for prepword in prepphrase:
                                if prepword.dep_ == "pobj":
                                    if any([prepword.lower_ in x.ingredient for x in recipe.ingredients]):
                                        act.ingrs.append(prepword.lower_)
                                    else:
                                        act.tools.append(prepword.lower_)
                                        tools.append(prepword.lower_)
                for wordx in act.verb.subtree:
                    if len(wordx.lower_) > 2 and wordx.pos_ == "NOUN" and any([wordx.lower_ in x.ingredient for x in recipe.ingredients]):
                        if wordx.lower_ not in act.ingrs:
                            act.ingrs.append(wordx.lower_)
                
    """for step in basic:
        for sentence in step:
            for act in sentence.phrases:
                print(act)"""

    recipe.steps = actionList
    recipe.pm = PrimaryMethod(recipe,actionList)
    recipe.tools =  tools

    return recipe

def DiscoverDescriptor(recipe):
    for ingredient in recipe.ingredients:
        x = nlp(ingredient.ingredient)
        for word in x:
            if word.pos_ in ["ADJ","ADV"]:
                ingredient.descriptions += word.text + " "
            elif word.tag_ in ["VBN","VBD"] or word.lower_ in ["ground"]:
                ingredient.preparations += word.text + " "
                    
def PrimaryMethod(recipe,actionList):
    titleverbs = re.findall(re.compile("[A-Za-z]*ed"), recipe.title)

    for each in titleverbs:
        a = nlp("I " + each + " it")
        for word in a:
            if word.pos_ == "VERB":
                return word.lemma_

    candidates = []
    for action in actionList:
        if action.verb.lemma_.lower() not in aprimary and action.typ == "Cook":
            return action.verb.lemma_
        elif action.verb.lemma_.lower() not in aprimary:
            candidates.append(action.verb.lemma_)

    if len(candidates) == 0:
        return "make"
    return candidates[-1]

def ActionMaker(sentence):
    acts = []
    for word in sentence:
        if word.tag_ in ["VBP","VB"] and word.text not in ["is","are"]:
            verb = word.text
            classify = verbClassify(verb)
            rang = [max(min([x.i for x in word.subtree]),1), max([x.i for x in word.subtree])]
            acts.append([classify,verb,rang])
    if(len(acts) > 1):
        acts[0][2][1] = acts[1][2][0]
    
    actb = []

    for act in acts:
        act[2] = sentence.doc[act[2][0]:act[2][1]]
        actb.append(Action(act[0],act[1],act[2]))

    return actb
        
def verbClassify(verb):
    for category in verbMap:
        if verb.lower() in verbMap[category]:
            return category
    #print("Not Recognized",verb)
    return "Prepare"

def ingredientMentions(ingr,actions):
    for act in actions:
        chunks = list(act.doc.noun_chunks)
        chunkIngrs = map(lambda x: x if any((ing in x for ing in ingr)) else None, [chunk.text for chunk in chunks])
        act.ingr = [chunkIngr for chunkIngr in chunkIngrs if chunkIngr is not None]
        act.tool = [nc.text for nc in chunks if nc.text not in act.ingr]

    return actions


def toolFinder(actions):
    for act in actions:
        objects = []
        pobjs = []
        for word in act.doc.noun_chunks:
            
            if word.dep_ in ["dobj","conj"] and word.pos_ == "NOUN":
                objects.append(word.text)
            if word.dep_ == "pobj" and word.text.lower() in ["with","into","in"]:
                pobjs.append(word.text)

#ActionMachine(rec)