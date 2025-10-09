# 🔁 Keyword Rotasyonu - Linkli Excel Web Uygulaması

Bu uygulama, yüklediğiniz keyword Excel dosyasını okuyup her marketplace ve class için
4'lü keyword rotasyonu oluşturur. Sonuç olarak tıklanabilir linklerle Excel çıktısı verir.

## 🚀 Kullanım

1. Bu klasörü GitHub’a yükleyin (örnek: `keyword-rotation-web`).
2. [https://streamlit.io/cloud](https://streamlit.io/cloud) adresine gidin.
3. "Deploy an app" → GitHub hesabınızı bağlayın.
4. `app.py` dosyasını seçin ve Deploy’a tıklayın.
5. Uygulamanız 1-2 dakika içinde yayınlanacak:  
   örnek: `https://kubra-keyword-rotation.streamlit.app`

### 💡 Alternatif: Hugging Face Spaces
- [https://huggingface.co/spaces](https://huggingface.co/spaces)’te yeni bir Space oluşturun.
- Framework olarak **Streamlit** seçin.
- Bu dosyaları yükleyin.
- Uygulama otomatik olarak yayına alınacaktır.

## 📦 Gerekli Excel Formatı
Excel dosyanızda şu sütunlar bulunmalıdır:

| Marketplace | Class | Keywords |
|--------------|--------|----------|
| DE           | Class1 | keyword1, keyword2, keyword3, ... |

Uygulama her seferinde 4’erli gruplar halinde linkli Excel çıktısı oluşturur.
