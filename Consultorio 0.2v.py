import mysql.connector
from datetime import datetime

def mostrar_pacientes():
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    print("Pesquisa de paciente")
    print("1 - Pesquisar Via CPF")
    print("2 - Pesquisar por nome")
    print("3 - Motrar todos Usuarios")
    escolha = int(input("Digite sua escolha: "))
    if escolha==1:
        cpf=input("Digite o CPF: ")
        query = ("SELECT * FROM pacientes WHERE cpf = '{}'".format(cpf))
        cursor.execute(query)
        print(cursor)
    else:
        query = ("SELECT * FROM pacientes")
        cursor.execute(query)
    records = cursor.fetchall()
    #print ("{:<5} {:<40} {:<10} {:<2} {:<15} {:<30} {:<11}\n".format('id','Nome','Nascimento','Sexo',
     #                                                                'CPF','Logadouro', 'Nº','Bairro', 'Cidade'
     #                                                                ,'Numero do Cel', 'Email'))
    if cursor.rowcount >0:
        for i in records:
            msg_select = "ID: {0} Nome: {1} Sexo:{2}\nNascimento: {3} CPF: {4}\nLogadouro: {5} Nº: {6} Bairro: {7} Cidade: {8}"
            msg_select += "\nNº contato: {9} E-mail: {10}"
            print(msg_select.format(i[0],i[1],i[3],i[2].strftime('%d/%m/%Y'),i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
            #print("""ID: {0} Nome: {1} Sexo:{2}\nNascimento: {3} CPF: {4}\nLogadouro: {5} Nº: {6} Bairro: {7} Cidade: {8}
            #      Nº contato: {9} E-mail: %{10}""".format() evitar uso de 3 aspas
    else:
        print("Não existe usuário cadastrado\n")
    print(60*"-")
    cnx.close()
    cursor.close()
def mostrar_agendamentos():
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    query = ("""SELECT a.id_agendamento, p.nome, f.nome, a.data_consulta FROM agendamentos as a 
                inner join pacientes as p on a.fk_cpf=p.cpf
                inner join fisioterapeutas as f on f.crefito=a.fk_crefito""")
    cursor.execute(query)
    records = cursor.fetchall()
    print ("{:<5} {:<30} Dr.{:<30} {:<10}\n".format('id','Paciente','fisioterapeuta', 'Data Consulta'))
    if cursor.rowcount >0:
        for i in records:
            print("{:<5} {:<30} {:<30} {:<10}".format(i[0], i[1], i[2], i[3]))
    else:
        print("Não existe consultas\n")
    print(60*"-")
    cnx.close()
    cursor.close()
def cadastrar_pacientes():
    nome_paciente = input("Digite o nome do paciente: ")
    data_nasc = input("Digite Data de Nascimento(dd/mm/yyyy): ")
    data_nasc = datetime.strptime(data_nasc, "%d/%m/%Y")#parse data to datetime mysql
    sexo = input("Qual Sexo do paciente (F/M)?: ")
    cpf = input("Digite o CPF do paciente: ")
    logadouro = input("Digite o nome da rua do paciente: ")
    n_casa = input("Digite o numero da casa do paciente: ")
    bairro = input("Digite o nome do bairro do paciente: ")
    cidade = input("Digite o nome da cidade do paciente: ")
    numero_cel = input("Digite o numero do celular: ")
    email = input("Digite o email do paciente: ")
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    data = (nome_paciente, data_nasc,sexo,cpf,logadouro,n_casa,bairro,cidade,numero_cel,email)
    query = ("INSERT INTO pacientes (nome, nascimento,sexo,cpf,logadouro, n_casa, bairro, cidade,n_celular, email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    cursor.execute(query,data)
    print(query)
    records = cursor.fetchall()
    print(records)
    if cursor.rowcount>0:
        print("\nCadastro Realizado!")
    else:
        print("\nFalha no Cadastro!")
    print(60*"-")
    cnx.commit()
    cnx.close()
    cursor.close()

def menu_atendente(id_atendente):
    c = 1
    while(c!=0):
        print("\t\t\tAtendente")
        print("1 - Agendar Atendimento")
        print("2 - Cadastrar Paciente")
        print("3 - Procurar Paciente")
        print("4 - Cadastrar Fisioterapeuta")
        print("5 - Procurar Prescrição")
        print("0 - Fechar Programa")
        c = int(input("Digite sua escolha: "))
        if c==3:
            mostrar_pacientes()
        elif c==5:
            mostrar_agendamentos()
        elif c==2:
            cadastrar_pacientes()
        elif c==0:
            return 0;
def menu_fisio(crefito):
    c = 1
    while(c!=0):
        print("\t\t\tFisio")
        print("1 - Ver Agendamentos")
        print("2 - Efetuar Atendimento")
        print("3 - Procurar Paciente")
        print("5 - Procurar Prescrição")
        print("6 - Ver grupos de condutas")
        print("0 - Fechar Programa")
        c = int(input("Digite sua escolha: "))
        if c==3:
            mostrar_pacientes()
        elif c==5:
            mostrar_atendimentos()
        elif c==2:
            cadastrar_pacientes()
        elif c==0:
            return 0;
#Inicio programa:
menu_atendente(0)
