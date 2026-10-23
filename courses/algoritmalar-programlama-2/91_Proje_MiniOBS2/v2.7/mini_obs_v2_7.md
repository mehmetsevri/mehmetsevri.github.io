# Mini-OBS 2 v2.7 — Dinamik Dizi ve Bağlı Liste: bekleme listesi, bağlı listede birleştirme ve bellek sahipliği (Hafta 8)

**Bu sürümün amacı:** Mini-OBS'ye ilk **bağlı yapıyı** eklemek ve "bağlı liste her zaman daha mı hızlıdır?" sorusunu ölçerek yanıtlamak. (1) **Bekleme listesi** — kontenjanı dolu derse kaydolmak isteyen öğrenciler tek bağlı listenin sonuna **kuyruk işaretçisiyle O(1)**'de eklenir; kayıtlı biri bırakınca açılan yer listenin **başındakine otomatik aktarılır** (baştan çıkarma, O(1)); bekleyen biri vazgeçerse **numarayla silinir** (`BeklemeDugumu **` ile, baş düğüm özel durum olmadan). (2) **Bağlı listede birleştirme** — iki şubenin sıralı kayıt listeleri **kukla düğümle, düğüm taşımadan** birleşir: v2.5'in dizi birleştirmesiyle aynı sonuç ve aynı karşılaştırma sayısı, ama 14 kayıt kopyası yerine 0 (örnek veride). (3) **Dinamik dizinin büyüme politikası** (× 2, `realloc` geçici işaretçiyle) belgelendi ve **kopyalama sayacı** eklendi. (4) Bütün yapıların bellek **sahipliği** bir tabloyla yazıldı (§ 5) ve **ASan + UBSan + LSan** ile **Valgrind**'de sızıntısız doğrulandı (`make valgrind`: 25 çalıştırmanın 25'ünde "ERROR SUMMARY: 0 errors", "definitely lost: 0 bytes"). Ölçümün dürüst sonucu (§ 8): **kuyruk davranışında liste kazanır** (10⁵ işlemde dizi 761,0 ms, liste 3,1 ms: 247 kat), **arama gerektiren işlemlerde dizi kazanır** — numarayla silmede dizi her silmede kalanları kaydırdığı hâlde n = 32 000'de bitişik listeden 4,5, düğümleri bellekte dağınık listeden 15,4 kat hızlıdır (Stroustrup, 2014).

Dosyalar (satır sayılarıyla): **`dinamik.h`** (86) · **`dinamik.c`** (124) · **`bekleme.h`** (94) · **`bekleme.c`** (162) · **`kontenjan.h`** (90) · **`kontenjan.c`** (156) · **`kayit_listesi.h`** (72) · **`kayit_listesi.c`** (109) · **`kayit.c`** (307) · **`olcer_yapi.c`** (669) · **`valgrind_denetle.sh`** (36) · `sayac.h` (55) · `sayac.c` (25) · `obs.h` (145) · `obs.c` (691) · `birlestir.c` (332) · `test_obs.c` (2094) · `test_kahin.c` (3302) · `Makefile` (469) · `ornek_veri/kayit_komutlari.txt`, `testler/kayit_hatali.txt` · önceki sürümlerin bütün dosyaları (değişmeden) · `olcum/bekleme.csv`, `olcum/dolasma.csv`, `olcum/buyume.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_7_ciktilar.txt` (1408 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_7_bekleme.png`, `mini_obs_v2_7_birlestir.png`; grafikler: `mini_obs_v2_7_olcum.png`, `mini_obs_v2_7_olcum_buyume.png`.

Derleme: `make` (`mini_obs`, `veri_uret`, `olcer`, `denetle`, `ders_sec`, `ara`, `listele`, `ortanca`, `birlestir`, `dagilim`, `ilk_k`, **`kayit`**, **`olcer_yapi`**), `make test`, `make olcum` (bu makinede 2 dakika 39 s), `make ornek`, `make asan`, **`make valgrind`** (v2.7'den itibaren zorunlu), `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 37 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0; 1 (dosya okunamadı, bellek yetersiz, hatalı komut satırı, şubelerde çakışma, kâhin uyuşmazlığı; testlerde uyuşmazlık); 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 8'in Büyük Sorusu — *bir dizinin ortasına eleman eklemek için bağlı liste her zaman daha mı hızlıdır?* — Mini-OBS'de somut bir soruya dönüşür: kontenjanı dolu bir dersin bekleme listesini dizide mi, bağlı listede mi tutmalıyız? Kuram, bağlı listenin baştan çıkarmada (O(1) ↔ Θ(n)) kazandığını söyler; ama numarayla silme ve sıra sorgusu iki yapıda da önce **aramadır** (Θ(n)), ve arama bitişik bellekte çok daha ucuzdur. Bu sürüm iki yapıyı **aynı iş yüküyle** ölçer (§ 8) ve haftanın öğrenme çıktılarını projeye bağlar:

- **Dinamik dizi ve amortize analiz** (ÖÇ 8.1): kayıt dizisinin (`Sinif`) ve dersin kayıtlı listesinin (`NoDizisi`) kapasitesi × 2 büyür; kopyalama sayacı n ekleme için toplam kopyanın < 2n olduğunu (toplam yöntemi), + 1 ve + 10 politikalarının ise Θ(n²) olduğunu **birebir** gösterir (§ 4.1).
- **Tek bağlı liste, kuyruk işaretçisi, `Node **`** (ÖÇ 8.2): bekleme listesi sona ekleme, baştan çıkarma, numarayla silme ve sıra sorgusu; baş ve son düğüm sınır durumları (§ 4.2, Şekil 1).
- **Kukla düğüm ve iki sıralı listenin birleştirilmesi** (ÖÇ 8.3): şube listeleri düğümleri yeniden bağlanarak birleşir (§ 4.4, Şekil 2).
- **Dizi ↔ liste deneyi** (ÖÇ 8.4): FIFO, numarayla silme, sıra sorgusu ve tek dolaşma; düğümlerin bellek yerleşimi (bitişik ↔ dağınık) ayrı bir değişken olarak (§ 8).
- **Bellek sahipliği ve araçlar** (ÖÇ 8.5): kim ayırır, kim serbest bırakır (§ 5); ASan/UBSan/LSan ve Valgrind bütün testlerde temiz; iki **kasıtlı hata** (`--hata-goster bas`, `--hata-goster cakisma`) kâhinle yakalanır (§ 9).

Yol haritasındaki karşılığı (Tablo A.1): **H8 · v2.7 · Bekleme listesi; sıralı listelerin birleştirilmesi · Bağlı liste, bellek sahipliği.**

## 2. v2.6'dan ne değişti?

| Konu | v2.6 (H7) | v2.7 (H8) |
|---|---|---|
| Dinamik dizi | `Sinif` × 2 büyür (belgelenmemiş) | **`dinamik.h/.c`**: `NoDizisi` (dört büyüme politikası, kopyalama ve büyütme sayaçları, `realloc` geçici işaretçiyle); `sinif_ekle_say` (kayıt dizisinin kopyalama sayacı; davranış aynı) |
| Bekleme listesi | — | **`bekleme.h/.c`**: tek bağlı liste + kuyruk işaretçisi; `bekleme_sona_ekle`, `bekleme_bastan_cikar`, `bekleme_sil` (`BeklemeDugumu **`), `bekleme_sira`, `bekleme_yok_et`, `bekleme_gecerli_mi` |
| Kontenjan | — | **`kontenjan.h/.c`**: `DersKontenjani` (kayıtlı dizi + bekleme listesi), `ders_kaydol`, `ders_birak` (otomatik aktarma), `ders_kontenjan_ayarla` |
| Bağlı listede birleştirme | dizi (`sube_birlestir`) | **`kayit_listesi.h/.c`**: kayıtların bağlı listesi, `kayit_listeleri_birlestir` (kukla düğüm, taşıma 0); `birlestir --yontem liste --denetle` |
| Program | — | **`kayit`**: komut güdümlü kayıt (`kaydol`, `birak`, `sira`, `kontenjan`, `durum`) |
| Ölçüm | `olcer` (sıralamalar) | **`olcer_yapi`**: bekleme listesi dizi ↔ liste (bitişik/dağınık), tek dolaşma, büyüme politikaları; `--butce` ile işaretli kestirim; kurma adımı süre dışında |
| Sayaç | 4 alan | + **`baglanti`** (bağlantı değişikliği; yalnız sıfır değilse yazılır: eski çıktılar aynı) |
| Bellek denetimi | `make asan`; isteğe bağlı `make valgrind` | `make asan` + **zorunlu `make valgrind`** (sanitizer'sız `-O0 -g` ikililer, `--show-leak-kinds=all --error-exitcode=3`, `valgrind_denetle.sh` ölçütü) |
| Testler | 245 birim; kâhin 354 990 denetim | 324 birim (+79 bağlı liste); kâhin 446 295 denetim; `--hata-goster bas`, `--hata-goster cakisma` |

Menü (`mini_obs`) ve yükleyici değişmedi; v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır (regresyon, `mini_obs_v2_7_ciktilar.txt`).

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `dinamik` (**yeni**) | `long long` dinamik dizisi: ekle, sil, araya ekle, bul; büyüme politikası; kopyalama sayacı | yalnız `sayac` |
| `bekleme` (**yeni**) | bekleme listesi: tek bağlı liste + kuyruk işaretçisi | yalnız `sayac` (öğrenci kaydını bilmez: düğüm yalnız numara taşır) |
| `kontenjan` (**yeni**) | bir dersin kayıtlı ve bekleme listeleri, aktarma kuralı, değişmez denetimi | `dinamik`, `bekleme` |
| `kayit_listesi` (**yeni**) | kayıtların (144 bayt) bağlı listesi, kukla düğümle birleştirme | `obs`, `sayac` |
| `kayit.c` (**yeni**) | komut güdümlü kayıt oturumu | `kontenjan`, `arama` (öğrenci var mı: ikili arama), `dosya` |
| `olcer_yapi.c` (**yeni**) | dizi ↔ liste ölçüm düzeneği | `dinamik`, `bekleme`, `deney`, `ortak_rastgele` |
| `birlestir.c` | + `--yontem liste`, `--denetle` (kâhin: `sube_birlestir`) | + `kayit_listesi` |
| `obs` | + `sinif_ekle_say` | — |
| diğerleri | v2.6'dan aynen | — |

Yeni nesne dosyaları `YAPI` grubundadır (`dinamik.o bekleme.o kontenjan.o kayit_listesi.o`). Bekleme listesi öğrenci kaydını değil **numarasını** tutar: kayıt `Sinif`'te tek yerde kalır, liste yalnızca ona "işaret eder" (numarayla). Böylece aynı kayıt iki yapıda kopyalanmaz ve sahiplik basit kalır (§ 5).

## 4. Algoritmalar ve veri yapıları

### 4.1 Dinamik dizi: büyüme politikası ve kopyalama sayacı

Dizi dolunca (n = kapasite) yeni kapasite hesaplanır ve **tek `realloc`** yapılır. `realloc`'un sonucu **önce geçici işaretçiye** alınır: başarısızlıkta `NULL` döner ama eski blok serbest bırakılmaz; sonucu doğrudan `d->a`'ya atamak bloğun tek adresini kaybettirir (sızıntı) ve diziyi bozar (Hata Avcısı, H8).

```
algoritma SONA-EKLE(d, x)
    eğer d.n = d.kapasite ise
        yeni ← POLİTİKA(d.kapasite)                  ▷ × 2: 0 → 1 → 2 → 4 …
        g ← realloc(d.a, yeni)                        ▷ önce GEÇİCİ işaretçi
        eğer g = NULL ise false döndür                ▷ d.a hâlâ geçerli
        d.a ← g; d.kapasite ← yeni
        kopyalama ← kopyalama + d.n                   ▷ model: n öğe taşınır
    d.a[d.n] ← x; d.n ← d.n + 1
```

**Toplam yöntemi** (Cormen vd., 2022)**.** × 2 politikasında n ekleme boyunca büyütmeler 1, 2, 4, …, P/2 öğe kopyalar (P: n'den büyük ya da eşit en küçük 2'nin kuvveti); toplam P − 1 < 2n, yani ekleme başına **amortize O(1)**. + 1'de büyütme her eklemede olur: 0 + 1 + … + (n − 1) = n(n − 1)/2 = **Θ(n²)**; + 10 bunu yalnızca 10'a böler. Kopyalama sayacı bu kapalı biçimlerle **birebir** eşleşir (birim testi: 12 n × 4 politika; kâhin: rastgele ekle/sil dizileri). 10⁶ eklemede:

| politika (n = 10⁶) | realloc sayısı | kopyalama (model) | kopya / n | süre (realloc) | bloğu taşıyan büyütme |
|:--|--:|--:|--:|--:|--:|
| × 2 | 21 | 1 048 575 | 1,05 | 3,9 ms | 0 |
| × 1,5 | 35 | 2 099 753 | 2,10 | 3,1 ms | 0 |
| + 10 | 100 000 | 49 999 500 000 | 49 999,50 | 4,6 ms | 0 |
| + 1 | 1 000 000 | 499 999 500 000 | 499 999,50 | 17,3 ms | 0 |

*Tablo 1. Büyüme politikaları, n = 10⁶ sona ekleme (`olcum/buyume.csv`). "Kopyalama" modeldir (büyütmede eski n öğe); "bloğu taşıyan büyütme" `realloc`'un yeni adres döndürdüğü büyütmelerin sayısıdır (bu çalıştırmada; adres yazdırılmaz, yalnız karşılaştırılır).*

**Kaputun altında — model ile gerçek ayrışır.** Bu makinede (glibc 2.39) dört politikanın 1 222 272 `realloc` çağrısının 0'ı bloğu taşıdı. Olası açıklama: tek başına büyüyen dizi yığının (heap) sonunda durur ve `realloc` onu yerinde genişletebilir; glibc ayrıca çok büyük blokları `mmap` ile ayırıp `mremap` ile kopyasız büyütebilir. Bu yüzden + 1 politikasının 10⁶ eklemesi model kopyası 499 999 500 000 olduğu hâlde 17,3 ms sürdü. Kopyalamayı gerçekten yapan "yeni blok + kopya + eski bloğu bırak" sürümüyle (AP-1 H12'nin elle büyütmesi) aynı model sayısı süreye yansır: 10⁵ eklemede × 2 850,2 µs, + 1 3,69 s (4 338 kat; Tablo 2, Şekil 4). Ders: **× 2'nin güvencesi ayırıcıya bağlı değildir**; + 1'in "ucuzluğu" bu ayırıcının, bu iş yükündeki bir kolaylığıdır ve başka bir platformda (ör. başka ayırmalar araya girince) karesel maliyet geri gelir.

| n | × 2, realloc | + 1, realloc | × 2, yeni blok + kopya | + 1, yeni blok + kopya |
|--:|--:|--:|--:|--:|
| 1 000 | 2,4 µs | 22,3 µs | 1,0 µs | 104,5 µs |
| 10 000 | 21,6 µs | 161,3 µs | 52,7 µs | 18,7 ms |
| 100 000 | 215,6 µs | 1,8 ms | 850,2 µs | 3,69 s |
| 1 000 000 | 3,9 ms | 17,3 ms | 13,2 ms | 368,84 s *(kestirim)* |

*Tablo 2. `realloc`'lu büyütme ↔ "yeni blok + kopya" (ölçülen; "kestirim" işaretli satır ölçülmedi, T(n) ≈ T(n/10)·10² ile kestirildi).*

`Sinif`'in kendi büyütmesi (başlangıç 4, × 2) `sinif_ekle_say` ile sayılır: 10⁶ kayıtta 19 büyütme, 2 048 572 kayıt kopyası (10⁶ ekleme + 1 048 572 büyütme kopyası) — ekleme başına ≈ 2,05 kopya.

### 4.2 Bekleme listesi: tek bağlı liste + kuyruk işaretçisi

Bağlı liste, her düğümün bir sonrakinin adresini taşıdığı "bağlı ayırma"dır (Knuth, 1997): rastgele erişim yoktur, ama bir düğümün bağlantısını değiştirmek O(1)'dir.

![Bekleme listesi](mini_obs_v2_7_bekleme.png)

*Şekil 1. Örnek oturumun (§ 6.1) bekleme listesi: (a) kontenjan dolu, üç öğrenci bekliyor; (b) kayıtlı biri bırakınca açılan yer listenin başındakine verilir (baştan çıkarma); (c) bekleyen biri vazgeçer: numarayla silme. Silinen son düğüm olduğu için kuyruk işaretçisi (`son`) önceki düğüme çekilir. Liste içerikleri programın gerçek çıktısından okunur.*

```
algoritma SONA-EKLE(b, no)                        ▷ O(1): kuyruk işaretçisi sayesinde
    d ← yeni düğüm(no, sonraki = NULL)
    eğer b.son = NULL ise b.bas ← d değilse b.son.sonraki ← d
    b.son ← d; b.n ← b.n + 1
algoritma BAŞTAN-ÇIKAR(b) → no                    ▷ O(1)
    d ← b.bas; b.bas ← d.sonraki
    eğer b.bas = NULL ise b.son ← NULL             ▷ tek düğüm vardı
    no ← d.no; free(d)
algoritma SİL(b, no) → konum                      ▷ Θ(konum); bag: düğümü GÖSTEREN bağlantı
    bag ← &b.bas; önceki ← NULL
    *bag ≠ NULL oldukça:                            ▷ değişmez: geçilen düğümlerin hiçbiri no değil
        eğer (*bag).no = no ise
            silinen ← *bag; *bag ← silinen.sonraki   ▷ baş düğüm için de AYNI satır
            eğer silinen = b.son ise b.son ← önceki  ▷ kuyruk işaretçisi
            free(silinen); konum'u döndür
        önceki ← *bag; bag ← &(*bag).sonraki
    0 döndür
```

- **Değişmez** (`bekleme_gecerli_mi`; testler her adımda denetler): (1) `bas`'tan tam n düğüm dolaşılır, sonuncusunun `sonraki`'si `NULL`; (2) n = 0 ⇔ `bas` = `NULL` ⇔ `son` = `NULL`; (3) n > 0 ise `son` dolaşmadaki son düğümdür. En kolay bozulan (3)'tür: son düğüm silinince `son` güncellenmezse serbest bırakılmış düğümü gösterir ve sonraki sona ekleme **free sonrası kullanımdır** (ASan: heap-use-after-free).
- **`Node **` neden?** "Önceki" işaretçisiyle yazılan silmede baş düğüm ayrı bir durumdur (`b->bas` değişir); bunu unutmak, `--hata-goster bas`'ın kasıtlı hatasıdır (§ 9). `bag` ise düğümü gösteren bağlantının **adresi** olduğu için `*bag = silinen->sonraki` hem `b->bas`'ı hem bir düğümün `sonraki`'sini aynı satırla değiştirir. `onceki` yalnızca `son`'u güncellemek için tutulur.
- **Sayaçlar** (birim testinde birebir): sona ekleme 2 bağlantı, baştan çıkarma 1 (son düğümse 2), silme 1 (son düğümse 2) bağlantı ve konum kadar karşılaştırma; bulunamazsa n karşılaştırma.
- **Düğüm boyutu:** `sizeof(BeklemeDugumu)` = 16 bayt (x86-64 LP64: 8 baytlık numara + 8 baytlık işaretçi); bu makinede art arda ayrılan düğümler arasında ortalama 32 bayt vardır (ayırıcının yönetim yükü ve hizalama; `olcer_yapi`'nın stderr'i, "bu çalıştırmada"). Dizide aynı numara 8 bayttır: listenin bellek bedeli bu iş yükünde ≈ 4 kattır.

### 4.3 Kontenjanlı ders ve otomatik aktarma

`DersKontenjani` bir dersin iki listesini birlikte tutar: **kayıtlı** (dinamik dizi, kayıt sırasında) ve **bekleme** (§ 4.2). Kurallar:

```
algoritma KAYDOL(d, no)
    no kayıtlıysa ya da bekliyorsa: DEĞİŞİKLİK YOK      ▷ iki listede doğrusal arama
    kayıtlı sayısı < kontenjan ise: kayıtlı listenin SONUNA ekle → KABUL
    değilse: bekleme listesinin SONUNA ekle → BEKLEME
algoritma BIRAK(d, no)
    no kayıtlıysa: kayıtlı listeden sil (sıra korunur); AKTAR(d) → (en çok bir aktarma)
    değilse no bekliyorsa: bekleme listesinden numarayla sil
algoritma AKTAR(d)                                      ▷ kontenjan değişince de çağrılır
    kayıtlı sayısı < kontenjan ve bekleme boş değil oldukça:
        kayıtlı listeye bekleme.bas.no'yu EKLE; sonra bekleme listesinden BAŞTAN ÇIKAR
```

Değişmez (`ders_gecerli_mi`): bir numara iki listede birden ya da bir listede iki kez yoktur; bekleme listesi boş değilse kayıtlı sayısı ≥ kontenjan (boş yer varken kimse beklemez). Aktarmada numara **önce** diziye eklenir, **sonra** listeden çıkarılır: dizi büyütmesi başarısız olursa öğrenci kaybolmaz, beklemede kalır. Kontenjan kayıtlı sayısının altına indirilirse kimse çıkarılmaz; yeni gelenler bekler.

### 4.4 Bağlı listede birleştirme: kukla düğüm, düğüm taşımadan

![Kukla düğümle birleştirme](mini_obs_v2_7_birlestir.png)

*Şekil 2. Kukla düğümle birleştirme, birim testindeki girdiyle (A = 1 3 5 7, B = 2 3 6 8 9; 3 iki listede de var). Sonuç A ve B'nin düğümlerinden oluşur; hiçbir kayıt kopyalanmaz. Sayılar (6 karşılaştırma, 7 bağlantı) Python izlemesinde hesaplanır ve birim testiyle aynıdır.*

```
algoritma BİRLEŞTİR(a, b)                    ▷ a, b: numaraya göre kesin artan listeler
    kukla.sonraki ← NULL; son ← &kukla          ▷ kukla YIĞINDA, sonuca girmez
    a ≠ NULL ve b ≠ NULL oldukça:               ▷ değişmez: kukla.sonraki..son sıralı ve a, b'dekilerden küçük
        eğer a.no < b.no ise son.sonraki ← a; son ← a; a ← a.sonraki
        değilse b.no < a.no ise son.sonraki ← b; son ← b; b ← b.sonraki
        değilse                                  ▷ çakışma: A'nınki kalır, B'nin düğümü free
            son.sonraki ← a; son ← a; a ← a.sonraki; x ← b; b ← b.sonraki; free(x)
    son.sonraki ← (a ≠ NULL ? a : b)             ▷ kalan zincir TEK bağlantıyla
    kukla.sonraki'yi döndür
```

- **Aynı sonuç, aynı karşılaştırma:** sonuç v2.5'in `sube_birlestir`'iyle (kâhin) kayıt kayıt aynıdır (`memcmp`); karşılaştırma sayısı da aynıdır (iki liste de boş değilken adım başına bir üç yollu karşılaştırma). Fark taşımadadır: dizi birleştirmesi her kaydı (144 bayt) bir kez kopyalar (örnek veride 14 taşıma), liste hiç kopyalamaz (taşıma 0, bağlantı 11 = adım + 1).
- **Kukla düğüm** "liste boşken ilk düğüm" durumunu ortadan kaldırır: `son` her zaman geçerli bir düğümü gösterir. Kukla bir `KayitDugumu` olduğu için yığında 152 bayt kaplar; yalnız `sonraki` alanı kullanılır.
- **Sahiplik aktarımı:** fonksiyon `a` ve `b`'nin sahipliğini alır, birleşik listenin sahipliğini döndürür; çağıran `a` ve `b`'yi bir daha kullanmaz. Çakışan B düğümünü bırakmak birleştirmenin sorumluluğudur (§ 5).

### 4.5 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `bekleme_sona_ekle`, `bekleme_bastan_cikar`, `bekleme_sil`, `bekleme_sira` | düz dizi modeli (kaydırmalı); rastgele işlem dizileri (yinelenen numaralar sık), **her adımda** dönüş değeri, bütün içerik, değişmez ve sayaçlar |
| `ders_kaydol`, `ders_birak`, `ders_kontenjan_ayarla` | iki düz diziyle kuralların doğrudan modeli: kabul/bekleme, konum, aktarılan numara ve aktarma sırası |
| `no_dizisi` (dört politika) | dizi modeli; kapasite ve kopyalama sayacı adım adım |
| `kayit_listeleri_birlestir` | v2.5 `sube_birlestir` (dizi): aynı kayıtlar, çakışmalar, karşılaştırma; taşıma 0, bağlantı = karşılaştırma + 1 |
| `birlestir --yontem liste --denetle` | aynı kâhin, program düzeyinde |

## 5. Bellek sahipliği

| Yapı | Kim ayırır | Kim serbest bırakır | Yaşam süresi |
|---|---|---|---|
| `Sinif.kayit` (kayıt dizisi, 144 bayt/kayıt) | `sinif_ekle_say` / `sinif_yukle` (`realloc`, × 2, geçici işaretçiyle) | `sinif_birak` (programların tek temizlik yolu) | yüklemeden program sonuna |
| `NoDizisi.a` (dersin kayıtlı listesi) | `no_dizisi_ekle` (`realloc`, × 2) | `no_dizisi_birak` (← `ders_yok_et`) | dersle birlikte |
| `BeklemeDugumu` (bekleme düğümü, 16 bayt) | `bekleme_sona_ekle` (`malloc`, düğüm başına bir) | `bekleme_bastan_cikar` (aktarmada), `bekleme_sil` (vazgeçmede), kalanlar `bekleme_yok_et` (← `ders_yok_et`) | istekten listeden çıkışa |
| `DersKontenjani` | çağıran: `kayit.c` `main`'inde yığında | yapı yığında kalır; içindekiler `ders_yok_et` ile | oturum boyunca |
| `KayitDugumu` (kayıt kopyası + işaretçi, 152 bayt) | `kayit_listesi_kur` (`malloc`, kayıt **kopyası**) | `kayit_listesi_yok_et` (yinelemeli); birleştirmede çakışan B düğümü `kayit_listeleri_birlestir` içinde | kurulmadan yok edilmeye; birleştirmede sahiplik birleşik listeye geçer |
| kukla düğüm | `kayit_listeleri_birlestir` (yığında) | otomatik (fonksiyon dönünce) | tek çağrı |
| birleşik `Sinif` (`birlestir.c`) | `kayit_listesi_sinifa` / `sube_birlestir` | `sinif_birak` | program sonuna |
| ölçüm düğüm tablosu (`olcer_yapi`) | `hazirla` (işaretçi tablosu), `liste_kur` (düğümler) | `temizle`; düğümler `bekleme_sil`/`bekleme_yok_et` | bir ölçüm noktası |

Kurallar (rehber 13.2): her ayıran fonksiyonun başlık yorumunda sahiplik sözleşmesi yazılıdır; her `malloc`/`realloc` dönüşü denetlenir; `realloc` sonucu önce geçici işaretçiye alınır; yok etme **yinelemelidir** ve bir düğümün `sonraki`'si `free`'den **önce** okunur (10⁶ düğümde de yığın taşmaz); yarım kurulan liste bırakılır (`kayit_listesi_kur` bellek yetmezse o ana kadarkileri free eder); bütün programlar çıkmadan bütün belleği bırakır. Sonuç: `make asan` (ASan + UBSan + LSan; yeni programların bütün işlemleri n = 1, 2, 3, 300 ile, kasıtlı hata kipleri dahil) temiz; `make valgrind` 25 çalıştırmanın hepsinde "ERROR SUMMARY: 0 errors" ve "All heap blocks were freed — definitely lost: 0 bytes":

```
valgrind ./obs_test_vg → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 20 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 2 --hata-goster bas → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 2 --hata-goster cakisma → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
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

### 6.1 `kayit`

```
./kayit ogrenciler.csv|.dat [--ders KOD] [--kontenjan K] [--komutlar dosya.txt]
  kaydol NO | birak NO | sira NO | kontenjan K | durum      (stdin ya da --komutlar; # açıklama)
```

```
$ ./kayit ornek_veri/ogrenciler.csv --kontenjan 3 --komutlar ornek_veri/kayit_komutlari.txt
Ders: BIL331 · kontenjan 3 · öğrenciler: ornek_veri/ogrenciler.csv (8 kayıt)
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
> kaydol 2301010052
  BEKLEME: 2301010052 ILGAZ ŞAHİN · kontenjan dolu (3/3) · bekleme sırası 3
> kaydol 2301010045
  DEĞİŞİKLİK YOK: 2301010045 zaten kayıtlı (sıra 1)
> sira 2301010047
  2301010047 İSMAİL ÖZTÜRK: bekleme sırası 2 / 3
> durum
  Kayıtlı (3/3):
     1) 2301010045 AYŞE NUR YILMAZ
     2) 2301010048 CAN YILMAZ
     3) 2301010050 EMRE ÇINAR
  Bekleme listesi (3):
     1) 2301010046 MEHMET ALİ KAYA
     2) 2301010047 İSMAİL ÖZTÜRK
     3) 2301010052 ILGAZ ŞAHİN
