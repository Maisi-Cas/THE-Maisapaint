tumamabank = [
    "tu mama",
    "tu mamá",
    "tu madre",
    "tu vieja",
    "tu progenitora",
    "mi polla"
]

def chekUrMonInStr(string):
    global tumamabank
    for i in tumamabank:
        if i in string:
            return True

    return False

saveFormat = "maisapt"

if __name__ == "__main__":
    dick = {
        "xd" : 1,
        "pene" : 7,
        "Putos" : [x + 1 for x in range(100)]
    }

    for i, j in dick.items():
        print(f"{i} : {j}")
        
    valor = int(input("Ingresa un valor papa -> "))

    print("Es par" if valor % 2 == 0 else "Es impar")