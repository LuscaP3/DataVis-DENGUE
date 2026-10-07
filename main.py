import json
from visualizations import *

# =-=-=-=-=-=-=-= Abir dados =-=-=-=-=-=-=-=

with open("data/sintomas_sexo.json", "r", encoding="utf-8") as arquivo:
    sint_sexo = json.load(arquivo)

with open("data/sintomas_idade.json", "r", encoding="utf-8") as arquivo:
    sint_idade = json.load(arquivo)

with open("data/diabetes_gravidade.json", "r", encoding="utf-8") as arquivo:
    grav_diabetes = json.load(arquivo)

with open("data/gestantes_frequencia.json", "r", encoding="utf-8") as arquivo:
    freq_gestantes = json.load(arquivo)


# =-=-=-=-=-=-=-= Gerar visualizações =-=-=-=-=-=-=-=

fem = sint_sexo[0]
masc = sint_sexo[1]

fem_sintomas = fem["sintomas"]
dados_fem = [fem_sintomas["FEBRE"], fem_sintomas["MIALGIA"], fem_sintomas["CEFALEIA"], fem_sintomas["EXANTEMA"], fem_sintomas["VOMITO"], fem_sintomas["NAUSEA"], fem_sintomas["DOR_COSTAS"], fem_sintomas["CONJUNTVIT"], fem_sintomas["ARTRITE"], fem_sintomas["ARTRALGIA"], fem_sintomas["PETEQUIA_N"], fem_sintomas["LEUCOPENIA"], fem_sintomas["LACO"], fem_sintomas["DOR_RETRO"]]
total_fem = fem["total"]

masc_sintomas = masc["sintomas"]
dados_masc = [masc_sintomas["FEBRE"], masc_sintomas["MIALGIA"], masc_sintomas["CEFALEIA"], masc_sintomas["EXANTEMA"], masc_sintomas["VOMITO"], masc_sintomas["NAUSEA"], masc_sintomas["DOR_COSTAS"], masc_sintomas["CONJUNTVIT"], masc_sintomas["ARTRITE"], masc_sintomas["ARTRALGIA"], masc_sintomas["PETEQUIA_N"], masc_sintomas["LEUCOPENIA"], masc_sintomas["LACO"], masc_sintomas["DOR_RETRO"]]
total_masc = masc["total"]

sintomas = ['Febre', 'Mialgia', 'Cefaleia', 'Exantema', 'Vômito', 'Náusea', 'Dor nas costas', 'Conjuntivite', 'Artrite', 'Artralgia', 'Petéquias', 'Leucopenia', 'Prova do laço', 'Dor retro-orbital']

diverging_bar_chart('Variação nos sintomas de acordo com o sexo', dados_masc, 'Masculino', '#8487e8', total_masc, dados_fem, 'Feminino', '#e884cd', total_fem, 4, sintomas, 'Sintomas', arquivo = 'output/diverging_bar_chart.png')

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

sintomas = ['Febre', 'Mialgia', 'Cefaleia', 'Exantema', 'Vômito', 'Náusea', 'Dor nas costas', 'Conjuntivite', 'Artrite', 'Artralgia', 'Petéquias', 'Leucopenia', 'Prova do laço', 'Dor retro-orbital']

grupos = []
dados = []
totais = []
for i in range(0, len(sint_idade)):
    dados.append([sint_idade[i]["sintomas"]["FEBRE"], sint_idade[i]["sintomas"]["MIALGIA"], sint_idade[i]["sintomas"]["CEFALEIA"], sint_idade[i]["sintomas"]["EXANTEMA"], sint_idade[i]["sintomas"]["VOMITO"], sint_idade[i]["sintomas"]["NAUSEA"], sint_idade[i]["sintomas"]["DOR_COSTAS"], sint_idade[i]["sintomas"]["CONJUNTVIT"], sint_idade[i]["sintomas"]["ARTRITE"], sint_idade[i]["sintomas"]["ARTRALGIA"], sint_idade[i]["sintomas"]["PETEQUIA_N"], sint_idade[i]["sintomas"]["LEUCOPENIA"], sint_idade[i]["sintomas"]["LACO"], sint_idade[i]["sintomas"]["DOR_RETRO"]])
    grupos.append(sint_idade[i]["faixa_etaria"])
    totais.append(sint_idade[i]["total"])

cor_min = "#AAE7FA"
cor_max = "#297991"

mapa_de_calor(grupos, sintomas, dados, totais, cor_max, cor_min, arquivo = 'output/mapa_de_calor.png')

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

# Grave, Não grave, descartado, Inconclusivo, outros
classificacao_diabetes = [0, 0, 0, 0, 0]
classificacao_nao_diabetes = [0, 0, 0, 0, 0]

# 01 Dengue clássico
# 02 Dengue com complicações
# 03 Febre hemorrágica da dengue
# 04 Síndrome do choque da dengue
# 05 Descartado
# 08 Inconclusivo
# 10 Dengue
# 11 Dengue com sinais de alarme
# 12 Dengue grave
# 13 Chikungunya

grave = [2, 3, 4, 11, 12]
nao_grave = [1, 10]
descartado = [5]
inconclusivo = [8]
outros = [3]

