import mysql.connector
from datetime import datetime, timedelta, timezone
import getpass

def data_atual():
    data_atual = datetime.now()
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    data_atual = data_atual.astimezone(fuso_horario)
    return data_atual.strftime("%Y-%m-%d")
    

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
    elif escolha==2:
        nome_consulta = input("Digite o Nome do paciente: ")
        query = ("SELECT * FROM pacientes WHERE nome LIKE '{}%'".format(nome_consulta))
        cursor.execute(query)
    else:
        query = ("SELECT * FROM pacientes")
        cursor.execute(query)
    records = cursor.fetchall()
    if cursor.rowcount >0:
        for i in records:
            print(60*"-")
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
    query=""
    escolha = int(input("1 - Por CPF\n2 - Por data\n3 - Por fisioterapeuta\n4 - Por nome\nDigite sua escolha: "))
    if escolha==1:
        cpf = input("Digite o CPF: ")
        query = ("""SELECT a.id_agendamento, p.nome, f.nome, a.data_consulta FROM agendamentos as a
                inner join pacientes as p on p.cpf=a.fk_cpf and a.fk_cpf='{}'
                inner join fisioterapeutas as f on f.crefito=a.fk_crefito""".format(cpf))
    elif escolha==2:
        data_consulta = input("Digite a dia de consulta (em dd/mm/yyyy): ")
        data_consulta = datetime.strptime(data_consulta, "%d/%m/%Y")
        query = ("""SELECT a.id_agendamento, p.nome, f.nome, a.data_consulta FROM agendamentos as a
                inner join pacientes as p on a.fk_cpf=p.cpf and a.data_consulta='{}'
                inner join fisioterapeutas as f on f.crefito=a.fk_crefito""".format(data_consulta))
    elif escolha==3:
        crefito = input("Digite o Crefito do fisioterapeuta: ")
        query = ("""SELECT a.id_agendamento, p.nome, f.nome, a.data_consulta FROM agendamentos as a
                inner join pacientes as p on a.fk_cpf=p.cpf
                inner join fisioterapeutas as f on f.crefito=a.fk_crefito and a.fk_crefito='{}'""".format(crefito))
    elif escolha==4:
        nome_consulta = input("Digite o nome do paciente: ")
        query = ("""SELECT a.id_agendamento, p.nome, f.nome, a.data_consulta FROM agendamentos as a
                inner join pacientes as p on p.cpf=a.fk_cpf and p.nome LIKE '{}%'
                inner join fisioterapeutas as f on f.crefito=a.fk_crefito""".format(nome_consulta))
    cursor.execute(query)
    records = cursor.fetchall()
    print(60*"-")
    print ("{:<5} {:<30} {:<30} {:<10}\n".format('id','Paciente','fisioterapeuta', 'Data Consulta'))
    if cursor.rowcount >0:
        for i in records:
            print("{:<5} {:<30} {:<30} {:<10}".format(i[0], i[1], i[2], i[3].strftime('%d/%m/%Y')))
    else:
        print("Não existe consultas\n")
    print(60*"-")
    cnx.close()
    cursor.close()

def mostrar_prescricao():
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    query=""
    escolha = int(input("1 - Por CPF\n2 - Por nome\nDigite sua escolha: "))
    if escolha==1:
        cpf = input("Digite o CPF: ")
        query = ("""SELECT a.id_agendamento, p.nome, a.triagem, at.prescricao FROM agendamentos as a
                inner join pacientes as p on p.cpf=a.fk_cpf and a.fk_cpf='{}'
                inner join atendimentos as at on at.fk_id_agendamento=a.id_agendamento""".format(cpf))
    
    elif escolha==2:
        nome_consulta = input("Digite o Nome do paciente: ")
        query = ("""SELECT a.id_agendamento, p.nome, a.triagem, at.prescricao  FROM agendamentos as a
                inner join pacientes as p on p.cpf=a.fk_cpf and p.nome LIKE '{}%'
                inner join atendimentos as at on at.fk_id_agendamento=a.id_agendamento""".format(nome_consulta))
    cursor.execute(query)
    records = cursor.fetchall()
    print(60*"-")
    print ("{:<5} {:<30} {:<30} {:<10}\n".format('id','Paciente','Triagem', 'Prescricao'))
    if cursor.rowcount >0:
        for i in records:
            print("{:<5} {:<30} {:<30} {:<10}".format(i[0], i[1], i[2], i[3]))
    else:
        print("Não existe consultas\n")
    print(60*"-")
    cnx.close()
    cursor.close()

