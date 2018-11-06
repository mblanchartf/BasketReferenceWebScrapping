from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd

llista_equips_est = ['TOR', 'MIL', 'IND', 'BOS', 'PHI', 'CHA', 'DET', 'MIA', 'ORL', 'NJN', 'ATL', 'NYK', 'CHI', 'WAS', 'CLE']
llista_equips_oest = ['GSW', 'DEN', 'POR', 'SAS', 'SAC', 'LAC', 'OKC', 'MEM', 'HOU', 'NOH', 'LAL', 'UTA', 'MIN', 'DAL', 'PHO']

equips_valids = llista_equips_est + llista_equips_oest

def get_url_content(url):
    """
    Obtenim el contingut the la URL. 
    Retorna None si no hem obtingut una request amb èxit
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if es_resposta_la_correcta(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error accedint a {0} : {1}'.format(url, str(e)))
        return None
    

def es_resposta_la_correcta(resp):
    """
    Retorna True si la resposta és correcta. False si no ho és. 
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
    
def obten_estadistiques_equip(equip):
    """
    Retorna un dataframe amb la informació obtinguda del equip indicat
    """
    
    # Obtenim la informació de la pàgina del equip
    contingut = get_url_content("https://www.basketball-reference.com/teams/" + equip + "/")
    
    # Transformem al format que enten BeautifulSoup
    html = BeautifulSoup(contingut, 'html.parser')
    
    # Anem a iterar en les taules
    data = []
    for tr in html.findAll('tr'):
        row = []

        # Guardem la capçalera
        for th in tr.findAll('th'):
            row.append(th.text)

        # Guardem les dades de cada temporada    
        for td in tr.findAll('td'):
            row.append(td.text)
        
        # Afegim una nova fila
        data.append(row)
    
    capcaleres = data.pop(0)        
    
    return pd.DataFrame(data, columns=capcaleres)

def obten_informacio_equip(llista_equips):
    """
    Retorna un dataframe amb la informació de tots els equip indicat com a argument
    """
    
    # Inicialitzem les variables de suport
    df = pd.DataFrame()
    
    # Fem un loop amb tots els equips
    for equip in llista_equips:
        
        # Comprovem si l'equip és valid
        equip_valid(equip)            
        
        # Cridem la funció previament creda
        df_tmp = obten_estadistiques_equip(equip) 
        
        # Afegim la informació al dataframe
        df = pd.concat([df, df_tmp], ignore_index = True)
    
    return df

def equip_valid(equip):
    """
    Checkeja si l'equip es valid o no
    """

    if equip not in equips_valids:
        raise Exception("Equip no vàlid")
        
    return True

def obten_llista_jugadors_per_equip(equip):
    """
    Funció que retorna la plantilla actual de l'equip donat
    """
    
    llista = []
    
    # Mirem si l'equip és valid
    equip_valid(equip)
    
    # Maoejem l'equip que ha canviat de nom recentment
    equip = mapeja_equips_nous(equip)
    
    # Mitjançant request obtenim el roster
    contingut = get_url_content("https://www.basketball-reference.com/teams/" + equip + "/2019.html")

    # Transformem al format que enten BeautifulSoup
    html = BeautifulSoup(contingut, 'html.parser')
    
    # Anem a iterar en les taules
    data = []
    for url in html.findAll('td', {'data-stat':'player'}):
        a = url.find('a')
        llista.append(a['href'])
        
    return llista

def mapeja_equips_nous(equip):
    """
    Mapeja els equips que han canviat de nom recentment
    """
    
    if equip is 'NOH':
        return 'NOP'
    elif equip is 'CHA':
        return 'CHO'
    elif equip is 'NJN':
        return 'BRK'
    else:
        return equip
    
def obten_estadistiques_jugadors(jugador_url):
    """
    Funció que recopila la informació dels jugadors en les diferents temporades NBA
    """
    
    # Obtenim la informació de la pàgina del jugador
    contingut = get_url_content("https://www.basketball-reference.com" + jugador_url)
    
    # Transformem al format que enten BeautifulSoup
    html = BeautifulSoup(contingut, 'html.parser')
    
    # Anem a treure el nom del jugador
    nom_jugador = html.select('h1')[0].text
    
    # Anem a iterar en les taules
    data = []
    career_flag = False
    for tr in html.findAll('tr'):
        row = []

        # Guardem la capçalera
        for th in tr.findAll('th'):
            row.append(th.text)

            # Acabem l'scrapping si trobem la capcalera 'career'
            if th.text == 'Career':
                career_flag = True
        
        # Si hem arribat a la segona capçalera, tallem
        if career_flag:
            break

        # Guardem les dades de cada temporada    
        for td in tr.findAll('td'):
            row.append(td.text)
        
        # Afegim una nova fila
        data.append(row)
    
    # Si no té experiencia, tornem dades nules
    if data == []:
        return [], '', False
    
    capcaleres = data.pop(0)        
    
    return pd.DataFrame(data, columns=capcaleres), nom_jugador, True

def obten_estadistiques_jugadors_equip(equip):
    """
    Funció que obté totes les estadistiques dels jugadors del equip donat
    """ 
    
    # Obtenim les URLs dels jugadors
    llista_jugadors = obten_llista_jugadors_per_equip(equip)
           
    # Inicialitzem les variables de suport
    df = pd.DataFrame()
    
    # Fem un loop amb tots els equips
    for jugador in llista_jugadors:         
        
        # Cridem la funció previament creada
        df_tmp, nom_jugador, experience = obten_estadistiques_jugadors(jugador) 
        
        # Afegim la columna del jugador si la data no és buida
        if experience:
            df_tmp['Player'] = nom_jugador
        
            # Afegim la informació al dataframe
            df = pd.concat([df, df_tmp], ignore_index = True)
    
    return df

def crea_fitxer_csv(dataframe, filename):
    """
    Funció que crea un fitxer CSV donat un dataframe
    """
    
    dataframe.to_csv(filename, sep='\t', encoding='utf-8')
    print("File created: " + filename)

