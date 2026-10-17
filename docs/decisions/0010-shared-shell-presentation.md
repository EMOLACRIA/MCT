# ADR-0010 — Shell sunumunu ortak kaynaklara bağlama

Tarih: 2026-10-17. Durum: **2.6.0 uygulandı; hedef oturum kabulü bekliyor**.

## Gerekçe

2.5.1 yerleşim denetimi sonrasında saat/tray/panel sınırları çalışıyordu; buna
rağmen shell/preview bar ve OSD ölçüleri ayrıydı. Başlık/kapatma yedi kez,
bildirim eylemi toast ve geçmişte ayrı yazılmıştı. Toast'taki uzun eylem geçmişteki
genişlik düzeltmesini almamıştı. Qt varsayılan açık tooltip paleti de görsel dilden
ayrılıyordu. Bunlar gelecekte özelliklerin temalar arasında ayrışması için somut
çoğaltma noktalarıydı.

## Karar

- Theme.qml shell QML literal paleti, font aileleri, varlık URL'leri ve açık görsel
  animasyon sürelerinin kaynağıdır. Mevcut ana renk değerleri korunur.
- SurfaceLayout saf Qt singleton'ıdır: panel türü ölçü/merkez varsayılanı ve sınır
  hesabı; bar/OSD/toast/Alt+Tab dış ölçüleri. Native pencere ve preview aynı kaynağı
  kullanır. Yeni QuickShell API'si veya tercih şeması yoktur.
- PanelHeader yedi panelde başlık/ikon/ek eylem/close sunar; parent UiState eylemini
  bağlar. Başlık ikonları 26, kapatma alanı 36 mantıksal pikselde ortaklaşır.
- NotificationActions aynı key/id backend çağrısını iki bildirim yüzeyinde sunar;
  uzun butonlar her iki yerde de sığar. ToastStack native ve preview'de paylaşılır.
- SurfaceHint koyu palet/font ve sınırlı genişlikte sarılan metin kullanır.
  ActionButton hint property sunar; workspace/tray aynı ipucu görünümünü kullanır.

Bildirim yaşam süresi, IPC adı, MRU, tercih kalıcılığı veya uygulama komutları
tema token'larına taşınmaz. Yeni tema yükleme/switch UI'si ve dış uygulama palet
üreticisi eklenmez. Yerel vektör/kart yerleşimi bileşen içinde kalır.

## Doğrulama ve sonuç

9 gerçek Qt yerleşim testi: önceki dar alan/uzun içerik kontrollerine yedi ortak
başlığın kapatması, Controls ↔ Settings ve preview toast eylemi/kapatma/arka planda
gizlenmesi eklendi. Yeni tipler qmldir'e kayıtlıdır; network import testi eksik
manifest ve Theme dışı palette literal'lerini denetler. Mevcut ayar/launcher/
Alt+Tab/OSD kontrolleri ve 35 QML bytecode derlemesi geçti.

Palet ve dış ölçü değerleri korunurken başlık alanı standartlaştı; bu tam piksel
eşitliği iddiası değildir. Qt software render örnekleri incelendi. Native
Wayland tooltip/toast, gerçek bar reserve ve yeniden başlatmada kalıcılık hâlâ
kullanıcı oturumu kontrolüdür. Harici adaptör/eksik kabul haritası
[THEME_SURFACES](../THEME_SURFACES.md) içindedir; M3/M4 kapısı açık kalır.
