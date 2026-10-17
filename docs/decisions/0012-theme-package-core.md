# ADR-0012 — Görsel paket işlemi ve kaynak güncellemesi sınırı

Tarih: 2026-10-17. Durum: **2.7.0 uygulandı / 28 izole çekirdek testi geçti**.

## Kullanıcı kararı

Kullanıcı önceki son canlı kontrol maddesinin tamamlandığını ve gün boyu full
kullandığını onayladı; geçiş çekirdeğini istedi, ikinci oyun konuşmasını bu işin
sonrasına bıraktı. Bu ürün/kullanım kapanışı M5'e geçiş için esas alınır. Genel
yayın/lisans ve ayrı ölçülmemiş donanım matrisi bağımsız kalır; eski son kullanım
onayı tekrar istenmez. Yeni CLI kendi native kabulünü ayrıca gerektirir.

## Uygulama

Şema 1 paket, ortak shell ABI'sini ve git blob envanterini tanımlar. İlk Plague
Tale paketi mevcut 38 görsel kaynağı ve gerçek preview PNG'sini taşır. İş komutu,
IPC, servis veya state dosyası tema paketi değildir. Görsel view'ların mevcut
input bağlantıları ortak backend/state'i tüketir; bütün sunum/etkileşim ayrımının
bittiği iddia edilmez. Fotoğraflı menü ve ikinci tema eklenmedi.

Engine native komutları kendisi belirler. Safe path/symlink, mevcut dosya sahipliği,
ABI ve paket bütünlüğü denetlenir; aday tam shell kökünde QML compile edilir.
Snapshot/journal → MCT stop → atomik dosyalar → reload → IPC hazır → commit.
Hata veya interrupted recovery önceki dosya/state/wallpaper yollarına döner.
Elle değişmiş dosya veya başka kuruluma ait snapshot sessizce uygulanmaz.
Eski first-install backup korunur; updater ile aynı update.lock kullanılır.

Kaynak updater, aktif paketin dosyalarını değiştirecekse açık rollback/reapply
ister. Byte-identical update'e izin verir. Otomatik tema sürümü rebase'i yerine
bu ilk sürümde görünür ve veri kaybetmeyen sınır seçildi. Recover journal'ı
başarısız toparlanmada tutulur; tam restore ve kaynak rollback ayrı işlemlerdir.

SDDM/Spotify/Dolphin ayrı kuruculardır. Engine active durumunda bunu bildirir;
bu adaptörleri otomatik apply etmiş gibi raporlamaz. CLI kapsamı lock medya ve
Kitty include dahil core görselleridir. Bu sınır bütün masaüstü adaptörlerini
tek atomik işlem olarak sunma iddiasını önler.

## Kanıt ve sınır

[CI](https://github.com/EMOLACRIA/MCT/actions/runs/39054714755): 28 core + 27 mevcut
test, Python/Bash syntax. Yerel executor kullanılamadığından kaynak GitHub API ile
düzenlendi, GitHub runner'ı kullanıldı. Runtime fake'tir; native Wayland/hyprpaper
ve yeni process readiness yolu hedef cihaz kabulüdür. [Rehber](../THEME_PACKAGES.md).
