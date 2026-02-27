import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai

# Gemini API Ayarları
GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')

def haberi_cevir_ve_analiz_et(baslik, ham_metin):
    if not GOOGLE_API_KEY:
        return "📝 TÜRKÇE ÖZET: API Anahtarı Eksik!\n🎯 STRATEJİK YORUM: Lütfen GitHub Secrets'a GEMINI_API_KEY ekle."
        
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Aşağıdaki metin bir haber sitesinden kazınmıştır. İçinde 'Subscribe', 'Privacy Policy', reklam veya anlamsız kodlar olabilir.
    Senden görevlerin:
    1. Gereksiz tüm çöpleri ve reklamları yok say, haberin asıl konusunu bul.
    2. Haberi profesyonel bir iş diliyle, kusursuz bir TÜRKÇE ile 2 cümlelik özetle.
    3. Bu haberi "RoboAI Cafe" (Robotik servis ve yapay zeka entegreli kafe) kurmak isteyen, otomasyonla maliyetleri düşürmeyi hedefleyen bir girişimci için stratejik olarak yorumla.
    
    Haber Başlığı: {baslik}
    Kazınan Metin: {ham_metin}
    
    Lütfen cevabını sadece şu formatta ver:
    📝 TÜRKÇE ÖZET: [Özet]
    🎯 STRATEJİK YORUM: [Yorum]
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"📝 TÜRKÇE ÖZET: Çeviri yapılamadı.\n🎯 STRATEJİK YORUM: API Hatası ({e})"

def bulten_hazirla():
    url = "https://www.bing.com/news/search?q=robotic+service+cafe+AI"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    haberler = soup.find_all('a', class_='title', limit=3)
    
    rapor = "🧠 ROBOAI CAFE - YAPAY ZEKA DESTEKLİ VİZYON RAPORU\n"
    rapor += "="*65 + "\n\n"
    
    for i, h in enumerate(haberler):
        baslik = h.text
        link = h['href']
        
        try:
            res = requests.get(link, headers=headers, timeout=10)
            detay_soup = BeautifulSoup(res.text, 'html.parser')
            ham_metin = " ".join([p.text for p in detay_soup.find_all('p')])[:3000]
        except:
            ham_metin = "Siteye erişilemedi, sadece başlığa göre yorumla."
            
        print(f"Yapay zeka analiz ediyor: {baslik}")
        ai_analizi = haberi_cevir_ve_analiz_et(baslik, ham_metin)
        
        rapor += f"【 HABER {i+1} 】: {baslik}\n"
        rapor += f"🔗 KAYNAK: {link}\n\n"
        rapor += f"{ai_analizi}\n"
        rapor += "-"*65 + "\n\n"
        
    return rapor

def eposta_gonder(icerik):
    email_user = "arifdabanci377@gmail.com"
    email_pass = os.environ.get('EMAIL_SIFRESI')
    
    msg = MIMEText(icerik, 'plain', 'utf-8')
    msg['Subject'] = '🧠 AI Destekli RoboAI Günlük Raporun!'
    msg['From'] = email_user
    msg['To'] = email_user

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_user, email_pass)
        server.send_message(msg)

if __name__ == "__main__":
    print("Sistem Başlatılıyor...")
    rapor_metni = bulten_hazirla()
    eposta_gonder(rapor_metni)
    print("İşlem Başarılı!")
