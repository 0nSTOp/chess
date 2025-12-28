type Piece = {"Tour_b", "Fou_b", "Cavalier_b", "Dame_b", "Roi_b", "Pion_b", "Tour_n", "Fou_n", "Cavalier_n", "Dame_n", "Roi_n", "Pion_n", "Vide"}

echiquier = [["Vide" for i in range(8)] for j in range(8)]
pieces_n = [(-1, -1) for i in range(8)]
pieces_b = [(-1, -1) for i in range(8)]
pions_n = [(-1, -1, 0) for i in range(8)]
pions_b = [(-1, -1, 0) for i in range(8)]
petit_roque_b = True
petit_roque_n = True
grand_roque_b = True
grand_roque_n = True
enpassant_n = [False for i in range(8)] #dit si les cases a6 à h6 peuvent etre prises en passant
enpassant_b = [False for i in range(8)] #dit si les cases a3 à h3 peuvent etre prises en passant
jeu = (echiquier, pieces_n, pieces_b, pions_n, pions_b, petit_roque_b, petit_roque_n, grand_roque_b, grand_roque_n, enpassant_n, enpassant_b)
#          0            1       2       3           4       5               6               7               8           9           10



def traduire(case):
    """
    prend un couple de valeurs (x,y) et le traduit en cases de l'echiquier 
    """
    if case[1] == 0:
        return "a" + str(case[0])
    elif case[1] == 1:
        return "b" + str(case[0])
    elif case[1] == 2:
        return "c" + str(case[0])
    elif case[1] == 3:
        return "d" + str(case[0])
    elif case[1] == 4:
        return "e" + str(case[0])
    elif case[1] == 5:
        return "f" + str(case[0])
    elif case[1] == 6:
        return "g" + str(case[0])    
    else:
        return "h" + str(case[0])
    
def trad_inv(s):
    """
    prend une valeur de case (type : "a1") et la traduit en un couple (x,y)
    """
    l = s[0]
    if l == "a":
        return (0, int(s[1]))
    if l == "b":
        return (1, int(s[1]))
    if l == "c":
        return (2, int(s[1]))    
    if l == "d":
        return (3, int(s[1]))
    if l == "e":
        return (4, int(s[1]))
    if l == "f":
        return (5, int(s[1]))   
    if l == "g":
        return (6, int(s[1]))
    else:
        return (7, int(s[1])) 

def cherche_pions_n(case, pions_n):
    i = 0
    trouve = False
    while not trouve and i < 8:
        if pions_n[i][0] == case[0] and pions_n[i][1] == case[1]:
            trouve = True
        i+=1
    if i == 8 : 
        return "Ne trouve pas le pion"
    return i

def cherche_pions_b(case, pions_b):
    i = 0
    trouve = False
    while not trouve and i < 8:
        if pions_b[i][0] == case[0] and pions_b[i][1] == case[1]:
            trouve = True
        i+=1
    if i == 8 : 
        return "Ne trouve pas le pion"
    return i

def cherche_pieces_n(case, pieces_n):
    i = 0
    trouve = False
    while not trouve and i < 8:
        if pieces_n[i][0] == case[0] and pieces_n[i][1] == case[1]:
            trouve = True
        i+=1
    if i == 8 : 
        return "Ne trouve pas la piece"
    return i

def cherche_pieces_b(case, pieces_b):
    i = 0
    trouve = False
    while not trouve and i < 8:
        if pieces_n[i][0] == case[0] and pieces_n[i][1] == case[1]:
            trouve = True
        i+=1
    if i == 8 : 
        return "Ne trouve pas la piece"
    return i

def occupe(echiquier, case):
    """
    renvoie la piece qui occupe cette case (-2 : impossible, -1 : rien 0, 1 : pion n/b, 2,3 : cavalier, 4,5 : fou, 6,7 : tour, 8,9 : dame, 10, 11 : roi)
    l'echiquier contient le tableau correspondant aux cases, et un deuxieme pour les prises en passant et les roques : les 8 premiers contiennent False si le pion blanc a double au dernier tour,
    resp les 8 suivants pour les noir, le 17 contient True si le roi blanc peut roquer, resp le 18 pour le noir, le 19 et le 20 les positions respectives du roi blanc et noir
    """
    if case[0]<0 or case[0]>7 or case[1]<0 or case[1]>7:
        return "Impossible"
    return echiquier[case[0]][case[1]] 

