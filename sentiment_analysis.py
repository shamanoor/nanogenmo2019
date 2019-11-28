from ast import literal_eval

import requests


def compute_sentiment(file):
    # CHECK SENTIMENT OF SURROUNDING TEXT, ADD IMAGE WITH MATCHING FACIAL EXPRESSION
    # CHECK WHO SENT THE MESSAGE, THEN CHECK THE SENTIMENT OF THEIR FOLLOWING/PRECEDING MESSAGES
    # THEN ADD IMAGE OF FACE IN THAT EXPRESSION

    missing_media = {}

    f = open(file, 'r', encoding='utf-8')
    for i, line in enumerate(f):
        print(line)
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
            if (i + j) >= 0 and j != 0:
                # store per missing media idx the idxes of the surrounding sentences
                if i in relevant_idx:
                    relevant_idx[i].append(i + j)
                else:
                    relevant_idx[i] = [i + j]

    f = open(file, 'r', encoding='utf-8')
    # extend missing media values with the lines of the speaker that surround the missing media message
    for i, line in enumerate(f):
        substr = line[17:]
        sender = substr[:substr.find(":")]
        for j in relevant_idx:
            if i == j or i in relevant_idx[j] and missing_media[j][0] == sender:
                missing_media[j].append(line[17:])
    f.close()

    sentiment = []
    for i in missing_media:
        # print("sentiment: ", sentiment)
        r = requests.post(
            "https://api.deepai.org/api/sentiment-analysis",
            data={
                'text': missing_media[i][1:len(missing_media[i])],
            },
            headers={'api-key': 'INSERT-YOUR-API-KEY'}
        )
        sentiment.append(r.json())

    with open('sentiments.txt', 'w', encoding='utf-8') as f:
        f.write(str(sentiment))


# compute_sentiment('chronological_generated.txt')
def process_sentiment(file):
    sentiments = []
    with open('sentiments.txt', 'r', encoding='utf-8') as f:
        data = f.read()
        data = literal_eval(data)
        for i in range(len(data)):
            sentiments.append(data[i])

    sender = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if "Media weggelaten" in line:
                substr = line[17:]
                sent = substr[:substr.find(":")]
                sender.append([sent])

    with open('sentiments.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
        content = literal_eval(content)
        for i in range(len(content)):
            item = content[i]
            output = item['output']
            sentiment = output[0]
            sender[i].append(sentiment)

    with open('sentiment_senders.txt', 'w', encoding='utf-8') as f:
        f.write(str(sender))
    f.close()
    return f


def insert_sentiments(file):
    idx = 0
    sender = open('sentiment_senders.txt', 'r', encoding='utf-8').read()
    sender = literal_eval(sender)

    dest = open('generated_copy_sentiments.txt', 'w', encoding='utf-8')
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if "Media weggelaten" in line:
                dest.write(line[:-1] + ' ' + str(sender[idx][1]) + '\n')
                idx += 1
            else:
                dest.write(line)
    dest.close()
    return dest


def remove_missing_media():
    dest = open('generated_copy_without_media.txt', 'w', encoding='utf-8')
    with open('generated_copy.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if "Media weggelaten" in line:
                pass
            else:
                dest.write(line)
    dest.close()
    return dest
