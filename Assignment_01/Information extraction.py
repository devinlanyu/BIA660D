from __future__ import print_function
import re
import spacy

from pyclausie import ClausIE


nlp = spacy.load('en')
re_spaces = re.compile(r'\s+')


class Person(object):
    def __init__(self, name, likes=None, has=None, travels=None):
        """
        :param name: the person's name
        :type name: basestring
        :param likes: (Optional) an initial list of likes
        :type likes: list
        :param dislikes: (Optional) an initial list of likes
        :type dislikes: list
        :param has: (Optional) an initial list of things the person has
        :type has: list
        :param travels: (Optional) an initial list of the person's travels
        :type travels: list
        """
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.travels = [] if travels is None else travels

    def __repr__(self):
        return self.name


class Pet(object):
    def __init__(self, pet_type, owner, name=None):
        self.name = name
        self.type = pet_type
        self.owner = owner


class Trip(object):
    def __init__(self, date, traveller, place):
        self.time = date
        self.traveller = traveller
        self.place = place



persons = []
pets = []
trips = []
root = None

def get_data_from_file(file_path='/Users/yulanyu/Downloads/BIA660D-master/Lecture_03/assignment_01_data.txt'):
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if not line.startswith(('$$$', '###', '==='))]

    return cleaned_lines


def select_person(name):
    for person in persons:
        if person.name == name:
            return person


def add_person(name):
    person = select_person(name)

    if person is None:
        new_person = Person(name)
        persons.append(new_person)

        return new_person

    return person


def select_pet(name):
    for pet in pets:
        if pet.name == name:
            return pet


def add_pet(type, owner, name=None):
    pet = None

    if name:
        pet = select_pet(name)

    if pet is None:
        pet = Pet(type, name)
        pets.append(pet)

    return pet


def get_persons_pet(person_name):

    person = select_person(person_name)

    for thing in person.has:
        if isinstance(thing, Pet):
            return thing


def select_place(place):
    for where in trips:
        if where.place == place :
            return where

def add_place(date,traveller,place):
    where = select_place(place)

    if  where is None:
        new_trip = Trip(date, traveller,place)
        trips.append(new_trip)
        return new_trip
    return where

def get_place (place):
    places = select_place(place)

    for places in trips:
        if isinstance(places,Trip):
            return places


def process_relation_triplet(triplet):
    """
    Process a relation triplet found by ClausIE and store the data

    find relations of types:
    (PERSON, likes, PERSON)
    (PERSON, has, PET)
    (PET, has_name, NAME)
    (PERSON, travels, TRIP)
    (TRIP, departs_on, DATE)
    (TRIP, departs_to, PLACE)

    :param triplet: The relation triplet from ClausIE
    :type triplet: tuple
    :return: a triplet in the formats specified above
    :rtype: tuple
    """

    sentence = triplet.subject + ' ' + triplet.predicate + ' ' + triplet.object

    doc = nlp(unicode(sentence))
    x=1
    root='apply'
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t
            x=0
        # elif t.pos_ == 'NOUN'

    # also, if only one sentence
    # root = doc[:].root
    if x:
        root = doc[0]

    """
    CURRENT ASSUMPTIONS:
    - People's names are unique (i.e. there only exists one person with a certain name).
    - Pet's names are unique
    - The only pets are dogs and cats
    - Only one person can own a specific pet
    - A person can own only one pet
    """


    # Process (PERSON, likes, PERSON) relations
    if root.lemma_ == 'like' and 'does' not in triplet.predicate:
        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and triplet.object in [e.text for e in doc.ents if e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(triplet.object)
            s.likes.append(o)

    if root.lemma_ == 'be' and triplet.object.startswith('friends with'):
        fw_doc = nlp(unicode(triplet.object))
        with_token = [t for t in fw_doc if t.text == 'with'][0]
        fw_who = [t for t in with_token.children if t.dep_ == 'pobj'][0].text

        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and fw_who in [e.text for e in doc.ents if e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(fw_who)
            s.likes.append(o)
            o.likes.append(s)


    # Process (PERSON, has, Pets, named)
    if root.lemma_ == 'have' and ('dog' in triplet.object or 'cat' in triplet.object):
        if 'named' in triplet.object:

            for e in doc.ents:
                if e.label_ == 'PERSON':
                    x = add_person(triplet.subject)
                    n = triplet.object.find('named')
                    pet_name = triplet.object[n + 6:]
                if x.has:
                    if x.has[0].name:
                        x = 0
                    else:
                        x.has[0].name = pet_name
                else:
                    x_pet_type = 'dog' if 'dog' in triplet.object else 'cat'
                    pet = add_pet(x_pet_type, x, pet_name)
                    x.has.append(pet)
        else:
            for e in doc.ents:
                if e.label_ == 'PERSON':
                    x = add_person(e.text)
                    #print(x)
                    x_pet_type = 'dog' if 'dog' in triplet.object else 'cat'
                    pet = add_pet(x_pet_type, x)
                    print(pet)
                    x.has.append(pet)


    # Process (PET, has, NAME)
    if triplet.subject.endswith('name') and ('dog' in triplet.subject or 'cat' in triplet.subject):
        obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))

        # handle single names, but what about compound names? Noun chunks might help.
        if len(obj_span) == 1 and obj_span[0].pos_ == 'PROPN':
            name = triplet.object
            subj_start = sentence.find(triplet.subject)
            subj_doc = doc.char_span(subj_start, subj_start + len(triplet.subject))

            s_people = [token.text for token in subj_doc if token.ent_type_ == 'PERSON']
            assert len(s_people) == 1
            s_person = select_person(s_people[0])

            s_pet_type = 'dog' if 'dog' in triplet.subject else 'cat'

            pet = add_pet(s_pet_type, name)

            s_person.has.append(pet)


    if [e.text for e in doc.ents if e.label_ == 'GPE']:
            personname = [e.text for e in doc.ents if e.label_ == 'PERSON' or e.label_ == 'ORG']
            date = [str(e.text) for e in doc.ents if e.label_ == 'DATE']
            place = [str(e.text) for e in doc.ents if e.label_ == 'GPE']
            for person in personname:
                s = add_person(person)
                o = add_place(date, s.name, place)
                s.travels.append(o)


