class ExamException(Exception):
    pass


class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        #provo ad aprire il file
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except:
            raise ExamException("Errore in apertura del file {}".format(
                self.name))
            # Inizializzo una lista vuota per salvare tutti i dati
        time_series = []
        # last_date è il mese precedente al primo che mi potrebbe venir assegnato
        # mi serve per verificare che l'input sia ordinato e non contenga righe doppie
        last_date = "1948-12"
        # Apro il file
        my_file = open(self.name, 'r')

        # Leggo il file linea per linea
        for line in my_file:

            # Faccio lo split di ogni linea sulla virgola
            if "," in line:
                elements = line.split(',')
                is_data = False
                is_int = True
                if len(elements) < 2:
                    #non lavoro su questi dati e li ignoro
                    is_data = False
                    is_int = False
                elif len(elements) == 2:
                    # Con la funzione strip() tolgo il carattere di new line:
                    elements[1] = elements[1].strip()
                    #print (elements[1])
                else:
                    while len(elements)>2:
                        elements.pop(-1)
                    elements[1].strip()
                
                #datum è una lista contentente la prima parte di elements, cioè la data
                datum = [0, 0]
                #provo a dividere sulla "-"
                if "-" in elements[0]:
                    datum = elements[0].split('-')
                    #quando non è presente, l'elemento che sto analizzando non è una data nel formato richiesto e quindi lo ignoro o è la riga di intestazione e quindi la ignoro
                    is_data = True
                    datum[0] = int(datum[0])
                    datum[1] = int(datum[1])
                    if datum[0] not in range(1949, 1960):
                        is_data = False
                    if datum[1] not in range(1, 13):
                        is_data = False
                    # is_data mi permette di controllare se si tratta dell'intestazione, di righe fuori dal range o se si tratta di pezzi di testo che non c'entrano nulla
                    #print (is_data)
                if is_data is True:
                #print ("E vero?")
                    try:
                        elements[1] = int(elements[1])
                    except: 
                        is_int = False
                if is_int == True and is_data == True:
                #se il valore non è nullo o negativo ed è un intero
                    if elements[1] > 0:
                    #print ("Sono qui")
                        if elements[0] > last_date:
                        # Aggiungo alla lista gli elementi di questa linea
                            time_series.append(elements)
                            last_date = elements[0]
                        elif elements[0] == last_date:
                            raise ExamException("L'elemento {} è duplicato".format(
                            elements[0]))
                        elif elements[0] < last_date:
                            raise ExamException("L'elemento {} è fuori sequenza".format(elements[0]))
                    #altrimenti ignoro, come da consegna

        # Chiudo il file
        my_file.close()

        # Quando ho processato tutte le righe, ritorno i dati
        return time_series


