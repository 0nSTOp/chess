type Case = str

echiquier = [["Vide" for i in range(8)] for j in range(8)]
pieces_n = [(-1, -1) for i in range(8)]
pieces_b = [(-1, -1) for i in range(8)]
pions_n = [(-1, -1, 0) for i in range(8)]
pions_b = [(-1, -1, 0) for i in range(8)]
pieces = [(-1, -1, 0) for i in range(32)] #liste des pieces : roi_b, roi_n, dame_b, dame_n, tour1b, tour1n, tour2b, tour2n, fou, cav, pions face a face (commence a 16) 
petit_roque_b = True
petit_roque_n = True
grand_roque_b = True
grand_roque_n = True
enpassant_n = [False for i in range(8)] #dit si les cases a6 à h6 peuvent etre prises en passant
enpassant_b = [False for i in range(8)] #dit si les cases a3 à h3 peuvent etre prises en passant


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

def cherche(echiquier, case):
    """
    renvoie la piece qui occupe cette case (-2 : impossible, -1 : rien 0, 1 : pion n/b, 2,3 : cavalier, 4,5 : fou, 6,7 : tour, 8,9 : dame, 10, 11 : roi)
    l'echiquier contient le tableau correspondant aux cases, et un deuxieme pour les prises en passant et les roques : les 8 premiers contiennent False si le pion blanc a double au dernier tour,
    resp les 8 suivants pour les noir, le 17 contient True si le roi blanc peut roquer, resp le 18 pour le noir, le 19 et le 20 les positions respectives du roi blanc et noir
    """
    if case[0]<0 or case[0]>7 or case[1]<0 or case[1]>7:
        return "Impossible"
    return echiquier[0][case[0]][case[1]] #work in progress : string

