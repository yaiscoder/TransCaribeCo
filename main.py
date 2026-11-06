# TRANSCARIBECOL - SISTEMA DE NOMINA


# CONSTANTES ADMINISTRATIVAS

VALOR_HORA_ADMIN = 20000
VALOR_HORA_EXTRA = 25000

SALUD_ADMIN = 0.04
PENSION_ADMIN = 0.04
ARL_ADMIN = 0.00522


# CONSTANTES OPERATIVAS

VALOR_HORA_OPERATIVO = 40000

IBC_OPERATIVO = 0.40

SALUD_OPERATIVO = 0.125
PENSION_OPERATIVO = 0.16


# CARGOS OPERATIVOS

CARGOS_OPERATIVOS = {
    "Conductor": {
        "horas": 160,
        "arl": 0.01044
    },
    "Oficios Generales": {
        "horas": 100,
        "arl": 0.00522
    },
    "Vigilancia": {
        "horas": 336,
        "arl": 0.04350
    }
}


# LISTA EMPLEADOS

empleados = []



# FUNCIONES AUXILIARES


def solicitar_texto(mensaje):
    texto = input(mensaje).strip()

    while texto == "":
        print("Este campo no puede estar vacio.")
        texto = input(mensaje).strip()

    if texto.upper() == "CANCELAR":
        return None

    return texto

def solicitar_horas(mensaje, minimo=0, maximo=None):
    valido = False

    while not valido:
        entrada = input(mensaje).strip()

        if entrada.upper() == "CANCELAR":
            return None

        try:
            valor = int(entrada)

            if valor < minimo:
                print("El valor no puede ser negativo.")

            elif maximo is not None and valor > maximo:
                print(f"Selecciona una opcion entre {minimo} y {maximo}.")

            else:
                valido = True

        except ValueError:
            print("Debes ingresar un numero entero.")

    return valor


def formato_pesos(valor):
    return f"${valor:,.0f}"



# FUNCIONES DE CALCULO


def calcular_administrativo(nombre, cargo, horas, horas_extras):

    salario = horas * VALOR_HORA_ADMIN

    total_horas_extras = horas_extras * VALOR_HORA_EXTRA

    ibc = salario + total_horas_extras

    salud = ibc * SALUD_ADMIN

    pension = ibc * PENSION_ADMIN

    arl = ibc * ARL_ADMIN

    total_descuentos = salud + pension + arl

    total_pagar = ibc - total_descuentos

    empleado = {
        "nombre": nombre,
        "tipo": "ADMINISTRATIVO",
        "cargo": cargo,
        "horas_trabajadas": horas,
        "salario": salario,
        "horas_extras": horas_extras,
        "total_horas_extras": total_horas_extras,
        "ibc": ibc,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "total_descuentos": total_descuentos,
        "total_pagar": total_pagar
    }

    return empleado


def calcular_operativo(nombre, cargo):

    horas = CARGOS_OPERATIVOS[cargo]["horas"]

    porcentaje_arl = CARGOS_OPERATIVOS[cargo]["arl"]

    salario = horas * VALOR_HORA_OPERATIVO

    ibc = salario * IBC_OPERATIVO

    salud = ibc * SALUD_OPERATIVO

    pension = ibc * PENSION_OPERATIVO

    arl = ibc * porcentaje_arl

    total_descuentos = salud + pension + arl

    total_pagar = salario - total_descuentos

    empleado = {
        "nombre": nombre,
        "tipo": "OPERATIVO",
        "cargo": cargo,
        "horas_trabajadas": horas,
        "salario": salario,
        "horas_extras": 0,
        "total_horas_extras": 0,
        "ibc": ibc,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "total_descuentos": total_descuentos,
        "total_pagar": total_pagar
    }

    return empleado



# VOLANTE DE PAGO


def mostrar_volante(empleado):

    print("\n" + "*" * 55)
    print("                  VOLANTE DE PAGO")
    print("*" * 55)

    print(f"Nombre: {empleado['nombre']}")
    print(f"Tipo: {empleado['tipo']}")
    print(f"Cargo: {empleado['cargo']}")
    print(f"Horas Trabajadas (mes): {empleado['horas_trabajadas']}")
    print(f"Salario Bruto: {formato_pesos(empleado['salario'])}")
    print(f"Horas Extras: {empleado['horas_extras']}")
    print(f"Total pago Horas Extras: {formato_pesos(empleado['total_horas_extras'])}")

    print("\n" + "*" * 55)
    print("                 DESCUENTOS DE LEY")
    print("*" * 55)

    if empleado["tipo"] == "ADMINISTRATIVO":
        print(f"Salud (4%): {formato_pesos(empleado['salud'])}")
        print(f"Pension (4%): {formato_pesos(empleado['pension'])}")
        print(f"ARL (0.522%): {formato_pesos(empleado['arl'])}")

    else:
        porcentaje_arl = CARGOS_OPERATIVOS[empleado["cargo"]]["arl"]

        print(f"Salud (12.5%): {formato_pesos(empleado['salud'])}")
        print(f"Pension (16%): {formato_pesos(empleado['pension'])}")
        print(f"ARL ({porcentaje_arl * 100:.3f}%): {formato_pesos(empleado['arl'])}")

    print(f"\nTotal Descuentos: {formato_pesos(empleado['total_descuentos'])}")

    print(f"\nTotal a pagar: {formato_pesos(empleado['total_pagar'])}")

    print("*" * 55)
    print("              FIN DEL VOLANTE DE PAGO")
    print("*" * 55)



