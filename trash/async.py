import asyncio
import time


async def sand_mail(num):
    print("Отправлено {}")
    await asyncio.sleep(1)
    print("Доставленно {}".format(num))


async def main():
    tasks = [sand_mail(i) for i in range(10)]
    await asyncio.gather(*tasks)


start_time = time.time()
asyncio.run(main())
print(f'Время выполнения программы: {time.time() - start_time} с')