for i in grav_diabetes:
    if(i["DIABETES"] == 1):
        if(i["CLASSI_FIN"] in grave):
            classificacao_diabetes[0] += i["quantidade"]

        if(i["CLASSI_FIN"] in nao_grave):
            classificacao_diabetes[1] += i["quantidade"]

        if(i["CLASSI_FIN"] in descartado):
            classificacao_diabetes[2] += i["quantidade"]
        
        if(i["CLASSI_FIN"] in inconclusivo):
            classificacao_diabetes[3] += i["quantidade"]

        if(i["CLASSI_FIN"] in outros):
            classificacao_diabetes[3] += i["quantidade"]

    if(i["DIABETES"] == 2):
        if(i["CLASSI_FIN"] in grave):
            classificacao_nao_diabetes[0] += i["quantidade"]

        if(i["CLASSI_FIN"] in nao_grave):
            classificacao_nao_diabetes[1] += i["quantidade"]

        if(i["CLASSI_FIN"] in descartado):
            classificacao_nao_diabetes[2] += i["quantidade"]
        
        if(i["CLASSI_FIN"] in inconclusivo):
            classificacao_nao_diabetes[3] += i["quantidade"]

        if(i["CLASSI_FIN"] in outros):
            classificacao_nao_diabetes[3] += i["quantidade"]


dados = [classificacao_diabetes, classificacao_nao_diabetes]
cores = ["#aa3b3b", "#3baa4a", "#aaa33b", "#6f3baa", "#423baa"]

mosaic_plot("Agravamento em casos com diabetes", dados, ['Diabéticos', 'Não diabéticos'], ["Grave", "Não grave", "descartado", "Inconclusivo", "outros"], cores, arquivo = 'output/mosaic_plot.png')

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

# 1 Primeiro Trimestre 
# 2 Segundo Trimestre
# 3 Terceiro Trimestre 
# 4 Idade gestacional ignorada 
# 5 Não 
# 6 Não se aplica 
# 9 ignorado

# 01 Dengue clássico
# 02 Dengue com complicações
# 03 Febre hemorrágica da dengue
# 04 Síndrome do choque da dengue
# 05 Descartado
# 08 Inconclusivo
# 10 Dengue
# 11 Dengue com sinais de alarme
# 12 Dengue grave
# 13 Chikungunya

grupos = ["Primeiro Trimestre", "Segundo Trimestre", "Terceiro Semestre"]
dados_gravidade = [[0 ,0 ,0 ,0 ,0], [0 ,0 ,0 ,0 ,0], [0 ,0 ,0 ,0 ,0]] # ordenado em relação às categorias
descricao = ["Grave", "Não grave", "Descartado", "Inconclusivo", "Outros"]
cores = ["#aa3b3b", "#3baa4a", "#aaa33b", "#6f3baa", "#423baa"]

grave = [2, 3, 4, 11, 12]
nao_grave = [1, 10]
descartado = [5]
inconclusivo = [8]
outros = [3, 9, 0, '']

for gest in freq_gestantes:
    if(gest["CS_GESTANT"] == 1):
        if(gest["CLASSI_FIN"] in grave):
            dados_gravidade[0][0] += gest["quantidade"]
        
        elif(gest["CLASSI_FIN"] in nao_grave):
            dados_gravidade[0][1] += gest["quantidade"]
        
        elif(gest["CLASSI_FIN"] in descartado):
            dados_gravidade[0][2] += gest["quantidade"]
                
        elif(gest["CLASSI_FIN"] in inconclusivo):
            dados_gravidade[0][3] += gest["quantidade"]
        
        elif(gest["CLASSI_FIN"] in outros):
            dados_gravidade[0][4] += gest["quantidade"]

    elif(gest["CS_GESTANT"] == 2):
        if(gest["CLASSI_FIN"] in grave):
            dados_gravidade[1][0] += gest["quantidade"]
                
        elif(gest["CLASSI_FIN"] in nao_grave):
            dados_gravidade[1][1] += gest["quantidade"]
                
        elif(gest["CLASSI_FIN"] in descartado):
            dados_gravidade[1][2] += gest["quantidade"]
                        
        elif(gest["CLASSI_FIN"] in inconclusivo):
            dados_gravidade[1][3] += gest["quantidade"]
                
        elif(gest["CLASSI_FIN"] in outros):
            dados_gravidade[1][4] += gest["quantidade"]

    elif(gest["CS_GESTANT"] == 3):
        if(gest["CLASSI_FIN"] in grave):
            dados_gravidade[2][0] += gest["quantidade"]
                
        elif(gest["CLASSI_FIN"] in nao_grave):
            dados_gravidade[2][1] += gest["quantidade"]
                
        elif(gest["CLASSI_FIN"] in descartado):
            dados_gravidade[2][2] += gest["quantidade"]
                        
        elif(gest["CLASSI_FIN"] in inconclusivo):
            dados_gravidade[2][3] += gest["quantidade"]
                
        elif(gest["CLASSI_FIN"] in outros):
            dados_gravidade[2][4] += gest["quantidade"]



barras_empilhadas("Agravamento em gestantes", grupos, dados_gravidade, descricao, cores, arquivo = 'output/barras_empilhadas.png')