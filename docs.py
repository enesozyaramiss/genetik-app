import streamlit as st


def show_documentation():
    """
    Uygulama içinde dokümantasyon sayfasını gösterir.
    """
    # Başlık ve Giriş
    st.title("🧬 Genetik Varyant Yorumlama Uygulaması — Kullanım Kılavuzu")
    st.markdown(
        """
        Bu kılavuz, genetik varyant yorumlama uygulamasının her adımda neler yaptığını, hangi bilgileri topladığını ve sonuçları nasıl sunduğunu herkesin anlayacağı bir dille anlatır.
        Uygulamayı başlatır başlamaz önce OpenAI (Gemini) API anahtarınızı girmeniz gerekmektedir. Bu adımı tamamlamadan dosya yükleme ve yorumlama işlemlerine devam edemezsiniz.
        """
    )

    # 1. OpenAI (Gemini) API Anahtarı Girme
    st.header("1. OpenAI (Gemini) API Anahtarı Girme")
    st.markdown(
        """
        Uygulamayı kullanmadan önce, dil modeli tabanlı yorumlama işlevini aktif hale getirmek için API anahtarınızı girin:

        1. Google Cloud hesabınıza giriş yapın veya yeni bir hesap oluşturun.
        2. [Google Cloud Console](https://console.cloud.google.com/) sayfasına gidin.
        3. Sol menüden **API’ler ve Hizmetler** > **Kimlik Bilgileri** bölümüne tıklayın.
        4. **Kimlik Bilgileri Oluştur** > **API Anahtarı** adımlarını izleyin.
        5. Oluşturduğunuz anahtarı kopyalayın.
        6. Uygulamaya döndüğünüzde yan menüdeki "Gemini API Key’iniz" alanına yapıştırın.

        Bu işlemi tamamlayınca "Yorumlama Yap" düğmesi etkinleşir.
        """
    )

    # 2. Dosya Hazırlığı ve Yükleme
    st.header("2. Dosya Hazırlığı ve Yükleme")
    st.markdown(
        """
        Uygulamayı kullanmak için bilgisayarınızda aşağıdaki formatlardan birinde bir dosya olmalı:
        
        - **VCF (.vcf)**: Genetik değişiklikleri listeleyen yaygın format.
        - **Sıkıştırılmış VCF (.vcf.gz)**: VCF dosyasının sıkıştırılmış hali.
        - **CSV (.csv)**: Excel tarzı tablo, içinde bu sütunlar bulunmalı:
          - **CHROM** (Kromozom numarası)
          - **POS** (Genetik konum)
          - **REF** (Referans harf)
          - **ALT** (Alternatif harf)
        
        **Yükleme adımları:**
        1. Yan menüde API anahtarınızı girdikten sonra kısımdaki "Dosya Yükle" butonuna tıklayın.
        2. Bilgisayarınızdan dosyayı seçin.
        3. Yükleme tamamlandığında dosya adı ekranda belirecektir.
        """
    )

    # 3. Değişkenlerin Anlamı
    st.header("3. Değişkenlerin Anlamı")
    st.markdown(
        """
        Yüklenen dosyada geçen başlıca terimler:

        - **Kromozom (CHROM):** DNA segmenti numarası (1–22, X veya Y).
        - **Pozisyon (POS):** Kromozom üzerindeki nokta.
        - **Referans Allel (REF):** Beklenen gen harfi.
        - **Alternatif Allel (ALT):** Varyasyon gösteren harf.
        """
    )

    # 4. ClinVar’dan Klinik Durum Bilgisi
    st.header("4. ClinVar’dan Klinik Durum Bilgisi")
    st.markdown(
        """
        Uygulama, ClinVar adı verilen halka açık veri kaynağından şu bilgileri çeker:

        - **Klinik Önemi:** Varyantın hastalıkla ilişkisi (örn. Patogenik, Benign).
        - **İnceleme Durumu:** Uzman onay düzeyi.

        Ekranda şöyle bir açıklama görürsünüz:
        > "Bu varyant patojenik olarak sınıflandırılmış, uzman incelemesi güçlüdür."
        """
    )

    # 5. ClinGen’den Geçerlilik Seviyesi
    st.header("5. ClinGen’den Geçerlilik Seviyesi")
    st.markdown(
        """
        ClinGen kaynağından, varyantın genetik toplulukta ne kadar iyi anlaşıldığını gösteren:

        - **Sınıflandırma:** "Kesin", "Muhtemel" gibi ifadeler.

        Böylece hangi sonuçların daha güvenilir olduğunu kolayca anlarsınız.
        """
    )

    # 6. gnomAD’dan Popülasyon Frekansları
    st.header("6. gnomAD’dan Popülasyon Frekansları")
    st.markdown(
        """
        gnomAD veritabanından alınan:

        - **Genel Frekans:** Tüm popülasyondaki oran.
        - **En Yüksek Frekans:** Varyantın en sık görüldüğü grubun oranı.

        Böylece varyantın yaygın mı yoksa nadir mi olduğunu görürsünüz.
        """
    )

    # 7. PubMed’den Literatür Bağlantıları
    st.header("7. PubMed’den Literatür Bağlantıları")
    st.markdown(
        """
        İlgili bilimsel makalelere hızlı erişim için pubmed.gov linkleri:

        - Makale başlıklarına tıklayarak ayrıntıya gidin.
        - Konuyla ilgili derin okumalar yapabilirsiniz.
        """
    )

    # 8. Google Gemini ile Özetleyici Yorumlar
    st.header("8. Google Gemini ile Özetleyici Yorumlar")
    st.markdown(
        """
        Tüm topladığımız verileri bir araya getirip dil modeliyle her varyant için:

        - **Patogenite Olasılığı**
        - **Hastalık İlişkisi**
        - **Klinik Öneriler**

        Bu özetler, tıbbi arka planı olmayan kişiler için bile anlaşılır bir dille hazırlanır.
        """
    )

    # 9. Sonuçların Görünümü ve İndirme
    st.header("9. Sonuçların Görünümü ve İndirme")
    st.markdown(
        """
        - Sonuçlar interaktif bir tabloyla gösterilir.
        - Tablo başlıkları tıklanarak sıralama yapılabilir.
        - "Detay" düğmesiyle tam açıklamaları inceleyin.
        - "CSV Olarak İndir" ile tüm verileri kaydedin.
        """
    )

    # 10. Destek ve İletişim
    st.header("10. Destek ve İletişim")
    st.markdown(
        """
        Sorunuz veya öneriniz mi var? Biz buradayız:

        - **E-posta:** enesozyaramiss@gmail.com
        """
    )

    # Sayfa sonu
    st.stop()