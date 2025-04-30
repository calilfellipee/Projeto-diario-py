from datetime import datetime
import os

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    Fore = Style = lambda x: x

ARQUIVO = "diario.txt"

def salvar_anotacao():
    texto = input("Digite sua anotação: ").strip()
    if texto:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(ARQUIVO, "a", encoding="utf-8") as f:
            f.write(f"[{data_hora}] {texto}\n\n")
        print(Fore.GREEN + "✅ Anotação salva com sucesso!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "⚠️ A anotação está vazia!" + Style.RESET_ALL)

def mostrar_anotacoes():
    if not os.path.exists(ARQUIVO) or os.path.getsize(ARQUIVO) == 0:
        print(Fore.CYAN + "📂 O diário ainda está vazio." + Style.RESET_ALL)
        return

    print(Fore.MAGENTA + "\n📝 Anotações salvas:")
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        print(f.read())
    print(Style.RESET_ALL)

def limpar_diario():
    if os.path.exists(ARQUIVO):
        confirm = input(Fore.RED + "🗑️ Tem certeza que deseja apagar todas as anotações? (s/n): " + Style.RESET_ALL).lower()
        if confirm == 's':
            open(ARQUIVO, "w").close()
            print(Fore.RED + "✅ Diário apagado com sucesso." + Style.RESET_ALL)
        else:
            print("❎ Ação cancelada.")

while True:
    print(Fore.CYAN + "\n📘 Diário Eletrônico" + Style.RESET_ALL)
    print("1. Escrever nova anotação")
    print("2. Ver anotações")
    print("3. Apagar todas as anotações")
    print("4. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        salvar_anotacao()
    elif opcao == "2":
        mostrar_anotacoes()
    elif opcao == "3":
        limpar_diario()
    elif opcao == "4":
        print("Encerrando... 👋")
        break
    else:
        print(Fore.RED + "❌ Opção inválida!" + Style.RESET_ALL)
