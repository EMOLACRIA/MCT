# ADR-0011 — Yayın öncesi SDDM ve lock medya cilası

Tarih: 2026-10-17. Durum: **2.6.2 uygulandı / native kabul açık**.

SDDM Qt fixture'ı iki mevcut sorunu üretti: wallpaper.png çözümlenemiyor ve
900×600'de hata mesajlı giriş kartı saatle çakışıyordu. Kesilmiş SDDM dosyası,
sağlam payload PNG'sinin byte byte önekidir; aynı kaynağın tam kopyası kullanıldı.
Yeni dış varlık alınmadı. Bozuk power preview'ı güncel DemoContext'ten render edildi.

Giriş kartı saat altında ve ekran içinde sınırlanır. Yükseklik yetmezse form
kaydırılır; alan/eylem/oturum klavye odağı ilgili satırı görünür tutar. Normal
1600×1000 sağ kart düzeni korunur. Boş liste girişe izin vermez. SDDM login ve
onaylı güç çağrıları aynı servis API'sini kullanır; test servisi gerçek işlem yapmaz.

Lock medya cache'inden gelen JSON yalnız nesneyse kullanılabilir. Metin alanları
string, playing yalnız gerçek boolean true kabul edilir; bozuk JSON/liste/null
yeniden IPC'den okunur. IPC yoksa mevcut boş durum döner. Kilit/parola işlemleri
ve seçili MPRIS oynatıcı protokolü değişmez.

5 Qt greeter testi, 4 SDDM dosya transaction testi, 6 medallion testi ve mevcut
helper kontrolleri geçti. Native PAM/unlock/login ve farklı DPI kompozisyonu
çalıştırılmış sayılmaz. Tam sonuçlar [VALIDATION](../VALIDATION.md) içindedir.

Kullanıcı tema menüsünün yerini daha sonra seçecek. Preferences konumu bir karar
değildir. Tema geçiş araştırması M4'ü kapatmaz, seçici/ikinci tema uygulanmaz.
