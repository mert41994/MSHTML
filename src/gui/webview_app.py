# src/gui/webview_app.py

import os
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl, pyqtSlot

class WebViewApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python PyQt6 WebView Uygulaması")
        self.setGeometry(100, 100, 1024, 768)

        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.webview = QWebEngineView()
        self.main_layout.addWidget(self.webview)

        # !!! İŞTE BURAYI DEĞİŞTİRECEKSİNİZ !!!
        # İnternet sitesini açmak için:
        self.webview.setUrl(QUrl("https://www.google.com")) # <-- İstediğiniz web sitesinin URL'sini buraya yazın

        # Eğer hala yerel dosyaları da yükleme seçenekleriniz olsun isterseniz,
        # bu satırları yorum satırı yapabilir veya silebilirsiniz:
        # self.page2_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'page2.html'))
        # self.index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'index.html'))
        # self.webview.setUrl(QUrl.fromLocalFile(self.index_path)) # Başlangıç sayfasını yerel dosya olarak yükle

        # --- Sayfa değiştirme düğmelerini (isteğe bağlı olarak) koruyabilirsiniz ---
        # Eğer bu düğmeler artık web sitesi geçişi yapmayacaksa, bunları kaldırmayı düşünebilirsiniz.
        self.button_layout = QVBoxLayout()
        self.change_page_button = QPushButton("Sayfayı Değiştir (Örnek URL)")
        # load_page2() veya load_index_page() yerine yeni bir method tanımlayabilir veya doğrudan URL verebilirsiniz.
        self.change_page_button.clicked.connect(lambda: self.webview.setUrl(QUrl("https://www.youtube.com")))
        self.button_layout.addWidget(self.change_page_button)

        self.go_back_button = QPushButton("Google'a Geri Dön")
        self.go_back_button.clicked.connect(lambda: self.webview.setUrl(QUrl("https://www.google.com")))
        self.button_layout.addWidget(self.go_back_button)

        self.main_layout.addLayout(self.button_layout)

        # QWebChannel'ı sayfa yüklendikten sonra başlatmak için loadFinished sinyaline bağlanıyoruz.
        # Bu kısım, JavaScript ile Python arasında iletişim kuracaksanız önemlidir.
        # Eğer sadece bir web sitesi gösterecekseniz ve iletişim kurmayacaksanız,
        # bu kısım gereksiz hale gelebilir ancak bırakmanız genellikle sorun yaratmaz.
        self.webview.page().loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok):
        # Eğer sadece bir web sitesi gösteriyorsanız ve JavaScript ile iletişim kurmayacaksanız,
        # buradaki QWebChannel kaydı mantıksal olarak gereksizdir.
        # Ancak hataya neden olmaz, bırakabilirsiniz.
        if ok:
            print(f"Web sayfası başarıyla yüklendi: {self.webview.url().toString()}")
            self.channel = self.webview.page().webChannel()
            if self.channel:
                self.channel.registerObject("py_obj", self)
                print("Python objesi 'py_obj' QWebChannel'a kaydedildi.")
            else:
                print("Hata: QWebChannel nesnesi alınamadı.")
        else:
            print(f"Hata: Web sayfası yüklenemedi: {self.webview.url().toString()}")

    # Eğer JavaScript ile Python arasında iletişim kuracaksanız bu metotları tutun,
    # aksi takdirde kaldırabilirsiniz.
    @pyqtSlot(str)
    def handle_js_message(self, message):
        print(f"JavaScript'ten gelen mesaj: {message}")
        # Bu metot, web sitesinde bu JavaScript kodunu çalıştırmak için bir Python objesi gerektirir.
        # Eğer açtığınız web sitesi (örneğin google.com) özel JavaScript içermiyorsa, bu çalışmaz.
        self.webview.page().runJavaScript(f"alert('Python\'dan yanıt: {message.upper()}');")

    @pyqtSlot(str, result=str)
    def get_data_from_python(self, query):
        print(f"JavaScript'ten veri isteği: {query}")
        if query == "app_version":
            return "1.0.0"
        return "Bilinmeyen veri isteği"