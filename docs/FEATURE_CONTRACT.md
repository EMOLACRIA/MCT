# Ortak özellik sözleşmesi

Bu belge hedef davranışı tanımlar; kaynakta her şeyin uygulandığını söylemez.
İlerleme `../STATUS.md` içindedir. Sözleşme değişikliği bütün temalara aynı anda
uygulanır. Yeni tema kabulünde her satır denetlenir.

## Sabit kullanım alışkanlıkları

| Eylem | Sözleşme |
|---|---|
| Super+R | Launcher aç/kapat; tüm uygulamalarda doğrudan arama; hesaplama sonucu. Ayrı “All applications” basamağı yok. |
| Super+Q | Varsayılan terminal. |
| Super+E | Varsayılan dosya yöneticisi; launcher/dosya bağlantılarıyla aynı tema ve başlatma ayarları. |
| Super+M | Beş seçenekli oturum menüsü; arama alanı yok. Tekrar basınca kapanır. |
| Super+B | Bildirim geçmişi ve DND; tema değiştirme kısayolu olarak yeniden kullanılmaz. |
| Super+T | Donanım paneli; launcher açmaz. |
| Super+L | Güvenli kilit; medya alanı mevcut seçili oynatıcıya bağlı. |
| Alt+Tab / Alt+Shift+Tab | Tüm çalışma alanlarından ileri/geri pencere seçimi; alan numarası görünür. **2.3.0 uygulandı; hedef oturum kabulü bekliyor.** |
| Ses/parlaklık tuşları | Gerçek cihazı değiştirir, ölçülen değeri OSD'de gösterir; Dunst bildirimine dönmez. |
| Esc | Açık shell panelini veya seçimi iptal eder. |

Ek ayarlar ekranının kısayolu henüz seçilmedi. Mevcut kişisel kısayollar keyfi
şekilde sahiplenilmez. SDDM giriş ekranı ve kilit yüzeyi farklı yaşam döngüleridir.

## Her temanın karşılayacağı yüzeyler

| Yüzey | Değişmeyen işlev | Tema tarafından değişebilenler |
|---|---|---|
| Bar / tray | Alanlar, doluluk, odak, tray eylemleri, durumlar | Malzeme, biçim, çerçeve, ikon, ölçü |
| Launcher | Arama, klavye gezinme, uygulama açma, hesaplama/kopyalama | Kart/satır görünümü, font, animasyon |
| Alt+Tab | Pencere/alan bilgisi, MRU, odak geçişi, iptal | Kart düzeni, geçiş, önizleme çerçevesi |
| Kontroller | Ses/mikrofon/çıkış, parlaklık, mevcut ağ yetenekleri, pil | Panel yapısı ve slider görünümü |
| Bildirim | Toast, geçmiş, DND, geçerli eylemler | Kartlar, tipografi, giriş/çıkış hareketi |
| Medya | Gerçek metadata, kapak, oynatıcı seçimi, yetenek bazlı kontroller | Albüm çerçevesi, biçim, görsel süs |
| Donanım | Gerçek veri/bilinmeyen durum; panel kapalıyken izlemeyi durdur | Gösterge düzeni ve çizim dili |
| OSD | Aynı tuşlar, drag/hover davranışı, sessize alma, ölçülmüş değer | Yerleşim tercihleri, malzeme, slider |
| Güç / oturum | Aynı beş işlem, hassas işlemlerde onay | Görsel düzen ve hareket |
| Ayarlar | Kalıcı tercih, doğrulama, sıfırlama, tanılama | Görsel yüzey; ayar anlamları aynı |
| Hyprlock | Güvenli parola akışı, medya bilgisi/kontrolleri | Arka plan, okunabilir yüzeyler, çerçeve |
| SDDM | Hesap/oturum seçimi ve giriş, gerçek greeter uyumu | İlk temayla uyumlu giriş görünümü |
| Dolphin / Spotify | Belgelenmiş kurulum/restore; gerçek başlatıcıyla uyum | Palet, ikonlar, CSS; restart ihtiyacı açık |
| Terminal | Okunabilir terminal paleti; mevcut CP437 madalyonunun teslimi | Tema paleti ve terminal süsü |

Hedef donanımda bulunmayan mikrofon/pil/sensör ve oynatıcının desteklemediği
kontrol, sahte değer üretmez. Yetenek yok mesajı veya pasif durum gösterilir;
bu, bir temanın özelliği unuttuğu anlamına gelmez.

## Pencere seçimi

- Alt+Tab MRU sırasında ileri; Alt+Shift+Tab geri gider. Liste seçim sırasında
  yeniden sıralanmaz. Alt bırakma/Enter seçimi açar; Esc/dışarı tıklama iptal eder.
- Uygulama ikonu yoksa ortak sembol; başlık, çalışma alanı ve monitör bilgisi kalır.
- Kapanan seçim geçerli komşuya geçer; boş liste kapanır. Yeni pencere sona eklenir.
- Seçici başladığı ekranda kalır; ekran çıkarılırsa, dış odak değişirse veya başka
  shell paneli açılırsa iptal edilir. Seçim pencerenin kendi çalışma alanına odaklar.
- Önizleme isteğe bağlı tek karedir; kapalıyken yakalama yoktur. Yakalama eksikliği
  seçim/iptal işlevini değiştirmez. Mevcut kişisel Alt/Tab bağları korunur.

## Panel ve ayar davranışı

- Bildirimde değişen başlık/metin/eylemler aynı kartı günceller, unread sayısını
  yeniden artırmaz. Bildirimin geçerli süresi dolunca canlı eylemler kaldırılır;
  arşiv metni kalabilir. `0` süresiz, `-1` sunucu varsayılanıdır (4500 ms).
  Toast en fazla 4500 ms görünür; uygulamanın daha kısa geçerli süresi korunur. Hedef sürümün
  aynı nesne güncellemeleri ve zaman birimi adaptör tarafından ele alınır.

- Paneller tek örnek: aynı kısayol kapatır, başka panel önceki paneli değiştirir.
- Odaklı ekran, mantıksal koordinatlar ve ekran sınırına sığma ortak davranıştır.
- Tema paketinde iş komutu veya yeni global kısayol tanımlanmaz. Bu hedef mimaridir;
  mevcut dosyaların henüz bu kurala tamamen taşındığı varsayılmaz.
- Kullanıcı ayarı, tema varsayılanından ayrıdır. Tema değişiminde kısayollar,
  uygulama tercihleri ve erişilebilirlik tercihleri sıfırlanmaz.
- Başarısız tema uygulaması bir önceki geçerli duruma döner. Bu gelecek M5 kabulüdür.
