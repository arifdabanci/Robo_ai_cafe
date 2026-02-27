import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
import re

def metni_temizle(metin):
    # Reklam ve menü yazılarını (Abone ol, Privacy Policy vb.) filtrele
    gereksizler = ["privacy policy", "terms of service", "sign up", "subscribe", "cookies", "press enter"]
    for kelime in gereksizler:
        if kelime in metin.lower():
            return ""
    return metin.strip()

def haber_derin_analiz(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Sadece anlamlı paragrafları al ve temizle
        paragraflar = []
        for p in soup.find_all('p'):
            temiz = metni_temizle(p.text)
            if len(temiz) > 60: # Çok kısa satırları (menü elemanlarını) atla
                paragraflar.append(temiz)
        
        if not paragraflar:
            return "İçerik çekilemedi, web sitesi bot korumalı olabilir.", "N/A"

        # Özet ve Sonuç kısımlarını belirle
        ozet = " ".join(paragraflar[:2])
        sonuc = paragraflar[-1] if len(paragraflar) > 2 else "Haberin detayları vizyonuna katkı sağlayacak teknik veriler içeriyor."
        
        return ozet, sonuc
    except:
        return "Bağlantı sağlanamadı.", "N/A"

def turkce_strateji_uret(baslik, icerik):
    # Basit bir çeviri/yorumlama motoru (AI API'si bağlayana kadar en iyisi bu)
    baslik_l = baslik.lower()
    icerik_l = icerik.lower()
    
    strateji = {
        "ozet": "Haber, robotik servislerin otel ve kafe sektöründeki yeni entegrasyon süreçlerini ele alıyor.",
        "aksiyon": "Uzun vadeli planda bu teknolojiyi yerelleştirip maliyet avantajı sağlamalıyız."
    }

    if "profit" in baslik_l or "money" in icerik_l:
        strateji["ozet"] = "Bu rapor, robotik kafelerin klasik kafelere göre kârlılık oranlarını ve yatırımın geri dönüş süresini (ROI) inceliyor."
        strateji["aksiyon"] = "70.000 TL borç yönetiminde, bu tür otomasyonların personel giderini nasıl kâra dönüştürdüğünü finansal planına ekle."
    elif "launch" in baslik_l or "new" in icerik_l:
        strateji["ozet"] = "Yeni bir AI servis robotu piyasaya sürüldü. Sektördeki donanım rekabeti kızışıyor."
        strateji["aksiyon"] = "RoboAI Cafe için en dayanıklı ve Lindy Etkisi'ne (zamana direnen) uygun donanımı seçmek için bu lansmanları takip et."

    return strateji

def rapor_olustur():
    url = "https://www.bing.com/news/search?q=robotic+service+cafe+AI"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    haberler = soup.find_all('a', class_='title', limit=3)
    
    rapor = "💎 ROBOAI CAFE - ELITE STRATEJİ RAPORU\n"
    rapor += "="*60 + "\n\n"
    
    for i, h in enumerate(haberler):
        baslik = h.text
        ozet_ham, sonuc_ham = haber_derin_analiz(h['href'])
        analiz = turkce_strateji_uret(baslik, ozet_ham)
        
        rapor += f"【 ANALİZ {i+1} 】: {baslik.upper()}\n"
        rapor += f"🔗 KAYNAK: {h['href']}\n\n"
        rapor += f"📝 PROFESYONEL ÖZET:\n{analiz['ozet']}\n\n"
        rapor += f"🎯 SENİN İÇİN STRATEJİK AKSİYON:\n{analiz['aksiyon']}\n"
        rapor += "-"*60 + "\n\n"
        
    return rapor

# eposta_gonder ve if __name__ == "__main__" bölümleri aynı kalacak
