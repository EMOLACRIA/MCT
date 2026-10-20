## 20 Ekim — Steam launcher etiketleri 0.1.0

Kullanıcı Snowgrave görünümünü ve normal kullanımı onayladı; ayrı PAM/donanım ölçümü
raporlanmadı. Launcher Steam girdileri Steam (Native) ve Steam (Flatpak) olarak
ayrılır. Desktop ID/execute ve oyun kısayollarının adları değişmez. Native/flatpak
araması desteklenir. Ortak katmandır; tema paketleri, wallpaper, ilk restore noktası
ve çalışan Steam korunur. Node backend + 3 izole kurucu/geri alma kontrolü geçti.
Native QuickShell/Steam burada çalıştırılmadı; kurucu cihazda native QML ön kontrolü
yapıp yalnız MCT shell'i yeniden açar.
