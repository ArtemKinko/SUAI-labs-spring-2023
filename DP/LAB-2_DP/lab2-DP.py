import io


A = 3
C = 5
T0 = 1
b = 7
M = 128


def get_alphabet_from_file(alphabet_file_name):
    with io.open(alphabet_file_name, encoding="utf-8") as alphabet_file:
        alphabet = []
        for _ in range(128):
            letter = alphabet_file.read().rsplit()
            alphabet.append(letter)
        alphabet.append(" ")
        return alphabet[0]


def encode_text(text_string, alphabet):
    print("\n--- Кодируем строку:", text_string)
    indexes = []
    gamma = []
    prev_T = T0
    control_summary = []
    for letter in text_string:
        indexes.append(alphabet.index(letter))
        current_gamma = (A * prev_T + C) % M
        prev_T = format(alphabet.index(letter), 'b').count('1')
        control_summary.append(prev_T)
        gamma.append(current_gamma)
    binary_indexes = [format(x, '07b') for x in indexes]
    print("Полученные коды букв текста:\t", binary_indexes)
    print("Соответствующие контрольные суммы:", control_summary)
    binary_gamma = [format(x, '07b') for x in gamma]
    print("Полученная гамма:\t\t\t\t", binary_gamma)
    encoded_indexes = [indexes[i] ^ gamma[i] for i in range(len(gamma))]
    binary_encoded = [format(x, '07b') for x in encoded_indexes]
    print("Полученные закодированные буквы:", binary_encoded)
    encoded_text = ""
    for encoded_index in encoded_indexes:
        encoded_text += alphabet[encoded_index]
    print("Закодированный текст:", encoded_text)
    return encoded_text, gamma


def decode_text(text_string, alphabet, gamma):
    print("\n--- Декодируем текст:", text_string)
    decoded_text = ""
    for i in range(len(text_string)):
        index = alphabet.index(text_string[i])
        decoded_text += alphabet[index ^ gamma[i]]
    print("Декодированный текст:", decoded_text)
    return decoded_text


letters = get_alphabet_from_file("symbols.txt")
string_to_decode = "Какой_прекрасный_день"
encoded_text, gamma_text = encode_text(string_to_decode, letters)
decoded_text = decode_text(encoded_text, letters, gamma_text)
