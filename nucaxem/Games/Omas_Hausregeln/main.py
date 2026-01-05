# utf-8
# Omas Hausregeln
# Autoren: Anna Stärke, Louis Thevis
# Benötigt: colorama
# Informationen:
# Man kann immer mit "n" für "Nein" und mit "j" für "Ja"



# alles notwendige importieren
import os
import time
from colorama import init, Fore, Style


# Colorama init
init(autoreset=True)



# funktion um den ganzen bildschirm zu leeren
def bildschirm_leeren():
    os.system('cls' if os.name == 'nt' else 'clear')


# funktion für eine kurze pause
def kurze_pause(sec=1.2):
    time.sleep(sec)




# funktion für den tod
def handle_death():
    for i in range(3):
        bildschirm_leeren()
        print(Fore.RED + Style.BRIGHT + "!!! DU BIST TOT !!!")
        time.sleep(0.35)
        bildschirm_leeren()
        time.sleep(0.25)
    print(Fore.RED + "Das Spiel startet von neuem...")
    time.sleep(1.6)
    return 'restart'






# !!!!!!!!! Entscheidungen
# !!!!!!!!! Entscheidungen
# !!!!!!!!! Entscheidungen




# Erste entscheidung
# In den ICE steigen?
def entscheidung_1_einsteigen():
    while True:
        ans = input("In den ICE nach Naumburg steigen? : ").strip().lower()
        if ans in ("ja","j"):
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print("Schade, du kehrst nach Berlin zurück.")
            kurze_pause(1.8)
            return {"choice":"nein"}
        print("Bitte mit 'ja' oder 'nein' antworten.")