> birak 2301010048
  BIRAKTI: 2301010048 CAN YILMAZ (kayıtlı listede 2. idi)
  AKTARMA: 2301010046 MEHMET ALİ KAYA bekleme listesinin başından kayıtlı listeye · kayıtlı 3/3 · bekleyen 2
> birak 2301010052
  SIRADAN ÇIKTI: 2301010052 ILGAZ ŞAHİN (bekleme listesinde 2. idi)
> sira 2301010047
  2301010047 İSMAİL ÖZTÜRK: bekleme sırası 1 / 1
> kaydol 2301010049
  BEKLEME: 2301010049 ZEYNEP ÇELİK · kontenjan dolu (3/3) · bekleme sırası 2
> kaydol 2301010099
  RET: 2301010099 numaralı öğrenci dosyada yok
> kontenjan 5
  KONTENJAN: 3 → 5 · aktarılan 2
  AKTARMA: 2301010047 İSMAİL ÖZTÜRK
  AKTARMA: 2301010049 ZEYNEP ÇELİK
> birak 2301010051
  DEĞİŞİKLİK YOK: 2301010051 bu derste yok
> durum
  Kayıtlı (5/5):
     1) 2301010045 AYŞE NUR YILMAZ
     2) 2301010050 EMRE ÇINAR
     3) 2301010046 MEHMET ALİ KAYA
     4) 2301010047 İSMAİL ÖZTÜRK
     5) 2301010049 ZEYNEP ÇELİK
  Bekleme listesi (0): —
