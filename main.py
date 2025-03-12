from datetime import datetime
import json
import time
from colorama import Fore
import requests
import re
import urllib.parse


class yescoin:
    BASE_URL = "https://api-backend.yescoin.fun/"
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "content-type": "application/json",
        "origin": "https://www.yescoin.fun",
        "priority": "u=1, i",
        "referer": "https://www.yescoin.fun/",
        "sec-ch-ua": '"Microsoft Edge";v="134", "Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge WebView2";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.config = self.load_config()

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Yescoin Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        def reduce_backslashes(s: str) -> str:
            # Untuk setiap grup backslash yang merupakan kelipatan 2,
            # gantikan dengan n/2 backslash, tapi hanya jika benar-benar berlebih.
            def repl(m):
                n = len(m.group(0))
                # Jika n minimal 2, kita ingin output = n // 2
                return "\\" * (n // 2)

            return re.sub(r"(\\+)", repl, s)

        self.log("🔒 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        token = self.query_list[index]
        self.log(f"📋 Using token: {token[:10]}... (truncated for security)", Fore.CYAN)

        # Decode token dari URL-encoded menjadi string biasa
        decoded_token = urllib.parse.unquote(token)

        # Cek apakah token mengandung parameter "user=" atau "query="
        for param in ["user=", "query="]:
            if param in decoded_token:
                start_index = decoded_token.find(param) + len(param)
                end_index = decoded_token.find("&", start_index)
                if end_index == -1:
                    end_index = len(decoded_token)
                json_part = decoded_token[start_index:end_index]
                try:
                    # Parse string JSON menjadi objek Python
                    user_obj = json.loads(json_part)
                    # Proses field photo_url: ubah setiap "/" menjadi "\\/" (hanya sekali)
                    if "photo_url" in user_obj:
                        user_obj["photo_url"] = user_obj["photo_url"].replace(
                            "/", "\\/"
                        )
                    # Dump ulang objek JSON ke string tanpa spasi ekstra
                    dumped = json.dumps(user_obj, separators=(",", ":"))
                    # Ganti tanda kutip ganda (") dengan escape satu kali (\"),
                    # hasilnya misalnya: {\"id\":5438209644,...}
                    escaped = dumped.replace('"', r"\"")
                except Exception as e:
                    self.log(f"❌ JSON parse error: {e}", Fore.RED)
                    escaped = json_part
                # Gantikan bagian JSON dalam decoded_token dengan string yang sudah diproses
                decoded_token = (
                    decoded_token[:start_index] + escaped + decoded_token[end_index:]
                )
                break

        payload = {"code": decoded_token}
        payload["code"] = reduce_backslashes(payload["code"])
        login_url = f"{self.BASE_URL}user/login"

        try:
            self.log("📡 Sending login request...", Fore.CYAN)
            login_response = requests.post(
                login_url, headers=self.HEADERS, json=payload
            )
            login_response.raise_for_status()
            login_data = login_response.json()

            if login_data.get("code") == 0:
                self.token = login_data["data"]["token"]
                self.log("✅ Login successful!", Fore.GREEN)
            else:
                message = login_data.get("message", "Unknown error")
                self.log(f"❌ Login failed: {message}", Fore.RED)
                self.log(f"📄 Response content: {login_response.text}", Fore.RED)
                return

            # Request untuk mendapatkan info akun dengan token yang didapat
            account_url = f"{self.BASE_URL}account/getAccountInfo"
            self.log("📡 Fetching account info...", Fore.CYAN)
            headers = {**self.HEADERS, "Token": self.token}
            account_response = requests.get(account_url, headers=headers)
            account_response.raise_for_status()
            account_data = account_response.json()

            if account_data.get("code") == 0:
                data = account_data.get("data", {})
                self.log("✅ Account info fetched successfully!", Fore.GREEN)
                self.log(
                    f"📊 Invite Amount: {data.get('inviteAmount', 'Unknown')}",
                    Fore.CYAN,
                )
                self.log(
                    f"💰 Total Amount: {data.get('totalAmount', 'Unknown')}", Fore.CYAN
                )
                self.log(
                    f"💸 Current Amount: {data.get('currentAmount', 'Unknown')}",
                    Fore.CYAN,
                )
                self.log(
                    f"⭐ User Level: {data.get('userLevel', 'Unknown')}",
                    Fore.LIGHTYELLOW_EX,
                )
                self.log(
                    f"🆔 User ID: {data.get('userId', 'Unknown')}", Fore.LIGHTGREEN_EX
                )
            else:
                message = account_data.get("message", "Unknown error")
                self.log(f"❌ Failed to fetch account info: {message}", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request failed: {e}", Fore.RED)
            if "login_response" in locals():
                self.log(f"📄 Response content: {login_response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error (JSON decode issue): {e}", Fore.RED)
            if "login_response" in locals():
                self.log(f"📄 Response content: {login_response.text}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Key error: {e}", Fore.RED)
            if "login_response" in locals():
                self.log(f"📄 Response content: {login_response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)
            if "login_response" in locals():
                self.log(f"📄 Response content: {login_response.text}", Fore.RED)

    def farming(self) -> None:
        self.log("📡 Starting farming...", Fore.CYAN)

        # Farming API: collectCoin
        farming_url = f"{self.BASE_URL}game/collectCoin"
        farming_headers = {**self.HEADERS, "Token": self.token}

        data_payload = "100"  # initial payload value
        payload_reduced = False  # flag to track if payload has been reduced

        while True:
            try:
                response = requests.post(
                    farming_url, headers=farming_headers, data=data_payload
                )
            except Exception as e:
                self.log(f"❌ Request error: {e}", Fore.RED)
                break

            if response.status_code != 200:
                self.log(
                    f"❌ Request failed with status code {response.status_code}.",
                    Fore.RED,
                )
                break

            try:
                result = response.json()
            except Exception as e:
                self.log("❌ Error parsing JSON response.", Fore.RED)
                break

            # If the API response code is not 0, handle it accordingly.
            if result.get("code") != 0:
                if not payload_reduced:
                    self.log(
                        f"⚠️ Received error code {result.get('code')}. Reducing payload from 100 to 10 and retrying...",
                        Fore.YELLOW,
                    )
                    data_payload = "10"
                    payload_reduced = True
                    continue  # try again with the reduced payload
                else:
                    self.log(
                        f"❌ Farming collect coin failed with code {result.get('code')}. Message: {result.get('message')}",
                        Fore.RED,
                    )
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
                    break
            else:
                data = result.get("data", {})
                collect_amount = data.get("collectAmount")
                collect_status = data.get("collectStatus")
                current_amount = data.get("currentAmount")
                total_amount = data.get("totalAmount")

                self.log("✅ Farming collect coin successful.", Fore.GREEN)
                self.log(f"💰 Coins Collected: {collect_amount}", Fore.GREEN)
                self.log(f"🔄 Status: {collect_status}", Fore.GREEN)
                self.log(f"📊 Current Amount: {current_amount}", Fore.GREEN)
                self.log(f"🏆 Total Amount: {total_amount}", Fore.GREEN)

            self.log("⏳ Waiting for 5 seconds before the next attempt...", Fore.BLUE)
            time.sleep(5)

    def upgrade(self) -> None:
        self.log("📡 Fetching build info...", Fore.CYAN)
        headers = {**self.HEADERS, "Token": self.token}
        # Ambil build info
        try:
            build_info_url = f"{self.BASE_URL}build/getAccountBuildInfo"
            build_resp = requests.get(build_info_url, headers=headers)
            build_resp.raise_for_status()
            build_json = build_resp.json()
            if build_json.get("code") != 0:
                self.log("❌ Failed to fetch build info.", Fore.RED)
                return
            build_data = build_json.get("data", {})
        except Exception as e:
            self.log(f"❌ Exception fetching build info: {e}", Fore.RED)
            return

        # Ambil upgrade cost (swipeBot tidak ikut)
        try:
            cost_single = build_data.get("singleCoinUpgradeCost", 0)
            cost_recovery = build_data.get("coinPoolRecoveryUpgradeCost", 0)
            cost_total = build_data.get("coinPoolTotalUpgradeCost", 0)
        except Exception as e:
            self.log(f"❌ Error extracting upgrade costs: {e}", Fore.RED)
            return

        upgrade_url = f"{self.BASE_URL}build/levelUp"

        while True:
            # Ambil currentAmount terbaru
            try:
                account_url = f"{self.BASE_URL}account/getAccountInfo"
                acct_resp = requests.get(account_url, headers=headers)
                acct_resp.raise_for_status()
                acct_json = acct_resp.json()
                if acct_json.get("code") != 0:
                    self.log("❌ Failed to fetch account info.", Fore.RED)
                    break
                current_amount = acct_json.get("data", {}).get("currentAmount", 0)
                self.log(f"ℹ️ Current coin amount: {current_amount}", Fore.CYAN)
            except Exception as e:
                self.log(f"❌ Exception fetching account info: {e}", Fore.RED)
                break

            # Buat daftar upgrade yang memungkinkan (index, cost)
            possible = []
            if current_amount >= cost_single and cost_single > 0:
                possible.append((1, cost_single))
            if current_amount >= cost_recovery and cost_recovery > 0:
                possible.append((2, cost_recovery))
            if current_amount >= cost_total and cost_total > 0:
                possible.append((3, cost_total))

            if not possible:
                self.log("ℹ️ Not enough coins to upgrade.", Fore.YELLOW)
                break

            # Pilih upgrade dengan biaya termurah
            upgrade_index = min(possible, key=lambda x: x[1])[0]
            self.log(f"📡 Attempting upgrade index {upgrade_index}...", Fore.CYAN)

            try:
                # Payload hanya berupa data sederhana, misalnya "1" atau "2" atau "3"
                upgrade_payload = str(upgrade_index)
                upgrade_resp = requests.post(
                    upgrade_url, headers=headers, data=upgrade_payload
                )
                upgrade_resp.raise_for_status()
                upgrade_result = upgrade_resp.json()
                if (
                    upgrade_result.get("code") == 0
                    and upgrade_result.get("data") is True
                ):
                    self.log(
                        f"✅ Upgrade (index {upgrade_index}) successful.", Fore.GREEN
                    )
                else:
                    self.log(
                        f"❌ Upgrade (index {upgrade_index}) failed: {upgrade_result.get('message')}",
                        Fore.RED,
                    )
                    break
            except Exception as e:
                self.log(f"❌ Exception during upgrade: {e}", Fore.RED)
                break

            # Tunggu sebentar sebelum mencoba upgrade lagi
            time.sleep(1)

    def task(self) -> None:
        headers = {**self.HEADERS, "Token": self.token}

        # ==========================
        # Process Tasks
        # ==========================
        self.log("📡 Starting tasks...", Fore.CYAN)
        task_list_url = f"{self.BASE_URL}task/getTaskList"

        try:
            response = requests.get(task_list_url, headers=headers)
        except Exception as e:
            self.log(f"❌ Request error while fetching tasks: {e}", Fore.RED)
            return

        if response.status_code != 200:
            self.log(
                f"❌ Request failed with status code {response.status_code} while fetching tasks.",
                Fore.RED,
            )
            return

        try:
            result = response.json()
        except Exception as e:
            self.log("❌ Error parsing JSON response from task list.", Fore.RED)
            return

        if result.get("code") != 0:
            self.log(
                f"❌ Failed to get task list: code {result.get('code')}, message: {result.get('message')}",
                Fore.RED,
            )
            return

        data = result.get("data", {})
        tasks = data.get("taskList", [])
        special_tasks = data.get("specialTaskList", [])
        all_tasks = tasks + special_tasks

        if not all_tasks:
            self.log("ℹ️ No tasks found.", Fore.YELLOW)
        else:
            self.log(f"🔍 Found {len(all_tasks)} tasks.", Fore.BLUE)
            for task_item in all_tasks:
                task_id = task_item.get("taskId")
                task_name = task_item.get("taskName")
                task_status = task_item.get("taskStatus")  # 1 indicates completed
                self.log(f"🚀 Processing Task ID: {task_id} - {task_name}", Fore.CYAN)
                if task_status == 1:
                    self.log(f"ℹ️ Task ID {task_id} is already completed.", Fore.YELLOW)
                    continue

                # 1. Click Task API
                click_url = f"{self.BASE_URL}task/clickTask"
                try:
                    click_response = requests.post(
                        click_url, headers=headers, data=task_id
                    )
                except Exception as e:
                    self.log(
                        f"❌ Request error during clickTask for Task ID {task_id}: {e}",
                        Fore.RED,
                    )
                    continue

                try:
                    click_result = click_response.json()
                except Exception as e:
                    self.log(
                        f"❌ Error parsing JSON from clickTask for Task ID {task_id}.",
                        Fore.RED,
                    )
                    continue

                if click_result.get("code") != 0:
                    self.log(
                        f"❌ clickTask failed for Task ID {task_id}: code {click_result.get('code')}, message: {click_result.get('message')}",
                        Fore.RED,
                    )
                    continue
                else:
                    self.log(
                        f"👍 clickTask successful for Task ID {task_id}.", Fore.GREEN
                    )

                # 2. Check Task API
                check_url = f"{self.BASE_URL}task/checkTask"
                try:
                    check_response = requests.post(
                        check_url, headers=headers, data=task_id
                    )
                except Exception as e:
                    self.log(
                        f"❌ Request error during checkTask for Task ID {task_id}: {e}",
                        Fore.RED,
                    )
                    continue

                try:
                    check_result = check_response.json()
                except Exception as e:
                    self.log(
                        f"❌ Error parsing JSON from checkTask for Task ID {task_id}.",
                        Fore.RED,
                    )
                    continue

                if check_result.get("code") != 0:
                    self.log(
                        f"❌ checkTask failed for Task ID {task_id}: code {check_result.get('code')}, message: {check_result.get('message')}",
                        Fore.RED,
                    )
                    continue
                else:
                    self.log(
                        f"🔍 checkTask successful for Task ID {task_id}.", Fore.GREEN
                    )

                # 3. Claim Task Reward API
                claim_url = f"{self.BASE_URL}task/claimTaskReward"
                try:
                    claim_response = requests.post(
                        claim_url, headers=headers, data=task_id
                    )
                except Exception as e:
                    self.log(
                        f"❌ Request error during claimTaskReward for Task ID {task_id}: {e}",
                        Fore.RED,
                    )
                    continue

                try:
                    claim_result = claim_response.json()
                except Exception as e:
                    self.log(
                        f"❌ Error parsing JSON from claimTaskReward for Task ID {task_id}.",
                        Fore.RED,
                    )
                    continue

                if claim_result.get("code") != 0:
                    self.log(
                        f"❌ claimTaskReward failed for Task ID {task_id}: code {claim_result.get('code')}, message: {claim_result.get('message')}",
                        Fore.RED,
                    )
                else:
                    bonus_amount = claim_result.get("data", {}).get("bonusAmount")
                    feature = claim_result.get("data", {}).get("feature")
                    self.log(
                        f"🏆 Task Reward Claimed for Task ID {task_id}:", Fore.GREEN
                    )
                    self.log(f"   💵 Bonus Amount: {bonus_amount}", Fore.GREEN)
                    self.log(f"   ⚙️ Feature: {feature}", Fore.GREEN)

                self.log(
                    "⏳ Waiting 2 seconds before processing the next task...", Fore.BLUE
                )
                time.sleep(2)

        # ==========================
        # Process Missions
        # ==========================
        self.log("📡 Starting missions...", Fore.CYAN)
        mission_list_url = f"{self.BASE_URL}mission/getDailyMission"

        try:
            response = requests.get(mission_list_url, headers=headers)
        except Exception as e:
            self.log(f"❌ Request error while fetching missions: {e}", Fore.RED)
            return

        if response.status_code != 200:
            self.log(
                f"❌ Request failed with status code {response.status_code} while fetching missions.",
                Fore.RED,
            )
            return

        try:
            result = response.json()
        except Exception as e:
            self.log("❌ Error parsing JSON response from mission list.", Fore.RED)
            return

        if result.get("code") != 0:
            self.log(
                f"❌ Failed to get mission list: code {result.get('code')}, message: {result.get('message')}",
                Fore.RED,
            )
            return

        missions = result.get("data", [])
        if not missions:
            self.log("ℹ️ No missions found.", Fore.YELLOW)
        else:
            self.log(f"🔍 Found {len(missions)} missions.", Fore.BLUE)
            for mission in missions:
                mission_id = mission.get("missionId")
                mission_name = mission.get("name")
                mission_status = mission.get("missionStatus")  # 1 means completed
                self.log(
                    f"🚀 Processing Mission ID: {mission_id} - {mission_name}",
                    Fore.CYAN,
                )
                if mission_status == 1:
                    self.log(
                        f"ℹ️ Mission ID {mission_id} is already completed.", Fore.YELLOW
                    )
                    continue

                # 1. Click Daily Mission API
                click_url = f"{self.BASE_URL}mission/clickDailyMission"
                try:
                    click_response = requests.post(
                        click_url, headers=headers, data=str(mission_id)
                    )
                except Exception as e:
                    self.log(
                        f"❌ Request error during clickDailyMission for Mission ID {mission_id}: {e}",
                        Fore.RED,
                    )
                    continue

                try:
                    click_result = click_response.json()
                except Exception as e:
                    self.log(
                        f"❌ Error parsing JSON from clickDailyMission for Mission ID {mission_id}.",
                        Fore.RED,
                    )
                    continue

                if click_result.get("code") != 0:
                    self.log(
                        f"❌ clickDailyMission failed for Mission ID {mission_id}: code {click_result.get('code')}, message: {click_result.get('message')}",
                        Fore.RED,
                    )
                    continue
                else:
                    self.log(
                        f"👍 clickDailyMission successful for Mission ID {mission_id}.",
                        Fore.GREEN,
                    )

                # 2. Check Daily Mission API
                check_url = f"{self.BASE_URL}mission/checkDailyMission"
                try:
                    check_response = requests.post(
                        check_url, headers=headers, data=str(mission_id)
                    )
                except Exception as e:
                    self.log(
                        f"❌ Request error during checkDailyMission for Mission ID {mission_id}: {e}",
                        Fore.RED,
                    )
                    continue

                try:
                    check_result = check_response.json()
                except Exception as e:
                    self.log(
                        f"❌ Error parsing JSON from checkDailyMission for Mission ID {mission_id}.",
                        Fore.RED,
                    )
                    continue

                if check_result.get("code") != 0:
                    self.log(
                        f"❌ checkDailyMission failed for Mission ID {mission_id}: code {check_result.get('code')}, message: {check_result.get('message')}",
                        Fore.RED,
                    )
                    continue
                else:
                    self.log(
                        f"🔍 checkDailyMission successful for Mission ID {mission_id}.",
                        Fore.GREEN,
                    )

                # 3. Claim Mission Reward API
                claim_url = f"{self.BASE_URL}mission/claimReward"
                try:
                    claim_response = requests.post(
                        claim_url, headers=headers, data=str(mission_id)
                    )
                except Exception as e:
                    self.log(
                        f"❌ Request error during claimReward for Mission ID {mission_id}: {e}",
                        Fore.RED,
                    )
                    continue

                try:
                    claim_result = claim_response.json()
                except Exception as e:
                    self.log(
                        f"❌ Error parsing JSON from claimReward for Mission ID {mission_id}.",
                        Fore.RED,
                    )
                    continue

                if claim_result.get("code") != 0:
                    self.log(
                        f"❌ claimReward failed for Mission ID {mission_id}: code {claim_result.get('code')}, message: {claim_result.get('message')}",
                        Fore.RED,
                    )
                else:
                    bonus_amount = claim_result.get("data", {}).get("bonusAmount")
                    feature = claim_result.get("data", {}).get("feature")
                    self.log(
                        f"🏆 Mission Reward Claimed for Mission ID {mission_id}:",
                        Fore.GREEN,
                    )
                    self.log(f"   💵 Bonus Amount: {bonus_amount}", Fore.GREEN)
                    self.log(f"   ⚙️ Feature: {feature}", Fore.GREEN)

                self.log(
                    "⏳ Waiting 2 seconds before processing the next mission...",
                    Fore.BLUE,
                )
                time.sleep(2)

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]


if __name__ == "__main__":
    yes = yescoin()
    index = 0
    max_index = len(yes.query_list)
    config = yes.load_config()
    if config.get("proxy", False):
        proxies = yes.load_proxies()

    yes.log(
        "🎉 [LIVEXORDS] === Welcome to Yescoin Automation === [LIVEXORDS]", Fore.YELLOW
    )
    yes.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        current_account = yes.query_list[index]
        display_account = (
            current_account[:10] + "..."
            if len(current_account) > 10
            else current_account
        )

        yes.log(
            f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}",
            Fore.YELLOW,
        )

        if config.get("proxy", False):
            yes.override_requests()
        else:
            yes.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

        yes.login(index)

        yes.log("🛠️ Starting task execution...")
        tasks = {
            "task": "Automatically solving tasks 🤖",
            "farming": "Automatic farming for abundant harvest 🌾",
            "upgrade": "Auto-upgrade for optimal performance 🚀"
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            yes.log(
                f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
                Fore.YELLOW if task_status else Fore.RED,
            )

            if task_status:
                yes.log(f"🔄 Executing {task_name}...")
                getattr(yes, task_key)()

        if index == max_index - 1:
            yes.log("🔁 All accounts processed. Restarting loop.")
            yes.log(
                f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting."
            )
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            yes.log(
                f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds."
            )
            time.sleep(config.get("delay_account_switch", 10))
            index += 1
