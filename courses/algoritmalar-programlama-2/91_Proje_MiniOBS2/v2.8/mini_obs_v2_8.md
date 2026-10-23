# Mini-OBS 2 v2.8 — Yığın ve Kuyruk: geri al / yinele ve ders kayıt kuyruğu (Hafta 9)

**Bu sürümün amacı:** Hafta 9'un iki soyut veri tipini Mini-OBS'nin iki gerçek ihtiyacına uygulamak. (1) **Geri al / yinele** — kayıt ekle, sil, güncelle ve v2.7'nin ders kaydı işlemleri (kaydol, bırak) **iki yığınla** geri alınır ve yinelenir: her işlem bir *işlem kaydı* (komut türü + işlemden önceki ve sonraki kayıt kopyası + listedeki konum) bırakır; yeni bir işlem yinele yığınını boşaltır; geri al geçmişi en çok 100 kayıt tutar ve sınır aşılınca **en eski kayıt bırakılır** (yığın iki uçlu dairesel tampondur). Bırakmanın geri alınması otomatik aktarmayı da geri alır: aktarılan öğrenci bekleme listesinin **başına** döner. (2) **Ders kayıt kuyruğu** — kayıt günü simülasyonunda istekler **FIFO** işlenir (dairesel tampon; kuyruk doluysa istek reddedilir), kontenjanı dolu derse gelen kayıt v2.7'nin bekleme listesine düşer; ortak LCG ve tamsayı zamanla gişe sayısının ve geliş hızının etkisi ölçülür. Ölçüm (§ 8): 10⁵ işlemde geri al işlem başına 0,81 µs, yinele 0,73 µs — işlemin kendisiyle (0,68 µs) aynı mertebe; geçmiş belleği işlem başına ≈ 287 bayttır ve sınırla O(sınır)'da kalır (sınır 100: 31 520 bayt). Simülasyonda 2 gişe ile 5 000 istekten 1 601'i kuyruk dolu olduğu için reddedilir (ortalama bekleme 183,43 s), 4 gişe ile hiçbiri (0,89 s).

