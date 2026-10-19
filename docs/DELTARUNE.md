# Deltarune — 0.3.1 / ağaç ve Kris

Ortak kaynak 2.9.0, ABI `mct-shell-2.9`; bu revizyon ortak ABI'yi değiştirmez.
Önceki 0.2.0 camgöbeği fountain görünümünün yerine kullanıcının seçtiği son
indigo/lavanta/fuşya referans uygulanır. [Dört tema kararı](decisions/0016-deltarune-four-worlds.md).

![Gerçek Qt launcher önizlemesi](../themes/deltarune/preview.png)

Kırık dal çizgili çerçeveler, Departure Mono, sade başlık ikonları; kompakt sol
launcher, sağ controls/medya/bildirim geçmişi. Merkez panel tercihi öncelikli,
alt şerit yok. Super+R/M/T/B/Q/E/L, Alt+Tab, hesaplama, tray ve sürüklenebilir
OSD ortak kaynaktır. Super+G mevcut kabul edilmiş tema çizgisini açar.

## Kurulu 2.9.0 üstüne dene

Aynı çalışma dalında güncel kaynakları al:

```bash
cd ~/newfolder/desktop-style
git pull --ff-only
bash theme.sh check deltarune && bash theme.sh apply deltarune
```

Bu görsel paket için `update.sh`, masaüstü restore veya önce eski temayı rollback
etmek gerekmez. Source ortak ABI farklı diyorsa bu komut zaten durur;
[2.9 yükseltme rehberi](UPGRADE_2_9.md) eski kaynaklar içindir, bu revizyonda
çalışan sistemi baştan kurma adımı değildir. Mevcut ilk restore yedeği ve tercihler
korunur. Aynı `deltarune` kimliği yeni 0.3.1 sürümünü uygular.

Kurulumsuz bakmak: `bash preview.sh deltarune`.
[Medya render'ı](../previews/deltarune/media.png). Preview altındaki bilgi etiketi
sadece önizleme penceresindedir; native masaüstüne alt menü eklenmez.

Wallpaper kullanıcının onayıyla **RealESRGAN_x4plus** üzerinden 4× büyütüldü:
1200×675 → 4800×2700 PNG. Bu, sanatçının yüksek çözünürlüklü orijinali değil,
sinir ağıyla restore edilmiş türevdir. Kaynak JPEG değişmeden korunur. Fırça
dokusunu daha fazla koruduğu için iki küçük örnekten genel model seçildi.
Kaynak/model/hash bilgisi [restoration.json](../themes/deltarune/restoration.json)
içindedir. 0.3.0 yalnız format dönüşümü kullanıyordu. Referanstaki
dekoratif müzik progress çizgisi bir sahte seek kontrolüne dönüştürülmedi;
mevcut gerçek MPRIS oynat/duraklat/önceki/sonraki ve oyuncu seçimi korunur.

## Ayrı uygulama uyarlamaları

Shell apply wallpaper, shell, Hyprland border, Kitty ve sonraki Hyprlock'u
uygular. Dolphin/Spotify/SDDM/CP437 ayrı kuruculardır; otomatik çalıştırılmaz.
Dolphin/Spotify'ı kapattıktan sonra mevcut kurucuyla yeni renkleri uygula:

```bash
bash apps/install.sh dolphin --theme deltarune --check
bash apps/install.sh dolphin --theme deltarune
bash apps/install.sh spotify --theme deltarune --check
bash apps/install.sh spotify --theme deltarune
```

Dolphin'in normal/seçili yazıları beyaz kalır; lavanta klasörler fuşya detay taşır.
Spotify'ın özel istemci/adblock başlatıcısı ve ilk yedeği mevcut kurucunun
sorumluluğundadır; tema bunları yeni bir yolla değiştirmez.
SDDM önizlemesi: `bash sddm/preview.sh --theme deltarune`.
Diğer mevcut komutlar [yükseltme rehberinde](UPGRADE_2_9.md); sudo SDDM adımı
ve ayrı terminal kurucusu gerektiğinde aynı akışla kullanılır.

Guardian, gün batımı ve Snowgrave sonbahar görünümleri kabul edilmiş sonraki
üç temadır; henüz çalışır paket olmadıkları için seçicide görünmezler.
