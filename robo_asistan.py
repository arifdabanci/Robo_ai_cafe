import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

def haber_icerigi_oku(url):
    """Haber linkine gider ve ana metni çeker."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Sayfadaki paragrafları birleştirerek içeriği anla
        paragraflar = soup.find_all('p')
        icerik = " ".join([p.text for p in paragraflar[:5]]) # İlk 5 paragraf genelde özettir
        return icerik if len(icerik) > 100 else "İçerik çekilemedi."
    except:
        return "Bağlantı hatası."

def stratejik_analiz_yap(baslik, icerik):
    """Haberi profesyonel bir perspektifle yorumlar."""
    analiz = {
        "ozet": "",
        "yorum": ""
    }
    
    # Profesyonel Özetleme (Basit NLP Mantığı)
    if "profit" in icerik.lower() or "revenue" in icerik.lower():
        analiz["ozet"] = "Bu rapor, robotik sistemlerin işletme maliyetleri ve kârlılık üzerindeki doğrudan etkisini inceliyor."
        analiz["yorum"] = "Kendi iş modelinde (RoboAI Cafe) ROI (Yatırım Getirisi) hesaplarken bu verileri kullanmalısın. Özellikle personel maliyeti tasarrufu ön planda."
    elif "customer" in icerik.lower() or "experience" in icerik.lower():
        analiz["ozet"] = "Haber, otomasyonun müşteri memnuniyeti ve sadakati üzerindeki psikolojik etkilerine odaklanıyor."
        analiz["yorum"] = "Müşterilerin robotlarla etkileşim kurarken 'kişiselleştirme' beklediğini gösteriyor. Servis robotlarını sadece taşıyıcı değil, birer karakter olarak tasarlamalıyız."
    else:
        analiz["ozet"] = "Sektördeki teknolojik altyapı ve yeni nesil donanım entegrasyonu hakkında teknik bilgiler içeriyor."
        analiz["yorum"] = "Lindy Etkisi'ni düşünürsek, bu yeni teknolojilerin hangilerinin kalıcı olacağını gözlemlemeli ve yatırım planına dahil etmelisin."
        
    return analiz

def bulten_olustur():
    url = "https://www.bing.com/news/search?q=robotic+service+cafe+AI"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    haber_listesi = soup.find_all('a', class_='title', limit=3)
    
    rapor = "🚀 ROBOAI CAFE - PROFESYONEL STRATEJİ RAPORU\n"
    rapor += "="*50 + "\n\n"
    
    for i, h in enumerate(haber_listesi):
        baslik = h.text
        link = h['href']
        metin = haber_icerigi_oku(link)
        analiz = stratejik_analiz_yap(baslik, metin)
        
        rapor += f"【 HABER {i+1} 】: {baslik}\n"
        rapor += f"🔗 LİNK: {link}\n\n"
        rapor += f"📋 ÖNEMLİ NOKTALAR:\n{analiz['ozet']}\n\n"
        rapor += f"🎯 STRATEJİK YORUM (Senin İçin):\n{analiz['yorum']}\n"
        rapor += "-"*50 + "\n\n"
        
    rapor += "Bu rapor senin stratejik avantajın için özel olarak analiz edilmiştir."
    return rapor

# E-posta gönderme fonksiyonu aynı kalacak...
