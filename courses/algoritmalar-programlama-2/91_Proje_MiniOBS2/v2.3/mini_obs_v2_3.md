# Mini-OBS 2 v2.3 — Arama Algoritmaları: numaraya göre ikili arama ve soyad önekiyle arama (Hafta 4)

**Bu sürümün amacı:** Mini-OBS'nin en sık işi olan "numarayla kaydı bul" sorusunu doğrusal taramadan (Θ(n)) **ikili aramaya** (Θ(log n)) taşımak. Bunun bedeli bir **önkoşuldur**: kayıt dizisi her an **numaraya göre sıralı** tutulmalıdır. v2.3'te yükleyici (`sinif_yukle`) her kaydı **ikili aramayla bulduğu konuma** ekler; aynı ikili arama mükerrer numarayı da yakalar. Bu sayede yükleyicinin mükerrer denetimi n(n − 1)/2 karşılaştırmadan Θ(n log n) karşılaştırmaya iner (10⁵ kayıtta 4 999 950 000 → 1 622 620). Ölçüm ise dürüst bir sürpriz verir: **yükleme hızlanmaz.** Karışık sıralı bir dosyada her ekleme ortalama n/4 kaydı sağa **kaydırır**; 10⁵ kayıtta 2 495 087 143 kayıt taşıması (toplam ≈ 359 GB kaydırılan veri) yüklemeyi 19,05 s'den 20,75 s'ye çıkarır. Darboğaz karşılaştırmadan **taşımaya** geçmiştir ve v2.5'te toplu yükleme + birleştirmeli sıralamayla çözülecektir. Arama tarafında kazanç kesindir: 10⁵ kayıtta doğrusal arama ortalama 190 µs, ikili arama 261 ns sürer (730 kat). Ayrıca **soyad önekiyle arama** eklenir: kayıtlara işaretçilerden oluşan bir soyad dizininde `lower_bound` ve önek karşılaştırması ("YIL" → YILMAZ, YILDIZ, YILDIRIM).

