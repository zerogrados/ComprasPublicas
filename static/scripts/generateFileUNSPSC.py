import csv


id_seg = ''
id_fami = ''
id_clas = ''
id_prod = ''
arraySegmento = []
arrayFamilia = []
arrayClase = []
arrayProducto = []

with open('clasificadorUNSPSC.csv', 'r') as csvfile:
    read_data = csv.reader(csvfile, delimiter=';')
    for row in read_data: 
        try:
            int(row[0])
            if id_seg != row[0]:
                arraySegmento.append({'id':row[0], 'title':row[1]})
                id_seg = row[0]
            else:
                continue
        except:
            continue

    for segmento in arraySegmento:
        with open('clasificadorUNSPSC.csv', 'r') as csvfile:
            read_data = csv.reader(csvfile, delimiter=';')
            for row in read_data:
                try:
                    int(row[0])
                    if (id_fami != row[2]) and (row[0] == segmento['id']):
                        arrayFamilia.append({'id':row[2], 'title':row[3]})
                        segmento['subs'] = arrayFamilia
                        id_fami = row[2]
                    else:
                        continue
                except:
                    continue
        arrayFamilia = []
    
    for segmento in arraySegmento:
        for familia in segmento['subs']:
            with open('clasificadorUNSPSC.csv', 'r') as csvfile:
                read_data = csv.reader(csvfile, delimiter=';')
                for row in read_data:
                    try:
                        int(row[0])
                        if (id_clas != row[4]) and (row[2] == familia['id']) and (row[0] == segmento['id']):
                            arrayClase.append({'id':row[4], 'title':row[5]})
                            familia['subs'] = arrayClase
                            id_clas = row[4]
                        else:
                            continue
                    except:
                        continue
            arrayClase = []
    
    for segmento in arraySegmento:
        for familia in segmento['subs']:
            for clase in familia['subs']:
                with open('clasificadorUNSPSC.csv', 'r') as csvfile:
                    read_data = csv.reader(csvfile, delimiter=';')
                    for row in read_data:
                        try:
                            int(row[0])
                            if (id_prod != row[6]) and (row[4] == clase['id']) and (row[2] == familia['id']) and (row[0] == segmento['id']):
                                arrayProducto.append({'id':row[6], 'title':row[7]})
                                clase['subs'] = arrayProducto
                                id_prod = row[6]
                            else:
                                continue
                        except:
                            continue
                arrayProducto = []
    print(arraySegmento)