def dispo(echiquier, case):
    """
    renvoie une liste des cases disponibles pour la piece occupant la case (ou une liste vide si la case est innocupee)
    """
    piece = occupe(echiquier, case)
    disp = []
    if piece == "Fou_b":
        disp += dispo_fou(echiquier, case, 0)
    elif piece == "Fou_n":
        disp += dispo_fou(echiquier, case, 1)
    elif piece == "Tour_b":
        disp = dispo_tour(echiquier, case, 0)
    elif piece == "Tour_n":
        disp = dispo_tour(echiquier, case, 1)
    elif piece == "Cavalier_b":
        disp = dispo_cavalier(echiquier, case, 0)
    elif piece == "Cavalier_n":
        disp = dispo_tour(echiquier, case, 1)
    elif piece == "Dame_b":
        disp1 = dispo_tour(echiquier, case, 0)
        disp2 = dispo_fou(echiquier, case, 0)
        disp = disp1 + disp2
    elif piece == "Dame_n":
        disp1 = dispo_tour(echiquier, case, 1)
        disp2 = dispo_fou(echiquier, case, 1)
        disp = disp1 + disp2
    elif piece == "Roi_b":
        disp = dispo_roi(echiquier, case, 0)
    elif piece == "Roi_n":
        disp = dispo_roi(echiquier, case, 1)

    return disp

def dispo_fou(echiquier, case, couleur):
    disp = []
    if couleur == 0: #blanc 
        for (i,j) in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:

            bloque = False
            k = 0
            while k < 7 and not bloque:
                case_testee = (case[0]+k*i, case[1]+k*j)
                x = occupe(echiquier, case_testee)
                if x == "Vide":
                    disp.append(case_testee)
                elif x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b":
                    bloque = True
                else: #si la piece est noire ou case impossible
                    bloque = True
                    disp.append(case_testee)
    
    if couleur == 1:
        for (i,j) in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:

            bloque = False
            k = 0
            while k < 7 and not bloque:
                case_testee = (case[0]+k*i, case[1]+k*j)
                x = occupe(echiquier, case_testee)
                if x == "Vide":
                    dispo.append(case_testee)
                elif x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n":
                    bloque = True
                else: #si la piece est blanche ou case impossible
                    bloque = True
                    dispo.append(case_testee)
    return disp

def dispo_cavalier(echiquier, case, couleur):
    disp = []
    if couleur == 0:
        for (i,j) in [(2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)]:
            x = occupe(echiquier, (case[0]+i, case[1]+j))
            if x == "Vide" or x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b":
                disp.append((case[0]+i,case[1]+j))

    if couleur == 1: 
        for (i,j) in [(2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)]:
            x = occupe(echiquier, (case[0]+i, case[1]+j))
            if x == "Vide" or x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n":
                disp.append((case[0]+i,case[1]+j))
    return disp

def dispo_tour(echiquier, case, couleur):
    disp = []
    if couleur == 0:
        for (i,j) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:

            bloque = False
            k = 0
            while k < 7 and not bloque:
                case_testee = (case[0]+k*i, case[1]+k*j)
                x = occupe(echiquier, case_testee)
                if x == "Vide":
                    disp.append(case_testee)
                elif x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b":
                    bloque = True
                else:
                    bloque = True
                    disp.append(case_testee)

    if couleur == 1:
        for (i,j) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            bloque = False
            k = 0
            while k < 7 and not bloque:
                case_testee = (case[0]+k*i, case[1]+k*j)
                x = occupe(echiquier, case_testee)
                if x == "Vide":
                    disp.append(case_testee)
                elif x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n":
                    bloque = True
                else:
                    bloque = True
                    disp.append(case_testee)
    return disp