def compute_avg_monthly_difference(time_series, first_year, last_year):
    
    #time_series è la variabile con la lista di liste tratta dal File
    
    # se first_year o last_year non sono una stringa, alzo un'eccezione
    if type(first_year) is not str:
        raise ExamException("L'anno di inizio non è stato inserito come stringa")

    if type(last_year) is not str:
        raise ExamException("L'anno di fine non è stato inserito come stringa")
    
    #se l'anno di fine è successivo all'anno di inizio, vengono invertiti
    if last_year < first_year:
        last_year, first_year = first_year, last_year
    
    #i dati del file iniziano con il 1949, quindi non è possibile che l'anno di inizio sia antecedente a questo, viene quindi alzata un'eccezione:
    if first_year < "1949":
        raise ExamException("L'anno di inizio è antecedente al 1949")

    #i dati del file finiscono con il 1960, quindi non è possibile che l'anno di fine sia successivo a questo, viene quindi alzata un'eccezione:
    if last_year > "1960":
        raise ExamException("L'anno di fine è successivo al 1960")

    #se l'anno di inizio e l'anno di fine coincidono, viene alzata un'eccezione in quanto non è possibile effettuare i calcoli
    if last_year == first_year:
        raise ExamException("L'anno di inizio e di fine coincidono, non è possibile effettuare la media richiesta")
    
    #l'anno con cui iniziare a costruire la matrice è first_year, viene convertito a intero in modo da permettere il confronto con dati successivi
    
    first_year = int (first_year)
    #l'anno con cui finire a costruire la matrice è last_year, viene convertito a intero in modo da permettere il confronto con dati successivi
    last_year = int (last_year)
    
    #totale dati mi permette di sapere la quante coppie di dati ho in time_series e quindi iterare più facilmente
    totale_dati = len(time_series)

    #curr_year_n_month è una lista contentente come primo elemento l'anno e come secondo il mese della coppia di dati di time_series che sto analizzando. Le dò come primo valore il primo della lista time_series in modo da controllare se è minore del primo anno
    curr_year_n_month = time_series[0] [0].split("-")

    #converto l'anno a intero per permettere il confronto
    curr_year_n_month [0] = int(curr_year_n_month[0])

    #se il primo anno di cui ho valori è successivo al primo anno da cui devo partire, alzo un'eccezione
    if curr_year_n_month [0] > first_year:
        raise ExamException ("Valore non presente nell'intervallo di dati")
    
    #curr_year_n_month è una lista contentente come primo elemento l'anno e come secondo il mese della coppia di dati di time_series che sto analizzando. Le dò come valore ora l'ultimo della lista time_series in modo da controllare se è maggiore dell'ultimo anno
    curr_year_n_month = time_series[len(time_series)-1] [0].split("-")
    
    #converto curr_year_n_month a intero per permettere il confronto
    curr_year_n_month [0] = int(curr_year_n_month[0])

    #se l'ultimo anno di cui ho valori è precedente all'ultimo anno con cui devo fare la media, alzo un'eccezione:
    if curr_year_n_month [0] < last_year:
        raise ExamException ("Valore non presente nell'intervallo di dati")
    
    #creo la lista di liste matrice_dati (la posso immaginare come una matrice) dove inserire solamente i valori degli anni di cui ho bisogno per fare i calcoli, se non ho qualche valore lo sostituisco con 0
    matrice_dati = []

    #delta mi permette di scoprire quante righe ho bisogno per la mia matrice
    delta = last_year - first_year + 1
    
    #creo un numero di righe uguali a delta
    for i in range (0, delta):
        matrice_dati.append([])

        #riempio con dodici elementi uguali a 0 ciascuna "riga" della matrice
        for j in range (0, 12):
            matrice_dati[i].append(0)
    
    #inizio a riempire la matrice
    #scorro tutta la lista che mi è stata data in imput dall'utente
    for i in range (0, totale_dati):

        #come prima, creo una lista, curr_year_n_month per sapere in che anno e in che mese mi trovo. Converto gli elementi in interi in modo da permettermi confronti con altri numeri
        curr_year_n_month = time_series [i] [0].split("-")
        curr_year_n_month[0] = int(curr_year_n_month[0])
        curr_year_n_month[1] = int (curr_year_n_month[1])
        
        #se l'anno che sto guardando è antecedente all'anno da cui devo partire per fare la media, lo ignoro
        if curr_year_n_month [0] < first_year:
            pass
        
        #se l'anno che sto analizzando è successivo all'anno con cui devo finire di fare la media, esco dal ciclo, in quanto so che la lista è stata ordinata cronologicamente e quindi non ho altri elementi da analizzare
        elif curr_year_n_month [0] > last_year:
            break

        #se sono in uno degli anni che mi interessa vado a compilare la matrice
        else:
            
            #indice_anno mi permette di capire in che riga della matrice sono, infatti è dato dalla differenza tra l'anno che sto analizzando e l'anno da cui devo partire
            indice_anno = curr_year_n_month[0] - first_year
            
            #indice_mese è uguale al mese attuale - 1, infatti, gennaio occuperebbe la posizione 0 nella lista
            indice_mese = curr_year_n_month [1] - 1

            #cambio il valore nella riga indice_anno nella colonna indice_mese di matrice_dati con il valore di time_series che sto analizzando
            matrice_dati [indice_anno] [indice_mese] = time_series [i] [1]

    #creo "risultati" una lista dove inserire i risultati delle medie
    risultati = []
    valore = 0
    
    #RAGIONAMENTO PER IL PROSSIMO CICLO:
    #La formula della differenza media è data da:
    #(b-a)+(c-b)+...+(z-y) / num
    #a causa della formula tutti gli elementi che non sono il primo (a) e l'ultimo (z) vengono semplificati: le proprietà delle operazioni infatti mi permettono di togliere le parentesi e riordinare, immaginando i - come +(-), ottenendo quindi al numeratore:
    #b+(-a)+c+(-b)+...+z+(-y)           =>
    #-a + b + (-b) + c + (-c) + ... + y + (-y) + z      =>
    #-a+z = z-a
    #cioè al numeratore ho la differenza tra l'ultimo e il primo elemento
    #riuscendo a sapere quanto vale il denumeratore, posso evitare di effettuare tutti i calcoli intermedi e andare a lavorare solo sul primo e sull'ultimo, gestendo quando eventualmente uno dei due o entrambi sono uguali a zero

    #itero su ciascuna colonna
    for i in range (0, 12):
        
        #la prima riga da cui devo partire è messa a -1 perché non appena entro nel while l'incremento di uno e quindi diventa zero. Se l'avessi messa a 0, avrei dovuto mettere nel while:
        #inizio = matrice_dati [r_ini] [i]
        #r_ini += 1
        #E quindi fuori dal while, dentro all'else, r_ini-=1. Ho pensato che per mantenere il codice sarebbe stato più semplice avere meno cambiamenti della variabile da controllare
        r_ini = -1

        #l'ultima riga da cui devo partire è uguale a len(matrice_dati) e non a (len(matrice_dati) - 1) per un ragionamento analogo a quello su r_ini
        r_fin = len(matrice_dati)

        #inizializzo inizio e fine a 0, sono rispettivamente il primo e l'ultimo valore non nulli della colonna e quelli utilizzati per la media
        inizio = 0
        fine = 0

        #fino a quando non ho un valore non nullo nella colonna o fino a quando non termino di analizzare i dati nella colonna, cerco il valore di inizio
        #nelle condizioni del while "r_ini < r_fin - 1" perché viene aumentato immediatamente dopo il valore di r_ini e se accettassi che r_ini sia minore stretto di r_fin (r_fin = len (matrice_dati)), avrei che nel caso di una colonna composta interamente da zeri, l'indice sarebbe uguale a len(matrice_dati), ma nella lista non ci sono valori in quell'indice, risultando in un errore
        while inizio == 0 and r_ini < r_fin - 1 :
            r_ini += 1
            inizio = matrice_dati [r_ini] [i]
        
        #se r_ini è uguale alla lunghezza della lista meno uno, vuol dire che l'ho attraversata tutta e, indifferentemente se il valore ultimo di inizio è uguale a zero o meno, non mi è possibile effettuare calcoli, quindi, come per istruzioni, il valore corrispondente a quel mese che verrà ritornato nella lista sarà uguale a 0
        if r_ini == (r_fin - 1):
            valore = 0
        
        #altrimenti, vuol dire che almeno per l'inizio posso effettuare i calcoli
        else:
            
            #fino a quanod non ho un valore non nullo nella colonna o fino a quando non termino di analizzare i dati nella colonna, cerco il valore di fine non nullo
            #nelle condizioni del while "r_fin > 0", così l'ultima volta che entro nel ciclo il suo valore sarà 1, e verrà quindi modificato in 0, rimanendo all'interno della lista
            #parto dall'ultima riga della matrice in maniera da trovare l'ultimo valore non nullo della colonna della matrice
            while fine == 0 and r_fin > 0:
                r_fin -= 1
                fine = matrice_dati [r_fin] [i]
            
            #se r_fin (cioè l'ultima riga della matrice nella cui colonna ho un valore non nullo) è uguale a r_ini (cioè la prima riga della matrice nella cui colonna ho un valore non nullo), il valore corrispondente a quel mese è 0, in quanto ho solamente un dato non nullo in tutta la colonna
            if r_fin == r_ini:
                valore = 0
            
            #altrimenti significa che ho almeno due valori con la riga distinta tra loro che mi permettono di effettuare i calcoli
            else:
                valore = (fine - inizio) / (r_fin - r_ini)

        #aggiungo il valore che ho calcolato alla lista contentente i risultati
        risultati.append(valore)

    return risultati


provina = CSVTimeSeriesFile(name="prova.csv")
testi = provina.get_data()
print(testi)
results = compute_avg_monthly_difference(testi, "1949", "1951")
print (results)