Özet: 17 komut · kabul 3 · bekleme 4 · aktarma 3 · bırakma 2 · ret 1 · hata 0 · son durum: kayıtlı 5/5, bekleyen 0
[çıkış kodu: 0]
```

Hatalı komut satırları satır numarasıyla bildirilir, oturum sürer ve çıkış kodu 1 olur:

```
$ cat testler/kayit_hatali.txt; ./kayit ornek_veri/ogrenciler.csv --komutlar testler/kayit_hatali.txt
# hatalı komut satırları: her biri satır numarasıyla bildirilir, işlem sürer
kaydol
kaydol abc
kaydet 2301010045
kaydol 2301010045 fazla
kontenjan -4
kaydol 2301010045
durum
Ders: BIL331 · kontenjan 3 · öğrenciler: ornek_veri/ogrenciler.csv (8 kayıt)
> kaydol
satır 2: HATA: komut anlaşılamadı (kaydol NO | birak NO | sira NO | kontenjan K | durum)
> kaydol abc
satır 3: HATA: komut anlaşılamadı (kaydol NO | birak NO | sira NO | kontenjan K | durum)
> kaydet 2301010045
satır 4: HATA: komut anlaşılamadı (kaydol NO | birak NO | sira NO | kontenjan K | durum)
> kaydol 2301010045 fazla
satır 5: HATA: komut anlaşılamadı (kaydol NO | birak NO | sira NO | kontenjan K | durum)
> kontenjan -4
  HATA: kontenjan 0..1000000 olmalı
