# Usarei a função exit() e sleep() mais tarde, logo dou um import aqui.
from sys import exit
from time import sleep
from datetime import datetime
from os import getcwd, path
import pandas as pd


# OBJETIVO: GERAR ORÇAMENTOS PARA LOCAÇÃO.
# REGRAS QUE SÃO APLICADAS
# A R.M (Empresa exemplo) trabalha com 3 tipos de locação e valores padrões:

# 1) Apartamentos R$ 700,00 / 1 Quarto
#   1.1) Caso opte por Apartamento 2 Quartos = + R$ 200,00 na mensalidade;
#   1.2) com Garagem = Acréscimo de R$ 300,00 na mensalidade;
#   1.3) Desconto aplicado de 5% no valor Aluguel para pessoas que não possuirem crianças

# 2) Casas R$ 900,00 / 1 Quarto
#   2.1) Caso opte por Casa 2 Quartos = + R$ 250,00 na mensalidade;
#   2.2) com Garagem = Acréscimo de R$ 300,00 na mensalidade;

# 3) Estudio R$ 1200,00
#   3.1) Caso queira adicionar vagas de Garagem:
#        2 Vagas garagem iniciais = + R$ 250,00 na mensalidade;
#        Caso queira mais vagas, acréscimo de R$ 60,00 cada.

# Regra geral:
#   O valor do contrato pode ser parcelado em até 5x.

# Anotações pessoais:
# Primeiro, criar um menu em Terminal definindo as regras base (local + valor base)
# Devo pensar que terá Valor de ACRÉSCIMO APENAS e valor de acréscimo sobre PARCELA

