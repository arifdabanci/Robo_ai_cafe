import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

def haber_analiz():
    # Bing üzerinden haberleri tara
    url = "https://www.bing.com/news/search?q=robotic+service+cafe+AI"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    haber_listesi = soup.find_all('a', class_='title', limit=3)
    
    # Rapor Başlığı
    rapor = "🤖 ROBOAI CAFE - GÜNLÜK VİZYON VE STRATEJİ BÜLTENİ\n"
    rapor += "--------------------------------------------------\n\n"
    
    for i, h in enumerate(haber_listesi):
        baslik = h.text
        link = h['href']
        
        # Sektörel Yorumlama Mantığı
        rapor += f"📰 HABER {i+1}: {baslik}\n"
        rapor += f"🔗 LİNK: {link}\n"
        
        # Basit AI Yorumu
        if any(x in baslik.lower() for x in ["cost", "price", "economy"]):
            yorum = "💡 STRATEJİ: Bu gelişme, kafedeki işletme maliyetlerini düşürmek için kullanılabilir."
        elif any(x in baslik.lower() for x in ["experience", "customer", "service"]):
            yorum = "💡 STRATEJİ: Müşteri memnuniyetini artıracak yeni bir 'deneyim' fırsatı sunuyor."
        else:
            yorum = "💡 STRATEJİ: Sektörün büyüme yönünü gösteren genel bir trend. Not almalısın."
        
        rapor += yorum + "\n\n"
        
    rapor += "--------------------------------------------------\n"
    rapor += "Bu rapor GitHub Actions tarafından otomatik oluşturulmuştur."
    return rapor

def eposta_gonder(icerik):
    email_user = "arifdabanci377@gmail.com" # Gönderen
    email_pass = os.environ.get('EMAIL_SIFRESI') # Kasadan alınan şifre
    
    msg = MIMEText(icerik, 'plain', 'utf-8')
    msg['Subject'] = '🚀 RoboAI Günlük Vizyonun Hazır!'
    msg['From'] = email_user
    msg['To'] = email_user # Kendine gönderiyorsun

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        print("Bülten başarıyla uçuruldu!")
    except Exception as e:
        print(f"Hata çıktı: {e}")

if __name__ == "__main__":
    bulten = haber_analiz()
    eposta_gonder(bulten)