def mostrar_agendamentos_fisio(fk_crefito):
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    print("\t\tMostrar agendamentos\n0 - Já concluidos\n1 - Não concluidos")
    escolha = int(input("Digite sua escolha: "))
    if escolha==1:
        query = ("""SELECT a.id_agendamento, p.nome, f.nome, a.data_consulta FROM agendamentos as a
                inner join pacientes as p on a.fk_cpf=p.cpf
                inner join fisioterapeutas as f on f.crefito=a.fk_crefito and a.fk_crefito='{}' and presente=FALSE""".format(fk_crefito))
    else:
        query = ("""SELECT a.id_agendamento, p.nome, f.nome, a.data_consulta FROM agendamentos as a
                inner join pacientes as p on a.fk_cpf=p.cpf
                inner join fisioterapeutas as f on f.crefito=a.fk_crefito and a.fk_crefito='{}' and presente=TRUE""".format(fk_crefito))
        
    cursor.execute(query)
    records = cursor.fetchall()
    print(60*"-")
    print ("{:<5} {:<30} {:<30} {:<10}\n".format('id','Paciente','fisioterapeuta', 'Data Consulta'))
    if cursor.rowcount >0:
        for i in records:
            print("{:<5} {:<30} {:<30} {:<10}".format(i[0], i[1], i[2], i[3].strftime('%d/%m/%Y')))
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

def cadastrar_fisio():
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    nome_fisio = input("Digite o nome do fisioterapeuta: ")
    crefito = input("Digite o numero do crefito: ")
    enable_atuacao = int(input("Escolha a area de atuação: \n1-Traumato-ortopedia\n2-Neuro-funcional\n3-Pós-Cirurgico\n4-DermatoFuncional\nDigite sua escolha: "))
    if enable_atuacao==1:
        atuacao="Traumato-ortopedia"
    elif enable_atuacao==2:
        atuacao="Neuro-funcional"
    elif enable_atuacao==3:
        atuacao="Pós-Cirurgico"
    elif enable_atuacao==4:
        atuacao="Dermato-Funcional"
    token = getpass.getpass(prompt="Digite Token: ", stream=None)
    query = "INSERT INTO fisioterapeutas (nome,crefito,token) VALUES (%s,%s,%s)"
    data = (nome_fisio, crefito, token)
    cursor.execute(query, data)
    results = cursor.fetchone()
    if cursor.rowcount>0:
        query="INSERT INTO especialidades (fk_crefito, atuacao) VALUES (%s,%s)"
        data = (crefito, atuacao)
        cursor.execute(query,data)
        results = cursor.fetchone()
        if cursor.rowcount>0:
            print("Cadastro realizado com sucesso!")
        else:
            print("Falha no cadastro de especialidade")
    else:
        print("Falha no cadastro do fisioterapeuta")
    cnx.commit()
    cnx.close()
    cursor.close()

def cadastrar_secretaria():
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    nome_secret = input("Digite o nome da secretaria: ")
    cpf_secretaria = input("Digite o numero do cpf: ")
    token = getpass.getpass(prompt="Digite Token: ", stream=None)
    query = "INSERT INTO secretarias (nome,cpf,token) VALUES (%s,%s,%s)"
    data = (nome_secret, cpf_secretaria, token)
    cursor.execute(query, data)
    results = cursor.fetchone()
    if cursor.rowcount>0:
        print("Cadastro realizado com sucesso!")
    else:
        print("Falha no cadastro")
    cnx.commit()
    cnx.close()
    cursor.close()
    
