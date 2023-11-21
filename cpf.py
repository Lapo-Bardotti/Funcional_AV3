def verificarCPF(cpf: str) -> bool:
    if not cpf and not len(cpf) == 11:
        print("Por favor, insira o CPF válido.")
        return False
    array = list(cpf)
    aux = 0
    aux2 = 0

    for i in range(len(array) - 2):
        # para o primeiro dígito verificador;
        aux += int(array[i]) * (i + 1)

    digver = aux % 11

    if digver == 10:
        digver = 0

    for k in range(len(array) - 1):
        # para o segundo dígito verificador;
        aux2 += int(array[k]) * k

    digver2 = aux2 % 11

    if digver2 == 10:
        digver2 = 0

    return int(array[9]) == digver and int(array[10]) == digver2

# print(verificarCPF("01587063310"))