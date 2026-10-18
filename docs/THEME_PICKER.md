# Fotoğraflı tema seçici

19 Ekim ilk arayüz. Kurulu **2.9.0** masaüstünde, mevcut `fix/shared-theme-behavior`
dalında:

```bash
cd ~/newfolder/desktop-style
git pull --ff-only
bash theme.sh menu
```

Seçici repo aracıdır; bu arayüz güncellemesi için `update.sh`, tema rollback veya
yeniden uygulama kurulumu gerekmez. Eski 2.8 kurulumları önce
[2.9 yükseltme rehberini](UPGRADE_2_9.md) izler.

1. Kartı **Select** ile seç. **View image** gerçek paket ekran görüntüsünü büyütür;
   resmi açmak masaüstünü değiştirmez. Aktif paket sürümü **ACTIVE** işaretlidir.
2. **Check compatibility** salt kontrol yapar. Başarılıysa **Apply theme** açılır.
   Check'i geçmek uygulama değildir; Apply core kontrollerini yeniden yapar.
3. İşlem bitince aktif işaret yenilenir. **Previous theme → Confirm restore**
   son tema snapshot'ına döner. Bu source update veya ilk kurulum restore'u değildir.

Sol/sağ ok kart seçer; Tab ve Enter/Space düğmeleri çalıştırır. Esc büyük resmi,
geri dönüş onayını veya boşta pencereyi kapatır. Dar pencerede kartlar kaydırılır;
uygula/geri dönüş düğmeleri alt alanda kalır. Aynı repo seçicisinin ikinci kopyası
açılmaz. Bar/ayar menüsüne düğme veya yeni global kısayol henüz atanmadı.

İşlem sırasında ikinci komut/tema seçimi kapalıdır. Normal pencere kapatma helper'ı
kesmez: pencere gizlenir, işlem bittikten sonra çıkar. Terminalden zorla kill veya
kesinti halinde core'un pending journal'ı ve `bash theme.sh recover` geçerlidir.
Hata yazısını dikkate al; kişisel dosyaları/yedekleri silmek çözüm değildir.

## Neler değişir?

Masaüstü bar/paneller, wallpaper, Hyprland görünümü, Kitty paleti ve Hyprlock
layout/medya mevcut core ile değişir. Kullanıcı tercihleri, kısayollar ve ilk
yedek korunur. Fotoğraflar mevcut Qt preview render'larıdır; bu arayüz canlı
masaüstü ekran görüntüsü yakalamaz veya yeni görsel üretmez.

**Dolphin, Spotify, SDDM ve terminal süsü ayrı kuruculardır.** Bu ilk arayüz onları
otomatik yeniden kurmaz. İlgili uygulama tamamen kapalıyken, seçilen tema için:

```bash
bash apps/install.sh dolphin --theme plague-tale --check && bash apps/install.sh dolphin --theme plague-tale
bash apps/install.sh spotify --theme plague-tale --check && bash apps/install.sh spotify --theme plague-tale
bash terminal-medallion/install.sh --theme plague-tale --check && bash terminal-medallion/install.sh --theme plague-tale
```

Diğer tema için `plague-tale` yerine `deltarune` kullan. Yeni terminal aç.
Uygulamalar kendi ilk yedeklerini ve Spotify adblock başlatıcısını korur.
SDDM sistem dosyaları ve mevcut kurulum restore'u ayrı olduğu için önce
`bash sddm/preview.sh --theme plague-tale` ile bak;
[SDDM kurulum/restore adımları](UPGRADE_2_9.md#ayrı-yüzeyleri-dene) geçerlidir.
Seçici şifre/PAM veya oturum kapatma işlemi yapmaz.

## Doğrulama sınırı

Qt input/render ve fake runtime ile core geçiş/geri dönüş test edilir. Bu,
kullanıcının Wayland oturumunda yeni seçiciyi çalıştırdığımız anlamına gelmez.
Hedef ilk deneme: menu → diğer kart → check → apply → previous theme → confirm.
