class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__ (self, name):
        self.name = name
    
    def get_data (self):
        #provo ad aprire il file
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except:
            raise ExamException ("Errore in apertura del file {}" .format(self.name))
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
                elements[-1] = elements[-1].strip()

                #datum è una lista contentente la prima parte di elements, cioè la data
                datum = 0
                #provo a dividere sulla "-"
                try:
                    datum = elements[0].split('-')
                #quando non è presente, l'elemento che sto analizzando non è una data nel formato richiesto e quindi lo ignoro o è la riga di intestazione e quindi la ignoro
                except:
                    datum = [0, 0]
                is_data = True
                if datum[0] not in range [1949, 1960]:
                    is_data = False
                if datum[1] not in range [1, 12]:
                    is_data = False
    
                # is_data mi permette di controllare se si tratta dell'intestazione, di righe fuori dal range o se si tratta di pezzi di testo che non c'entrano nulla
                if is_data is True:
                    #se il valore non è nullo o negativo ed è un intero
                    if elements[1] > 0 and elements[1] is int:
                        if elements[0] > last_date:
                            # Aggiungo alla lista gli elementi di questa linea
                            time_series.append(elements)
                            last_date = elements[0]
                        elif elements[0] == last_date:
                            raise ExamException ("L'elemento {} è duplicato" .format(elements[0]))
                        else:
                            raise ExamException ("L'elemento {} è fuori sequenza" .format(elements[0]))
                    #altrimenti ignoro, come da consegna
                
            
            # Chiudo il file
            my_file.close()
            
            # Quando ho processato tutte le righe, ritorno i dati
            return time_series