Dosyalar (satır sayılarıyla): **`kuyruk.h`** (71) · **`kuyruk.c`** (102) · **`geri_al.h`** (150) · **`geri_al.c`** (431) · **`kayit_gunu.c`** (340) · `kayit.c` (575) · `bekleme.h` (106) · `bekleme.c` (209) · `dosya.h` (114) · `dosya.c` (561) · `olcer_yapi.c` (953) · `test_obs.c` (2317) · `test_kahin.c` (3700) · `Makefile` (518) · `ornek_veri/islem_komutlari.txt`, `testler/islem_hatali.txt` · önceki sürümlerin bütün dosyaları · `olcum/gecmis.csv`, `olcum/gecmis_sinir.csv`, `olcum/fifo.csv`, `olcum/kayit_gunu.csv`, `olcum/kayit_gunu_kuyruk.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_8_ciktilar.txt` (1277 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_8_yiginlar.png`, `mini_obs_v2_8_halka.png`; grafik: `mini_obs_v2_8_olcum.png`.

Derleme: `make` (önceki programlar + **`kayit_gunu`**; `kayit` genişletildi), `make test`, `make olcum` (bu makinede 16 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 40 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0; 1 (dosya okunamadı, bellek yetersiz, hatalı komut satırı; testlerde uyuşmazlık); 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 9 yığını (LIFO) ve kuyruğu (FIFO) **soyut veri tipi** olarak, arayüzü gerçekleştirimden ayırarak ele alır. Mini-OBS'de ikisi de doğal olarak ortaya çıkar:

- **Yığın — geri al / yinele** (Konu: "Uygulamalar: geri al/yinele, tarayıcı geri tuşu"): son yapılan işlem ilk geri alınır. İki yığınla (geri, yinele) *geri al ∘ işlem = kimlik* ve *yinele ∘ geri al = işlem* özdeşlikleri kurulur ve kâhin testi bunları her adımda bütün tablonun anlık görüntüsüyle sınar (§ 4.2, § 9).
- **Dairesel tampon ve dolu/boş ayrımı** (ÖÇ 9.2): sabit kapasiteli kuyruk baş indisi ve öğe sayısıyla tutulur; hiçbir işlem öğe kaydırmaz (v2.7'nin kaydırmalı dizisiyle karşılaştırma: § 8.2). Aynı yapı iki **taşma politikasıyla** kullanılır (Mühendis Gözüyle): kayıt kuyruğunda **reddet**, geri al geçmişinde **en eskinin üzerine yaz** (§ 4.1).
- **Kuyruk simülasyonu** (ÖÇ 9.5; atölye: "gişe sayısının ortalama beklemeye etkisi"): kayıt günü, ortak LCG ile deterministik olarak canlandırılır; ρ = λ·E[S]/G ≥ 1 olduğunda kuyruğun dolduğu ölçülür (§ 4.3, § 8.3).
- **ADT ve arayüz** (ÖÇ 9.1): `kuyruk.h` öğe türünü bilmez (öğe boyutu parametredir); aynı arayüz kayıt isteklerini değer olarak, işlem kayıtlarını işaretçi olarak saklar.

Yol haritasındaki karşılığı (Tablo A.1): **H9 · v2.8 · Geri al/yinele; ders kayıt kuyruğu · Yığın, kuyruk.**

## 2. v2.7'den ne değişti?

| Konu | v2.7 (H8) | v2.8 (H9) |
|---|---|---|
| Dairesel tampon | — | **`kuyruk.h/.c`**: sabit kapasiteli, iki uçlu (sona ekle, baştan al, sondan al, i. öğe); dolu/boş sayaçla; sarma sayacı; öğe türünden bağımsız |
| Geri al / yinele | — | **`geri_al.h/.c`**: `IslemKaydi` (tür + önce/sonra kopyası + konum + aktarılan), `Gecmis` (iki yığın, sınır, düşürülen, bellek); `islem_ekle/sil/guncelle/kaydol/birak`, `geri_al`, `yinele` ve alt adımları |
| Bekleme listesi | sona ekle, baştan çıkar, sil, sıra | + `bekleme_basa_ekle`, `bekleme_konuma_ekle` (geri almada aktarmanın ve vazgeçmenin tersi) |
| `kayit` | kaydol, birak, sira, kontenjan, durum | + `ekle`, `sil`, `guncelle`, `goster`, **`geri`**, **`yinele`**, `gecmis`; `--sinir` (varsayılan 100); kontenjan değişikliği geçmişi temizler |
| Simülasyon | — | **`kayit_gunu`**: FIFO istek kuyruğu (dairesel tampon, reddet), G gişe, 14 ders × kontenjan, bekleme listeleri, otomatik aktarma; `--csv` |
| Dosya modülü | — | `csv_satiri_ayristir` (dosyadaki kurallarla tek satır; `ekle` komutu) |
| Ölçüm | `olcer_yapi` (v2.7 işlemleri) | + `fifo_halka`, `gecmis_kayitsiz/islem/geri/yinele/sinirli`; CSV'de `parametre`, `bellek_bayt`, `dusurulen` |
| Testler | 324 birim; kâhin 446 295 denetim | 353 birim (+29 yığın-kuyruk); kâhin 502 819 denetim; `--hata-goster dolu`, `--hata-goster yinele` |

Menü (`mini_obs`) değişmedi; v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır. v2.7'nin kayıt oturumu aynı sonucu verir; özet satırına yalnızca geri al / yinele sayıları eklendi.

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `kuyruk` (**yeni**) | iki uçlu dairesel tampon (öğe boyutu parametre) | yok (öğe türünü bilmez) |
| `geri_al` (**yeni**) | işlem kayıtları, iki yığın, tersler, sınır, bellek muhasebesi | `kuyruk`, `kontenjan`, `obs`, `arama` (sıralı ekleme, ikili arama) |
| `bekleme` | + başa ve konuma ekleme | — |
| `kayit.c` | + kayıt işlemleri ve geçmiş komutları | + `geri_al` |
| `kayit_gunu.c` (**yeni**) | kayıt günü simülasyonu | `kuyruk`, `kontenjan`, `secmeli` (ders havuzu), `uretec` |
| `olcer_yapi.c` | + dairesel tampon ve geçmiş ölçümleri | + `kuyruk`, `geri_al` |
| diğerleri | v2.7'den aynen | — |

`kuyruk.o` ve `geri_al.o` `YAPI` grubuna eklendi. Geçmiş, sınıfı (`Sinif`) ve dersi (`DersKontenjani`) **değiştirmek için** parametre alır ama onlara sahip olmaz; yalnızca kendi kayıtlarının sahibidir (§ 5).

## 4. Algoritmalar ve veri yapıları

### 4.1 Dairesel tampon

![Dairesel tampon](mini_obs_v2_8_halka.png)

*Şekil 1. Kapasite 4'lük dairesel tampon (birim testindeki örnek): (a) 1, 2, 3, 4 eklendi — dolu; (b) 1 baştan alındı, 5 sona eklendi: yazma indisi 3'ten 0'a sardı. İçerik baştan sona 2 3 4 5'tir.*

```
algoritma SONA-EKLE(q, x)                       ▷ O(1)
    eğer q.n = q.kapasite ise false döndür       ▷ dolu: REDDET (kuyruk değişmez)
    q.tampon[(q.bas + q.n) mod q.kapasite] ← x;  q.n ← q.n + 1
algoritma BAŞTAN-AL(q) → x                       ▷ O(1)
    eğer q.n = 0 ise false döndür                ▷ boş
    x ← q.tampon[q.bas];  q.bas ← (q.bas + 1) mod q.kapasite;  q.n ← q.n − 1
algoritma SONDAN-AL(q) → x                       ▷ O(1): yığın kullanımı
    x ← q.tampon[(q.bas + q.n − 1) mod q.kapasite];  q.n ← q.n − 1
```

- **Dolu mu, boş mu?** Yalnız baş ve son indisleri tutulursa `bas == son` hem boş hem dolu kuyruğu gösterir; çözüm ya bir hücreyi hep boş bırakmak ya da öğe sayısını tutmaktır. Burada sayaç tutulur: kapasitenin tamamı kullanılır, boş ⇔ n = 0, dolu ⇔ n = kapasite. İki çözümü karıştırmak (sayaçlı yapıda "dolu ⇔ n = kapasite − 1") `--hata-goster dolu`'nun kasıtlı hatasıdır (§ 9).
- **Mod işlemi:** 0 ≤ bas + i < 2·kapasite olduğundan mod tek bir çıkarmayla hesaplanır; kapasite 2'nin kuvveti seçilirse `& (kapasite − 1)` bit maskesi de kullanılabilir (Kaputun Altında, H9).
- **İki uçlu kullanım ve iki politika:** kayıt kuyruğu sona ekler, baştan alır ve **doluysa reddeder**; geri al geçmişi sona ekler (it), sondan alır (çek) ve doluysa **baştan alıp bırakır** (en eskinin üzerine yazar). Böylece sınırlı bir yığın da O(1) kalır: en eski kaydı düşürmek için dizinin kaydırılması gerekmez.
- **Sarma sayacı** yazma indisinin halkanın sonundan başına kaç kez döndüğünü sayar (simülasyon çıktısında görünür; testlerde sınır durumu).

### 4.2 Geri al / yinele: iki yığın

![İki yığın](mini_obs_v2_8_yiginlar.png)

*Şekil 2. Örnek oturumun (§ 6.1) iki yığını: (a) beş kayıt isteği ve bir bırakmadan sonra; (b) `geri` — bırakma geri alındı, kaydı yinele yığınına geçti; (c) oturumun sonunda yeni bir işlem (kaydol …051) yapıldığı için yinele yığını boşaltılmış. Yığın içerikleri komut dosyasından izlenir ve programın `gecmis` çıktısıyla karşılaştırılır.*

```
algoritma İŞLEM(op)                              ▷ ekle, sil, güncelle, kaydol, bırak
    kayıt ← (tür, numara, önceki kopya, sonraki kopya, konum, aktarılan)   ▷ önce ayrılır
    op'u uygula;  durum değişmediyse kaydı bırak ve dön
    yinele yığınını BOŞALT (kayıtları bırak)
    geri yığını doluysa EN ESKİ kaydı baştan al ve bırak (düşürülen + 1)
    geri yığınına it(kayıt)
algoritma GERİ-AL                                ▷ geri al ∘ işlem = kimlik
    kayıt ← geri yığınından çek;  yoksa "geri alınacak işlem yok"
    kaydın TERSİNİ uygula;  yinele yığınına it(kayıt)
algoritma YİNELE                                 ▷ yinele ∘ geri al = işlem
    kayıt ← yinele yığınından çek;  yoksa "yinelenecek işlem yok"
    işlemi aynı girdiyle YENİDEN uygula (durum aynı → sonuç aynı; denetlenir);  geri yığınına it(kayıt)
```

| İşlem | Kayıtta tutulan | Tersi (geri al) |
|---|---|---|
| ekle | sonraki kopya | numaradaki kaydı sil |
| sil | önceki kopya | önceki kopyayı sıralı ekle (numara sırası aynı konumu verir) |
| güncelle | önceki ve sonraki kopya, ders | kaydın üzerine önceki kopyayı yaz |
| kaydol (KABUL / BEKLEME) | sonuç | kayıtlı listenin / bekleme listesinin SONUNDAN sil |
| bırak (kayıtlıdan) | konum, aktarılan | bırakanı eski konumuna ekle; aktarılanı kayıtlı listenin sonundan alıp bekleme listesinin BAŞINA koy |
| bırak (bekleyenden) | konum | bekleme listesinde eski konumuna ekle (`bekleme_konuma_ekle`, `Node **`) |

- **"Sondan sil" neden doğru?** Geri al LIFO'dur: bir işlem geri alınırken ondan sonraki bütün işlemler zaten geri alınmıştır, yani durum işlemden hemen sonraki durumla aynıdır. Kayıtlı listeye son eklenen öğrenci listenin sonundadır, aktarılan öğrenci de öyle. Tersler bunu ön koşul olarak **denetler**; tutmazsa geri alma reddedilir ve kayıt geri yığınına döner.
- **Geri alınamayanlar:** durum değiştirmeyen istekler (ZATEN, RET) kaydedilmez. Kontenjan değişikliği geri alınamaz; `kayit` onu uygularken geçmişi temizler ve bunu yazar (tasarım kararı 4).
- **Bellek:** kayıt `sizeof(IslemKaydi)` = 56 bayt (x86-64 LP64) + kopya başına `sizeof(Ogrenci)` = 144 bayt: ders işlemleri 56, ekle ve sil 200, güncelle 344 bayt (ayırıcının yönetim yükü hariç). Geçmiş en çok `sinir` kayıt tuttuğundan bellek O(sınır)'dır (§ 8.1).

### 4.3 Kayıt günü simülasyonu

```
algoritma KAYIT-GÜNÜ(istekler, G gişe, C kapasite)     ▷ zaman t = 0, 1, 2, … (saniye)
    t'de gelen her istek: kuyruğa SONA-EKLE; dolu ise REDDET
    her boş gişe g (sırayla): kuyruk boş değilse
        x ← BAŞTAN-AL;  bekleme ← t − x.geliş;  g, t + hizmet(3..9 s) anına kadar meşgul
        x kayıt isteğiyse: ders_kaydol → KABUL | BEKLEME (bekleme listesinin sonu) | ZATEN
        x bırakma isteğiyse: ders_birak → (kayıtlıdan çıktıysa) bekleme listesinin başı OTOMATİK aktarılır
    bütün istekler geldi ve kuyruk boşaldı ise dur
```

İstekler önceden üretilir (ortak LCG, tohum + 100): ardışık iki geliş arası [0, 2A] aralığında düzgün (ortalama A s); isteklerin %10'u bırakma; kayıt isteğinde ders "popüler önde" seçilir (iki düzgün indisin küçüğü). Hizmet süreleri ayrı bir alt akıştan (tohum + 101) hizmet başlarken çekilir. Böylece aynı parametreler bayt bayt aynı çıktıyı verir. Yük oranı ρ = λ·E[S]/G (λ = 1/A istek/s, E[S] = 6 s): ρ < 1 iken kuyruk kısa kalır, ρ ≥ 1 iken dolar ve istekler reddedilir.

### 4.4 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `kuyruk_sona_ekle`, `kuyruk_bastan_al`, `kuyruk_sondan_al`, `kuyruk_oge` | düz dizi modeli (kapasite 1..9, kaydırmalı); her adımda dönüş, değer, n, dolu/boş ve bütün içerik |
| `islem_*`, `geri_al`, `yinele` | **anlık görüntü dizisi** S₀, S₁, …: her adımda bütün tablo (kayıtlar + kayıtlı liste + bekleme listesi) beklenen görüntüyle bayt bayt aynı; yeni işlem S[p+1..]'i atar; sınır 1..15 (en eskinin düşmesi); geri ve yinele yığınlarının boyları; bellek muhasebesi; ders değişmezi |
| `kayit_gunu` | dersin değişmezi her derste (`ders_gecerli_mi`); sonuçlar deterministik (aynı tohum, aynı çıktı) |

## 5. Bellek sahipliği

| Yapı | Kim ayırır | Kim serbest bırakır | Yaşam süresi |
|---|---|---|---|
| `Kuyruk.tampon` (kapasite × öğe boyutu) | `kuyruk_olustur` | `kuyruk_yok_et` | kuyruk boyunca; öğeler işaretçiyse gösterdikleri KULLANANINDIR |
| `IslemKaydi` + `once`/`sonra` kopyaları | `islem_*` (kayıt işlemden ÖNCE ayrılır: bellek yoksa işlem yapılmaz) | geçmiş: sınır aşılınca en eski (`gecmis_geri_it`), yeni işlemde yinele yığınının hepsi, `gecmis_temizle`, `gecmis_yok_et` (hepsi `islem_kaydi_birak` ile) | işlemden düşürülmeye ya da geçmişin sonuna; kayıt yığınlar arasında TAŞINIR, kopyalanmaz |
| `Gecmis` (iki tampon) | `gecmis_olustur` | `gecmis_yok_et` | oturum boyunca |
| `kayit_gunu`: istek dizisi, ders dizisi, gişe dizisi, başarılı kayıt listesi | `main` | `main` sonunda (her ders `ders_yok_et`) | simülasyon boyunca |
| önceki sürümlerin yapıları | v2.7 § 5 | v2.7 § 5 | — |

Kopyalar sınıftaki kayıttan bağımsızdır: kayıt silinse de geçmişteki kopya geçerlidir (sarkan işaretçi yoktur). Ayıran her fonksiyonun yorumunda sahiplik sözleşmesi vardır; kayıt ve kopyaları işlemden önce ayrıldığı için bellek yetmezliği yarım bir durum bırakmaz. `make asan` (yeni programlar ve kasıtlı hata kipleri dahil) temiz; `make valgrind` 35 çalıştırmanın hepsinde "ERROR SUMMARY: 0 errors" ve "definitely lost: 0 bytes":

```
valgrind ./obs_test_vg → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 20 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 2 --hata-goster bas → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 2 --hata-goster cakisma → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 2 --hata-goster dolu → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 5 --hata-goster yinele → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./kayit_vg ornek_veri/ogrenciler.csv --komutlar ornek_veri/islem_komutlari.txt → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./kayit_vg ornek_veri/ogrenciler.csv --sinir 2 --komutlar ornek_veri/islem_komutlari.txt → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./kayit_gunu_vg --istek 2000 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./kayit_gunu_vg --gise 1 --kuyruk 1 --istek 300 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg gecmis_geri --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg gecmis_yinele --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg gecmis_sinirli --n 300 --k 7 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg fifo_halka --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./kayit_vg ornek_veri/ogrenciler.csv --kontenjan 3 --komutlar ornek_veri/kayit_komutlari.txt → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./kayit_vg ornek_veri/ogrenciler.csv --komutlar testler/kayit_hatali.txt → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./birlestir_vg ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv --yontem liste --denetle → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./birlestir_vg ornek_veri/ogrenciler.csv testler/sube_cakisma.csv --yontem liste --denetle → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg sil_liste_dagin --n 1,2,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg sira_liste_dagin --n 1,2,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg fifo_liste --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg buyume_p10 --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg buyume_p1_elle --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg dolas_liste_dagin --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./dagilim_vg ornek_veri/ogrenciler.csv --liste 5 --denetle → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ilk_k_vg ornek_veri/ogrenciler.csv --k 3 --denetle → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./birlestir_vg ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv ornek_veri/sube_c.csv → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ortanca_vg ornek_veri/ogrenciler.csv --denetle → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./listele_vg testler/kararlilik.csv --yontem hepsi → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ara_vg ornek_veri/ogrenciler.csv --soyad yıl → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_sec_vg --alt 18 --ust 20 --yontem hepsi → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./denetle_vg testler/yinelenen_k3.csv → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./veri_uret_vg --n 500 --cikti vg.csv → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_vg kiyas_birlestirmeli --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./mini_obs_vg oturum.csv → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
```

## 6. Kullanım

### 6.1 `kayit`: işlemler ve geçmiş

```
./kayit ogrenciler.csv|.dat [--ders KOD] [--kontenjan K] [--sinir S] [--komutlar dosya.txt]
  kaydol NO | birak NO | sira NO | kontenjan K | durum
  ekle NO;AD;SOYAD;ALG_v;ALG_f;MAT_v;MAT_f;FIZ_v;FIZ_f | sil NO | guncelle NO ALG|MAT|FIZ VIZE FINAL | goster NO
  geri | yinele | gecmis
```

```
$ ./kayit ornek_veri/ogrenciler.csv --komutlar ornek_veri/islem_komutlari.txt
Ders: BIL331 · kontenjan 3 · öğrenciler: ornek_veri/ogrenciler.csv (8 kayıt) · geri al sınırı 100
> kaydol 2301010045
  KABUL: 2301010045 AYŞE NUR YILMAZ · kayıtlı 1/3
> kaydol 2301010048
  KABUL: 2301010048 CAN YILMAZ · kayıtlı 2/3
> kaydol 2301010050
  KABUL: 2301010050 EMRE ÇINAR · kayıtlı 3/3
> kaydol 2301010046
  BEKLEME: 2301010046 MEHMET ALİ KAYA · kontenjan dolu (3/3) · bekleme sırası 1
> kaydol 2301010047
  BEKLEME: 2301010047 İSMAİL ÖZTÜRK · kontenjan dolu (3/3) · bekleme sırası 2
> birak 2301010048
  BIRAKTI: 2301010048 CAN YILMAZ (kayıtlı listede 2. idi)
  AKTARMA: 2301010046 MEHMET ALİ KAYA bekleme listesinin başından kayıtlı listeye · kayıtlı 3/3 · bekleyen 1
> geri
  GERİ ALINDI: birak 2301010048 · kayıtlı listede 2. sıraya döndü; 2301010046 MEHMET ALİ KAYA bekleme listesinin başına döndü · geri 5, yinele 1
> durum
  Kayıtlı (3/3):
     1) 2301010045 AYŞE NUR YILMAZ
     2) 2301010048 CAN YILMAZ
     3) 2301010050 EMRE ÇINAR
  Bekleme listesi (2):
     1) 2301010046 MEHMET ALİ KAYA
     2) 2301010047 İSMAİL ÖZTÜRK
