import copy


class Configuratie:
    def __init__(self, matrice):
        self.matrice = matrice

    def __repr__(self):
        return f"{self.matrice}"

    def __eq__(self, other):
        return self.matrice == other.matrice

    # def __getitem__(self):
    #     return self.matrice

    def pozitie(self):
        # cheia este numarul, valoarea este un tuplu cu (index_linie, index_col) indecsii numarului pe tablita
        pozitie = {}
        for i in range(3):
            for j in range(3):
                pozitie[self.matrice[i][j]] = (i, j)
        return pozitie

    def euristica(self, cfg_final_dict):
        h = 0
        cfg_curenta = self.pozitie()

        for tablita in tablite:
            if cfg_curenta[tablita] != cfg_final_dict[tablita]:
                # distanta Manhattan de la pozitia curenta la pozitia dorita
                h += abs(cfg_curenta[tablita][0] - cfg_final_dict[tablita][0]) +\
                     abs(cfg_curenta[tablita][1] - cfg_final_dict[tablita][1])
        return h


class Nod:
    def __init__(self, config):
        self.info = config
        self.h = config.euristica(cfg_final_dict)

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Arc:
    def __init__(self, capat, varf, cost):
        self.capat = capat
        self.varf = varf
        self.cost = cost


class Problema:
    def __init__(self):
        self.noduri = [Nod(cfg_initial)]
        self.arce = []
        self.nod_start = self.noduri[0]
        self.nod_scop = cfg_final

    def cauta_nod_nume(self, info):
        """Stiind doar informatia "info" a unui nod,
        trebuie sa returnati fie obiectul de tip Nod care are acea informatie,
        fie None, daca nu exista niciun nod cu acea informatie."""
        # TO DO ... DONE
        for nod in self.noduri:
            if nod.info == info:
                return nod
        return None


""" Sfarsit definire problema """


""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
            Cuprinde o referinta catre nodul in sine (din graf)
            dar are ca proprietati si valorile specifice algoritmului A* (f si g).
            Se presupune ca h este proprietate a nodului din graf
    """

    problema = None  # atribut al clasei

    def __init__(self, nod_graf, parinte=None, g=0, f=None):
        self.nod_graf = nod_graf  	# obiect de tip Nod
        self.parinte = parinte  	# obiect de tip Nod
        self.g = g  	# costul drumului de la radacina pana la nodul curent
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        """
                Functie care calculeaza drumul asociat unui nod din arborele de cautare.
                Functia merge din parinte in parinte pana ajunge la radacina
        """
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        """
                Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
                Verificarea se face mergand din parinte in parinte pana la radacina
                Se compara doar informatiile nodurilor (proprietatea info)
                Returnati True sau False.
                "nod" este obiect de tip Nod (are atributul "nod.info")
                "self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
        """
        # TO DO ... DONE
        nod_c = self
        while nod_c.parinte is not None:
            if nod.info == nod_c.nod_graf.info:
                return True
            nod_c = nod_c.parinte
        return False

    # se modifica in functie de problema

    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
        si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
        sau lista vida, daca nu exista niciunul.(Fiecare tuplu contine un obiect d
        e tip Nod si un numar.)
        """
        # TO DO ... DONE

        # generam toate mutarile posibile. o mutare reprezinta umplerea spatiului gol cu o tablita vecina lui.
        # vechea pozitie a tablitei mutate devine spatiu gol

        configuratie = self.nod_graf.info
        succesori = []
        spatiu_gol = configuratie.pozitie()[0]
        vecini_i = [-1, 0, 1, 0]
        vecini_j = [0, 1, 0, -1]

        for ndx in range(4):
                posibil_vecin = copy.deepcopy(configuratie)
                if spatiu_gol[0] + vecini_i[ndx] < 0:
                    continue
                elif spatiu_gol[0] + vecini_i[ndx] > 2:
                    continue
                elif spatiu_gol[1] + vecini_j[ndx] < 0:
                    continue
                elif spatiu_gol[1] + vecini_j[ndx] > 2:
                    continue
                else:
                    posibil_vecin.matrice[spatiu_gol[0]][spatiu_gol[1]] = configuratie.matrice[spatiu_gol[0] +\
                                                                          vecini_i[ndx]][spatiu_gol[1] + vecini_j[ndx]]
                    posibil_vecin.matrice[spatiu_gol[0] + vecini_i[ndx]][spatiu_gol[1] + vecini_j[ndx]] =\
                                                                          configuratie.matrice[spatiu_gol[0]][spatiu_gol[1]]
                    succesor = problema.cauta_nod_nume(posibil_vecin)
                    if not succesor:
                        nod_nou = Nod(posibil_vecin)
                        problema.noduri.append(nod_nou)
                        succesor = nod_nou
                    succesori.append((succesor, 1))

        return succesori


    def test_scop(self):
        return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def str_info_noduri(l):
    """
            o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = "[\n"
    for ndx, x in enumerate(l):
        sir += "Mutarea " + str(ndx) + ": " + str(x) + "\n"
    sir += "]"
    return sir


def afis_succesori_cost(l):
    """
            o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: "+str(x)+", cost arc:" + str(cost)
    return sir


