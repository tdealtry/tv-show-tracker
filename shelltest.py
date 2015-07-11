#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, json, random, time, signal
import pprint


from difflib import SequenceMatcher

def signal_handler(signal, frame):
    return

signal.signal(signal.SIGINT, signal_handler)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])


def print_logo():
    logo = """LATEIN"""
    print(30 * '-')
    print(logo)
    print(30 * '-')


def print_stats(score_string):
    if score_string == "":
        return
    if score_string.count('2') == len(score_string):
        return 0.0

    percent = float(score_string.count('1')) / float(len(score_string) - score_string.count('2')) * 100
    print(str(percent) + "% richtig"),


def print_scores(score_string):
    if score_string == "":
        return
    i = 1
    for c in score_string:
        if c == "0":
            sys.stdout.write("[-]")
        elif c == "1":
            sys.stdout.write("[X]")
        elif c == "2":
            sys.stdout.write("[?]")
        else:
            sys.stdout.write("[_]")
        if (i % 15) == 0:
            sys.stdout.write("\n\t\t")
        i = i + 1


def print_main_menu():
    print("HAUPTMENÜ")
    print(30 * '-')
    print("1. Verben lernen")
    print("2. Adjektive lernen")
    print("3. Zeiten lernen")
    print("4. Vokabeln lernen")
    print("5. Programm verlassen")
    print(30 * '-')


def main_menu():
    choice = 0;
    try:
        choice = int(input('Was wählst du [1-5] : '))
    except ValueError:
        print("\nLeere Eingabe!")

    if choice == 1:
        return 1
    elif choice == 2:
        return 2
    elif choice == 3:
        return 3
    elif choice == 4:
        return 4
    elif choice == 5:
        return 5
    else:
        return 0


def print_adjektive_lernen_header():
    cls()
    print_logo()
    print("ADEKTIVE LERNEN")
    print(30 * '-')
    print("""Setze die passenden Endungen ein!
Ihren Fortschritt sehen Sie an der SCORE-Leiste.
Wenn Sie die Endung nicht kennen, tippen Sie als Antwort '?' ein, um zum nächsten Adjektiv zu wechseln.
Um das Lernen abzubrechen und zum Hauptmenü zu wechseln, geben Sie "Exit" ein.
Und nun viel Erfolg!""")
    print(30 * '-')


def adjektive_lernen():
    print_adjektive_lernen_header()

    # load adjectives
    with open('adjektive_a.json') as data_file:
        adj = json.load(data_file)

    with open('adjektive_n.json') as data_file:
        nouns = json.load(data_file)

    score = ""
    done = 0
    while done != 1:
        print_adjektive_lernen_header()
        sys.stdout.write("SCORE:\t"),
        print_scores(score)
        sys.stdout.write("\nSTATS:\t"),
        print_stats(score)
        print("")
        print(30 * '-')

        adjectiveid = random.randint(0, len(list(adj)) - 1)
        adjective = list(adj.keys())[adjectiveid]
        adjective_root = adj[adjective]["stamm"]

        nounid = random.randint(0, len(list(nouns)) - 1)
        noun = list(nouns.keys())[nounid]
        nounquestid = random.randint(0, len(list(nouns[noun])) - 1)
        nounquest = list(nouns[noun].keys())[nounquestid]
        ending = nouns[noun][nounquest]

        print("WÖRTER:\t\t" + str(adjective) + " " + str(noun))

        print("GESUCHT:\t" + str(adjective_root) + '__ ' + str(nounquest))

        answer = input('ENDUNG:\t\t' + str(adjective_root) + " ")

        if (answer == "?") or (answer == "?"):
            done = 0
            score += '2'
            print("\nANTWORT:\t" + str(ending))
            print("ALSO:\t" + str(adjective_root) + str(ending) + " " + str(nounquest))
            time.sleep(2)

        elif answer == "EXIT" or answer == "exit":
            return
        else:
            if similar(answer, ending) >= 0.95:
                score += '1'
                print("\nRICHTIG, " + str(adjective_root) + str(ending) + " " + str(nounquest) + "!")
                time.sleep(1)
            else:
                score += '0'
                print("\nFALSCH!")
                print("RICHTIG:\t" + str(ending))
                print("ALSO:\t" + str(adjective_root) + str(ending) + " " + str(nounquest))
                time.sleep(2)