Dosyalar (satır sayılarıyla): `arama.h` (113) · `arama.c` (227) · `ara.c` (231) · `dosya.h` (93) · `dosya.c` (381) · `main.c` (336) · `obs.h` (137) · `obs.c` (657) · `sayac.h` (49) · `sayac.c` (21) · `olcer.c` (805) · `test_obs.c` (1075) · `test_kahin.c` (1229) · `metin.h` (35) · `metin.c` (340) · `yinelenen.h` (43) · `yinelenen.c` (71) · `denetle.c` (140) · `secmeli.h` (102) · `secmeli.c` (330) · `ders_sec.c` (184) · `uretec.h` (54) · `uretec.c` (160) · `veri_uret.c` (94) · `deney.h` (28) · `deney.c` (32) · `ortak_rastgele.h` (43) · `ortak_rastgele.c` (50) · `zamanlayici.h` (34) · `zamanlayici.c` (63) · `Makefile` (201) · `ornek_veri/`, `testler/` (önceki sürümlerden) · `olcum/arama.csv`, `olcum/yukleme.csv`, `olcum/ekleme.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_3_ciktilar.txt` (674 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_3_ikili.png`, `mini_obs_v2_3_onek.png`; grafikler: `mini_obs_v2_3_olcum_arama.png`, `mini_obs_v2_3_olcum_yukleme.png`.

Derleme: `make` (`mini_obs`, `veri_uret`, `olcer`, `denetle`, `ders_sec`, **`ara`**), `make test`, `make olcum` (bu makinede 2 dakika 51 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 19 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0, 1 (dosya okunamadı ya da bellek yetersiz; testlerde uyuşmazlık), 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 4'ün Büyük Sorusu: bir milyon isimlik **sıralı** bir listede bir ismi en fazla kaç soruda bulursunuz? Her soru adayların yarısını elediği için ⌊log₂ 10⁶⌋ + 1 = 20 soru yeter. Mini-OBS'de "liste" numaraya göre sıralı kayıt dizisidir:

- **İkili arama ve değişmez** (ÖÇ 4.2): yarı açık aralık [lo, hi) sözleşmesi — aranan, varsa, `kayit[lo .. hi−1]` içindedir; solu küçük, sağı büyüktür. Her adım aralığı en az bir eleman küçültür; döngü sonlanır ve en çok ⌊log₂ n⌋ + 1 inceleme yapılır. Kapalı aralık [lo, hi] sürümü karşılaştırma için tutulur.
- **Güvenli orta nokta**: `lo + (hi − lo) / 2`. `(lo + hi) / 2` ifadesi lo + hi > INT_MAX olduğunda taşar; işaretli taşma C'de tanımsız davranıştır. Java'nın `Arrays.binarySearch` gerçekleştirimindeki bu hata yaklaşık dokuz yıl fark edilmemişti (Bloch, 2006).
- **Varyantlar** (ÖÇ 4.3): `lower_bound` (ilk ≥ konum) hem **ekleme konumunu** hem mükerrer denetimini verir; `upper_bound` (ilk > konum) soyad dizinini **kararlı** kurar; önek araması "önekle başlayanlar sıralı dizide ardışıktır" gözlemine dayanır.
- **Genel arama** (ÖÇ 4.5): `alt_sinir_genel` / `ust_sinir_genel` C kütüphanesinin `bsearch` arayüzünü (anahtar, taban, n, boyut, karşılaştırıcı) kullanır; öğe adresi taban + i × boyut ile hesaplanır.
- **Mühendis gözüyle — ön işleme ile sorgu maliyeti ödünleşimi**: veriyi sıralı tutmak her sorguyu ucuzlatır ama her eklemeyi pahalılaştırır. Bu sürümün ölçümü ödünleşimin iki yüzünü de sayılarla gösterir (bölüm 7).

Yol haritasındaki karşılığı (Tablo A.1): **H4 · v2.3 · Numaraya göre ikili arama; soyad önekiyle arama · İkili arama, lower_bound.** Sarmallar (Tablo 4.2): *Arama* — v1.0 doğrusal → **v2.3 ikili** → v2.9 karma tablosu. *Yükleyicinin mükerrer denetimi* — v2.0 n(n − 1)/2 karşılaştırma → **v2.3 Θ(n log n) karşılaştırma, Θ(n²) taşıma** → v2.5 toplu yükleme + birleştirmeli sıralama, Θ(n log n) → v2.9 karma tablosu. Bu yükleyici sorunu gerçek yazılımlarda da görülür: GTA Online'ın uzun yükleme süresinin iki karesel nedeninden biri, yaklaşık 63 000 kaydın her biri eklenirken tüm diziyle karşılaştırılmasıydı (t0st, 2021).

## 2. v2.2'den ne değişti?

| Konu | v2.2 (H3) | v2.3 (H4) |
|---|---|---|
| Kayıt dizisinin sırası | dosya sırası | **numaraya göre kesin artan** (değişmez; yükleme, ekleme ve silme korur) |
| Numarayla bulma (ara, güncelle, sil, transkript) | `sinif_numara_bul`, doğrusal | `ikili_ara_no`, yarı açık ikili arama |
| Yükleyicinin mükerrer denetimi | doğrusal tarama, n(n − 1)/2 karşılaştırma | ikili arama + kaydırma (`sinif_sirali_ekle`): Θ(n log n) karşılaştırma, ≈ n²/4 taşıma |
| Menü 3 (Ara) | numara ya da tam ad | + **soyad öneki**: `YIL*` (soyad dizini + lower_bound) |
| Yeni modül | — | `arama.h/.c`: `orta_nokta`, `ikili_ara_no(_kapali)`, `no_alt_sinir`, `sinif_sirali_ekle`, `alt/ust_sinir_genel`, `SoyadDizini`, `soyad_onek_ara` |
| `dosya` | tek kip | `YuklemeKipi` (DOGRUSAL v1.0, SIRALI v2.3, DENETIMSIZ v2.1); `csv_oku_kipli`, `ikili_oku_kipli`, `sinif_yukle_kipli` |
| `sayac` | karşılaştırma, toplama, çarpma | + `tasima` (kaydırılan kayıt); `sayac_yaz` taşıma 0 ise eski biçimde yazar |
| Program | 5 program | + **`ara`** (ikili arama izlemesi, doğrusal karşılaştırma, soyad öneki) |
| `olcer` | kayıt ve seçim işlemleri | + `dogrusal`, `ikili`, `ikili_kapali`, `bsearch`, `yukleme_v10`, `ayristirma`, `sirali_ekleme`, `anahtar_ekleme`; `--sira karisik\|artan\|azalan` |
| Testler | 150 birim; kâhin 59 342 denetim | 177 birim (+27 arama); kâhin 297 205 denetim; `--hata-goster ikili` |

Akış düzeyindeki `csv_oku` ve `ikili_oku` v1.0 davranışını (**dosya sırası**, doğrusal denetim) korur: v1.0'ın 99 doğrulaması, üreteç testleri ve v2.3 yükleyicisinin kâhini ("v1.0 yükleyicisi + sıralama") bunlara dayanır. Menü metni değişmedi; yalnızca arama istemi `Numara ya da ad (soyad öneki: YIL*) :` oldu. v1.0'ın T2 oturumu v2.3'te program başlığı ve bu istem dışında **aynı** çıktıyı verir (`mini_obs_v2_3_ciktilar.txt`, Regresyon).

## 3. Mimari

| Modül / program | Sorumluluk | Başlıca öğeler |
|---|---|---|
| `arama.h/.c` (**yeni**) | sıralı dizi değişmezi, ikili arama ailesi, soyad dizini | `orta_nokta`, `sinif_sirali_mi`, `ikili_ara_no_say`, `ikili_ara_no_kapali_say`, `no_alt_sinir_say`, `sinif_sirali_ekle_say`, `alt_sinir_genel`, `ust_sinir_genel`, `SoyadDizini`, `soyad_dizini_kur`, `soyad_onek_ara` |
| `dosya.h/.c` | kalıcılık + yükleme kipleri | `YuklemeKipi`, `kayit_yerlestir` (iç), `csv_oku_kipli`, `ikili_oku_kipli`, `sinif_yukle` (SIRALI) |
| `main.c` | menü | numarayla bulma ikili; ekleme sıralı; `onek_ara` (her aramada dizini kurar) |
| `obs.c` | raporlar | + `kayit_listesi_yaz` (işaretçi dizisinden liste) |
| `ara.c` (**yeni**) | komut satırı aracı | `--no` (iki ikili sürüm, `--izle`, `--dogrusal`), `--soyad` |
| `olcer.c` | ölçüm | arama işlemleri (süre arama başına), yükleme/ekleme işlemleri (sayım ısınma çalıştırmasında) |
| diğerleri | v2.2'den aynen | — |

`arama` yalnızca `obs.h` (kayıt tipi) ve `sayac.h`'yi bilir; `dosya` yükleme sırasında `arama`yı çağırır. Soyad dizini kayıtları **kopyalamaz**: 8 baytlık işaretçiler tutar; kayıtlar `Sinif` dizisinde kalır.

## 4. Algoritmalar

### 4.1 Yarı açık aralıkla ikili arama

```
algoritma İKİLİ-ARA(kayit[0..n−1], aranan)       ▷ ön koşul: numaraya göre kesin artan
    lo ← 0;  hi ← n                               ▷ aday aralık [lo, hi)
    ▷ değişmez: kayit[0..lo−1] < aranan < kayit[hi..n−1]
    lo < hi olduğu sürece
        orta ← lo + (hi − lo) / 2                 ▷ lo ≤ orta < hi; taşmaz
        eğer kayit[orta] = aranan ise orta'yı döndür
        eğer kayit[orta] < aranan ise lo ← orta + 1   ▷ orta ve solu elendi
        değilse hi ← orta                         ▷ orta ve sağı elendi
    −1 döndür                                     ▷ lo = hi: aday kalmadı
```

![İkili arama daralma şeridi](mini_obs_v2_3_ikili.png)

*Şekil 1. Örnek veride (8 kayıt) 2301010050'nin yarı açık ikili aramayla bulunuşu. Dikey çizgiler aralığın sınırlarıdır: lo dahil, hi hariç. Soluk hücreler değişmez gereği elenmiştir; adımlar `./ara --izle` çıktısından alınmıştır.*

**Doğruluk.** *Başlatma:* lo = 0, hi = n iken değişmezin iki yanı boştur. *Koruma:* `kayit[orta] < aranan` ise dizi sıralı olduğundan `kayit[0..orta]` de küçüktür; lo ← orta + 1 değişmezi korur. `kayit[orta] > aranan` ise `kayit[orta..n−1]` büyüktür; hi ← orta korur. *Sonlanma:* her adımda hi − lo en az 1 azalır; lo = hi olduğunda aday kalmaz ve aranan dizide yoktur.

**Karmaşıklık.** Aralık boyu s, bir adımda ⌊s/2⌋ ya da ⌈s/2⌉ − 1 olur; boy her adımda en az yarıya iner: T(n) = T(n/2) + c → Θ(log n), en çok ⌊log₂ n⌋ + 1 inceleme (Cormen vd., 2022; Knuth, 1998). Elle izleme (birim testleri): 10, 20, …, 80 dizisinde (n = 8) 10'u arayan yarı açık sürüm orta = 4, 2, 1, 0 konumlarını (50, 30, 20, 10) sırayla inceleyip **4** incelemede bulur (= ⌊log₂ 8⌋ + 1); kapalı sürüm orta = 3, 1, 0 (40, 20, 10) ile **3** incelemede bulur. İki sürümün en çok inceleme sayısı aynı sınırdadır; tek tek sorgularda farklı olabilir (Tablo 1'de ortalamaları neredeyse aynıdır).

**Kapalı aralık farkı.** Kapalı sürümde aralık [lo, hi], başlangıç hi = n − 1, döngü koşulu `lo <= hi`, daraltma `hi = orta − 1`. Hata Avcısı bu ikisinin karıştırılmasıdır: yarı açık aralıkta `hi = orta − 1` yazmak `orta − 1` konumunu elenmiş sayar ve o konumdaki kayıt **kaçar** (bölüm 8, `--hata-goster ikili`); kapalı aralıkta `hi = orta` yazmak ise `lo == hi` iken sonsuz döngüye yol açar.

### 4.2 lower_bound ve sıralı ekleme

```
algoritma ALT-SINIR(kayit[0..n−1], x)              ▷ ilk kayit[i] ≥ x
    lo ← 0;  hi ← n                                ▷ değişmez: kayit[0..lo−1] < x ≤ kayit[hi..n−1]
    lo < hi olduğu sürece
        orta ← lo + (hi − lo) / 2
        eğer kayit[orta] < x ise lo ← orta + 1 değilse hi ← orta
    lo döndür

algoritma SIRALI-EKLE(kayit, n, yeni)
    k ← ALT-SINIR(kayit, yeni.no)
    eğer k < n ve kayit[k].no = yeni.no ise "mükerrer" döndür
    kayit[k..n−1]'i bir sağa kaydır (memmove)       ▷ n − k taşıma
    kayit[k] ← yeni;  n ← n + 1
```

`lower_bound` erken çıkış yapmaz: n elemanda ⌊log₂(n + 1)⌋ ya da ⌈log₂(n + 1)⌉ inceleme. Sıralı eklemenin arama kısmı Θ(log n)'dir ama kaydırma O(n)'dir: n kaydın sırayla eklenmesinde toplam taşıma, girdinin **ters çevrim** (inversion) sayısına eşittir — her kayıt, kendisinden önce gelmiş ve kendisinden büyük olan kayıtların sayısı kadar kaydırma yaptırır (kâhin testi bu eşitliği tanımdan, O(n²) sayımla denetler). Karışık sırada beklenen ters çevrim n(n − 1)/4, artan sırada 0, azalan sırada n(n − 1)/2'dir. Ters çevrim kavramı H5'te araya ekleme sıralamasıyla yeniden karşımıza çıkacak: sıralı ekleme, **ikili aramalı araya ekleme sıralamasının** ta kendisidir.

### 4.3 Soyad önekiyle arama

![Soyad dizini: bayt sırası ve Türkçe sıra](mini_obs_v2_3_onek.png)

*Şekil 2. Örnek verinin soyad dizini. Solda v2.3'ün bayt sırası (`strcmp`): "YIL" önekli soyadlar ardışık bir bloktur ve `lower_bound("YIL")` bloğun başını verir. Türkçe harfle başlayan soyadlar (ilk baytı C3 ya da C5) Y'den sonra gelir. Sağda v2.4'te gelecek Türkçe alfabe sırası.*

```
algoritma ÖNEK-ARA(dizin[0..n−1], P)              ▷ dizin (soyad, no) sırasında
    k ← ALT-SINIR(dizin, P)                       ▷ ilk soyad ≥ P
    j ← k
    j < n ve dizin[j].soyad P ile başladığı sürece j ← j + 1
    dizin[k..j−1] döndür                          ▷ Θ(log n + eşleşen)
```

**Neden ardışık?** P'yle başlayan her soyad P'den büyük ya da eşittir; P'yle başlamayan ama P'den büyük bir soyad ise ilk farklı konumda P'den büyük bir bayt taşır ve bu yüzden P'yle başlayan **bütün** soyadlardan büyüktür. Dolayısıyla P'yle başlayanlar `lower_bound(P)`'den başlayan kesintisiz bir bloktur. Bu kanıt herhangi bir sözlük sırası için geçerlidir; v2.4'te Türkçe karşılaştırıcıya geçildiğinde algoritma aynen kalır.

**Dizin kurma.** Kayıtlar numara sırasında dolaşılır ve her işaretçi `ust_sinir` konumuna (aynı soyadlıların **sonuna**) kaydırmayla eklenir: eşit soyadlar numara sırasında kalır (kararlılık; H5). Kurma Θ(n log n) karşılaştırma ve en çok n(n − 1)/2 işaretçi taşıması ister; 10⁵ kayıtta 1 521 295 karşılaştırma, 2 431 766 848 taşıma ve bu makinede 402 ms sürdü. Arama ise Θ(log n + eşleşen): 10⁵ kayıtta "ÖZ" öneki 9 906 kaydı 9 924 karşılaştırmayla buldu.

**Türkçe büyük harf uyumu.** Sorgu, adların kaydedildiği kuralla (`ad_normallestir`) normalleştirilir: "yıl" → "YIL", "i" → "İ", "ç" → "Ç". Normalleştirilmiş UTF-8 dizgiler tam karakterlerden oluştuğu için bayt öneki karakter önekine denktir; çok baytlı bir harf ortasından bölünmez.

### 4.4 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `ikili_ara_no`, `ikili_ara_no_kapali`, `no_alt_sinir` | doğrusal tanım (ilk eşleşen indis; ilk ≥ konum); her denemede kayıtlı bütün numaralar + aralığın altı, her boşluk ve üstü; inceleme ≤ ⌊log₂ n⌋ + 1 |
| `sinif_sirali_ekle` | karıştırılmış kayıtları sona ekleyip `qsort` ile sıralamak; taşıma = ters çevrim sayısı (tanımdan, O(n²)) |
| `csv_oku_kipli(SIRALI)` | `csv_oku` (v1.0, dosya sırası) + `qsort`: aynı durum kodu, aynı hata satırı, aynı kayıtlar |
| `soyad_onek_ara` | bütün kayıtların `strncmp` ile süzülüp (soyad, no) sırasına dizilmesi |

`qsort` yalnızca kâhinde kullanılır (Yol Haritası 6.5).

## 5. Kullanım

### 5.1 `ara`

```
./ara dosya.csv|dosya.dat (--no N | --soyad ÖNEK) [--dogrusal] [--izle] [--goster K]
  --no N       : yarı açık ve kapalı ikili arama; bulunamazsa ekleme konumu
  --dogrusal   : karşılaştırma için doğrusal arama da
  --izle       : yarı açık aramanın her adımı (lo, orta, hi)
  --soyad ÖNEK : soyad dizini + lower_bound + önek denetimi (Türkçe büyük harfe çevrilir)
```

```
$ ./ara ornek_veri/ogrenciler.csv --no 2301010050 --izle --dogrusal
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 (numaraya göre sıralı: EVET)
Süre: yükleme 0.089 ms
Aranan numara: 2301010050
İzleme (yarı açık aralık [lo, hi), orta = lo + (hi - lo) / 2):
  adım  1: lo =       0  hi =       8  orta =       4  kayit[orta].no = 2301010049  < aranan → lo = 5
  adım  2: lo =       5  hi =       8  orta =       6  kayit[orta].no = 2301010051  > aranan → hi = 6
  adım  3: lo =       5  hi =       6  orta =       5  kayit[orta].no = 2301010050  = aranan → bulundu
  izleme 3 adım · ikili_ara_no 3 inceleme: AYNI
İkili arama (yarı açık [lo, hi)) : sıra 6 · 3 inceleme (en çok ⌊log2 n⌋ + 1 = 4)
İkili arama (kapalı [lo, hi])    : sıra 6 · 2 inceleme
Doğrusal arama                   : sıra 6 · 6 karşılaştırma
Öğrenci no  : 2301010050
Ad Soyad    : EMRE ÇINAR
Algoritma ve Prog. I   96.80  AA  BAŞARILI
Matematik I            69.60  CB  BAŞARILI
Fizik I                78.60  BB  BAŞARILI
YANO        : 3.18
Süre: ikili 0.135 µs · doğrusal 0.125 µs
[çıkış kodu: 0]
```

Bulunamayan numarada ekleme konumu (`lower_bound`) yazılır:

```
$ ./ara ornek_veri/ogrenciler.csv --no 2301010044 --izle --dogrusal
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 (numaraya göre sıralı: EVET)
Süre: yükleme 0.082 ms
Aranan numara: 2301010044
İzleme (yarı açık aralık [lo, hi), orta = lo + (hi - lo) / 2):
  adım  1: lo =       0  hi =       8  orta =       4  kayit[orta].no = 2301010049  > aranan → hi = 4
  adım  2: lo =       0  hi =       4  orta =       2  kayit[orta].no = 2301010047  > aranan → hi = 2
  adım  3: lo =       0  hi =       2  orta =       1  kayit[orta].no = 2301010046  > aranan → hi = 1
  adım  4: lo =       0  hi =       1  orta =       0  kayit[orta].no = 2301010045  > aranan → hi = 0
  lo = hi = 0: aralık boş → bulunamadı
  izleme 4 adım · ikili_ara_no 4 inceleme: AYNI
İkili arama (yarı açık [lo, hi)) : bulunamadı (ekleme konumu: sıra 1) · 4 inceleme (en çok ⌊log2 n⌋ + 1 = 4)
```

Soyad öneki (sorgu küçük harfle verildi):

```
$ ./ara ornek_veri/ogrenciler.csv --soyad yıl
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 (numaraya göre sıralı: EVET)
Süre: yükleme 0.089 ms
Soyad dizini: 8 işaretçi, (soyad, no) sırasında (soyad: bayt sırası) · kurma: 15 karşılaştırma, 10 taşıma
Önek: "YIL" (girilen: "yıl") → 2 kayıt (dizin konumu 3–4) · 6 karşılaştırma (lower_bound + önek denetimi)
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   4  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
Süre: dizin kurma 0.001 ms · önek araması 0.247 µs
```

Boş önek bütün kayıtları soyad sırasıyla verir; sıra **bayt** sırasıdır (Şekil 2):

```
$ ./ara ornek_veri/ogrenciler.csv --soyad ''
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 (numaraya göre sıralı: EVET)
Süre: yükleme 0.074 ms
Soyad dizini: 8 işaretçi, (soyad, no) sırasında (soyad: bayt sırası) · kurma: 15 karşılaştırma, 10 taşıma
Önek: "" (girilen: "") → 8 kayıt (dizin konumu 1–8) · 12 karşılaştırma (lower_bound + önek denetimi)
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   7  2301010051  ŞULE DOĞAN                 55.60 DC   56.20 DC   57.60 DC   1.50
   2  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
   1  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   4  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
   5  2301010049  ZEYNEP ÇELİK               76.00 BB   63.00 CC   53.00 DC   2.21
   6  2301010050  EMRE ÇINAR                 96.80 AA   69.60 CB   78.60 BB   3.18
   3  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   8  2301010052  ILGAZ ŞAHİN                36.00 FF   86.80 BA   77.00 BB   2.12
Süre: dizin kurma 0.001 ms · önek araması 0.305 µs
[çıkış kodu: 0]
```

### 5.2 `mini_obs`

Menü ve oturum v2.2 ile aynıdır; farklar: (1) dosya numara sırasına göre yüklenir ve kaydedilir; (2) 1) Öğrenci ekle, kaydı numara sırasındaki yerine koyar; (3) 3) Ara'da `*` ile biten metin soyad önekidir (`yıl*`, `ö*`; yalnızca `*` bütün kayıtları soyad sırasıyla listeler). Örnek oturumun bir bölümü (menü satırları süzüldü):

```
$ printf '3\nyıl*\n3\nö*\n3\nx*\n1\n2301010044\nselin\naksoy\n80\n85\n70\n75\n60\n65\n2\n3\n2301010044\n10\nH\n' | ./mini_obs ornek_veri/ogrenciler.csv      # menü satırları süzüldü
==========================================
  MİNİ-OBS 2 v2.3 · Öğrenci Not Sistemi
==========================================
Yüklendi: 8 kayıt (ornek_veri/ogrenciler.csv)

Seçiminiz (1-10) : Numara ya da ad (soyad öneki: YIL*) : 
--------------------------------- SOYAD ÖNEKİ: YIL*
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   4  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
Eşleşen kayıt: 2 (soyad sırasıyla)

Seçiminiz (1-10) : Numara ya da ad (soyad öneki: YIL*) : 
--------------------------------- SOYAD ÖNEKİ: Ö*
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   3  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
Eşleşen kayıt: 1 (soyad sırasıyla)

Seçiminiz (1-10) : Numara ya da ad (soyad öneki: YIL*) :   Soyadı X ile başlayan kayıt yok.
```

### 5.3 `olcer` — v2.3 işlemleri

```
./olcer dogrusal|ikili|ikili_kapali|bsearch --n N1,N2,... [--tekrar T]
./olcer yukleme|yukleme_v10|ayristirma|sirali_ekleme|anahtar_ekleme --n ... [--sira karisik|artan|azalan]
```

Arama işlemlerinde dizi numaraya göre sıralıdır; her n için **aynı** kayıtlı numaralar aranır (tohum + 3; doğrusal: en çok 1 000, ikili: 100 000 sorgu) ve süre **arama başına** verilir. Yükleme işlemlerinde geçici CSV seçilen sırada yazılır; sayaçlar (karşılaştırma, taşıma) **ısınma** çalıştırmasında toplanır, ölçülen çalıştırmalarda sayaç kapalıdır. `--sira artan` ve `azalan` için kapalı biçim kuramsal değerler programda hesaplanır ve `kuram: UYUMLU/UYUMSUZ` yazılır. CSV sütunları: `islem;n;sira;tekrar;ic_tekrar;ortanca_ms;ortalama_ms;en_az_ms;en_cok_ms;ilk_ms;isinma_ms;kontrol;karsilastirma;tasima`.

## 6. Tasarım kararları

1. **Kayıt dizisinin kendisi sıralı.** v1.0'ın API'si (`Sinif`, `sinif_sil`, raporlar) olduğu gibi kalır, liste numara sırasında görünür ve kaydedilen dosya sıralı olur. Bedel: 144 baytlık kayıtların kaydırılması (bölüm 7.3). Yalnızca 8 baytlık bir numara dizinini sıralı tutmak, aynı karşılaştırma ve taşıma sayılarıyla sıralı ekleme işini 34 kat hızlandırırdı (bölüm 7.4; 32 000 kayıt) ama her silmede dizindeki indisleri de güncellemek gerekirdi. Ölçerek karar vermek bu sürümün dersidir; kalıcı çözüm v2.5'tedir.
2. **Yarı açık aralık birincil sürüm.** [lo, hi) sözleşmesi boş aralığı (lo = hi) ve ekleme konumunu doğal biçimde ifade eder; `lower_bound` ile aynı iskeleti paylaşır. Kapalı sürüm, iki sözleşmenin karıştırılmasından doğan hataları göstermek için tutuldu.
3. **Güvenli orta nokta her yerde.** n ≤ 10⁷ iken `(lo + hi) / 2` taşmaz; ama aynı fonksiyonlar `int` aralığının tamamında doğru olmalıdır. `orta_nokta(1073741824, 2147483647)` testi 1 610 612 735 verir; `(lo + hi) / 2` bu girdide işaretli taşma (tanımsız davranış) olurdu ve test bu yüzden yalnızca güvenli sürümü çalıştırır.
4. **v1.0 akış okuyucuları korundu.** `csv_oku`/`ikili_oku` dosya sırasını korur; v2.3 yükleyicisi `csv_oku_kipli(..., YUKLEME_SIRALI)`dır. Böylece eski testler değişmeden geçer ve eski yükleyici yenisinin kâhini olur. İki kipte bozuk ya da mükerrer satır **aynı satır numarasıyla** bildirilir: mükerrer numara, kendisinden önce okunmuş kayıtlar arasında arandığı için ikisi de numaranın ikinci kez görüldüğü ilk satırda durur.
5. **Soyad dizini işaretçilerden ve her aramada yeniden.** Dizin kayıt dizisinin içini gösterdiği için ekleme (realloc) ve silme onu geçersiz kılar. Menüde dizin her önek aramasında kurulur: menü boyutlarında (≤ 10⁴ kayıt) anlıktır; 10⁵ kayıtta yarım saniyedir. Dizini kalıcı tutup güncellemek ileri alıştırmadır.
6. **Bayt sırası bilinçli olarak bırakıldı.** `strcmp` önek araması için doğrudur (her sözlük sırası olur) ama Türkçe için yanlış sırayla listeler (Şekil 2). Türkçe alfabe karşılaştırıcısı H5'in (v2.4) konusudur; önek algoritması değişmeyecektir.
7. **Taşıma sayacı.** `Sayac`'a `tasima` alanı eklendi; `sayac_yaz` taşıma sıfırsa v2.2'nin biçimini aynen korur, böylece eski işlemlerin çıktıları değişmez.
8. **Ölçüm düzeneği algoritma değildir.** Arama ölçümlerinde sıralı dizi, üretecin numaralarının TABAN + 1 … TABAN + n permütasyonu olmasından yararlanılarak her kaydı `no − TABAN − 1` konumuna koyarak Θ(n)'de kurulur (`sirala_yerlestir`). Bu bir sıralama algoritması değildir, yalnızca bu üretece özgü bir düzenektir; sıralama algoritmaları H5–H7'de gelir.
9. **Sayım ısınmada.** 10⁵ kayıtlık bir yükleme ≈ 20 s sürdüğü için sayaçlar ayrı bir sayım çalıştırması yerine ölçülmeyen ısınma çalıştırmasında toplanır; ölçülen çalıştırmalar sayaçsızdır.

## 7. Ölçümler

### 7.1 Ölçüm düzeni ve ortam

Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB (2 × 1 MiB), L3 33 MiB; gcc 13.3.0, `-std=c17 -Wall -Wextra -pedantic -O2 -g`; tarih 2026-10-13 07:22. Düzen: 1 ısınma + 5 tekrar, ortanca (Sedgewick & Wayne, 2011). Pahalı yüklemelerde tekrar azaltıldı: 32 000 kayıtta 3, 64 000 ve 100 000 kayıtta 1 tekrar (tablolarda parantez içinde). Veri: `veri_uret` üreteci, tohum 42, yinelenen yok. `make olcum` toplam 2 dakika 51 s sürdü. Makine başka işlerle paylaşıldığı için ölçümler gürültülüdür; sayaçlar deterministiktir, süreler bu makineye özgüdür.

### 7.2 Arama: doğrusal ve ikili

| n | doğrusal | ikili (yarı açık) | ikili (kapalı) | bsearch | doğrusal / ikili | doğrusal: ort. karş. | yarı açık: ort. inceleme | kapalı: ort. inceleme | ⌊log₂ n⌋ + 1 |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 10 | 15 ns | 25 ns | 24 ns | 35 ns | 0,6 | 5,6 | 2,89 | 2,90 | 4 |
| 100 | 56 ns | 46 ns | 48 ns | 70 ns | 1,2 | 51,3 | 5,80 | 5,80 | 7 |
| 1 000 | 466 ns | 77 ns | 71 ns | 114 ns | 6,1 | 495,9 | 8,99 | 8,99 | 10 |
| 10 000 | 5,3 µs | 117 ns | 132 ns | 124 ns | 45 | 4 994,9 | 12,36 | 12,36 | 14 |
| 100 000 | 190,5 µs | 261 ns | 258 ns | 392 ns | 730 | 52 339,9 | 15,69 | 15,69 | 17 |
| 1 000 000 | 6,84 ms | 757 ns | 1,0 µs | 967 ns | 9 041 | 463 565,9 | 18,95 | 18,95 | 20 |

*Tablo 1. Numaraya göre sıralı dizide kayıtlı numaraların aranması (ortanca, arama başına). "ort. karş./inceleme": sayaçtan, arama başına ortalama.*

![Arama süreleri](mini_obs_v2_3_olcum_arama.png)

*Şekil 3. Arama başına süre (log–log). Doğrusal arama n ile orantılı büyür; üç ikili arama (iki gerçekleştirim ve `bsearch`) log n ile, çok yavaş büyür.*

Yorum:

- **10⁵ kayıtta** doğrusal arama 190,5 µs, ikili arama 261 ns sürer: **730 kat**; 10⁶ kayıtta fark 9 041 kata çıkar. Sayaçlar kuramla uyumludur: doğrusal aramada ortalama karşılaştırma ≈ (n + 1)/2 (10⁵'te 52 340; yalnızca 100 sorgu olduğu için ±%5 oynar), ikili aramada ortalama inceleme ⌊log₂ n⌋ + 1'in hemen altındadır (10⁵'te 15,69, sınır 17): kayıtların yaklaşık yarısı ağacın en alt düzeyindedir.
- **Küçük n'de doğrusal arama kazanır:** n = 10'da doğrusal 15 ns, ikili 25 ns; n = 100'de doğrusal 56 ns, ikili 46 ns. Doğrusal arama ardışık belleği tarar ve dalı kolay tahmin edilir; ikili aramanın her adımı tahmin edilemeyen bir daldır. Kesişim bu makinede 10 ile 100 kayıt arasındadır (H4 deneyinin konusu).
- **İkili aramanın süresi log n'den hızlı büyür:** sayaç 10³'ten 10⁶'ya yalnızca 2,1 katına çıkarken süre 10 katına çıkar. Sebep önbellektir: 10⁶ kayıt 144 MB'tır ve L3'e (33 MiB) sığmaz; her inceleme farklı bir bellek bölgesine sıçrar ve çoğu inceleme bir önbellek ıskasıdır. Karmaşıklık işlem sayısını, önbellek ise işlem başına maliyeti belirler.
- Yarı açık, kapalı ve `bsearch` sürümleri aynı büyüme sınıfındadır; aralarındaki farklar (ortanca ile en az süre arasındaki aralıkla karşılaştırılabilir büyüklükte) sabit çarpan ve ölçüm gürültüsüdür. Bu ölçümden "biri ötekinden hızlıdır" sonucu çıkarılmamalıdır.

### 7.3 Yükleme: v1.0 ve v2.3

| n | ayrıştırma (taban) | v1.0 (doğrusal denetim) | v2.3 karışık | v2.3 / v1.0 | v2.3 artan (en iyi) | v2.3 azalan (en kötü) |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 2,4 ms | 1,8 ms | 1,9 ms | 1,08 | 3,4 ms | 3,9 ms |
| 2 000 | 4,5 ms | 4,6 ms | 5,1 ms | 1,10 | 3,3 ms | 10,9 ms |
| 4 000 | 8,4 ms | 13,4 ms | 16,5 ms | 1,23 | 5,2 ms | 31,3 ms |
| 8 000 | 15,4 ms | 42,6 ms | 74,6 ms | 1,75 | 17,1 ms | 123,3 ms |
| 16 000 | 23,2 ms | 214,2 ms | 375,5 ms | 1,75 | 33,4 ms | 812,3 ms |
| 32 000 | 43,1 ms | 1,51 s (3) | 1,53 s (3) | 1,02 | 62,0 ms | 3,47 s (3) |
| 64 000 | 79,1 ms | 6,59 s (1) | 7,37 s (1) | 1,12 | 79,9 ms | — |
| 100 000 | 121,0 ms | 19,05 s (1) | 20,75 s (1) | 1,09 | 176,8 ms | — |

*Tablo 2. CSV yükleme süreleri (ortanca; parantez: tekrar sayısı). "Ayrıştırma": mükerrer denetimi yapmayan okuma, iki yükleyicinin ortak taban maliyeti.*

| n | v1.0 karşılaştırma = n(n−1)/2 | v2.3 karşılaştırma | oran | v2.3 taşıma | taşıma / (n²/4) | kaydırılan bayt (GB) |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 499 500 | 9 587 | 52 | 255 893 | 1,024 | 0,04 |
| 2 000 | 1 999 000 | 21 129 | 95 | 1 005 991 | 1,006 | 0,14 |
| 4 000 | 7 998 000 | 46 355 | 173 | 4 043 489 | 1,011 | 0,58 |
| 8 000 | 31 996 000 | 100 666 | 318 | 15 995 770 | 1,000 | 2,30 |
| 16 000 | 127 992 000 | 217 294 | 589 | 64 542 091 | 1,008 | 9,29 |
| 32 000 | 511 984 000 | 466 615 | 1 097 | 257 145 963 | 1,004 | 37,0 |
| 64 000 | 2 047 968 000 | 997 068 | 2 054 | 1 023 493 768 | 1,000 | 147,4 |
| 100 000 | 4 999 950 000 | 1 622 620 | 3 081 | 2 495 087 143 | 0,998 | 359,3 |

*Tablo 3. Karışık sıralı dosyada sayaçlar (ısınma çalıştırmasından). Taşıma ≈ n²/4: girdinin ters çevrim sayısı. Bayt: taşıma × 144.*

![Yükleme süreleri ve sayaçlar](mini_obs_v2_3_olcum_yukleme.png)

*Şekil 4. Solda yükleme süreleri, sağda karışık sıralı dosyada sayaçlar (log–log). v1.0 ile v2.3'ün süre eğrileri neredeyse üst üstedir; sağda v2.3'ün karşılaştırması n log n ile, taşıması n² ile büyür.*

Yorum:

- **Karşılaştırma 3 081 kat azaldı, süre azalmadı.** 10⁵ kayıtta v1.0 4 999 950 000 karşılaştırma yapar ve 19,05 s sürer; v2.3 yalnızca 1 622 620 karşılaştırma yapar ama 2 495 087 143 kayıt taşır ve 20,75 s sürer (v1.0'ın 1,09 katı). Her taşıma 144 baytlık bir kaydın kopyasıdır: toplam ≈ 359 GB. Ayrıştırma payı çıkarılınca bu, saniyede ≈ 17,4 GB'lık bir kopyalama hızına, taşınan kayıt başına ≈ 8,3 ns'ye karşılık gelir; memmove hızlıdır ama n² tane kayıt taşımak yine n² iştir.
- **Büyüme sınıfı değişmedi:** n iki katına çıkınca v2.3'ün süresi (n ≥ 16 000) 5,03, 4,08, 4,81 katına çıkar — karesel algoritmanın beklenen değeri 4'tür; 4'ün üstündeki sapma dizinin önbellek sınırlarını aşmasındandır. **Asimptotik sınıfı belirleyen işlem, sayılması en kolay olan değil, en çok yapılandır**: v2.3'te bu karşılaştırma değil taşımadır.
- **Girdi sırası belirleyicidir:** dosya numara sırasındaysa (artan) taşıma sıfırdır ve 10⁵ kayıt 176,8 ms'de yüklenir — ayrıştırmanın kendisi 121,0 ms'dir; yani v2.3 yükleyicisi bu durumda Θ(n log n) karşılaştırmayla neredeyse bedavadır. Ters sırada (azalan) taşıma n(n − 1)/2'ye çıkar: 32 000 kayıtta 511 984 000 taşıma (karışık sıranın 1,99 katı) ve 2,26 kat süre. v2.3 dosyayı numara sırasında **kaydettiği** için bir kez yüklenip kaydedilen dosyanın sonraki yüklemeleri en iyi durumdadır; kötü durum, dışarıdan gelen (ör. üretilmiş ya da başka bir sistemden aktarılmış) sırasız dosyadır.
- Artan ve azalan sıradaki sayaçlar programın hesapladığı kapalı biçim değerlerle karşılaştırıldı: ölçüm günlüğündeki 22 satırın hepsi `kuram: UYUMLU` (0 uyumsuz).

### 7.4 Kaydırmanın bedeli: taşınan bayt

| n | taşıma (iki işlemde aynı) | kayıt ekleme (144 B) | numara ekleme (8 B) | kayıt / numara |
|--:|--:|--:|--:|--:|
| 1 000 | 255 893 | 934,4 µs | 82,0 µs | 11,4 |
| 2 000 | 1 005 991 | 3,4 ms | 232,9 µs | 14,8 |
| 4 000 | 4 043 489 | 13,8 ms | 710,7 µs | 19,4 |
| 8 000 | 15 995 770 | 49,7 ms | 2,6 ms | 19,1 |
| 16 000 | 64 542 091 | 289,7 ms | 10,4 ms | 27,9 |
| 32 000 | 257 145 963 | 1,39 s | 40,4 ms | 34,5 |
| 64 000 | 1 023 493 768 | — | 155,1 ms | — |
| 100 000 | 2 495 087 143 | — | 415,8 ms | — |

*Tablo 4. Bellekte n kaydın karışık sırayla sıralı eklenmesi (ayrıştırma yok). İki işlem aynı algoritmayı çalıştırır ve aynı sayıda karşılaştırma ve taşıma yapar; tek fark taşınan öğenin boyutudur (144 B kayıt ↔ 8 B numara).*

Aynı sayıda taşıma, öğe 144 bayttan 8 bayta inince 32 000 kayıtta **34 kat** hızlanır; bayt oranı 18'dir, aradaki fark önbellek etkisidir (32 000 numara 256 KB'tır, L2'ye sığar; 32 000 kayıt 4,6 MB'tır). 8 baytlık sürüm 10⁵ kayıtta bile 415,8 ms sürer. Bu, H5'in "büyük kayıtları taşımak yerine indis ya da işaretçi dizisini sırala" ilkesinin ölçülmüş biçimidir; v2.4'teki sıralı listeler bu yüzden işaretçi dizileri üzerinde çalışacak.

### 7.5 10⁶ kayıt için kestirim

10⁶ kayıtlık karışık sıralı dosyada taşıma ≈ n(n − 1)/4 ≈ 2,5 · 10¹¹ olur. 10⁵ kayıtta ölçülen taşıma başına maliyetle (8,3 ns) ve on kat ayrıştırma payıyla yükleme ≈ **34 dakika** sürerdi (**kestirim**; yöntem: maliyet = taşıma × taşıma başına süre + 10 × T_ayrıştırma(10⁵)). Bu bir alt sınırdır: 10⁶ kayıt (144 MB) L3'e sığmadığı için taşıma başına maliyet artacaktır. v2.0'ın v1.0 yükleyicisi için yaptığı kestirim ≈ 1,6 saatti. İki kestirim de pratik değildir; bu yüzden ölçmedik.

### 7.6 Sonuç ve v2.5'e köprü

v2.3, sorgu tarafında sözünü tutar: numarayla arama 730 kat (10⁵) hızlandı ve menüdeki her "numara sor" işlemi artık Θ(log n)'dir. Yükleme tarafında ise "karşılaştırmayı azalttık, öyleyse hızlandık" çıkarımının yanlış olduğunu ölçtük. Çözüm, kayıtları tek tek yerine yerleştirmek yerine **önce hepsini okuyup sonra bir kez sıralamaktır**: v2.5'te toplu yükleme + birleştirmeli sıralama (Θ(n log n) karşılaştırma **ve** Θ(n log n) taşıma) + komşu karşılaştırmayla mükerrer denetimi aynı sonucu verecek; v2.3 yükleyicisi (ve onun kâhini v1.0) o sürümün kâhini olacaktır.

## 8. Testler

- **Birim testleri** (`obs_test`): `177 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama`. Arama testleri: güvenli orta nokta (int sınırında dahil); `sinif_sirali_mi` (sırasız ve eşit numaralı diziler); 7 ve 8 elemanlı dizilerde yarı açık ve kapalı arama (her konum, aralık altı/arası/üstü) ve **elle izlenen inceleme sayıları** (n = 7: 40 → 1, 10/70/35 → 3'er; n = 8: 10 → yarı açık 4, kapalı 3); `lower_bound` konumları ve inceleme sınırları; boş dizi; 50, 30, 40, 10, 20 sırasıyla sıralı ekleme (konumlar 0, 0, 1, 0, 1; taşıma 8 = ters çevrim; karşılaştırma 12) ve mükerrer ekleme; yükleme kipleri (dosya sırası ↔ numara sırası, ikili dosya, iki kipte aynı hata satırı, sıralı dosyada taşıma 0); `alt/ust_sinir_genel` (tekrar eden anahtarlar); soyad dizininin bayt sırası; "YIL", "ÖZ", "Ç", "Z", "", "YILMAZLAR" önekleri ve "yıl", " öz ", "çe", "i" sorgularının normalleştirilmesi.
- **Kâhin testleri** (`test_kahin`): 300 denemede 297 205, 1 000 denemede 979 964 denetim (ikili arama ↔ doğrusal: 767 128; sıralı ekleme/yükleme ve önek: 23 559), uyuşmazlık yok. Her denemede 0–300 kayıtlık, boşluklu kesin artan numaralar; dizinin karıştırılmış kopyası; olasılığı üçte bir olan bir mükerrer numara; 12 sabit (Türkçe küçük harfli olanlar dahil) ve 6 rastgele (var olan soyadların harf sınırında kesilmiş) önek.
- **Kasıtlı hata** (`--hata-goster ikili`): yarı açık aramada `hi = orta − 1` (kapalı aralık alışkanlığı). Kâhin hatayı yakalar ve karşı örneği **küçültür**:

```
$ ./test_kahin --hata-goster ikili
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : ikili_ara_no / kapalı / no_alt_sinir
  n          : 66
  Beklenen   : indis 0, lower_bound 0; inceleme <= 7 (lower_bound 6..7)
  Bulunan    : yarı açık -1 (5), kapalı 0 (6), lower_bound 0 (7)
  Aranan numara: 1
  Küçültülmüş karşı örnek (ilk 2 kayıt): numara 1; beklenen 0, bulunan -1
  Karşı örnek: numaralar = [1, 4]
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster ikili
```

  İki kayıtlık [1, 4] dizisinde 1 aranırken ilk orta 1'dir (4 > 1); hatalı daraltma hi = 0 yapar ve 0. konumdaki 1 hiç incelenmeden elenir. Değişmez "kayit[hi..n−1] > aranan" bozulmuştur: `kayit[0]` = aranan, hi'nin sağına düşmüştür.
- **Bellek**: `make asan` temiz (`ara`, `mini_obs` önek oturumu, `olcer`'in yeni işlemleri dahil).

## 9. Ders notu için özet (Hafta 4 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'nin kayıt dizisini numaraya göre sıralı tutuyor, numarayla bulmayı ikili aramaya çeviriyor, soyad önekiyle arama ekliyor ve doğrusal ile ikili aramayı 10⁵ kayıtta karşılaştırmalı ölçüyoruz. Yükleyicinin mükerrer denetimi de ikili aramaya geçiyor; bunun karşılaştırmayı neden azalttığını ama süreyi neden azaltmadığını ölçerek göstereceğiz.

### Gereksinimler

- `arama.h/.c`: `orta_nokta`, `sinif_sirali_mi`, `ikili_ara_no_say` (yarı açık [lo, hi), erken çıkışlı), `ikili_ara_no_kapali_say` (kapalı [lo, hi]), `no_alt_sinir_say` (lower_bound), `sinif_sirali_ekle_say` (lower_bound + memmove; mükerrerde −1), soyad dizini (`soyad_dizini_kur`: upper_bound ile kararlı ekleme) ve `soyad_onek_ara` (lower_bound + önek denetimi). Her fonksiyonun başında ön/son koşul ve döngü değişmezi yorumu.
- Değişmez: `mini_obs`'un kayıt dizisi her an numaraya göre **kesin artan**dır. `sinif_yukle` sıralı kipte yükler; menüden ekleme sıralı konuma yapar; numarayla bulan her menü işlemi ikili arama kullanır.
- Orta nokta yalnızca `lo + (hi − lo) / 2` ile hesaplanır.
- Mükerrer numara satırı v1.0'daki **aynı satır numarasıyla** bildirilir.
- Menü 3: `*` ile biten metin soyad önekidir; sorgu `ad_normallestir` ile Türkçe büyük harfe çevrilir.
- `ara` programı: `--no N` (`--izle`, `--dogrusal`), `--soyad ÖNEK`, `--goster K`; çıkış kodları 0/1/2.
- `olcer`: en az `dogrusal`, `ikili`, `yukleme` ve `yukleme_v10`; `--sira artan|azalan` ile en iyi/en kötü durum; CSV'de karşılaştırma ve taşıma sayaçları.
- `test_obs.c`: elle izlenmiş inceleme sayıları; `test_kahin.c`: doğrusal kâhin, qsort kâhini, ters çevrim kâhini; `--hata-goster ikili`.
- Ölçüm raporu: arama başına süre (n = 10 … 10⁶, en az 10⁵ dahil) ve yükleme süresi (n = 10³ … ≥ 6,4 · 10⁴) tabloları, log–log grafikler, sayaçların kuramla karşılaştırılması ve yorum.

### İpuçları

- İkili aramayı yazmadan önce **değişmezi** yazın ve her daraltmanın onu koruduğunu kâğıt üstünde gösterin. Yarı açık aralıkta `hi = orta`, kapalı aralıkta `hi = orta − 1`; karıştırmak ya kayıt kaçırır ya sonsuz döngü üretir.
- `lower_bound` hem "var mı?" hem "nereye eklenir?" sorusunu yanıtlar: `k < n && kayit[k].no == no` ise var; değilse ekleme konumu k'dir.
- Kaydırmayı döngüyle değil `memmove` ile yapın (örtüşen bölgede `memcpy` tanımsız davranıştır). Eklemeden önce kapasiteyi büyütmeyi unutmayın.
- Sıralı ekleme yaparken taşıma sayısını da sayın: karışık sırada ≈ n²/4 olduğunu görünce süre ölçümü sizi şaşırtmayacak.
- Önek aramasında karşılaştırıcı ile önek denetimi **aynı sırayı** kullanmalıdır (v2.3: bayt sırası, `strcmp`/`strncmp`).
- Sorguyu ve kayıtları aynı kuralla normalleştirin; "yıl" ile "YIL" aynı önek olmalıdır.
- Ölçüm verisini kurarken sıralı diziyi "hile" ile (bölüm 6.8) kurmak ölçüm düzeneğidir; algoritma olarak kendi sıralı eklemenizi kullanın.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri ve `test_kahin` (300 deneme) geçer.
2. `./ara ornek_veri/ogrenciler.csv --no 2301010050 --izle`: ortalar sırasıyla 4, 6, 5; kayıt 3 incelemede bulunur (sıra 6, EMRE ÇINAR); `--no 2301010044`: "bulunamadı (ekleme konumu: sıra 1)".
3. `./ara ornek_veri/ogrenciler.csv --soyad yıl` → 2 kayıt (2301010045 AYŞE NUR YILMAZ, 2301010048 CAN YILMAZ), bu sırayla; `--soyad ç` → ZEYNEP ÇELİK ve EMRE ÇINAR; `--soyad i` → 0 kayıt ("İ" ile başlayan soyad yok).
4. 10⁵ kayıt (`veri_uret --n 100000 --tohum 42`): `./ara u.csv --no 2400050000` en çok 17 incelemede bulur; `--dogrusal` ile doğrusal arama 50 000 karşılaştırma yapar.
5. Sırasız bir CSV `mini_obs` ile açılıp kaydedilince dosya numara sırasında yazılır; menü 2 listesi numara sırasındadır; menü 1 ile en küçük numarayı eklemek kaydı sıra 1'e koyar.
6. Mükerrer numaralı dosya v1.0 ile **aynı satır numarasıyla** reddedilir (ör. `testler/yinelenen_k3.csv` → "dosya biçimi hatalı (satır 12)" hem v1.0 hem v2.3).
7. Sayaçlar: `./olcer yukleme --sira azalan --n 1000` → taşıma 499 500 ve `kuram: UYUMLU`; `--sira artan` → taşıma 0, `kuram: UYUMLU`; `./olcer yukleme_v10 --n 1000` → karşılaştırma 499 500.
8. Kendi makinenizde 10⁵ kayıtta ikili arama doğrusal aramadan en az 100 kat hızlıdır (bu makinede 730 kat).
9. Rapor, 10⁵ kayıtlık karışık dosyada v2.3 yükleyicisinin karşılaştırma ve taşıma sayılarını ve süresini v1.0 ile karşılaştırır ve "neden hızlanmadı?" sorusunu taşınan bayt üzerinden yanıtlar.
10. `./test_kahin --hata-goster ikili` uyuşmazlığı ve küçültülmüş karşı örneği basar, 1 ile çıkar; `make asan` temizdir.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | `ara ornek_veri/ogrenciler.csv --no 2301010050 --izle` | 3 adım (orta 4, 6, 5), sıra 6 |
| 2 | aynı dosya, `--no 2301010099` | bulunamadı, ekleme konumu sıra 9; 3 inceleme |
| 3 | aynı dosya, `--no 2301010044` | bulunamadı, ekleme konumu sıra 1; 4 inceleme |
| 4 | aynı dosya, `--soyad yıl` | 2 kayıt: …045, …048 (numara sırasında) |
| 5 | aynı dosya, `--soyad ''` | 8 kayıt, bayt sırası: DOĞAN, KAYA, YILMAZ, YILMAZ, ÇELİK, ÇINAR, ÖZTÜRK, ŞAHİN |
| 6 | `mini_obs`, menü 3: `x*` | "Soyadı X ile başlayan kayıt yok." |
| 7 | `mini_obs`, menü 1: numara 2301010044 | kayıt sıra 1'e eklenir; menü 2'de ilk satır |
| 8 | sırasız 3 kayıtlı CSV (30, 10, 20), menü 9 | dosya 10, 20, 30 sırasıyla yazılır |
| 9 | `testler/bozuk.csv` | "dosya biçimi hatalı (satır 3)", çıkış 1 |
| 10 | `olcer yukleme --sira azalan --n 1000,2000` | taşıma 499 500 ve 1 999 000; kuram UYUMLU |
| 11 | `olcer ikili --n 100000` | arama başına ortalama inceleme ≤ 17 |
| 12 | `test_kahin --hata-goster ikili` | KÂHİN UYUŞMAZLIĞI; küçültülmüş örnek [1, 4], numara 1; çıkış 1 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.2'niz (ya da referans v2.2), `arama.h` (bildirimler, sözleşmeler, değişmezler), `dosya.h`'deki `YuklemeKipi` bildirimi, `sayac.h`'nin `tasima` alanı, `olcer`'in ölçüm düzeneği (`sirala_yerlestir`, `--sira`).
- **Yazılır:** `arama.c`; `dosya.c`'de `kayit_yerlestir` ve kipli okuyucular; `main.c`'de ikili aramaya geçiş ve önek araması; `ara.c`; `olcer.c`'ye arama ve yükleme işlemleri; `test_obs.c` ve `test_kahin.c`'ye arama testleri; `Makefile`'a `ara` ve yeni `olcum` adımları.
- **Değiştirilmez:** v1.0'ın kuralları ve dosya biçimleri, `csv_oku`/`ikili_oku`'nun dosya sırası davranışı (kâhin), ortak modüller.
- **Meydan okuma:** (a) soyad dizinini kalıcı tutun ve ekleme/silmede güncelleyin; (b) mükerrer denetimini yalnızca 8 baytlık bir numara dizini üzerinde yapıp kayıtları sona ekleyen bir yükleyici yazın ve süresini Tablo 2 ile karşılaştırın (dikkat: kayıt dizisi artık sıralı değildir — ikili arama için dizine bakmanız gerekir); (c) `lower_bound` + `upper_bound` ile "soyadı tam olarak YILMAZ olanların sayısı"nı Θ(log n)'de bulun.

## 10. Bilinen sınırlılıklar

- Karışık sıralı büyük dosyaların yüklenmesi karesel kalır (10⁵ kayıt ≈ 21 s; 10⁶ için kestirim ≈ 34 dakika). Çözüm v2.5'tedir.
- Soyad dizini her önek aramasında yeniden kurulur ve kurma karesel sayıda işaretçi taşıması ister (10⁵ kayıtta 402 ms).
- Soyad sırası bayt sırasıdır; Türkçe alfabe sırası v2.4'te gelir. Tam ad araması (`sinif_isim_bul`) doğrusal kalır; ad içinde alt dizgi araması v2.9'da (Rabin–Karp).
- Ölçümdeki sıralı dizi kurulumu yalnızca bu üretecin (ardışık numaralar, yinelenen yok) verisi için geçerlidir.
- Süreler tek bir, paylaşılan sanal makinede ölçülmüştür; ikili aramanın üç sürümü arasındaki küçük farklar gürültü düzeyindedir. Sayaçlar makineden bağımsızdır.

## 11. Kaynaklar

- Bloch, J. (2006, June 2). *Extra, extra – read all about it: Nearly all binary searches and mergesorts are broken*. Google Research Blog. https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Knuth, D. E. (1998). *The art of computer programming: Vol. 3. Sorting and searching* (2nd ed.). Addison-Wesley.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
- t0st. (2021, February 28). *How I cut GTA Online loading times by 70%*. https://nee.lv/2021/02/28/How-I-cut-GTA-Online-loading-times-by-70/