> yinele
  YİNELENDİ: birak 2301010048 · yeniden bıraktı (kayıtlı listede 2. idi); aktarma: 2301010046 MEHMET ALİ KAYA · geri 6, yinele 0
> guncelle 2301010052 ALG 60 70
  GÜNCELLENDİ: 2301010052 ILGAZ ŞAHİN · ALG vize 30.00 final 40.00 → vize 60.00 final 70.00 · ortalama 36.00 → 66.00
> geri
  GERİ ALINDI: guncelle 2301010052 ALG · ALG vize 30.00 final 40.00 (ortalama 36.00) · geri 6, yinele 1
> goster 2301010052
Öğrenci no  : 2301010052
Ad Soyad    : ILGAZ ŞAHİN
Algoritma ve Prog. I   36.00  FF  BAŞARISIZ (final barajı)
Matematik I            86.80  BA  BAŞARILI
Fizik I                77.00  BB  BAŞARILI
YANO        : 2.12
> ekle 2301010060;Deniz;Arslan;80;85;70;75;90;95
  EKLENDİ: 2301010060 DENİZ ARSLAN · sıra 9 · kayıt sayısı 9
> sil 2301010049
  SİLİNDİ: 2301010049 ZEYNEP ÇELİK · kayıt sayısı 8
> sil 2301010045
  RET: 2301010045 AYŞE NUR YILMAZ derste (kayıtlı ya da bekliyor): önce birak
