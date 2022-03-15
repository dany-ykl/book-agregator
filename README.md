# book-agregator
Парсер популярных книжных онлайн магазинов на Python/Django
Также были применены:
- PostgreSql (избранное, информация о пользователе)
- Redis (создание кэша для сокращения времени пользования)
- Docker (для быстрого развертывания приложения)

<h2>Для запуска в Docker:</h2>

1. Создайте docker-контейнер из папки book
    docker build -t book-agregator
    
2. Запустите docker-compose:
    docker-compose up

