import numpy as np
import time

start_time = time.time()  
SEED = np.random.seed(42)



def hand_berechnen(hand):
    '''
    Die Hand berechnen
    Input: Hand
    Output: Wert der Hand
    '''
    wert = 0
    asse = 0

    #Generelle Berechnung
    for karte in hand:
        if karte in ['K', 'Q', 'J']:
            wert+= 10
        elif karte == 'A':
            asse += 1
            wert += 11
        else:
            wert += int(karte)
    
    #Für Asse nachjustieren
    while wert > 21 and asse != 0:
        wert -= 10
        asse -= 1
    
    return wert



def deck_erstellen(decks):
    '''
    Deck erstellen
    Input: Deckanzahl
    Output: Gemischtes Deck
    '''
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = ranks * 4 * decks
    np.random.shuffle(deck)  
    return deck



def karte_austeilen(deck):
    '''
    Karte aus Deckziehen
    Input: Deck
    Output: gezogene Karte, restliches Deck
    '''
    karten = []
    m = deck.pop()
    karten.append(m)
    return m, deck



def berechne_zuverlaessigkeit(eigene_hand, zaehlweise, bisherige_karten, uebrige_karten):
    '''
    Wie sicher kommen gute Karten?
    Input: eigene Hand, Zaehlweise, Kartenhistorie aller Spieler, Anzahl übriger Karten
    Output: Zuverlässigkeits-Score
    '''

    if zaehlweise == 'groß&klein':
        #Zaehlweise Niedrige und Hohe Karten zaehlen
        niedriege_karten = 0
        hohe_karten = 0
        for karte in bisherige_karten:
            if karte in ['K', 'Q', 'J', '9', '10', 'A']:
                hohe_karten += 1
            elif karte in ['2', '3', '4', '5', '6', '7']:
                niedriege_karten += 1

        #Schätzen welche Karte nötig
        gebrauchte_karte = 21 - hand_berechnen(eigene_hand)

        if gebrauchte_karte == 0:
            return 0
        elif gebrauchte_karte == 8:
            return 1
        elif gebrauchte_karte < 8 and niedriege_karten+2 <= hohe_karten:
            return 4
        elif gebrauchte_karte < 8 and niedriege_karten+1 <= hohe_karten:
            return 3
        elif gebrauchte_karte < 8 and niedriege_karten <= hohe_karten:
            return 2
        elif gebrauchte_karte > 8 and hohe_karten+2 <= niedriege_karten:
            return 4
        elif gebrauchte_karte > 8 and hohe_karten+1 <= niedriege_karten:
            return 3
        elif gebrauchte_karte > 8 and hohe_karten <= niedriege_karten:
            return 2
        else:
            return 1

    elif zaehlweise == 'plus/minus':
        #Zahlweise plusminus
        plusminus = 0
        for karte in bisherige_karten:
            if karte in ['K', 'Q', 'J', '9', '10', 'A']:
                plusminus += 1
            elif karte in ['2', '3', '4', '5', '6', '7']:
                plusminus -= 1

        #Gebrauchte Hand
        gebrauchte_karte = 21 - hand_berechnen(eigene_hand)

        if gebrauchte_karte == 0:
            return 0
        elif gebrauchte_karte == 8:
            return 1
        elif gebrauchte_karte > 8 and plusminus <= -2:
            return 4
        elif gebrauchte_karte > 8 and plusminus <= -1:
            return 3
        elif gebrauchte_karte > 8 and plusminus <= 0:
            return 2
        elif gebrauchte_karte < 8 and plusminus >= 2:
            return 4
        elif gebrauchte_karte < 8 and plusminus >= 1:
            return 3
        elif gebrauchte_karte < 8 and plusminus >= 0:
            return 2
        
        else:
            return 1

    elif zaehlweise == 'gerade, ungerade':
        gerade = 0
        ungerade = 0
        for karte in bisherige_karten:
            if karte in ['2', '4', '6', '8', '10']:
                gerade += 1
            elif karte in ['A', '3', '5', '7', '9']:
                ungerade += 1

        #Gebrauchte Hand
        gebrauchte_karte = 21 - hand_berechnen(eigene_hand)

        if gebrauchte_karte == 0:
            return 0
        elif gebrauchte_karte%2 == 0 and gerade < ungerade:
            return 2
        elif gebrauchte_karte%2 == 0 and ungerade+2 > gerade:
            return 3
        elif gebrauchte_karte%2 != 0 and gerade < ungerade:
            return 2
        elif gebrauchte_karte%2 != 0 and gerade+2 < ungerade:
            return 3

        else:
            return 1
        


        print()

    elif zaehlweise == 'keine Strategie':
        bauchgefühl = np.random.randint(0, 10) 
        gebrauchte_karte = 21 - hand_berechnen(eigene_hand)
        if gebrauchte_karte == 0:
            return 0
        if bauchgefühl > 7:
            return 3
        elif bauchgefühl > 5:
            return 2
        else:
            return 1



