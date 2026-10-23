# Mini-OBS 2 v2.4 — Temel Sıralama: çok ölçütlü sıralı listeler ve Türkçe karşılaştırıcı (Hafta 5)

**Bu sürümün amacı:** Mini-OBS'ye **sıralı listeler** eklemek — ortalamaya (YANO) göre başarı sırası (eşitlikte soyad, sonra ad), soyada göre liste, ders ortalamasına göre liste — ve bunu yaparken Hafta 5'in üç sorusunu proje üzerinde yanıtlamak: (1) **karşılaştırıcı** nasıl yazılır (qsort arayüzü, taşmaya güvenli fark, çok anahtarlı sözlük sırası); (2) Türkçe adlar **nasıl doğru sıralanır** (`strcmp`'nin bayt sırası "ÇELİK"i "DEMİR"den sonraya koyar; `tr_karsilastir` UTF-8'i kod noktalarına çözüp Türkçe alfabe sırasıyla karşılaştırır); (3) **kararlılık** neden önemlidir (eşit kayıtların sırasını koruyan araya ekleme ve kabarcık sıralaması ile korumayan seçmeli sıralama; kararlı geçişlerle çok anahtarlı sıralama). Seçmeli, kabarcık ve araya ekleme sıralaması `qsort` ile aynı arayüzde (taban, n, boyut, karşılaştırıcı) gerçeklenir ve kayıtların kendisi yerine **işaretçi dizilerini** sıralar. Her sonuç `qsort` + numarayla tamamlanmış ölçüt **kâhinine** karşı sınanır. Ölçüm: n = 4 000 kayıtlık başarı listesinde araya ekleme 146,2 ms, seçmeli 358,0 ms, kabarcık 1,24 s, `qsort` 6,5 ms sürer; sıralı girdide araya ekleme 904,6 µs'ye iner.

