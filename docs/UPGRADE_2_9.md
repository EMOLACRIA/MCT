# 2.9.0 / Deltarune 0.2.0 denemesi

Yeni dal: `fix/shared-theme-behavior`. Eski `feature/deltarune` korunur.
Ortak QML şablonları nedeniyle ABI `mct-shell-2.9` oldu. Eski kurulu ortak
dosyaların üstüne yalnız `theme.sh apply` yeterli değildir.

## Önce mevcut dalda

Aşağıdaki ilk adımı **git switch/pull yapmadan**, şu an çalışan 2.8 kaynak
klasöründe uygula. Yalnız tema geçişlerini geri alır; full restore yapmaz,
ilk kurulum yedeğini ve kullanıcı tercihlerini silmez. Kayıtlı apply sayısına
göre geçici olarak birkaç önceki görünümden geçebilir.

```bash
cd ~/newfolder/desktop-style
python3 - <<'PY'
import theme_core
engine = theme_core.Engine()
while engine.optional('active.json') is not None:
    engine.rollback()
print('Tema geçişleri geri alındı; kaynak güncellenebilir.')
PY
```

Bu komut hata verirse sonraki adımlara geçme; elle değişmiş dosya korunur ve
hata gerçek nedeni gösterir. Zaten yeni dala geçtiysen, çalışma dosyalarını
silmeden önce eski `feature/deltarune` dalına dönüp bu hazırlığı orada yap.

## Yeni ortak kaynağı ve görünümü kur

```bash
git fetch origin fix/shared-theme-behavior
git switch fix/shared-theme-behavior
bash update.sh --check && bash update.sh
bash theme.sh check deltarune && bash theme.sh apply deltarune
```

Yerel dal zaten varsa, switch sonrasında `git pull --ff-only` kullan. Özel
Hyprlock düzenin varsa source update onu korur; tema check, tam görsel geçiş için
`~/.config/desktop-style/hyprlock/layout.conf` source satırını ister. Özel ayarını
silme; bu durum otomatik değiştirme yerine açık uyarlama gerektirir.

## Ayrı yüzeyleri dene

Ana apply shell, wallpaper, Hyprland görünümü, Kitty ve artık Hyprlock'un
parola/saat/medya görsellerini değiştirir. Uygulama adaptörleri ayrı işlemlerdir.
Dolphin ve Spotify'ı tamamen kapattıktan sonra:

```bash
bash apps/install.sh dolphin --theme deltarune --check
bash apps/install.sh dolphin --theme deltarune
bash apps/install.sh spotify --theme deltarune --check
bash apps/install.sh spotify --theme deltarune
bash terminal-medallion/preview.sh --theme deltarune
bash terminal-medallion/install.sh --theme deltarune --check
bash terminal-medallion/install.sh --theme deltarune
```

Yeni terminal aç. Fastfetch'in mevcut bilgi modülleri korunur; yeni çizim gerçek
karakterlerden oluşur. `--compact` da desteklenir. Uygulama ve terminal komutlarında
`--theme` verilmezse kayıtlı aktif tema okunur; açık seçim aynı sonucu garantiler.
Plague Tale için aynı komutlarda `--theme plague-tale` kullanılır. Bu yeniden
uygulamalar orijinal uygulama/terminal yedeklerini korur. Reklam engelleyici
başlatıcının `LD_PRELOAD` ortamı korunur; gerçek reklam sonucu burada ölçülmedi.

SDDM önce kurmadan önizlenebilir:

```bash
bash sddm/preview.sh --theme deltarune
```

Görünümü kabul ettiğinde sistem giriş teması için mevcut ayrı kurucuyu kullan:

```bash
sudo bash sddm/install.sh --theme deltarune --check
sudo bash sddm/install.sh --theme deltarune
```

SDDM adaptörü daha önce kuruluysa bu kurucu ilk kaydı ezmez ve durur. Bu durumda
önce `sudo bash sddm/restore.sh`, sonra yukarıdaki check/install uygulanır; eski
yedek tutulur. Display manager veya açık oturum yeniden başlatılmaz. Gerçek
parola/PAM ve sonraki giriş kabulü preview değildir. SDDM'de temayı açıkça belirt;
sudo kullanıcısının HOME'undan masaüstü tercihi tahmin edilmez.

## Kontrol ve geri dönüş

Super+R/M/T/B, Alt+Tab, hesaplama, ses/parlaklık OSD'si ve sağ kontrol menüsünü
dene. Sonra Super+L ile yeni lock görünümüne bak. Anahtarlar aynı kalır.
`bash theme.sh check plague-tale && bash theme.sh apply plague-tale` ile diğer
shell görünümüne geçilebilir; ayrı adaptörlerin aynı anda değiştiği iddia edilmez.

Son görsel geçişi geri almak `bash theme.sh rollback` ile olur. Kaynak revizyonunu
da geri almak istersen yeni dalda bütün tema apply'larını ilk bloktaki döngüyle
geri al, `bash rollback-update.sh` çalıştır ve eski kaynak dalına dön. Full
`restore.sh` günlük kaynak/tema güncellemesinin gereği değildir.

Fotoğraflı seçicinin konumu bu sürümde belirlenmedi ve yeni kısayol atanmadı.
Bu kaynaklar hazırlama ortamında test edildi; cihazdaki son görsel onayı bekler.

## 2.9 kurulmuşsa — Dolphin klasör düzeltmesi

İlk 0.2.0 adaptöründeki klasör SVG'leri yanlışlıkla eski pirinç renginde kalmıştı.
Düzeltme yalnız Dolphin görselleridir. Bütün Dolphin pencerelerini kapatıp:

```bash
cd ~/newfolder/desktop-style
git pull --ff-only
bash apps/install.sh dolphin --theme deltarune --check && bash apps/install.sh dolphin --theme deltarune
```

Sonra Super+E veya launcher'dan yeniden aç. Beyaz yazılar ve ilk uygulama yedeği
korunur. Source update, shell tema apply/rollback veya SDDM kurulumu tekrarlanmaz.
