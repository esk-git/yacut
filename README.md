# Проект `Ya`Cut
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
## Используемые технологии
В данном проекте были применены следующие технологии:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
## Как запустить проект
- Клонировать репозиторий
```
git clone https://github.com/esk-git/yacut.git
```
```
cd yacut
```

- Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
```
source venv/scripts/activate
```
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
```
source venv/bin/activate
```

- Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
- Запустить сервис
```
flask run
```
Открыть [страницу](http://127.0.0.1:5000)
```
http://127.0.0.1:5000
```
## API проекта
Доступен всем желающим. Обслуживает два эндпоинта:
- `POST`-запрос на создание новой короткой ссылки
```
/api/id/
```
тело запроса
```
{
  "url": "string",
  "custom_id": "string"
}
```
- `GET`-запрос на получение оригинальной ссылки по указанному короткому идентификатору.
```
/api/id/<short_id>/
```
#### Автор
Каликов Евгений

![Jokes Card](https://readme-jokes.vercel.app/api)