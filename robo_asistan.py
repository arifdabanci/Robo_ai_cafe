name: RoboAI Haber Otomasyonu

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Kodları depodan çek
        uses: actions/checkout@v3

      - name: Python'u hazırla
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Gerekli kütüphaneleri yükle
        # İŞTE BURAYA google-generativeai EKLENDİ
        run: pip install requests beautifulsoup4 google-generativeai

      - name: Botu çalıştır ve mail at
        env:
          EMAIL_SIFRESI: ${{ secrets.EMAIL_SIFRESI }}
          # YAPAY ZEKA ŞİFRENİ DE BURAYA EKLEDİK Kİ KOD GÖREBİLSİN
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python robo_asistan.py
