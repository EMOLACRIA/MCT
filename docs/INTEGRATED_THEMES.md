# Forgotten Tree Fastfetch görseli — 0.3.1

20 Ekim 2026: kullanıcı, küçük piksel yazılı ağaç görselini onayladı.
Yalnız deltarune/Forgotten Man görseli değişir. PNG tam renkli ve gerçek alfa
kanallıdır. Onaylanan dosya yeniden renklendirilmeden aynen kullanılır.
Kare görsel için alan normal 36×18, compact 28×14 hücredir; oran korunur.

```bash
unzip -o ~/Downloads/MCT-forgotten-tree-0.3.1.zip -d ~/Downloads &&
python3 ~/Downloads/MCT-forgotten-tree-0.3.1/import_source.py ~/newfolder/desktop-style &&
cd ~/newfolder/desktop-style &&
bash theme.sh integrations enable
```

Mevcut 0.3.0 kaynakları üstüne uygulanır. İlk enable aktif temayı eşitler;
Forgotten Man şu an seçili değilse Super+G ile seçildiğinde yeni ağaç görünür.
Yeni terminal açmak veya fastfetch çağırmak yeterli. Diğer dört replik, tema
paketleri, adapter/terminal renk listeleri ve Dolphin/Spotify/Hyprlock/SDDM
kurulumları korunur. update.sh veya SDDM kurulumu gerekmez.
PNG, mevcut quote journal'ında tutulur; rollback eski görseli ve boyutları geri
alır. Önceki kaynak dosyaları indirilen paketin source-backups klasöründedir.
[Onay ve doğrulama kaydı](FORGOTTEN_TREE_FASTFETCH.md).

Aşağıdaki 0.3.0 notları önceki tam replik paketini anlatır; Forgotten Man artık
tek renkli tipografik PNG yerine tam renkli ağaç görselini kullanır.

# Tema geçişi: şeffaf Fastfetch replikleri — 0.3.0

20 Ekim 2026. Kullanıcı 0.2.0 replik/Dolphin geçişini onayladı; bu revizyon beş
temanın tamamını doğrulanmış, büyük ve şeffaf yazı PNG'sine geçirir.
[Replikler, kaynaklar ve noktalama](FASTFETCH_QUOTES.md).

## 0.2.0 üstüne bir kez güncelle

```bash
unzip -o ~/Downloads/MCT-theme-sync-0.3.0.zip -d ~/Downloads &&
python3 ~/Downloads/MCT-theme-sync-0.3.0/import_source.py ~/newfolder/desktop-style &&
cd ~/newfolder/desktop-style &&
bash theme.sh integrations enable
```

Mevcut Dolphin tercihi korunur. SDDM root kurulumu, update.sh veya dal değişimi
gerekmez. Import yalnız entegrasyon motoru, yeni replik yardımcı modülü, beş PNG,
PNG manifesti ve iki belgeyi yazar; tema paketleri, terminal.py, adapter listesi ve
başlatıcılara dokunmaz. Önceden düzenlenmiş hedefleri yazmadan durur; eski kaynak
sürümleri indirilen paket içindeki source-backups'ta saklanır. Yeni PNG'nin gerçek
kullanıcı verisi kopyası da aynı tema journal'ıyla korunur; elle değişmişse ezilmez.
Pillow/ImageMagick kurulumu gerekmez. Normal kullanım mevcut Kitty terminalindedir.
İlk import sonrasında enable aktif temayı hemen günceller; sonraki Super+Q veya
fastfetch çağrısı büyük yazıyı gösterir. Normal boyut 36×15, kompakt 28×12 hücredir.

## Günlük kullanım

Super+G veya `bash theme.sh apply TEMA` beş yüzeyi ortak işlemden geçirir:

- Fastfetch: sonraki çağrıda doğru süs/replik. JSONC yorumları, bilgi modülleri,
  display seçenekleri ve ilk restore yedeği korunur.