> kaydol 2301010045
  KABUL: 2301010045 AYŞE NUR YILMAZ · kayıtlı 1/3
> durum
  Kayıtlı (1/3):
     1) 2301010045 AYŞE NUR YILMAZ
  Bekleme listesi (0): —
Özet: 7 komut · kabul 1 · bekleme 0 · aktarma 0 · bırakma 0 · ret 0 · hata 5 · son durum: kayıtlı 1/3, bekleyen 0
[çıkış kodu: 1]
```

### 6.2 `birlestir --yontem liste`

```
$ ./birlestir ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv --yontem liste --denetle --ilk 6
Şube A: ornek_veri/ogrenciler.csv · 8 kayıt
Şube B: ornek_veri/sube_b.csv · 6 kayıt
Birleşik: 14 kayıt (numara sırasında; bağlı liste, kukla düğüm) · 10 karşılaştırma, 0 taşıma, 11 bağlantı
Kâhin (v2.5 dizi birleştirmesi): AYNI · dizide 14 taşıma (144 baytlık kayıt kopyası), listede 0
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010041  BURAK AKSOY                69.20 CB   61.60 CC   73.00 BB   2.47
   2  2301010043  ELİF ŞİMŞEK                89.80 AA   78.80 BB   72.00 CB   3.21
   3  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   4  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
   5  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   6  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
  ... (8 kayıt daha)
