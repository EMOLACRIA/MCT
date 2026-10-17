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

## 2.6.1 düzeltme — native bar ipucu

17 Ekim kullanıcı ipucunun düğmeyi örttüğünü bildirdi. 2.6.0 offscreen sahnesi tam
ekran olduğu için 48 px native bar penceresinde Qt ToolTip clamp sorununu
yakalamamıştı. Gecikme de açıkça tanımlanmamıştı. PR #9 aynı dalda düzeltildi.

SurfaceHint artık Item tabanlı 600 ms bekleme/iptal modelidir; basılı düğmede veya
ayrılmada ipucu kapanır, başka owner için süre baştan başlar. HintBubble görünümü
native bar ve Qt fallback paylaşır. shell.qml, bar ActionButton/workspace/tray
hint'lerine HintPopup component'ini geçirir; Loader yalnız gösterilirken yaratır.
Native popup target'a bağlanıp 8 px aşağıda açılır; yatay slide ekran kenarını
korur, boş Region maskesi click-through, grabFocus:false ToolTip pencere flag'i
sağlar. Panel/preview fallback focus/modal/etkileşim almaz; yer varsa aşağı,
yoksa yukarı konumlanır. Gecikme bir animasyon süresi değildir.

Birincil kaynaklar: QuickShell **v0.3.1**
[PopupWindow](https://quickshell.org/docs/v0.3.1/types/Quickshell/PopupWindow/),
[PopupAnchor](https://quickshell.org/docs/v0.3.1/types/Quickshell/PopupAnchor/),
[QsWindow.mask](https://quickshell.org/docs/v0.3.1/types/Quickshell/QsWindow/),
yerel aynı tag proxywindow.cpp/popupwindow.cpp ve
[Qt 6.8 Loader non-visual components](https://doc.qt.io/qt-6.8/qml-qtquick-loader.html).

12 Qt testi; 37 QML bytecode; 122 native binding ve input-mask/flag kaynak kontrolü
geçti. QtObject presenter fixture'ı Loader köprüsünü çalıştırır; gerçek Wayland
popup/click-through çalıştırılmış sayılmaz. Native son kabul yine açıktır.
