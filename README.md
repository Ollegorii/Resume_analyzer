## Исследования и описание работы над моделью
Проект для анализа соответствия резюме и вакансий, написанный на студкемпе Яндекс x ВШЭ

Основная механика работы - построение эмбеддингов текстов резюме и вакансий и поиск косинусного расстояния между ними.
В качестве моделей были взяты BoW, TfIdf, W2V, а также SBERT, который был дообучен с помощью сближения соответсвующих текстов резюме и вакансий.
Интерфейс написан на streamlit. Проект работает через fastapi.
## Запуск приложения

### Development

Для запуска приложения в среде разработки доступны варианты запуска напрямую через `python` и
через `docker-compose`. Оба варианта используют для конфигурации переменные окружения, которые
описаны в файле `app/settings/settings.py`. В данных режимах запуска доступно обновление кода приложения
на лету, без перезапуска (кроме случаев добавления новых зависимостей).

#### Python Runner

```bash
python -m fastapi_service
```

#### Docker runner

Перед запуском docker-compose необходимо :

```bash
make build
```

Команда создаст .env из .env.example и сделает "билд" контейнеров.

```bash
make run_build
```

#### Docker runner GPU

Перед запуском docker-compose необходимо :

```bash
make build_cuda
```

Команда создаст .env из .env.example и сделает "билд" контейнеров.

```bash
make run_build_gpu
```
### Разработка

"Линтинг" проекта :

```bash
make lint 
```

### Зависимости

Управлением зависимостями занимается утилита `poetry`. \
Перечень зависимостей находится в файле `pyproject.toml`. \
Инструкция по настройке poetry-окружения для
pyCharm [здесь](https://www.jetbrains.com/help/pycharm/poetry.html).

Для добавления зависимости достаточно написать `poetry add requests`, утилита сама подберёт версию,
не конфликтующую с текущими зависимостями. \
Зависимости с точными версиями фиксируются в файл `poetry.lock`. \
Для получения дерева зависимостей можно воспользоваться командой `poetry show --tree`. Остальные
команды доступны в официальной документации к утилите.

## Важно!

Модели должны быть загружены на S3.
Путь до модели в S3 указывается в переменных окружения описанных в `app/settings/settings.py`.