> gecmis
  Geçmiş: geri 8 (sınır 100) · yinele 0 · düşürülen 0 · bellek 736 bayt (tepe 736)
  geri   tepesi: sil 2301010049 (200 B) · ekle 2301010060 (200 B) · birak 2301010048 (56 B) · kaydol 2301010047 (56 B) · kaydol 2301010046 (56 B) · …
  yinele tepesi: —
> geri
  GERİ ALINDI: sil 2301010049 · kayıt geri geldi · geri 7, yinele 1
> geri
  GERİ ALINDI: ekle 2301010060 · kayıt silindi · geri 6, yinele 2
> yinele
  YİNELENDİ: ekle 2301010060 · kayıt yeniden eklendi · geri 7, yinele 1
> kaydol 2301010051
  BEKLEME: 2301010051 ŞULE DOĞAN · kontenjan dolu (3/3) · bekleme sırası 2
> yinele
  YİNELENECEK İŞLEM YOK
> gecmis
  Geçmiş: geri 8 (sınır 100) · yinele 0 · düşürülen 0 · bellek 592 bayt (tepe 736)
  geri   tepesi: kaydol 2301010051 (56 B) · ekle 2301010060 (200 B) · birak 2301010048 (56 B) · kaydol 2301010047 (56 B) · kaydol 2301010046 (56 B) · …
  yinele tepesi: —
> durum
  Kayıtlı (3/3):
     1) 2301010045 AYŞE NUR YILMAZ
     2) 2301010050 EMRE ÇINAR
     3) 2301010046 MEHMET ALİ KAYA
  Bekleme listesi (2):
     1) 2301010047 İSMAİL ÖZTÜRK
     2) 2301010051 ŞULE DOĞAN
Özet: 23 komut · kabul 3 · bekleme 3 · aktarma 1 · bırakma 1 · ret 1 · hata 0 · geri al 4 · yinele 2 · son durum: kayıtlı 3/3, bekleyen 2, kayıt 9
[çıkış kodu: 0]
```

Sınır 2 ile aynı oturumda geri yığınında en çok iki kayıt kalır (6 kayıt düşürülür). Hatalı komutlar satır numarasıyla bildirilir:

```
$ cat testler/islem_hatali.txt; ./kayit ornek_veri/ogrenciler.csv --komutlar testler/islem_hatali.txt
# hatalı işlem komutları: her biri satır numarasıyla bildirilir, oturum sürer
ekle 2301010061;Deniz;Arslan;80;85
ekle 2301010061;Deniz;Arslan;180;85;70;75;90;95
guncelle 2301010045 KIM 50 50
guncelle 2301010045 ALG 50
ekle 2301010045;Ayşe;Nur;1;1;1;1;1;1
sil 2301010099
geri
geri
yinele
Ders: BIL331 · kontenjan 3 · öğrenciler: ornek_veri/ogrenciler.csv (8 kayıt) · geri al sınırı 100
> ekle 2301010061;Deniz;Arslan;80;85
  HATA: kayıt satırı geçersiz (NO;AD;SOYAD;ALG_v;ALG_f;MAT_v;MAT_f;FIZ_v;FIZ_f)
