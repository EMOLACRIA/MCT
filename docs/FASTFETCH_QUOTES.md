# Fastfetch replik kaydı — 20 Ekim 2026

Kullanıcı beş tema için araştırılmış replik, noktalama doğrulaması ve büyük,
şeffaf yazı istedi. Görünen cümleler şunlardır; tipografik tırnak eklenmez:

| Kimlik | Görünen metin | Bağlam |
|---|---|---|
| plague-tale | We will live. And we will heal. | Amicia, Requiem; yayıncının seçkisiyle doğrulandı. |
| deltarune | (Well, there is a man here.) | Ağaç arkasındaki adamı inceleme anlatımı. |
| deltarune-snowgrave | Proceed | Oyuncunun rota seçeneği; sonunda nokta yok. |
| deltarune-adventure | Nothing is stronger than... a... Flower's... dream...! | Flowery, Knight ile karşılaşma. |
| deltarune-guardian | AND TITANS SHAPE FROM DARKENED EYES. | Bölüm 4 kehanet paneli; Titan'ın konuşması diye sunulmaz. |

## Doğrulama kaynakları

- Plague Tale, yayıncının kendi topluluk sayfasındaki replik seçkisi:
  https://community.focus-entmt.com/focus-entertainment/a-plague-tale-series/votes/59-what%E2%80%99s-your-favorite-line-from-a-plague-tale
  Amicia cümlesi iki noktalı cümle halinde yayımlanıyor; Wikiquote XIII bölümüyle
  de eşleşiyor: https://en.wikiquote.org/wiki/A_Plague_Tale:_Requiem
- Man, anlatım transkripsiyonu: https://deltarune.wiki/w/Man#References
  Oyun betiği aynası, Chapter 5 `gml_Object_obj_room_man_Step_0`, satır 15:
  https://code.deltarune.wiki/raw/ch5/gml_Object_obj_room_man_Step_0.txt
  Metin, görünmeyen hız/bitirme kodları çıkarıldığında parantezli cümledir.
  Baştaki diyalog yıldızı, cümlenin bir parçası değil arayüz işaretidir.
- Snowgrave seçeneği: https://deltarune.wiki/w/Weird_Route/Chapter_2
  Oyun betiği aynasında Chapter 2 `gml_GlobalScript_scr_text`, satır 6133
  (`scr_text_slash_scr_text_gml_7047_0`), Noelle bulmacasının `#Proceed` seçeneği
  de karşılaştırıldı: https://code.deltarune.wiki/raw/ch2/gml_GlobalScript_scr_text.txt
  `Proceed` bir seçim etiketidir; önceki tasarımdaki noktalı öneriyle karıştırılmaz.
- Adventure, Chapter 5 `gml_Object_obj_dw_post_fountain_close_Step_0`:
  https://code.deltarune.wiki/raw/ch5/gml_Object_obj_dw_post_fountain_close_Step_0.txt
  Arama indeksi de indirildi: https://code.deltarune.wiki/ch5/index.json
  Satır 851 ve 858'de iki kutu var. `&` satır sonu, `^1` bekleme kodu, `/%`
  diyalog kontrolüdür. Kodların çıkarılması büyük F'yi, ASCII apostrofu,
  her üçlü noktayı ve son ünlemi korur. İkinci karşılaştırma:
  https://dark.namu.moe/w/%ED%94%8C%EB%9D%BC%EC%9B%8C%EB%A6%AC
  Bu ikincil sayfa üç noktaları tek ellipsis glifiyle yazdığından render'da
  noktalama için oyun betiği esas alındı.
- Guardian, bölüm 4 panelinin tamamından tek cümle:
  https://deltarune.wiki/w/Prophecy#Dark_Sanctuaries
  https://deltarune.wiki/w/The_Roaring
  Asıl oyun metni aynasında Chapter 4 `gml_GlobalScript_scr_prophecytext`, satır 18
  (`scr_prophecytext_slash_scr_prophecytext_gml_29_0`) ile de doğrulandı:
  https://code.deltarune.wiki/raw/ch4/gml_GlobalScript_scr_prophecytext.txt
  Büyük harf ve son nokta korunur. Tema referansı Titan/GUARDIAN sahnesidir.

Bu betik aynası Toby Fox'un resmî sitesi değildir; oyun metnini incelemek için
kullanılan topluluk çıkarımıdır. Ham mesajlarda görünen kontrol kodları kullanıcıya
gösterilmez. Kaynaklar 20 Ekim 2026'da okundu. Tam oyun/betik dökümü dağıtılmaz.

## Tipografi ve aktarım

PNG'ler 1536×1280, gerçek alfa kanallı paletli PNG'dir: arka plan sıfır alfa,
yazı kenarları yumuşak geçişlidir. Plague Tale serif, Deltarune temaları mevcut
Departure Mono ile üretildi. Render aracı: tools/render_fastfetch_quotes.py.
Metin, font hash'i, çizim sınırı ve PNG SHA256'sı fastfetch-quotes/manifest.json'da.
Yazı görüntüsü yeniden AI ile yazdırılmadı; noktalama ve harfler doğrudan fontla
çizildi. Font dosyası hedef makineye yeniden kurulmaz.

Fastfetch, Kitty'nin `kitty-direct` görüntü protokolünü kullanır. Ayrı quote.png
aynı transaction'da tutulur; eski medallion.txt düz metin fallback olarak kalır.
Normal boyut 36×15 terminal hücresi, mevcut compact seçeneğinde 28×12'dir.
Renk, kullanıcının mevcut terminal.py tema renk eşlemesinden alınır; standart
kütüphaneyle yalnız PNG paleti değiştirilir, alfa ve harf şekilleri korunur.
Hedefte Pillow, ImageMagick veya yeni font gerekmez. Kitty dışı terminalde görüntü
protokolünün görünmesi vaat edilmez. Salt metin denemesi gerekiyorsa:

```bash
fastfetch --logo-type file --logo ~/.local/share/terminal-medallion/medallion.txt
```

Fastfetch birincil belge:
https://github.com/fastfetch-cli/fastfetch/wiki/Logo-options#kitty-direct
Kitty bu yöntemde PNG alır; width/height açık verilerek imleç konumu sorgulanmaz.
Gerçek Fastfetch 2.69.0 PTY'de PNG dosyasını Kitty komutuyla iletti ve örnek bilgi
modülünü korudu. Bu, gerçek Kitty pencere render'ının cihazda doğrulandığı anlamına
gelmez. Görsel atlas yalnız yerleşim/piksel incelemesidir; arka planlar önizlemeye aittir.
