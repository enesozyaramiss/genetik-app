import streamlit as st


def show_documentation():
    """
    Uygulama içinde kapsamlı dokümantasyon sayfasını gösterir.
    """
    # Ana Başlık
    st.title("🧬 Genetik Varyant Yorumlama Uygulaması — Detaylı Kullanım Kılavuzu")
    
    # İçindekiler
    with st.expander("📚 İçindekiler", expanded=True):
        st.markdown("""
        1. [Genel Bakış](#genel-bakis)
        2. [Başlangıç](#baslangic)
        3. [API Anahtarı Alma ve Kullanma](#api-anahtari)
        4. [Dosya Hazırlığı ve Formatları](#dosya-hazirlik)
        5. [Analiz Süreci](#analiz-sureci)
        6. [Veri Kaynakları](#veri-kaynaklari)
        7. [Sonuçların Yorumlanması](#sonuclarin-yorumlanmasi)
        8. [PDF Rapor Oluşturma](#pdf-rapor)
        9. [İstatistikler ve Grafikler](#istatistikler)
        10. [Hata Çözümleri](#hata-cozumleri)
        11. [Sıkça Sorulan Sorular](#sss)
        12. [Teknik Detaylar (Geliştiriciler İçin)](#teknik-detaylar)
        """)

    # 1. Genel Bakış
    st.header("1. 🌟 Genel Bakış", anchor="genel-bakis")
    st.markdown("""
    Bu uygulama, genetik varyantlarınızı (DNA'daki değişiklikleri) analiz ederek:
    
    - **ClinVar** veritabanından klinik önem bilgilerini
    - **ClinGen** veritabanından gen-hastalık ilişkilerini
    - **gnomAD** veritabanından popülasyon frekanslarını
    - **PubMed** veritabanından ilgili bilimsel makaleleri
    - **Google Gemini AI** ile kapsamlı klinik yorumları
    
    bir araya getirerek size detaylı bir rapor sunar.
    
    ### 🎯 Kimler İçin?
    - Genetik uzmanları ve doktorlar
    - Araştırmacılar
    - Biyoinformatik uzmanları
    - Genetik test sonuçlarını anlamak isteyen bireyler
    
    ### ⚡ Temel Özellikler
    - VCF/CSV formatında varyant dosyası yükleme
    - Otomatik veritabanı eşleştirme
    - AI destekli klinik yorumlama
    - Profesyonel PDF rapor oluşturma
    - İnteraktif sonuç görüntüleme
    """)

    # 2. Başlangıç
    st.header("2. 🚀 Başlangıç", anchor="baslangic")
    st.markdown("""
    ### Gereksinimler
    - Güncel bir web tarayıcı (Chrome, Firefox, Safari, Edge)
    - İnternet bağlantısı
    - Google Gemini API anahtarı (ücretsiz alınabilir)
    
    ### Kullanıma Başlama
    
    1. **Web uygulamasına erişin**
       - Uygulama linki size sağlanacaktır
       - Tarayıcınızda açmanız yeterlidir
    
    2. **API anahtarınızı hazırlayın**
       - Google AI Studio'dan ücretsiz alabilirsiniz
       - Detaylar bir sonraki bölümde
    
    3. **Varyant dosyanızı hazırlayın**
       - VCF, VCF.GZ veya CSV formatında
       - Detaylar "Dosya Hazırlığı" bölümünde
    
    ### ⚡ Hızlı Başlangıç
    1. Uygulamayı açın
    2. API anahtarınızı girin
    3. Dosyanızı yükleyin
    4. "Yorumla" butonuna tıklayın
    5. Sonuçları inceleyin ve PDF raporu indirin
    
    💡 **Not:** Kurulum gerektirmez, tamamen web tabanlıdır!
    """)

    # 3. API Anahtarı
    st.header("3. 🔑 API Anahtarı Alma ve Kullanma", anchor="api-anahtari")
    st.markdown("""
    ### Google Gemini API Anahtarı Alma
    
    1. **Google AI Studio'ya gidin:** [https://aistudio.google.com/](https://aistudio.google.com/)
    
    2. **Google hesabınızla giriş yapın**
    
    3. **"Get API Key" butonuna tıklayın**
    
    4. **Yeni bir proje oluşturun veya mevcut projeyi seçin**
    
    5. **API anahtarınızı kopyalayın**
    
    ### Uygulamada Kullanma
    
    1. Sol menüdeki **"Uygulama"** sekmesinde olduğunuzdan emin olun
    
    2. **"Gemini API Key'iniz"** alanına anahtarınızı yapıştırın
    
    3. Anahtar doğrulandıktan sonra dosya yükleme alanı aktif olacak
    
    ⚠️ **Güvenlik Notu:** API anahtarınızı kimseyle paylaşmayın. Ücretsiz plan günlük 60 istek hakkı verir.
    """)

    # 4. Dosya Hazırlığı
    st.header("4. 📁 Dosya Hazırlığı ve Formatları", anchor="dosya-hazirlik")
    st.markdown("""
    ### Desteklenen Formatlar
    
    #### 1. VCF Format (.vcf veya .vcf.gz)
    ```
    ##fileformat=VCFv4.2
    #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
    1       14370   rs6054257 G      A       29      PASS    .
    1       17330   .         T      A       3       q10     .
    ```
    
    #### 2. CSV Format (.csv)
    En az şu 4 sütun olmalıdır:
    ```csv
    CHROM,POS,REF,ALT
    1,14370,G,A
    1,17330,T,A
    2,234567,C,T
    ```
    
    ### Örnek Veri Hazırlama
    
    **Excel'den CSV'ye dönüştürme:**
    1. Excel'de varyant verilerinizi hazırlayın
    2. Dosya → Farklı Kaydet → CSV UTF-8 seçin
    3. Sütun başlıklarının doğru olduğundan emin olun
    
    **VCF dosyası sıkıştırma:**
    ```bash
    gzip varyantlar.vcf
    # varyantlar.vcf.gz oluşacak
    ```
    
    ### ⚠️ Önemli Notlar
    - Kromozom değerleri: 1-22, X, Y veya chr1-chr22, chrX, chrY
    - Pozisyon değerleri sayısal olmalı
    - REF ve ALT değerleri A, C, G, T harflerinden oluşmalı
    - Maksimum dosya boyutu: 200MB
    """)

    # 5. Analiz Süreci
    st.header("5. 🔬 Analiz Süreci", anchor="analiz-sureci")
    st.markdown("""
    ### Adım Adım Analiz
    
    #### 1️⃣ Dosya Yükleme
    - "Dosya yükle" butonuna tıklayın
    - VCF, VCF.GZ veya CSV dosyanızı seçin
    - Dosya otomatik olarak okunup doğrulanacak
    
    #### 2️⃣ Varyant Eşleştirme
    Sistem şu işlemleri yapar:
    - Yüklenen varyantları ClinVar veritabanıyla karşılaştırır
    - CHROM, POS, REF, ALT değerlerini eşleştirir
    - Eşleşen varyantlar için klinik bilgileri getirir
    
    #### 3️⃣ Veri Zenginleştirme
    Her eşleşen varyant için:
    - **ClinVar'dan:** Klinik önem, hastalık ilişkisi, gen adı
    - **ClinGen'den:** Gen-hastalık geçerlilik sınıflandırması
    - **gnomAD'dan:** Popülasyon frekansları, allel sayıları
    - **PubMed'den:** İlgili bilimsel makale bağlantıları
    
    #### 4️⃣ AI Yorumlama
    Google Gemini her varyant için:
    1. Patojenik olma olasılığını değerlendirir
    2. Bilinen hastalık ilişkilerini açıklar
    3. Klinik önemini yorumlar
    4. Anlaşılır bir özet sunar
    
    #### 5️⃣ Sonuç Gösterimi
    - İnteraktif tablo
    - Sıralanabilir sütunlar
    - Detaylı bilgi görüntüleme
    - CSV/PDF dışa aktarma
    """)

    # 6. Veri Kaynakları
    st.header("6. 📊 Veri Kaynakları", anchor="veri-kaynaklari")
    st.markdown("""
    ### ClinVar
    - **Ne:** NCBI'nin genetik varyant veritabanı
    - **İçerik:** 1+ milyon varyant, klinik önem bilgileri
    - **Güncelleme:** Aylık
    
    #### Alınan Bilgiler:
    - `CLNSIG`: Klinik önem (Pathogenic, Benign, vb.)
    - `GENE`: İlgili gen adı
    - `DISEASE`: İlişkili hastalıklar
    - `CLNREVSTAT`: İnceleme durumu
    
    ### ClinGen
    - **Ne:** Klinik genom kaynağı
    - **İçerik:** Gen-hastalık ilişki geçerlilikleri
    - **Sınıflandırmalar:** Definitive, Strong, Moderate, Limited, No Evidence
    
    ### gnomAD
    - **Ne:** Genom toplama veritabanı
    - **İçerik:** 141,456 kişinin genom verisi
    - **Veriler:**
      - Allel frekansları
      - Popülasyon dağılımları
      - Filtreleme durumları
    
    ### PubMed
    - **Ne:** Biyomedikal literatür veritabanı
    - **İçerik:** 35+ milyon makale
    - **Kullanım:** Varyantla ilgili yayınlara bağlantılar
    """)

    # 7. Sonuçların Yorumlanması
    st.header("7. 📈 Sonuçların Yorumlanması", anchor="sonuclarin-yorumlanmasi")
    st.markdown("""
    ### Klinik Önem Kategorileri
    
    #### 🔴 Pathogenic (Patojenik)
    - Hastalığa neden olduğu kanıtlanmış
    - Klinik takip gerektirir
    - Aile taraması önerilir
    
    #### 🟠 Likely Pathogenic (Muhtemel Patojenik)
    - %90+ olasılıkla hastalık nedeni
    - Patojenik gibi değerlendirilir
    
    #### 🟡 Uncertain Significance (Belirsiz Önem)
    - Yeterli kanıt yok
    - Takip ve yeniden değerlendirme gerekir
    
    #### 🟢 Likely Benign (Muhtemel İyi Huylu)
    - %90+ olasılıkla zararsız
    
    #### ⚪ Benign (İyi Huylu)
    - Hastalık riski yok
    - Normal varyasyon
    
    ### Popülasyon Frekansı Değerlendirmesi
    
    | Frekans | Yorum |
    |---------|--------|
    | < 0.0001 | Çok nadir |
    | 0.0001-0.001 | Nadir |
    | 0.001-0.01 | Az yaygın |
    | 0.01-0.05 | Yaygın |
    | > 0.05 | Çok yaygın |
    
    ### AI Yorumlarını Anlama
    
    Gemini yorumları 4 ana başlıkta toplanır:
    1. **Patojenik olasılık:** Hastalık yapma potansiyeli
    2. **Hastalık ilişkisi:** Bilinen hastalıklarla bağlantı
    3. **Klinik önem:** Tıbbi açıdan önemi
    4. **Özet:** Sade dilde açıklama
    """)

    # 8. PDF Rapor
    st.header("8. 📄 PDF Rapor Oluşturma", anchor="pdf-rapor")
    st.markdown("""
    ### PDF Rapor İçeriği
    
    1. **Kapak Sayfası**
       - Başlık ve tarih
       - Hasta bilgileri
       - Özet istatistikler
    
    2. **Analiz Özeti**
       - Klinik önem dağılımı (pasta grafik)
       - Kromozom dağılımı (çubuk grafik)
       - Allel frekans histogramı
       - En sık görülen genler
    
    3. **Klinik Önem Analizi**
       - Yüksek risk varyantları
       - Düşük risk varyantları
       - Belirsiz varyantlar
    
    4. **Detaylı Varyant Listesi**
       - İlk 15-20 varyantın tablosu
       - Kromozom, pozisyon, genler
       - Klinik önem bilgileri
    
    5. **AI Yorumları**
       - Her varyant için detaylı açıklama
       - Klinik öneriler
                
    6. **Sonuç ve Öneriler**
       - Genel değerlendirme
       - Takip önerileri
    
    ### PDF Oluşturma Adımları
    
    1. Analiz tamamlandıktan sonra **"PDF Rapor"** sekmesine gidin
    2. Hasta bilgilerini doldurun:
       - Hasta ID (otomatik oluşturulur)
       - Hasta Adı
       - Yaş
       - Test Tarihi
    3. **"PDF Raporu Oluştur"** butonuna tıklayın
    4. Oluşan raporu **"PDF Raporu İndir"** ile kaydedin
    
    """)

    # 9. İstatistikler
    st.header("9. 📊 İstatistikler ve Grafikler", anchor="istatistikler")
    st.markdown("""
    ### Görüntülenen İstatistikler
    
    #### Özet Metrikler
    - **Toplam Varyant:** Analiz edilen varyant sayısı
    - **Pathogenic:** Hastalık yapan varyantlar
    - **Benign:** Zararsız varyantlar
    - **Uncertain:** Belirsiz varyantlar
    
    #### Grafikler
    
    1. **Klinik Önem Dağılımı**
       - Pasta grafik
       - Yüzdelik dağılım
       - Renk kodlu kategoriler
    
    2. **Kromozom Dağılımı**
       - Çubuk grafik
       - En çok varyant içeren kromozomlar
       - Sayısal dağılım
    
    3. **Allel Frekans Histogramı**
       - Nadir vs yaygın varyantlar
       - Popülasyon dağılımı
       - Log ölçekli görünüm
    
    4. **Gen Bazlı Dağılım**
       - En sık etkilenen genler
       - Varyant sayıları
       - Top 10 gen listesi
    """)

    # 10. Hata Çözümleri
    st.header("10. 🛠️ Hata Çözümleri", anchor="hata-cozumleri")
    st.markdown("""
    ### Sık Karşılaşılan Hatalar
    
    #### 1. "API anahtarı geçersiz"
    - **Sebep:** Yanlış veya eksik API anahtarı
    - **Çözüm:** Google AI Studio'dan yeni anahtar alın
    
    #### 2. "Dosya formatı desteklenmiyor"
    - **Sebep:** Yanlış dosya uzantısı veya format
    - **Çözüm:** VCF, VCF.GZ veya CSV formatında kaydedin
    
    #### 3. "Gerekli sütunlar eksik"
    - **Sebep:** CHROM, POS, REF, ALT sütunları yok
    - **Çözüm:** Dosyanızı kontrol edip eksik sütunları ekleyin
    
    #### 4. "Eşleşen varyant bulunamadı"
    - **Sebep:** Varyantlar ClinVar'da yok
    - **Çözüm:** 
      - Referans genom versiyonunu kontrol edin (GRCh37/38)
      - Kromozom formatını kontrol edin (1 vs chr1)
    
    #### 5. "gnomAD verisi alınamadı"
    - **Sebep:** API bağlantı hatası veya varyant yok
    - **Çözüm:** İnternet bağlantınızı kontrol edin
    
    #### 6. "PDF oluşturulamadı"
    - **Sebep:** Bellek yetersizliği veya çok fazla varyant
    - **Çözüm:** Daha az varyantla deneyin veya özet rapor seçin
    
    ### Performans İyileştirme
    
    - **Yavaş analiz:** Varyant sayısını azaltın (max 100-200)
    - **Bellek hatası:** Büyük dosyaları parçalara bölün
    - **API limiti:** Ücretsiz planda günlük 60 istek sınırı
    """)

    # 10. Teknik Detaylar (Geliştiriciler İçin)
    st.header("10. 🔧 Teknik Detaylar (Geliştiriciler İçin)", anchor="teknik-detaylar")
    st.markdown("""
    ### Sistem Mimarisi
    
    #### Ana Bileşenler
    1. **app.py** - Ana Streamlit uygulaması
    2. **clinvar_parser.py** - ClinVar veri işleme
    3. **gemini_handler.py** - Google Gemini AI entegrasyonu
    4. **gnomad_handler.py** - gnomAD API bağlantısı (GraphQL)
    5. **pubmed_handler.py** - PubMed veri çekme
    6. **clingen_handler.py** - ClinGen veri işleme
    7. **pdf_report_generator.py** - PDF rapor oluşturma
    8. **docs.py** - Bu dokümantasyon sayfası
    
    #### Veri Akışı
    ```
    Kullanıcı Dosyası → VCF/CSV Parser → ClinVar Eşleştirme
                                            ↓
    PDF Rapor ← AI Yorumlama ← Veri Zenginleştirme
                                    ↓
                            gnomAD + PubMed + ClinGen
    ```
    
    #### Kullanılan Teknolojiler
    - **Frontend:** Streamlit
    - **Veri İşleme:** Pandas, NumPy
    - **Görselleştirme:** Matplotlib
    - **PDF:** ReportLab
    - **AI:** Google Generative AI (Gemini 1.5 Flash)
    - **API'ler:** GraphQL (gnomAD), REST (NCBI E-utilities)
    
    #### Geliştirici Kurulumu
    Eğer kodu yerel olarak çalıştırmak isterseniz:
    ```bash
    # Gereksinimler
    pip install streamlit pandas numpy matplotlib reportlab 
    pip install google-generativeai requests streamlit-option-menu
    
    # Çalıştırma
    streamlit run app.py
    ```
    
    #### Veri Dosyaları
    - `sampled_100.parquet` - ClinVar örnek verisi
    - `Clingen-Gene-Disease-Summary-2025-07-01.csv` - ClinGen verisi
    
    #### Güvenlik Önlemleri
    - API anahtarları session state'de saklanır
    - Dosyalar geçici bellekte işlenir
    - SSL/TLS üzerinden API iletişimi
    - Hasta isimleri harici API'lere gönderilmez
    
    #### Cache Mekanizması
    - gnomAD ve PubMed sorguları 24 saat cache'lenir
    - Tekrarlayan sorgular için performans artışı sağlar
    """)

    # 11. Sıkça Sorulan Sorular
    st.header("11. ❓ Sıkça Sorulan Sorular", anchor="sss")
    st.markdown("""
    **S: Ücretsiz mi?**
    C: Uygulama ücretsizdir, ancak Google Gemini API'si için ücretsiz plan limitleri vardır (günlük 60 istek).
    
    **S: Kurulum gerekiyor mu?**
    C: Hayır! Tamamen web tabanlıdır. Sadece tarayıcınızdan erişip kullanabilirsiniz.
    
    **S: Hangi tarayıcıları destekliyor?**
    C: Chrome, Firefox, Safari, Edge gibi güncel tüm tarayıcılar desteklenir.
    
    **S: Hangi referans genom versiyonunu kullanıyor?**
    C: Varsayılan olarak GRCh38 (hg38) kullanılır.
    
    **S: Kaç varyant analiz edebilirim?**
    C: Teknik olarak sınır yok, ancak performans için 100-200 varyant önerilir.
    
    **S: Sonuçlar ne kadar güvenilir?**
    C: Sonuçlar güncel veritabanlarına dayanır ancak kesin tanı için değildir. Mutlaka uzman görüşü alın.
    
    **S: Verilerim güvende mi?**
    C: Veriler sadece analiz süresince bellekte tutulur. Hasta isimleri harici API'lere gönderilmez.
    
    **S: Hangi hastalıklar tespit edilebilir?**
    C: ClinVar'da kayıtlı tüm genetik hastalıklar. Özellikle tek gen hastalıkları.
    
    **S: WGS/WES verisi kullanabilir miyim?**
    C: Evet, ancak önce varyantları filtreleyip VCF/CSV formatına dönüştürmelisiniz.
    
    **S: Mobil cihazlardan kullanabilir miyim?**
    C: Evet, ancak büyük ekranlı cihazlarda (tablet, bilgisayar) daha iyi deneyim sunar.
    
    **S: Offline çalışır mı?**
    C: Hayır, veritabanı sorguları ve AI yorumları için internet gereklidir.
    """)

    # İletişim
    st.header("📧 İletişim ve Destek")
    st.markdown("""
    ### Geliştirici Bilgileri
    - **E-posta:** enesozyaramiss@gmail.com
    - **Proje Güncellemeleri:** GitHub üzerinden takip edilebilir
    
    ### Katkıda Bulunma
    - Hata bildirimleri için issue açın
    - Yeni özellik önerileri hoş karşılanır
    - Dokümantasyon iyileştirmeleri için PR gönderin
    
    ### Teşekkürler
    Bu uygulama açık kaynak topluluğu ve bilimsel veritabanları sayesinde mümkün olmuştur.
    
    ---
    *Son güncelleme: Temmuz 2025*
    """)

    # Sayfa sonu
    st.stop()