> ekle 2301010061;Deniz;Arslan;180;85;70;75;90;95
  HATA: kayıt satırı geçersiz (NO;AD;SOYAD;ALG_v;ALG_f;MAT_v;MAT_f;FIZ_v;FIZ_f)
> guncelle 2301010045 KIM 50 50
  HATA: guncelle NO ALG|MAT|FIZ VIZE FINAL (notlar 0..100)
> guncelle 2301010045 ALG 50
  HATA: guncelle NO ALG|MAT|FIZ VIZE FINAL (notlar 0..100)
> ekle 2301010045;Ayşe;Nur;1;1;1;1;1;1
  RET: 2301010045 zaten kayıtlı
> sil 2301010099
  RET: 2301010099 numaralı öğrenci yok
> geri
  GERİ ALINACAK İŞLEM YOK
> geri
  GERİ ALINACAK İŞLEM YOK
> yinele
  YİNELENECEK İŞLEM YOK
Özet: 9 komut · kabul 0 · bekleme 0 · aktarma 0 · bırakma 0 · ret 2 · hata 4 · geri al 0 · yinele 0 · son durum: kayıtlı 0/3, bekleyen 0, kayıt 8
[çıkış kodu: 1]
```

### 6.2 `kayit_gunu`

```
./kayit_gunu [ogrenciler.csv] [--ogrenci N] [--dersler D.csv] [--kontenjan K] [--istek N] [--birakma Y]
             [--gise G] [--kuyruk C] [--gelis A] [--hizmet MIN,MAX] [--tohum T] [--csv dosya [--ekle]]
```

```
$ ./kayit_gunu
Kayıt günü simülasyonu · tohum 42 · 2000 öğrenci · 14 ders × kontenjan 20 · 5000 istek (%10 bırakma)
Gişe 2 · kuyruk kapasitesi 64 (dairesel tampon) · geliş aralığı ortalama 2 s (0..4) · hizmet 3..9 s
İstekler          : 5000 (kayıt 3064, bırakma 335 işlendi)
Kuyruk dolu: ret  : 1601
İşlenen           : 3399
  kayıt   → kabul 310 · bekleme listesi 2541 · zaten 213
  bırakma → kayıtlıdan 114 (otomatik aktarma 76) · bekleyenden 178 · derste yok 43
