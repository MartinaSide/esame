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
            elements = line.split(',')

            # Con la funzione strip() tolgo il carattere di new line:
            elements[1] = elements[1].strip()
            #print (elements[1])

            #datum è una lista contentente la prima parte di elements, cioè la data
            datum = [0, 0]
            #provo a dividere sulla "-"
            if "-" in elements[0]:
                datum = elements[0].split('-')
            #quando non è presente, l'elemento che sto analizzando non è una data nel formato richiesto e quindi lo ignoro o è la riga di intestazione e quindi la ignoro
            is_data = True
            #print (datum[0])
            #print (datum[1])
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
                elements[1] = int(elements[1])

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
                    else:
                        raise ExamException(
                            "L'elemento {} è fuori sequenza".format(
                                elements[0]))
                    #altrimenti ignoro, come da consegna

        # Chiudo il file
        my_file.close()

        # Quando ho processato tutte le righe, ritorno i dati
        return time_series


def compute_avg_monthly_difference(time_series, first_year, last_year):
    #se last year e first_year non sono presenti nel file csv, bisogna alzare un'eccezione
    #time_series è la variabile con la lista di liste tratta dal File
    #print (type(first_year))
    if type(first_year) is not str:
        raise ExamException(
            "L'anno di inizio non è stato inserito come stringa")

    if type(last_year) is not str:
        raise ExamException("L'anno di fine non è stato inserito come stringa")

    if first_year < "1949":
        raise ExamException("L'anno di inizio è antecedente al 1949")

    if last_year > "1960":
        raise ExamException("L'anno di fine è successivo al 1960")

    if last_year <= first_year:
        raise ExamException(
            "L'intervallo di dati non è valido, si prega di inserire come secondo argomento della funzione l'anno di inizio e come terzo argomento l'anno di fine, che deve essere successivo a quello di inizio"
        )
    first_year = int (first_year)
    last_year = int (last_year)
    totale_dati = len(time_series)
    
    #creo la matrice
    curr_year_n_month = time_series[0] [0].split("-")
    curr_year_n_month [0] = int(curr_year_n_month[0])
    if curr_year_n_month [0] > first_year:
        raise ExamException ("Valore non presente nell'intervallo di dati")
    curr_year_n_month = time_series[len(time_series)-1] [0].split("-")
    curr_year_n_month [0] = int(curr_year_n_month[0])
    if curr_year_n_month [0] < last_year:
        raise ExamException ("Valore non presente nell'intervallo di dati")
    matrice_dati = []
    anno_precedente = first_year - 1
    mese_precedente = 12
    for i in range (0, totale_dati):
        curr_year_n_month = time_series [i] [0].split("-")
        curr_year_n_month[0] = int(curr_year_n_month[0])
        curr_year_n_month[1] = int (curr_year_n_month[1])
        if curr_year_n_month [0] < first_year:
            pass
        elif curr_year_n_month [0] > last_year:
            break
            #dato che la lista è ordinata cronologicamente, è certo che non ci sono più dati da analizzare
        else:
        #indice anno mi permette di capire in che riga della matrice sono
            indice_anno = len (matrice_dati) - 1
        #fino a quando 
            """
            while curr_year_n_month [0] > (anno_precedente + 1):
                matrice_dati.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                anno_precedente += 1
                """
            if curr_year_n_month [0] > anno_precedente:
                #aggiungo un numero di zeri alla riga dell'anno precedente della matrice, tali che ho un totale di 12 valori nella riga
                for j in range (mese_precedente, 12):
                    matrice_dati[indice_anno].append(0)
                #aggiunto una nuova riga alla matrice
                matrice_dati.append([])
                #ricalcolo il numero di righe della matrice
                indice_anno = len (matrice_dati) - 1
                for j in range (0, curr_year_n_month[1]-1):
                    matrice_dati [indice_anno].append (0)
                matrice_dati [indice_anno].append(time_series [i] [1])
                mese_precedente = curr_year_n_month [1]
                anno_precedente = curr_year_n_month [0]
                print ("Sono l'if, piacere!")
                print (matrice_dati)
            else:
                while curr_year_n_month [1] > mese_precedente + 1:
                    matrice_dati [indice_anno].append(0)
                    mese_precedente += 1
                matrice_dati [indice_anno].append(time_series [i] [1])
                mese_precedente = curr_year_n_month [1]
                print ("Sono l'else, e sono piu carino dell'if ehe!")
                print (matrice_dati)
    #print (matrice_dati)
    #aggiungo l'opportuna quantità di zeri all'ultima riga della matrice in modo che sia anche questa formata da 12 elementi
    print (len(matrice_dati[0]))
    lunghezza = len (matrice_dati) - 1
    lunghezza_ul_el = len (matrice_dati[lunghezza])
    for i in range (lunghezza_ul_el, 12):
        matrice_dati[lunghezza].append (0)
    print (len(matrice_dati[lunghezza]))
    print (matrice_dati)

    """
            
    flag_start_y = False
    flag_end_y = False

    for i in range(0, totale_dati):
        curr_year_n_month = time_series[i][0].split("-")
        
        if curr_year_n_month[0] == first_year:
            flag_start_y = True
        if curr_year_n_month[0] == last_year:
            flag_end_y = True

    if flag_start_y is False:
        raise ExamException(
            "Intervallo di tempo non valido: inizio non presente nel file")

    if flag_end_y is False:
        raise ExamException(
            "Intervallo di tempo non valido: data di fine non presente nel file"
        )
    """
    risultati = []
    precedente = 0
    contatore = 0
    somma = 0
    valore = 0

    for i in range (1, 13): #i = mese che sto analizzando, 1 = gennario, 2 = febbraio, ... non viene usato mai in un array o in una lista ma solo per confronto
        for j in range (0, totale_dati):
            curr_year_n_month = time_series[j][0].split("-")
            curr_year_n_month [1] = int (curr_year_n_month [1])
            if curr_year_n_month [1] == i:
                if precedente == 0:
                    precedente = time_series [j] [1]
                    print (precedente)
                else:
                    if time_series [j] [1] != 0:
                        differenza = time_series [j] [1] - precedente
                        somma = somma + differenza
                        contatore = contatore + 1
        if contatore > 0:
            valore = somma / contatore
        else:
            valore = somma
        differenza = 0
        contatore = 0
        somma = 0
        risultati.append(valore)

    

    return risultati


        


provina = CSVTimeSeriesFile(name="prova.csv")
testi = provina.get_data()
print(testi)
results = compute_avg_monthly_difference(testi, "1949", "1951")
print (results)
print (len(results))