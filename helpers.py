import random

def choiceCard(collection):
    tagss = [i[1] for i in collection]
    index = random.randint(0, len(collection)-1)
    card = collection[index]
    tagss.pop(index)
    goodTags = []
    for tag in card[1].split():
        if tag not in ' '.join(tagss):
            goodTags.append(tag)

    print(card[1], goodTags)

    if len(goodTags) == 0:
        goodTags.append(card[1].split()[0])

    return dict(card=card, tag=goodTags[0], ans = index+1)