def print_verben_lernen_header():
    cls()
    print_logo()
    print("VERBEN LERNEN")
    print(30 * '-')
    print("""Lernablauf:
Im Folgenden werden Verben in der Grundform und die Valenzen
angezeigt. Ihre Aufgabe ist es, zu dem Verb in dieser Valenz
möglichst viele Übersetzungen zu finden. Ihr Wissen wird sich in der SCORE wiederspiegeln,
negative Zahlen wird es allerdings nicht geben.
Wenn Sie eine Antwort nicht wissen, geben Sie ein '?' ein.
Zum Wechseln ins Hauptmenü, geben Sie bitte "Exit" ein.
Und nun viel Erfolg!""")
    print(30 * '-')


def verben_lernen():
    print_verben_lernen_header()

    # load json file
    with open('verben.json') as data_file:
        verben = json.load(data_file)
    score = ""
    fertig = 0
    while fertig != 1:
        print_verben_lernen_header()
        sys.stdout.write("SCORE:\t\t"),
        print_scores(score)
        sys.stdout.write("\nSTATS:\t\t"),
        print_stats(score)
        print("")
        print(30 * '-')

        wordid = random.randint(0, len(list(verben)) - 1)
        word = list(verben.keys())[wordid]
        valenzid = random.randint(0, len(list(verben[word])) - 1)
        valenz = list(verben[word].keys())[valenzid]

        print("VERB:\t\t" + word)
        if valenz == "translation":
            print("VALENZ:\t\tkeine (einfache Übersetzung)")
        else:
            print("VALENZ:\t\t" + valenz)
        answer = input('ÜBERSETZUNG:\t')
        if answer == "?":
            fertig = 0
            print("\nANTWORT:\t" + list(verben.keys())[wordid])
            score += '2'
            if len(list(verben[word][valenz][0])) == 1:
                print("\nANTWORT:\t" + verben[word][valenz])
                time.sleep(2)
            else:
                sys.stdout.write("\nANTWORT:\t")
                for d in verben[word][valenz]:
                    sys.stdout.write(d + "; ")
                time.sleep(2)
        elif (answer == "EXIT") or (answer == "exit"):
            return
        else:
            if len(list(verben[word][valenz][0])) == 1:  # single translation for a modus
                if similar(answer, verben[word][valenz]) >= 0.89:
                    score += '1'
                    print("\nRICHTIG!")
                    time.sleep(1)
                else:
                    score += '0'
                    print("\nFALSCH!")
                    print("RICHTIG:\t" + verben[word][valenz])
                    time.sleep(2)
            else:
                answer_correct = False
                for ans in verben[word][valenz]:
                    if similar(answer, ans) >= 0.89:
                        score += '1'
                        answer_correct = True
                        break

                if answer_correct == False:
                    score += '0'
                    print("\nFALSCH!")
                    sys.stdout.write("RICHTIG:\t")
                    for d in verben[word][valenz]:
                        sys.stdout.write(d + "; ")
                    time.sleep(2)
                else:
                    print("\nRICHTIG!")
                    time.sleep(1)

def print_vokabeln_lernen_header():
    cls()
    print_logo()
    print("VOKABELN LERNEN")
    print(30 * '-')
    print("""Lernablauf: Bitte geben Sie eine passende Übersetzung ein für die Vokabel, die abgefragt wird.
    Wenn Sie ein Wort nicht wissen, können Sie ein '?' Fragezeichen eintippen.
    Zurück zum Hauptmenü kommen Sie mit der Eingabe 'EXIT'.

Und nun viel Erfolg!""")
    print(30 * '-')


