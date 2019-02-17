import timeit


class Song:
    def __init__(self, artistid, artistnamn, sångtitel, låtlängd, år):
        self.artistid = artistid
        self.artistnamn = artistnamn
        self.sångtitel = sångtitel
        self.låtlängd = låtlängd
        self.år = år

    # def __contains__(self, låtlängd):
    #     if self.låtlängd:
    #         return True

    def __lt__(self, other):
        return float(self.låtlängd) < float(other.låtlängd)

    def __str__(self):
        return self.sångtitel + ' är skriven av ' + self.artistnamn + ' och är ' + self.låtlängd + 's lång.'


def readfile(filename):
    with open(filename, "r", encoding="utf-8") as låtfil:
        rader = låtfil.readlines()
        a = []
        for rad in rader:
            a.append(rad.strip('\n').strip().split('\t'))
        lista = []
        # dictionary = {}
        for i in a:
            lista.append(Song(i[0], i[1], i[2], i[3], i[4]))
        # for låt in lista:
        #     dictionary[låt.sångtitel] = låt.låtlängd
        return lista

def quicksort(lista):
    sista = len(lista) - 1
    qsort(lista, 0, sista)


def qsort(lista, low, high):
    pivotindex = (low + high) // 2              # ett förhållandevis random objekt väljs som pivot. Konstanten blir ca 1.4 i nlog(n)

    # flytta pivot till kanten
    lista[pivotindex], lista[high] = lista[high], lista[pivotindex]

    # damerna först med avseende på pivotlista
    pivotmid = partitionera(lista, low - 1, high, lista[high])

    # flytta tillbaka pivot
    lista[pivotmid], lista[high] = lista[high], lista[pivotmid]

    if pivotmid - low > 1:
        qsort(lista, low, pivotmid - 1)
    if high - pivotmid > 1:
        qsort(lista, pivotmid + 1, high)


def partitionera(lista, v, h, pivot):
    while True:
        v = v + 1
        while lista[v] > pivot:
            v = v + 1
        h = h - 1
        while h != 0 and lista[h] < pivot:
            h = h - 1
        lista[v], lista[h] = lista[h], lista[v]
        if v >= h:
            break
    lista[v], lista[h] = lista[h], lista[v]
    return v


def längdsökning(lista, låt):
    redan_hittad = []
    for j in range(0, låt):
        kortare = Song(0, 0, 0, 0, 0)      # initialt en dummy
        for låt in lista:
            if låt > kortare and låt not in redan_hittad:
                kortare = låt
        redan_hittad.append(kortare)
    print(kortare)


def main():
    filename = 'sang-artist-data.txt'
    lista = readfile(filename)
    låt = 31                        # tal* längsta låten
    linsökning = timeit.timeit(stmt=lambda: längdsökning(lista, låt), number=1)
    sorteringstid = timeit.timeit(stmt=lambda: quicksort(lista), number=1)
    print(lista[låt-1])
    print('Linjärsökningstid för den', låt, 'längsta låten:', round(linsökning, 6), 's')
    print('Sorteringstid:', round(sorteringstid, 6), 's')


main()