# Zweite Entscheidung
# Oma umarmen?
def entscheidung_2_umarmen():
    while True:
        ans = input("Oma zur Begrüßung umarmen? : ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.GREEN + "Oma freut sich und umarmt dich auch.")
            kurze_pause(1.6)
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print(Fore.YELLOW + "Oma ist traurig, sagt aber trotzdem nett Hallo und erzählt, wie sie dich vermisst hat.")
            kurze_pause(1.6)
            return {"choice":"nein"}
        print("Bitte mit 'ja' oder 'nein' antworten.")





# Dritte Entscheidung
# Essen von Oma nehmen?
def entscheidung_3_essen_nehmen():
    while True:
        ans = input("Essen von Oma nehmen? : ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.GREEN + "Oma freut sich und macht dir etwas zu essen.")
            kurze_pause(1.6)
            return {"choice":"ja","meal_prepared":True}
        if ans in ("nein","n"):
            print(Fore.YELLOW + "Oma guckt ein wenig beleidigt, Cheesecake miaut laut, aber Oma sagt: 'Doch Kind, ich mach dir etwas leckeres'.")
            kurze_pause(1.8)
            return {"choice":"nein","meal_prepared":True}
        print("Bitte mit 'ja' oder 'nein' antworten.")





# Vierte Entscheidung
# Ominöses Essen zu sich nehmen?
def entscheidung_4_ominous_food():
    while True:
        ans = input("Das ominöse Essen zu sich nehmen? : ").strip().lower()
        if ans in ("ja","j"):
            print("Du nimmst einen Bissen. Es schmeckt nicht ganz wie es sollte, aber vorerst merkst du keinen Unterschied.")
            kurze_pause(1.8)
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print("Du nimmst es nicht — die Oma wirft das Essen wütend weg.")
            kurze_pause(1.6)
            return {"choice":"nein"}
        print("Bitte mit 'ja' oder 'nein' antworten.")






# Fünfte Entscheidung
# Die Katze füttern?
def entscheidung_5_katze_fuettern():
    while True:
        ans = input("Fütterst du die Katze? : ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.GREEN + "Die Oma ist glücklich und gibt dir das Katzenfutter. Du fütterst die Katze.")
            kurze_pause(1.6)
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print("Die Oma sagt es sei kein Problem, aber du merkst, dass sie beleidigt ist. Du fütterst die Katze nun selbst.")
            kurze_pause(1.6)
            return {"choice":"nein"}
        print("Bitte mit 'ja' oder 'nein' antworten.")






def entscheidung_6_couch_bleiben():
    while True:
        ans = input("Bleibst du bei der Oma auf der Couch? : ").strip().lower()
        if ans in ("ja","j"):
            print("Du bleibst bei deiner Oma auf der Couch und ihr schaut weiter. Die Katze liegt irgendwann auf ihrem Kratzbaum.")
            kurze_pause(1.6)
            return {"choice":"ja","time_advanced_to":"21:00"}
        if ans in ("nein","n"):
            print("Du gehst ins Gästezimmer, holst Handy und iPad: Kein Internet. Du liest stattdessen dein Lieblingsbuch.")
            kurze_pause(2.2)
            return {"choice":"nein","time_advanced_to":"20:00"}
        print("Bitte mit 'ja' oder 'nein' antworten.")








def entscheidung_7_tuer_oeffnen():
    """Entscheidung 7: Öffnet das Mädchen die Tür (als Kratzen ertönt)?"""
    while True:
        ans = input("Öffnest du die Tür? : ").strip().lower()
        if ans in ("ja","j"):
            print("Draußen steht die Katze und miaut ängstlich. Sie huscht ins Gästezimmer und versteckt sich unter dem Bett.")
            kurze_pause(1.8)
            print("Du gehst in den dunklen Flur, hörst leise Fernseher-Geräusche und spähst durchs Wohnzimmer: Oma sitzt da, sieht kurz sehr seltsam aus, dreht dann den Kopf und lächelt wieder.")
            kurze_pause(2.5)
            return {"choice":"ja","result":"saw_odd_omawatch"}
        if ans in ("nein","n"):
            print("Du öffnest nicht und schläfst irgendwann ängstlich ein.")
            kurze_pause(1.6)
            return {"choice":"nein","result":"slept_fearfully"}
        print("Bitte mit 'ja' oder 'nein' antworten.")








def entscheidung_8_vorhang_ziehen():
    """Entscheidung 8: Vorhang zur Seite ziehen bei Klopfen am Fenster (Nacht 1)."""
    while True:
        ans = input("Entscheidung 8 — Vorhang zur Seite ziehen? (ja/nein): ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.CYAN + "Du siehst aus dem Augenwinkel eine Person, die verpixelt aussieht. Sie verschwindet blitzschnell wieder.")
            kurze_pause(2.0)
            print("Du redest dir ein, dass es Einbildung war, und fällst wieder ängstlich in den Schlaf.")
            kurze_pause(1.4)
            return {"choice":"ja","result":"saw_pixel_person"}
        if ans in ("nein","n"):
            # Escalation -> leads to death sequence in doc
            print("Das Klopfen wird lauter und lauter. Du rennst zur Tür deiner Oma, doch sie ist nicht da. Plötzlich klopft es hinter dir an der Wand. Du drehst dich um...")
            kurze_pause(2.0)
            print(Fore.RED + "Du bist tot.")
            kurze_pause(1.2)
            return {"choice":"nein","result":"death"}
        print("Bitte mit 'ja' oder 'nein' antworten.")








def entscheidung_9_aufstehen():
    """Entscheidung 9: Aufstehen oder nicht? (nächster Morgen)"""
    while True:
        ans = input("Entscheidung 9 — Aufstehen? (auf/nein): ").strip().lower()
        if ans in ("auf","ja","j"):
            print("Du stehst auf, begrüßt deine Oma vorsichtig und sie macht Frühstück. Du gehst duschen, isst, und spielst bis 14:00 Uhr 'Mensch ärgere dich nicht' mit deiner Oma.")
            kurze_pause(2.0)
            return {"choice":"auf"}
        if ans in ("nein","n"):
            print("Du schläfst weiter bis 14:00 Uhr. Die Oma weckt dich sanft. Das Licht flackert kurz, aber du denkst dir nichts dabei.")
            kurze_pause(1.8)
            return {"choice":"nein"}
        print("Bitte mit 'auf' oder 'nein' antworten.")






def entscheidung_10_zeichnungen_fragen():
    """Entscheidung 10: Oma nach den Zeichnungen fragen?"""
    while True:
        ans = input("Entscheidung 10 — Oma nach den Zeichnungen fragen? (ja/nein): ").strip().lower()
        if ans in ("ja","j"):
            print("Die Oma guckt ein wenig komisch und sagt: 'Das wirst du wahrscheinlich selbst noch herausfinden. Vielleicht ist es bald nützlich.'")
            kurze_pause(1.8)
            return {"choice":"ja","hint_received":True}
        if ans in ("nein","n"):
            print("Du fragst nicht weiter. Das Spiel geht weiter...")
            kurze_pause(1.4)
            return {"choice":"nein","hint_received":False}
        print("Bitte mit 'ja' oder 'nein' antworten.")







def entscheidung_11_mit_oma_serie_gucken():
    """Entscheidung 11: Mit Oma Serie gucken?"""
    while True:
        ans = input("Entscheidung 11 — Mit Oma Serie gucken? (ja/nein): ").strip().lower()
        if ans in ("ja","j"):
            print("Du schaust mit Oma die Serie. Es wird schnell 21:00 Uhr.")
            kurze_pause(1.6)
            return {"choice":"ja","time_advanced_to":"21:00"}
        if ans in ("nein","n"):
            print("Du sagst nein — die Oma macht dir etwas zu essen.")
            kurze_pause(1.6)
            return {"choice":"nein","time_advanced_to":"17:00"}
        print("Bitte mit 'ja' oder 'nein' antworten.")








def entscheidung_12_was_essen():
    """Entscheidung 12: Was willst du essen? (freie Antwort)"""
    ans = input("Entscheidung 12 — Was willst du essen? (schreib deine Antwort): ").strip()
    if not ans:
        ans = "etwas"
    print(f"Die Oma macht dir {ans} und ihr esst zusammen. Es schmeckt wieder etwas seltsam, aber du traust dich nicht es anzusprechen.")
    kurze_pause(2.0)
    return {"choice":ans}







def entscheidung_13_wochenende_gefaellt():
    """Entscheidung 13: Gefällt dir das Wochenende bisher?"""
    while True:
        ans = input("Entscheidung 13 — Gefällt dir das Wochenende bisher? (ja/nein): ").strip().lower()
        if ans in ("ja","j"):
            print(Fore.GREEN + "Die Oma lächelt zufrieden und freut sich sichtlich.")
            kurze_pause(1.6)
            return {"choice":"ja"}
        if ans in ("nein","n"):
            print(Fore.RED + "Die Oma ist traurig. (dieser Text rot)")  # gemäß Dokument
            kurze_pause(1.0)
            print(Fore.YELLOW + "Sie sagt trotzdem, sie hoffe, dass es morgen besser wird. Sie starrt dich merkwürdig durchdringend an, ihr Tonfall macht dich unwohl.")
            kurze_pause(2.2)
            return {"choice":"nein"}
        print("Bitte mit 'ja' oder 'nein' antworten.")







def entscheidung_schluessel_suchen():
    """Spezialszene: Zettel gefunden -> Schlüssel suchen (Option 1/2/3)"""
    print("Du hebst den Zettel auf — er zeigt eine grobe Skizze des Hauses.")
    kurze_pause(1.6)
    print("Auf dem Zimmer deiner Oma ist ein kleines Schlüsselsymbol abgebildet. Du solltest zum Zimmer deiner Oma gehen — aber sei leise.")
    kurze_pause(2.0)
    print("Wo könnte der Schlüssel sein?")
    print("1) In ihrer Nachttischschublade")
    print("2) Auf ihrem Schreibtisch")
    print("3) Auf einem Wandschrank")
    while True:
        ans = input("Wähle 1, 2 oder 3: ").strip()
        if ans == "1":
            print("Du öffnest die Nachttischschublade leise und findest den Schlüssel! Sehr gut.")
            kurze_pause(1.4)
            return {"choice":"1","found_key":True}
        if ans == "2":
            print("Du gehst zum Schreibtisch. Als du dich vorbeugst, knarrt der Stuhl — zu spät.")
            kurze_pause(1.0)
            print(Fore.RED + "Die Oma steht plötzlich auf, sieht dich, und du bist tot.")
            kurze_pause(1.0)
            return {"choice":"2","found_key":False,"death":True}
        if ans == "3":
            print("Du untersuchst den Wandschrank. Es wirkt unheimlich. Plötzlich ist da ein Messer in der Hand deiner Oma...")
            kurze_pause(1.0)
            print(Fore.RED + "Du bist tot.")
            kurze_pause(1.0)
            return {"choice":"3","found_key":False,"death":True}
        print("Bitte 1, 2 oder 3 eingeben.")

def entscheidung_verstecken_bei_schritten():
    """Entscheidung: Verstecken wenn Schritte im Flur (nach Testen der Türen)."""
    while True:
        ans = input("Versteckst du dich? (ja/nein): ").strip().lower()
        if ans in ("ja","j"):
            print("Du kriechst schnell unter dein Bett. Die Oma schaut herein, bleibt aber ohne Ergebnis und geht wieder.")
            kurze_pause(1.8)
            print("Du kommst hervor und denkst an die Hintertür. Du wagst es, zur Hintertür zu schleichen.")
            kurze_pause(1.4)
            return {"choice":"ja","result":"hidden_success"}
        if ans in ("nein","n"):
            print(Fore.RED + "Du hörst Schritte näherkommen. Du drehst dich um... Du bist tot. (Dieser Text rot)")
            kurze_pause(1.4)
            return {"choice":"nein","result":"death"}
        print("Bitte mit 'ja' oder 'nein' antworten.")






def szene_hintertuer(found_bag=False):
    """Escape attempt through back door; if bag forgotten, different outcome."""
    if found_bag:
        print("Du öffnest die Hintertür vorsichtig — die Freiheit ist kalt, aber du bist draußen.")
        kurze_pause(1.6)
        print(Fore.GREEN + "Du hast überlebt und bist entkommen! Spielende: Glückliches Ende.")
        kurze_pause(2.2)
        return {"escaped":True}
    else:
        print("Du öffnest die Hintertür — doch du hast deine Tasche vergessen. Was nun?")
        kurze_pause(1.4)
        print("Trotzdem schaffst du es hinaus. Du spürst die Kälte, aber erreichst die Freiheit.")
        kurze_pause(2.0)
        print(Fore.GREEN + "Du hast entkommen! Spielende.")
        kurze_pause(2.0)
        return {"escaped":True}

# Szenenablauf
def spiel_starten():
    """Steuert den kompletten Ablauf. Auf Todesfälle mit 'restart' reagieren."""
    while True:  # loop für Neustarts nach Tod
        bildschirm_leeren()
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
        print("Das Mädchen sitzt im Zug und fährt wie geplant zu ihrer Oma.")
        kurze_pause(1.1)
        print("Sie kommt an, steigt aus dem Zug und läuft das letzte Stück zu ihrer Oma.")
        kurze_pause(1.1)
        print("Sie klingelt, die Oma öffnet. Die Katze Cheesecake springt freudig entgegen.")
        kurze_pause(1.4)




        
        # Entscheidung 2
        res2 = entscheidung_2_umarmen()



        
        # weiter im Haus
        bildschirm_leeren()
        print("Das Mädchen, die Oma und die Katze gehen hinein. Du bringst deine Übernachtungssachen für 3 Nächte ins Gästezimmer.")
        kurze_pause(1.6)
        print("Die Oma fragt, ob du etwas essen oder trinken möchtest nach deiner langen Reise.")
        kurze_pause(1.2)




        
        # Entscheidung 3
        res3 = entscheidung_3_essen_nehmen()





        
        # Entscheidung 4
        res4 = entscheidung_4_ominous_food()
        # Zeitangabe special colour
        print(Fore.CYAN + "Es ist nun 15:00 Uhr.")
        kurze_pause(0.9)
        print("Fütterungszeit für die Katze.")
        kurze_pause(0.9)



        
        # Entscheidung 5
        res5 = entscheidung_5_katze_fuettern()


        
        # 16:00 Uhr Serienzeit
        print(Fore.CYAN + "Es ist jetzt 16:00 Uhr.")
        kurze_pause(0.7)
        print("Du und deine Oma schauen eine Serie. Cheesecake kuschelt sich auf deinen Schoß.")
        kurze_pause(1.2)
        print(Fore.CYAN + "Die Zeit verging schnell, jetzt ist es 19:00 Uhr.")
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
            # not stayed: we are in guests room at 20:00 and hear Kratzen
            print(Fore.CYAN + "Es ist nun 20:00 Uhr.")
            kurze_pause(0.9)
            print("Du liest, als du plötzlich ein lautes Kratzen an der Tür hörst.")
            kurze_pause(0.9)
            res7 = entscheidung_7_tuer_oeffnen()
            if res7["choice"] == "ja":
                # saw odd oma but everything ok -> proceed
                skip_door_event = True
            else:
                skip_door_event = False






        
        # Nacht 1: 3:00 Uhr Klopfen
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
                    continue  # outer while loop -> restart game
        else:
            # if skip_door_event True, it's the 'saw odd' scenario or slept after door event; still may get to next day normally
            print("Du bist wach, aber es bleibt ruhig. Du schläfst wieder ein.")
            kurze_pause(1.0)





        
        # Nächster Morgen
        bildschirm_leeren()
        print(Fore.CYAN + "Nächster Morgen — Es ist 11:00 Uhr.")
        kurze_pause(1.0)
        res9 = entscheidung_9_aufstehen()




        
        print(Fore.CYAN + "Es ist 14:00 Uhr — Mittagessen.")
        kurze_pause(0.9)




        
        # Entscheidung 10: Zeichnungen
        res10 = entscheidung_10_zeichnungen_fragen()




        
        # 15:00 Spaziergang / Serie
        print("Es ist nun 15:00 Uhr. Nach dem Mittagessen willst du spazieren gehen und fragst deine Oma.")
        kurze_pause(1.0)
        print("Sie lacht merkwürdig und sagt trocken: 'nein'. Du findest das komisch, willst aber lieber nichts erzwingen.")
        kurze_pause(1.1)




        
        # Entscheidung 11
        res11 = entscheidung_11_mit_oma_serie_gucken()




        
        # Entscheidung 12: Was essen?
        res12 = entscheidung_12_was_essen()



        
        # 17:00 Uno
        print(Fore.CYAN + "Es ist 17:00 Uhr. Ihr spielt Uno zusammen.")
        kurze_pause(1.0)
        res13 = entscheidung_13_wochenende_gefaellt()




        # Nacht 2 - Unbehagen, Fluchtplan
        print("Nacht 2.")
        kurze_pause(0.8)
        print("Der Blick deiner Oma bleibt dir im Kopf. Das Essen liegt dir schwer im Magen.")
        kurze_pause(1.2)
        print("Du kannst bis 12:00 Uhr nicht schlafen. Du entscheidest, lieber wieder nach Hause zu wollen.")
        kurze_pause(1.4)
        print("Du gehst zur Tür — alles abgeschlossen. Fenster ebenfalls. Du erinnerst dich an den Zettel mit der Haus-Skizze.")
        kurze_pause(1.6)




        
        # Schlüssel-Szene (Entscheidung  in 3 Optionen)
        schluessel_res = entscheidung_schluessel_suchen()
        if schluessel_res.get("death"):
            # immediate death -> restart
            outcome = handle_death()
            if outcome == 'restart':
                continue





        
        if schluessel_res.get("found_key"):
            # Nun testen der Türen: Haustür passt nicht, Fenster passt nicht, Schritte im Flur
            print("Du testest die Haustür: passt nicht.")
            kurze_pause(0.8)
            print("Du testest das Fenster: passt nicht.")
            kurze_pause(0.8)
            print("Plötzlich hörst du Schritte im Flur.")
            kurze_pause(0.9)
            versteck_res = entscheidung_verstecken_bei_schritten()
            if versteck_res["result"] == "death":
                outcome = handle_death()
                if outcome == 'restart':
                    continue
            # falls das verstecken richtig geht
            if versteck_res["result"] == "hidden_success":
                # Hintertür Szene
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
            # fallback falls ein unerwarteter Ablauf passiert.
            print("Du konntest keinen Schlüssel finden. Die Situation wird gefährlich...")
            outcome = handle_death()
            if outcome == 'restart':
                continue




        
        # zweiter fallback falls vorher auch kein richtiges ende kam.
        print("Das Abenteuer ist (vorerst) vorbei. Zurück zum Hauptmenü.")
        kurze_pause(1.6)
        return





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
            print("Ungültige Eingabe. Bitte 1 oder 2 wählen.")
            time.sleep(1.0)


    # zum hauptmenü gehen
    if __name__ == "__main__":
    hauptmenu()