def dispo_pion(echiquier, case, couleur):
    disp = []
    if couleur == 0: 
        x = occupe(echiquier, (case[0]+1, case[1]+1)) #prise a droite
        y = occupe(echiquier, (case[0]-1, case[1]+1)) #prise a gauche
        z = occupe(echiquier, (case[0], case[1]+2)) #deux cases
        t = occupe(echiquier, (case[0], case[1]+1)) #avancee normale     
        if x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n": 
            disp.append(case[0]+1, case[1]+1)
        if y == "Pion_n" or y == "Cavalier_n" or y == "Tour_n" or y == "Fou_n" or y == "Dame_n":
            disp.append(case[0]-1, case[1]+1)
        if t == "Vide":
            disp.append(case[0], case[1]+1)
            if z == "Vide":
                disp.append(case[0], case[1]+2)

        if case[1] == 4: #enpassant 
            if case[0] > 0:
                if enpassant_n[case[0]-1]:
                    disp.append(case[0]+1, case[1]-1)
            if case[1]<8:
                if enpassant_n[1+case[1]]:
                    disp.append(case[0]+1, case[1]+1)
                

    if couleur == 1: 
        x = occupe(echiquier, (case[0]+1, case[1]+1)) #prise a droite
        y = occupe(echiquier, (case[0]-1, case[1]+1)) #prise a gauche
        z = occupe(echiquier, (case[0], case[1]+2)) #deux cases
        t = occupe(echiquier, (case[0], case[1]+1)) #avancee normale     
        if x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b": 
            disp.append(case[0]+1, case[1]+1)
        if y == "Pion_b" or y == "Cavalier_b" or y == "Tour_b" or y == "Fou_b" or y == "Dame_b":
            disp.append(case[0]-1, case[1]+1)
        if t == "Vide":
            disp.append(case[0], case[1]+1)
            if z == "Vide":
                disp.append(case[0], case[1]+2)

        if case[1] == 4: #enpassant 
            if case[0] > 0:
                if enpassant_b[case[0]-1]:
                    disp.append(case[0]+1, case[1]-1)
            if case[1]<8:
                if enpassant_b[1+case[1]]:
                    disp.append(case[0]+1, case[1]+1)
    return disp

def dispo_roi(echiquier, case, couleur): #wip
    disp = []
    if couleur == 0: 
        for (i,j) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            case_testee = (case[0]+i, case[1]+j)
            x = occupe(echiquier, case_testee)
            if x == "Vide" or x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n":
                disp.append(case_testee)
        if petit_roque_b == True:
            disp.append(case[0]+2, case[1])
        if grand_roque_b == True:
            disp.append(case[0]-2, case[1])

        disp_copie = disp[:]
        for coup in disp_copie:
            tab = [[echiquier[i][j] for j in range(8)] for i in range(8)]
            tab[case[0]][case[1]] = "Vide"
            tab[coup[0]][coup[1]] = "Roi_b"
            for i in pieces_n:
                for attaque in dispo(tab, (pieces_n[0], pieces_n[1])):
                    if coup[0] == attaque[0] and coup[1] == attaque[1]:
                        disp.remove(coup)
            for i in pions_n:
                for attaque in dispo(tab, (pieces_n[0], pieces_n[1])):
                    if coup[0] == attaque[0] and coup[1] == attaque[1]:
                        disp.remove(coup)

    if couleur == 1: 
        for (i,j) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            case_testee = (case[0]+i, case[1]+j)
            x = occupe(echiquier, case_testee)
            if x == "Vide" or x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b":
                disp.append(case_testee)
        if petit_roque_n == True:
            disp.append(case[0]-2, case[1])
        if grand_roque_n == True:
            disp.append(case[0]+2, case[1])

        disp_copie = disp[:]
        for coup in disp_copie:
            tab = [[echiquier[i][j] for j in range(8)] for i in range(8)]
            tab[case[0]][case[1]] = "Vide"
            tab[coup[0]][coup[1]] = "Roi_n"
            for i in pieces_b:
                for attaque in dispo(tab, (pieces_n[0], pieces_n[1])):
                    if coup[0] == attaque[0] and coup[1] == attaque[1]:
                        disp.remove(coup)
            for i in pions_b:
                for attaque in dispo(tab, (pieces_n[0], pieces_n[1])):
                    if coup[0] == attaque[0] and coup[1] == attaque[1]:
                        disp.remove(coup)
###############################################################################
    return disp

