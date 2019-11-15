from collections import defaultdict, Counter
import random

# This is the length of the "state" the current character is predicted from.
# For Markov chains with memory, this is the "order" of the chain. For n-grams,
# n is STATE_LEN+1 since it includes the predicted character as well.
STATE_LEN = 10

with open('chat.txt', 'r', encoding='utf-8') as file:
  data = file.read()

model = defaultdict(Counter)

print('Learning model...')
for i in range(len(data) - STATE_LEN):
    state = data[i:i + STATE_LEN]
    next = data[i + STATE_LEN]
    model[state][next] += 1

print('Sampling...')
state = random.choice(list(model))
out = list(state)
for i in range(250000):
    out.extend(random.choices(list(model[state]), model[state].values()))
    state = state[1:] + out[-1]

with open('generated.txt', 'w', encoding='utf-8') as f:
    for line in out:
        f.write(line)

# list of keywords that exist in the TTI engine:
tti_keywords = []

def add_images():
    # CHECK SENTIMENT OF SURROUNDING TEXT, ADD IMAGE WITH MATCHING FACIAL EXPRESSION
    # CHECK WHO SENT THE MESSAGE, THEN CHECK THE SENTIMENT OF THEIR FOLLOWING/PRECEDING MESSAGES
    # THEN ADD IMAGE OF FACE IN THAT EXPRESSION FROM ARTBREEDER

    missing_media = {}
    f = open('generated.txt', encoding='utf-8')

    for i, line in enumerate(f):
        if "<Media weggelaten>" in line:
            substr = line[17:]
            # store idx and name of sender of media
            missing_media[i] = [substr[:substr.find(":")]]
    f.close()
    print("missing media: ", missing_media)

    # extend missing media indices with 3 lines surrounding it that the sender sent
    relevant_idx = {}
    for i in missing_media:
        for j in range(-2, 3):
            if (i + j) >= 0: # CHECK IF THIS WORKS CORRECTLY, SHOULDN'T GET NEGATIVE INDICES, IS 0 INCLUDED???
                # store per missing media idx the idxes of the surrounding sentences
                if i in relevant_idx:
                    relevant_idx[i].append(i + j)
                else:
                    relevant_idx[i] = [i + j]

    f = open('generated.txt', encoding='utf-8')
    # extend missing media values with the lines of the speaker that surround the missing media message
    for i, line in enumerate(f):
        for j in missing_media:
            for k in range(-2, 3):
                if i == j and (i + k) >= 0: # CHECK IF THIS WORKS CORRECTLY, SHOULDN'T GET NEGATIVE INDICES, IS 0 INCLUDED???
                    missing_media[j].append(line)
    f.close()

    print("new missing media: ", missing_media)

    relevant_lines = []
    f = open('generated.txt', encoding='utf-8')

    for i, line in enumerate(f):
        if i in relevant_idx:
            relevant_idx[i].append(line)
            # print(line)

    for i in missing_media:
        if i in relevant_lines:
            missing_media[i].append()
    print("relevant lines: ", relevant_idx)

add_images()