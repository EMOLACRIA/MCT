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
| Alt+Tab / Alt+Shift+Tab | Tüm çalışma alanlarından ileri/geri pencere seçimi; alan numarası görünür. **2.3.0 normal kullanım kullanıcı onayı.** |
| Ses/parlaklık tuşları | Gerçek cihazı değiştirir, ölçülen değeri OSD'de gösterir; Dunst bildirimine dönmez. |
| Esc | Açık shell panelini veya seçimi iptal eder. |

Ayarlar kontrol panelindeki dişliden açılır; yeni global kısayol yoktur. Mevcut
kişisel kısayollar keyfi şekilde sahiplenilmez. SDDM giriş ekranı ve kilit yüzeyi farklı yaşam döngüleridir.

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

## Launcher hesaplama

- Super+R uygulama aramasını korur. Aritmetik tanınırsa sonuç ilk satırda yer alır;
  eşleşen uygulamalar aşağıda kalır. ↑/↓ seçer; Enter seçili uygulamayı açar veya
  sonucu kopyalar. Ctrl+Enter seçili satırdan bağımsız sonucu kopyalar; Ctrl+C
  metin alanının normal kopyalama davranışıdır. Fare/Copy de sonucu kopyalar.
- Kopyalama launcher'ı kapatmaz veya ifadeyi silmez; kartta geçici “Copied” görünür.
  Yeni girdi eski kopyalama durumunu kaldırır. Hata/eksik ifadede eski sonuç kopyalanmaz.
- `+ - * / ^`, parantez, unary `+/-`, ondalık nokta veya virgül; `× ÷ −`
  sembolleri ve bilimsel sayı gösterimi desteklenir. Binlik ayıracı/örtük çarpma yoktur.
- Yüzde postfix `/100` anlamındadır: `50%=0.5`, `200*10%=20`, `200+10%=200.1`.
  `^` sağdan birleşir; `-2^2=-4`, `2^-2=0.25`. Modulo/bağlamsal indirim değildir.
- Standart IEEE-754 double kullanılır. Görünen/kopyalanan metin en fazla 12 anlamlı
  basamak; noktalı, binlik gruplamasızdır. Sonsuz/NaN sonuç gösterilmez.
- Eksik ifade veya sıfıra bölme satır içi mesajdır. Parser yalnız aritmetik okur;
  eval/Function, shell, dosya veya fonksiyon çağrısı çalıştırmaz. En çok 512 karakter,
  256 token ve 32 iç içe ifade. `=` öneki açık hesaplama niyetini belirtir; uygulama
  adları (ör. `1password`) arama olarak kalır. Birim dönüşümü henüz uygulanmadı.
- 2.4.0 normal kullanım 17 Ekim kullanıcı tarafından onaylandı; her alt pano testi
  tek tek raporlanmış sayılmaz.

## Pencere seçimi

- Alt+Tab MRU sırasında ileri; Alt+Shift+Tab geri gider. Liste seçim sırasında
  yeniden sıralanmaz. Alt bırakma/Enter seçimi açar; Esc/dışarı tıklama iptal eder.
- Uygulama ikonu yoksa ortak sembol; başlık, çalışma alanı ve monitör bilgisi kalır.
- Kapanan seçim geçerli komşuya geçer; boş liste kapanır. Yeni pencere sona eklenir.
- Seçici başladığı ekranda kalır; ekran çıkarılırsa, dış odak değişirse veya başka
  shell paneli açılırsa iptal edilir. Seçim pencerenin kendi çalışma alanına odaklar.
- Önizleme isteğe bağlı tek karedir; kapalıyken yakalama yoktur. Yakalama eksikliği
  seçim/iptal işlevini değiştirmez. Mevcut kişisel Alt/Tab bağları korunur.

## Ortak ayarlar

- 2.5.0'da kaynakta uygulanmıştır; native oturum kabulü bekliyor. Kontrol panelinin
  dişlisi açar, Esc kapatır; UiState içinde diğer panellerle tek örnektir.
- Shell font ölçeği %90–120, hareketi azaltma, ana yüzey alpha %75–100. Metin alpha'sı
  azaltılmaz. Varsayılanlar %100 yazı, hareket açık, %96 yüzeydir.
- Floating bar, tarih ve tray görünürlüğü; yan panel ortalama; üst/alt OSD. Varsayılan
  yerleşim korunur. Bunlar monitör çözünürlüğü/ölçeği/GPU/VRR ayarı değildir.
- Kurulu Kitty/Alacritty/Foot seçimi Super+Q ve terminal isteyen launcher girdilerinde
  ortaktır. Super+E seçili FileManager desktop girdisini GIO ile açar. Açıkça adıyla
  aranan uygulama kendi girdisini açar; OS MIME varsayılanları değiştirilmez.
- Stok Q/E bağları yönlendirilir; kullanıcıya özel farklı bağ/komut korunur.
- Tercihler tema payload'ı dışındaki sürümlü JSON'dadır. Güncelleme, tema revizyonu
  rollback'i ve full restore dosyayı silmez. Kaydetme başarısızsa aktif değer korunur.
- Hatalı değerler açıklanır; bozuk dosyaya otomatik yazılmaz. Reset ikinci onay ister
  ve eski dosyayı saklar. Varsayılan uygulama yardımcıları bozuk JSON'da varsayılana
  döner; temel terminal/dosya yöneticisi erişimi kalır.
- Preview yalnız bellektir. Ayarı yeniden yükleme ve salt okunur sürüm/path tanılaması
  vardır. Harici uygulama, Hyprlock ve SDDM yazı/palet ayarları ayrı adaptörlerdir.

## Panel ve ayar davranışı

- Bildirimde değişen başlık/metin/eylemler aynı kartı günceller, unread sayısını
  yeniden artırmaz. Bildirimin geçerli süresi dolunca canlı eylemler kaldırılır;
  arşiv metni kalabilir. `0` süresiz, `-1` sunucu varsayılanıdır (4500 ms).
  Toast en fazla 4500 ms görünür; uygulamanın daha kısa geçerli süresi korunur. Hedef sürümün
  aynı nesne güncellemeleri ve zaman birimi adaptör tarafından ele alınır.

- Paneller tek örnek: aynı kısayol kapatır, başka panel önceki paneli değiştirir.
- Uzun medya/oturum içeriği sıkıştırılmaz; kullanılabilir yükseklik yetmiyorsa
  kaydırılır, klavye seçimi görünür tutulur. Uzun oynatıcı/eylem adları paneli
  genişletmez; tam ad hover'da okunabilir. Güç işlemlerinin onay koşulu değişmez.
- Tray ortak eylemlere bağlı kalır. Alan yetmediğinde gezinme okları simgeleri
  gösterir; sağ tık/orta tık/tekerlek uygulamanın kendi eylemi olarak korunur.
  Yerleşim kontrol kapsamı ve çok dar ekran sınırı `VALIDATION.md` içindedir.
- Odaklı ekran, mantıksal koordinatlar ve ekran sınırına sığma ortak davranıştır.
- Tema paketinde iş komutu veya yeni global kısayol tanımlanmaz. Bu hedef mimaridir;
  mevcut dosyaların henüz bu kurala tamamen taşındığı varsayılmaz.
- Kullanıcı ayarı, tema varsayılanından ayrıdır. Tema değişiminde kısayollar,
  uygulama tercihleri ve erişilebilirlik tercihleri sıfırlanmaz.
- Başarısız tema uygulaması bir önceki geçerli duruma döner. Bu gelecek M5 kabulüdür.
