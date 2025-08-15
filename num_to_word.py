from random import randint


def number_to_words(num, ed=""):
    units_map = {"": ["", "один", "два", "три", "четыре", "пять",
                      "шесть", "семь", "восемь", "девять"],
                 "rub": ["", "один", "два", "три", "четыре", "пять",
                         "шесть", "семь", "восемь", "девять"],
                 "kop": ["", "одна", "две", "три", "четыре", "пять",
                         "шесть", "семь", "восемь", "девять"]
                 }
    units_female = ["", "одна", "две", "три", "четыре", "пять",
                    "шесть", "семь", "восемь", "девять"]  # Для тысяч
    teens = ["десять", "одиннадцать", "двенадцать",
             "тринадцать", "четырнадцать", "пятнадцать",
             "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
    tens = ["", "десять", "двадцать", "тридцать", "сорок", "пятьдесят",
            "шестьдесят", "семьдесят", "восемьдесят", "девяносто"]
    hundreds = ["", "сто", "двести", "триста", "четыреста",
                "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот"]
    thousands = ["тысяча", "тысячи", "тысяч"]
    millions = ["миллион", "миллиона", "миллионов"]
    ed_map = {
        "rub": ["рубль", "рубля", "рублей"],
        "kop": ["копейка", "копейки", "копеек"]
        }

    if num == 0:
        if ed == "rub":
            return "ноль рублей"
        if ed == "kop":
            return "ноль копеек"
        return "ноль"

    def get_thousand_word(n):
        if 10 <= n % 100 <= 20:
            return thousands[2]
        if n % 10 == 1:
            return thousands[0]
        if 2 <= n % 10 <= 4:
            return thousands[1]
        return thousands[2]

    def get_million_word(n):
        if 10 <= n % 100 <= 20:
            return millions[2]
        if n % 10 == 1:
            return millions[0]
        if 2 <= n % 10 <= 4:
            return millions[1]
        return millions[2]

    def get_end_word(n, ed):
        if 10 <= n % 100 <= 20:
            return ed_map[ed][2]
        if n % 10 == 1:
            return ed_map[ed][0]
        if 2 <= n % 10 <= 4:
            return ed_map[ed][1]
        return ed_map[ed][2]

    def convert_chunk(n, is_thousand=False):
        if n == 0:
            return ""
        words = []
        if n // 100 > 0:
            words.append(hundreds[n // 100])
        if n % 100 >= 20:
            words.append(tens[(n % 100) // 10])
            if n % 10 > 0:
                words.append(units_female[n % 10]
                             if is_thousand else units_map[ed][n % 10])
        elif 10 <= n % 100 < 20:
            words.append(teens[n % 10])
        else:
            words.append(units_female[n % 10]
                         if is_thousand else units_map[ed][n % 10])
        # print("WORDS")
        # print(words)
        return ' '.join([word for word in words if word])

    words = []
    if num // 1000000 > 0:
        million_chunk = num // 1000000
        words.append(convert_chunk(million_chunk))
        words.append(get_million_word(million_chunk))
        num %= 1000000
    if num // 1000 > 0:
        thousand_chunk = num // 1000
        words.append(convert_chunk(thousand_chunk, is_thousand=True))
        words.append(get_thousand_word(thousand_chunk))
        num %= 1000
    if num > 0:
        words.append(convert_chunk(num))

    if ed == "rub" or ed == "kop":
        # Добавляем еденицу измерения в правильном склонении
        words.append(get_end_word(num, ed))
    return ' '.join([word for word in words if word])


if __name__ == "__main__":
    print("Hello world!")
    a = 0
    b = 123456789
    for i in range(10):
        num = randint(a, b)
        word = number_to_words(num)
        print("{}".format(i), end=" _ ")
        print("{:,}".format(num).replace(",", " "))
        print("{}".format(word))
