#!/path/to/python 
#-*- coding: UTF-8 -*-
#
# The script, consists in PYTHON exercise to identify smaller connections 
# between the habitat fragment (polygons // input shapefile), resulting in wildlife 
# corridors (lines // output shapefile). Basic Function: Create line between the closest 
# vertices of the polygons in shapefile. It works pairing all input polygons, but is limited to save 
# smaller lines (< 10000 m) 
#
# Basic Function: Create line between the closest vertices of the polygons in shapefile
# Created by Alex Mazurec in October/2015
# It works pairing all input polygons, but is limited to save smaller lines (< 10000 m) 
# Conditions of base shapefile: 1: isolated and non-overlapping polygons; 2: Single Class; 3: No multipart.
#

## módulos
import ogr, osgeo , math

## Funções
def lista_pontos(qual_feicao):    
    # abre Shapefile e retorna pontos da qual_feicao

    del xy[:]
    xy.append([])
    xy.append([])
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shape = driver.Open(onde + fragmentos, 0)

    layer = shape.GetLayer(0) # assume uma layer por aquivo
    num_feicoes = layer.GetFeatureCount()
    xy[0] = num_feicoes

    feicao = layer.GetFeature(qual_feicao) # assume a feição
    geometria = feicao.GetGeometryRef() # assume 1 objeto por poligono 
    objeto = geometria.GetGeometryRef(0) # assume somente um objeto dentro da feição
    num_pontos = objeto.GetPointCount()
    for pontos in range (0, num_pontos):
        lon, lat, z = objeto.GetPoint(pontos)
        xy[1].append((lon,lat))
    return xy

def estima():
# compara feiçoes e estima as menores ligações

    num_feicoes = lista_pontos(0)[0] #qual_feição // retorna num de feições e lista (x,y)
    for pol1 in range(0, num_feicoes): # 1o loop polígonos
        xy1 = lista_pontos(pol1)[1]
        for pol2 in range((pol1 + 1), num_feicoes): # loop nos demais polígonos
            xy2 = lista_pontos(pol2)[1]
            for vert1 in range(0, len(xy1)): # loop nos vértices do 1o polígono
                for vert2 in range(0, len(xy2)): # loop nos vértices do 2o polígono
                    linha = osgeo.ogr.Geometry(osgeo.ogr.wkbLineString)
                    linha.AddPoint(xy1[vert1][0],xy1[vert1][1]) #ponto inicial da linha nn
                    linha.AddPoint(xy2[vert2][0],xy2[vert2][1]) #ponto final da linha nn
                    H = linha.Length()
                    Ho.append([H,linha]) 
                    Ho.sort()  # escolhe menor ligação
                    Ho.pop(1)
            if Ho[0][0] <= 10000: # tamanho máximo da ligação
                elo.append([pol1,pol2,Ho[0][1]])
                Ho[0][0] = 1000000000 # corrige regra de ordenamento
    return elo  

def cria_ln(elo):
    # Cria o shp de linha e anota par como nome
    Referencia_I = osgeo.osr.SpatialReference() #sistema de referência
    Referencia_I.ImportFromProj4(referencia) 
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile') 

    shp = driver.CreateDataSource(onde + ligacoes) #local e nome composto do shp de saída
    camada = shp.CreateLayer('customs',  Referencia_I, osgeo.ogr.wkbLineString) 
    camada_defn = camada.GetLayerDefn() 
    novo = ogr.FieldDefn('Par', ogr.OFTString) #cria campo 'par'
    camada.CreateField(novo)
    novo = ogr.FieldDefn('Tamanho', ogr.OFTReal) #cria campo
    camada.CreateField(novo)

    for nn in range (0, len(elo)):

        linha = elo[nn][2]
        ## insere linhas no shp
        feicao = osgeo.ogr.Feature(camada_defn)
        feicao.SetGeometry(linha)
        feicao.SetFID(nn)
        camada.CreateFeature(feicao)
        #anota a relação no campo 'par'
        par = str(elo[nn][0]) + "_" + str(elo[nn][1])
        feicao.SetField('Par', par) # anota no campo pelo indice nn
        feicao.SetField('Tamanho', int(linha.Length())) # anota no campo pelo indice nn
        camada.SetFeature(feicao)        

    shp.Destroy() # fecha o shapefile

## declaração de variaveis
onde = "/home/user/Documentos/Py/qgis/" #caminho do shp
referencia = "+proj=utm +zone=24 +south +ellps=aust_SA +towgs84=-57,1,-41,0,0,0,0 +units=m +no_defs"

fragmentos = "pg_fragmentos.shp" # nome shape de fragmentos
ligacoes = "ln_ligacoes_de_" + fragmentos #nome do arquivo de ligacoes

xy = ([])
xy1 = ([])
xy2 = ([])
elo = ([])
Ho = [()]


## maquina
elo = estima()
cria_ln(elo)
