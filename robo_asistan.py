import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai
import random

GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')

def haberi_cevir_ve_analiz_et(baslik, link, ham_metin):
    if not GOOGLE_API_KEY:
        return "<p>API Anahtarı Eksik! GitHub Secrets kontrol edin.</p>"
        
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # PROMPT DEĞİŞTİ: Artık sadece kafe değil, genel iş fırsatı ve risk analizi yapıyor.
    prompt = f"""
    Sen Ray Dalio'nun "Fikir Meritokrasisi" ve Nassim Taleb'in "Lindy Etkisi" felsefelerini benimsemiş üst düzey bir strateji ve yatırım danışmanısın.
    Aşağıdaki metni analiz et.
    
    Görevlerin:
    1. Haberin detaylı, en az 3-4 paragraflık kapsamlı bir TÜRKÇE özetini çıkar.
    2. Haberdeki teknolojiyi veya gelişmeyi, yeni bir İŞ FİKRİ veya PAZAR FIRSATI olarak TAMAMEN OBJEKTİF analiz et. (Kendini kafe sektörüyle sınırlama, haberin sektörü neyse ona göre değerlendir).
    3. Sermayesini akıllıca kullanmak zorunda olan vizyoner bir girişimci için bu konseptin FIRSATLARI (Kârlılık, pazardaki boşluk, ölçeklenebilirlik) ve RİSKLERİ (Kırılganlık, AR-GE maliyeti, teknolojik eskime) dengeli sun.
    
    Haber Başlığı: {baslik}
    Metin: {ham_metin}
    
    Cevabını SADECE aşağıdaki HTML şablonuna uygun ver. Kod bloğu (```html) kullanma, doğrudan HTML etiketleriyle başla:
    
    <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); font-family: 'Segoe UI', Arial, sans-serif;">
        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 0;">📰 {baslik}</h2>
        <p><a href="{link}" style="color: #3498db; text-decoration: none; font-size: 14px; font-weight: bold;">🔗 Haberin Orijinal Kaynağına Git</a></p>
        
        <h3 style="color: #34495e; margin-top: 25px;">📑 Kapsamlı Özet</h3>
        <p style="font-size: 15px; line-height: 1.7; color: #444;">[Buraya 3-4 paragraflık uzun ve detaylı özeti yaz]</p>
        
        <h3 style="color: #27ae60; margin-top: 25px;">💡 İş Fikri Olarak Fırsatlar (Upside)</h3>
        <ul style="font-size: 15px; line-height: 1.6; color: #444;">
            <li>[Fırsat 1]</li>
            <li>[Fırsat 2]</li>
        </ul>
        
        <h3 style="color: #c0392b; margin-top: 25px;">⚠️ Sektörel Riskler ve Kırılganlık (Downside)</h3>
        <ul style="font-size: 15px; line-height: 1.6; color: #444;">
            <li>[Risk 1]</li>
            <li>[Risk 2]</li>
        </ul>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-left: 5px solid #8e44ad; margin-top: 25px; border-radius: 0 8px 8px 0;">
            <h4 style="color: #8e44ad; margin-top: 0;">🎯 Yatırım ve Aksiyon Stratejisi</h3>
            <p style="font-size: 15px; margin-bottom: 0; color: #333;">[Bu haberi okuyan bir girişimci ne yapmalı? Bu alana nasıl girmeli veya uzak mı durmalı? Objektif nihai tavsiye]</p>
        </div>
    </div>
    """
    try:
        response = model.generate_content(prompt)
        html_cikti = response.text.replace('```html', '').replace('```', '').strip()
        return html_cikti
    except Exception as e:
        return f"<p>API Hatası: {e}</p>"

def bulten_hazirla():
    arama_terimleri = [
        "artificial intelligence business opportunities",
        "robotics startup trends automation",
        "AI service industry disruption",
        "autonomous technology market gaps",
        "future of AI automation profitable"
    ]
    gunun_terimi = random.choice(arama_terimleri)
    arama_motoru = "https://www.bing.com"
    url = arama_motoru + "/news/search?q=" + gunun_terimi.replace(' ', '+')

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    haberler = soup.find_all('a', class_='title', limit=3)
    
    rapor = f"""
    <html>
    <body style="background-color: #e9ecef; padding: 20px;">
        <div style="max-width: 800px; margin: auto;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2c3e50; font-family: 'Segoe UI', Arial, sans-serif; margin-bottom: 5px;">🌍 GLOBAL AI & OTOMASYON VİZYONU</h1>
                <p style="color: #7f8c8d; font-family: Arial, sans-serif; font-size: 16px;">Bugünün Araştırma Odağı: <b>{gunun_terimi.upper()}</b></p>
            </div>
    """
    
    for i, h in enumerate(haberler):
        baslik = h.text
        link = h['href']
        
        try:
            res = requests.get(link, headers=headers, timeout=10)
            detay_soup = BeautifulSoup(res.text, 'html.parser')
            ham_metin = " ".join([p.text for p in detay_soup.find_all('p')])[:3500]
        except:
            ham_metin = "Siteye erişilemedi, sadece başlığı yorumla."
            
        print(f"Yapay zeka analiz ediyor: {baslik}")
        ai_analizi = haberi_cevir_ve_analiz_et(baslik, link, ham_metin)
        rapor += ai_analizi
        
    rapor += """
        </div>
    </body>
    </html>
    """
    return rapor

def eposta_gonder(icerik):
    email_user = "arifdabanci377@gmail.com"
    email_pass = os.environ.get('EMAIL_SIFRESI')
    
    msg = MIMEText(icerik, 'html', 'utf-8')
    msg['Subject'] = '🚀 Yeni İş Fikirleri ve AI Otomasyon Analizin Hazır!'
    msg['From'] = email_user
    msg['To'] = email_user

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_user, email_pass)
        server.send_message(msg)

if __name__ == "__main__":
    print("Global Sistem Başlatılıyor...")
    rapor_metni = bulten_hazirla()
    eposta_gonder(rapor_metni)
    print("Harika tasarımlı global e-posta gönderildi!")
