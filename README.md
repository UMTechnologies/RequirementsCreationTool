# RequirementsCreationTool

<span style = 'color: whitesmoke'>Проект предоставляет инструмент для автоматической генерации файла `requirements.txt` на основе импортов в вашем Python-проекте.

## Особенности

- Автоматическое обнаружение всех Python-файлов в вашем проекте.
- Учитывает `.gitignore` при сканировании файлов.
- Опциональное добавление последних версий библиотек.

## Установка

1. Убедитесь, что у вас установлен Python 3.
2. Клонируйте репозиторий:

```bash
git clone https://github.com/UMTechnologies/RequirementsCreationTool.git
cd RequirementsCreationTool
```

3. Установите необходимые зависимости:

```bash
pip install pathspec
pip install tqdm
```

## Использование

Для генерации файла `requirements.txt` без версий:

```bash
python main.py
```

Для генерации файла `requirements.txt` с последними версиями библиотек:

```bash
python main.py --add_last_versions
```

Для генерации файла `requirements.txt` для библиотек, у которых были найдены версии:

```bash
python main.py --only_packets_w_versions
```

После выполнения команды выберите папку с вашим проектом.

## Лицензия


Этот проект лицензирован под лицензией Creative Commons Attribution 4.0 International License. Вы свободны:

- **Делиться** — копировать и распространять материал на любом носителе и в любом формате.
- **Адаптировать** — ремикшировать, изменять и создавать произведения на основе материала для любых целей, включая коммерческие.

При соблюдении следующих условий:

- **Attribution (Указание авторства)** — Вы должны указать авторство, предоставить ссылку на лицензию и указать на наличие изменений. Вы можете это делать любым разумным способом, но не таким образом, чтобы создавалось впечатление, что лицензиар поддерживает вас или использование вами данного произведения.

Подробнее о лицензии можно прочитать [здесь](https://creativecommons.org/licenses/by/4.0/).
