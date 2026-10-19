# Tema çizgisi — 19 Ekim 01:07 revizyonu

Normal uygulama penceresi yerine odaklı ekranda masaüstü katmanı açılır. Ortadaki
yatay çizgide temalar sıralanır. Fareyle üzerine gelince tema genişler ve gerçek
fotoğrafı görünür. **Tek tıklama / Enter** arka planda kontrolleri yapıp uygular;
ayrı check düğmesi veya ikinci seçim adımı yoktur. Hover tek başına uygulamaz.

Kurulu 2.9.0 ve mevcut `fix/shared-theme-behavior` dalında:

```bash
cd ~/newfolder/desktop-style
git pull --ff-only
bash theme.sh bind --check && bash theme.sh bind
```

Sonra **Super+G**. Kurucu depodaki tahmine güvenmez: canlı `hyprctl -j binds`
çıktısını, temiz config'i ve yeni overlay QML'sini kontrol eder. G doluysa, bir
Super+keycode nedeniyle boşluk kanıtlanamıyorsa veya veri okunamıyorsa durur;
başka bir kişisel bağ silinmez. Bu durumda seçici elle açılabilir:

```bash
bash theme.sh menu
```

Super+G/aynı komut tekrar basınca kapatır. İlk açılış QS overlay'i başlatır;
sonraki açılışlar aynı sıcak katmanı IPC ile kullanır. **Sol/sağ veya Tab** gezinir;
**Enter/Space** uygular. **Esc / dışarı tıklama** gizler. Başarılı geçiş kısa “Ready”
yazısından sonra kapanır, hata okunabilir biçimde kalır. Dar ekranda yatay kayar.
Reduce motion/font scale kullanıcı tercihleri korunur ve okunur.

Apply aynı core'un paket/PNG/QML/ABI/elle düzenleme, kilit, snapshot ve journal
kontrollerini kullanır. İkinci elle check olmadığı için aynı aday gereksiz iki
kez derlenmez. İşlem sırasında başka apply başlatılmaz. Paneli gizlemek devam
eden helper'ı kesmez; ayrı QS yaşam döngüsü ana shell restart'ından etkilenmez.
Bu, ayrı normal uygulama açmak değildir; başlık çubuğu/taskbar girdisi yoktur.

**RESTORE LAST** iki tıklamalı son tema snapshot'ına dönüşü korur. İlk kurulum
restore'u veya kaynak rollback'i değildir. Yarım journal varsa önce
`bash theme.sh recover` gerekir. Kişisel dosyaları/yedekleri silme.

Yalnız bu kısayolu kaldırmak:

```bash
bash theme.sh unbind --check && bash theme.sh unbind
```

Sonradan eklenmiş diğer bağlar korunur. Kurucu ayrı ilk binding yedeğini tutar;
ana masaüstünün ilk restore noktasını değiştirmez. Tam desktop restore'dan önce
unbind kullanılabilir. Repo taşınırsa aynı bind komutu kayıtlı bloğu günceller.
`update.sh`, tema rollback veya ayrı uygulamaları tekrar kurmak bu revizyonun
gereği değildir. 2.8 kullanıcıları önce [2.9 yükseltmesini](UPGRADE_2_9.md) yapar.

## Kapsam

Masaüstü, wallpaper, Hyprland görünümü, Kitty paleti ve Hyprlock layout/medya
core tarafından değişir. Kitty paletini yeni terminalde görürsün. Dolphin,
Spotify, SDDM ve terminal süsü önceki gibi ayrı kuruculardır. Bu revizyon onları
zorla kapatıp yeniden kurmaz veya hepsinin otomatik değiştiğini iddia etmez.

İlgili uygulama kapalıyken, seçilen tema için:

```bash
bash apps/install.sh dolphin --theme plague-tale --check && bash apps/install.sh dolphin --theme plague-tale
bash apps/install.sh spotify --theme plague-tale --check && bash apps/install.sh spotify --theme plague-tale
bash terminal-medallion/install.sh --theme plague-tale --check && bash terminal-medallion/install.sh --theme plague-tale
```

Diğer tema için `plague-tale` yerine `deltarune`. SDDM'nin ayrı root/restore
sınırları [yükseltme rehberinde](UPGRADE_2_9.md#ayrı-yüzeyleri-dene).
Yeni Wayland katmanı, compositor odağı ve gerçek Super+G kontrolü cihazdaki yeni
denemedir; offscreen test başarıları bu native sonucun yerine geçmez.
