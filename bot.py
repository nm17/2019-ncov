from datetime import datetime

from colorama import init

from config import TOKEN
from game import nCoV
from texts import *

init(autoreset=True)

wrapper = nCoV(
    access_token=TOKEN,
)

ill = f"{Fore.RED}Болен{Style.RESET_ALL}"
healthy = f"{Fore.GREEN}Здоров{Style.RESET_ALL}"

i = 0

while True:
    index = wrapper.index()
    is_ill = index["user"]["state"] == "ILL"
    time_before_death = (
            datetime.strptime(index["user"]["kill_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            - datetime.now()
    )
    if i % 20 == 0:
        print(
            f"{Fore.LIGHTCYAN_EX}[{index['user']['me']['name']}]{Style.RESET_ALL} {ill if is_ill else healthy}. Смерть через {time_before_death}. Таблеток: {index['user']['item_count']}"
        )
    if index["government"]:
        if index["government"]["type"] == "pill":
            wrapper.government_take()
            print(
                f"{Fore.LIGHTCYAN_EX}[{index['user']['me']['name']}]{Style.RESET_ALL} {Fore.GREEN}Получил{Style.RESET_ALL} таблетку от государства."
            )
    friends = wrapper.top("friends")
    for pill in friends["pill"]:
        wrapper.government_steal(pill)
        print(
            f"{Fore.LIGHTCYAN_EX}[{index['user']['me']['name']}]{Style.RESET_ALL} {Fore.GREEN}Своровал{Style.RESET_ALL} таблетку у https://vk.com/id{pill}."
        )

    if 86400 - time_before_death.total_seconds() < 18000:
        wrapper.eat()
        print(
            f"{Fore.LIGHTCYAN_EX}[{index['user']['me']['name']}]{Style.RESET_ALL} {Fore.GREEN}Съел таблетку."
        )

    i += 1