def preprocess_question(question):
    # remove articles: a, an, the

    q_words = question.split(' ')

    # when won't this work?
    for article in ('a', 'an', 'the'):
        try:
            q_words.remove(article)
        except:
            pass

    return re.sub(re_spaces, ' ', ' '.join(q_words))


def has_question_word(string):
    # note: there are other question words
    for qword in ('who', 'what'):
        if qword in string.lower():
            return True

    return False

def answer_question():
    answer = 'answer'
    return answer


def main():
    sents = get_data_from_file()

    cl = ClausIE.get_instance()

    triples = cl.extract_triples(sents)

    for t in triples:
        r = process_relation_triplet(t)
        # print(r)
    print(trips)
    question = ' '
    while question[-1] != '?':
        question = raw_input("Please enter your question: ")

        if question[-1] != '?':
            print('This is not a question... please try again')
    answer_question(question)

def answer_question(question_string):
    cl = ClausIE.get_instance()



    # Q1: Who has a <pet_type>? (e.g. Who has a dog?)
    q_trip = cl.extract_triples([preprocess_question(question_string)])[0]
    sentence = q_trip.subject + ' ' + q_trip.predicate + ' ' + q_trip.object

    doc = nlp(unicode(sentence))
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t

    if q_trip.subject.lower() == 'who' and ('dog' in q_trip.object or 'cat' in q_trip.object):

        answer = '{} has a {}.'

        pet_type = 'dog' if 'dog' in q_trip.object else 'cat'
        for person in persons:
            pet = get_persons_pet(person.name)
            if pet:
                if pet.type == pet_type:
                    print(answer.format(person.name, pet_type, pet.name))

    # Q2: Who is [going to|flying to|traveling to] <place>? (e.g. Who is flying to Japan?)
    if q_trip.subject.lower() == 'who' and (root.lemma_ == 'go' or root.lemma_ =='fly' or root.lemma_ =='travel'):
        answer = '{} is going to {}'

        place_doc = nlp(unicode(q_trip.object))
        for e in place_doc.ents:
            if e.label_ == 'GPE':
                place = e.text
                # print(place)
                for where in trips:
                    # print(where.place)
                    if  where.place[0] == place:
                        # a = get_place(where)
                        print(answer.format(where.traveller,where.place[0] ))

    # Q3: Does <person> like <person>? (e.g. Does Bob like Sally?)
    if 'does' in q_trip.subject.lower() and 'like' in sentence:
        list = [e.text for e in doc.ents if e.label_ == 'PERSON']
        person_sub = list[0]
        person_obj = list[1]
        x = 0
        for person in persons:
            if person.name == person_sub:
                for person1 in person.likes:
                    if person1.name == person_obj:
                        x = 1
        if x:
            print("Yes.")
        else:
            print("No")

    # Q4: When is <person> [going to|flying to|traveling to] <place>?
    if 'when' in sentence.lower() and (root.lemma_ == 'go' or root.lemma_ =='fly' or root.lemma_ =='travel'):
        answer="{} is going to {} in {}."
        personD = [e.text for e in doc.ents if e.label_ == 'PERSON' or (e.label_ == 'ORG')][0]
        for e in doc.ents:
            if e.label_ == 'GPE':
                place = e.text
                # print(place)
        for where in trips:
            # print(where.place[0])
            # print(where.traveller)
            if where.place[0]==place and where.traveller==personD:
                print(answer.format(where.traveller,where.place[0],where.time[0]))

    # 5) Who likes <person>?
    if 'who' in q_trip.subject.lower() and root.lemma_ == 'like':
        qdoc=nlp(unicode(sentence))
        personB = [e.text for e in qdoc.ents if e.label_ == 'PERSON'][0]
        for person in persons:
            for personC in person.likes:
                if personC.name == personB:
                    print(person)

    # 6) Who does <person> like?
    if 'does' in q_trip.predicate.lower() and root.lemma_ == 'like':
        qdoc=nlp(unicode(sentence))
        personD = [e.text for e in qdoc.ents if e.label_ == 'PERSON' or (e.label_ == 'ORG') ][0]
        m = add_person(personD)
        for person in m.likes:
                    print(person)


if __name__ == '__main__':
    main()