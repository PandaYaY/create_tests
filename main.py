import os
import docx
import random


def shuffle(test, cols):
    random.shuffle(test)
    test = test[:cols]
    for i in range(len(test)):
        variants = test[i][2:]
        answers = []
        for g in range(len(test[i][1])):
            answers.append(variants[int(test[i][1][g]) - 1])

        random.shuffle(variants)
        for g in range(len(answers)):
            answers[g] = variants.index(answers[g])  # тут можно убрать '+ 1' из-за бд или индексов

        new_question = [test[i][0], answers]
        new_question.extend(variants)
        test[i] = new_question
    return test


def get_docx_text(path):
    text = []
    doc = docx.Document(path)
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return text


def parsing(path):
    text = get_docx_text(path)

    for _ in range(text.count('')):
        text.remove('')

    questions = []
    question = []
    for i in range(len(text)):
        text[i] = text[i].strip()

        if text[i][text[i].find('.') - 1].isdigit():
            if question:
                questions.append(question)
            question = [text[i][text[i].find('.') + 2:]]
        elif text[i].lower().find('ответ') == 0:
            question.append(text[i][7:].split(', '))
            continue
        else:
            question.append(text[i])
    questions.append(question)
    return questions


def get_paths():
    paths = []  # список адресов файлов
    for root, dirs, files in os.walk(os.getcwd()):
        print(root, dirs, files)
        for file in files:
            if file.endswith('docx') and not file.startswith('~'):
                paths.append(os.path.join(root, file))
    return paths


def get_names():
    paths = get_paths()  # пути к файлам
    names = []
    for path in paths:
        name = path[len(os.getcwd()) + 1: -5]
        names.append(name)
    return names


def main():
    folder = os.getcwd()  # рабочая папка
    os.chdir(folder + '\\tests')  # переход в папку \tests

    paths = get_paths()
    names = get_names()

    print('Выберите тему: ')
    for i in range(len(names)):
        print(f'{i + 1}: {names[i]}')

    # select_theme = int(input('Тема №: ')) - 1
    # cols = int(input('Число вопросов: '))

    select_theme = 0
    cols = 3

    test = parsing(paths[select_theme])
    test = shuffle(test, cols)
    print(test)


main()