Süre: birleştirme 0.001 ms
[çıkış kodu: 0]
```

```
$ ./birlestir ornek_veri/ogrenciler.csv testler/sube_cakisma.csv --yontem liste --denetle
Şube A: ornek_veri/ogrenciler.csv · 8 kayıt
Şube B: testler/sube_cakisma.csv · 3 kayıt
Birleşik: 10 kayıt (numara sırasında; bağlı liste, kukla düğüm) · 9 karşılaştırma, 0 taşıma, 10 bağlantı
Kâhin (v2.5 dizi birleştirmesi): AYNI · dizide 10 taşıma (144 baytlık kayıt kopyası), listede 0
ÇAKIŞMA: 1 numara birden çok şubede var: 2301010047
Süre: birleştirme 0.001 ms
[çıkış kodu: 1]
```

## 7. Tasarım kararları

1. **Bekleme listesi numara tutar, kayıt değil.** Kayıt `Sinif`'te tek yerde kalır; liste düğümü 16 bayttır ve sahiplik basittir (düğüm başka bir şeyin sahibi değildir). Öğrencinin adı gerektiğinde numarayla ikili aramayla bulunur.
2. **Kuyruk işaretçisi zorunlu.** Bekleme listesi bir kuyruktur: sona ekleme O(1) olmazsa n istek Θ(n²) olur. Bedeli tek bir değişmezdir (`son` son düğümü gösterir) ve onu bozan tek işlem son düğümü silmektir.
3. **Silme `Node **` ile.** Baş düğüm ayrı bir dal olmadan silinir; hata olasılığı azalır (§ 9'daki kasıtlı hata tam bu dalı unutur).
4. **Kayıtlı liste dinamik dizi.** Kayıtlı öğrenciler kayıt sırasında tutulur ve sık dolaşılır (durum, değişmez denetimi); bırakma ortadan silmedir ama önce aramadır: § 8'in ölçümü, aramanın baskın olduğu işlemde dizinin kazandığını gösterir.
5. **Bağlı listede birleştirme kayıtları kopyalamaz.** Kayıtlar 144 bayttır; dizi birleştirmesi her kaydı bir kez kopyalar ve n kayıtlık ek dizi ister. Listede iş yalnızca bağlantılardır. Bedeli: listeyi kurmak için kayıtların bir kez kopyalanması ve düğüm başına 8 bayt + ayırıcı yükü.
6. **Ölçümde yerleşim bir değişkendir.** Ayırıcı serbest bırakılan düğümleri ters sırada yeniden verdiği için "malloc sırası" tekrarlı çalıştırmalarda bitişik kalmaz; bu yüzden ölçüm düzeneği düğümleri açıkça adres sırasında (bitişik) ya da karıştırılmış sırada (dağınık) bağlar ve iki seriyi ayrı raporlar (rehber 13.5). İş (karşılaştırma sayısı, kontrol) iki seride aynıdır.
7. **Sayaçta yeni alan: `baglanti`.** Bağlı yapıların işi kayıt taşımak değil bağlantı değiştirmektir; ayrı bir sayaç bunu görünür kılar. Alan yalnızca sıfır değilse yazıldığı için önceki sürümlerin bütün çıktıları aynı kaldı.

## 8. Ölçümler

**Düzen:** `-O2`; her nokta için önce sayaç açık bir çalıştırma (sayılar stdout'a ve CSV'ye), sonra 1 ısınma + 5 tekrar, ortanca (n ≥ 32 000'de 3 tekrar); her çalıştırmadan önce kurma adımı (liste/dizi kurulur, süre dışında). Büyüme sınıfı oran testi ve log–log eğimle okunur (Sedgewick & Wayne, 2011). Karesel iş yüklerinde 40 s'lik bütçe: tahmini süresi bütçeyi aşan nokta ölçülmez, CSV'ye **kestirim** satırı yazılır (T(n) ≈ T(n′)·(n/n′)²; bu ölçümde 6 nokta). Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L1d 64 KiB (2 × 32), L2 2 MiB, L3 33 MiB; gcc 13.3.0, glibc 2.39; tarih 2026-10-13 14:49. `make olcum` 2 dakika 39 s sürdü. Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 0,18, sonda 1,52 idi (2 çekirdek; başka işlerle paylaşıldı).

### 8.1 Bekleme listesi: dizi ↔ bağlı liste

![Dizi ve bağlı liste](mini_obs_v2_7_olcum.png)

*Şekil 3. Aynı iş yükü, iki yapı (log–log). İçi boş işaretler kestirimdir. Sağ alt: n öğenin tek dolaşmasında öğe başına süre (önbellek düzeyleri).*

| n (sona ekle + baştan çıkar) | dizi (kaydırmalı) | bağlı liste | dizi / liste |
|--:|--:|--:|--:|
| 1 000 | 101,3 µs | 26,7 µs | 3,8 |
| 2 000 | 263,4 µs | 53,3 µs | 4,9 |
| 4 000 | 988,6 µs | 106,6 µs | 9,3 |
| 8 000 | 5,6 ms | 260,3 µs | 21,3 |
| 16 000 | 17,0 ms | 660,7 µs | 25,7 |
| 32 000 | 71,9 ms | 1,1 ms | 67,4 |
| 100 000 | 761,0 ms | 3,1 ms | 246,7 |
| 1 000 000 | — | 33,8 ms | — |

*Tablo 3. FIFO iş yükü: n sona ekleme + n baştan çıkarma (`fifo_*`). Dizide her çıkarma kalanları kaydırır: 10⁵'te 4 999 950 000 öğe taşıma; listede 300 001 bağlantı, taşıma 0.*

| n | silme: dizi | liste (bitişik) | liste (dağınık) | bitişik / dizi | dağınık / dizi | sıra: dizi | liste (bitişik) | liste (dağınık) | bitişik / dizi | dağınık / dizi |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 380,3 µs | 643,3 µs | 548,0 µs | 1,7 | 1,4 | 309,4 µs | 855,5 µs | 645,7 µs | 2,8 | 2,1 |
| 2 000 | 753,8 µs | 3,0 ms | 4,0 ms | 4,0 | 5,3 | 1,2 ms | 5,0 ms | 8,2 ms | 4,1 | 6,7 |
| 4 000 | 2,8 ms | 14,1 ms | 25,3 ms | 5,0 | 9,0 | 5,0 ms | 20,9 ms | 41,1 ms | 4,2 | 8,3 |
| 8 000 | 11,7 ms | 57,3 ms | 102,1 ms | 4,9 | 8,7 | 19,7 ms | 92,7 ms | 181,9 ms | 4,7 | 9,2 |
| 16 000 | 48,1 ms | 233,9 ms | 565,2 ms | 4,9 | 11,8 | 78,3 ms | 364,5 ms | 1,03 s | 4,7 | 13,2 |
| 32 000 | 213,5 ms | 959,1 ms | 3,28 s | 4,5 | 15,4 | 404,5 ms | 1,43 s | 6,86 s | 3,5 | 17,0 |
| 100 000 | 2,17 s | 9,37 s *(kestirim)* | 32,02 s *(kestirim)* | ≈ 4,3 | ≈ 14,7 | 3,72 s | 14,01 s *(kestirim)* | 66,97 s *(kestirim)* | ≈ 3,8 | ≈ 18,0 |

*Tablo 4. Numarayla silme (n öğe rastgele sırada silinir) ve sıra sorgusu (n rastgele sorgu). Bitişik: düğümler adres sırasında bağlı; dağınık: aynı düğümler karıştırılmış sırada bağlı. ≈: kestirime dayanan oran. İki yapıda da karşılaştırma sayısı ve kontrol AYNIDIR (n = 32 000'de silmede 257 177 963, sorguda 511 370 444 karşılaştırma); dizide silme ayrıca 254 838 037 taşıma yapar.*

**Yorum (Stroustrup deneyiyle bağ).**

- **Liste, kuyruk davranışında kazanır.** Baştan çıkarma dizide Θ(n) kaydırmadır; FIFO'da toplam n(n − 1)/2 taşıma ve log–log eğim 1,89 (1 000 → 32 000). Listede her işlem O(1): eğim 1,03 (10³ → 10⁶) ve 10⁵ işlemde 247 kat fark. Bekleme listesinin asıl işi budur: **kuyruk için bağlı liste (ya da H9'un dairesel tamponu)**, kaydırmalı dizi değil.
- **Arama gerektiren işlemde dizi kazanır.** Numarayla silme iki yapıda da önce doğrusal aramadır ve aynı sayıda karşılaştırma yapar. Dizi buna ek olarak kalanları kaydırır — ama `memmove` ardışık bloğu çok hızlı taşır ve arama bitişik bellekte önbellek dostudur. n = 32 000'de karşılaştırma başına süre: dizi 0,83 ns (kaydırma dahil), bitişik liste 3,73 ns, dağınık liste 12,75 ns. Sıra sorgusunda (kaydırma yok) dizi 0,79 ns, liste 2,81 ns ve 13,41 ns. Bu, Stroustrup'un (2014) gözlemidir: kuramdaki "listede silme O(1)" yalnızca düğüm **elde** iken geçerlidir; düğümü bulmak gerekiyorsa doğrusal aramanın maliyeti eklemenin ya da silmenin maliyetini gölgeler ve bitişik bellek kazanır.
- **Yerleşim ikinci bir etkendir.** Aynı liste, düğümleri bellekte dağınıkken bitişikten 3,4 (silme) ve 4,8 kat (sorgu) yavaştır; dağınık serilerin eğimi 2'nin belirgin üstündedir (silme 2,51, sorgu 2,67): liste büyüdükçe önbellek düzeyleri aşılır ve her düğüm erişimi daha uzak bir düzeye gider. Tek dolaşma deneyi bunu doğrudan gösterir (Tablo 5): dizide öğe başına süre 10³'ten 10⁶'ya 1 ns dolayında kalır (0,62 → 0,82 ns), dağınık listede 1,42 → 144,5 ns. Uzun ömürlü bir programda (ekleme ve silmeler karıştıkça) düğümler dağınıklaşır; gerçek hayat dağınık seriye daha yakındır.
- **Kestirim iyimserdir.** 10⁵'teki liste kestirimleri 32 000'den (n/n′)² ile hesaplandı; 10⁵ düğüm (≈ 3,2 MB) L2'yi aştığı için gerçek süre büyük olasılıkla daha uzundur.

| n | dizi (ns/öğe) | liste, bitişik (ns/öğe) | liste, dağınık (ns/öğe) | dağınık / dizi |
|--:|--:|--:|--:|--:|
| 1 000 | 0,62 | 1,23 | 1,4 | 2,3 |
| 3 000 | 0,61 | 1,74 | 5,7 | 9,3 |
| 10 000 | 0,61 | 1,73 | 6,8 | 11,1 |
| 30 000 | 0,61 | 1,79 | 15,4 | 25,5 |
| 100 000 | 0,63 | 1,92 | 37,1 | 58,8 |
| 300 000 | 0,63 | 2,40 | 144,6 | 228,3 |
| 1 000 000 | 0,82 | 5,86 | 144,5 | 175,8 |

*Tablo 5. Tek dolaşma: n öğenin toplamı, bir çalıştırmada ⌈10⁶/n⌉ kez (≈ 10⁶ erişim); öğe başına ns.*

### 8.2 Sınırlılıklar

Tek ve paylaşılan bir sanal makinede ölçüldü; sayaçlar (karşılaştırma, taşıma, bağlantı, kopyalama) makineden bağımsızdır, süreler değildir. `realloc`'un davranışı ayırıcıya bağlıdır (Tablo 1). Dağınık seri yapay bir karıştırmadır; gerçek programdaki dağınıklık iş yüküne bağlıdır. Öğrenciden aynı ölçümleri kendi makinesinde tekrarlaması beklenir: sayılar değişir, büyüme sınıfları ve "aramada dizi, kuyrukta liste" sonucu değişmez.

## 9. Testler

- **Birim testleri** (`obs_test`): `324 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama + 23 böl-fethet + 19 öbek-doğrusal + 79 bağlı liste`. Bağlı liste testleri: dört büyüme politikasında 12 farklı n için içerik ve kopyalama sayacı = kapalı biçim; × 2'de 1 000 eklemede 11 büyütme ve 1 023 kopya; sil/araya ekle kaydırma sayıları; `Sinif` sayacı (100 kayıt → 224 taşıma); bekleme listesi: boş liste, baş düğüm silme (`Node **`), son düğüm silme ve ardından sona ekleme (kuyruk işaretçisi), FIFO sırası, tek düğüm, yinelenen numara (ilki silinir), 1 002 düğümün yok edilmesi, bağlantı ve karşılaştırma sayaçları; kontenjan: kabul, bekleme, ZATEN durumları, bırakmada aktarma, bekleyenin vazgeçmesi, kontenjan artırma (iki aktarma) ve azaltma, geçersiz kontenjan, kodun kesilmesi; bağlı listede birleştirme = dizi birleştirmesi (çakışmada A'nın kaydı, 6 karşılaştırma, taşıma 0, 7 bağlantı), boş listeler, örnek dosyalarla çakışma.
- **Kâhin testleri** (`test_kahin`): 300 denemede 446 295, 1 000 denemede 1 478 677 denetim (bağlı yapılar: 305 906), uyuşmazlık yok.
- **Kasıtlı hatalar.** (a) `--hata-goster bas` — numarayla silme "önceki" işaretçisiyle, baş düğüm ayrı ele alınmadan yazılmış; kâhin uyuşmazlığı bulur ve 1..4 işlemlik bütün diziler denenerek en kısa karşı örnek basılır (2 işlem: `sona_ekle(1); sil(1)` → dönüş 0 (beklenen 1)):

```
$ ./test_kahin --hata-goster bas
KÂHİN UYUŞMAZLIĞI (tohum 2)
  İşlev      : bekleme listesi
  n          : 220
  Beklenen   : dizi modeli (kaydırmalı): 34. işlem sil(3)
  Bulunan    : dönüş 3 (beklenen 1)
  Son işlemler: sona_ekle(3) sona_ekle(2) bastan_cikar sona_ekle(3) sona_ekle(2) bastan_cikar bastan_cikar bastan_cikar sil(1) bastan_cikar sira(1) sil(3)
  En kısa karşı örnek (2 işlem): sona_ekle(1); sil(1) → dönüş 0 (beklenen 1)
  Yeniden üretmek için: ./test_kahin --tohum 2 --deneme 1 --hata-goster bas
