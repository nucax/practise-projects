# -*- coding: utf-8 -*-
# Projekt: Omas Hausregeln
# Datei: main.py
# Autoren: Anna Stärke, Louis Thevis
# Benötigt: Python 3.10+
# Benötigte Module: colorama





# alles notwendige importieren
import os
import time
from colorama import init, Fore, Style


# Colorama initalisieren
init(autoreset=True)



# funktion um den ganzen bildschirm zu leeren
def bildschirm_leeren():
    os.system('cls' if os.name == 'nt' else 'clear')


# funktion für eine kurze pause
def kurze_pause(sec=1.2): # normal ist also 1.2 sekunden wenn nichts anderes angeben ist
    time.sleep(sec)




# funktion für den tod
def handle_death():
    for i in range(3): # damit es drei mal passiert
        bildschirm_leeren() # damit davor weg gemacht wird
        print(Fore.RED + Style.BRIGHT + "!!! DU BIST TOT !!!") # roter du bist tot text mit !!!
        time.sleep(0.35) # 0,35 sekunden damit man es nur ganz kurz sieht und es "flashy" ist
        bildschirm_leeren() # das auch für den flashy effekt
        time.sleep(0.25) # für den flashy effekt
    print(Fore.RED + "Das Spiel startet von neuem.") # der neustart
    time.sleep(1.6) # pause zwischen dem restart
    return 'restart' # restart zurückbringen



# ans steht für answer und ist die variable die für die antworten benutzt wird

# !!!!!!!!! Entscheidungen
# !!!!!!!!! Entscheidungen
# !!!!!!!!! Entscheidungen
# Man kann immer mit "n" für "Nein" und mit "j" für "Ja"




# Erste entscheidung
# In den ICE steigen?
def entscheidung_1_einsteigen():
    while True: # ERINNERUNG = für alle entscheidungen benutzen
        ans = input("In den ICE nach Naumburg steigen? : ").strip().lower() # ERINNERUNG = für alle inputs anwenden
        if ans in ("ja","j"):
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print("Duu kehrst nach Berlin zurück.")
            kurze_pause(1.8)
            return {"choice":"nein"}
        print("Mit ja oder nein antworten.")





