# Домашнее задание №5
## Разработать клиент-серверное приложение.
- Есть приложение клиента, есть приложение сервера;
- Сервер открывает сетевой сокет по порту и ждёт соединения;
- Первым и единственным аргументом у приложения сервера задаётся путь до конфигурационного файла (конфиг);
- Что должно содержаться в конфиге:
    - Номер порта;
    - Путь до лога. Может быть пустым и тогда вся информация должна печатать в стандартный поток вывода;
    - Режим запуска (демон или нет);
    - Таймаут;
    - Максимальное количество соединений.
- Очевидно, что параметры конфига должны быть распределены по секциям;
- Каждый запрос сервер должен логировать. Должно быть указано время начала обработки запроса, время окончания запроса, затраченное на обработку запроса время, размер ответа и т.д.
- Сделать поддержку разного формата ответа. Клиент будет передавать параметр, в каком формате он хочет получить ответ от сервера format=[xml|json];
- Первым аргументом у приложения-клиента задаётся запрос, который необходимо отправить на сервер (запрос состоит из параметров, один из параметров format, остальные зависят от бизнес-логики);
- Клиент ждёт ответ;
- Сервер получает запрос, парсит его, делает бизнес-логику (например ходит за информацией в сторонний сервис по API (например API duckduckgo)), формирует результат и возвращает его клиенту;
- Бизнес-логика не должна быть тривиальной. Перевод в верхний/нижний регистр входящего запроса считается тривиальной бизнес-логикой;
- Клиент печатает ответ сервера в стандартный вывод, далее клиент завершает работу;
- Код должен быть оформлен согласно PEP-8 (*pylint* в помощь);
- В случае ошибки (таймаут, отсутствие необходимых параметров), инцидент должен быть залогирован;


Пример запуска сервера (да, нужно прописать [shebang](https://ru.wikipedia.org/wiki/%D0%A8%D0%B5%D0%B1%D0%B0%D0%BD%D0%B3_(Unix)) в скриптах и сделать файлы исполняемыми при помощи chmod +x):

```bash
./server.py config
```

Пример запуска клиента:

```bash
./client.py "q=Москва&format=json&n=3"
```

Пример ответа клиента (понятное дело, что полей должно быть больше):
```json
{
   "results" : [
      {
         "title" : "Москва — Википедия"
      },
      {
         "title" : "История / Информация / Город / Сайт Москвы"
      },
      {
         "title" : "Агентство городских новостей «Москва»"
      }
   ],
    "error": null
}
```

##### Подсказка
Чтобы распарсить конфиг можно (или нужно?) использовать библиотеку Python [configparser](https://docs.python.org/3/library/configparser.html).