- Spotify: mevcut özel istemcinin CSS/paleti güncellenir. Açıksa kısaca yeniden
  açılır; kapalıysa açılmaz. Adblock/preload ve başlatıcılar korunur. MPRIS ile
  konum/durum geri yükleme best-effort'tur; ilk kurucu tekrar çalıştırılmaz.
- Hyprlock: sonraki kilit açılışında seçilen düzen/görseller.
- SDDM: sonraki greeter açılışında seçilen önbellek. Sabit desktop-style yolu
  root tarafından atomik bağ değiştirmeyle güncellenir; giriş servisi restart edilmez.
- Dolphin: palet ve klasör ikonları değişir. qt6ct ayar klasörüne geçici bildirim
  dosyası oluşturulup kaldırılır; qt6ct yaklaşık 3 saniye sonra palet ve ikon
  önbelleğini yeniler. Dolphin kapatılmaz; sekmeler/klasörler ve dosya işlemleri
  olduğu gibi kalır. Canlı yenileme hedef cihazdaki qt6ct sürümüyle doğrulanmalıdır;
  eski görünüm kalırsa normal kapatıp açmak güncel başlangıç paletini yükler.

Dolphin'in normal/seçili metni beyaz kalır. dolphinrc, qt6ct.conf ve desktop
başlatıcısına geçiş sırasında yazılmaz; sahiplenilen ilgili ayarların hâlâ geçerli
olduğu kontrol edilir. Elle değiştirilmiş yönetilen palet/ikon/config ezilmez.

## Fastfetch replik görselleri

Beş temada da [kaynak kaydındaki](FASTFETCH_QUOTES.md) kısa metin görünür.
Arka plan yüzde yüz şeffaftır; kutu/plaka veya tema adı basılmaz. Cümlenin
noktalaması ve büyük/küçük harfleri korunur, yalnız satır kırılımları yerleşime
uyarlanır. Mevcut modüller, yorumlar ve display ayarları değişmez. PNG'ye ek olarak
aynı cümlenin düz metni mevcut medallion.txt alanında tutulur.

## Geri alma ve kurtarma

```bash
bash theme.sh rollback
bash theme.sh recover
bash theme.sh integrations status
```

Dolphin ve Fastfetch PNG de aynı transaction içinde before/after byte, mode ve SHA256 ile tutulur.
Başarısız geçişte önceki palet/ikonlar geri yazılır ve qt6ct tekrar haberdar edilir.
Yarım işlem recover ile tamamlanmadan yeni seçim yapılmaz. Sonraki kişisel düzenleme
varsa recovery onu koruyup durur; journal silinmez. Eski 0.1.0/0.2.0 işlemleri okunabilir; PNG öncesi geri almada yeni quote.png kaldırılır;
eski işlemde Dolphin snapshot'ı yoksa önceki tema için Dolphin paleti hesaplanır.

```bash
bash theme.sh integrations disable
```

Otomatik uygulama/SDDM geçişini durdurur ve mevcut görünümü korur. Bağımsız
kurucuları/restore'u çalıştırmadan önce bunu kullan. Dolphin normal bağımsız
restore'u ilk yedeği kullanmaya devam eder. SDDM sistem yardımcısını kaldırmak
istenirse önce disable, ardından `sudo python3 sddm/sync_setup.py remove`.
SDDM cache görsellerini ileride değiştirdiğinde önceki kurulum komutuyla yenile:
`sudo python3 sddm/sync_setup.py install --user "$USER"`.

## Doğrulama sınırı

Hazırlama ortamında geçici dosya kökleri/mock süreçlerle journal, rollback,
recovery, eski işlem uyumluluğu, ilk yedek ve elle düzenleme koruması sınandı.
Gerçek native Dolphin/qt6ct yenilemesi, Spotify/MPRIS ve sonraki kilit/greeter
bu kaynak testleriyle doğrulanmış sayılmaz. Bu revizyonda Wayland oturumu veya
sistem kurucusu çalıştırılmadı. Adventure görsellerinin gerçek paketi burada
bulunmadığından kaynak koruması ve aynı kimlikli manifest fixture'ı kullanıldı.
