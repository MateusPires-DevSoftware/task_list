# Este script implementa uma lista de tarefas simples usando Redis como armazenamento.
# Permite adicionar, listar e remover tarefas por meio de um menu interativo em linha de comando.
# Cada tarefa é armazenada com um ID único gerado automaticamente usando uma chave contador.


import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def adicionartarefa(descricao):
    proximo_id = r.incr('contadorID')
    r.set(proximo_id, descricao)
    return proximo_id

def listartarefas():
    ids = r.keys()

    tarefas = []
    for id in ids:
        if id != b'contadorID':
            descricao = r.get(id).decode('utf-8')
            tarefas.append({'id': id.decode('utf-8'), 'descricao': descricao})

    return tarefas

def removertarefa(id):
    if r.exists(id):
        r.delete(id)
        print("Tarefa removida com sucesso!")
    else:
        print("ID de tarefa inexistente.")

if __name__ == '__main__':
    while True:
        print("\n1. Adicionar Tarefa\n2. Listar Tarefas\n3. Remover Tarefa\n4. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            descricao = input("Digite a descrição da tarefa: ")
            adicionartarefa(descricao)
            print("Tarefa adicionada com sucesso!")

        elif escolha == '2':
            tarefas = listartarefas()
            if tarefas:
                for tarefa in tarefas:
                    print(f"ID: {tarefa['id']},\nDescrição: {tarefa['descricao']}")
            else:
                print("Nenhuma tarefa encontrada.")

        elif escolha == '3':
            id = input("Digite o ID da tarefa que deseja remover: ")
            removertarefa(id)

        elif escolha == '4':
            break
        else:
            print("Escolha Inválida!")