def agendar(cpf_secretaria):
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    print("Marcação de consultas: ")
    cpf = input("Digite o cpf do paciente: ")
    query = "SELECT nome FROM pacientes where cpf='{}'".format(cpf)
    cursor.execute(query)
    results = cursor.fetchone()
    if cursor.rowcount>0:
        nome_paciente=results[0]
    else:
        print("Não existe esse Paciente")
    data_consulta = input("Digite a data para o agendamento (em dd/mm/yyyy): ")
    data_consulta_mysql = datetime.strptime(data_consulta, "%d/%m/%Y")
    triagem = input("Quais os sintomas do paciente e área acometida: ")
    enable_atuacao = int(input("Escolha a area de atuação: \n1-Traumato-ortopedia\n2-Neuro-funcional\n3-Pós-Cirurgico\n4-DermatoFuncional\nDigite sua escolha: "))
    if enable_atuacao==1:
        atuacao="Traumato-ortopedia"
    elif enable_atuacao==2:
        atuacao="Neuro-funcional"
    elif enable_atuacao==3:
        atuacao="Pós-Cirurgico"
    elif enable_atuacao==4:
        atuacao="Dermato-Funcional"
    query = """SELECT f.nome, e.fk_crefito FROM especialidades as e 
            inner join fisioterapeutas as f on f.crefito=e.fk_crefito and e.atuacao='{}'""".format(atuacao)
    cursor.execute(query)
    results = cursor.fetchall()
    if cursor.rowcount>0:
        count=0
        for i in results:
            count+=1
            print("ID:{0} Nome Fisio: {1} Crefito: {2}".format(count, i[0],i[1]))
        escolha = int(input("Digite o id do fisiotetapeuta: "))
        count=0
        for i in results:
            count+=1
            if count==escolha:
                nome_fisio = i[0]
                crefito = i[1]
    print("Confirmação de agendamento:\nCPF: {0} Nome: {1}\nNome do Fisio: {2} Crefito: {3}\nTriagem: {4} Data da Consulta: {5}".format(cpf,nome_paciente,nome_fisio,crefito,triagem,data_consulta))
    data = (cpf,triagem, data_consulta_mysql, crefito, cpf_secretaria)
    confirma = int(input("Confirma o agendamento?\n0 - Não 1 - Sim\nDigite sua escolha: "))
    if confirma == 1:
        query="INSERT INTO agendamentos (fk_cpf,triagem, data_consulta, fk_crefito, fk_cpf_secretarias) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query,data)
        results = cursor.fetchall()
        if cursor.rowcount>0:
            print("\nAgendamento Realizado!")
        else:
            print("\nFalha no Agendamento!")
    else:
        print("Agendamento Não Concluido!")
        
    cnx.commit()
    cnx.close()
    cursor.close()