def dispo(echiquier, case): #work in progress : roque ; changer le nom de la liste en disp
    """
    renvoie une liste des cases disponibles pour la piece occupant la case (ou une liste vide si la case est innocupee)
    """
    piece = cherche(echiquier, case)
    dispo = []
    if piece == "Pion_b": 
        x = cherche(echiquier, (case[0]+1, case[1]+1)) #prise a droite
        y = cherche(echiquier, (case[0]-1, case[1]+1)) #prise a gauche
        z = cherche(echiquier, (case[0], case[1]+2)) #deux cases
        t = cherche(echiquier, (case[0], case[1]+1)) #avancee normale     
        if x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n": 
            dispo.append(case[0]+1, case[1]+1)
        if y == "Pion_n" or y == "Cavalier_n" or y == "Tour_n" or y == "Fou_n" or y == "Dame_n":
            dispo.append(case[0]-1, case[1]+1)
        if t == "Vide":
            dispo.append(case[0], case[1]+1)
            if z == "Vide":
                dispo.append(case[0], case[1]+2)

        if case[1] == 4: #enpassant 
            if case[0] > 0:
                if enpassant_n[case[0]-1]:
                    dispo.append(case[0]+1, case[1]-1)
            if case[1]<8:
                if enpassant_n[1+case[1]]:
                    dispo.append(case[0]+1, case[1]+1)
                

    if piece == "Pion_n": 
        x = cherche(echiquier, (case[0]+1, case[1]+1)) #prise a droite
        y = cherche(echiquier, (case[0]-1, case[1]+1)) #prise a gauche
        z = cherche(echiquier, (case[0], case[1]+2)) #deux cases
        t = cherche(echiquier, (case[0], case[1]+1)) #avancee normale     
        if x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b": 
            dispo.append(case[0]+1, case[1]+1)
        if y == "Pion_b" or y == "Cavalier_b" or y == "Tour_b" or y == "Fou_b" or y == "Dame_b":
            dispo.append(case[0]-1, case[1]+1)
        if t == "Vide":
            dispo.append(case[0], case[1]+1)
            if z == "Vide":
                dispo.append(case[0], case[1]+2)

        if case[1] == 4: #enpassant 
            if case[0] > 0:
                if enpassant_b[case[0]-1]:
                    dispo.append(case[0]+1, case[1]-1)
            if case[1]<8:
                if enpassant_b[1+case[1]]:
                    dispo.append(case[0]+1, case[1]+1)
    
    if piece == "Cavalier_b":
        for (i,j) in [(2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)]:
            x = cherche(echiquier, (case[0]+i, case[1]+j))
            if x == "Vide" or x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b":
                dispo.append((case[0]+i,case[1]+j))

    if piece == "Cavalier_n": 
        for (i,j) in [(2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)]:
            x = cherche(echiquier, (case[0]+i, case[1]+j))
            if x == "Vide" or x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n":
                dispo.append((case[0]+i,case[1]+j))
        
    if piece == "Fou_b" or piece == "Dame_b": 
        for (i,j) in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:

            bloque = False
            k = 0
            while k < 7 and not bloque:
                case_testee = (case[0]+k*i, case[1]+k*j)
                x = cherche(echiquier, case_testee)
                if x == "Vide":
                    dispo.append(case_testee)
                elif x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b":
                    bloque = True
                else: #si la piece est noire ou case impossible
                    bloque = True
                    dispo.append(case_testee)
    
    if piece == "Fou_n" or piece == "Dame_n":
        for (i,j) in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:

            bloque = False
            k = 0
            while k < 7 and not bloque:
                case_testee = (case[0]+k*i, case[1]+k*j)
                x = cherche(echiquier, case_testee)
                if x == "Vide":
                    dispo.append(case_testee)
                elif x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n":
                    bloque = True
                else: #si la piece est blanche ou case impossible
                    bloque = True
                    dispo.append(case_testee)

    if piece == 'Tour_b' or piece == "Dame_b":
        for (i,j) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:

            bloque = False
            k = 0
            while k < 7 and not bloque:
                case_testee = (case[0]+k*i, case[1]+k*j)
                x = cherche(echiquier, case_testee)
                if x == "Vide":
                    dispo.append(case_testee)
                elif x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b":
                    bloque = True
                else:
                    bloque = True
                    dispo.append(case_testee)

    if piece == 'Tour_n' or piece == "Dame_n":
        for (i,j) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            bloque = False
            k = 0
            while k < 7 and not bloque:
                case_testee = (case[0]+k*i, case[1]+k*j)
                x = cherche(echiquier, case_testee)
                if x == "Vide":
                    dispo.append(case_testee)
                elif x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n":
                    bloque = True
                else:
                    bloque = True
                    dispo.append(case_testee)

    if piece == "Roi_b": 
        for (i,j) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            case_testee = (case[0]+k*i, case[1]+k*j)
            x = cherche(echiquier, case_testee)
            if x == "Vide" or x == "Pion_n" or x == "Cavalier_n" or x == "Tour_n" or x == "Fou_n" or x == "Dame_n":
                dispo.append(case_testee)
        if petit_roque_b == True:
            dispo.append(case[0]+2, case[1])
        if grand_roque_b == True:
            dispo.append(case[0]-2, case[1])


    if piece == "Roi_n": 
        for (i,j) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            case_testee = (case[0]+k*i, case[1]+k*j)
            x = cherche(echiquier, case_testee)
            if x == "Vide" or x == "Pion_b" or x == "Cavalier_b" or x == "Tour_b" or x == "Fou_b" or x == "Dame_b":
                dispo.append(case_testee)
        if petit_roque_n == True:
            dispo.append(case[0]-2, case[1])
        if grand_roque_n == True:
            dispo.append(case[0]+2, case[1])

        for coup in dispo:
            tab = [[echiquier[i][j] for j in range(8)] for i in range(8)]
            tab[case[0]][case[1]] = "Vide"
            tab[coup[0]][coup[1]] = "Roi_b"
            for i in pieces_n:
                if dispo()
###############################################################################

    if piece % 2 == 0: #verifie que le mouvement met pas le roi blanc en danger
        for i in dispo:
            tab = [[i for i in echiquier[j]] for j in range(len(echiquier))]
            deplacer(tab, case, i)
            positionroi = pieces[0]
            for j in range(1, len(pieces), 2):
                for k in dispo(echiquier, (pieces[j][0], pieces[j][1])):
                    if k[0] == positionroi[0] and k[1] == positionroi[1]:
                        dispo.pop(i)
    
    if piece % 2 == 1: #pareil mais pour le noir
        for i in dispo:
            tab = [[i for i in echiquier[j]] for j in range(len(echiquier))]
            deplacer(tab, case, i)
            positionroi = pieces[1]
            for j in range(0, len(pieces), 2):
                for k in dispo(echiquier, (pieces[j][0], pieces[j][1])):
                    if k[0] == positionroi[0] and k[1] == positionroi[1]:
                        dispo.pop(i)
    return dispo

