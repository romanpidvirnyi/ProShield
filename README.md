# Визначення коефіцієнта захисту захисних споруд цивільного захисту

## Зміст
1. [Налаштування системи](#налаштування-системи)
   - [Генерація SSH-ключів для доступу до GitHub](#генерація-ssh-ключів-для-доступу-до-github)
   - [Git](#налаштування-git-для-різних-систем)
   - [Docker і Docker Compose](#docker-і-docker-compose)

---

## Налаштування системи

### Генерація SSH-ключів для доступу до GitHub

Цей документ описує, як згенерувати SSH-ключі на різних операційних системах для доступу до вашого GitHub-акаунта.

#### Загальні кроки
1. Перевірте, чи у вас вже є SSH-ключі.
2. Якщо ключі вже є, переконайтесь, що вони не використовуються для інших проєктів. Якщо їх немає, створіть новий ключ.
3. Додайте SSH-ключ до GitHub.

#### Інструкції за платформами

##### Windows

1. Відкрийте [Git Bash](https://git-scm.com/downloads).
2. Виконайте команду для створення нового ключа:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   > Якщо ваш клієнт не підтримує `ed25519`, скористайтеся `rsa`:  
   > `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`

3. У відповідь на запит вкажіть місце для збереження ключа (або залиште за замовчуванням, натиснувши `Enter`).
4. Встановіть або залиште порожнім парольну фразу (рекомендується встановити для безпеки).
5. Перевірте, чи ключ успішно створено:
   ```bash
   ls ~/.ssh
   ```
6. Скопіюйте вміст публічного ключа:
   ```bash
   clip < ~/.ssh/id_ed25519.pub
   ```
   > Якщо ключ називається інакше, замініть `id_ed25519.pub` на відповідну назву.
7. Додайте ключ до GitHub (інструкції нижче).

##### macOS

1. Відкрийте **Термінал**.
2. Виконайте команду для створення нового ключа:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   > Якщо ваш клієнт не підтримує `ed25519`, скористайтеся `rsa`:  
   > `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`

3. У відповідь на запит вкажіть місце для збереження ключа (або залиште за замовчуванням, натиснувши `Enter`).
4. Встановіть або залиште порожнім парольну фразу (рекомендується встановити для безпеки).
5. Додайте SSH-ключ до ssh-agent:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add --apple-use-keychain ~/.ssh/id_ed25519
   ```
6. Скопіюйте вміст публічного ключа:
   ```bash
   pbcopy < ~/.ssh/id_ed25519.pub
   ```
   > Якщо ключ називається інакше, замініть `id_ed25519.pub` на відповідну назву.
7. Додайте ключ до GitHub (інструкції нижче).

##### Linux

1. Відкрийте **Термінал**.
2. Виконайте команду для створення нового ключа:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   > Якщо ваш клієнт не підтримує `ed25519`, скористайтеся `rsa`:  
   > `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`

3. У відповідь на запит вкажіть місце для збереження ключа (або залиште за замовчуванням, натиснувши `Enter`).
4. Встановіть або залиште порожнім парольну фразу (рекомендується встановити для безпеки).
5. Додайте SSH-ключ до ssh-agent:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```
6. Скопіюйте вміст публічного ключа:
   ```bash
   cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard
   ```
   > Якщо у вас немає `xclip`, встановіть його за допомогою:
   > ```bash
   > sudo apt install xclip
   > ```
7. Додайте ключ до GitHub (інструкції нижче).

---

### Додавання SSH-ключа до GitHub
1. Увійдіть до вашого GitHub-акаунта.
2. Перейдіть до [SSH and GPG keys](https://github.com/settings/keys):
   - Відкрийте: `Settings` → `SSH and GPG keys` → `New SSH key`.
3. Введіть назву для ключа (наприклад, "My Laptop") і вставте вміст вашого публічного ключа.
4. Натисніть **Add SSH key**.

---

### Перевірка підключення
Перевірте, чи ключ працює:
```bash
ssh -T git@github.com
```
У відповідь має бути приблизно таке повідомлення:
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

---

### Налаштування Git для різних систем

#### Windows
1. Завантажте та встановіть [Git для Windows](https://git-scm.com/download/win).
2. Відкрийте Git Bash і налаштуйте глобальні параметри:
   ```bash
   git config --global user.name "Ваше ім'я"
   git config --global user.email "your_email@example.com"
   ```
3. Перевірте налаштування:
   ```bash
   git config --list
   ```

#### macOS
1. Встановіть Git через Homebrew:
   ```bash
   brew install git
   ```
2. Налаштуйте глобальні параметри:
   ```bash
   git config --global user.name "Ваше ім'я"
   git config --global user.email "your_email@example.com"
   ```
3. Перевірте налаштування:
   ```bash
   git config --list
   ```

#### Linux
1. Встановіть Git через пакетний менеджер (наприклад, для Ubuntu):
   ```bash
   sudo apt update
   sudo apt install git
   ```
2. Налаштуйте глобальні параметри:
   ```bash
   git config --global user.name "Ваше ім'я"
   git config --global user.email "your_email@example.com"
   ```
3. Перевірте налаштування:
   ```bash
   git config --list
   ```

---

### Docker і Docker Compose

Документація для налаштування Docker і Docker Compose буде додана пізніше.
