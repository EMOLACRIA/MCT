# ADR-0015 — İlk fotoğraflı seçici (tarihsel)

19 Ekim 01:07 kullanıcı revizyonuyla sunum/entry kararı ADR-0016 ile değişti.
Aşağıdaki FloatingWindow ve açık konum notları önceki denemedir.

19 Ekim 2026 · Uygulandı / yeni arayüz native denemesi bekliyor.

Kullanıcı önceki komutlar ve diğer uyarlamalar çalışıyor beyanından sonra son
Dolphin düzeltmesini de onayladı ve devam istedi. Deltarune mevcut görünüm/kullanım
kapısı kapanır; önceki Plague Tale onayı korunur. Ayrı PAM/sensör ölçümü üretilmez.
Fotoğraflı seçici istenmişti, fakat kullanıcı menünün yerini kendisi seçmek istiyor.

`theme.sh menu`, repo içinden ayrı QuickShell FloatingWindow açar. Yerleşim/global
kısayol atamaz ve payload/skin/ABI'ye dosya eklemez. Böylece kurulu 2.9 üstüne yalnız
git pull ile denenir; ana shell'in stop/start işleminde seçici hedef süreç olmaz.
QuickShell 0.3.1 Process/FloatingWindow/shellPath ve --no-duplicate kaynakları
kontrol edildi. Normal close busy helper'ı öldürmez; helper tamamlanınca çıkar.

Python JSON köprüsü yalnız katalog ve mevcut Engine check/apply/rollback çağırır.
Yeni dosya-kopyalama/restore veya theme hook yolu yoktur. Katalog paket/PNG bütünlüğünü
core ile doğrular, bozuk kartı pasifleştirir. Check sonucu yalnız aynı seçim için
geçerlidir; apply core kontrollerini kilit altında tekrarlar. Geri dönüş ikinci
onay ister. Hata sonrası katalog gerçek aktif/pending kayıtlarını tekrar okur.

PickerState saf Qt etkileşim modelidir; PickerView/Card/Button sunumdur. Native
shell.qml yalnız Process JSON taşımasını ve pencere yaşam döngüsünü bağlar. İki
fotoğraf mevcut gerçek Qt render'larıdır; görsel üretim veya harici varlık alınmadı.
Kaydırılabilir gövde ve sabit işlem alanı dar pencerede uygulanır.

Ayrı Dolphin/Spotify/SDDM/terminal kurucuları bu ilk arayüze gizlice eklenmez.
Uygulama kapatma, root izni ve ilk yedek sınırları UI'da görünürdür. Tek tıkla
bütün harici uygulamaların taşınması iddiası yoktur. İleride karar verilirse aynı
kurucular açık seçim/sonuçla bağlanabilir. Menü konumu hâlâ kullanıcı kararıdır.
