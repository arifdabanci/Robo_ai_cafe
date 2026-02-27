import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

def haber_detay_cek(url):
    """Habere gider, ana hatları ve sonuçları bulmaya çalışır."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Sitedeki tüm paragrafları topla
        paragraphs = [p.text.strip() for p in soup.find_all('p') if len(p.text) > 40]
        
        if not paragraphs:
            return "Detaylı içerik çekilemedi, ancak başlık sektör trendini doğruluyor."

        # Ana Hatlar: İlk 3 anlamlı paragraf
        ana_hatlar = " ".join(paragraphs[:3])
        # Sonuç: Genelde son paragraflarda olur
        sonuc = paragraphs[-1] if len(paragraphs) > 3 else ""
        
        return f"{ana_hatlar}\n\n[SONUÇ/ÖNGÖRÜ]: {sonuc}"
    except Exception as e:
        return f"İçerik analizi sırasında teknik bir kısıtlama oluştu: {str(e)}"

def analiz_motoru(baslik, detay):
    """Haberi senin iş modelin için yorumlar."""
    analiz = ""
    detay_lower = detay.lower()
    
    if "robot" in detay_lower or "ai" in detay_lower:
        analiz = "🤖 STRATEJİK YORUM: Bu teknoloji, RoboAI Cafe'de insan hatasını sıfırlamak için kullanılabilir. Özellikle operasyonel hızı artırarak vardiya yükünü hafifletebilir."
    if "profit" in detay_lower or "cost" in detay_lower:
        analiz = "💰 FİNANSAL YORUM: Haberdeki maliyet verileri, 70 bin TL'lik borç yönetiminde nakit akışını optimize etmek için referans alınabilir."
    
    return analiz if analiz else "📈 SEKTÖREL YORUM: Bu gelişme pazarın dijitalleşme hızını gösteriyor, uzun vadeli stratejine dahil etmelisin."

def bulten_hazirla():
    url = "https://www.bing.com/news/search?q=robotic+service+cafe+AI"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    haberler = soup.find_all('a', class_='title', limit=3)
    
    rapor = "🚀 ROBOAI CAFE - DERİN ANALİZ VE STRATEJİ RAPORU\n"
    rapor += "="*60 + "\n\n"
    
    for i, h in enumerate(haberler):
        baslik = h.text
        link = h['href']
        
        print(f"Analiz ediliyor: {baslik}") # Log kaydı için
        detayli_ozet = haber_detay_cek(link)
        strateji = analiz_motoru(baslik, detayli_ozet)
        
        rapor += f"【 HABER {i+1} 】: {baslik.upper()}\n"
        rapor += f"🔗 KAYNAK: {link}\n\n"
        rapor += f"📝 HABERİN ANA HATLARI VE ÖZETİ:\n{detayli_ozet}\n\n"
        rapor += f"{strateji}\n"
        rapor += "-"*60 + "\n\n"
        
    return rapor

# eposta_gonder fonksiyonu (Sende mevcut olanı buraya ekle)