# REGISTRO DE EMPLEADOS


def registrar_administrativo():

    print("\n--- REGISTRO DE EMPLEADO ADMINISTRATIVO ---")
    print("Escribe CANCELAR para volver al menu.")

    nombre = solicitar_texto("Nombre del empleado: ")

    if nombre is None:
        return

    cargo = solicitar_texto("Cargo del empleado: ")

    if cargo is None:
        return

    horas = solicitar_horas("Horas trabajadas en el mes: ")

    if horas is None:
        return

    horas_extras = solicitar_horas("Horas extras trabajadas: ")

    if horas_extras is None:
        return

    empleado = calcular_administrativo(
        nombre,
        cargo,
        horas,
        horas_extras
    )

    empleados.append(empleado)

    print("\nEmpleado registrado correctamente.")

    mostrar_volante(empleado)
    

def registrar_operativo():
    print("\n--- REGISTRO OPERATIVO ---")
    print("Escriba CANCELAR en cualquier momento para volver al menu.")

    nombre = solicitar_texto("Ingrese el nombre: ")

    if nombre is None:
        return

    cargos = list(CARGOS_OPERATIVOS.keys())

    print("\nCARGOS DISPONIBLES:")

    for i, cargo in enumerate(cargos, start=1):
        print(f"{i}. {cargo}")

    opcion = solicitar_horas("Seleccione el cargo: ", 1, len(cargos))

    if opcion is None:
        return

    cargo = cargos[opcion - 1]

    empleado = calcular_operativo(nombre, cargo)

    empleados.append(empleado)

    mostrar_volante(empleado)


#  CONSULTAR EMPLEADOS


def consultar_empleados():

    print("\n--- EMPLEADOS REGISTRADOS ---")

    if len(empleados) == 0:
        print("No hay empleados registrados.")

    else:
        for i in range(len(empleados)):

            empleado = empleados[i]

            print("\n" + "-" * 55)

            print(f"Registro: {i + 1}")
            print(f"Nombre: {empleado['nombre']}")
            print(f"Tipo: {empleado['tipo']}")
            print(f"Cargo: {empleado['cargo']}")
            print(f"Salario: {formato_pesos(empleado['salario'])}")
            print(f"Total descuentos: {formato_pesos(empleado['total_descuentos'])}")
            print(f"Total a pagar: {formato_pesos(empleado['total_pagar'])}")

        print("\n" + "-" * 55)
        print(f"Total de empleados registrados: {len(empleados)}")



# GENERAR ARCHIVO TXT


def generar_archivo_txt():

    if len(empleados) == 0:
        print("\nNo hay empleados registrados para exportar.")

    else:
        try:
            with open("nomina_transcaribecol.txt", "w", encoding="utf-8") as archivo:

                archivo.write("TRANSCARIBECOL - REPORTE DE NOMINA\n")

                archivo.write("=" * 100 + "\n\n")

                encabezado = (
                    "Nombre | Tipo | Cargo | HT | Salario | "
                    "HE | TPHE | Salud | Pension | ARL | Total a pagar\n"
                )

                archivo.write(encabezado)

                archivo.write("-" * 100 + "\n")

                for empleado in empleados:

                    linea = (
                        f"{empleado['nombre']} | "
                        f"{empleado['tipo']} | "
                        f"{empleado['cargo']} | "
                        f"{empleado['horas_trabajadas']} | "
                        f"{empleado['salario']:.0f} | "
                        f"{empleado['horas_extras']} | "
                        f"{empleado['total_horas_extras']:.0f} | "
                        f"{empleado['salud']:.0f} | "
                        f"{empleado['pension']:.0f} | "
                        f"{empleado['arl']:.0f} | "
                        f"{empleado['total_pagar']:.0f}\n"
                    )

                    archivo.write(linea)

            print("\nArchivo TXT generado correctamente.")
            print("Nombre: nomina_transcaribecol.txt")

        except OSError:
            print("\nError al generar el archivo TXT.")



#  MENU PRINCIPAL


def menu_principal():

    opcion = 0

    while opcion != 5:

        print("\n")
        print("=" * 55)
        print("       TRANSCARIBECOL - SISTEMA DE NOMINA")
        print("=" * 55)

        print("1. Registrar empleado administrativo")
        print("2. Registrar empleado operativo")
        print("3. Consultar empleados registrados")
        print("4. Generar archivo TXT de nomina")
        print("5. Salir")

        opcion = solicitar_horas("\nSeleccione una opcion: ")

        if opcion == 1:
            registrar_administrativo()

        elif opcion == 2:
            registrar_operativo()

        elif opcion == 3:
            consultar_empleados()

        elif opcion == 4:
            generar_archivo_txt()

        elif opcion == 5:
            print("\nGracias por utilizar el sistema de nomina.")

        else:
            print("\nOpcion no valida. Intente nuevamente.")



# EJECUCION DEL PROGRAMA

if __name__ == "__main__":
    menu_principal()
