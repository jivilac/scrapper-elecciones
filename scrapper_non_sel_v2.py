dict_results = {}
dict_check = {}
for i in range(6,29):
    distrito =  i
    if distrito <10:
        url_d = 'https://www.servelelecciones.cl/data/elecciones_convencionales_g/computo/distritos/600' +  str(distrito) +'.json'
        url_d_c = 'https://www.servelelecciones.cl/data/elecciones_convencionales_g/filters/comunas/bydistrito/600' + str(distrito) + '.json'
        comuna = requests.get(url_d_c )
    else:
        url_d = 'https://www.servelelecciones.cl/data/elecciones_convencionales_g/computo/distritos/60' +  str(distrito) +'.json'
        url_d_c = 'https://www.servelelecciones.cl/data/elecciones_convencionales_g/filters/comunas/bydistrito/60' + str(distrito) + '.json'
        comuna = requests.get(url_d_c )
    data = pd.DataFrame(columns = ['Lista/Pacto', 'Partido', 'Votos','comuna','comuna_id',
    'circ_electoral','circ_electoral_id','mesa','id_mesa', 'Porcentaje', 'Candidatos',
     'Electo', None])
    for c in comuna.json():
        info_comuna = requests.get('https://www.servelelecciones.cl/data/elecciones_convencionales_g/filters/circ_electoral/bycomuna/'+ str(c['c']) + '.json')
        for ic in info_comuna.json():
            mesas = requests.get('https://www.servelelecciones.cl/data/elecciones_convencionales_g/filters/mesas/bycirc_electoral/' + str(ic['c']) + '.json')
            print(ic['d'])
            for m in mesas.json():
                mesa = requests.get('https://www.servelelecciones.cl/data/elecciones_convencionales_g/computomesas/' + str(m['c']) + '.json')
                    #data = pd.DataFrame(columns = mesa.json()['title'].values())
                for d in mesa.json()['data']:
                    data_i= pd.DataFrame(d['sd'])
                    data_i  = data_i.drop(columns='sd')
                    data_i.columns = ['Candidatos','Partido','Votos','Porcentaje','Electo',None]
                    data_i['Lista/Pacto'] = d['a']
                    data_i['mesa'] = m['d']
                    data_i['id_mesa'] = int(m['c'])
                    data_i['circ_electoral'] = ic['d']
                    data_i['circ_electoral_id'] = int(ic['c'])
                    data_i['comuna'] = c['d']
                    data_i['comuna_id'] = int(c['c'])
                    data_i['distrito'] = distrito
                    data = data.append(data_i)
    dict_results['Distrito' + str(distrito)] = data

for i in dict_results.keys():
    dict_results[i].to_csv(str(i)+ '.csv', encoding='latin-1')
