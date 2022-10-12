from bd_utils import *


def menu() -> str:
    """ интерактив с пользователем и формирование соответствующего текста запроса """
    print("доступные действия:")
    print(" 1. показать все объявления")
    print(" 2. показать объявления конкретных пользователей")
    print(" 3. показать объявления в диапазоне цен")
    print(" 4. показать объявления для конкретного города")
    print(" 5. показать информацию для определенного пользователя и цены")
    print(" 6. выход")
    user_input = input("выберите пункт и введите его номер: >>> ")

    where = ""
    order = ""
    match user_input:
        case "1":
            where = ""
        case "2":
            user_input = input("введите пользователей через запятую: >>> ")
            list_user_str = []
            for each in user_input.split(','):
                list_user_str.append(f"{each.strip()!r}")
            list_user_str = ",".join(list_user_str)
            where = f"\n AND aut.name in ({list_user_str})"
        case "3":
            user_input = input("введите 2 цены через запятую: >>> ")
            user_input = user_input.split(",")
            min_price = min(int(user_input[0].strip()), int(user_input[1].strip()))
            max_price = max(int(user_input[0].strip()), int(user_input[1].strip()))
            where = f"\n AND ads.price < {max_price} AND ads.price > {min_price}"
            order = f"\n ORDER BY ads.price"
        case "4":
            user_input = input("введите наименование города: >>> ")
            where = f"\n AND adr.address LIKE '%{user_input}%'"
        case "5":
            user_input = input("введите пользователя и цену через запятую: >>> ")
            user_input = user_input.split(",")
            user_name = user_input[0].strip()
            user_price = user_input[1].strip()
            where = f"\n AND aut.name = {user_name!r} AND ads.price = {user_price}"
        case "6":
            return "stop"
        case _:
            return ""

    return get_base_req() + where + order  # базовый запрос+условия+сортировка


def get_print(rez: list[tuple]) -> None:
    """ красивый вывод результата выполнения запроса """
    print("--результат--")
    num = 0
    for each in rez:
        num += 1
        print(str(num) + ".", each[1].strip(), ":", str(each[2]).strip(),
              f"--- ({str(each[3]).strip()}: {str(each[4]).strip()})")
        print("   ", str(each[5]).strip().replace('\n', '\n    '))
    print("-" * 20)


def main() -> None:
    """ главный цикл """
    connection = get_connect_bd()  # попытка подключение к бд
    if connection:
        cursor = connection.cursor()  # получение курсора

        while True:
            req = menu()  # вывод меню и ввод пользователя, вернет текст запроса или stop
            if req == "stop":
                break
            try:
                cursor.execute(req)  # выполнение запроса
                rez = cursor.fetchall()
                get_print(rez)
            except:
                print("не удалось выполнить запрос")

        disconntct_bd(connection, cursor)  # закрытие курсора и подключения к бд


if __name__ == '__main__':
    main()
