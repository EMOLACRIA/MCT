# Referanslar ve araştırma kaydı

İnceleme: **2026-10-17**. Özellikler aşağıdaki upstream belgelerinin iddiasıdır;
projeleri kurup canlı test ettiğimiz anlamına gelmez. Kod/görsel bu görevde alınmadı.

## Vitreus — kullanıcının özellikle seçtiği referans

- Repo: https://github.com/natepayn3/Vitreus
- İncelenen ana dal commit'i: `9376f72953d666181958fca29e366145f7a40513`.
- README içerik blob'u: `15503a6fe03ff0b49298dc9cd5d5205038129c6a`.
- Güncel runtime **pleamar**. QuickShell teması sanılarak kod taşınmamalı.
- Dikkat çekenler: bardan akarak çıkan bağlı paneller, yay benzeri tutarlı hareket,
  ada/çerçeve düzenleri, canlı hesaplama ve dönüşümler, workspace overview,
  bütünlüklü settings ve farklı malzeme/font kullanan görsel stiller.
- Bizim için ilham: yüzeyler arası süreklilik; tek eyleme ait akışın tutarlılığı;
  farklı tema görünümüyle aynı kullanım alışkanlığı. Camı Plague Tale'e
  zorunlu estetik olarak taşımak kararlaştırılmadı.
- README'nin AI, pano, ekran yakalama, not, hava durumu gibi ekleri bu projenin
  kapsamına otomatik kabul edilmiş değildir.
- README lisansı MIT; pleamar ayrı BSD-3-Clause olarak belirtiliyor. Kod alınacaksa
  dosya bazında lisans/bildirim ayrıca doğrulanmalı.

## Caelestia — kullanıcının özellikle beğendiği referans

- Shell: https://github.com/caelestia-dots/shell
- Dots: https://github.com/caelestia-dots/caelestia
- İncelenen shell ana dal commit'i: `a3a8fe59aba2c0048ab02dc817748678f96076ff`.
- README içerik blob'u: `f7af78dd0db30186c20124dc36f7fe81b4ce1e1c`.
- QuickShell/Hyprland tabanı; shell ve tüm dotfiles ayrı projeler.
- Dikkat çekenler: tutarlı bileşenler; hareket ve görünüm ayarları; aynı servisleri
  kullanan paneller ve uygulama varsayılanları. Güncel README manual kurulumda
  QuickShell-git ister; bizim 0.3.1 ile doğrudan uyum varsayılmaz.
- Repo GPL-3.0 lisanslı görünüyor. Kod taşınmadan önce uyum ve attribution değerlendirilir.

## Belge biçimi araştırması

- https://agents.md/ — ajan çalışma bağlamı, kurallar, komutlar; README'den ayrı.
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
  — projenin ne olduğu, niye yararlı olduğu, nasıl başlanacağı ve ayrıntı bağlantıları.
- https://adr.github.io/ — tek önemli kararın bağlamı, gerekçesi ve sonuçlarını kaydetmek.

Bu nedenle PROJECT_BRIEF.txt ürün niyetini; AGENTS.md çalışma kurallarını;
ROADMAP.md sırayı; STATUS.md gerçek ilerleme/sınırlamayı; karar kaydı gerekçeyi tutar.
Belgeler birbirinin uzun kopyaları olarak sürdürülmez.
