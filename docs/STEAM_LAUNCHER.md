# Steam launcher etiketleri — 0.1.0

Launcher Steam girdilerini masaüstü id/command metadata'sından ayırır:
Steam (Native) ve Steam (Flatpak). İkon, id, execute ve oyun adları korunur.
Native veya flatpak arayarak filtreleyebilirsin. Aktif tema değiştirilmez.

```bash
unzip -o ~/Downloads/MCT-launcher-steam-0.1.0.zip -d ~/Downloads &&
python3 ~/Downloads/MCT-launcher-steam-0.1.0/install.py ~/newfolder/desktop-style
```

Kaynak ve kurulu ortak QML doğrulanır; native compile sonrası yalnız MCT shell
stop/start edilir. İlk restore yedeği korunur; hata önceki dosyalara döner.
Kişisel kaynak değişikliği varsa hiçbir hedef yazılmaz. update.sh gerekmez.

## GitHub kaydı

Hazırlama dalı ulaşılabilen Snowgrave/Fastfetch kaynaklarını içerir. Adventure ve
Guardian tam paketleri bu hazırlama checkout'unda yoktur; cihazdaki beş temanın
üstüne bu dalı checkout etme. Küçük kurucuyu uyguladıktan sonra cihazdaki tam
kaynak ağacını kaydetmek için aşağıdakini çalıştır (normal kaynaklar; log/hesap/
bağımlılık/yedek dosyalarını ekleme):

```bash
cd ~/newfolder/desktop-style &&
git add -A -- payload themes apps sddm terminal-medallion docs checks \
  PROJECT_BRIEF.txt STATUS.md ROADMAP.md adapter_assets.py \
  theme.sh theme_core.py theme_integrations.py fastfetch_quotes.py fastfetch-quotes &&
(git diff --cached --quiet || git commit -m "Save five themes and Steam launcher labels") &&
git push -u origin HEAD
```

Push tamamlanmadan cihazdaki beş temanın tamamı GitHub'da kayıtlı sayılmaz.