[çıkış kodu: 1]
```

  (b) `--hata-goster cakisma` — bağlı listede birleştirmede çakışan numarada B'nin düğümü kalıyor; karşılaştırma ve bağlantı sayıları doğru olduğu için yalnız **içerik** karşılaştırması yakalar:

```
$ ./test_kahin --hata-goster cakisma
KÂHİN UYUŞMAZLIĞI (tohum 2)
  İşlev      : kayit_listeleri_birlestir
  n          : 117
  Beklenen   : 117 kayıt, 14 çakışma, 105 karşılaştırma (sube_birlestir, v2.5)
  Bulunan    : 117 kayıt, 14 çakışma, 105 karşılaştırma, taşıma 0, bağlantı 106
  İlk fark: sıra 16 · numara 2400000016 · beklenen ad HÜSEYİN, bulunan BAŞKA
  Yeniden üretmek için: ./test_kahin --tohum 2 --deneme 1 --hata-goster cakisma
[çıkış kodu: 1]
```

- **Bellek:** § 5. Kasıtlı hata kiplerinde de bellek temizdir (hatalar mantıksaldır; `make asan` ve `make valgrind` bu kipleri de çalıştırır ve çıkış kodunun 1 olduğunu denetler).

## 10. Ders notu için özet (Hafta 8 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'ye ilk bağlı yapıyı ekliyoruz: kontenjanı dolu bir dersin **bekleme listesi** (tek bağlı liste + kuyruk işaretçisi) ve kontenjan açılınca **otomatik aktarma**; iki şubenin sıralı kayıt listelerini **bağlı listede, kukla düğümle, düğüm taşımadan** birleştiriyoruz; kayıt dizisinin **büyüme politikasını** belgeleyip **kopyalama sayacı** ekliyoruz. Bütün yapıların **bellek sahipliğini** bir tabloyla yazıyor, **ASan** ve **Valgrind** ile sızıntısız olduğunu gösteriyoruz. Ölçümde bekleme listesi işlemlerini dizi ve bağlı listeyle karşılaştırıyoruz (Stroustrup deneyi).

### Gereksinimler

- `dinamik.h/.c`: `NoDizisi` — `no_dizisi_ekle` (× 2; `realloc` sonucu geçici işaretçiye), `no_dizisi_sil_say` (kaydırma = taşıma), `no_dizisi_bul_say`, `no_dizisi_birak`; **kopyalama sayacı** (büyütmede eski n) ve büyütme sayacı; isteğe bağlı + 1, + 10, × 1,5 politikaları.
- `bekleme.h/.c`: `BeklemeDugumu { long long no; BeklemeDugumu *sonraki; }`, `BeklemeListesi { bas, son, n }`; `bekleme_sona_ekle` (O(1)), `bekleme_bastan_cikar` (O(1)), `bekleme_sil` (**`BeklemeDugumu **`** ile; son düğümde `son` güncellenir), `bekleme_sira` (1'den başlayan konum, yoksa 0), `bekleme_yok_et` (yinelemeli), `bekleme_gecerli_mi` (değişmez).
- `kontenjan.h/.c`: `ders_kaydol` (KABUL / BEKLEME / ZATEN_*), `ders_birak` (kayıtlıdan çıkınca bekleme listesinin başını **otomatik aktar**; bekleyenden çıkınca numarayla sil), `ders_kontenjan_ayarla`, `ders_yok_et`, `ders_gecerli_mi`.
- `kayit_listesi.h/.c`: `kayit_listesi_kur` (kayıt kopyaları), `kayit_listeleri_birlestir` (**kukla düğüm**, çakışmada A'nın düğümü kalır, B'ninki free), `kayit_listesi_yok_et`; `birlestir --yontem liste --denetle`.
- `kayit` programı: `kaydol NO`, `birak NO`, `sira NO`, `kontenjan K`, `durum` komutları; hatalı satır numarasıyla bildirilir.
- **Bellek sahipliği tablosu** (yapı | kim ayırır | kim serbest bırakır | yaşam süresi) RAPOR.md'de; her ayıran fonksiyonun yorumunda sahiplik sözleşmesi.
- `make asan` ve **`make valgrind`** bütün testlerde temiz ("ERROR SUMMARY: 0 errors", "definitely lost: 0 bytes").
- Ölçüm: bekleme listesi işlemlerinde dizi ↔ bağlı liste, n = 10³…10⁵ (FIFO, numarayla silme, sıra sorgusu); en az bir seride düğümlerin dağınık yerleşimi; büyüme politikalarının kopyalama sayıları; dürüst yorum.

### İpuçları

- Boş liste, tek düğüm, baş düğüm ve son düğüm: her işlemi bu dört durumda kâğıtta kutu–okla çizin. Son düğümü silince `son`'u, tek düğümü çıkarınca **hem** `bas`'ı hem `son`'u güncelleyin.
- `BeklemeDugumu **bag = &b->bas;` ile başlayın; ilerlerken `bag = &(*bag)->sonraki;`. Silmede `*bag = silinen->sonraki;` baş düğümde de çalışır.
- Yok ederken `sonraki`'yi `free`'den **önce** okuyun: `BeklemeDugumu *s = d->sonraki; free(d); d = s;`.
- `realloc(p, …)` sonucunu doğrudan `p`'ye atamayın: `long long *g = realloc(p, …); if (g == NULL) { … } p = g;`.
- Kukla düğümü yığında açın (`KayitDugumu kukla; kukla.sonraki = NULL;`); sonuç `kukla.sonraki`'dir, kukla free edilmez.
- Aktarmada önce kayıtlı diziye ekleyin, ekleme başarılıysa bekleme listesinden çıkarın (bellek hatasında öğrenci kaybolmaz).
- Valgrind için sanitizer'sız ikili derleyin (`-O0 -g`): ASan ile derlenmiş program Valgrind altında anlamlı sonuç vermez (iki araç belleği farklı yollarla izler).
- Kâhin için listenin içeriğini her adımda düz bir diziyle karşılaştırın; yalnız uzunluğu karşılaştırmak yanlış düğümün silinmesini kaçırır.
- Ölçümde listeyi bir kez kurup tekrar tekrar silmeyin: her çalıştırmadan önce yeniden kurun ve kurmayı süreye katmayın; düğüm yerleşimini (bitişik/dağınık) bilinçli seçin.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri ve `test_kahin` (300 deneme) geçer.
2. × 2 politikasında n sona eklemenin kopyalama sayacı P − 1'dir (P: n'den büyük ya da eşit en küçük 2'nin kuvveti; 1 000 eklemede 1 023 kopya, 11 büyütme); + 1 politikasında n(n − 1)/2 (1 000 eklemede 499 500).
3. Bekleme listesinde 10, 20, 30 eklendikten sonra 30 (son düğüm) silinir ve 40 eklenirse liste 10, 20, 40 olur ve `son` 40'ı gösterir; 10 (baş düğüm) silinirse `bas` 20'yi gösterir; tek düğüm çıkarılınca `bas` = `son` = `NULL`.
4. `./kayit ornek_veri/ogrenciler.csv --kontenjan 3 --komutlar ornek_veri/kayit_komutlari.txt` şu özet satırını basar ve 0 ile çıkar: `Özet: 17 komut · kabul 3 · bekleme 4 · aktarma 3 · bırakma 2 · ret 1 · hata 0 · son durum: kayıtlı 5/5, bekleyen 0`; 2301010048 bırakınca "AKTARMA: 2301010046 …" satırı görünür.
5. `./kayit ornek_veri/ogrenciler.csv --komutlar testler/kayit_hatali.txt`: beş hatalı satır satır numarasıyla bildirilir, sonraki geçerli komut yine çalışır; çıkış 1.
6. `./birlestir ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv --yontem liste --denetle`: 14 kayıt, 10 karşılaştırma, **0 taşıma**, 11 bağlantı; "Kâhin (v2.5 dizi birleştirmesi): AYNI"; çıkış 0. `testler/sube_cakisma.csv` ile: "ÇAKIŞMA: 1 numara … 2301010047", çıkış 1.
7. `./test_kahin --hata-goster bas` uyuşmazlığı ve en kısa karşı örneği (`sona_ekle(1); sil(1)`) basar, 1 ile çıkar; `--hata-goster cakisma` 1 ile çıkar.
8. `make asan` "bellek hatası, tanımsız davranış ve sızıntı yok" ile biter; `make valgrind`'in her satırında "ERROR SUMMARY: 0 errors" ve "definitely lost: 0 bytes" (ya da "All heap blocks were freed") vardır.
9. RAPOR.md'de bellek sahipliği tablosu en az bekleme düğümünü, kayıtlı diziyi, kayıt dizisini ve birleştirmedeki kayıt düğümlerini kapsar.
10. Kendi makinenizde 10⁵ işlemlik FIFO'da bağlı liste dizi sürümünden en az 10 kat hızlıdır (bu makinede 247 kat); numarayla silmede ise dizi bitişik listeden hızlıdır (bu makinede n = 32 000'de 4,5 kat). İki yapının karşılaştırma sayıları aynıdır.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | boş listede baştan çıkar, sil, sıra | false, 0, 0; `bas` = `son` = `NULL` |
| 2 | sona ekle 10, 20, 30; sıra(30) | 3; karşılaştırma 3; bağlantı (eklemeler) 6 |
| 3 | sil(10) — baş düğüm | konum 1; `bas` → 20; bağlantı 1 |
| 4 | sil(30) — son düğüm; sona ekle 40 | konum 2; `son` → 20, sonra 40; liste 20 40 |
| 5 | sona ekle 5, 6, 5; sil(5) | ilk 5 silinir; liste 6 5; sıra(5) = 2 |
| 6 | 1..5 ekle, 5 kez baştan çıkar | 1 2 3 4 5 (FIFO); liste boş |
| 7 | kontenjan 2: kaydol 1, 2, 3, 4 | KABUL, KABUL, BEKLEME (1), BEKLEME (2) |
| 8 | birak 1 | kayıtlı 2 3; aktarılan 3; bekleyen 4 |
| 9 | birak 4 (bekleyen) | BEKLEMEDEN, konum 1; bekleme boş |
| 10 | kontenjan 2 → 5 (iki kişi bekliyor) | iki aktarma, geliş sırasıyla |
| 11 | birleştir A = 1 3 5 7, B = 2 3 6 8 9 | 1 2 3 5 6 7 8 9; çakışma 3 (A'nın kaydı); 6 karşılaştırma, 0 taşıma, 7 bağlantı |
| 12 | `kayit ... --kontenjan -1` | kullanım iletisi; çıkış 2 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.6'nız (ya da referans v2.6), `dinamik.h`, `bekleme.h`, `kontenjan.h`, `kayit_listesi.h` (bildirimler, sözleşmeler, sahiplik yorumları), `valgrind_denetle.sh`, `ornek_veri/kayit_komutlari.txt`, `olcer_yapi`'nın ölçüm düzeneği (kurma adımı, düğüm yerleşimi, bütçe).
- **Yazılır:** `dinamik.c`, `bekleme.c`, `kontenjan.c`, `kayit_listesi.c`, `kayit.c`; `birlestir.c`'ye `--yontem liste`; testler (birim + kâhin); sahiplik tablosu; ölçüm ve yorum.
- **Değiştirilmez:** v1.0 kuralları ve menü, kayıt dizisinin numara sırası, önceki sürümlerin yöntemleri (kâhin olarak kalırlar), ortak modüller.
- **Meydan okuma:** (a) çift bağlı bekleme listesi: kayıt dizininde düğüm adresini tutarak vazgeçmeyi O(1) yapın ve ölçün; (b) bağlı listede birleştirmeli sıralama (öge taşımadan) ile kayıt listesini başarıya göre sıralayın, v2.5'in dizi sürümüyle karşılaştırın; (c) Floyd döngü tespitiyle `bekleme_gecerli_mi`'yi döngülü listede de sonlanır yapın; (d) bekleme listesini dizide **kaydırmasız** tutun (baş indisi; H9'un dairesel tamponu) ve FIFO ölçümünü tekrarlayın.

## 11. Bilinen sınırlılıklar

- Kayıt ve bırakma, iki listede doğrusal arama yaptığı için Θ(kayıtlı + bekleyen)'dir; kontenjanı binlerce olan derslerde v2.9'un karma tablosuyla (numara → durum) O(1) beklenen olur.
- Tek ders: `kayit` bir dersin kontenjanını yönetir; çok dersli kayıt günü v2.8'in simülasyonundadır. Menü (`mini_obs`) ders kaydını içermez (v3.0).
- Öğrenci silindiğinde derslerdeki kaydı kendiliğinden düşmez (iki yapı ayrıdır); v2.8'in işlem kabuğu bunu açıkça yönetir.
- Kopyalama sayacı modeldir: `realloc`'un yerinde büyütmesi ya da sayfa eşlemesiyle taşıması gerçek kopyayı azaltır (Tablo 1).
- Süreler tek ve paylaşılan bir sanal makinede ölçüldü; dağınık yerleşim yapay bir karıştırmadır.

## 12. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Knuth, D. E. (1997). *The art of computer programming: Vol. 1. Fundamental algorithms* (3rd ed.). Addison-Wesley.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
- Stroustrup, B. (2014). *Are lists evil?* Standard C++ Foundation. https://isocpp.org/blog/2014/06/stroustrup-lists
