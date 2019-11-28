# ADD OLD DATES AND TIMES OF MESSAGES SO IT IS CHRONOLOGICAL, REPLACE REAL NAMES WITH FICTIONAL NAMES

def remove_white_lines(file):
    stripped = open('chat_stripped.txt', 'w', encoding='utf-8')
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if len(line) > 1:
                # print("length of line: ", len(line), "line: ", line)
                stripped.write(line)
    stripped.close()
    return stripped

def replace_names(file):
    # NAMES TO REMOVE:
    # NAMES TO BE REPLACED ARE BLANKED OUT FOR PRIVACY REASONS
    target = open('romeo_juliet.txt', 'w', encoding='utf-8')
    with open(file, 'r+', encoding='utf-8') as f:
        for line in f:
            target.write(line.replace('*', 'Romeo').replace('*', 'Juliet').replace('*', 'Rosaline')
                         .replace('*', 'Benvolio').replace('*', 'Nurse ').replace('*', 'Mercutio')
                         .replace('*', 'Prince Escalus').replace('*', 'Friar John').replace('*', 'Balthasar')
                         .replace('*', 'Capulet'))
    target.close()
    return target


def add_titles_clean_timestamps(timestamps, file):
    day_month = []
    for i in range(len(timestamps)):
        if '-' in timestamps[i][:8] and timestamps[i][:8] not in day_month:
            day_month.append(timestamps[i][:8])

    # ADD DATES AS TITLES IN CHAT
    with_titles = open('clean_chat_titles.txt', 'w', encoding='utf-8')
    idx = 0
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if line[:8] == day_month[idx] and idx < len(day_month) - 1:
                if idx == 0:
                    whitespace = 0
                else:
                    whitespace = 7
                word_list = str.split(line)
                last_word = word_list[-1]
                with_titles.write(whitespace * '<br/>' + '<font fontSize = 14><b>' + day_month[idx] + ' | ' +
                                  last_word.capitalize() + '</b> </font>' + 2 * '<br/>')
                idx += 1
                with_titles.write(line[8:])
            else:
                with_titles.write(line[8:])
    with_titles.close()
    return with_titles


def make_time_chronological(source_file, generated_text):
    with open(source_file, 'r', encoding='utf-8') as f:
        timestamps = []
        for line in f:
            timestamps.append(line[:15])

    dest = open('chronological_generated.txt', 'w', encoding='utf-8')
    with open(generated_text, 'r', encoding='utf-8') as f:
        idx = 0
        for line in f:
            dest.write(timestamps[idx] + line[15:])
            idx += 1
    dest.close()
    return timestamps, dest