def fazer_atendimento(fk_crefito):
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    data_consulta = data_atual()
    query = ("""SELECT p.nome, p.nascimento, a.triagem, a.fk_cpf, a.id_agendamento FROM agendamentos as a
                inner join pacientes as p on a.fk_cpf=p.cpf
                inner join fisioterapeutas as f on f.crefito=a.fk_crefito
                and a.fk_crefito='{}' and a.data_consulta='{}' and presente=FALSE""".format(fk_crefito,data_consulta))
    cursor.execute(query)
    results = cursor.fetchall()
    if cursor.rowcount>0:
        count=0
        print("Selecione o id do agendamento: ")
        for i in results:
            count+=1
            print("ID:{0} Nome Paciente: {1} Data de Nascimento: {2} \nTriagem: {3}".format(count, i[0],i[1],i[2]))
        escolha = int(input("Digite o id do agendamento: "))
        count=0
        for i in results:
            count+=1
            if count==escolha:
                nome_paciente = i[0]
                data_nascimento = i[1].strftime("%d/%m/%y")
                triagem = i[2]
                cpf_paciente = i[3]
                id_agendamento = i[4]
        print("\n\t\tConfirmação de atendimento\n")
        print("Paciente: {0} Data de Nascimento: {1}\nTriagem: {2}".format(nome_paciente,data_nascimento,triagem))
        confirma = int(input("Confirma o agendamento?\n0 - Não 1 - Sim\nDigite sua escolha: "))
        if confirma == 1:
            confirmacao=0
            while(confirmacao!=1):
                print("Consulta com o Paciente: {0}".format(nome_paciente))
                prescricao = input("Digite a prescrição para o paciente: ")
                confirmacao = int(input("Confirma o atendimento ao paciente?\n0 - Não 1 - Sim 2 - Cancelar operação\nDigite sua escolha: "))
                if confirmacao == 2:
                    return
            query="UPDATE agendamentos SET presente=TRUE WHERE id_agendamento = {}".format(id_agendamento)
            cursor.execute(query)
            results = cursor.fetchall()
            if cursor.rowcount>0:
                query="INSERT INTO atendimentos (fk_id_agendamento, prescricao) VALUES ({0},'{1}')".format(id_agendamento,prescricao)
                cursor.execute(query)
                results = cursor.fetchall()
                if cursor.rowcount>0:
                    print("Atendimento Realizado com sucesso!")
                else:
                    print("\nFalha a gravar atendimento!")
            escolha_conduta=-1
            while(escolha_conduta!=0):
                print("Escolha Os grupos de condutas para o paciente:")
                print("1 - Eletroterapia\n2 - Cinesioterapia\n3 - Terapia Manual\n4 - Termoterapia\n5 - Orientações")
                escolha_conduta = int(input("Digite sua escolha: "))
                if escolha_conduta == 1:
                    nome_conduta = "Eletroterapia"
                elif escolha_conduta == 2:
                    nome_conduta = "Cinesioterapia"
                elif escolha_conduta == 3:
                    nome_conduta = "Terapia Manual"
                elif escolha_conduta == 4:
                    nome_conduta = "Termoterapia"
                elif escolha_conduta == 5:
                    nome_conduta = "Orientações"
                query="SELECT id FROM atendimentos WHERE fk_id_agendamento = {}".format(id_agendamento)
                cursor.execute(query)
                results = cursor.fetchone()
                if cursor.rowcount>0:
                    id_atendimento=results[0]
                query="""INSERT INTO condutas (fk_cpf, nome_conduta, fk_id_atendimento) VALUES ('{0}','{1}',{2})""".format(cpf_paciente,nome_conduta,id_atendimento)
                cursor.execute(query)
                results = cursor.fetchall()
                if cursor.rowcount>0:
                    print("Conduta Adiciona Com sucesso!")
                    print("Deseja adicionar mais condutas? 0 - Não 1 - Sim")
                    escolha_conduta = int(input("Digite sua escolha: "))
            print("Agentamento Finalizado com sucesso!")
            
        else:
            print("Agendamento Não Concluido!")
    else:
        print("Não Existe agendamentos para hoje!")
    cnx.commit()
    cnx.close()
    cursor.close()

def mostrar_grupos():
    cnx = mysql.connector.connect(user='root', database='consultorios')
    cursor = cnx.cursor()
    print("Escolha Os grupos de condutas para o paciente:")
    print("1 - Eletroterapia\n2 - Cinesioterapia\n3 - Terapia Manual\n4 - Termoterapia\n5 - Orientações")
    escolha_conduta = int(input("Digite sua escolha: "))
    if escolha_conduta == 1:
        nome_conduta = "Eletroterapia"
    elif escolha_conduta == 2:
        nome_conduta = "Cinesioterapia"
    elif escolha_conduta == 3:
        nome_conduta = "Terapia Manual"
    elif escolha_conduta == 4:
        nome_conduta = "Termoterapia"
    elif escolha_conduta == 5:
        nome_conduta = "Orientações"
    query="""SELECT p.nome,a.prescricao FROM condutas as c
            inner join pacientes as p on p.cpf = c.fk_cpf
            inner join atendimentos as a on a.id = c.fk_id_atendimento and c.nome_conduta='{}'""".format(nome_conduta)
    cursor.execute(query)
    results = cursor.fetchall()
    if cursor.rowcount>0:
        print("Grupo de condutas: "+nome_conduta)
        for i in results:
            print(60*"-")
            print("Nome Paciente: {0} \nTriagem: {1}".format(i[0],i[1]))
    else:
        print("Não existe pacientes nesse grupo")
        
    
