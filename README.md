# 🧬 Genetik Varyant Yorumlama Uygulaması

Streamlit tabanlı, Google Gemini AI destekli kapsamlı genetik varyant analiz ve yorumlama platformu.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 İçindekiler

- [Genel Bakış](#-genel-bakış)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Veri Kaynakları](#-veri-kaynakları)
- [API Entegrasyonları](#-api-entegrasyonları)
- [Dosya Yapısı](#-dosya-yapısı)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

## 🌟 Genel Bakış

Bu uygulama, genetik varyantların (DNA değişikliklerinin) kapsamlı analizini yapmak için geliştirilmiş modern bir web platformudur. Birden fazla bilimsel veritabanını entegre ederek, yapay zeka destekli yorumlarla klinik düzeyde raporlar üretir.

### 🎯 Hedef Kitle

- **Genetik Uzmanları** - Klinik yorumlama ve hasta değerlendirmesi
- **Araştırmacılar** - Bilimsel çalışmalar ve literatür taraması
- **Biyoinformatik Uzmanları** - Veri analizi ve pipeline entegrasyonu
- **Tıp Öğrencileri** - Eğitim ve öğrenme amaçlı

## ✨ Özellikler

### 🔬 Analiz Yetenekleri
- **Multi-format Dosya Desteği**: VCF, VCF.GZ, CSV formatlarında varyant dosyası işleme
- **Otomatik Veri Eşleştirme**: ClinVar veritabanı ile CHROM:POS:REF:ALT bazlı eşleştirme
- **Kapsamlı Annotation**: 7 farklı veri kaynağından bilgi zenginleştirme
- **AI Yorumlama**: Google Gemini ile profesyonel klinik değerlendirme

### 📊 Veri Zenginleştirme
- **ClinVar**: Klinik önem, hastalık ilişkileri, gen bilgileri
- **ClinGen**: Gen-hastalık geçerlilik sınıflandırmaları
- **gnomAD**: Popülasyon frekansları, allel istatistikleri
- **PubMed**: İlgili bilimsel makale bağlantıları

### 📄 Raporlama Sistemi
- **İnteraktif Görüntüleme**: Streamlit tabanlı dinamik tablolar
- **Profesyonel PDF Raporları**: Hasta bilgileri, grafikler, AI yorumları
- **CSV Export**: Ham veri indirme seçenekleri
- **İstatistiksel Görseller**: Pasta ve bar grafikleri

### 🎨 Kullanıcı Deneyimi
- **Responsive Tasarım**: Masaüstü ve tablet uyumlu arayüz
- **Real-time Progress**: Analiz sürecinde canlı ilerleme takibi
- **Session Management**: Analiz sonuçlarını oturum boyunca saklama
- **Hata Yönetimi**: Kullanıcı dostu hata mesajları ve çözüm önerileri

## 🚀 Kurulum

### Gereksinimler

```bash
Python 3.8+
```

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/yourusername/genetic-variant-interpreter.git
cd genetic-variant-interpreter
```

### 2. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

#### Requirements.txt İçeriği:
```txt
streamlit>=1.28.0
streamlit-option-menu>=0.3.6
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
reportlab>=4.0.0
google-generativeai>=0.3.0
requests>=2.28.0
```

### 3. Veri Dosyalarını Hazırlayın

Aşağıdaki dosyaların proje dizininde olduğundan emin olun:
- `sampled_100.parquet` - ClinVar örnek verisi
- `Clingen-Gene-Disease-Summary-2025-07-01.csv` - ClinGen geçerlilik verileri

### 4. Google Gemini API Anahtarı Alın

1. [Google AI Studio](https://aistudio.google.com/) adresine gidin
2. Google hesabınızla giriş yapın
3. "Get API Key" butonuna tıklayın
4. API anahtarınızı kopyalayın

### 5. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde çalışacaktır.

## 📖 Kullanım

### Hızlı Başlangıç

1. **API Anahtarı Girişi**
   ```
   Uygulama açıldıktan sonra Google Gemini API anahtarınızı girin
   ```

2. **Dosya Yükleme**
   ```
   VCF, VCF.GZ veya CSV formatında varyant dosyanızı yükleyin
   ```

3. **Analiz Başlatma**
   ```
   "Gemini ile Yorumla" butonuna tıklayın
   ```

4. **Sonuçları İnceleme**
   ```
   Sonuçlar, PDF Rapor ve İstatistikler sekmelerini kullanın
   ```

### Desteklenen Dosya Formatları

#### VCF Format
```vcf
##fileformat=VCFv4.2
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
1       14370   rs6054257 G      A       29      PASS    .
1       17330   .         T      A       3       q10     .
```

#### CSV Format
```csv
CHROM,POS,REF,ALT
1,14370,G,A
1,17330,T,A
2,234567,C,T
```

### Örnek Kullanım Senaryoları

#### 1. WGS/WES Varyantlarının Analizi
```bash
# VCF dosyasını filtreleyin (sadece coding region varyantları)
bcftools view -R coding_regions.bed input.vcf > filtered.vcf

# Uygulamaya yükleyin ve analiz edin
```

#### 2. Targeted Panel Sonuçları
```bash
# Panel sonuçlarını CSV formatına dönüştürün
# CHROM, POS, REF, ALT sütunlarının olduğundan emin olun
```

#### 3. Araştırma Varyantları
```bash
# Literatürden aldığınız varyantları CSV formatında hazırlayın
# Tek tek veya toplu analiz yapabilirsiniz
```

## 🗄️ Veri Kaynakları

### ClinVar
- **Kaynak**: NCBI ClinVar Database
- **İçerik**: 1+ milyon genetik varyant
- **Veriler**: Klinik önem (CLNSIG), Gen adı (GENE), Hastalık (DISEASE)
- **Güncelleme**: Aylık

### ClinGen
- **Kaynak**: Clinical Genome Resource
- **İçerik**: Gen-hastalık ilişki geçerlilikleri
- **Sınıflandırmalar**: Definitive, Strong, Moderate, Limited, No Evidence
- **Güncelleme**: Üç aylık

### gnomAD
- **Kaynak**: Genome Aggregation Database
- **İçerik**: 141,456 kişinin genom verisi
- **Veriler**: Allel frekansları, popülasyon dağılımları
- **Versiyonlar**: r2.1 (GRCh37), r4 (GRCh38)

### PubMed
- **Kaynak**: NCBI PubMed Database
- **İçerik**: 35+ milyon biyomedikal makale
- **Erişim**: E-utilities API üzerinden

## 🔌 API Entegrasyonları

### Google Gemini AI
```python
# Örnek kullanım
prompt = f"""
You are a clinical geneticist. Based on the following variant data:
- Variant: {chrom}:{pos} {ref}→{alt}
- ClinVar: {clnsig}, {gene}, {disease}
- gnomAD AF: {af}

Provide clinical interpretation...
"""
response = generate_with_gemini(prompt, api_key)
```

### gnomAD GraphQL
```python
# Örnek sorgu
query = """
query ($variantId: String!) {
  variant(variantId: $variantId, dataset: gnomad_r4) {
    exome { ac an }
    genome { ac an }
  }
}
"""
```

### NCBI E-utilities
```python
# PubMed bağlantıları
pmids = get_pubmed_ids_from_clinvar(variation_id)
links = build_pubmed_links(pmids)
```

## 📁 Dosya Yapısı

```
genetic-variant-interpreter/
├── app.py                     # Ana Streamlit uygulaması
├── clinvar_parser.py          # ClinVar veri işleme modülü
├── gemini_handler.py          # Google Gemini AI entegrasyonu
├── gnomad_handler.py          # gnomAD API bağlantısı (opsiyonel)
├── pubmed_handler.py          # PubMed veri çekme modülü
├── clingen_handler.py         # ClinGen veri işleme modülü
├── pdf_report_generator.py    # PDF rapor oluşturma modülü
├── docs.py                    # Dokümantasyon sayfası
├── requirements.txt           # Python bağımlılıkları
├── README.md                  # Bu dosya
├── LICENSE                    # Lisans dosyası
├── sampled_100.parquet       # ClinVar örnek verisi
├── Clingen-Gene-Disease-Summary-2025-07-01.csv  # ClinGen verisi
└── assets/                    # Görsel ve dokümantasyon dosyaları
    ├── screenshots/
    └── examples/
```

### Ana Modüller

#### `app.py`
- Streamlit arayüzü
- Session state yönetimi
- Ana analiz döngüsü
- Tab-based görüntüleme

#### `clinvar_parser.py`
- INFO string parsing
- Varyant eşleştirme
- gnomAD link oluşturma
- GraphQL sorguları

#### `gemini_handler.py`
- Google Generative AI entegrasyonu
- Prompt engineering
- Rate limiting
- Error handling

#### `pdf_report_generator.py`
- ReportLab tabanlı PDF oluşturma
- Grafik entegrasyonu
- Hasta bilgisi yönetimi
- Template sistemi

## 🛠️ Geliştirici Rehberi

### Yeni Veri Kaynağı Ekleme

```python
# Yeni handler dosyası oluşturun
# örnek: mydb_handler.py

def fetch_mydb_data(chrom, pos, ref, alt):
    """Yeni veritabanından veri çekin"""
    # API çağrısı
    # Veri işleme
    return result

# app.py'a entegre edin
from mydb_handler import fetch_mydb_data

# Ana döngüde kullanın
mydb_data = fetch_mydb_data(row['CHROM'], row['POS'], 
                           row['REF'], row['ALT'])
```

### Özel Prompt Template

```python
# gemini_handler.py içinde
def create_custom_prompt(variant_data, clinical_context="general"):
    """Özel klinik bağlam için prompt oluşturun"""
    
    if clinical_context == "oncology":
        prompt = f"""
        Oncology-focused interpretation for:
        {variant_data}
        
        Focus on:
        1. Cancer predisposition
        2. Therapeutic implications
        3. Prognostic value
        """
    
    return prompt
```

### Cache Optimizasyonu

```python
# Büyük veri setleri için cache ayarları
@st.cache_data(
    ttl=24*3600,  # 24 saat cache
    max_entries=1000,  # Maksimum entry sayısı
    show_spinner=False
)
def expensive_api_call(params):
    return api_response
```

## 🧪 Test Verisi

### Örnek VCF Dosyası
```bash
# Test için kullanabileceğiniz örnek varyantlar
wget https://github.com/yourusername/genetic-variant-interpreter/raw/main/examples/test_variants.vcf
```

### Bilinen Patojenik Varyantlar
```csv
CHROM,POS,REF,ALT,EXPECTED_RESULT
17,43094077,G,A,Pathogenic
13,32315474,G,T,Pathogenic
7,117199644,G,A,Likely_Pathogenic
```

## 🔒 Güvenlik ve Gizlilik

- **API Anahtarları**: Session state'de saklanır, kalıcı depolama yapılmaz
- **Hasta Verileri**: Sadece analiz süresince bellekte tutulur
- **Dış API'lar**: Hasta isimleri harici servislere gönderilmez
- **GDPR Uyumlu**: Kişisel veri işleme politikaları

## 📊 Performans Metrikleri

- **Dosya Boyutu**: Maksimum 200MB VCF dosyası
- **Varyant Sayısı**: Optimum 100-200 varyant/analiz
- **API Limitleri**: Gemini ücretsiz plan - 60 istek/gün
- **Bellek Kullanımı**: ~500MB typical, 2GB maksimum

## 🐛 Bilinen Sorunlar ve Çözümler

### 1. API Rate Limiting
```python
# Çözüm: Exponential backoff
import time
import random

def api_call_with_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = (2 ** i) + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

### 2. Büyük Dosya İşleme
```python
# Çözüm: Chunk-based processing
def process_large_vcf(df, chunk_size=50):
    results = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk_results = process_chunk(chunk)
        results.extend(chunk_results)
    return results
```

### 3. Memory Optimization
```python
# Çözüm: Lazy loading ve cleanup
import gc

def cleanup_memory():
    gc.collect()
    
# Büyük DataFrame'leri del ile temizleyin
del large_dataframe
cleanup_memory()
```

## 🔄 Güncellemeler ve Roadmap

### v2.0.0 (Planlanan)
- [ ] Multi-threading desteği
- [ ] Database backend entegrasyonu
- [ ] REST API endpoint'leri
- [ ] Kullanıcı authentication sistemi
- [ ] Batch processing yetenekleri

### v1.5.0 (Gelecek)
- [ ] HGVS notasyon desteği
- [ ] PolyPhen/SIFT score entegrasyonu
- [ ] Custom annotation pipeline
- [ ] Excel export seçenekleri

### v1.1.0 (Mevcut)
- [x] PDF rapor sistemi
- [x] Multiple veri kaynağı entegrasyonu
- [x] AI-powered yorumlama
- [x] İnteraktif görselleştirme

## 🤝 Katkıda Bulunma

### Kod Katkısı
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

### Bug Raporu
- Issue açarken template kullanın
- Reproduce adımlarını detaylandırın
- Environment bilgilerini ekleyin
- Ekran görüntüleri ekleyin

### Özellik İsteği
- Use case'i açıklayın
- Mevcut alternatifler varsa belirtin
- Teknik gereksinimleri listeleyin

## 📞 Destek ve İletişim

- **Email**: enesozyaramiss@gmail.com
- **GitHub Issues**: [Issues sayfası](https://github.com/enesozyaramiss/genetik-app/issues)
- **Dokümantasyon**: Uygulama içi "Dokümantasyon" sekmesi

## 📜 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

Bu proje aşağıdaki açık kaynak projeler ve veritabanları sayesinde mümkün olmuştur:

- **Streamlit** - Web framework
- **Google Generative AI** - AI yorumlama
- **ClinVar** - Genetik varyant veritabanı
- **ClinGen** - Klinik genom kaynağı
- **gnomAD** - Popülasyon genomik verisi
- **NCBI** - Biyoinformatik araçları
- **ReportLab** - PDF oluşturma

---

**⚠️ Önemli Uyarı**: Bu uygulama bilgi amaçlıdır ve kesin tıbbi tanı koymaz. Klinik kararlar için mutlaka uzman hekim görüşü alınmalıdır.

*Son güncelleme: Temmuz 2025*