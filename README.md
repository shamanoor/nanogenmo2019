# nanogenmo2019

This project takes a WhatsApp conversation and generates a new one, making use of a Markov chain. It replaces the name in the chat with character names from Romeo and Juliet (requires user input, not automatically detected), and files in missing media gaps with images of either Romeo or Juliet in the sentiment that was retrieved from the senders' surrounding messages. 

A big thank you to my friends who trusted me with their WhatsApp conversation and were enthusiastic for me to do this project on their chat!

How to use this project:

Add to the root directory your whatsapp chat as a txt file, with the filename 'chat.txt'.
Go to the function replace_names() in class clean_chat and fill in which names you want to replac with which character names.

Go to the class sentiment_analysis and inert your API key to retrieve the sentiments of the surrounding texts. This is needed to be able to exract the sentiments and insert the images. The original chat was in Dutch, so it looks for tags with <Media weggelaten>, which means 'Media left out', and uses those locations to insert the images.
  
It is possibel to run the project without the images, just go to the main class generate_novel and skip the steps that relate to sentiment analysis and image pre-processing, and replace the file name 'file.name' that is inserted in reportlab_markov.generate_pdf(final.name) to 'chronological.name'.