def deplacer(echiquier, pieces, roque, enpassant, casedepart, casearrivee, grroque = False, ptroque = False, deuxcases = False): #work in progress : promotion, manger la piece sur un enpassant, deux cases
    """
    enleve la piece eventuellement capturee de la liste des pieces et deplace la piece
    si on essaye de se déplacer sur la case d'un roi, renvoie 1 ; sinon, renvoie 0
    """
    x = echiquier[casearrivee[0]][casearrivee[1]]
    echiquier[casearrivee[0]][ casearrivee[1]] = echiquier[casedepart[0]][casedepart[1]]
    echiquier[casedepart[0]][casedepart[1]] = -1
    enpassant = [False for i in range(16)]
    if grroque :
        if casedepart[1] == 7: #grand roque roi noir
            echiquier[0][7] = -1
            echiquier[3][7] =  7
            roque[1] = False
        else: #grand roque roi blanc
            echiquier[0][0] = -1
            echiquier[3][0] = 6
            roque[0] = False
    elif ptroque:
        if casedepart[1] == 7: #petit roque roi noir
            echiquier[7][7] = -1
            echiquier[5][7] =  7
            roque[1] = False
        else: #petit roque roi blanc
            echiquier[7][0] = -1
            echiquier[5][0] = 6
            roque[0] = False
    elif deuxcases:
        ordonnee = casearrivee[1]
        #work
            

    else:
        if x != -1:
            if x == 0:
                i = 16
                while i<32: #trouve le pion sur la case prise et le capture
                    if pieces[i][0] == casearrivee[0] and pieces[i][1] == casearrivee[1]:
                        pieces[i] = (-1,-1, 0)
                        break
                    i+=2
            if x == 1:
                i = 17
                while i < 33:
                    if pieces[i][0] == casearrivee[0] and pieces[i][1] == casearrivee[1]:
                        pieces[i] = (-1,-1, 0)
                        break
                    i+=2

            if x == 2:
                if pieces[12][0] == casearrivee[0] and pieces[12][1] == casearrivee[1]:
                    pieces[12] = (-1,-1,0)
                else:
                    pieces[14] = (-1,-1,0)
            
            if x == 3:
                if pieces[13][0] == casearrivee[0] and pieces[13][1] == casearrivee[1]: #si le cavalier pris est le premier des deux
                    pieces[13] = (-1,-1,0)
                else:
                    pieces[15] = (-1,-1,0)
            
            if x == 4:
                if pieces[8][0] == casearrivee[0] and pieces[8][1] == casearrivee[1]: #si le fou pris est le premier des deux
                    pieces[8] = (-1,-1,0)
                else:
                    pieces[10] = (-1,-1,0)

            if x == 5:
                if pieces[9][0] == casearrivee[0] and pieces[9][1] == casearrivee[1]: #si le fou pris est le premier des deux
                    pieces[9] = (-1,-1,0)
                else:
                    pieces[11] = (-1,-1,0)

            if x == 6:
                if pieces[6][0] == casearrivee[0] and pieces[6][1] == casearrivee[1]: #si la tour prise est la première des deux
                    pieces[6] = (-1,-1,0)
                else:
                    pieces[4] = (-1,-1,0)

            if x == 7:
                if pieces[7][0] == casearrivee[0] and pieces[7][1] == casearrivee[1]: #si la tour prise est la première des deux
                    pieces[7] = (-1,-1,0)
                else:
                    pieces[5] = (-1,-1,0)

            if x == 8:
                pieces[2] = (-1, -1, 0)
            if x == 9:
                pieces[3] = (-1, -1, 0)
            if x == 10 or x == 11:
                return 1
    return 0





dispo([[[-1,-1], [-1,-1]], []], (0, 1))

