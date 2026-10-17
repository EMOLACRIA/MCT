# ADR-0003 — Shell süreçlerini tam profil seçicisiyle tanı

Tarih: 2026-10-17. Durum: uygulandı; hedef oturum kabulü bekliyor.

## Sorun

Eski HyprCADE profilinin `/home/emo/...` yoluyla tanınması farklı kullanıcı veya
kurulum konumunda çalışmaz. Komut satırında yalnızca profil yolunu aramak ise
aynı yolu hedefleyen QuickShell IPC istemcisini çalışan shell sanabilir.

## Karar

- `qs`/`quickshell` başlatmasındaki tek `-p/--path` veya `-c/--config` seçicisini
  çözümle. IPC, list, log, kill, msg ve yardım/sürüm komutlarını dışarıda bırak.
- Mutlak dosya yollarını normalize et; profil dizini ve `shell.qml` aynı profili
  tanımlasın. Eksik, göreli veya birden fazla seçiciye göre süreç durdurma.
- Eski profil için mevcut HOME/XDG altında gerçekten bulunan HyprCade profili
  veya ilk yedeğin kaydettiği tam seçici kullanılabilir. Benzer adlı dizinleri
  ya da bütün QuickShell süreçlerini sahiplenme.
- İlk kurulumun süreç yedeği ve süreç durdurma aynı sınıflandırmayı kullansın.
  Restore kayıtlı komutları açsın; süreç listesi olmayan eski kayıtta shell yolu
  tahmin etmesin.

## Sınırlar ve doğrulama

İlk kurulumda bu standart konumlar dışında başlatılmış, henüz kayda alınmamış
bir eski profil otomatik keşfedilmez. İlgisiz bir shell'i kapatmamak için bu
durumda kullanıcı tarafından açık konum uyarlaması gerekir.

`checks/test_session_discovery.py` içindeki 10 kontrollü test; HOME/XDG,
taşınmış/symlink profil, eski kayıt, IPC ayrımı, seçilen PID'ler ve restore
davranışını denetler. Gerçek süreçlere sinyal gönderilmez. Native oturum sonucu
ayrıca [STATUS.md](../../STATUS.md) içinde kaydedilir.
