---

<h1 align="center">Yescoin Bot</h1>

<p align="center">Automate tasks in Yescoin to enhance your efficiency and maximize your results! 🚀</p>

---

## 🚀 **About the Bot**

Yescoin Bot is your go-to automation tool for Yescoin, designed to simplify your workflow and boost productivity. With Yescoin Bot, you get:

- 🤖 **Auto Task:** Automatically solve tasks.
- 🌾 **Auto Farming:** Enjoy automatic farming for an abundant harvest.
- 🚀 **Auto Upgrade:** Upgrade automatically for optimal performance.
- 👥 **Multi-Account Support:** Manage multiple accounts simultaneously.
- 🔌 **Proxy Support:** Dynamically assign proxies to each account.
- 🧵 **Thread System:** Execute tasks concurrently using configurable threads.
- ⏱️ **Delay Loop & Account Switching:** Configure custom delays for looping tasks and switching between accounts.
- 💎 **Auto Open Chest:** Automatically open chests to claim rewards.
- ♻️ **Auto Recovery Pool:** Automatically perform pool recovery to maintain account stability.

Yescoin Bot is built to save you time and maximize outcomes without manual intervention.

---

## 🌟 Version v1.0.2

### Updates

- **Auto Open Chest System:** The bot now automatically opens chests to claim rewards.
- **Auto Recovery Pool System:** The bot can automatically perform pool recovery to maintain account stability.
- **System Optimizations:** Performance and stability improvements across several features.

---

## ⚙️ **Configuration in `config.json`**

Below is the updated configuration for Yescoin Bot:

| **Function**           | **Description**                             | **Default** |
| ---------------------- | ------------------------------------------- | ----------- |
| `task`                 | Automatically solving tasks                 | `true`      |
| `upgrade`              | Auto-upgrade for optimal performance        | `true`      |
| `farming`              | Automatic farming for abundant harvest      | `true`      |
| `proxy`                | Enable proxy usage for account management   | `false`     |
| `thread`               | Number of threads for concurrent tasks      | `1`         |
| `delay_account_switch` | Delay between account switches (in seconds) | `10`        |
| `delay_loop`           | Delay before the next loop (in seconds)     | `3000`      |

And here is a sample `config.json`:

```json
{
  "task": true,
  "upgrade": true,
  "farming": true,
  "proxy": false,
  "thread": 1,
  "delay_account_switch": 10,
  "delay_loop": 3000
}
```

---

## 📥 **How to Register**

Start using Yescoin Bot by registering through the following link:

<div align="center">
  <a href="https://t.me/theYescoin_bot/Yescoin?startapp=RTQrBY" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Yescoin&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---

## 📖 **Installation Steps**

1. **Clone the Repository**  
   Copy the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/yescoin-bot.git
   ```

2. **Navigate to the Project Folder**  
   Move to the project directory:

   ```bash
   cd yescoin-bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Query**  
   Create a `query.txt` file and add your Yescoin query data.

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the following format:

   ```
   http://username:password@ip:port
   ```

   - Only HTTP and HTTPS proxies are supported.

6. **Run the Bot**  
   Execute the bot using the following command:

   ```bash
   python main.py
   ```

---

## 🛠️ **Contributing**

This project is developed by **Livexords**. If you have suggestions, questions, or would like to contribute, feel free to contact us:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