def menu_secretaria(cpf_secretaria):
    c = 1
    while(c!=0):
        print("\t\t\tSecretaria")
        print("1 - Agendar Atendimento")
        print("2 - Cadastrar Paciente")
        print("3 - Procurar Paciente")
        print("4 - Cadastrar Fisioterapeuta")
        print("5 - Procurar agendamentos")
        print("6 - Cadastrar Secretarias")
        print("0 - Logout")
        c = int(input("Digite sua escolha: "))
        if c==3:
            mostrar_pacientes()
        elif c==5:
            mostrar_agendamentos()
        elif c==1:
            agendar(cpf_secretaria)
        elif c==2:
            cadastrar_pacientes()
        elif c==4:
            cadastrar_fisio()
        elif c==6:
            cadastrar_secretaria()
        elif c==0:
            return 0
def menu_fisio(crefito):
    c = 1
    while(c!=0):
        print("\t\t\tFisio")
        print("1 - Ver Agendamentos")
        print("2 - Efetuar Atendimento")
        print("3 - Procurar Paciente")
        print("5 - Procurar Prescrição")
        print("6 - Ver grupos de condutas")
        print("0 - Logout")
        c = int(input("Digite sua escolha: "))
        if c==3:
            mostrar_pacientes()
        elif c==5:
            mostrar_prescricao()
        elif c==1:
            try: 
                mostrar_agendamentos_fisio(crefito)
            except:
                print("Erro no agendamento")
        elif c==2:
            try:
                fazer_atendimento(crefito)
            except:
                print("Erro ao efetuar atendimento")
        elif c==6:
            mostrar_grupos()
        elif c==0:
            return 0
def login():
    enable=-1
    while(enable!=0):
        enable = int(input("Login:\n1 - Secretaria\n2 - Fisioterapeuta\n0 - Para sair\nDigite a opção: "))
        if enable==1:
            user_secretaria = "-1"
            while(user_secretaria!="0"):
                user_secretaria = input("Digite o cpf (digite 0 para sair): ")
                if(user_secretaria=='0'):
                    break
                else:
                    pass_secretaria = getpass.getpass(prompt="Digite Token: ", stream=None)
                    #pass_secretaria = input("Digite o token: ")
                cnx = mysql.connector.connect(user='root', database='consultorios')
                cursor = cnx.cursor()
                query = "SELECT token FROM secretarias WHERE cpf='{}'".format(user_secretaria)
                cursor.execute(query)
                results = cursor.fetchone()
                if cursor.rowcount>0:
                    token=results[0]
                    if token == pass_secretaria:
                        print("Login Realizado com Sucesso!")
                        menu_secretaria(user_secretaria)
                    else:
                        print("Token ERRADO!")
                else:
                    print("\nNão existe Usuário")
                cnx.close()
                cursor.close()
        elif enable==2:
            crefito="-1"
            while(crefito!="0"):
                crefito = input("Digite o crefito (digite 0 para sair): ")
                if(crefito=='0'):
                    break
                else:
                    pass_fisio = getpass.getpass(prompt="Digite o Token: ", stream=None)
                    #pass_fisio = input("Digite o token: ")
                cnx = mysql.connector.connect(user='root', database='consultorios')
                cursor = cnx.cursor()
                query = "SELECT token FROM fisioterapeutas WHERE crefito='{}'".format(crefito)
                cursor.execute(query)
                results = cursor.fetchone()
                if cursor.rowcount>0:
                    token=results[0]
                    if token == pass_fisio:
                        print("Login Realizado com Sucesso!")
                        menu_fisio(crefito)
                    else:
                        print("Token ERRADO!")
                else:
                    print("\nNão existe Crefito cadastrado")
                cnx.close()
                cursor.close()
    
#Inicio programa:
login()
print("Fechando programa")