Kuyrukta bekleme  : ortalama 183.43 s · en uzun 214 s · en uzun kuyruk 64 · sarma 53
Bitiş             : 10219 s · gişe doluluğu %99.9
Ders        kontenjan  kayıtlı  bekleyen
BIL331             20       20       340
BIL333             20       20       287
BIL335             20       20       270
BIL337             20       20       265
BIL339             20       20       219
BIL341             20       20       213
BIL343             20       20       178
BIL345             20       20       170
BIL347             20       20       121
BIL349             20       20       100
BIL351             20       20        52
BIL353             20       20        47
BIL355             20       20        25
BIL357             20       12         0
toplam            280      272      2287
[çıkış kodu: 0]
```

## 7. Tasarım kararları

1. **Yığın = iki uçlu dairesel tampon.** Sınırlı geçmişte en eski kaydı düşürmek bağlı listeyle ya da kaydırmalı diziyle de yapılabilirdi; dairesel tamponda üç işlem de (it, çek, en eskiyi düşür) O(1)'dir ve düğüm ayırma yoktur. Aynı modül kayıt kuyruğunu da taşır.
2. **Komut kaydı (önce/sonra kopyası), anlık görüntü değil.** Her işlemden sonra bütün tabloyu kopyalamak O(n) bellek ve zaman ister; kayıt yalnız değişen kaydı (en çok iki kopya) tutar. Anlık görüntü yalnızca **kâhinde** kullanılır (doğruluğu apaçık, yavaş).
3. **Yinele, işlemi yeniden çalıştırır.** Ters işlem kaydı gerektirmez: durum işlemden önceki durumla aynı olduğu için sonuç da aynıdır; yine de sonuç kayıttakiyle karşılaştırılır (iç tutarlılık denetimi).
4. **Kontenjan değişikliği geçmişi temizler.** Kontenjan artırımı birden çok aktarma yapar; tersini kaydetmek değişken uzunlukta bir kayıt gerektirirdi. Bunun yerine değişiklik, kullanıcıya yazılarak geri alınamaz kabul edilir.
5. **Derste olan öğrenci silinemez.** Kayıt ile ders listesi arasındaki tutarlılık `sil`'i reddederek korunur (önce `birak`); böylece silmenin tersi ders listelerine dokunmaz.
6. **Simülasyonda zaman adımlı döngü.** Olay kuyruğu (öncelik kuyruğu, H7'nin öbeği) yerine saniye saniye ilerlemek kodu kısaltır; istek sayısı × ortalama aralık kadar adım vardır (bu iş yükünde ≈ 10⁴), maliyeti önemsizdir. İstekler ve hizmet süreleri ayrı LCG alt akışlarından gelir: gişe sayısını değiştirmek istekleri değiştirmez.

## 8. Ölçümler

**Düzen:** `-O2`; her nokta için önce sayaç açık bir çalıştırma, sonra 1 ısınma + 5 tekrar, ortanca; kurma adımı (başlangıç sınıfının kopyası, gerekirse işlemlerin ve geri almaların ön uygulaması) süre dışında. Simülasyon sonuçları süre değil sayıdır (deterministik). Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB, L3 33 MiB; gcc 13.3.0, glibc 2.39; tarih 2026-10-13 15:16. `make olcum` 16 s sürdü. Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 1,38, sonda 1,52 idi (2 çekirdek; aynı anda başka ajanların derleme ve ölçümleri çalışıyordu: süreler gürültülüdür, sayaçlar ve simülasyon sonuçları değildir).

![Ölçümler](mini_obs_v2_8_olcum.png)

*Şekil 3. Üstte kayıt günü simülasyonu (5 000 istek; kuyruk 64): ortalama bekleme (log) ve reddedilen istek, gişe sayısına karşı. Altta FIFO'nun üç yapıda süresi (log–log) ve geri al sınırının geçmiş belleğine etkisi (log–log).*

### 8.1 Geri al / yinele: süre ve bellek

İş yükü: 1 000 kayıtlık sınıfta n işlemlik akış (%20 ekle, %20 sil, %60 güncelle; hedefler o anda var olan kayıtlardan), önceden üretilir.

| n işlem | kaydetmeden (µs/işlem) | kaydederek | geri al | yinele | geçmiş belleği (bayt) | bayt / işlem |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 0,709 | 0,624 | 0,558 | 0,768 | 286 112 | 286,1 |
| 10 000 | 0,506 | 0,607 | 0,488 | 0,487 | 2 863 280 | 286,3 |
| 100 000 | 0,681 | 0,805 | 0,808 | 0,734 | 28 660 160 | 286,6 |

*Tablo 1. İşlem başına süre ve geçmiş belleği (`olcum/gecmis.csv`). Kontrol (son sınıfın sağlaması) kaydederek ve kaydetmeden aynıdır; n işlemin hepsi geri alınınca başlangıç sınıfının sağlaması (674266000) elde edilir, yinelenince yine işlemlerinki.*

- **Geri al ≈ işlem.** Ekleme ve silmenin tersi yine bir sıralı ekleme/silmedir (1 000 kayıtlık dizide kaydırma, Θ(n)); güncellemenin tersi bir ikili arama ve bir kayıt kopyasıdır. 10⁵ işlemde geri al 0,81 µs, yinele 0,73 µs, kaydetmeden işlem 0,68 µs. Kaydetmenin ek maliyeti (kayıt + 1–2 kopya için `malloc`) bu ölçümde %18'dir; yığın işlemlerinin kendisi O(1)'dir.
- **Bellek = kayıt kopyası boyutu × işlem sayısı.** Sınırsız geçmişte bellek n ile doğrusal büyür: işlem başına ≈ 286,6 bayt (karışımın beklenen değeri 0,2·200 + 0,2·200 + 0,6·344 = 286,4 bayt). Sınır bunu O(sınır)'a indirir:

| sınır (10⁵ işlem) | geçmiş belleği, tepe (bayt) | düşürülen kayıt | süre (işlemler + geri al) |
|--:|--:|--:|--:|
| 10 | 3 440 | 99 990 | 103,4 ms |
| 100 | 31 520 | 99 900 | 86,3 ms |
| 1 000 | 294 464 | 99 000 | 81,3 ms |
| 10 000 | 2 882 432 | 90 000 | 114,2 ms |
| 100 000 | 28 660 160 | 0 | 176,7 ms |

*Tablo 2. 10⁵ işlem, farklı sınırlar (`olcum/gecmis_sinir.csv`): geçmiş belleğinin tepesi ≈ sınır × 287 bayt; düşürülen = n − sınır. Sınır 10⁵'te bütün işlemler geri alınır ve başlangıç sınıfına dönülür.*

### 8.2 FIFO: kaydırmalı dizi, bağlı liste, dairesel tampon

| n (ekle + çıkar) | dizi (kaydırmalı) | bağlı liste | dairesel tampon | liste / tampon | dizi / tampon |
|--:|--:|--:|--:|--:|--:|
| 1 000 | 56,1 µs | 39,3 µs | 25,0 µs | 1,57 | 2,25 |
| 10 000 | 6,7 ms | 263,2 µs | 218,3 µs | 1,21 | 31 |
| 100 000 | 805,9 ms | 2,9 ms | 2,3 ms | 1,26 | 356 |
| 1 000 000 | — | 34,5 ms | 22,7 ms | 1,52 | — |

*Tablo 3. n sona ekleme + n baştan çıkarma (`olcum/fifo.csv`). Dairesel tampon da bağlı liste de O(1)'dir; tampon düğüm başına `malloc`/`free` yapmadığı ve bitişik olduğu için 10⁶'da listeden 1,52 kat hızlıdır. Kaydırmalı dizi Θ(n²)'dir (v2.7 § 8).*

### 8.3 Kayıt günü simülasyonu

| geliş aralığı (s) | gişe | ρ = λ·E[S]/G | ret (kuyruk dolu) | işlenen | ort. bekleme (s) | en uzun (s) | en uzun kuyruk | gişe doluluğu |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 2 | 1 | 3,00 | 3 269 | 1 731 | 373,09 | 425 | 64 | %100,0 |
| 2 | 2 | 1,50 | 1 601 | 3 399 | 183,43 | 214 | 64 | %99,9 |
| 2 | 3 | 1,00 | 14 | 4 986 | 53,98 | 138 | 64 | %98,9 |
| 2 | 4 | 0,75 | 0 | 5 000 | 0,89 | 15 | 10 | %74,9 |
| 3 | 1 | 2,00 | 2 462 | 2 538 | 374,64 | 429 | 64 | %100,0 |
| 3 | 2 | 1,00 | 35 | 4 965 | 110,18 | 208 | 64 | %99,6 |
| 3 | 3 | 0,67 | 0 | 5 000 | 0,84 | 16 | 7 | %67,2 |
| 3 | 4 | 0,50 | 0 | 5 000 | 0,18 | 9 | 6 | %50,4 |
| 4 | 1 | 1,50 | 1 578 | 3 422 | 371,17 | 428 | 64 | %100,0 |
| 4 | 2 | 0,75 | 0 | 5 000 | 1,70 | 19 | 7 | %74,6 |
| 4 | 3 | 0,50 | 0 | 5 000 | 0,20 | 10 | 6 | %49,7 |
| 4 | 4 | 0,38 | 0 | 5 000 | 0,04 | 5 | 4 | %37,3 |

*Tablo 4. 5 000 istek, kuyruk kapasitesi 64, hizmet 3..9 s, 14 ders × kontenjan 20 (`olcum/kayit_gunu.csv`). ρ, istek akışının gişe kapasitesine oranıdır.*

| kuyruk kapasitesi | ret | ort. bekleme (s) | en uzun bekleme (s) | en uzun kuyruk | sarma |
|--:|--:|--:|--:|--:|--:|
| 4 | 352 | 2,83 | 13 | 4 | 1 161 |
| 16 | 93 | 14,75 | 39 | 16 | 306 |
| 64 | 14 | 53,98 | 138 | 64 | 77 |
| 256 | 0 | 61,33 | 156 | 78 | 19 |
| 1 024 | 0 | 61,33 | 156 | 78 | 4 |

*Tablo 5. Kuyruk kapasitesinin etkisi: 3 gişe, geliş aralığı 2 s (ρ = 1,00) (`olcum/kayit_gunu_kuyruk.csv`).*

**Yorum.** ρ > 1 iken (ör. 1 gişe) kuyruk hemen dolar, istekler reddedilir ve kuyruktakiler kapasite × ortalama hizmet / G kadar bekler: kuyruk sınırı bekleme süresini de sınırlar. ρ < 1 iken bekleme saniyelere iner (geliş aralığı 2 s, 4 gişe: ρ = 0,75, ortalama 0,89 s). ρ = 1 sınırında küçük kuyruk istekleri reddeder ama bekleme kısalır; büyük kuyruk reddetmez ama bekleme uzar (Tablo 5) — **taşma politikası bir ödünleşimdir** (reddet ↔ beklet). Kontenjan bütün senaryolarda aynı darboğazdır (14 ders × 20 = 280 yer): istek reddedilmeyen bütün senaryolarda doğrudan kabul sayısı 315'tir (bırakmayla boşalan bir yere bekleme listesi boşken gelen istek de doğrudan kabul edilir); kalan kayıt istekleri bekleme listelerine düşer ve kayıtlıdan bırakmalar otomatik aktarma üretir. Sayılar birbirini tutar: son kayıtlı = kabul + aktarma − kayıtlıdan bırakma (varsayılan senaryo: 310 + 76 − 114 = 272).

### 8.4 Sınırlılıklar

Süreler paylaşılan bir sanal makinede, yük altında ölçüldü (yukarıda); sayaçlar, bellek baytları ve simülasyon sonuçları makineden bağımsızdır. Geçmiş belleği ayırıcının yönetim yükünü içermez. Simülasyon modeli basittir (düzgün geliş aralığı ve hizmet süresi, tek kuyruk, sabırsız müşteri yok); kuyruk kuramının Poisson modelleriyle doğrudan karşılaştırılmamalıdır.

## 9. Testler

- **Birim testleri** (`obs_test`): `353 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama + 23 böl-fethet + 19 öbek-doğrusal + 79 bağlı liste + 29 yığın-kuyruk`. Yığın-kuyruk testleri: dairesel tampon (geçersiz kapasite; boşta alma; dolunca reddetme ve kuyruğun değişmemesi; sarma; i. öğe; sondan alma; 10 turluk dönüşte sarma sayısı; kapasite 1); geçmiş: boş geçmişte geri al/yinele; ekle → geri al → yinele (bayt bayt aynı sınıf); mükerrer eklemenin kaydedilmemesi; güncelle ve geri alınması; yeni işlemde yinele yığınının boşalması; silmenin aynı konuma dönmesi; temizleme ve bellek; ders kaydı: ZATEN'in kaydedilmemesi, bırakmanın geri alınmasında aktarılanın bekleme listesinin başına dönmesi, bekleyenden bırakmanın eski konuma dönmesi; derste olanın silinememesi; sınır 3'te 5 işlem: 2 düşürülen, 3 geri al; kayıt boyutu ve tanımı; CSV satırı ayrıştırıcısı.
- **Kâhin testleri** (`test_kahin`): 300 denemede 502 819, 1 000 denemede 1 667 035 denetim (dairesel tampon ve geçmiş: 188 358), uyuşmazlık yok.
- **Kasıtlı hatalar.** (a) `--hata-goster dolu` — sayaçlı tamponda "dolu ⇔ n = kapasite − 1"; kâhin uyuşmazlığı bulur ve kapasite 1..3, 3 işleme kadar bütün diziler denenerek en kısa karşı örnek basılır (kapasite 1, 1 işlem: `sona_ekle(1)`):

```
$ ./test_kahin --hata-goster dolu
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : dairesel tampon (kuyruk.h)
  n          : 265
  Beklenen   : düz dizi modeli (kapasite 6): 65. işlem sona_ekle
  Bulunan    : dönüş false/-1 (beklenen true/-1)
  En kısa karşı örnek (kapasite 1, 1 işlem): sona_ekle(1) → dönüş false/-1 (beklenen true/-1)
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster dolu
[çıkış kodu: 1]
```

  (b) `--hata-goster yinele` — geri alınan kayıt yinele yığınına itilmiyor; anlık görüntü dizisinin ilk denetimi yığın boylarında yakalar:

```
$ ./test_kahin --hata-goster yinele
KÂHİN UYUŞMAZLIĞI (tohum 3)
  İşlev      : geri_al / yinele
  n          : 148
  Beklenen   : anlık görüntüler (sınır 14): 6. adım geri
  Bulunan    : yığınlar: geri 0, yinele 0 (beklenen 0, 1)
  Yeniden üretmek için: ./test_kahin --tohum 3 --deneme 1 --hata-goster yinele
