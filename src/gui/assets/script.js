// src/assets/script.js

document.addEventListener('DOMContentLoaded', () => {
    const sendMessageButton = document.getElementById('sendMessageButton');
    const requestDataButton = document.getElementById('requestDataButton');
    const goToGoogleButton = document.getElementById('goToGoogle');
    const goToSecondPageButton = document.getElementById('goToSecondPage');
    const messageResponseParagraph = document.getElementById('messageResponse');
    const dataResponseParagraph = document.getElementById('dataResponse');

    // Bu fonksiyon, Python'dan JS'e mesaj göndermek için pywebview.api.evaluate_js() içinde kullanılır.
    window.updateResponse = function(message) {
        messageResponseParagraph.textContent = message;
    };

    // pywebview API'si hazır olduğunda (window.pywebview.api erişilebilir olduğunda)
    // çağrılacak fonksiyon. IE motoru için bu durumun biraz daha gecikmeli olabileceğini unutmayın.
    function initPywebviewApi() {
        // pywebview.api, pywebview kütüphanesi tarafından otomatik olarak HTML'e enjekte edilen bir objedir.
        if (typeof pywebview !== 'undefined' && typeof pywebview.api !== 'undefined') {
            console.log("pywebview API'si başarıyla yüklendi.");
            // Python'dan ilk veri isteği
            pywebview.api.get_data_from_python("app_version").then(version => {
                dataResponseParagraph.textContent = `Uygulama Versiyonu: ${version}`;
            }).catch(error => {
                console.error("Uygulama versiyonu alınırken hata oluştu:", error);
                dataResponseParagraph.textContent = "Versiyon bilgisi alınamadı.";
            });
        } else {
            // Eğer API henüz hazır değilse, biraz bekleyip tekrar dene
            console.log("pywebview API'si bekleniyor...");
            setTimeout(initPywebviewApi, 100); // Küçük bir gecikme ile tekrar dene
        }
    }

    // API'yi başlat
    initPywebviewApi();


    // Python'a mesaj gönderme düğmesi olayı
    sendMessageButton.addEventListener('click', () => {
        if (typeof pywebview !== 'undefined' && typeof pywebview.api !== 'undefined') {
            const messageToSend = "Merhaba Python, ben JavaScript'ten geldim!";
            messageResponseParagraph.textContent = "Python'a mesaj gönderiliyor...";
            // pywebview.api.handle_js_message, Python'daki Api sınıfındaki handle_js_message metodunu çağırır.
            pywebview.api.handle_js_message(messageToSend).then(response => {
                console.log("Python'dan gelen direkt yanıt (async):", response);
                // Python tarafında `evaluate_js` kullanıldığı için bu response genellikle kullanılmaz.
                // updateResponse fonksiyonu ile güncellenecektir.
            }).catch(error => {
                messageResponseParagraph.textContent = `Mesaj gönderme hatası: ${error}`;
                console.error("Mesaj gönderme hatası:", error);
            });
        } else {
            messageResponseParagraph.textContent = "Python bağlantısı henüz hazır değil.";
        }
    });

    // Python'dan veri isteme düğmesi olayı
    requestDataButton.addEventListener('click', () => {
        if (typeof pywebview !== 'undefined' && typeof pywebview.api !== 'undefined') {
            dataResponseParagraph.textContent = "Python'dan veri isteniyor...";
            // Python'daki get_data_from_python metodunu çağırır ve Promise döner.
            pywebview.api.get_data_from_python("some_random_query").then(data => {
                dataResponseParagraph.textContent = `Python'dan gelen veri: ${data}`;
            }).catch(error => {
                dataResponseParagraph.textContent = `Veri isteği hatası: ${error}`;
                console.error("Veri isteği hatası:", error);
            });
        } else {
            dataResponseParagraph.textContent = "Python bağlantısı henüz hazır değil.";
        }
    });

    // Sayfa değiştirme düğmesi: Google'a git
    goToGoogleButton.addEventListener('click', () => {
        if (typeof pywebview !== 'undefined' && typeof pywebview.api !== 'undefined') {
            // Python'daki change_page metodunu çağırarak Google'a gitmesini isteriz.
            pywebview.api.change_page("https://www.google.com").catch(error => {
                console.error("Google'a giderken hata oluştu:", error);
            });
        } else {
            console.error("Python bağlantısı henüz hazır değil. Sayfa değiştirilemiyor.");
        }
    });

    // Sayfa değiştirme düğmesi: İkinci yerel HTML sayfasına git
    goToSecondPageButton.addEventListener('click', () => {
        if (typeof pywebview !== 'undefined' && typeof pywebview.api !== 'undefined') {
            // Python'daki change_page metodunu çağırarak page2.html'e gitmesini isteriz.
            pywebview.api.change_page("page2.html").catch(error => {
                console.error("page2.html'e giderken hata oluştu:", error);
            });
        } else {
            console.error("Python bağlantısı henüz hazır değil. Sayfa değiştirilemiyor.");
        }
    });
});