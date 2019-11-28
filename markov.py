import random
from collections import defaultdict, Counter


# full credits to  Eli Bendersky!
# source: https://eli.thegreenplace.net/2018/elegant-python-code-for-a-markov-chain-text-generator/

def generate(file):
    STATE_LEN = 10

    with open(file, 'r', encoding='utf-8') as file:
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
    for i in range(5000):
        out.extend(random.choices(list(model[state]), model[state].values()))
        state = state[1:] + out[-1]
    print("Finished sampling")

    skip_first_line = out.index('\n') + 1
    with open('generated.txt', 'w', encoding='utf-8') as f:
        for line in out[skip_first_line:]:
            f.write(line)
    f.close()
    return f
