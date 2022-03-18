# book-agregator
Парсер популярных книжных онлайн магазинов на Python/Django
Также были применены:
- PostgreSql (избранное, информация о пользователе)
- Redis (создание кэша для сокращения времени пользования)
- Docker (для быстрого развертывания приложения)

<h2>Для запуска в Docker:</h2>
<br>
1. Создайте docker-контейнер из папки book:
    <h3>docker build -t book-agregator .</h3>
<br>
2. Запустите docker-compose:
    <h3>docker-compose up</h3>

