import clean_chat
import markov
import reportlab_markov
import sentiment_analysis

chat = clean_chat.remove_white_lines('chat-london.txt')

chat = clean_chat.replace_names(chat.name)

# generate chat WORKS WELL
generated = markov.generate(chat.name)

# make times chronological again WORKS WELL
timestamps, chronological = clean_chat.make_time_chronological('chat.txt', generated.name)

# get sentiments, store in file, prepare everything to be able to insert sentiment pictures
sentiment_analysis.compute_sentiment(chronological.name)
sentiment_senders = sentiment_analysis.process_sentiment(chronological.name)

# add titles
with_titles = clean_chat.add_titles_clean_timestamps(timestamps, chronological.name)

# insert sentiments, needed for image input
final = sentiment_analysis.insert_sentiments(with_titles.name)

# prepare images
reportlab_markov.prepare_images()

# export to pdf, includes replacing sentiments with images
reportlab_markov.generate_pdf(final.name)