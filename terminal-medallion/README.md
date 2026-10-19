# Tema seçimi — 2.9.0

MCT içindeyken `bash preview.sh --theme deltarune` ve
`bash install.sh --theme deltarune` yeni karakter fountain çizimini kullanır;
`--theme plague-tale` önceki madalyona döner. `--compact` desteklenir. Bilgi
modülleri/yorumlar ve ilk restore yedeği aynı kurucuyla korunur. Gerçek CP437
byte kopyaları Deltarune adapters/terminal klasöründedir. Ayrı eski madalyon
paketi MCT helper'ı olmadan da Plague Tale varsayılanıyla çalışır.

# Terminal madalyonu — 1.3 CP437

Ağaç, sağ üstte güneş ve sol altta ay; çevresinde çift yuvarlak çerçeve. Çizim CP437'nin `░`, `▒`, `▓`, `█`, `│`, `─`, `·` ve `°` karakterleriyle düzenlendi. Varsayılan çizim **61 sütun × 29 satır**: ince dal çatalları, kabuk çizgileri, yayılan kökler ve güneş/ay motifleri. Soluk pirinç renkli gerçek karakter çizimidir. Terminalde PNG veya görüntü protokolü kullanılmaz.

## CP437 dosyaları ve Kitty gösterimi

- `medallion.cp437`: **gerçek CP437 byte kodlaması**, CRLF satır sonları, renk etiketi içermeyen bağımsız büyük çizim.
- `medallion-compact.cp437`: aynı kodlamada küçük çizim.
- `medallion.txt`: aynı CP437 karakterlerinin **UTF-8 temsili**, Fastfetch'in `$1` renk etiketiyle.
- `medallion-compact.txt`: küçük çizimin Fastfetch/UTF-8 sürümü.

Kitty ve Fastfetch'te `.txt` dosyaları kullanılır; kurucu bunu otomatik seçer. Gerçek `.cp437` dosyalarını CP437 destekleyen bir editörde veya DOS/ANSI art aracında açabilirsin. Font veya terminalin karakter kodlamasını değiştirmen gerekmez. Bu metin dosyaları imleç/grafik kontrol dizisi içermez.

Önceki 39 × 17 küçük çizim de `medallion-compact.txt` olarak korunur. Yeni çizim yaklaşık 2,7 kat fazla karakter alanı kullanır; bu yüzden terminalde daha fazla yer kaplar. Normal karakter boyutunu değiştirmez.

## Önceki ASCII veya PNG sürümünden geçiş

Yeni ZIP'i ayrı bir klasöre çıkar ve çıkan `terminal-medallion` klasöründe çalıştır:

```bash
bash preview.sh
bash install.sh --check
bash install.sh
```

Ardından Super+Q ile yeni terminal aç. Normal kullanıcınla çalıştır, sudo kullanma. Önceki terminal ekini veya masaüstü temasını geri alman gerekmez. Kurucu önceki ASCII ve PNG sürümlerini tanır, CP437 çizimine geçirir ve **ilk kurulumun orijinal geri dönüş yedeğini korur**. Geçiş öncesindeki config ve metin logo ayrıca yedeklenir. İlk kez kullanıyorsan da aynı komutlar geçerlidir.

Logo ile bilgi satırları arasında beş karakter boşluk bulunur. Küçük çizimi denemek veya ona dönmek için:

```bash
bash preview.sh --compact
bash install.sh --compact
```

Tekrar detaylı sürüme dönmek için `bash install.sh` yeterlidir; bu geçişlerde restore gerekmez. Özel çizim için ilgili UTF-8 `.txt` dosyasının satırlarını düzenleyip kurucuyu tekrar çalıştırabilirsin. Kurucu config aynı kalsa bile logo içeriğinin değiştiğini algılar ve günceller. Görüntüye ait `--width`/`--height` seçenekleri kullanılmaz.

## Sağdaki bilgi satırlarının düzeltmesi

Önceki sürüm, mevcut config bulunmadığında yalnızca `logo` alanı içeren bir dosya oluşturuyordu. Test edilen Fastfetch sürümünde böyle bir config varsayılan bilgi modüllerini devralmadığı için yazılar görünmüyordu.

Bu sürüm, `modules` alanı yoksa veya boşsa bilgisayarında kurulu Fastfetch'in `--gen-config` çıktısından kendi varsayılan bilgi modüllerini alıp ekler. OS, kernel, terminal, CPU, GPU, bellek gibi bilgiler böylece geri gelir. Var olan dolu modül listesi, modül formatları, display ayarları ve logo dışındaki JSONC yorumları korunur. Karşılama fonksiyonu ve prompt değiştirilmez.

Önizleme de bu düzeltilmiş configi geçici dosyadan kullanır; kalıcı ayarlarını değiştirmez. Python 3 ve mevcut Fastfetch yeterlidir; paket program indirmez. Dosya sembolik bağlantıları yerel kopyaya çevrilir, hedeflerine yazılmaz; geri dönüşte bağlantı yeniden kurulur.

## Geri dönüş

Bu paketin klasöründe:

```bash
bash restore.sh --check
bash restore.sh
```

Orijinal, madalyon eklenmeden önceki Fastfetch configine döner. Yedek silinmez. Kurulumdan sonra configi elle değiştirdiysen üzerine yazmaz, yedek yolunu gösterir.

Logo `~/.local/share/terminal-medallion/medallion.txt` altında tutulur; paket klasörünü sonradan taşıyabilirsin. Yedekler `~/.local/state/terminal-medallion/` altında tutulur. XDG_DATA_HOME ve XDG_STATE_HOME desteklenir. Masaüstü paketindeki `desktop-style/restore.sh` bu bağımsız terminal ekini geri almaz.

Özel karşılama fonksiyonun başka config kullanıyorsa:

```bash
bash preview.sh --config "$HOME/.config/fish/motd.jsonc"
bash install.sh --config "$HOME/.config/fish/motd.jsonc"
```

Hâlâ farklı bir logo görünüyorsa `fastfetch --version` ve Fish'te `functions fish_greeting` çıktılarını paylaş.

## Doğrulama

İki `.cp437` dosyası sıkı CP437 kodlama ile yazıldı ve UTF-8 çizimlere kayıpsız geri dönüşü doğrulandı. Gerçek Fastfetch 2.69.0 ile iki çizimin de sağdaki bilgi satırlarıyla birlikte üretildiği, bilgi sütununun 61/39 karakter genişliğinden sonra doğru hizalandığı ve bozuk karakter oluşmadığı kontrol edildi. 1.2'den geçiş, ilk geri dönüş yedeğinin ve modül/display ayarlarının korunması, küçük çizime geçiş ve restore doğrulandı. Önceki geri dönüş/başarısız güncelleme testleri korundu. Kullanıcının canlı Hyprland oturumu bu ortamda bulunmuyor.

Fastfetch metin logo seçenekleri: https://github.com/fastfetch-cli/fastfetch/wiki/Logo-options
