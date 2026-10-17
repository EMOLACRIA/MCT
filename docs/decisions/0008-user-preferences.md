# ADR-0008 — Tema dışı kullanıcı tercihleri

Tarih: 2026-10-17. Durum: uygulandı; native oturum kabulü bekliyor.

## Karar

`logic/Preferences.js` şema/default kaynağıdır. İşaretli blok strict JSON'dur;
Python yardımcı aynı bloğu JSON olarak okur. Alan türü, aralık, enum ve application-ID
kuralları burada tanımlanır; JS/Python doğrulayıcıları bunun iki tüketicisidir.
`PreferencesState` saf Qt istek/cevap modelidir. `PreferencesStore` QuickShell Process
ile fixed argv/JSON paketleri kullanır; UI `Settings` yalnız modeli tüketir.

Native kayıt `$XDG_CONFIG_HOME/mct/preferences.json` dosyasına 0600 geçici dosya,
flush/fsync ve os.replace ile yapılır. Başarılı JSON cevabı gelmeden yeni değer aktif
olmaz. Hata halinde önceki değer/dosya korunur. Şema sürümü 1; eksik bilinen alanlar
evrim için default'la tamamlanır. Bilinmeyen alan/sürüm korunarak reddedilir.
Bozuk dosyaya normal save yapılamaz; açık onaylı reset önce eski dosyayı saklar.
Preview yalnız bellektir; native yardımcı veya gerçek tercih dosyası çalıştırmaz.

Tercih dosyası tema payload/snapshot dışında kalır; install/update/restore onu
sahiplenmez. Root Theme yalnız fontSize, duration ve yüzey alpha'sını/yerleşimi alır;
metin alpha'sını azaltmaz. Yeni tema veya tema değiştirici uygulanmaz. Harici
uygulama/Hyprlock/SDDM ayarları bu shell font tercihi değildir.

Terminal ve FileManager yardımcıları aynı dosyayı okur. Stok Super+Q tek terminal
script'ine taşınır; launcher Terminal=true yolu da onu çağırır. Kitty/Alacritty/Foot
argümanları ayrı argv'dir. Super+E seçilen desktop girdisini GIO'ya bırakır; Dolphin'in
kullanıcı/system önceliği ve temalı Exec ortamı korunur. Özel Q/E bağı değiştirilmez.
Bozuk tercih dosyasında bu temel yardımcılar varsayılanlara döner; dosyayı onarmaz.
Eksik seçili uygulama için keyfi yeni uygulama kurulmaz veya shell komutu üretilmez.
OS MIME varsayılanlarını değiştirme kararı yoktur.

Ayar girişi kontrol panelinin dişlisidir; global tuş sahiplenilmez. Native helper
tek süreçte çalışır, bekleyen istek sıraya alınır; başarısız başlama/eksik cevap ve
uzun süren işlem görünür hata verir. Elle düzenleme panel açılınca/Reload ile okunur;
eşzamanlı dosya birleştirme servisi yoktur. Tanılama yalnız path ve sürüm komutlarıdır.

## Kaynak ve doğrulama

QuickShell v0.3.1 yerel kaynakları: Process command/running/exited/runningChanged ve
StdioCollector streamFinished; DesktopEntry categories/id, uzantısız ID üretimi.
[Process](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/io/process.hpp),
[DesktopEntry](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/core/desktopentry.hpp).
Terminal seçenekleri 17 Ekim birincil belgelerde karşılaştırıldı:
[Kitty](https://sw.kovidgoyal.net/kitty/invocation/),
[Alacritty](https://alacritty.org/cmd-alacritty.html),
[Foot upstream man, Arch paketi](https://man.archlinux.org/man/foot.1.en).
Bu, kullanıcı paketlerinin gerçek başlatma testi değildir.

15 stdlib + 10 gerçek Qt testi; JS şema, atomik hata/kayıt, reload, bozuk dosya/reset,
Q/E koruması, GIO/terminal argümanları ve update/rollback korunması geçti. Network
import yeni paneli oluşturdu. 30 QML bytecode, 105 native binding ve önceki
launcher/Alt+Tab/OSD/kurulum kontrolleri geçti. 1600×1000'de %120 font üst/alt panel
render'ları incelendi; 900×600 sınırları test edildi.

Native Process, gerçek uygulama başlatması, bar reserve/OSD konumu ve restart'ta
kalıcılık hedef kullanıcı oturumunda bekliyor. M2/M3 veya Plague Tale yayın kapısı
bu hazırlama kontrolleriyle kapanmaz. Kabul listesi `../VALIDATION.md` içindedir.