def in_lista(l, nod):
    """
            lista "l" contine obiecte de tip NodParcurgere
            "nod" este de tip Nod
    """
    for i in range(len(l)):
        if l[i].nod_graf.info == nod.info:
            return l[i]
    return None


def a_star():
    """
            Functia care implementeaza algoritmul A-star
    """
    # TO DO ... DONE

    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere
    nod_nou = None

    while len(open) > 0:
        # print(str_info_noduri(open))  # afisam lista open
        nod_curent = open.pop(0)  # scoatem primul element din lista open
        closed.append(nod_curent)  # si il adaugam la finalul listei closed

        # testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
        if nod_curent.test_scop():
            break

        l_succesori = nod_curent.expandeaza()  # contine tupluri de tip (Nod, numar)
        for (nod_succesor, cost_succesor) in l_succesori:
            # "nod_curent" este tatal, "nod_succesor" este fiul curent

            # daca fiul nu e in drumul dintre radacina si tatal sau (adica nu se creeaza un circuit)
            if (not nod_curent.contine_in_drum(nod_succesor)):

                # calculez valorile g si f pentru "nod_succesor" (fiul)
                # g-ul tatalui + cost muchie(tata, fiu)
                g_succesor = nod_curent.g + cost_succesor
                f_succesor = g_succesor + nod_succesor.h  # g-ul fiului + h-ul fiului

                # verific daca "nod_succesor" se afla in closed
                # (si il si sterg, returnand nodul sters in nod_parcg_vechi
                nod_parcg_vechi = in_lista(closed, nod_succesor)

                if nod_parcg_vechi is not None:  # "nod_succesor" e in closed
                    # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                    # 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista closed)
                    # atunci actualizez parintele, g si f
                    # si apoi voi adauga "nod_nou" in lista open
                    if (f_succesor < nod_parcg_vechi.f):
                        # scot nodul din lista closed
                        closed.remove(nod_parcg_vechi)
                        nod_parcg_vechi.parinte = nod_curent  # actualizez parintele
                        nod_parcg_vechi.g = g_succesor  # actualizez g
                        nod_parcg_vechi.f = f_succesor  # actualizez f
                        nod_nou = nod_parcg_vechi  # setez "nod_nou", care va fi adaugat apoi in open

                else:
                    # daca nu e in closed, verific daca "nod_succesor" se afla in open
                    nod_parcg_vechi = in_lista(open, nod_succesor)

                    if nod_parcg_vechi is not None:  # "nod_succesor" e in open
                        # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                        # 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista open)
                        # atunci scot nodul din lista open
                        # 		(pentru ca modificarea valorilor f si g imi va strica sortarea listei open)
                        # actualizez parintele, g si f
                        # si apoi voi adauga "nod_nou" in lista open (la noua pozitie corecta in sortare)
                        open.remove(nod_parcg_vechi)
                        nod_parcg_vechi.parinte = nod_curent
                        nod_parcg_vechi.g = g_succesor
                        nod_parcg_vechi.f = f_succesor
                        nod_nou = nod_parcg_vechi

                    else:  # cand "nod_succesor" nu e nici in closed, nici in open
                        nod_nou = NodParcurgere(
                            nod_graf=nod_succesor, parinte=nod_curent, g=g_succesor)
                        # se calculeaza f automat in constructor

                if nod_nou:
                    # inserare in lista sortata crescator dupa f
                    # (si pentru f-uri egale descrescator dupa g)
                    i = 0
                    while i < len(open):
                        if open[i].f < nod_nou.f:
                            i += 1
                        else:
                            while i < len(open) and open[i].f == nod_nou.f and open[i].g > nod_nou.g:
                                i += 1
                            break

                    open.insert(i, nod_nou)

    if len(open) == 0:
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        print("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))

n=3
cfg_initial = Configuratie([
                                [1, 8, 2],
                                [0, 4, 3],
                                [7, 6, 5]
                              ])
cfg_final = Configuratie([
                          [1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 0]
                        ])
cfg_final_dict = cfg_final.pozitie()
tablite = [i for i in range(9)]


if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()