[çıkış kodu: 1]
```

## 10. Ders notu için özet (Hafta 9 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'ye iki yığınla **geri al / yinele** ekliyoruz: kayıt ekle, sil, güncelle ve geçen haftanın ders kaydı işlemleri (kaydol, bırak) geri alınabilir ve yinelenebilir. Ders kayıt günü için **FIFO istek kuyruğunu dairesel tamponla** kuruyor, kontenjanı dolu derse gelen isteği geçen haftanın bekleme listesine düşürüyor ve ortak LCG ile bir **kayıt günü simülasyonu** yapıyoruz.

### Gereksinimler

- `kuyruk.h/.c`: sabit kapasiteli dairesel tampon — `kuyruk_olustur`, `kuyruk_sona_ekle` (doluysa false: reddet), `kuyruk_bastan_al`, `kuyruk_sondan_al`, `kuyruk_bos_mu`, `kuyruk_dolu_mu`, `kuyruk_yok_et`; dolu/boş ayrımı **sayaçla**; hiçbir işlem öğe kaydırmaz.
- `geri_al.h/.c`: `IslemKaydi` (tür, numara, `Ogrenci *once`, `Ogrenci *sonra`, konum, aktarılan) ve `Gecmis` (geri ve yinele yığınları, sınır); `islem_ekle`, `islem_sil`, `islem_guncelle`, `islem_kaydol`, `islem_birak` (uygula + kaydet; **yeni işlem yinele yığınını boşaltır**); `geri_al`, `yinele`; sınır aşılınca **en eski kayıt bırakılır** (varsayılan 100).
- Bekleme listesine `bekleme_basa_ekle` ve `bekleme_konuma_ekle` (geri almada kullanılır).
- `kayit` programına `ekle`, `sil`, `guncelle`, `goster`, `geri`, `yinele`, `gecmis` komutları ve `--sinir`.
- `kayit_gunu` programı: N istek, G gişe, kapasitesi C olan istek kuyruğu (doluysa ret), tamsayı zaman; çıktı: istek, ret, kabul, bekleme listesi, otomatik aktarma, ortalama ve en uzun bekleme, en uzun kuyruk; deterministik.
- Testler: geri al ∘ işlem = kimlik ve yinele ∘ geri al = işlem, **rastgele işlem dizileriyle**, her adımda bütün tablonun anlık görüntüsüyle karşılaştırarak; kuyruk sarma ve dolu/boş sınırları.
- Ölçüm: geri al/yinele süresi (işlem başına) ve bellek tüketimi (kayıt kopyası boyutu × işlem sayısı; sınırla); simülasyon sonuçları tablosu (en az gişe sayısı × geliş aralığı).

### İpuçları

- Kuyrukta yalnız `bas` ve `n` tutun; son konum `(bas + n) % kapasite`'dir. "Dolu" `n == kapasite`, "boş" `n == 0`.
- Geri al yığınında en eski kaydı düşürmek için yığını **iki uçlu** kullanın: itme ve çekme sondan, düşürme baştan.
- İşlem kaydını işlemden **önce** ayırın: bellek yoksa işlem hiç yapılmasın (yarım durum kalmasın).
- Silmenin tersi için kaydın **kopyasını** saklayın (işaretçisini değil): sınıf dizisi `realloc` ile taşınabilir, silinen kaydın yeri başkası tarafından kullanılabilir.
- Bırakmanın tersini kâğıtta çizin: bırakan eski konumuna, aktarılan öğrenci bekleme listesinin **başına** döner. Sıra önemlidir: önce bellek isteyen adım (diziye ekleme), sonra diğerleri.
- Yeni işlemde yinele yığınındaki kayıtları **serbest bırakmayı** unutmayın (yalnızca sayacı sıfırlamak sızıntıdır; Valgrind "definitely lost" der).
- Kâhin için her adımın sonunda bütün tablonun kopyasını bir diziye koyun: geri al bir önceki kopyaya, yinele bir sonrakine eşit olmalıdır.
- Simülasyonda istekleri ve hizmet sürelerini ayrı tohumlu alt akışlardan üretin: gişe sayısını değiştirmek istek dizisini değiştirmesin.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri ve `test_kahin` (300 deneme) geçer.
2. Kapasite 4'lük kuyrukta 1, 2, 3, 4 eklenince `kuyruk_dolu_mu` doğru ve 5 reddedilir; 1 baştan alınıp 5 eklenince içerik baştan sona 2 3 4 5 olur ve sarma sayısı 1'dir; kapasite 1'lik kuyruğa bir öğe girer.
3. `./kayit ornek_veri/ogrenciler.csv --komutlar ornek_veri/islem_komutlari.txt` şu satırı basar: `GERİ ALINDI: birak 2301010048 · kayıtlı listede 2. sıraya döndü; 2301010046 MEHMET ALİ KAYA bekleme listesinin başına döndü · geri 5, yinele 1`; özet satırı: `Özet: 23 komut · kabul 3 · bekleme 3 · aktarma 1 · bırakma 1 · ret 1 · hata 0 · geri al 4 · yinele 2 · son durum: kayıtlı 3/3, bekleyen 2, kayıt 9`; çıkış 0.
4. Aynı oturumda `kaydol 2301010051`'den sonraki `yinele` "YİNELENECEK İŞLEM YOK" der (yeni işlem yinele yığınını boşalttı).
5. `--sinir 2` ile aynı oturumda `gecmis` "geri 2 (sınır 2)" ve "düşürülen 6" gösterir.
6. Güncellemenin geri alınması kaydı bayt bayt eski hâline döndürür (`goster` aynı ortalamaları ve harf notlarını basar).
7. `./kayit_gunu` (varsayılanlar: 2 gişe, kuyruk 64, geliş aralığı 2 s) `Kuyruk dolu: ret  : 1601` ve `Kuyrukta bekleme  : ortalama 183.43 s` satırlarını basar; `--gise 4` ile ret 0; aynı parametrelerle iki çalıştırma bayt bayt aynıdır.
8. `./test_kahin --hata-goster dolu` ve `--hata-goster yinele` uyuşmazlık basar ve 1 ile çıkar; `make asan` ve `make valgrind` temizdir.
9. Ölçüm raporunda geri al ve yinele işlem başına süresi ölçülür (bu makinede 10⁵ işlemde 0,81 µs ve 0,73 µs) ve geçmiş belleği sınırla O(sınır)'da kalır (sınır 100: 31 520 bayt).

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | kapasite 4: ekle 1..4, ekle 5 | 5 reddedilir; kuyruk değişmez |
| 2 | baştan al, ekle 5, sondan al | 1; sarma 1; 5; içerik 2 3 4 |
| 3 | boş kuyrukta baştan/sondan al | false |
| 4 | ekle (yeni numara) → geri → yinele | kayıt yok olur, sonra aynı konuma geri gelir |
| 5 | güncelle → geri | eski not ve ortalama (bayt bayt) |
| 6 | sil → geri | kayıt aynı sıraya döner |
| 7 | geri → yeni işlem → yinele | "YİNELENECEK İŞLEM YOK" |
| 8 | kontenjan 2: kaydol A, B, C; birak A; geri | kayıtlı A B; C bekleme listesinin başında |
| 9 | bekleyen B, C; birak B; geri | B bekleme listesinde yine 1. sırada |
| 10 | sınır 3: 5 güncelleme, 5 kez geri | 3 geri al başarılı, 4.'sü "yok"; düşürülen 2 |
| 11 | kaydol (ZATEN) | geçmişe kayıt eklenmez |
| 12 | `kayit_gunu --gise 1 --kuyruk 4` | ret > 0; en uzun kuyruk 4; sarma > 0 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.7'niz (ya da referans v2.7), `kuyruk.h`, `geri_al.h` (bildirimler, tersler tablosu, sahiplik), `ornek_veri/islem_komutlari.txt`, `kayit_gunu`'nun model açıklaması ve istek üretimi (tohumlar), `olcer_yapi`'nın geçmiş ölçüm düzeneği.
- **Yazılır:** `kuyruk.c`, `geri_al.c`, `bekleme.c`'ye iki ekleme, `kayit.c`'ye yeni komutlar, `kayit_gunu.c`'nin simülasyon döngüsü; testler (birim + anlık görüntülü kâhin); ölçüm ve yorum.
- **Değiştirilmez:** v1.0 kuralları ve menü, kayıt dizisinin numara sırası, v2.7'nin kontenjan kuralları, ortak modüller.
- **Meydan okuma:** (a) `Kuyruk`'u opak tip yapın (başlıkta yalnız `typedef struct Kuyruk Kuyruk;`); (b) kontenjan değişikliğini de geri alınabilir yapın (aktarılanların listesi kayıtta); (c) simülasyonu olay güdümlü yazın (gişe bitiş anları H7'nin öbeğinde) ve zaman adımlı sürümle aynı sonucu verdiğini gösterin; (d) "geri al" yerine anlık görüntü tutan sürümü yazın, bellek ve süresini ölçüp komut kaydıyla karşılaştırın.

## 11. Bilinen sınırlılıklar

- Kontenjan değişikliği geri alınamaz (geçmiş temizlenir); dosyaya kaydetme `kayit`'te yoktur (oturum bellekte; menü programı kaydeder).
- Geri al geçmişi tek bir ders içindir; çok dersli kayıt (simülasyondaki gibi) geri alınmaz.
- Simülasyon zaman adımlıdır: çok büyük geliş aralıklarında adım sayısı artar (olay güdümlü sürüm meydan okumadadır).
- Geçmiş belleği sayımı ayırıcı yükünü içermez; süreler yük altında ölçüldü.

## 12. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Knuth, D. E. (1997). *The art of computer programming: Vol. 1. Fundamental algorithms* (3rd ed.). Addison-Wesley.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
