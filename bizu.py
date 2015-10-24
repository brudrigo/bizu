#!/usr/bin/python
# -*- coding: utf8 -*-
# Script Desenvolvido por Bruno Rodrigo
# github.com/brudrigo

import os, sqlite3, commands, string
import time
import datetime

#configurar o editor padrão
os.system("clear")
editor = raw_input('Qual editor de texto você gostaria de utilizar?\n')

############################################################################
################### CONEXÃO COM O BANCO DE DADOS ###########################
############################################################################
db = sqlite3.connect('data.db')
cursor = db.cursor()

def select_list(sch):
    cursor.execute("SELECT * FROM bizu where pchaves like %s" % sch)
    res = cursor.fetchall()
    return res


def excluir(cond):
    cursor.execute("DELETE FROM bizu WHERE id = '%s'" % cond)
    db.commit()
    return True


def select_ln(tabela, cond):
    try:
        cursor.execute("SELECT * FROM %s %s" % (tabela, cond))
        res = cursor.fetchall()
        return res[0]
    except Exception, e:
        return False


def criar_cont(titulo, pchaves, cont):
    cursor.execute("INSERT INTO bizu ( titulo, pchaves, bizu ) VALUES ('%s', '%s', '%s')" % (titulo, pchaves, cont))
    db.commit()
    return True


############################################################################
#######################  FUNÇÕES DE COMANDO  ###############################
############################################################################

def inicial():
    os.system("clear")
    print('+----------------------------------------------------------+')
    print('|                                                          |')
    print('|                          BIZU                            |')
    print('|                 Banco de dados do milk!                  |')
    print('|                                                by C0rt35 |')
    print('+----------------------------------------------------------+')
    print('| Comandos:                                                |')
    print('|                                                          |')
    print('|   [search|s] - Pesquisar por dicas (Ex. search pchaves)  |')
    print('|   [add]      - Adicionar nova dica                       |')
    print('|   [del]      - Excluir dica                              |')
    print('|   [edit|e]   - Editar arquivo de dica                    |')
    print('|   [ls]       - Listar bizus cadastrados                  |')
    print('|   [menu]     - Listar opções de comandos                 |')
    print('|   [print|p]  - Mostra o bizu (Ex. p 50)                  |')
    print('|   [sair]     - sair do script                            |')
    print('+----------------------------------------------------------+')
    print('\n')


# COMANDO SEARCH
def search():
    pam = parametros.split(' ')
    search = string.join(pam[1:], "%' or pchaves like '%")
    search = "'%" + search + "%'"
    result = select_list(search)
    print("ID \t TÍTULO DO BIZÚ")
    print('------------------------------------------------------------')
    for record in result:  print("%s \t %s" % (record[0], record[1]))
    print('\n')


# COMANDO ADD
def add():
    os.system("clear")
    titulo = raw_input('Qual o título do bizú?\n')
    pchaves = raw_input('Quais as palavras chaves?\n')
    print(
        'você será redirecionado para um editor de texto, coloque o conteúdo no arquivo que será criado e salve o arqvuivo antes de sair')
    time.sleep(3)
    ts = time.time()
    arq = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H-%M-%S')
    os.system("%s ./bizus/bizu_%s.txt" % (editor, arq))
    criar_cont(titulo, pchaves, "bizu_%s.txt" % arq)


# COMANDO DEL
def excluir_bizu():
    try:
        idt = parametros.split(' ')
        arq = select_ln("bizu", "WHERE id='%s'" % idt[1])
        excluir(idt[1])
        os.system("rm /etc/garruk/bizus/%s" % arq[3])
        print("Bizu exlcuído com sucesso!")
    except Exception, e:
        print("não foi possível excluir o registro informado!")
    inicial()


# COMANDO DEL
def show_bizu():
    try:
        pam = parametros.split(' ')
        idt = pam[1]
        projetol = select_ln('bizu', "WHERE id='%s'" % idt)
        if projetol == False:
            print("O bizu solicitado não foi encontrado! tente novamente!")
        else:
            os.system('clear')
            os.system('cat ./bizus/%s' % projetol[2])
            print('\n')
    except Exception, e:
        print('não foi possível mostrar o conteúdo do bizú selecionado!')


# COMANDO PARA EXIBIR O MENU
def clear():
    os.system("clear")
    inicial()


# COMANDO PARA O ARQUIVO DE HELP
def ajuda():
    os.system("clear")
    inicial()


# COMANDO PARA RETORNAR A TELA ANTERIOR
def back():
    os.system("clear")
    global parametros
    global cmd
    parametros = "back"


# COMANDO PARA EDITAR UMA DICA
def edit():
    pam = parametros.split(' ')
    idt = pam[1]
    projetol = select_ln('bizu', "WHERE id='%s'" % idt)
    os.system("%s ./bizus/%s" % (editor, projetol[2]))


# LISTA DOS COMANDOS DESTA TELA
dict = {"add": add, "exit": exit, "help": ajuda, "menu": clear, "sair": back, "search": search, "s": search, "ls": search,
        "del": excluir_bizu, "print": show_bizu, "p": show_bizu, "edit": edit, "e": edit}


def comando(x):
    '''
    Função que interpreta os
    comandos no dicionário dict
    '''
    try:
        res = x.split(' ')
        global cmd
        cmd = res[0]
        global parametros
        parametros = x
        dict[cmd]()
    except:
        case_default()


inicial()
while True:
    try:
        comando(raw_input("\033[32m\033[1mbizu> \033[0;0m"))
        if parametros == "back":
            break
    except:
        print('Opção não encontrada, tente novamente')
