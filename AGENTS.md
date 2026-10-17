# Çalışma talimatları

## Her görevin başında

- `PROJECT_BRIEF.txt`, `STATUS.md`, `ROADMAP.md` ve ilgili kaynakları oku.
- Davranış değişecekse `docs/FEATURE_CONTRACT.md`; mimari değişecekse
  `docs/ARCHITECTURE.md` ve ilgili `docs/decisions/` kaydını oku.
- Kullanıcının yeni açık talimatı bu kayıtlardan önce gelir. Kabul edilen kapsam
  değişikliğini aynı işte belgelerde güncelle; kendi önerini kabul edilmiş karar sayma.
- Tamamlanmış, uygulanmış fakat canlı doğrulanmamış ve sadece planlanmış işleri
  ayır. Belleğe veya eski sohbet iddiasına dayanarak bir sorunu kapatma.

## Ürün kuralları

- Önce Plague Tale tamamlanır. Sürüm kapısı kapanmadan ikinci tema ve tema
  değiştirici arayüzü geliştirilmez. Ortak davranış/görsel ayrımı mevcut temada yapılabilir.
- Tema değişince özellik veya kısayol kaybolmaz. İlgili özellik sözleşmesi esas alınır.
- Pano/yakalama paneli kapsam dışı, oyun kütüphanesi ertelenmiştir.
- Vitreus ve Caelestia ilhamdır; runtime göçü veya kod kopyalama kararı değildir.
- Görünen masaüstüne oyun/tema markası ekleme. Okunabilirlik ve ikon merkezleri önemlidir.

## Kaynak haritası ve hedef

- `payload/style/shell/`: QuickShell QML, servis erişimi ve Python yardımcıları.
- `payload/style/scripts/`: süreç, oturum, menü ve OSD komutları.
- `payload/hypr/`: Hyprland Lua payload'ı. `apps/`: bağımsız Dolphin/Spotify eklentileri.
- `sddm/`: ayrı, sistem dosyalarına yazan SDDM kurucusu.
- Hedef Hyprland 0.56.2 Lua, QuickShell 0.3.1; yeni API'yi ilgili sürüm kaynağıyla doğrula.
- Ekran konumları mantıksal koordinatlarla hesaplanır; fiziksel çözünürlüğü sabit kodlama.
- Kullanıcının monitör/GPU/VRR/giriş ayarlarını tema özelliği gibi değiştirme.

## Değişiklik ve doğrulama

- `rg` ile ara. Mevcut arayüzleri ve kurucunun rollback/ilk yedek davranışını koru.
- Eşdeğer başlatma yolları aynı uygulama ayarına ulaşmalı; özellikle Dolphin
  launcher/Super+E için ortak desktop girdisi kullanımını koru; güncel kabul
  durumu STATUS.md üzerinden kontrol edilir.
- QuickShell `feedback.present` adını koru; CLI'nin `show` alt komutuyla eski çakışmayı tekrarlama.
- İlgili, mevcut kontrolleri çalıştır. Basit metin/renk değişikliğine kopya test ekleme.
- `checks/` kaynaklarının bir bölümü eski hazırlama çalışma alanına bağlıdır;
  onları çalıştırılabilir bağımsız CI gibi sunma. `checks/README.md` ve
  `docs/VALIDATION.md` sınırlarını kullan.
- Önizleme: `bash preview.sh`. Kullanıcının gerçek oturumunda salt kontrol:
  `bash update.sh --check`; Dolphin/Spotify için `bash apps/install.sh APP --check`.
  Bunlar yerel hedef ortam gerektirir. Hazırlama makinesinde başarılı olmuş gibi yazma.
- Kullanıcının açık talimatı olmadan preview/validasyon sırasında oturum kapatma,
  servis devralma veya installer çalıştırma. Bu komutların ne yaptığını oku.
- Kaynak değişikliğiyle birlikte STATUS, ilgili kabul ölçütü ve karar kaydını güncelle.
  Tarih/komut/sonuç bilgisi olmayan test iddiası üretme.

## Git ve varlıklar

- Geliştirme bu çalışma dalındadır; eski masaüstü otomatik taşınmış sayılmaz.
- Önce `git status` ve diff'e bak; kullanıcı değişikliğini silme, force push yapma.
- Önbellek, log, yedek, hesap bilgisi, yerel kullanıcı konfigürasyonu veya bağımlılık
  ortamını commitleme. Runtime payload'ı ile gerçek kullanıcı dosyasını ayır.
- Kaynak ve görsel kökenlerini `docs/ASSETS_AND_LICENSES.md` içinde tut.
  Harici projeyi referans vermek, kodunu/görsellerini kopyalamaya izin değildir.
- Son raporda değişen davranış, gerçek kontrol sonucu ve kalan canlı doğrulama yazılır.
