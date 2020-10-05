from os import listdir, path
from os.path import isfile, join
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import string


def load_dataset():
    _path = './data/data/CORPS_II/'
    files = [f for f in listdir(_path) if isfile(join(_path, f))]
    list_files = []
    for file_name in files:
        rel_path = _path + file_name
        file_path = path.relpath(rel_path)
        reading_stream = open(file_path, "r", encoding="utf8")
        file = reading_stream.read()
        reading_stream.close()
        list_files.append(file)
    return list_files


def format_dataset(data):
    new_dataset = []
    new_speeches = []

    for one_file in data:
        title_result = re.search('{title}(.*){/title}', one_file)
        title = title_result.group(1).strip()

        event_result = re.search('{event}(.*){/event}', one_file)
        event = event_result.group(1).strip()

        speaker_result = re.search('{speaker}(.*){/speaker}', one_file)
        speaker = speaker_result.group(1).strip()

        date_result = re.search('{date}(.*){/date}', one_file)
        date = date_result.group(1).strip()

        source_result = re.search('{source}(.*){/source}', one_file)
        source = source_result.group(1).strip()

        description_result = re.search('{description}(.*){/description}', one_file)
        description = description_result.group(1).strip()

        file_speech = one_file.split('{speech}')[1].replace('{/speech}', '').strip()

        new_dataset.append([title, event, speaker, date, source, description, file_speech])
        new_speeches.append(file_speech)

    return new_dataset, new_speeches


if __name__ == '__main__':

    # reading the dataset
    raw_dataset = load_dataset()

    # formatting the data in rows and column for easier use
    dataset, speeches = format_dataset(raw_dataset)
    columns = ['title', 'event', 'speaker', 'date', 'source', 'description', 'speech']

    # get sentences from text
    speeches_sentences = []
    # words from sentences from speech
    words_speeches = []
    print('sentences')
    count = 0
    labeled_dataset = []
    for i in range(0,len(speeches)):
        result = sent_tokenize(speeches[i])
        label_sentences = []
        for j in range(0,len(result)):
            pair = {}
            if result[j].__contains__('{LAUGHTER}') and j > 0:
                result[j] = result[j].replace('{LAUGHTER}', '')
                label_sentences[j - 1]['label'] = 'laughter'

            if result[j].__contains__('{APPLAUSE}') and j > 0:
                result[j] = result[j].replace('{APPLAUSE}', '')
                label_sentences[j - 1]['label'] = 'applause'

            pair['sentence'] = result[j]
            pair['label'] = 'none'
            pair['speech_number'] = i
            label_sentences.append(pair)

        labeled_dataset.append(label_sentences)

        #speeches_sentences.append(speech_sentences)
        count +=1
        if count == 4:
            break

    # for speech in speeches:
    #    clean_speech = speech.replace('{LAUGHTER}', '').replace('{APPLAUSE}', '')

    #    speech_sentences = sent_tokenize(clean_speech)
    #    speeches_sentences.append(speech_sentences)

    #    word_speech = word_tokenize(clean_speech)
    #    words_speeches.append(word_speech)

    #print('before word cleaning')
    #for speech_in_words in words_speeches:
    #    for word in speech_in_words:
    #        if word in string.punctuation:
    #            speech_in_words.remove(word)
    #print(words_speeches[0])

