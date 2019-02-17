import timeit

# stmt - tar in uttrycket som ska time:as
# antalet gånger som uttrycket exekveras.
# timeit mäter hur lång tid det tar att köra ett uttryck samtidigt garbage collectorn är avstängd, dvs python frigör inte minne allt eftersom. Oberoende körningar blir mer jämförbara.
# timeit returnerar tiden som det tar att köra huvudprogrammet "a number of times", mätt i sekunder som en float.

class Song:
    def __init__(self, trackid, låtid, artist, låttitel):
        self.trackid = trackid
        self.låtid = låtid
        self.artist = artist
        self.låttitel = låttitel

    def __lt__(self, other):
        return self.artist < other.artist

    def __str__(self):
        return self.låttitel + ' är skriven av ' + self.artist


def readfile(filename, antal):
    with open(filename, "r", encoding="utf-8") as låtfil:
        rader = låtfil.readlines()
        a = []
        for rad in rader[0:antal]:
            a.append(rad.strip('\n').strip().split('<SEP>'))
        lista = []
        dictionary = {}
        for i in a:
            lista.append(Song(i[0], i[1], i[2], i[3]))
        for låt in lista:
            dictionary[låt.artist] = låt.låttitel
        return lista, dictionary


def linsok(lista, testtrackid):
    for i in lista:
        if i.trackid == testtrackid:
            return True
    return False


def quicksort(lista):
    sista = len(lista) - 1
    qsort(lista, 0, sista)


def qsort(lista, low, high):
    pivotindex = (low + high) // 2
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
        while lista[v] < pivot:
            v = v + 1
        h = h - 1
        while h != 0 and lista[h] > pivot:
            h = h - 1
        lista[v], lista[h] = lista[h], lista[v]
        if v >= h:
            break
    lista[v], lista[h] = lista[h], lista[v]
    return v


def slåuppdict(dictionary, testartist):
    if dictionary[testartist] is not None:
        return True
    else:
        return False


def binärsökning(lista, testtrackid):
    low = 0
    high = len(lista)-1
    found = False

    while low <= high and not found:
        middle = (low + high)//2
        if lista[middle].trackid == testtrackid:
            found = True
        else:
            if testtrackid < lista[middle].trackid:
                high = middle - 1
            else:
                low = middle + 1
    return found


def tabell(sökning, ant_låtar, körtider):
    print("##", sökning)
    print("|     N     |    tid    |")
    print("| --------- | --------- |")
    for i in range(len(ant_låtar)):
        print("|", ant_låtar[i], "|", round(körtider[i], 7), "|")
    print('\n')


def main():

    filename = "unique_tracks.txt"
    #lista, dictionary = readfile(filename)
    ant_låtar = [1000, 10000, 50000, 200000, 500000, 1000000]
    körtiderl = []
    körtiderq = []
    körtiderb = []
    körtiderd = []
    for i in ant_låtar:
        lista, dictionary = readfile(filename, i)
        sista = lista[-1]
        testartist = sista.artist
        testtrackid = sista.trackid
        körtiderl.append(timeit.timeit(stmt=lambda: linsok(lista, testtrackid), number=1000))
        körtiderq.append(timeit.timeit(stmt=lambda: quicksort(lista), number=1))
        körtiderb.append(timeit.timeit(stmt=lambda: binärsökning(lista, testtrackid), number=1000))
        körtiderd.append(timeit.timeit(stmt=lambda: slåuppdict(dictionary, testartist), number=1000))

    tabell('Linjärsökning', ant_låtar, körtiderl)
    tabell('Quicksortering', ant_låtar, körtiderq)
    tabell('Binärsökning', ant_låtar, körtiderb)
    tabell('Dictionary-uppslagning', ant_låtar, körtiderd)


main()