def deplacer(jeu, casedepart, casearrivee, grroque = False, ptroque = False): #work in progress : promotion
    """
    enleve la piece eventuellement capturee de la liste des pieces et deplace la piece
    si on essaye de se déplacer sur la case d'un roi, renvoie 1 ; sinon, renvoie 0
    """


    pieceabouger = occupe(jeu[0], (casedepart[0],casedepart[1]))
    place_mangee = occupe(jeu[0], (casearrivee[0], casearrivee[1]))

    if place_mangee != "Vide":
        if place_mangee == "Pion_n":
            jeu[3][cherche_pions_n(place_mangee, jeu[3])] = (-1, -1)
        elif place_mangee == "Pion_b":
            jeu[4][cherche_pions_b(place_mangee, jeu[4])] = (-1, -1)
        elif place_mangee == "Tour_n" or place_mangee == "Cavalier_n" or place_mangee == "Fou_n" or place_mangee == "Dame_n" or place_mangee == "Roi_n":
            jeu[1][cherche_pieces_n(place_mangee, jeu[1])] = (-1, -1)
        elif place_mangee == "Tour_b" or place_mangee == "Cavalier_b" or place_mangee == "Fou_b" or place_mangee == "Dame_b" or place_mangee == "Roi_b":
            jeu[2][cherche_pieces_b(place_mangee, jeu[2])] = (-1, -1)

    jeu[9] = [False for i in range(8)]
    jeu[10] = [False for i in range(8)]

    if pieceabouger == "Pion_b":
        if casedepart[1] == 1 and casearrivee[1] == 3:
            jeu[10][casedepart[0]] = True #on marque que la case de ce pion peut etre en passant
            jeu[4][casedepart[0]] = (casearrivee[0], casearrivee[1])
            jeu[0][casedepart[0]][casedepart[1]] = "Vide"
            jeu[0][casearrivee[0]][casearrivee[1]] = "Pion_b"
            
        else:
            #il faut savoir quel pion est sur la case (améliorable)
            i = cherche_pions_n(casedepart, jeu[3])
            jeu[3][i] = (casearrivee[0], casearrivee[1])
            
        
    elif pieceabouger == "Pion_n":
        if casedepart[1] == 1 and casearrivee[1] == 3:
            jeu[9][casedepart[0]] = True #on marque que la case de ce pion peut etre en passant
            jeu[3][casedepart[0]] = (casearrivee[0], casearrivee[1])
            jeu[0][casedepart[0]][casedepart[1]] = "Vide"
            jeu[0][casearrivee[0]][casearrivee[1]] = "Pion_n"
        else:
            #il faut savoir quel pion est sur la case (améliorable)
            i = cherche_pions_b(casedepart, jeu[4])
            jeu[4][i] = (casearrivee[0], casearrivee[1])

    elif grroque:
        if casedepart[1] == 7: #grand roque roi noir
            jeu[0][0][7] = "Vide"
            jeu[0][3][7] =  "Tour_n"
            jeu[0][2][7] = "Roi_n"
            jeu[1][0] = (3,7)
            jeu[1][4] = (2,7)
            jeu[8] = False
            jeu[6] = False
        else: #grand roque roi blanc
            jeu[0][0][0] = "Vide"
            jeu[0][3][0] = "Tour_b"
            jeu[0][2][0] = "Roi_b"
            jeu[2][0] = (3,0)
            jeu[2][4] = (2,0)
            jeu[7] = False
            jeu[5] = False
    elif ptroque:
        if casedepart[1] == 7: #petit roque roi noir
            jeu[0][0][7] = "Vide"
            jeu[0][5][7] =  "Tour_n"
            jeu[0][6][7] = "Roi_n"
            jeu[1][0] = (5,7)
            jeu[1][4] = (6,7)
            jeu[8] = False
            jeu[6] = False
        else: #petit roque roi blanc
            jeu[0][0][0] = "Vide"
            jeu[0][5][0] = "Tour_b"
            jeu[0][6][0] = "Roi_b"
            jeu[2][0] = (5,0)
            jeu[2][4] = (6,0)
            jeu[7] = False
            jeu[5] = False

    else:#c'est une piece autre qu'un pion qui se deplace, et ce n'est pas un roque
        if pieceabouger == "Tour_n" or pieceabouger == "Cavalier_n" or pieceabouger == "Fou_n" or pieceabouger == "Dame_n" or pieceabouger == "Roi_n":
            i = cherche_pieces_n((casedepart[0], casedepart[1]))
            jeu[1][i] = (casearrivee[0], casearrivee[1])
            

        if pieceabouger == "Tour_b" or pieceabouger == "Cavalier_b" or pieceabouger == "Fou_b" or pieceabouger == "Dame_b" or pieceabouger == "Roi_b":
            i = cherche_pieces_b((casedepart[0], casedepart[1]))
            jeu[2][i] = (casearrivee[0], casearrivee[1])

        jeu[0][casedepart[0]][casedepart[1]] = "Vide"
        jeu[0][casearrivee[0]][casearrivee[1]] = pieceabouger
    
    return jeu