Dosyalar (satır sayılarıyla): `turkce.h` (51) · `turkce.c` (135) · `siralama.h` (47) · `siralama.c` (141) · `liste.h` (90) · `liste.c` (264) · `listele.c` (203) · `arama.h` (119) · `arama.c` (258) · `ara.c` (232) · `obs.h` (140) · `obs.c` (673) · `main.c` (338) · `olcer.c` (1018) · `test_obs.c` (1308) · `test_kahin.c` (1645) · `dosya.h` (93) · `dosya.c` (381) · `sayac.h` (49) · `sayac.c` (21) · `metin.h` (35) · `metin.c` (340) · `yinelenen.h` (43) · `yinelenen.c` (71) · `denetle.c` (140) · `secmeli.h` (102) · `secmeli.c` (330) · `ders_sec.c` (184) · `uretec.h` (54) · `uretec.c` (160) · `veri_uret.c` (94) · `deney.h` (28) · `deney.c` (32) · `ortak_rastgele.h` (43) · `ortak_rastgele.c` (50) · `zamanlayici.h` (34) · `zamanlayici.c` (63) · `Makefile` (229) · `testler/kararlilik.csv` (8 kayıt; eşit anahtarlı üç kayıt) ve önceki sürümlerin test girdileri · `olcum/siralama.csv`, `olcum/karsilastirici.csv`, `olcum/tasima.csv`, `olcum/esitlik.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_4_ciktilar.txt` (805 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_4_karsilastirici.png`, `mini_obs_v2_4_kararlilik.png`; grafikler: `mini_obs_v2_4_isi_haritasi.png`, `mini_obs_v2_4_olcum_sure.png`.

Derleme: `make` (`mini_obs`, `veri_uret`, `olcer`, `denetle`, `ders_sec`, `ara`, **`listele`**), `make test`, `make olcum` (bu makinede 1 dakika 28 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 23 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0, 1 (dosya okunamadı, bellek yetersiz ya da `--denetle` bir uyuşmazlık buldu; testlerde uyuşmazlık), 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 5'in Büyük Sorusu: elinizdeki iskambil kâğıtlarını sıralarken hangi algoritmayı kullanıyorsunuz ve bir milyon tamsayıyı sıralamak için kabarcık sıralaması neden "yanlış yol"dur? Mini-OBS'de "kâğıtlar" öğrenci kayıtlarıdır:

- **Üç temel algoritma ve değişmezleri** (ÖÇ 5.1): seçmeli (önek sıralı ve dizinin en küçükleri), kabarcık (her geçişte en büyük yerine), araya ekleme (önek sıralı; kart sıralama analojisi).
- **Karşılaştırma, takas, kararlılık, uyarlanabilirlik** (ÖÇ 5.2–5.3): sayaçlar her algoritmanın ve girdi türünün imzasını verir: seçmeli her girdide tam n(n − 1)/2 karşılaştırma; kabarcığın takas sayısı ve araya eklemenin kaydırma sayısı tam olarak **ters çevrim** sayısıdır (v2.3'te sıralı eklemenin taşıması da buydu).
- **Karşılaştırıcılar** (ÖÇ 5.4): qsort arayüzü (`int (*)(const void *, const void *)`), taşmaya güvenli `(x > y) − (x < y)`, çok anahtarlı sözlük sırası, Türkçe alfabe.
- **Kararlılık deneyi** (ÖÇ 5.5): kararlı geçişlerle çok anahtarlı sıralama = tek karşılaştırıcılı sıralama; kararsız algoritmayla değil.
- **Mühendis gözüyle — kütüphaneyi kullan ama güvencesini oku:** C'nin `qsort`'u algoritma ve kararlılık güvencesi vermez. Bu makinedeki glibc `qsort`'u testlerimizde eşit kayıtları numara sırasında bıraktı; ama başka bir kütüphanede bırakmayabilir. Bu yüzden kâhin, numarayı son anahtar olarak ekleyen **tam** ölçütü kullanır.

Yol haritasındaki karşılığı (Tablo A.1): **H5 · v2.4 · Çok ölçütlü sıralı listeler; Türkçe alfabetik karşılaştırıcı · Karşılaştırıcı, kararlılık.** v2.3'ün soyad önek araması da bu sürümde Türkçe sıraya geçer (aynı lower_bound algoritması, yeni karşılaştırıcı).

## 2. v2.3'ten ne değişti?

| Konu | v2.3 (H4) | v2.4 (H5) |
|---|---|---|
| Sıralı listeler | yok (yalnız numara sırası) | **`listele`**: başarı, soyad, ad, numara, ALG/MAT/FIZ ortalaması; 5 yöntem; `--denetle` |
| Dizgi karşılaştırma | `strcmp` (bayt) | **`turkce.h/.c`**: `utf8_coz`, `tr_sira_degeri`, `tr_karsilastir` (tam sıralama), `tr_birincil_karsilastir`, `tr_onek_mi` |
| Sıralama algoritmaları | — | **`siralama.h/.c`**: `secmeli_sirala_say`, `kabarcik_sirala_say`, `araya_ekleme_sirala_say` (qsort arayüzü + sayaç), `sirali_mi_genel` |
| Karşılaştırıcılar | — | **`liste.h/.c`**: 8 ölçüt × (numarasız, numarayla tamamlanmış), tek anahtarlılar; `liste_sirala`, `cok_gecisli_sirala`, `esitler_numara_sirasinda` |
| Soyad öneki (menü 3, `ara`) | bayt sırası | **Türkçe sıra** (`soyad_dizini_kur_tr`); v2.3'ün bayt dizini korunur |
| `obs` | — | + `ogrenci_yano100` (tamsayı YANO), `sira_listesi_yaz` |
| `olcer` | arama, yükleme | + `liste_secmeli/kabarcik/araya/qsort/cok_gecisli`, `kars_tr/bayt`, `kayit_araya`, `liste_esitlik`; `--sira neredeyse` |
| Testler | 177 birim; kâhin 297 205 | 203 birim (+26 sıralama); kâhin 345 505 denetim; `--hata-goster kesme`, `--hata-goster kararsiz` |

Kayıt dizisi, yükleyici ve menü v2.3'teki gibidir; menüdeki tek fark önek araması sonuçlarının Türkçe sırayla listelenmesidir. v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır.

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `turkce` (**yeni**) | UTF-8 çözme, Türkçe birincil sıra, karşılaştırma, önek | yalnız standart kütüphane: öğrenci kaydını bilmez |
| `siralama` (**yeni**) | üç temel algoritma, qsort arayüzünde | yalnız `sayac`: öğe türünü bilmez |
| `liste` (**yeni**) | kayıt karşılaştırıcıları, ölçüt tablosu, liste kurma ve sıralama | `obs`, `turkce`, `siralama` |
| `listele.c` (**yeni**) | komut satırı aracı | `liste`, `dosya` |
| `arama` | + Türkçe soyad dizini | + `turkce` |
| diğerleri | v2.3'ten aynen | — |

Katmanlar: `turkce` ve `siralama` genel amaçlıdır (başka bir projede aynen kullanılabilir); kayda özgü bilgi yalnızca `liste`'dedir. Liste, `const Ogrenci *` işaretçilerinden oluşur: kayıtlar (144 bayt) `Sinif` dizisinde, numara sırasında kalır.

## 4. Algoritmalar ve karşılaştırıcılar

### 4.1 Türkçe karşılaştırıcı

![Türkçe karşılaştırıcı](mini_obs_v2_4_karsilastirici.png)

*Şekil 1. "ÇELİK" ile "DEMİR": `strcmp` ilk baytları (C3 ve 44) karşılaştırır ve ÇELİK'i sona koyar; `tr_karsilastir` her harfi kod noktasına çözer ve Türkçe sıra değeriyle (Ç = 13, D = 14) karşılaştırır. Değerler `turkce.c`'nin kendisiyle hesaplandı.*

```
algoritma TR-KARŞILAŞTIR(a, b)
    a ve b bitmediği sürece
        ka ← UTF8-ÇÖZ(a);  kb ← UTF8-ÇÖZ(b)          ▷ 1–4 bayt → kod noktası
        sa ← SIRA(ka);     sb ← SIRA(kb)             ▷ boşluk < ' < - < A < … < Z
        eğer sa ≠ sb ise işaret(sa − sb) döndür
    eğer biri bittiyse kısa olan önce                ▷ AYŞE < AYŞE NUR
    işaret(strcmp(a, b)) döndür                      ▷ ikincil: tam sıralama
```

Sıra tablosu: boşluk, kesme işareti, kısa çizgi, sonra **A B C Ç D E F G Ğ H I İ J K L M N O Ö P Q R S Ş T U Ü V W X Y Z** (29 Türkçe harf; Q, W, X Latin alfabesindeki yerlerinde), sonra öbür karakterler (kod noktası sırasıyla). Küçük harfler büyükleriyle aynı sıradadır ve Türkçe kurala uyar: i → İ, ı → I. Şapkalı Â, Î, Û şapkasız karşılıklarıyla aynı birincil sıradadır. Birincil sıralar eşitse (ör. HALE / HÂLE) bayt sırası karar verir; böylece `tr_karsilastir(a, b) = 0 ⇔ strcmp(a, b) = 0` ve karşılaştırıcı **tam bir sıralamadır** (sort kararlılığı yalnızca gerçekten aynı dizgiler için anlam taşır).

`strcmp`'nin yanlış sıraladığı çiftler (birim testlerinde): ÇELİK/DEMİR, İREM/JALE, ÖZTÜRK/PEKER, ŞEN/ÜNAL, AĞA/AHA. Kendi aralarında da bayt sırası Ç Ö Ü Ğ İ Ş, alfabe sırası Ç Ğ İ Ö Ş Ü'dür. IŞIK/İNCE çiftinde ise `strcmp` tesadüfen doğrudur (I = 49 < İ = C4 B0). C'nin `strcoll` + `setlocale(LC_COLLATE, "tr_TR.UTF-8")` çözümü yerel ayarın kurulu olmasına bağlıdır ve platformlar arasında farklı sonuç verebilir; bu modül her yerde aynıdır.

### 4.2 Üç temel algoritma (qsort arayüzü)

```
algoritma SEÇMELİ(a[0..n−1])                       ▷ değişmez: a[0..i−1] sıralı, en küçük i öğe
    i ← 0'dan n−2'ye: en ← i; j ← i+1'den n−1'e: eğer a[j] < a[en] ise en ← j
                      eğer en ≠ i ise a[i] ↔ a[en]     ▷ uzak takas: KARARSIZ
algoritma KABARCIK(a[0..n−1])                      ▷ değişmez: a[son..n−1] yerinde
    son ← n'den 2'ye: takas ← yanlış
        j ← 1'den son−1'e: eğer a[j−1] > a[j] ise a[j−1] ↔ a[j]; takas ← doğru
        eğer takas yoksa dur                        ▷ erken çıkış; yalnız > ile takas: KARARLI
algoritma ARAYA-EKLEME(a[0..n−1])                  ▷ değişmez: a[0..i−1] sıralı
    i ← 1'den n−1'e: anahtar ← a[i]; j ← i
        j > 0 ve a[j−1] > anahtar olduğu sürece a[j] ← a[j−1]; j ← j − 1
        a[j] ← anahtar                              ▷ eşitte durur: KARARLI
```

Üç algoritmanın çözümlemesi Knuth (1998) ve Cormen vd. (2022) ile aynıdır. Gerçekleştirim öğenin türünü bilmez: i. öğenin adresi `taban + i × boyut`, taşıma `memcpy`. Sayaçlar: karşılaştırma = karşılaştırıcı çağrısı; taşıma = öğe kopyası (takas 3). Kapalı biçimler (T: ters çevrim sayısı; programla ve kâhinle doğrulandı):

| Algoritma | Karşılaştırma | Taşıma | Kararlı | Uyarlanabilir |
|---|---|---|---|---|
| seçmeli | tam n(n − 1)/2 | 3 × takas, takas ≤ n − 1 | hayır | hayır |
| kabarcık (erken çıkış) | n − 1 (sıralı) … n(n − 1)/2 | 3T (takas = T) | evet | zayıf |
| araya ekleme | T + (n − 1) − m | 2(n − 1) + T | evet | evet (Θ(n + T)) |

(m: kendisinden önceki bütün öğelerden **kesin** küçük olan öğe sayısı, i ≥ 1.) Elle izleme (birim testi; Cormen vd., 2022'nin 5, 2, 4, 6, 1, 3 örneği, T = 9): seçmeli 15 karşılaştırma; kabarcık 9 takas = 27 taşıma; araya ekleme 12 karşılaştırma ve 2 · 5 + 9 = 19 taşıma.

### 4.3 Kayıt karşılaştırıcıları ve kararlılık

Bir karşılaştırıcı **sözlük sırası** kurar: ilk anahtar eşitse sonrakine geçer. Başarı ölçütü:

```c
static int kars_basari(const void *a, const void *b)
{
    int c = kars_yano_azalan(a, b);    /* YANO ↓ (tamsayı: YANO × 100) */
    return c != 0 ? c : kars_soyad(a, b);   /* soyad ↑, ad ↑ (Türkçe) */
}
```

`kars_yano_azalan`, YANO'yu `ogrenci_yano100` ile **tamsayı** olarak karşılaştırır (2,91 → 291): kayan noktada eşit görünen iki değerin farklı yuvarlanması riski yoktur. Ders ortalaması gibi kayan nokta anahtarlarda `(x < y) − (x > y)` kullanılır; `(int)(x − y)` farkı 1'den küçük ortalamaları eşit sayar (Hata Avcısı; bölüm 8, `--hata-goster kesme`). Tamsayıda `return x − y` taşabilir (işaretli taşma tanımsız davranıştır).

Ölçütlerin **hiçbiri numarayı içermez**. Liste numara sırasıyla kurulduğu için kararlı bir algoritma tam eşit kayıtları (aynı YANO, aynı soyad, aynı ad) numara sırasında bırakır; bu, numarayı son anahtar olarak ekleyen **tam** karşılaştırıcıyla (`liste_tam_karsilastirici`) yapılan herhangi bir sıralamanın sonucuyla aynıdır — kâhin `qsort` + tam ölçüttür.

![Kararlılık](mini_obs_v2_4_kararlilik.png)

*Şekil 2. `testler/kararlilik.csv`: üç ECE KAYA kaydı başarı ölçütüne göre eşittir. Araya ekleme onları girdi (numara) sırasında bırakır; seçmeli sıralamanın uzak takasları sırayı …066, …062, …061 yapar. Listeler `listele` çıktısından alınmıştır.*

**Çok geçişli sıralama.** En az önemli anahtardan başlayarak her anahtar için ayrı bir **kararlı** geçiş (başarı: önce ada, sonra soyada, en son YANO'ya göre) tek karşılaştırıcılı sıralamayla aynı sonucu verir: son geçiş YANO'ya göre sıralar; YANO'su eşit olanlar önceki geçişin (soyad, ad) sırasını korur. Kararsız bir algoritmayla (seçmeli) geçişler önceki sırayı bozar ve sonuç farklı olur (birim testi ve kâhin). Bu, H7'de taban sıralamasının doğruluk koşuludur.

### 4.4 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `tr_karsilastir`, `tr_birincil_karsilastir`, `tr_onek_mi` | **bağımsız** sıra hesabı: harfler UTF-8 dizgi tablosunda `strncmp` ile eşlenir (kod noktası çözümü kullanılmaz); ters simetri; `== 0 ⇔ strcmp == 0` |
| üç algoritma | `qsort`; sayaçlar ters çevrim sayısından (tanımdan, O(n²)) |
| kararlılık | (anahtar, kimlik) çiftlerinde `qsort` + kimlik |
| `liste_sirala` (8 ölçüt; araya, kabarcık, çok geçişli) | `qsort` + numarayla tamamlanmış ölçüt; seçmeli için yalnızca sıralılık |

## 5. Kullanım

### 5.1 `listele`

```
./listele dosya.csv|dosya.dat [--olcut basari|soyad|soyad_bayt|ad|no|alg|mat|fiz]
          [--yontem araya|secmeli|kabarcik|qsort|cok_gecisli|hepsi] [--ilk K] [--denetle]
```

Türkçe soyad sırası ve bayt sırası (aynı veri):

```
$ ./listele ornek_veri/ogrenciler.csv --olcut soyad --ilk 8
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8
Ölçüt: soyad — soyad ↑, ad ↑ (Türkçe alfabe)
Yöntem: araya · karşılaştırma 21 · toplama 0 · çarpma 0 · taşıma 30
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010049  ZEYNEP ÇELİK               76.00 BB   63.00 CC   53.00 DC   2.21
   2  2301010050  EMRE ÇINAR                 96.80 AA   69.60 CB   78.60 BB   3.18
   3  2301010051  ŞULE DOĞAN                 55.60 DC   56.20 DC   57.60 DC   1.50
   4  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
   5  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   6  2301010052  ILGAZ ŞAHİN                36.00 FF   86.80 BA   77.00 BB   2.12
   7  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   8  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
```

```
$ ./listele ornek_veri/ogrenciler.csv --olcut soyad_bayt --ilk 8
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8
Ölçüt: soyad_bayt — soyad ↑, ad ↑ (bayt sırası, strcmp)
Yöntem: araya · karşılaştırma 15 · toplama 0 · çarpma 0 · taşıma 24
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010051  ŞULE DOĞAN                 55.60 DC   56.20 DC   57.60 DC   1.50
   2  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
   3  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   4  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
   5  2301010049  ZEYNEP ÇELİK               76.00 BB   63.00 CC   53.00 DC   2.21
   6  2301010050  EMRE ÇINAR                 96.80 AA   69.60 CB   78.60 BB   3.18
   7  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   8  2301010052  ILGAZ ŞAHİN                36.00 FF   86.80 BA   77.00 BB   2.12
```

Başarı sırası ve denetim (bu sekiz kayıtta YANO eşitliği yoktur; eşit kayıtlar aşağıda `testler/kararlilik.csv` ile sınanır):

```
$ ./listele ornek_veri/ogrenciler.csv --denetle
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8
Ölçüt: basari — YANO ↓, soyad ↑, ad ↑ (başarı sırası)
Yöntem: araya · karşılaştırma 18 · toplama 0 · çarpma 0 · taşıma 26
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010050  EMRE ÇINAR                 96.80 AA   69.60 CB   78.60 BB   3.18
   2  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   3  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
   4  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   5  2301010049  ZEYNEP ÇELİK               76.00 BB   63.00 CC   53.00 DC   2.21
   6  2301010052  ILGAZ ŞAHİN                36.00 FF   86.80 BA   77.00 BB   2.12
   7  2301010051  ŞULE DOĞAN                 55.60 DC   56.20 DC   57.60 DC   1.50
   8  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
Kâhin (qsort + numara): AYNI
Eşit kayıtlar numara sırasında (kararlılık): EVET
Süre (araya): 0.003 ms
```

Beş yöntem aynı listede (`--yontem hepsi`) ve kararsız yöntemin denetimi:

```
$ ./listele testler/kararlilik.csv --yontem hepsi
Dosya: testler/kararlilik.csv · kayıt: 8
Ölçüt: basari — YANO ↓, soyad ↑, ad ↑ (başarı sırası)
Yöntem        karşılaştırma        taşıma   kâhinle aynı   eşitler numara sırasında
araya                    23            31   EVET           EVET
Süre (araya): 0.004 ms
secmeli                  28            12   HAYIR          HAYIR
Süre (secmeli): 0.003 ms
kabarcik                 27            51   EVET           EVET
Süre (kabarcik): 0.002 ms
qsort                     -             -   EVET           EVET
Süre (qsort): 0.002 ms
cok_gecisli              52            77   EVET           EVET
Süre (cok_gecisli): 0.003 ms
```

```
$ ./listele testler/kararlilik.csv --yontem secmeli --denetle
Dosya: testler/kararlilik.csv · kayıt: 8
Ölçüt: basari — YANO ↓, soyad ↑, ad ↑ (başarı sırası)
Yöntem: secmeli · karşılaştırma 28 · toplama 0 · çarpma 0 · taşıma 12
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010063  ALİ ŞEN                    93.00 AA   93.00 AA   93.00 AA   4.00
   2  2301010067  İPEK IŞIK                  83.00 BA   83.00 BA   83.00 BA   3.50
   3  2301010068  ŞULE ÜNAL                  83.00 BA   83.00 BA   83.00 BA   3.50
   4  2301010065  CEM CAN                    66.00 CB   66.00 CB   66.00 CB   2.50
   5  2301010064  ÜMİT ÇAKIR                 66.00 CB   66.00 CB   66.00 CB   2.50
   6  2301010066  ECE KAYA                   66.00 CB   66.00 CB   66.00 CB   2.50
   7  2301010062  ECE KAYA                   66.00 CB   66.00 CB   66.00 CB   2.50
   8  2301010061  ECE KAYA                   66.00 CB   66.00 CB   66.00 CB   2.50
Kâhin (qsort + numara): FARKLI (ilk fark: sıra 6)
Eşit kayıtlar numara sırasında (kararlılık): HAYIR
Süre (secmeli): 0.005 ms
[çıkış kodu: 1]
```

Üretilmiş 2 000 kayıtta üç ölçüt (eşit kayıtlar kendiliğinden oluşur):

```
$ ./veri_uret --n 2000 --tohum 42 --cikti u2000.csv; for o in basari soyad alg; do ./listele u2000.csv --olcut $o --yontem hepsi 2>/dev/null; done
Dosya: u2000.csv · kayıt: 2000
Ölçüt: basari — YANO ↓, soyad ↑, ad ↑ (başarı sırası)
Yöntem        karşılaştırma        taşıma   kâhinle aynı   eşitler numara sırasında
araya               1021539       1023547   EVET           EVET
secmeli             1999000          5985   HAYIR          HAYIR
kabarcik            1998847       3058647   EVET           EVET
qsort                     -             -   EVET           EVET
cok_gecisli         2892802       2898805   EVET           EVET
Dosya: u2000.csv · kayıt: 2000
Ölçüt: soyad — soyad ↑, ad ↑ (Türkçe alfabe)
Yöntem        karşılaştırma        taşıma   kâhinle aynı   eşitler numara sırasında
araya                999993       1001997   EVET           EVET
secmeli             1999000          5973   HAYIR          HAYIR
kabarcik            1996372       2993997   EVET           EVET
qsort                     -             -   EVET           EVET
cok_gecisli         1961154       1965155   EVET           EVET
Dosya: u2000.csv · kayıt: 2000
Ölçüt: alg — ALG ortalaması ↓, soyad ↑, ad ↑
Yöntem        karşılaştırma        taşıma   kâhinle aynı   eşitler numara sırasında
araya               1018913       1020918   EVET           EVET
secmeli             1999000          5976   EVET           EVET
kabarcik            1998220       3050760   EVET           EVET
qsort                     -             -   EVET           EVET
cok_gecisli         2945903       2951908   EVET           EVET
```

### 5.2 `mini_obs` ve `ara`

Menü 3'te `*` (bütün kayıtlar soyad sırasıyla) artık Türkçe sırayı verir:

```
$ printf '3\n*\n10\n' | ./mini_obs ornek_veri/ogrenciler.csv | grep -A10 'SOYAD ÖNEKİ'
--------------------------------- SOYAD ÖNEKİ: *
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   5  2301010049  ZEYNEP ÇELİK               76.00 BB   63.00 CC   53.00 DC   2.21
   6  2301010050  EMRE ÇINAR                 96.80 AA   69.60 CB   78.60 BB   3.18
   7  2301010051  ŞULE DOĞAN                 55.60 DC   56.20 DC   57.60 DC   1.50
   2  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
   3  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   8  2301010052  ILGAZ ŞAHİN                36.00 FF   86.80 BA   77.00 BB   2.12
   1  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   4  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
Eşleşen kayıt: 8 (soyad sırasıyla)
```

## 6. Tasarım kararları

1. **İşaretçi dizisini sırala, kaydı taşıma.** Sıralı listeler kayıt dizisini değiştirmez (değişmez: numara sırası, v2.3); her liste ayrı bir işaretçi dizisidir ve birçok liste aynı anda var olabilir. Bu sürümün ölçümünde kayıtların kendisini sıralamanın süresi işaretçileri sıralamanınkinin 1,27 katıdır (bölüm 7.4): karşılaştırıcı pahalı olduğunda taşıma payı küçülür. v2.3'te (ucuz karşılaştırma) aynı fark 31 kattı.
2. **qsort arayüzü.** Algoritmalar `(taban, n, boyut, kars)` alır: aynı fonksiyon tamsayı dizisini, işaretçi dizisini ya da kayıt dizisini sıralar ve sonuç doğrudan `qsort` ile karşılaştırılabilir. Bedeli, her karşılaştırmanın bir fonksiyon işaretçisi çağrısı ve her taşımanın `memcpy` olmasıdır.
3. **Türkçe karşılaştırıcı kendi modülünde ve tam sıralama.** `strcoll` taşınabilir değildir; tablo tabanlı karşılaştırıcı her platformda aynı sonucu verir. İkincil bayt ölçütü, "eşit" sonucunu yalnızca aynı dizgilere bırakır: aksi hâlde HALE ile HÂLE "eşit" olur ve kâhin karşılaştırması belirsizleşirdi.
4. **YANO tamsayı.** `ogrenci_yano100` eklendi; `ogrenci_yano` ondan türetildi (sonuçlar v1.0 ile aynı). Karşılaştırıcılar kayan nokta eşitliğine dayanmaz.
5. **Numara karşılaştırıcıda yok, kâhinde var.** Kararlılığı görünür kılmak için ölçütler numarasızdır; kâhin numaralı tam ölçütle tek doğru sonucu tanımlar. `--denetle` ve kâhin testleri iki şeyi ayrı ayrı denetler: sonuç doğru mu, eşitler numara sırasında mı?
6. **Kararsız algoritma da korunur.** Seçmeli sıralama yanlış değil, kararsızdır: sonuç ölçüte göre sıralıdır (kâhin bunu da denetler) ama eşitlerin sırası rastgeledir. Kararlılığın gerekli olup olmadığı ölçüte değil kullanım amacına bağlıdır.
7. **Soyad dizini Türkçe sıraya geçti, algoritma değişmedi.** v2.3'ün `lower_bound` + önek denetimi, karşılaştırıcı (`tr_birincil_karsilastir`) ve önek kuralı (`tr_onek_mi`) değiştirilerek aynen kullanıldı; v2.3'ün bayt dizini ve testleri korundu.
8. **Neredeyse sıralı girdi.** Ölçümde "neredeyse sıralı" liste, başarı sırasına n/20 rastgele komşu takası uygulanarak kurulur: ters çevrim sayısı en çok n/20'dir ve araya ekleme bu girdide doğrusal davranır.

## 7. Ölçümler

### 7.1 Ölçüm düzeni ve ortam

Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB, L3 33 MiB; gcc 13.3.0, `-std=c17 -Wall -Wextra -pedantic -O2 -g`; tarih 2026-10-13 07:19. Düzen: 1 ısınma + 5 tekrar, ortanca (Sedgewick & Wayne, 2011); 8 000 kayıtta 3 tekrar. Veri: `veri_uret` üreteci, tohum 42; liste başarı ölçütüyle (YANO ↓, soyad ↑, ad ↑), işaretçi dizisi üzerinde sıralanır; her çalıştırma başlangıç listesini kopyalar (O(n), ölçüme dahil). Girdi türleri: **karışık** (numara sırası; başarıya göre rastgele), **sıralı** (zaten başarı sırasında), **ters**, **neredeyse sıralı** (sıralı + n/20 rastgele komşu takası). Sayaçlar ısınma çalıştırmasında toplanır. `make olcum` 1 dakika 28 s sürdü. Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 1,06, sonda 1,08 idi (2 çekirdek; başka işlerle paylaşıldı): süreler gürültülüdür ve ayrı çalıştırmalar arasında belirgin farklar görülebilir. Sayaçlar deterministiktir.

### 7.2 Algoritma × girdi türü

| algoritma | girdi | karşılaştırma | taşıma | süre |
|:--|:--|--:|--:|--:|
| seçmeli | karışık | 7 998 000 | 11 967 | 358,0 ms |
| seçmeli | sıralı | 7 998 000 | 0 | 255,2 ms |
| seçmeli | ters | 7 998 000 | 6 066 | 1,16 s |
| seçmeli | neredeyse sıralı | 7 998 000 | 522 | 260,2 ms |
| kabarcık | karışık | 7 997 370 | 12 089 385 | 1,24 s |
| kabarcık | sıralı | 3 999 | 0 | 848,6 µs |
| kabarcık | ters | 7 998 000 | 23 993 130 | 348,6 ms |
| kabarcık | neredeyse sıralı | 11 994 | 522 | 3,1 ms |
| araya ekleme | karışık | 4 033 780 | 4 037 793 | 146,2 ms |
| araya ekleme | sıralı | 3 999 | 7 998 | 904,6 µs |
| araya ekleme | ters | 7 997 966 | 8 005 708 | 266,8 ms |
| araya ekleme | neredeyse sıralı | 4 173 | 8 172 | 974,1 µs |

*Tablo 1. n = 4 000 kayıtlık başarı listesi: sayaçlar ve süreler (ortanca).*

![Isı haritası](mini_obs_v2_4_isi_haritasi.png)

*Şekil 3. Algoritma × girdi türü: karşılaştırma sayısı (bin) ve süre (ms), n = 4 000. Renk ölçeği logaritmiktir.*

Yorum:

- **Seçmeli sıralama girdiye kördür:** dört girdide de tam 7 998 000 = n(n − 1)/2 karşılaştırma yapar. Taşıması en azdır (en çok n − 1 takas): karışık girdide 11 967 taşıma, araya eklemenin 4 037 793 taşımasına karşı.
- **Kabarcık ve araya ekleme uyarlanabilirdir:** sıralı girdide ikisi de n − 1 = 3 999 karşılaştırmayla biter; neredeyse sıralı girdide araya ekleme 4 173 karşılaştırma yapar (Θ(n + T)). Ters girdide kabarcık 7 997 710 takas (23 993 130 taşıma), araya ekleme 8 005 708 taşıma yapar; karşılaştırma sayıları n(n − 1)/2'ye çok yakındır (7 997 966 araya eklemede): eşit kayıt çiftleri ters çevrim sayılmaz.
- **Karışık girdide kabarcık en yavaştır** (1,24 s): araya ekleme kadar ters çevrimi düzeltir ama bunu komşu **takaslarıyla** (3 taşıma) ve n(n − 1)/2'ye yakın karşılaştırmayla yapar; ders kitaplarındaki kalıcı yerine karşın pratikte neden tercih edilmediği budur (Astrachan, 2003). Ters girdide (348,6 ms) karışık girdiden hızlıdır: her karşılaştırma takasla sonuçlanır ve dal tahmini kolaylaşır.
- **Aynı karşılaştırma sayısı, farklı süre — seçmeli sıralamada ters girdi:** dört girdide sayı aynı olduğu hâlde ters girdi sıralı girdiden 4,5 kat yavaştır. Sebep karşılaştırıcının kendisidir: başarı ölçütü YANO'lar eşitse Türkçe soyad ve ad karşılaştırmasına geçer. Ters girdide seçmeli sıralamanın "şimdiye kadarki en iyi" adayı her adımda bir sonraki, çoğu zaman **aynı YANO'lu** kayda geçer:

| girdi | karşılaştırma | ilk anahtarı (YANO) eşit | pay | seçmeli sıralama süresi |
|:--|--:|--:|--:|--:|
| karışık | 7 998 000 | 500 252 | %6,3 | 358,0 ms |
| sıralı | 7 998 000 | 486 730 | %6,1 | 255,2 ms |
| ters | 7 998 000 | 4 308 645 | %53,9 | 1,16 s |
| neredeyse sıralı | 7 998 000 | 486 730 | %6,1 | 260,2 ms |

*Tablo 2. Seçmeli sıralamada ilk anahtarı (YANO) eşit olan karşılaştırmaların payı (`olcer liste_esitlik`, n = 4 000).*

  Ters girdide ikinci anahtara (Türkçe dizgi karşılaştırmasına) geçen karşılaştırmaların payı %53,9, karışık girdide yalnızca %6,3 olur. **Karmaşıklık işlem sayısını sayar; çok anahtarlı karşılaştırıcıda bir işlemin maliyeti girdiye bağlıdır.**

### 7.3 Büyüme ve kütüphane sıralaması

| n | seçmeli | kabarcık | araya ekleme | qsort | çok geçişli | araya ekleme (sıralı girdi) |
|--:|--:|--:|--:|--:|--:|--:|
| 500 | 6,4 ms | 10,0 ms | 3,0 ms | 360,0 µs | 7,0 ms | 72,7 µs |
| 1 000 | 20,6 ms | 50,4 ms | 11,7 ms | 871,0 µs | 25,7 ms | 191,8 µs |
| 2 000 | 104,3 ms | 239,1 ms | 39,1 ms | 2,1 ms | 105,7 ms | 371,2 µs |
| 4 000 | 358,0 ms | 1,24 s | 146,2 ms | 6,5 ms | 404,0 ms | 904,6 µs |
| 8 000 | 1,43 s (3) | 5,86 s (3) | 619,6 ms (3) | 13,0 ms | — | — |
| 16 000 | — | — | — | 31,9 ms | — | — |
| 100 000 | — | — | — | 342,8 ms | — | — |

*Tablo 3. Karışık başarı listesinde süreler (ortanca; parantez: tekrar sayısı). Son sütun: araya ekleme, sıralı girdi.*

![Süreler](mini_obs_v2_4_olcum_sure.png)

*Şekil 4. Süre (log–log). Üç karesel algoritmanın eğimi ≈ 2; araya eklemenin sıralı girdideki eğrisi ve `qsort` ≈ 1 eğimlidir.*

- **Oran testi** (karışık, n = 8 000 / 4 000): seçmeli 4,00, kabarcık 4,72, araya ekleme 4,24 (kuram 4; karşılaştırma sayıları 4,00, 4,00, 4,00 kat). Süre oranları paylaşılan makinede gürültüye açıktır (8 000'de 3 tekrar); sayaç oranları kesindir ve kuramla birebir uyuşur.
- **qsort** n = 4 000 için 6,5 ms sürer — araya eklemeden 23 kat hızlı — ve 10⁵ kayıtta bile 342,8 ms'dir. Aradaki fark büyüme sınıfıdır (n log n ↔ n²); H6'da birleştirmeli ve hızlı sıralamayla kendimiz yazacağız.
- **Çok geçişli sıralama** (3 × araya ekleme) n = 4 000 için 11 660 359 karşılaştırma (2,89 kat) yapar ve 404,0 ms sürer: doğrudur ama tek karşılaştırıcılı sıralamadan pahalıdır. Değeri kararlılığın gücünü göstermesidir; H7'deki taban sıralaması bu fikrin karşılaştırmasız sürümüdür.
- **Kararlılık sağlaması:** her n'de `kontrol` (sıranın sağlaması) kabarcık, araya ekleme, `qsort` ve çok geçişli sıralamada aynıdır; seçmeli sıralamada farklıdır (n = 4 000: 7974366344 ↔ 7974458084): üretilmiş veride eşit kayıtlar vardır ve seçmeli sıralama onların sırasını değiştirir.

### 7.4 Doğru karşılaştırıcının ve taşımanın bedeli

| n | qsort, Türkçe | qsort, bayt | oran | karşılaştırma (Türkçe) | ns/karş. (Türkçe) | ns/karş. (bayt) |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 1,2 ms | 172,9 µs | 7,2 | 8 711 | 142 | 20 |
| 10 000 | 22,9 ms | 2,8 ms | 8,2 | 120 352 | 190 | 23 |
| 100 000 | 470,2 ms | 52,8 ms | 8,9 | 1 536 159 | 306 | 34 |

*Tablo 4. `qsort` ile soyad listesi (soyad ↑, ad ↑, numara ↑): Türkçe karşılaştırıcı ↔ bayt (`strcmp`) karşılaştırıcısı. Karşılaştırma sayısı sarıcı fonksiyonla ısınmada sayıldı.*

Türkçe karşılaştırıcı 10⁵ kayıtta 8,9 kat yavaştır: her harf için UTF-8 çözümü ve 32 elemanlı tabloda doğrusal arama yapar. Bu doğruluğun bedelidir ve ölçülebilir; kodu hızlandırmanın iki yolu ileri alıştırmadır: sıra değerlerini doğrudan bir diziyle bulmak ya da her kaydın **sıralama anahtarını** (sıra değerleri dizisi) bir kez hesaplayıp karşılaştırmada onu kullanmak (C'nin `strxfrm`'ü ve Python'un `key=` parametresi bu fikirdir).

| n | karşılaştırma (ikisinde aynı) | taşıma (ikisinde aynı) | kayıt (144 B) | işaretçi (8 B) | kayıt / işaretçi |
|--:|--:|--:|--:|--:|--:|
| 500 | 67 862 | 68 364 | 3,2 ms | 2,8 ms | 1,11 |
| 1 000 | 262 446 | 263 452 | 11,2 ms | 10,5 ms | 1,06 |
| 2 000 | 1 021 539 | 1 023 547 | 41,4 ms | 39,1 ms | 1,06 |
| 4 000 | 4 033 780 | 4 037 793 | 222,5 ms | 175,8 ms | 1,27 |

*Tablo 5. Araya ekleme: kayıtların kendisi (144 B) ↔ işaretçiler (8 B); karşılaştırma ve taşıma sayıları aynıdır.*

v2.3'te öğe boyutunun etkisi 31 kattı; burada kayıtları sıralamanın işaretçileri sıralamaya oranı 1,27 oldu — fark ölçüm gürültüsünün içindedir. Sebep karşılaştırıcıdadır: v2.3'te karşılaştırma iki `long long`'un kıyaslanmasıydı, burada her karşılaştırma iki YANO hesabı ve gerekirse Türkçe dizgi karşılaştırmasıdır (araya eklemede ≈ 36 ns). İşaretçi sıralamanın asıl kazancı burada bellek ve esnekliktir: kayıtlar yerinde kalır ve aynı anda birçok liste tutulabilir.

### 7.5 Sonuç ve H6'ya köprü

Üç temel algoritma da doğru, ama Θ(n²): n = 4 000 için bile en iyisi (araya ekleme) `qsort`'tan 23 kat yavaştır; 10⁵ kayıtta araya ekleme dakikalar sürerdi. Araya ekleme yine de kazanır: sıralı ve neredeyse sıralı girdide doğrusaldır ve kararlıdır — gerçek kütüphaneler (introsort, Timsort) küçük parçaları bu yüzden araya eklemeyle sıralar. v2.5'te birleştirmeli sıralama (kararlı, Θ(n log n)) `listele`'nin varsayılanı olacak; v2.4'ün araya ekleme ve tam ölçütlü `qsort` sonuçları onun kâhinidir.

## 8. Testler

- **Birim testleri** (`obs_test`): `203 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama`. Sıralama testleri: sıra değerleri (noktalama, Ç/Ğ/İ/Ö/Ş/Ü komşulukları, küçük harf ve şapkalı harf eşlemeleri); UTF-8 çözme (1, 2, 3 bayt, bozuk dizi); `strcmp`'nin yanlış, `tr_karsilastir`'ın doğru sıraladığı beş çift; birincil/ikincil eşitlik (ALİ/ali, HALE/HÂLE), önek kuralları (AYŞE < AYŞE NUR < AYŞEGÜL); üç algoritmada CLRS örneğinin elle izlenmiş sayaçları, sıralı ve ters girdide kapalı biçimler, n = 0, 1 ve hepsi eşit; 300 baytlık öğe; (2, 0) (2, 1) (1, 2) dizisinde kararlılık; örnek sınıfta soyad ve başarı sırası; `kararlilik.csv`'de çok geçişli = tek karşılaştırıcı = kâhin, seçmeli kararsız ve çok geçişli seçmeli farklı; Türkçe soyad dizini ve önekleri.
- **Kâhin testleri** (`test_kahin`): 300 denemede 345 505, 1 000 denemede 1 140 964 denetim (Türkçe karşılaştırıcı: 120 000; temel sıralama: 9 000; listeler: 32 000), uyuşmazlık yok.
- **Kasıtlı hatalar:** (a) `--hata-goster kesme`: ders ortalaması karşılaştırıcısında `(int)(x − y)`; farkı 1'den küçük ortalamalar eşit sayılır ve liste soyada göre sıralanmış olur:

```
$ ./test_kahin --hata-goster kesme
KÂHİN UYUŞMAZLIĞI (tohum 3)
  İşlev      : liste_sirala
  n          : 116
  Beklenen   : qsort + numara (ölçüt alg)
  Bulunan    : araya: ilk fark sıra 3 (ölçüte göre sırasız)
  Beklenen: 2400000108 YUSUF KOÇ (ALG 94.60, YANO 3.82)
  Bulunan : 2400000049 ÖMER CAN (ALG 94.40, YANO 3.65)
  Yeniden üretmek için: ./test_kahin --tohum 3 --deneme 1 --hata-goster kesme
```

  (b) `--hata-goster kararsiz`: başarı listesinde araya ekleme yerine seçmeli sıralama; kâhin eşit iki kaydın yer değiştirdiğini gösterir:

```
$ ./test_kahin --hata-goster kararsiz
KÂHİN UYUŞMAZLIĞI (tohum 6)
  İşlev      : liste_sirala
  n          : 115
  Beklenen   : qsort + numara (ölçüt basari)
  Bulunan    : secmeli: ilk fark sıra 112
  Beklenen: 2400000063 İREM ŞEN (ALG 19.60, YANO 0.00)
  Bulunan : 2400000102 İREM ŞEN (ALG 22.20, YANO 0.00)
  Yeniden üretmek için: ./test_kahin --tohum 6 --deneme 1 --hata-goster kararsiz
```
- **Bellek:** `make asan` temiz (`listele`'nin bütün ölçütleri ve yöntemleri, `olcer`'in sıralama işlemleri dahil).

## 9. Ders notu için özet (Hafta 5 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'ye çok ölçütlü sıralı listeler ekliyoruz: başarı sırası (YANO ↓, eşitlikte soyad ↑, ad ↑), Türkçe alfabe sırasıyla soyad listesi ve ders ortalaması listeleri. Seçmeli, kabarcık ve araya ekleme sıralamasını qsort arayüzünde yazıyor, karşılaştırıcıları ve kararlılığı kâhinle sınıyor, üç algoritmayı dört girdi türünde sayıp ölçüyoruz.

### Gereksinimler

- `turkce.h/.c`: `utf8_coz`, `tr_sira_degeri`, `tr_karsilastir` (birincil sıra + bayt ikincil ölçüt: tam sıralama), `tr_onek_mi`. Sıra: boşluk < ' < - < A B C Ç D E F G Ğ H I İ J K L M N O Ö P (Q) R S Ş T U Ü V (W X) Y Z; i → İ, ı → I.
- `siralama.h/.c`: `secmeli_sirala_say`, `kabarcik_sirala_say` (erken çıkışlı), `araya_ekleme_sirala_say`; arayüz `(void *taban, size_t n, size_t boyut, int (*kars)(const void *, const void *), Sayac *sy)`; karşılaştırma ve taşıma sayaçları; her fonksiyonda değişmez yorumu.
- `liste.h/.c`: en az `basari`, `soyad`, `no` ve bir ders ölçütü; her ölçütün numarasız ve numarayla tamamlanmış karşılaştırıcısı; liste `const Ogrenci *` dizisidir.
- Karşılaştırıcılar taşmaya güvenlidir: `(x > y) − (x < y)`; YANO tamsayı (× 100) karşılaştırılır.
- `listele`: `--olcut`, `--yontem` (araya, secmeli, kabarcik, qsort, cok_gecisli, hepsi), `--ilk`, `--denetle`; çıkış kodları 0/1/2.
- Menü 3 ve `ara`'nın soyad önek araması Türkçe sırayla.
- Testler: elle izlenmiş sayaçlar; kâhin olarak `qsort` + tam ölçüt; kararlılık testi (eşit kayıtlar numara sırasında); çok geçişli = tek karşılaştırıcı.
- Ölçüm raporu: üç algoritma × dört girdi türü (karışık, sıralı, ters, neredeyse sıralı) × n = 500 … ≥ 4 000 için karşılaştırma, taşıma ve süre tablosu, ısı haritası ve log–log grafik; `qsort` ile karşılaştırma; Türkçe ↔ bayt karşılaştırıcısının maliyeti.

### İpuçları

- Karşılaştırıcıyı önce kâğıtta yazın: "a, b'den önce gelmeliyse negatif". Azalan sıra için işaretleri değiştirin: `(x < y) − (x > y)`.
- qsort karşılaştırıcısına gelen `void *` bir **öğeyi** gösterir: işaretçi dizisinde öğe `const Ogrenci *`'dır, yani `*(const Ogrenci *const *)p`.
- Araya eklemede döngü koşulunun sırası önemlidir: `j > 0 && kars(a[j−1], anahtar) > 0` — önce sınır.
- Kararlılık için araya eklemede `> 0` ile kaydırın (eşitte durun); kabarcıkta yalnızca `> 0` ile takas edin.
- Türkçe harfleri bayt bayt değil karakter karakter (UTF-8 çözerek) karşılaştırın; `strcmp` yalnızca son eşitlik ölçütü olarak kalsın.
- Kâhin karşılaştırıcısına numarayı son anahtar olarak ekleyin: `qsort` kararlı değildir, ama tam bir sıralamada sonucu tektir.
- Ölçümde her çalıştırma başlangıç listesini kopyalasın; aksi hâlde ikinci çalıştırma zaten sıralı listeyi sıralar.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri ve `test_kahin` (300 deneme) geçer.
2. `./listele ornek_veri/ogrenciler.csv --olcut soyad --ilk 8` sırası: ÇELİK, ÇINAR, DOĞAN, KAYA, ÖZTÜRK, ŞAHİN, YILMAZ (AYŞE NUR), YILMAZ (CAN); `--olcut soyad_bayt` aynı veride DOĞAN ile başlar ve ÇELİK'i YILMAZ'lardan sonraya koyar.
3. `./listele ornek_veri/ogrenciler.csv --denetle`: sıra 2301010050 (EMRE ÇINAR, 3,18), 2301010045 (AYŞE NUR YILMAZ, 2,91), 2301010048 (CAN YILMAZ, 2,79), …, son satır 2301010046 (MEHMET ALİ KAYA, 1,26); "Kâhin (qsort + numara): AYNI", "kararlılık: EVET", çıkış 0.
4. `./listele testler/kararlilik.csv --yontem hepsi`: araya, kabarcik, qsort ve cok_gecisli için "kâhinle aynı EVET / EVET"; secmeli için "HAYIR / HAYIR". `--yontem secmeli --denetle` çıkış kodu 1.
5. Sayaçlar (`olcer`, n = 1 000): `liste_araya --sira artan` → karşılaştırma 999, taşıma 1 998; `liste_secmeli` her `--sira` için karşılaştırma 499 500; `liste_kabarcik --sira artan` → karşılaştırma 999, taşıma 0.
6. `tr_karsilastir` en az şu çiftleri doğru sıralar: ÇELİK < DEMİR, İREM < JALE, ÖZTÜRK < PEKER, ŞEN < ÜNAL, IŞIK < İNCE, AYŞE NUR < AYŞEGÜL.
7. Menü 3'te `*` girdisi soyadları Türkçe sırayla listeler (ÇELİK ilk, YILMAZ son).
8. Kendi makinenizde n = 4 000 karışık başarı listesinde araya ekleme seçmeliden ve kabarcıktan hızlıdır; sıralı girdide araya ekleme karışık girdiden en az 50 kat hızlıdır (bu makinede 162 kat).
9. `--hata-goster kesme` ve `--hata-goster kararsiz` uyuşmazlığı basar ve 1 ile çıkar; `make asan` temizdir.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | `listele ornek_veri/ogrenciler.csv --olcut soyad` | Ç… Ç… D… K… Ö… Ş… Y… Y… (Türkçe) |
| 2 | aynı, `--olcut soyad_bayt` | D… K… Y… Y… Ç… Ç… Ö… Ş… (bayt) |
| 3 | aynı, `--olcut basari --denetle` | 3,18 (ÇINAR) · 2,91 (AYŞE NUR YILMAZ) · 2,79 (CAN YILMAZ) · … · 1,26 (KAYA); AYNI, EVET |
| 4 | `testler/kararlilik.csv --yontem araya` | ECE KAYA …061, …062, …066 (numara sırası) |
| 5 | `testler/kararlilik.csv --yontem secmeli --denetle` | ECE KAYA …066, …062, …061; FARKLI, HAYIR; çıkış 1 |
| 6 | aynı, `--yontem cok_gecisli --denetle` | AYNI, EVET (kararlı geçişler) |
| 7 | `listele ... --olcut alg --ilk 4` | ALG ortalaması azalan: 96,80, 90,40, 88,35, 79,00 |
| 8 | `listele ... --olcut yas` | kullanım iletisi, çıkış 2 |
| 9 | `olcer liste_araya --sira artan --n 1000` | karşılaştırma 999, taşıma 1 998 |
| 10 | `olcer liste_secmeli --sira artan --n 1000` | karşılaştırma 499 500 |
| 11 | `test_kahin --hata-goster kesme` | KÂHİN UYUŞMAZLIĞI (ölçüt alg); çıkış 1 |
| 12 | `test_kahin --hata-goster kararsiz` | KÂHİN UYUŞMAZLIĞI (ölçüt basari, secmeli); çıkış 1 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.3'ünüz (ya da referans v2.3), `turkce.h`, `siralama.h` ve `liste.h` (bildirimler, sözleşmeler, kapalı biçim sayaçlar), `testler/kararlilik.csv`, `olcer`'in liste ölçüm düzeneği (girdi türleri, sağlama).
- **Yazılır:** `turkce.c`, `siralama.c`, `liste.c`, `listele.c`; `obs.c`'ye `ogrenci_yano100` ve `sira_listesi_yaz`; `arama.c`'ye Türkçe dizin; testler; `Makefile`'a `listele` ve yeni `olcum`.
- **Değiştirilmez:** kayıt dizisinin numara sırası (v2.3 değişmezi), v1.0 kuralları, ortak modüller.
- **Meydan okuma:** (a) Türkçe karşılaştırıcıyı sıra değeri dizisiyle (her kayıt için bir kez hesaplanan sıralama anahtarı) hızlandırın ve Tablo 4'ü yeniden ölçün; (b) ikili aramalı araya ekleme yazın (karşılaştırma O(n log n), taşıma yine T) ve sayaçlarını karşılaştırın; (c) Shell sıralamasını (h-sıralama) aynı arayüzle yazıp aralık dizisinin etkisini ölçün.

## 10. Bilinen sınırlılıklar

- Üç algoritma Θ(n²)'dir: `listele` 10⁴ kayıtta saniyeler, 10⁵ kayıtta dakikalar sürer (bu makinede n = 4 000, araya ekleme: 146,2 ms). Büyük veride `--yontem qsort` kullanılmalıdır; birleştirmeli sıralama v2.5'te.
- Türkçe karşılaştırıcı yalnızca Türk alfabesini (ve Q, W, X'i) sıralar; öbür harfler kod noktası sırasıyla sona gider. Büyük/küçük harf ve şapka farkı yalnızca ikincil ölçütte (bayt sırası) ayrışır.
- Türkçe karşılaştırıcı `strcmp`'den 9 kat kadar yavaştır (10⁵ kayıtlık `qsort`).
- C'nin `qsort`'u kararlılık güvencesi vermez; bu makinedeki glibc testlerimizde eşitleri korudu, ama kâhin buna güvenmez.
- Süreler tek ve paylaşılan bir sanal makinede ölçüldü; 8 000 kayıtlık noktalar 3 tekrarlıdır. Sayaçlar makineden bağımsızdır.
- **Sonradan bulunan hata (v2.6'da düzeltildi):** ders ortalaması ölçütleri (`alg`, `mat`, `fiz`) ortalamaları kayan nokta olarak karşılaştırır. 0,4·vize + 0,6·final, matematiksel olarak eşit iki ortalamayı son bitte farklı hesaplayabilir (ör. 0,4·3 + 0,6·0 = 1,2000000000000002, 0,4·0 + 0,6·2 = 1,2); bu kayıtlar soyada göre değil bu farka göre sıralanır. Kâhin aynı karşılaştırıcıyı kullandığı için hatayı göremedi; v2.6'nın sayma sıralaması (tamsayı anahtar) onu ortaya çıkardı. Başarı ölçütü (tamsayı YANO) etkilenmez.

## 11. Kaynaklar

- Astrachan, O. (2003). Bubble sort: An archaeological algorithmic analysis. *ACM SIGCSE Bulletin, 35*(1), 1–5. https://doi.org/10.1145/792548.611918
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Knuth, D. E. (1998). *The art of computer programming: Vol. 3. Sorting and searching* (2nd ed.). Addison-Wesley.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