def gewinnt_spieler(spieler_hand, dealer_hand, punktlandung=False):
    '''
    Gewinnt der Spieler, bzw mach er eine Punktlandung
    Input: Spielerhand, Dealerhand, Punktlandung
    Output: Spieler gewinnt? Boolean
    '''
    '''Rückgabe Spieler gewinne -> true sonst false'''
    if punktlandung:
        if hand_berechnen(spieler_hand) == 21:
            return True
    else:
        if (21 - hand_berechnen(spieler_hand)) < (21 - hand_berechnen(dealer_hand)):
            return False
        elif (21 - hand_berechnen(spieler_hand)) > (21 - hand_berechnen(dealer_hand)):
            return True
        elif (21 - hand_berechnen(spieler_hand)) == (21 - hand_berechnen(dealer_hand)):
            if len(spieler_hand) > len(dealer_hand):
                return False
            elif len(spieler_hand) < len(dealer_hand):
                return True



def blackjack_spielrunde(spieler_buget, dealer_buget, deck, bisherige_karten, spielerstrategie, dealerstrategie):
    uebrige_karten = len(deck)
    while uebrige_karten > 10 and spieler_buget > 0 and dealer_buget > 0:
        einsatz = 0
        dealer_karten_total = []
        spieler_karten_total = []
        #Zwei Karten nehmen
        spieler_karten, deck = karte_austeilen(deck)
        spieler_karten_total.append(spieler_karten)
        bisherige_karten.append(spieler_karten)
        spieler_karten, deck = karte_austeilen(deck)
        spieler_karten_total.append(spieler_karten)
        bisherige_karten.append(spieler_karten)

        dealer_karten, deck = karte_austeilen(deck)
        dealer_karten_total.append(dealer_karten)
        bisherige_karten.append(dealer_karten)
        dealer_karten, deck = karte_austeilen(deck)
        dealer_karten_total.append(dealer_karten)
        bisherige_karten.append(dealer_karten)

        #Patt
        if gewinnt_spieler(spieler_karten_total, dealer_karten_total, True) and gewinnt_spieler(dealer_karten_total, spieler_karten_total, True):
            print("Patt")
            spieler_buget = einsatz/2
            dealer_buget = einsatz/2
            break
        #Spieler gewinnt
        elif gewinnt_spieler(spieler_karten_total, dealer_karten_total, True):
            print("Spieler gewinnt")
            spieler_buget += einsatz
            break
        #Dealer gewinnt
        elif gewinnt_spieler(dealer_karten_total, spieler_karten_total, True):
            print("Dealer gewinnt")
            dealer_buget += einsatz
            break

        einsatz = 50
        spieler_buget -= einsatz/2
        dealer_buget -= einsatz/2

        #Spieler denkt nach
        spieler_chance = berechne_zuverlaessigkeit(spieler_karten_total, spielerstrategie, bisherige_karten, uebrige_karten)
        dealer_chance = berechne_zuverlaessigkeit(dealer_karten_total, spielerstrategie, bisherige_karten, uebrige_karten)
        totale_chance = spieler_chance - dealer_chance
        
        print('Spielerhand: ', spieler_karten_total)
        print('Dealerhand: ', dealer_karten_total)
        print(totale_chance)

        if totale_chance >= 2:
            print('Krass')
        elif totale_chance >= 1:
            print('Ok')
        elif totale_chance == 0:
            print('Naja')
        elif totale_chance <= -3:
            print('Nicht krass')
        elif totale_chance <= -2:
            print('Nicht ok')
        else:
            print('Bruh')
        
        print()


blackjack_spielrunde(1000,1000,deck_erstellen(4), [], 'groß&klein', 'groß&klein')