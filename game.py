import random
import os
from typing import List, Set

# Константы и данные
MAX_ATTEMPTS = 5
ALPHABET = ["А",'Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ь','Э','Ю','Я']
WORDS = [
    "ПРОГРАММИРОВАНИЕ", "АЛГОРИТМ", "КОМПЬЮТЕР", "ВИСЕЛИЦА", 
    "СТУДЕНТ", "УНИВЕРСИТЕТ", "ЛЕКЦИЯ", "ПРАКТИКА", 
    "ПИТОН", "КОД", "ФУНКЦИЯ", "ПЕРЕМЕННАЯ", "ЦИКЛ", 
    "УСЛОВИЕ", "СПИСОК", "СЛОВАРЬ", "МНОЖЕСТВО"
]

stats = {
    "games_played": 0,
    "games_won": 0,
    "total_score": 0,
    "best_score": 0,
    "sum_score": 0
}

def main():
    print("Добро пожаловать в игру 'Виселица'!")
    print("Попробуйте угадать слово по буквам.")
    # Загрузка статистики
    global stats
    
    while True:
        # Выбор случайного слова
        secret_word = choose_random_word(WORDS)
        guessed_word = get_masked_word(secret_word)
        guessed_letters = set()
        attempts_left = MAX_ATTEMPTS + len(secret_word)//2
        game_won = False
        letter = ""
        bonus = 0
        print(secret_word)
        # Игровой цикл
        while attempts_left > 0:
           
            clear_console()
            print(f"Попыток осталось: {attempts_left}")
            draw_gallows(attempts_left)
            print("\nСлово: " + guessed_word)
            print("Использованные буквы: " + ", ".join(sorted(guessed_letters)))
            
            # Ввод буквы
            letter="\n"
            while not (get_user_guess(guessed_letters, letter)):
                letter = input()
                letter=letter.upper()
                
        
            
            guessed_letters.add(letter)
            bonus = 0
            for i in range (0,len(secret_word)):
                 if(secret_word[i]==letter):
                      
                       if i+1== len(secret_word):
                           guessed_word = guessed_word[:i]+letter
                       else:
                           guessed_word = guessed_word[:i]+letter+guessed_word[i+1:]
                       bonus=1
            
            attempts_left=attempts_left+bonus-1
           
            if bonus:
                print("Вы угадали!")
            else:
                print("Такой буквы нет")
            
            
            input("\nНажмите Enter чтобы продолжить...")
            
            # Проверка условий окончания игры
            if check_win(secret_word, guessed_word):
                game_won = True
                break
        
        clear_console()
        if game_won:
            print("Поздравляем! Вы выиграли!")
            print(f"Загаданное слово: {secret_word}")
            stats["total_score"]=calculate_score(secret_word, MAX_ATTEMPTS + len(secret_word)//2 - attempts_left)
           
            print (f"Ваш счет:  ",stats["total_score"])
            update_stats(1)
        else:
            print("К сожалению, вы проиграли.")
            print(f"Загаданное слово: {secret_word}")
            update_stats(0)
            draw_gallows(0)
        
        show_stats()
        
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("Спасибо за игру!")
            break

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_random_word(word_list: List[str]) -> str:
    """Выбор случайного слова из списка"""
    return random.choice(word_list)

def get_masked_word(secret_word: str) -> str:
    """Генерация замаскированного слова"""
    str1 = ""
    for i in range (0, len(secret_word)):
     str1 += '?'
    return str1
        

def draw_gallows(attempts_left: int):
    """Отрисовка виселицы в зависимости от количества оставшихся попыток"""
    print("--------")
    if(attempts_left)<5:
        print("|      |")
    else:
        print("|       ")
    if(attempts_left)<4:
        print("|      O")
    else:
        print("|       ")
    if(attempts_left)<3:
        print("|     \\|/")
    else:
        print("|       ")
    if(attempts_left)<2:
        print("|      |")
    else:
        print("|       ")
    if(attempts_left)<1:
        print("|     / \\")
    else:
        print("|      ")
    

def get_user_guess(guessed_letters: Set[str], letter: str) -> bool:
    """Ввод и валидация буквы от пользователя"""
    if len(letter) > 1:
        print("Пожалуйста, введите только одну букву")
        return 0
    else:
        if letter in guessed_letters:
            print("Вы уже называли эту букву")
            return 0
        else:
            if not letter in ALPHABET:
                if letter != "\n":
                    print("Это не буква :(")
                
                return 0
            
            return 1
        
            
            


def check_win(secret_word: str, guessed_word: str) -> bool:
    """Проверка, угадано ли все слово"""
    return secret_word == guessed_word

def calculate_score(secret_word: str, attempts_used: int) -> int:
    """Вычисление счета за игру"""
    return len(secret_word)*10-attempts_used

def update_stats(won: bool):
    """Обновление статистики в памяти"""
    global stats
    stats["games_played"]+=1
    stats["games_won"]+=won
    stats["best_score"]=max(stats["best_score"],stats["total_score"])
    stats["sum_score"]+=stats["total_score"]

def show_stats():
    """Отображение статистики"""
    global stats
    print ("Процент побед: ", (stats["games_won"]*100)//stats["games_played"],"%")
    print ("Средний счет: ", stats["sum_score"]/max(stats["games_played"],1))


    print("\n=== Статистика ===")
    print("Всего игр: ", stats["games_played"])
    print("Побед: ", (stats["games_won"])," (", (stats["games_won"]*100/max(1,stats["games_played"])),"%)")
    print("Лучший счет: ", stats["best_score"])

if __name__ == "__main__":
    main()