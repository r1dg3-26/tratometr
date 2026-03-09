# [RU] Тратометр

Телеграм-бот для отслеживания расходов и доходов.

## Возможности
- Регистрация через /start
- Добавление расходов и доходов
- Хранение и вывод истории операций

## Требования
- Python
- PostgreSQL

## Установка
1. Клонируй репозиторий
2. Создай venv, войди в него `source venv/bin/activate` и установи зависимости `pip install -r requirements.txt`
3. Создай базу данных и исполни команды из директории sql
4. Задай переменные окружения
5. Запусти: `python main.py`

## Переменные окружения
| Переменная | Описание |
|------------|----------|
| TG_TOKEN   | Токен Telegram бота |
| PSQL_IP    | Хост PostgreSQL |
| PSQL_PORT  | Порт PostgreSQL |
| PSQL_USER  | Пользователь PostgreSQL |
| PSQL_PASS  | Пароль PostgreSQL |
| PSQL_DB    | Название базы данных |

## Использование
- /start — регистрация
- /operations — вывести все операции
- /timezone 5 — установить часовой пояс
- /balance 1000 — установить баланс
- -50 обед — списать расход
- +1000 зарплата — добавить доход

---

# [EN] Tratometr

Telegram bot for tracking expenses and income.

## Features
- Registration via /start
- Adding expenses and income
- Storing and viewing operation history

## Requirements
- Python
- PostgreSQL

## Installation
1. Clone the repository
2. Create a venv, activate it `source venv/bin/activate` and install dependencies `pip install -r requirements.txt`
3. Create a database and execute the commands from the sql directory
4. Set environment variables
5. Run: `python main.py`

## Environment Variables
| Variable   | Description |
|------------|-------------|
| TG_TOKEN   | Telegram bot token |
| PSQL_IP    | PostgreSQL host |
| PSQL_PORT  | PostgreSQL port |
| PSQL_USER  | PostgreSQL user |
| PSQL_PASS  | PostgreSQL password |
| PSQL_DB    | PostgreSQL database name |

## Usage
- /start — register
- /operations — show all operations
- /timezone 5 — set timezone
- /balance 1000 — set balance
- -50 lunch — log expense
- +1000 salary — log income