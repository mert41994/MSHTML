# src/main.py

import webview
import os

# threading ve time modülleri bu senaryoda doğrudan kullanılmadığı için kaldırılabilir,
# ancak hata ayıklama kolaylığı için veya gelecekteki olası kullanımlar için tutulabilir.
# import threading
# import time

# assets klasörünün tam yolunu hesaplıyoruz.
# Bu yollar, eğer JavaScript üzerinden yerel HTML sayfalarına geçiş yapmayı planlıyorsanız gereklidir.
ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))

# HTML dosyalarının tam yollarını oluşturuyoruz.
INDEX_HTML_PATH = os.path.join(ASSETS_DIR, 'index.html')
PAGE2_HTML_PATH = os.path.join(ASSETS_DIR, 'page2.html')

# --- DEBUG BİLGİSİ BAŞLANGICI ---
# Bu kısımlar, dosya yollarının doğru hesaplanıp hesaplanmadığını kontrol etmenize yardımcı olur.
# Uygulamanız sorunsuz çalıştığında bu satırları silebilir veya yorum satırı yapabilirsiniz.
print("\n--- DEBUG BİLGİSİ BAŞLANGICI ---")
print(f"__file__ (main.py'nin konumu): {__file__}")
print(f"os.path.dirname(__file__): {os.path.dirname(__file__)}")
print(f"ASSETS_DIR (Hesaplanan assets klasörü yolu): {ASSETS_DIR}")
print(f"INDEX_HTML_PATH (Hesaplanan index.html yolu): {INDEX_HTML_PATH}")
print(f"PAGE2_HTML_PATH (Hesaplanan page2.html yolu): {PAGE2_HTML_PATH}")
print(f"os.path.exists(ASSETS_DIR)? (assets klasörü var mı?): {os.path.exists(ASSETS_DIR)}")
print(f"os.path.exists(INDEX_HTML_PATH)? (index.html dosyası var mı?): {os.path.exists(INDEX_HTML_PATH)}")
print(f"os.path.exists(PAGE2_HTML_PATH)? (page2.html dosyası var mı?): {os.path.exists(PAGE2_HTML_PATH)}")
print("--- DEBUG BİLGİSİ SONU ---\n")


# --- DEBUG BİLGİSİ SONU ---

class Api:
    """
    JavaScript'ten çağrılabilecek Python API'si.
    Bu sınıfın metotları, webview içindeki JavaScript tarafından erişilebilir olacaktır.
    """

    def __init__(self, window_instance):
        self.window = window_instance

    def handle_js_message(self, message):
        """
        JavaScript'ten gelen mesajları işler.
        Bu metot, `pywebview.api.handle_js_message('mesaj')` şeklinde JS'den çağrılabilir.
        """
        print(f"JavaScript'ten gelen mesaj: {message}")
        # Not: Eğer açtığınız web sitesi (örneğin google.com) bu JS fonksiyonunu içermiyorsa,
        # bu `evaluate_js` çağrısı bir etki yaratmaz.
        self.window.evaluate_js(f"console.log('Python\'dan yanıt: {message.upper()}');")
        return "Mesaj alındı!"

    def get_data_from_python(self, query):
        """
        JavaScript'ten veri isteğini işler ve bir string döndürür.
        Bu metot, `pywebview.api.get_data_from_python('veri isteği').then(...)` şeklinde JS'den çağrılabilir.
        """
        print(f"JavaScript'ten veri isteği: {query}")
        if query == "app_version":
            return "IE WebView App v1.0"
        return f"Bilinmeyen veri isteği: {query}"

    def change_page(self, page_name):
        """
        JavaScript'ten gelen sayfa adı isteğine göre webview sayfasını değiştirir.
        Hem yerel HTML dosyalarını hem de harici URL'leri destekler.
        """
        print(f"JavaScript'ten sayfa değiştirme isteği: {page_name}")

        target_url = None
        if page_name == "index.html":
            # Yerel bir dosyayı yüklerken 'file://' önekini kullanmak önemlidir.
            # assets klasörünün gerçekten var ve içinde index.html olduğunu varsayar.
            if os.path.exists(INDEX_HTML_PATH):
                target_url = f'file://{INDEX_HTML_PATH}'
            else:
                print(f"Hata: Yerel dosya bulunamadı: {INDEX_HTML_PATH}")
                return "Yerel dosya bulunamadı."
        elif page_name == "page2.html":
            # assets klasörünün gerçekten var ve içinde page2.html olduğunu varsayar.
            if os.path.exists(PAGE2_HTML_PATH):
                target_url = f'file://{PAGE2_HTML_PATH}'
            else:
                print(f"Hata: Yerel dosya bulunamadı: {PAGE2_HTML_PATH}")
                return "Yerel dosya bulunamadı."
        elif page_name.startswith(('http://', 'https://')):
            # Harici bir URL ise doğrudan kullanırız.
            target_url = page_name
        else:
            print(f"Geçersiz veya bilinmeyen sayfa adı: {page_name}")
            return "Geçersiz sayfa"

        if target_url:
            self.window.load_url(target_url)  # webview penceresinin URL'sini değiştirir.
            return "Sayfa değiştirildi."
        return "Sayfa değiştirme başarısız."


def run_webview_app():
    """
    Pywebview uygulamasını başlatır ve Internet Explorer (MSHTML) motorunu kullanır.
    """
    # webview.create_window ile yeni bir pencere oluşturulur.
    # Ana sayfa olarak doğrudan Google'ı yüklüyoruz.
    window = webview.create_window(
        title="OnePowership Uygulaması",  # Pencere başlığı güncellendi
        url="http://192.168.3.215/parcmenu",  # <--- BURASI DEĞİŞTİ: Direkt Google yüklüyoruz!
        width=1024,  # Pencere genişliği
        height=768,  # Pencere yüksekliği
        fullscreen=False,  # Tam ekran olmasın
        resizable=True,  # Yeniden boyutlandırılabilir olsun
        min_size=(600, 400)  # Minimum pencere boyutu
    )

    # JavaScript'ten Python'a iletişim için API sınıfının bir örneğini oluşturup pywebview'a tanıtıyoruz.
    api = Api(window)
    # Api sınıfının her bir metodunu tek tek expose ediyoruz.
    window.expose(api.handle_js_message, api.get_data_from_python, api.change_page)

    # Pywebview uygulamasını başlat.
    # debug=True: Hata ayıklama çıktısını konsola yazdırır.
    # http_server=True: Yerel dosyaları bir dahili web sunucusu üzerinden servis eder (hala gerekebilir
    #                   eğer JavaScript üzerinden yerel HTML'lere geçiş yapacaksanız).
    # gui='mshtml': GUI arka ucunu burada belirtiyoruz!
    webview.start(debug=True, http_server=True, gui='mshtml')


if __name__ == "__main__":
    # Eğer doğrudan harici bir URL yüklüyorsanız, dosya kontrolüne gerek yoktur.
    # Ancak, debug çıktıları için yine de varlık kontrolünü tutmak faydalıdır.
    run_webview_app()
    print("Uygulama kapandı.")