# Zweite Entscheidung
# Oma umarmen?
def entscheidung_2_umarmen():
    while True:
        ans = input("Oma zur Begrüßung umarmen? : ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.GREEN + "Oma freut sich und erzählt wie sie dich vermisst hat..")
            kurze_pause(1.6)
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print(Fore.YELLOW + "Oma wirkt enttäuscht, sagt aber trotzdem nett Hallo zu dir.")
            kurze_pause(1.6)
            return {"choice":"nein"}
        print("Mit ja oder nein antworten.")





# Dritte Entscheidung
# Essen von Oma nehmen?
def entscheidung_3_essen_nehmen():
    while True:
        ans = input("Essen von Oma nehmen? : ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.GREEN + "Oma freut sich und macht dir etwas zu essen.")
            kurze_pause(1.6)
            return {"choice":"ja","meal_prepared":True} #später beachten
        if ans in ("nein","n"):
            print(Fore.YELLOW + "Oma guckt ein wenig beleidigt und Cheesecake miaut laut, aber Oma sagt: Doch Kind ich mach dir etwas leckeres.")
            kurze_pause(1.8)
            return {"choice":"nein","meal_prepared":True}
        print("Mit ja oder nein antworten.")





# Vierte Entscheidung
# Ominöses Essen zu sich nehmen?
def entscheidung_4_ominous_food():
    while True:
        ans = input("Das ominöse Essen zu sich nehmen? : ").strip().lower()
        if ans in ("ja","j"):
            print("Du nimmst einen Bissen. Es schmeckt komisch, aber du sagst nichts.")
            kurze_pause(1.8)
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print("Du nimmst es nicht. Oma wirft das Essen wütend weg.")
            kurze_pause(1.6)
            return {"choice":"nein"}
        print("Mit ja oder nein antworten.")






# Fünfte Entscheidung
# Die Katze füttern?
def entscheidung_5_katze_fuettern():
    while True:
        ans = input("Fütterst du Cheesecake? : ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.GREEN + "Die Oma ist glücklich und gibt dir das Katzenfutter und Du fütterst Cheesecake.")
            kurze_pause(1.6)
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print("Oma sagt das alles gut ist, aber du merkst das sie beleidigt ist.")
            kurze_pause(1.6)
            return {"choice":"nein"}
        print("Mit ja oder nein antworten.")





# Sechste Entscheidung
# auf der Couch bleiben?
def entscheidung_6_couch_bleiben():
    while True:
        ans = input("Bleibst du bei der Oma auf der Couch? : ").strip().lower()
        if ans in ("ja","j"):
            print("Du bleibst bei deiner Oma auf der Couch und ihr schaut weiter. Cheesecake liegt auf ihrem Kratzbaum.")
            kurze_pause(1.6)
            return {"choice":"ja","time_advanced_to":"21:00"} # zeit geht zu 21 uhr
        if ans in ("nein","n"):
            print("Du gehst ins Gästezimmer und holst Handy und iPad raus. Oma hat kein Internet also liest du.")
            kurze_pause(2.2)
            return {"choice":"nein","time_advanced_to":"20:00"} # zeit geht zu 20 uhr
        print("Mit ja oder nein antworten.")







# Siebte Entscheidung
# Tür öffnen
def entscheidung_7_tuer_oeffnen():
    while True: #unendlicher loop
        ans = input("Öffnest du die Tür? : ").strip().lower()
        if ans in ("ja","j"):
            print("Draußen steht die Katze und miaut ängstlich. Sie huscht ins Gästezimmer und versteckt sich unter dem Bett.")
            kurze_pause(1.8)
            print("Du gehst in den dunklen Flur, hörst leise Fernseher-Geräusche und guckst durchs Wohnzimmer: Oma sitzt da, aber sie sieht komisch aus. Sie dreht dann den Kopf und lächelt wieder.")
            kurze_pause(2.5)
            return {"choice":"ja","result":"saw_odd_omawatch"}
        if ans in ("nein","n"):
            print("Du öffnest nicht und schläfst irgendwann ängstlich ein.")
            kurze_pause(1.6)
            return {"choice":"nein","result":"slept_fearfully"}
        print("Mit ja oder nein antworten.")







# Achte Entscheidung
# Vorhang ziehen?
def entscheidung_8_vorhang_ziehen():
    while True: # unendlicher loop
        ans = input("Vorhang zur Seite ziehen? : ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.CYAN + "Du siehst aus dem Augenwinkel eine Person, die verpixelt aussieht. Sie verschwindet blitzschnell wieder.")
            kurze_pause(2.5) # pause verlängert, damit man es besser lesen kann.
            print("Du redest dir ein, dass es Einbildung war, und fällst wieder ängstlich in den Schlaf.")
            kurze_pause(1.6)
            return {"choice":"ja","result":"saw_pixel_person"}
        if ans in ("nein","n"):
            print("Das Klopfen wird lauter und lauter. Du rennst zur Tür deiner Oma doch sie ist nicht da. Plötzlich klopft es hinter dir an der Wand. Du drehst dich um...")
            kurze_pause(3.0) # pause nochmal verlängert, damit man es besser lesen kann.
            print(Fore.RED + "Du bist tot.")
            kurze_pause(1.2)
            return {"choice":"nein","result":"death"} # geh zu handledeath
        print("Mit ja oder nein antworten.")







# Neunte Entscheidung
# aufstehen??
def entscheidung_9_aufstehen():
    while True: # unendlicher loop
        ans = input("Aufstehen? : ").strip().lower()
        if ans in ("ja","j"):
            print("Du stehst auf, begrüßt deine Oma und sie macht Frühstück. Du gehst duschen, isst, und spielst bis 14 Uhr 'Mensch ärgere dich nicht' mit deiner Oma.")
            kurze_pause(2.0)
            return {"choice":"auf"}
        if ans in ("nein","n"):
            print("Du schläfst weiter bis 14:00 Uhr. Die Oma weckt dich sanft. Das Licht flackert kurz, aber du denkst dir nichts dabei.")
            kurze_pause(1.8)
            return {"choice":"nein"}
        print("Mit ja oder nein antworten.")





# Zehnte entscheidung
# Nach zeichnungen fragen?
def entscheidung_10_zeichnungen_fragen():
    while True:
        ans = input("Oma nach den Zeichnungen an der Wand fragen? : ").strip().lower()
        if ans in ("ja","j"):
            print("Die Oma guckt ein wenig komisch und sagt: Das wirst du wahrscheinlich selbst noch herausfinden.")
            kurze_pause(1.8)
            return {"choice":"ja","hint_received":True} # so das einem später hilft
        if ans in ("nein","n"):
            print("Du fragst nicht.")
            kurze_pause(1.4)
            return {"choice":"nein","hint_received":False} # man hat den hinweis nicht bekommen
        print("Mit ja oder nein antworten.")






# 11. entscheidung
# serie mitgucken?
def entscheidung_11_mit_oma_serie_gucken():
    while True:
        ans = input("Mit Oma Serie gucken? : ").strip().lower()
        if ans in ("ja","j"):
            print("Du schaust mit Oma die Serie. Es wird schnell 21:00 Uhr.")
            kurze_pause(1.6)
            return {"choice":"ja","time_advanced_to":"21:00"}
        if ans in ("nein","n"):
            print("Du sagst nein — die Oma macht dir etwas zu essen.")
            kurze_pause(1.6)
            return {"choice":"nein","time_advanced_to":"17:00"}
        print("Mit ja oder nein antworten.")







# 12. Entscheidung
# custom essen frage (was willst du essen?)
def entscheidung_12_was_essen():
    ans = input("Was willst du essen? : ").strip()
    if not ans:
        ans = "etwas" # zur sicherheit falls der user den input leer lässt
    print(f"Die Oma macht dir {ans} und ihr esst zusammen. Es schmeckt wieder etwas seltsam aber du traust dich nicht es anzusprechen.")
    kurze_pause(2.0)
    return {"choice":ans}






# 13. Entscheidung
# gefällt dir das wochende?
def entscheidung_13_wochenende_gefaellt():
    while True:
        ans = input("Gefällt dir das Wochenende bisher? : ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.GREEN + "Die Oma lächelt zufrieden und freut sich.")
            kurze_pause(1.6)
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print(Fore.RED + "Die Oma ist traurig.")
            kurze_pause(1.0)
            print(Fore.YELLOW + "Sie starrt dich merkwürdig durchdringend an.")
            kurze_pause(2.2)
            print(Fore.YELLOW + "Der Ton ihrer Stimme lässt dich unwohl fühlen")
            return {"choice":"nein"}
        print("Mit ja oder nein antworten.")






# schlüssel suchen. es ist random, weil man vorher keine hints bekommen hat
# 1: richtig
# 2: tot
# 3: tot
def entscheidung_schluessel_suchen():
    print("Du hebst den Zettel auf. Der Zettel zeigt eine grobe Skizze des Hauses.")
    kurze_pause(2.0)
    print("Auf dem Zimmer deiner Oma ist ein kleines Schlüsselsymbol abgebildet. Du solltest zum Zimmer deiner Oma gehen, aber sei leise.")
    kurze_pause(3.0)
    print("Wo könnte der Schlüssel sein?")
    print("1: In ihrer Nachttischschublade")
    print("2: Auf ihrem Schreibtisch")
    print("3: Auf einem Wandschrank")
    while True:
        ans = input("Wähle 1, 2 oder 3: ").strip()
        if ans == "1":
            # schlüssel gefunden
            print("Du öffnest die Nachttischschublade leise und findest den Schlüssel! Sehr gut.")
            kurze_pause(1.4)
            return {"choice":"1","found_key":True}
        if ans == "2":
            # schlüssel nicht gefunden und death returned
            print("Du gehst zum Schreibtisch. Als du dich vorbeugst, knarrt der Stuhl — zu spät.")
            kurze_pause(1.0)
            print(Fore.RED + "Die Oma steht plötzlich auf, sieht dich, und du bist tot.")
            kurze_pause(1.0)
            return {"choice":"2","found_key":False,"death":True} # tot
        if ans == "3":
            # schlüssel nicht gefunden und death returned
            print("Du untersuchst den Wandschrank. Du siehst keinen Schlüssel.. und dann siehst im Schatten deine Oma mit einem Messer in der Hand..")
            kurze_pause(2.0)
            print(Fore.RED + "Du bist tot.")
            kurze_pause(1.0)
            return {"choice":"3","found_key":False,"death":True}  # tot 
        print("Mit ja oder nein antworten.")


# Verstecken nachdem man Schritte gehört hat?
def entscheidung_verstecken_bei_schritten():
    while True:
        ans = input("Versteckst du dich?: ").strip().lower()
        if ans in ("ja","j"):
            print("Du kriechst schnell unter dein Bett. Die Oma schaut herein, aber sieht dich nicht.")
            kurze_pause(2.0) # 0.2 sekunden länger
            print("Du kommst hervor und denkst an die Hintertür. Du gehst langsam zur Hintertür.")
            kurze_pause(2.0) # auch 0.2 sekunden länger
            return {"choice":"ja","result":"hidden_success"}
        if ans in ("nein","n"):
            print(Fore.RED + "Du hörst Schritte näherkommen. Du drehst dich um...") # eigentlich sollte in diesem print der tot revealed werden, aber für den flashy effekt in handledeath, habe ich es rausgenommen
            kurze_pause(1.4)
            return {"choice":"nein","result":"death"} # rip
        print("Mit ja oder nein antworten.")





# Enden 
def szene_hintertuer(found_bag=False):
    if found_bag:
        # Gutes (ein bisschen besseres) ende
        print("Du öffnest die Hintertür vorsichtig. Es ist sehr kalt, aber du bist draußen.")
        kurze_pause(1.6)
        print(Fore.GREEN + "Du hast deine Tasche und bist entkommen! Spielende: Glückliches Ende.")
        kurze_pause(4.0)
        return {"escaped":True}
    else:
        # Normales ende
        print("Du öffnest die Hintertür.. doch du hast deine Tasche vergessen.")
        kurze_pause(1.4)
        print("Trotzdem schaffst du es hinaus. Du spürst die Kälte aber erreichst die Freiheit.")
        kurze_pause(2.0)
        print(Fore.GREEN + "Du bist entkommen.. Spielende.")
        kurze_pause(3.0)
        return {"escaped":True}

# Szenenablauf für den neustart nach dem tot mit dem ascii art
def spiel_starten():
    while True:  # loop für Neustarts nach Tod
        bildschirm_leeren() # WICHTIG
        print("   ___                  _  _                               _ ")
        print("  / _ \\ _ __  __ _ ___ | || |__ _ _  _ ____ _ ___ __ _ ___| |_ _  ")
        print(" | (_) | '  \\/ _` (_-< | __ / _` | || (_-< '_/ -_) _` / -_) | ' \\ ")
        print("  \\___/|_|_|_\\__,_/__/ |_||_\\__,_|\\_,_/__/_| \\___\\__, \\___|_|_||_|")
        print("                                                 |___/            ")
        print("\nDas Abenteuer beginnt...\n")
        kurze_pause(1.0)





        
        # Szene 1
        print("Du bist ein vierzehnjähriges Mädchen aus Berlin, und du willst deine Oma in Naumburg besuchen.")
        kurze_pause(1.2)
        res1 = entscheidung_1_einsteigen()
        if res1["choice"] == "nein":
            # erste entscheidung nein als antwort gegeben
            kurze_pause(1.2)
            print("Du kehrst nach Berlin zurück. Spiel wird beendet.")
            kurze_pause(1.6)
            return


        
        bildschirm_leeren()
        print("Du sitzt im Zug und fährst wie geplant zu deiner Oma.")
        kurze_pause(1.1)
        print("Du kommst an, steigst aus dem Zug und läufst das letzte Stück zu deiner Oma.")
        kurze_pause(1.1)
        print("Du klingelst, die Oma öffnet. Ihre Katze Cheesecake springt freudig entgegen.")
        kurze_pause(1.4)




        
        # Entscheidung 2
        res2 = entscheidung_2_umarmen()



        
        # weiter im Haus
        bildschirm_leeren() # noch hinzugefügt, damit es übersichtlicher ist!
        print("Das Mädchen und die Oma und die Katze gehen hinein. Du bringst deine Übernachtungssachen für 3 Nächte ins Gästezimmer..")
        kurze_pause(1.6)
        print("Oma fragt, ob du etwas essen oder trinken möchtest.")
        kurze_pause(1.2)




        
        # Entscheidung 3
        res3 = entscheidung_3_essen_nehmen()





        
        # Entscheidung 4
        res4 = entscheidung_4_ominous_food()
        print(Fore.CYAN + "Es ist nun 15:00 Uhr.")
        kurze_pause(0.9)
        print("Fütterungszeit für Cheesecake.")
        kurze_pause(0.9)



        
        # Entscheidung 5
        res5 = entscheidung_5_katze_fuettern()


        
        # 16:00 Uhr Serienzeit
        print(Fore.CYAN + "Es ist jetzt 16:00 Uhr.")
        kurze_pause(0.7)
        print("Du und deine Oma schauen eine Serie. Cheesecake kuschelt sich auf deinen Schoß.")
        kurze_pause(1.2)
        print(Fore.CYAN + "Die Zeit verging schnell. Jetzt ist es 19:00 Uhr.")
        kurze_pause(1.2)





        
        # Entscheidung 6
        res6 = entscheidung_6_couch_bleiben()





        
        if res6["choice"] == "ja":
            bildschirm_leeren()
            print(Fore.CYAN + "Es wird schnell 21:00 Uhr.")
            kurze_pause(1.0)
            # Mädchen geht schlafen
            print("Du gehst schlafen.")
            kurze_pause(1.0)
            skip_door_event = True
        else:
            # nicht geblieben
            print(Fore.CYAN + "Es ist nun 20:00 Uhr.")
            kurze_pause(0.9)
            print("Du liest, als du plötzlich ein lautes Kratzen an der Tür hörst.")
            kurze_pause(0.9)
            res7 = entscheidung_7_tuer_oeffnen()
            if res7["choice"] == "ja":
                # saw odd oma
                skip_door_event = True # geh nicht zum door event
            else:
                skip_door_event = False # geh zum door event






        
        # Nacht 1 um  3:00 Uhr Klopfen
        print(Fore.CYAN + "Nacht 1 — Es ist 3:00 Uhr mitten in der Nacht.")
        kurze_pause(1.0)
        print("Du hörst ein Klopfen an deinem Fenster.")
        kurze_pause(0.8)

        if not skip_door_event:
            res8 = entscheidung_8_vorhang_ziehen()
            if res8.get("result") == "death":
                # death -> restart
                outcome = handle_death()
                if outcome == 'restart':
                    continue  # Alles Weitere überspringen und von vorne anfangen basically
        else:
            # Wenn skip_door_event auf True gesetzt ist, geh normal zum nächstem tag
            kurze_pause(1.0)





        
        # Nächster Morgen
        bildschirm_leeren()
        print(Fore.CYAN + "Nächster Morgen. Es ist 11:00 Uhr.")
        kurze_pause(1.0)
        res9 = entscheidung_9_aufstehen()




        
        print(Fore.CYAN + "Es ist 14:00 Uhr. Mittagessen.")
        kurze_pause(0.9)




        
        # Entscheidung 10: Zeichnungen
        res10 = entscheidung_10_zeichnungen_fragen()




        
        # 15:00 Spaziergang / Serie
        print("Es ist nun 15:00 Uhr. Nach dem Mittagessen fragst du deine Oma ob sie lust hat spatzieren zu gehen..")
        kurze_pause(1.0)
        print("Sie lacht merkwürdig und sagt trocken nein. Du findest das komisch. Willst aber nichts sagen.")
        kurze_pause(1.1)




        
        # Entscheidung 11
        res11 = entscheidung_11_mit_oma_serie_gucken()




        
        # Entscheidung 12: Was essen?
        res12 = entscheidung_12_was_essen()



        
        # 17:00 Uno mit Oma
        print(Fore.CYAN + "Es ist 17:00 Uhr. Ihr spielt Uno zusammen.")
        kurze_pause(1.0)
        res13 = entscheidung_13_wochenende_gefaellt()




        # Nacht 2. Unbehagen und Fluchtplan hier
        print("Nacht 2.")
        kurze_pause(0.8)
        print("Der Blick deiner Oma bleibt dir im Kopf. Das Essen liegt dir schwer im Magen.")
        kurze_pause(1.2)
        print("Du kannst bis 12:00 Uhr nicht schlafen. Du entscheidest, lieber wieder nach Hause zu wollen.")
        kurze_pause(1.4)
        print("Du gehst zur Tür — alles abgeschlossen. Fenster ebenfalls. Du erinnerst dich an den Zettel mit der Haus-Skizze.")
        kurze_pause(1.6)




        
        # Schlüssel Szene
        schluessel_res = entscheidung_schluessel_suchen()
        if schluessel_res.get("death"):
            # tod
            outcome = handle_death()
            if outcome == 'restart':
                continue





        
        if schluessel_res.get("found_key"):
            # testen der Türen usw
            print("Du testest die Haustür: passt nicht.")
            kurze_pause(0.8)
            print("Du testest das Fenster: passt nicht.")
            kurze_pause(0.8)
            print("Plötzlich hörst du Schritte im Flur.")
            kurze_pause(0.9)
            versteck_res = entscheidung_verstecken_bei_schritten()
            if versteck_res["result"] == "death":
                outcome = handle_death() # gestorben
                if outcome == 'restart':
                    continue
            # falls das verstecken richtig geht
            if versteck_res["result"] == "hidden_success":
                # Hintertür szene
                # fragen ob der user die tasche vergessen hat damit es noch interaktiver ist
                while True:
                    bag_ans = input("Hast du deine Tasche dabei? (ja/nein): ").strip().lower()
                    if bag_ans in ("ja","j"):
                        escape_res = szene_hintertuer(found_bag=True)
                        break
                    if bag_ans in ("nein","n"):
                        escape_res = szene_hintertuer(found_bag=False)
                        break
                    print("Bitte mit 'ja' oder 'nein' antworten.")
                if escape_res.get("escaped"):
                    print(Fore.GREEN + "Glückwunsch — du konntest entkommen.")
                    kurze_pause(2.0)
                    print("ENDE — Du hast das Spiel abgeschlossen.")
                    kurze_pause(2.0)
                    return
        else:
            # fallback falls ein unerwarteter Ablauf kommt.
            # !!!ZUR SICHERHEIT
            print("Du konntest keinen Schlüssel finden. Die Situation wird gefährlich...")
            outcome = handle_death()
            if outcome == 'restart':
                continue




        
        # zweiter fallback falls vorher auch kein richtiges ende kam.
        # !!!ZUR SICHERHEIT
        print("Das Abenteuer ist (vorerst) vorbei. Zurück zum Hauptmenü.")
        kurze_pause(1.6)
        return  # ende





# Hauptmenü
def hauptmenu():
    while True:
        bildschirm_leeren()
        # ascii art im hauptmenü
        print("   ___                  _  _                               _ ")
        print("  / _ \\ _ __  __ _ ___ | || |__ _ _  _ ____ _ ___ __ _ ___| |_ _  ")
        print(" | (_) | '  \\/ _` (_-< | __ / _` | || (_-< '_/ -_) _` / -_) | ' \\ ")
        print("  \\___/|_|_|_\\__,_/__/ |_||_\\__,_|\\_,_/__/_| \\___\\__, \\___|_|_||_|")
        print("                                                 |___/            ")
        print("\n1. Neues Spiel")
        print("2. Beenden")
        w = input("Auswahl: ").strip()
        if w == "1":
            spiel_starten()
        elif w == "2":
            print("Spiel wird beendet.")
            time.sleep(0.6)
            break
        else:
            print("Mit ja oder nein antworten.")
            time.sleep(1.0)


# zum hauptmenü gehen
hauptmenu()