class gerarOrçamento():
    def __init__(self):
        self.locacao = ["Apartamento", "Casa", "Estudio"]
        self.name = ""
        self.selection = ""
        self.value = 0
        self.installment = 1
        self.room = 1 # Como o mínimo começa em 1 quarto, defini o início em 1 em vez de 0
        self.garage = 0
        self.discount = False
    def infoColect(self):
        # Essa função coleta as informações usadas tanto para o cálculo quanto geração de arquivo
        # Além disso faz uma checagem simples caso a opção não esteja no escopo do menu
        
        # Aqui eu defino o nome do cliente, para facilitar na hora de gerar arquivo .csv
        self.name = input(f"{"---"*15}\nDigite o nome do cliente: ").strip().title()
        
        print(f'''{"=-="*15}
    Escolha qual o tipo de locação:
        1) Apartamento
        2) Casa
        3) Estudio
    X) Voltar''')
        option = input(f"{"Escolha uma das opções a acima:".center(45)}\n").strip().upper()
        
        while option not in ("1", "2", "3", "X"):
            print(f"{"---"*15}\n{"A opção escolhida não é válida.".center(45)}\n{"---"*15}")
            sleep(1)
            print('''   Escolha qual o tipo de locação:
        1) Apartamento
        2) Casa
        3) Estudio
    X) Voltar''')
            option = input(f"{"Escolha uma das opções a acima:".center(45)}\n").strip().upper()
            
        if option == "X":
            self.terminal()
        elif option == "1":
            self.value = 700
            self.selection = self.locacao[0]
        elif option == "2":
            self.value = 900
            self.selection = self.locacao[1]
        else:
            self.value = 1200
            self.selection = self.locacao[2]
        
        # Caso NÃO FOR um Estudio (vulgo Apartamento ou Casa), pergunta sobre quartos
        if self.selection not in "Estudio":
            option = input(f"{"-x="*15}\nDeseja alugar um(a) {self.selection} com 2 quartos? [S/N]\n").strip().upper()
            while option not in ("SN"):
                print(f"{"---"*15}\n{"Erro. Opção inválida, tente novamente."}\n{"---"*15}")
                sleep(1)
                option = input(f"Deseja alugar um(a) {self.selection} com 2 quartos? [S/N]\n").strip().upper()
            
            if option == "S":
                self.room = 2
        
        # Caso FOR UM APARTAMENTO, pergunta se o cadastro se enquadra na regra 1.3, desconto se as pessoas
        # que alugarem não possuirem crianças
        
        if self.selection == "Apartamento":
            option = input("As pessoas que alugarem tem crianças? [S/N]\n").strip().upper()
            while option not in ("SN"):
                print(f"{"---"*15}\n{"Erro. Opção inválida, tente novamente."}\n{"---"*15}")
                sleep(1)
                option = input("As pessoas que alugarem tem crianças? [S/N]\n").strip().upper()
            if option == "N":
                self.discount = True
        
        # Definindo quantas garagens.
        if self.selection != "Estudio":
            option = input("Deseja adicionar vaga de garagem? [S/N]\n").strip().upper()
            while option not in ("SN"):
                print(f"{"---"*15}\n{"Erro. Opção inválida, tente novamente."}\n{"---"*15}")
                sleep(1)
                option = input("Deseja adicionar vaga de garagem? [S/N]\n").strip().upper()
            if option == "S":
                self.garage = 1
        
        elif self.selection == "Estudio":
            option = input("Deseja adicionar 2 vagas de garagem? [S/N]\n").strip().upper()
            while option not in ("SN"):
                print(f"{"---"*15}\nErro. Opção inválida, tente novamente.\n{"---"*15}")
                sleep(1)
                option = input("Deseja adicionar 2 vagas de garagem? [S/N]\n").strip().upper()
            if option == "S":
                self.garage = 2
            
            if self.garage > 0:        
                try:
                    option = int(input(f'''{"-=-"*15}
{"Deseja adicionar vagas de garagem adicionais? Digite a quantidade.\n[Digite 0 se não quiser nenhuma]: \n".center(45)}'''))
                except ValueError:
                    while type(option) != int():
                        print(f"{"---"*15}\nValor inválido\n{"---"*15}")
                        sleep(1)
                        option = int(input(f"{"Você deseja alugar com quantas garagens?\n[Digite 0 se não quiser nenhuma]: \n".center(45)}"))
            
                if option > 0:
                    self.garage += option

            # Quantidade de Parcelas (Installments)
        try:
                option = int(input(f'''{"-=-"*15}
{"Quantas parcelas deseja pagar? \n[Digite 1 se for à vista]\n".center(45)}'''))
                if not isinstance(option, int):
                    raise TypeError("Valor não pode ser diferente de Int")
                elif option > 5 or option <= 0:
                    raise ValueError("Valor não pode ser maior que 5 ou menor ou igual 0")
        except ValueError or TypeError:
            while not isinstance(option, int) or option > 5 or option <= 0:
                print(f"{"---"*15}\nValor inválido\n{"---"*15}")
                sleep(1)
                option = int(input(f"{"Quantas parcelas deseja pagar? [Digite 1 se for à vista]\n".center(45)}"))
        
        if option > 1:
            self.installment = option
        
        # resumo pra debug
        if self.discount:
            ativo = "Ativo"
        else:
            ativo = "Indisponível"
        
        info_Parcela = self.calculate()
        # Aqui usa da função calculate() para obter resultados importantes de relação financeira
        # (valor de parcela, antes dos acréscimos, depois dos acréscimos, quantidade de acréscimo)
        # os valores possíveis são: Valor (obrigatorio), ValorAC (obrigatorio), Discount, Acrescimo
        
        print(f'''{"=-="*15}\nAté o momento, o orçamento segue da seguinte forma:
    Você decidiu alugar: um(a) {self.selection};''', end="")
        if info_Parcela["Tipo"][0] == "Apartamento":
            print(f";\n    Status de Desconto: {ativo}", end="")
        if info_Parcela["Garagem"][0] > 0:
            print(f";\n    Vagas para garagem: {self.garage} vaga(s)", end="")
        if info_Parcela["Tipo"][0] != "Estudio":
            print(f";\n    Quartos: {self.room}.")
        
        print(f'''\n{"Informações Financeiras:".center(45)}
 Valor Inicial: R$ {self.value}
 Valor da Parcela (antes do acréscimo):  R$ {info_Parcela["ValorAC"][0] / self.installment:.2f}''')
        
        if info_Parcela["Acrescimo"][0] > 0:
            print(f" Valor de acréscimos:     + R$ {info_Parcela["Acrescimo"][0]:.2f}")
        
        # gera o texto de forma dinâmica (A vista ou x Parcelas)
        if info_Parcela["Parcelas"][0] == 1:
            print(" Quantidade de Parcelas: À Vista")
        else:
            print(f" Quantidade de Parcelas: {info_Parcela["Parcelas"][0]}x")
        
        if info_Parcela["Desconto"][0] > 0:
            print(f" Valor de desconto por parcela | - R$ {info_Parcela["Desconto"][0]:.2f}")
        
        print(f"Valor de cada parcela: R$ {info_Parcela["Valor"][0]:.2f}")
        
        option = input('''\n
    1) Exportar para arquivo .csv
 X) Voltar

Escolha uma das opções acima: ''').strip().upper()
        
        while option not in ("1", "X"):
            print(f"{"=x="*15}\n{"Erro, opção selecionada inválida".center(45)}\n{"=x="*15}")
            sleep(1)
            option = input('''\n
    1) Exportar para arquivo .csv
 X) Voltar

Escolha uma das opções acima: ''').strip().upper()
        if option == "X":
            self.terminal()
        elif option == "1":
            self.generateFile(info_Parcela)
        
    def calculate(self):
        # Aqui abaixo está sendo calculado o valor inicial de cada parcela, depois adicionado
        # qualquer acréscimo se relevante.
        
        # Faz o cálculo de:
        # Valor da parcela (após descontos), Valor do desconto, salva o valor antes do desconto
        # Valor de acréscimos
        
        installmentValue = self.value / self.installment 
        installmentAdditions = 0
        installmentVBefore = self.value
        
        # define o dicionário
        installmentInfo = {"NomeCliente": [self.name], "Tipo": [self.selection], "Quartos": [self.room], "Garagem": [self.garage], "Parcelas": [self.installment], "Valor": [0], "ValorAC": [0], "Acrescimo": [0], "Desconto": [0]}
        
        if self.room == 2: # Aqui está sendo somado acréscimo se for Apartamento/Casa com 2 quartos
            if self.selection == "Apartamento":
                installmentValue += 200
                installmentAdditions += 200
            elif self.selection == "Casa":
                installmentValue += 250
                installmentAdditions += 250
        
        if self.garage > 0: # Aqui se refere ao valor das vagas de Garagem para Apartamento/Casa ou Estudio
            if self.selection == "Apartamento" or self.selection == "Casa":
                installmentValue += 300
                installmentAdditions += 300
            elif self.selection == "Estudio":
                installmentValue += 250
                installmentAdditions += 250
                # Abaixo, caso exista mais que 2 vagas, adiciona o acréscimo de R$ 60,00 por vaga
                installmentValue += 60*(self.garage-2) # Se só houverem 2 vagas de garagem, o -2 transforma essa conta em 60 * 0, ou seja valordaParcela + 0
                installmentAdditions += 60*(self.garage-2)
        
        # Atualiza o dicionário com o valor da parcela, caso possuir desconto, atualizará a lista mais abaixo.
        installmentInfo["Valor"][0] = installmentValue
        
        # Adiciona o valor antes do desconto:
        installmentInfo["ValorAC"][0] = installmentVBefore
        
        if self.discount: # Caso possua desconto de não possuir crianças, reduz o valor da parcela em 5%
            installmentDiscount = installmentValue * 0.05
            # Adiciona os valores de Desconto
            installmentInfo["Desconto"][0] = installmentDiscount
            
            installmentValue -= installmentDiscount
            # Atualiza o valor da Parcela após o desconto
            installmentInfo["Valor"][0] = installmentValue
        
        # Adiciona o valor de acréscimos ao dicionário
        if installmentAdditions > 0:
            installmentInfo["Acrescimo"][0] = installmentAdditions
        
        # Por fim retorna o dicionário para a classe.
        return installmentInfo
    def terminal(self):
        # Essa função é o começo de tudo, ela vai levar o usuário pelos menus, podendo informar como
        # funciona os parâmetros caso haja dúvida.
        
        print(f'''{("=x="*15)}
{"Bem vindo ao modo Terminal".center(45)}
{("=x="*15)}
{"Escolha uma opção para continuar:".center(45)}
    1) Fazer orçamento
    2) Ver informações de locação.
    X) Sair''')
        option = str(input("Digite a opção: \n".center(45))).upper().strip()
        
        # Caso o usuário erre as opções do menu ↓
        while option not in ("1", "2", "X"):
            option = str(input("Tente novamente, digite a opção: \n".center(45))).upper().strip()
        if option == "X": # Sair
            print(f"{"---"*15}\n{"Saindo com sucesso!".center(45)}\n{"---"*15}")
            sleep(0.5) # Efeito visual
            exit()
        if option == "1":
            self.infoColect()
        elif option == "2": # Ver opções de locação
            option2 = ""
            print(f'''{"---"*15}
 Existem as seguintes formas de alugar imóveis:
    {self.locacao[0]} | Valor: R$   700,00
    {self.locacao[1] + " "*7} | Valor: R$   900.00
    {self.locacao[2] + " "*4} | Valor: R$ 1.200,00

{"Quarto adicional".center(45)}
 Caso for decidido ter um quarto adicional
 o valor segue como abaixo:
 
 Para Apartamentos:
    Acréscimo de R$ 200,00 na mensalidade

 Para Casas:
    Acréscimo de R$ 250,00 na mensalidade

{"Garagem".center(45)}
 Para Apartamentos e Casas:
    Vaga de Garagem: Adicional de R$ 300,00*
 Para Estúdios:
    2 Vagas iniciais: R$ 250,00*
    Vagas adicionais: R$  60,00* por vaga

Legenda:
* valores são somados no valor da mensalidade.

{"Caso Especial".center(45)}
 Caso a pessoa deseje alugar um Apartamento, 
ela pode receber 5% de desconto nas parcelas
caso não possua crianças.

1) Voltar
X) Sair''')
            option2 = str(input("Digite a opção: \n".center(45))).upper().strip()
            # Caso o usuário erre as opções do menu ↓
            while option2 not in ("1", "X"):
                option2 = str(input("Tente novamente, digite a opção: \n".center(45))).upper().strip()
            
            if option2 == "X": # Sair
                print(f"{"---"*15}\n{"Saindo com sucesso!".center(45)}\n{"---"*15}")
                sleep(0.5) # Efeito visual
                exit()
            elif option2 == "1": # Voltar
                print(f"{"=-="*15}\n{"Voltando".center(45)}")
                sleep(0.5)
                self.terminal()
    def generateFile(self, sheetInfo):
        # Essa função usa a variável que é informada (sheetInfo), para criar um arquivo .csv
        # Além disso mostra onde foi criado.
        
        sheet = pd.DataFrame(sheetInfo)
        
        directory = getcwd()
        file_path = path.join(directory, f"Orçamento {sheetInfo["NomeCliente"][0]} {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv")
        
        print(f"{"-=-"*15}\n{f"Arquivo gerado no caminho:\n{directory}"}\n{"-=-"*15}")
        
        sheet.to_csv(file_path, encoding="utf-8-sig")
        
        return file_path

# Aqui defino uma variável como a classe gerarOrçamento()
orçamento = gerarOrçamento()

# Daí começo a usar a classe comm a função terminal()
orçamento.terminal()