def vokabeln_lernen():
    print_vokabeln_lernen_header()

    with open('vokabeln.json') as data_file:
        vokabeln = json.load(data_file)
    score = ""
    done = 0
    while done != 1:
        print_vokabeln_lernen_header()
        sys.stdout.write("SCORE:\t\t"),
        print_scores(score)
        sys.stdout.write("\nSTATS:\t\t"),
        print_stats(score)
        print("")
        print (30 * '-')

        wordid = random.randint(0, len(list(vokabeln)) - 1)
        word = list(vokabeln.keys())[wordid]
        modeid = random.randint(0, len(list(vokabeln[word])) - 1)
        mode = list(vokabeln[word].keys())[modeid]
        translation_count = len(list(vokabeln[word][mode]))

        print("VOKABEL:\t\t" + word)
        if (mode == "translation"):
            print("ZUSAMMENHANG:\t\tkein (einfache Übersetzung)")
        else:
            print("ZUSAMMENHANG:\t\t" + mode)

        answer = input('ÜBERSETZUNG:\t')

        if ((answer == "?")):
            done = 0
            score += '2'
            if (len(list(vokabeln[word][mode][0])) == 1):
                print("\nANTWORT:\t" + vokabeln[word][mode])
                time.sleep(3)
            else:
                sys.stdout.write("\nANTWORT:\t")
                for d in vokabeln[word][mode]:
                    sys.stdout.write(d + " ")
                time.sleep(3)

        elif ((answer == "EXIT") or (answer == "exit")):
            return
        else:
            if (len(list(vokabeln[word][mode][0])) == 1):  # single translation for a modus
                if (similar(answer, vokabeln[word][mode]) >= 0.89):
                    score += '1'
                    print("\nRICHTIG!")
                    time.sleep(1)
                else:
                    score += '0'
                    print("\nFALSCH!")
                    print("RICHTIG:\t" + vokabeln[word][mode])
                    time.sleep(2)
            else:
                answer_correct = False
                for ans in vokabeln[word][mode]:
                    if (similar(answer, ans) >= 0.89):
                        score += '1'
                        answer_correct = True
                        break

                if (answer_correct == False):
                    score += '0'
                    print("\nFALSCH!")
                    sys.stdout.write("RICHTIG:\t")
                    for d in vokabeln[word][mode]:
                        sys.stdout.write(d + " ")
                    time.sleep(2)
                else:
                    print("\nRICHTIG!")
                    time.sleep(1)


def print_zeiten_lernen_header():
    cls()
    print_logo()
    print("ADEKTIVE LERNEN")
    print (30 * '-')
    print("""Lernablauf:
    Im Folgenden werden Adjektivstämme mit einem bereits deklinierten Nomen angezeigt. Bitte stellen Sie eine KNG-Kongruenz her.
    Falls Sie eine Endung nicht wissen, geben Sie ein '?' ein.
    Wollen Sie die Abfrage beenden, so tippen Sie 'EXIT' ein.
    Und nun viel Erfolg!""")
    print (30 * '-')


def zeiten_lernen():
    tempus = ["Präsens", "Imperfekt", "Perfekt", "Plusquamperfekt", "Fut", "Fut_II"]
    modus = ["Indikativ", "Konjunktiv"]
    person = ["1.", "2.", "3."]
    anzahl = ["Singular", "Plural"]
    diathese = ["Aktiv", "Medium", "Passiv"]

    print_zeiten_lernen_header()

    with open('zeitformen.json') as data_file:
        zeiten = json.load(data_file)
    score = ""
    done = 0
    while (done != 1):

        print_verben_lernen_header()
        sys.stdout.write("SCORE:\t\t"),
        print_scores(score)
        sys.stdout.write("\nSTATS:\t\t"),
        print_stats(score)
        print("")
        print (30 * '-')

        wordid = random.randint(0, len(list(zeiten)) - 1)
        word = list(zeiten.keys())[wordid]

        # print(wordid)
        # print("WORT:\t\t" + word)
        # print(len(verben[word])-1)
        # print(modeid)


        print("GRUNGFORM:\t" + zeiten[word]["grundform"])
        sys.stdout.write("BESTIMME:\t"),
        sys.stdout.write(person[int(zeiten[word]["person"])] + " Person, "),
        sys.stdout.write(anzahl[int(zeiten[word]["anzahl"])] + ", "),
        sys.stdout.write(tempus[int(zeiten[word]["zeit"])] + ", "),
        sys.stdout.write(diathese[int(zeiten[word]["diathese"])] + ", "),
        sys.stdout.write(modus[int(zeiten[word]["modus"])] + "\n")

        answer = input('WORT:\t\t')
        if (answer == "?"):
            done = 0
            score += '2'
            print("RICHTIG:\t" + word)
            time.sleep(2)
        elif (answer == "EXIT") or (answer == "exit"):
            return
        else:
            if (similar(answer, word) >= 0.95):
                score += "1"
                print("RICHTIG!")
                time.sleep(1)
            else:
                score += "0"
                print("FALSCH!")
                print("RICHTIG:\t" + word)
                time.sleep(2)


def main():
    cls()
    lernmodus = 0
    print_logo()
    print_main_menu()

    while (True):
        cls()
        print_logo()
        print_main_menu()
        lernmodus = main_menu()
        if lernmodus == 1:
            verben_lernen()
        elif lernmodus == 2:
            adjektive_lernen()
        elif lernmodus == 3:
            zeiten_lernen()
        elif lernmodus == 4:
            vokabeln_lernen()
        elif lernmodus == 5:
            cls()
            sys.exit()
        else:
            print("extremely bad error")

if __name__ == '__main__':
    main()
