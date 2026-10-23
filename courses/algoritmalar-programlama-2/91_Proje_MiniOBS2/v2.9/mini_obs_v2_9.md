# Mini-OBS 2 v2.9 — Karma: numara dizini, O(n) yinelenen tespiti ve alt dizgi araması (Hafta 10)

**Bu sürümün amacı:** Hafta 10'un karma tablosunu ve desen eşlemeyi Mini-OBS'nin üç sorusuna uygulamak. (1) **Öğrenci numarası → kayıt karma tablosu** — açık adresleme, doğrusal yoklama, Fibonacci (çarpımsal) karması, yük eşiği 0,7 ve × 2 yeniden boyutlandırma, mezar taşıyla silme; v2.3'ün ikili aramasıyla 10⁵–10⁶ kayıtta karşılaştırılır. (2) **Yinelenen numara tespiti O(n)'e** — karma kümesiyle tek geçiş; v2.1'in tüm çiftleri (Θ(n²)) ve v2.5'in sıralaması (Θ(n log n)) ile **aynı çiftleri aynı sırada** verir (kâhin) ve üçü n = 10³…10⁶'da ölçülür. (3) **Ad–soyad içinde alt dizgi** — v2.4'ün Türkçe sırasıyla katlanmış metinde naif yöntem, **Rabin–Karp** (sahte eşleşme sayacıyla) ve kâhin `strstr`; büyük/küçük harf duyarsız ve Türkçe kurallı ("yıl" YILMAZ'da geçer, "ilgaz" ILGAZ'da geçmez). Ölçüm (§ 8): 10⁶ kayıtta numarayla arama ikili aramada 762 ns, karma tablosunda 186 ns (kayda erişim dahil; 4,1 kat), olmayan numarada 829 ns ↔ 71 ns; 10⁵ kayıtta yinelenen tespiti tüm çiftlerle 1,89 s, sıralamayla 22,9 ms, karma kümesiyle 8,1 ms; 10⁶'da tüm çiftler ölçülmedi (işaretli kestirim ≈ 188,96 s), sıralama 297,2 ms, karma 160,2 ms. Fibonacci çarpanını bilen biri 16 000 geçerli numarayla tabloyu 215 717 554 yoklamaya zorlar; aynı numaralar tohumlu çarpanla 102 596 yoklamadır. Rabin–Karp 10⁵ kayıtlık metinde (1 357 400 bayt) ≈ 16,4 ms sürer — doğal metinde naif yöntemden (3,3 ms) yavaş, naifin en kötü durumunda hızlı (§ 8.6).

Dosyalar (satır sayılarıyla): **`karma.h`** (156) · **`karma.c`** (291) · **`desen.h`** (118) · **`desen.c`** (264) · **`olcer_karma.c`** (702) · `yinelenen.h` (71) · `yinelenen.c` (283) · `turkce.h` (74) · `turkce.c` (194) · `sayac.h` (61) · `sayac.c` (29) · `ara.c` (437) · `denetle.c` (207) · `test_obs.c` (2711) · `test_kahin.c` (4317) · `Makefile` (610) · önceki sürümlerin bütün dosyaları · `olcum/arama.csv`, `olcum/yinelenen.csv`, `olcum/yuk.csv`, `olcum/saldiri.csv`, `olcum/desen.csv`, `olcum/desen_q.csv`, `olcum/desen_kotu.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_9_ciktilar.txt` (1664 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_9_karma.png`, `mini_obs_v2_9_rk.png`; grafik: `mini_obs_v2_9_olcum.png`.

Derleme: `make` (önceki programlar + **`olcer_karma`**; `ara` ve `denetle` genişletildi), `make test`, `make olcum` (bu makinede 2 dakika 14 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 43 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0; 1 (dosya okunamadı, bellek yetersiz, yinelenen numara var — `denetle`; testlerde uyuşmazlık); 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 10 **sözlük (map) ADT'sini** karma tablosuyla gerçekleştirir: anahtar evreni geniştir (10 basamaklı numaralar), doğrudan adresleme olanaksızdır; karma fonksiyonu anahtarı küçük bir indis aralığına indirger, çakışmalar (güvercin yuvası ilkesi) bir yöntemle çözülür. Mini-OBS'de bunun üç karşılığı vardır:

- **Numara dizini** (Konu: "Açık adresleme: doğrusal yoklama, birincil kümelenme; silmede mezar taşı", "Yük faktörü α ve yeniden boyutlandırma"): kayıt dizisi v2.3'ten beri numara sırasındadır ve ikili aramayla Θ(log n)'de bulunur; karma tablosu aynı soruyu sıra gerektirmeden **ortalama O(1)**'de yanıtlar (§ 4.1, § 8.1).
- **Yinelenen tespiti** (Konu: "Uygulamalar: … yinelenen tespiti"): sarmalın üçüncü basamağı — v2.1 Θ(n²) → v2.5 Θ(n log n) → v2.9 ortalama Θ(n); üç gerçekleştirim aynı sonucu verir ve aynı veride ölçülür (§ 4.2, § 8.3).
- **Desen eşleme** (Konu: "naif yöntem (en kötü durumda O(nm)); Rabin–Karp kayan karma"): ad–soyad içinde arama; v2.4'ün Türkçe sıra değerleriyle katlanmış metinde bayt düzeyinde çalışılır (§ 4.3, § 8.6).
- **Güvenlik** (Konu: "karma taşkını saldırısı, rastgele tohumlu ve anahtarlı karma"): numaralar dışarıdan (ör. bir CSV ile) geldiğinde sabit karma fonksiyonu saldırıya açıktır; tohumlu çarpan bunu kapatır (§ 4.4, § 8.5).
- **Kaputun Altında**: kapasite 2'nin kuvvetidir, indis mod yerine **kaydırmayla** bulunur (çarpımın üst bitleri); açık adreslemenin yoklaması bitişik hücrelerde ilerler; işaretsiz taşma (mod 2⁶⁴) karma çarpımında ve kayan karmada bilinçli olarak kullanılır.

Yol haritasındaki karşılığı (Tablo A.1): **H10 · v2.9 · Öğrenci no → kayıt karma tablosu; yinelenen numara tespiti O(n); ad–soyad alt dizgi araması · Karma tablosu, Rabin–Karp.**

## 2. v2.8'den ne değişti?

| Konu | v2.8 (H9) | v2.9 (H10) |
|---|---|---|
| Karma tablosu | — | **`karma.h/.c`**: açık adresleme + doğrusal yoklama; Fibonacci çarpanı ya da tohumlu çarpan; hücre BOŞ/DOLU/MEZAR; eşik %70, × 2 (ya da yalnız mezar temizleyen) yeniden kurma; `karma_bul`, `karma_yer` (bul-ya da-ekle), `karma_ekle`, `karma_sil`, `karma_gecerli_mi`, `karma_dizin_kur` |
| Yinelenen numara | v2.1 tüm çiftler, v2.5 sıralayarak | + `yinelenen_bul_karma`, `yinelenen_var_mi_karma` (karma kümesi; aynı çiftler, aynı sıra) |
| Alt dizgi | — | **`desen.h/.c`**: katlanmış ad–soyad metni (`AdMetni`), naif, Rabin–Karp (d = 256, q asal; sahte eşleşme sayacı), `strstr` (kâhin); `desen_kayitlari` |
| Türkçe | birincil sıra (`tr_sira_degeri`) | + katlama: `tr_katla_kod`, `tr_katla`, `utf8_kodla` (sıra değeri eşitliği ⇔ katlanmış bayt eşitliği) |
| Sayaç | karşılaştırma, taşıma, bağlantı | + `yoklama` (incelenen hücre) |
| `ara` | `--no` (ikili), `--soyad` (önek) | + `--karma [--tohum T]`, `--icinde DESEN [--yontem naif\|rk\|strstr\|hepsi] [--q Q]` |
| `denetle` | `--yontem siralama\|ciftler` | + `--yontem karma` |
| Ölçüm | `olcer_yapi` (dinamik yapılar) | + **`olcer_karma`**: arama, dizin kurma, üçlü yinelenen, yük faktörü, saldırı, alt dizgi |
| Testler | 353 birim; kâhin 502 819 denetim | 389 birim (+36 karma-desen); kâhin 670 897 denetim; `--hata-goster mezar`, `--hata-goster rk` |

Menü (`mini_obs`) ve önceki programların çıktıları değişmedi (v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır). `ara` ve `denetle`'nin eski seçenekleri aynen çalışır; `denetle`'nin varsayılan yöntemi v2.5'in sıralamasıdır.

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `karma` (**yeni**) | numara → indis karma tablosu; dizin kurma | `obs` (yalnız `karma_dizin_kur`), `sayac` |
| `desen` (**yeni**) | katlanmış ad–soyad metni; naif, Rabin–Karp, strstr | `turkce` (katlama), `obs` |
| `turkce` | + katlama ve UTF-8 kodlama | — |
| `yinelenen` | + karma kümesiyle tespit | + `karma` |
| `ara.c` | + karma tablosunda arama, ad–soyad içinde arama | + `karma`, `desen` |
| `denetle.c` | + `--yontem karma` | + `karma` |
| `olcer_karma.c` (**yeni**) | v2.9 ölçümleri | `karma`, `desen`, `yinelenen`, `arama`, `uretec`, `deney` |
| diğerleri | v2.8'den aynen | — |

`karma.o` ve `desen.o` `KARMA` grubundadır; `yinelenen.o`'yu kullanan her program (`olcer`, `denetle`, testler) `KARMA` ile de bağlanır. Karma tablosu kayıtlara **sahip olmaz**: değer, kayıt dizisindeki indistir (§ 5).

## 4. Algoritmalar ve veri yapıları

### 4.1 Karma tablosu: açık adresleme, doğrusal yoklama, mezar taşı

![Karma tablosu](mini_obs_v2_9_karma.png)

*Şekil 1. Gerçek numaralar, Fibonacci çarpanı, 8 hücre (birim testindeki örnek). (a) Üç numaranın evi 2'dir: 2, 3, 4'e yerleşirler; evi 3 olan …042 de kümenin sonuna (5) itilir — **birincil kümelenme**. (b) …050 silinince hücresi MEZAR olur; …058'in araması mezarın üzerinden geçer (3 yoklama). (c) Silinen hücre BOŞ yapılsaydı arama 3'te durur ve …058 "yok" bulunurdu. (d) Yeni …071 eklenirken yokluk BOŞ hücreye kadar doğrulanır, sonra yoldaki ilk mezara yazılır (5 yoklama).*

```
ev(k) = (A · k mod 2^64) >> (64 − p)        ▷ kapasite m = 2^p, A = ⌊2^64/φ⌋ (tek)
algoritma BUL(T, k)                          ▷ ortalama O(1)
    i ← ev(k)
    döngü: T[i] BOŞ ise "yok" döndür
           T[i] DOLU ve T[i].anahtar = k ise T[i].değer döndür
           i ← (i + 1) mod m                 ▷ MEZAR ve başka anahtar: devam
algoritma EKLE(T, k, v)
    yolda ilk MEZAR'ı hatırlayarak k'yi ara (BOŞ'a kadar); bulunursa "zaten var"
    MEZAR varsa oraya yaz                    ▷ (n + mezar) değişmez
    yoksa: (n + mezar + 1)/m > 0,7 ise YENİDEN-KUR    ▷ n + 1 > 0,35·m ise m ← 2m
           BOŞ hücreye yaz
algoritma SİL(T, k)
    k'nin hücresini bul; DOLU → MEZAR        ▷ BOŞ değil: zincir kopmasın
algoritma YENİDEN-KUR(T, m')
    yeni dizi (hepsi BOŞ); her DOLU anahtarı ev'inden yoklayarak yerleştir   ▷ Θ(n); mezarlar düşer
```

- **Neden açık adresleme + doğrusal yoklama?** Anahtar 8 bayt, değer 4 bayttır: hücre 16 bayttır ve tablo **tek bitişik dizidir**. Yoklama ardışık hücrelerde ilerler (önbellek dostu); zincirlemede her kova ayrı ayrılmış düğümlerden oluşan bir bağlı listedir (H8), düğüm başına `malloc` ve bir işaretçi izi gerekir. Bedeli: yük 1'e yaklaştıkça birincil kümelenme yoklamayı hızla uzatır — bu yüzden **eşik** tutulur ve silme **mezar taşı** ister (§ 8.4).
- **Fibonacci (çarpımsal) karma:** çarpımın **üst** p biti alınır; anahtarın bütün bitleri indise katılır (k mod 2^p gibi yalnız düşük bitler değil). Ardışık numaralar (Mini-OBS'nin numaraları) neredeyse kusursuz yayılır: 1..8 anahtarları 8 hücrelik tabloda 4 1 6 3 0 5 2 7 hücrelerine düşer (birim testi). Kapasite 2'nin kuvveti olduğu için mod işlemi yerine kaydırma yapılır.
- **Eşik ve yeniden boyutlandırma:** yük (n + mezar)/m ≤ 0,7. Knuth'a göre doğrusal yoklamada başarılı arama ≈ ½(1 + 1/(1 − α)), başarısız ≈ ½(1 + 1/(1 − α)²) yoklama sürer: α = 0,7'de 2,2 ve 6,1; α = 0,9'da 5,5 ve 50,5. × 2 sonrası yük 0,35'e iner. Yeniden kurma Θ(n)'dir; ama n ekleme boyunca toplam taşınan anahtar < 2n'dir (amortize O(1); § 8.2). Silmeler mezar biriktirirse aynı kapasitede yeniden kurulur (yalnız mezarlar temizlenir).
- **Mezar taşı:** silinen hücre BOŞ yapılırsa, aynı kümede o hücreden sonra yerleşmiş anahtarlar artık bulunamaz (Şekil 1c) — `--hata-goster mezar` bu hatayı kâhine yakalatır (§ 9). Ekleme, anahtarın gerçekten olmadığını BOŞ hücreye kadar doğruladıktan sonra yoldaki **ilk** mezarı yeniden kullanır; aksi hâlde aynı anahtar iki kez eklenebilirdi.
- **`karma_yer` (bul-ya da-ekle):** tek yoklama zinciriyle "varsa değerini ver, yoksa ekle" — yinelenen tespiti ve sayım işlerinin temel adımı (C++ `operator[]`, Python `dict.setdefault`). Dönen adres tablo bir sonraki kez değişene kadar geçerlidir.

| İşlem | En iyi | Ortalama (düzgün karma) | En kötü |
|---|---|---|---|
| bul (başarılı) | 1 yoklama | ½(1 + 1/(1 − α)) | Θ(n) |
| bul (başarısız), ekle | 1 | ½(1 + 1/(1 − α)²) | Θ(n) |
| sil | 1 | başarılı arama | Θ(n) |
| yeniden kurma | — | Θ(n), amortize O(1) | Θ(n) (her eklemede değil) |

### 4.2 Yinelenen numara: karma kümesiyle Θ(n)

```
algoritma YİNELENEN-KARMA(kayıt[0..n−1])     ▷ ortalama Θ(n + P), P: yazılan çift
    T ← boş tablo (n kaydı eşik altında alacak boyutta)
    j = 0 .. n−1 için:
        b ← BUL-YA-DA-EKLE(T, kayıt[j].no)
        yeni ise   b.değer ← j;  son[j] ← j;  boy[j] ← 1         ▷ grubun başı
        değilse    sonraki[son[b.değer]] ← j;  son[b.değer] ← j
                   çift_sayısı ← çift_sayısı + boy[b.değer];  boy[b.değer] ← boy[b.değer] + 1
    i = 0 .. n−1 için:  zincirde i'den sonra gelen her j için (i, j) yaz   ▷ sözlük sırası
```

| Sürüm | Yöntem | Zaman | Ek bellek | Sayılan temel işlem |
|---|---|---|---|---|
| v2.1 | tüm çiftler | Θ(n²) (her zaman n(n−1)/2) | Θ(n) (numara dizisi) | karşılaştırma |
| v2.5 | (numara, indis) kararlı sırala + komşular | Θ(n log n) | Θ(n) | karşılaştırma + taşıma |
| v2.9 | karma kümesi | ortalama Θ(n), en kötü Θ(n²) | Θ(n) (tablo + üç dizi) | yoklama |

- **Aynı sonuç, aynı sıra:** grubun indis zinciri artan sıradadır; çiftler i artan, her i için j artan sırada yazılır — v2.1'in sözlük sırası. Kâhin üç gerçekleştirimi her denemede karşılaştırır (§ 9).
- **Erken çıkış yok:** v2.1'in `yinelenen_var_mi`'si sözlük sırasındaki **ilk** çifti döndürür. Karma kümesinde **ilk rastlanan** çift bu olmayabilir: [5, 7, 7, 5]'te tek geçiş önce (1, 2)'yi görür, sözlükte ilk çift (0, 3)'tür. `yinelenen_var_mi_karma` bu yüzden tam geçiş yapar ve "ilk indisi en küçük olan grubun ilk iki üyesini" seçer (birim testi).

### 4.3 Ad–soyad içinde alt dizgi: katlama, naif, Rabin–Karp

![Rabin–Karp](mini_obs_v2_9_rk.png)

*Şekil 2. "CAN YILMAZ" (örnek veride bir kayıt) içinde "YIL", q = 29: pencere karmaları 7 20 23 22 22 14 14 8; desenin karması 22. s = 3 ("␣YI") karma eşitliğine rağmen ilk baytta düşer — **sahte eşleşme**; s = 4 gerçek eşleşmedir. Değerler birim testinde de sınanır.*

- **Katlama (normalleştirme):** v2.4'ün birincil sırası her kod noktasını bir sıra değerine eşler (küçük = büyük, Türkçe kural i → İ, ı → I; â → A). `tr_katla` her kod noktasını aynı sıra değerli **büyük harfe** çevirir; böylece *sıra değeri eşitliği ⇔ katlanmış bayt eşitliği* (birim testi bunu 0..0x17F'nin bütün çiftlerinde denetler). UTF-8 kendini eşzamanlar (devam baytları 10xxxxxx): geçerli bir desenin geçerli bir metindeki bayt eşleşmesi karakter sınırında başlar ve biter. Arama bu yüzden **baytlar** üzerinde yapılır (alfabe d = 256) ve harf düzeyindeki aramayla aynı sonucu verir. `tolower`/`toupper` kullanılmaz (yerel ayara bağlıdır, İ/ı kuralını bilmez).
- **Metin:** bütün kayıtların katlanmış "AD SOYAD\n" satırları art arda (`AdMetni`, × 2 büyüyen dinamik dizi); desen `\n` içeremeyeceği için eşleşme iki kaydı kesemez; eşleşme konumu ikili aramayla kayda çevrilir.

```
algoritma NAİF(T[0..n−1], P[0..m−1])         ▷ en kötü Θ(n·m), doğal metinde ≈ n
    s = 0 .. n − m için:  j ← 0;  j < m ve T[s+j] = P[j] iken j ← j + 1;  j = m ise s eşleşme
algoritma RABİN-KARP(T, P, d = 256, q)       ▷ beklenen Θ(n + m), en kötü Θ(n·m)
    h ← d^(m−1) mod q;  p ← karma(P);  k ← karma(T[0..m−1])        ▷ Horner
    s = 0 .. n − m için:
        k = p ise                            ▷ ADAY
            T[s..s+m−1] = P ise s eşleşme değilse SAHTE eşleşme    ▷ DOĞRULA
        k ← (d · (k − T[s] · h) + T[s+m]) mod q                  ▷ kaydır, O(1)
```

- **Doğrulama zorunludur:** q'dan fazla farklı pencere vardır; eşit karma eşit metin demek değildir. Doğrulamayı atlamak (karma eşitliğini eşleşme saymak) H10'un Hata Avcısı'ndaki hatadır: `--hata-goster rk` bunu yapar ve kâhin, q = 3 ile tek harfli bir metinde bile yanlış eşleşme bulur — üstelik bir UTF-8 karakterinin **içinde** (§ 9).
- **Gerçekleştirim ayrıntısı (Kaputun Altında):** soldan çıkan baytın payı desen hazırlanırken tablolanır, cikar[b] = d·(q − b·h mod q) mod q; kaydırma k ← (d·k + cikar[T[s]] + T[s+m]) mod q olur — üç mod yerine **bir** mod (d·k < 2⁴⁰: 64 bitte taşmaz). Kalan maliyet pencere başına bir 64 bitlik bölmedir (§ 8.6).
- **q seçimi:** varsayılan q = 2³¹ − 1 (asal). Rastgele bir karma için sahte eşleşme sayısı ≈ (pencere − eşleşme)/q olurdu; doğal metinde pencereler az sayıda farklı bayt üçlüsüdür ve sapma büyüktür (§ 8.6, Tablo 8). Karp ve Rabin (1987) q'yu her aramada **rastgele** seçer: saldırgan sahte eşleşmeyi önceden kuramaz.

### 4.4 Tohumlu karma: numaralar dışarıdan geldiğinde

Fibonacci çarpanı A herkesçe bilinir (bu belgede yazılıdır). Numaraları dışarıdan veren biri (ör. kayıt için CSV yükleyen) A·k mod 2⁶⁴'ün üst bitleri aynı olan numaraları seçerek hepsini **aynı ev hücresine** düşürebilir: her ekleme kümenin sonuna kadar yoklar, n ekleme Θ(n²) olur (karma taşkını saldırısı; Crosby ve Wallach, 2003). `olcer_karma saldiri_sabit` bunu **geçerli 10 basamaklı numaralarla** yapar: 2 400 000 001'den başlayarak çarpımın üst 16 biti 0 olan numaralar (yaklaşık 2¹⁶ adaydan biri) seçilir; bu numaralar kapasite 2¹⁶'ya kadar hep 0. hücreye düşer.

**Savunma:** çarpanı gizli ve rastgele seçmek (`karma_tohumlu_carpan(tohum)`: splitmix64 ile tek bir 64 bitlik sayı). Rastgele tek çarpanlı çarp-kaydır ailesi evrenseldir: iki farklı anahtarın aynı eve düşme olasılığı ≤ 2/2^p'dir (Dietzfelbinger vd., 1997) — saldırgan, çarpanı bilmeden çakışan numara seçemez. Bu kriptografik değildir: zamanlama gözlemiyle çarpan sızdırılabilir; gerçek sistemler tohumu süreç başında işletim sisteminin rastgele kaynağından alır ve anahtarlı bir karma kullanır (Python ve Rust'ta SipHash; Aumasson ve Bernstein, 2012). Bu projede çıktılar **deterministik** olmak zorunda olduğundan tohum komut satırından verilir (`ara --karma --tohum T`); tohumun gizli kalması gerektiği belgede ve başlık yorumunda yazılıdır.

### 4.5 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `karma_ekle`, `karma_yer`, `karma_bul`, `karma_sil` | düz model (anahtar evreni ≤ 40: küçük, negatif ve üst bitli anahtarlar; çarpan Fibonacci, tohumlu, 1 ya da 3; kapasite 8..64; eşik %20..%95 ya da büyüme kapalı): her adımda sonuç, değer, n, yoklama ≥ 1 ve `karma_gecerli_mi`; 8 adımda bir bütün evren aranır |
| `yinelenen_bul_karma`, `yinelenen_var_mi_karma` | v2.1'in kâhini: (numara, indis) sıralanıp bütün grup çiftleri üretilir ve sözlük sırasına dizilir; kısaltılmış (azami) yazımda ilk çiftler; ilk çift |
| `desen_ara` (naif; Rabin–Karp, q ∈ {2, 3, 13, 101, 65521, 2³¹ − 1}; strstr), `desen_kayitlari`, `ad_metni_kayit` | **harf düzeyinde** kâhin: katlanmamış ham metin ve desenin sıra değeri dizilerinde (v2.4) naif eşleme; aynı sayı ve konumlar (bayt konumu → harf indisi); sayaç değişmezleri (pencere = n − m + 1, aday = eşleşme + sahte); küçük bir sınıfta kayıt kayıt sonuç |

## 5. Bellek sahipliği

| Yapı | Kim ayırır | Kim serbest bırakır | Yaşam süresi |
|---|---|---|---|
| `KarmaTablosu.hucre` (kapasite × 16 bayt) | `karma_olustur` (`calloc`: hepsi BOŞ); yeniden kurmada yeni dizi (eski dizi `free`) | `karma_yok_et` | tablo boyunca; değerler kayıt dizisinde **indistir**, tablo kayıtlara sahip olmaz |
| numara dizini (`karma_dizin_kur`) | çağıran (`ara`, `olcer_karma`) | çağıran (`karma_yok_et`) | kayıt dizisi değişene kadar: ekleme/silme indisleri kaydırır, dizin yeniden kurulur |
| `yinelenen_bul_karma`: tablo + `sonraki`, `son`, `boy` | fonksiyonun kendisi | aynı fonksiyon (her çıkış yolunda) | çağrı boyunca |
| `AdMetni.metin`, `AdMetni.bas` | `ad_metni_kur` (`realloc` geçici işaretçiyle, × 2) | `ad_metni_birak` | sınıf değişene kadar |
| `Desen` | çağıranın değişkeni (yığında; dizi ayırmaz) | — | arama boyunca |
| önceki sürümlerin yapıları | v2.8 § 5 | v2.8 § 5 | — |

Ayıran her fonksiyonun yorumunda sahiplik sözleşmesi vardır; yeniden kurma bellek bulamazsa tablo **değişmez** (eski dizi korunur, ekleme başarısız döner). `make asan` (yeni programlar, yeni seçenekler ve kasıtlı hata kipleri dahil) temiz; `make valgrind` 48 çalıştırmanın hepsinde "ERROR SUMMARY: 0 errors" ve "definitely lost: 0 bytes":

```
valgrind ./obs_test_vg → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 20 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 2 --hata-goster mezar → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 5 --hata-goster rk → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ara_vg ornek_veri/ogrenciler.csv --no 2301010050 --karma → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ara_vg ornek_veri/ogrenciler.csv --icinde yıl → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ara_vg ornek_veri/ogrenciler.csv --icinde a --q 13 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./denetle_vg testler/yinelenen_k3.csv --yontem karma → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_karma_vg ara_karma --n 1,300 --sorgu 300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_karma_vg karma_kur --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_karma_vg yin_karma --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_karma_vg yuk_basarisiz --n 1024 --yuk 90 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_karma_vg saldiri_sabit --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_karma_vg desen_rk --n 1,300 --desen nur y --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_karma_vg desen_kotu_naif --n 300 --m 8 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
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

### 6.1 `ara`: karma tablosu ve ad–soyad içinde arama

```
./ara dosya.csv|.dat (--no N | --soyad ÖNEK | --icinde DESEN) [--dogrusal] [--izle] [--karma [--tohum T]]
      [--yontem naif|rk|strstr|hepsi] [--q Q] [--goster K]
```

```
$ ./ara ornek_veri/ogrenciler.csv --no 2301010050 --karma
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 (numaraya göre sıralı: EVET)
Aranan numara: 2301010050
İkili arama (yarı açık [lo, hi)) : sıra 6 · 3 inceleme (en çok ⌊log2 n⌋ + 1 = 4)
İkili arama (kapalı [lo, hi])    : sıra 6 · 2 inceleme
Karma tablosu (doğrusal yoklama)  : sıra 6 · 1 yoklama (ev hücresi 5)
  tablo: kapasite 16 · 8 anahtar · yük α = 0.500 · eşik %70 · çarpan Fibonacci ⌊2^64/φ⌋ · kurma 8 yoklama
Öğrenci no  : 2301010050
Ad Soyad    : EMRE ÇINAR
Algoritma ve Prog. I   96.80  AA  BAŞARILI
Matematik I            69.60  CB  BAŞARILI
Fizik I                78.60  BB  BAŞARILI
YANO        : 3.18
[çıkış kodu: 0]
```

```
$ ./ara ornek_veri/ogrenciler.csv --icinde yıl
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 (numaraya göre sıralı: EVET)
Ad–soyad metni: 8 kayıt · 117 bayt (katlanmış "AD SOYAD" satırları: Türkçe büyük harf, şapkasız)
Desen: "yıl" → "YIL" (3 bayt) · Rabin–Karp: d = 256, q = 2147483647, desen karması 5851468
  Rabin–Karp : 2 kayıt · 2 eşleşme · 115 pencere · 2 aday · 0 sahte · 6 karakter karşılaştırması
  naif       : 2 kayıt · 2 eşleşme · 115 pencere · 122 karakter karşılaştırması
  strstr     : 2 kayıt · 2 eşleşme (kâhin: C kütüphanesi)
Üç yöntem: AYNI (kayıtlar ve eşleşme sayısı)
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   4  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
[çıkış kodu: 0]
```

Küçük q sahte eşleşmeleri görünür kılar; doğrulama sonucu değiştirmez:

```
$ ./ara ornek_veri/ogrenciler.csv --icinde a --q 13
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 (numaraya göre sıralı: EVET)
Ad–soyad metni: 8 kayıt · 117 bayt (katlanmış "AD SOYAD" satırları: Türkçe büyük harf, şapkasız)
Desen: "a" → "A" (1 bayt) · Rabin–Karp: d = 256, q = 13, desen karması 0
  Rabin–Karp : 7 kayıt · 12 eşleşme · 117 pencere · 23 aday · 11 sahte · 23 karakter karşılaştırması
  naif       : 7 kayıt · 12 eşleşme · 117 pencere · 117 karakter karşılaştırması
  strstr     : 7 kayıt · 12 eşleşme (kâhin: C kütüphanesi)
Üç yöntem: AYNI (kayıtlar ve eşleşme sayısı)
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   2  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
   3  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   4  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
   6  2301010050  EMRE ÇINAR                 96.80 AA   69.60 CB   78.60 BB   3.18
   7  2301010051  ŞULE DOĞAN                 55.60 DC   56.20 DC   57.60 DC   1.50
   8  2301010052  ILGAZ ŞAHİN                36.00 FF   86.80 BA   77.00 BB   2.12
[çıkış kodu: 0]
```

### 6.2 `denetle --yontem karma`

```
$ ./denetle testler/yinelenen_k3.csv --yontem karma --erken
Dosya: testler/yinelenen_k3.csv · kayıt: 30
Yöntem: karma kümesi, ilk çift (yinelenen_var_mi_karma; tam geçiş)
Yoklama: 30 (karma tablosu: kapasite 64, n = 30)
İlk yinelenen çift:
  sıra      8 ↔ sıra     11 · numara 2400000017 · MEHMET KESKİN / ŞULE KAYA
Sonuç: yinelenen numara VAR; dosya mini_obs ile yüklenemez.
[çıkış kodu: 1]
```

Üç yöntem aynı çiftleri yazar (`mini_obs_v2_9_ciktilar.txt`, bölüm 4). 20 000 kayıtlık, 40 kasıtlı yinelenenli dosyada temel işlem sayıları: tüm çiftler 199 990 000 karşılaştırma, sıralama 280 832 karşılaştırma, karma kümesi 20 393 yoklama.

## 7. Tasarım kararları

1. **Açık adresleme, doğrusal yoklama** (zincirleme değil): bitişik 16 baytlık hücreler, düğüm ayırma yok, yok etme tek `free`. Birincil kümelenmenin bedeli eşikle sınırlanır (§ 4.1, § 8.4).
2. **Değer = kayıt dizisinde indis** (kaydın kopyası ya da işaretçisi değil): tablo kayıtlara sahip olmaz, 16 baytlık hücre önbelleğe sığar; bedeli, kayıt dizisi değişince dizinin yeniden kurulmasıdır. Kayıt dizisi `realloc` ile taşınabildiği için işaretçi de aynı nedenle geçersizleşirdi.
3. **Fibonacci çarpanı varsayılan, tohumlu çarpan seçenek.** Ardışık numaralar Fibonacci çarpanıyla rastgele karmadan **daha iyi** yayılır (§ 8.4); dış kaynaklı numaralarda tohumlu çarpan kullanılır. Bölme yöntemi (k mod asal) yerine çarpma: kapasite 2'nin kuvveti kalır, bölme yoktur.
4. **Eşik 0,7 ve × 2.** Knuth'a göre başarısız arama 0,7'de ≈ 6, 0,9'da ≈ 50 yoklamadır; 0,5 belleği iki katına çıkarır. Mezarlar eşiğe sayılır (yoklamayı uzatırlar) ve yeniden kurmada düşer.
5. **Bayt düzeyinde desen eşleme, katlanmış metinde.** Harf düzeyinde (kod noktası dizilerinde) Rabin–Karp da yazılabilirdi; katlama + bayt araması `strstr`'yi **kâhin** yapabilmeyi sağlar ve üç dilde aynı sonucu verir (rehber 13.3). Harf düzeyindeki doğruluk ayrıca kâhinle sınanır.
6. **Rabin–Karp'ta tek modlu kaydırma** (önceden hesaplanan `cikar` tablosu) ve **sahte eşleşme sayacı**: algoritmanın kuramdaki maliyetini (pencere başına O(1)) ve doğrulamanın gerekliliğini ölçülebilir kılar.
7. **Yinelenen tespitinde tablo baştan boyutlandırılır** (n bilinir): yeniden kurma yoktur. Dizin kurma ölçümü (`karma_kur`) ise kapasite 8'den büyüyerek amortize maliyeti gösterir.

## 8. Ölçümler

**Düzen:** `-O2`; her nokta için önce sayaç açık bir çalıştırma (yoklama, karşılaştırma, pencere, aday, sahte), sonra 1 ısınma + 5 tekrar, ortanca; veri hazırlama (üretim, sıralama, tablo kurma, sorgu dizisi) süre dışında. `yin_siralama` ve `yin_karma` **üç ayrı süreçte** 7'şer tekrarla ölçüldü; tabloda üç süreç ortancasının ortancası ve (en az–en çok) aralığı vardır. Θ(n²) yöntem için süre bütçesi 30 s'dir: tahmini toplam süresi bütçeyi aşan nokta ölçülmez, önceki ölçümden T(n) ≈ T(n′)·(n/n′)² ile **kestirilir** ve tabloda "≈ …*" ile işaretlenir. Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB, L3 33 MiB; gcc 13.3.0, glibc 2.39; tarih 2026-10-13 16:35. `make olcum` 2 dakika 14 s sürdü; en büyük noktalarda süreç belleğinin tepesi 183 MiB'dir (`getrusage`, çıktılar dosyası; 10⁶ kayıt × 144 bayt + tablo). Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 0,06, sonda 0,90 idi (2 çekirdek; aynı anda başka ajanların derleme ve ölçümleri çalışıyordu: süreler gürültülüdür; yoklama, karşılaştırma ve pencere sayıları değildir).

![Ölçümler](mini_obs_v2_9_olcum.png)

*Şekil 3. Sol üst: yinelenen tespitinin üç yöntemi (log–log; içi boş kareler kestirim, hata çubukları üç sürecin en az–en çok aralığı). Sağ üst: 10⁶ sorguda sorgu başına süre. Sol alt: yük faktörüne göre ortalama yoklama (2²⁰ hücre, büyüme kapalı) ve Knuth'un eğrileri. Sağ alt: karma taşkını — n eklemenin toplam yoklaması (log–log).*

### 8.1 Numarayla arama: ikili arama ↔ karma tablosu

İş yükü: n kayıt (numaralar 2 400 000 001 + 2i; olmayan numaralar aradaki çift farklı sayılar), 10⁶ rastgele sorgu (ortak LCG). İki yöntem de bulunan **kayda erişir**: ikili arama son incelemede kaydın numarasını zaten okumuştur; karma tablosu indisi verir ve kayıt ayrıca okunur.

| n kayıt | ikili, var (ns) | karma, var (ns) | kat | ikili, yok (ns) | karma, yok (ns) | kat | ort. inceleme (ikili) | ort. yoklama (var) | ort. yoklama (yok) | tablo kapasitesi |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 100 000 | 260 | 115 | 2,3 | 335 | 40 | 8,4 | 15,69 | 1,007 | 1,035 | 262 144 |
| 200 000 | 381 | 114 | 3,4 | 471 | 57 | 8,3 | 16,69 | 1,000 | 1,122 | 524 288 |
| 500 000 | 585 | 158 | 3,7 | 755 | 62 | 12,3 | 17,95 | 1,073 | 1,183 | 1 048 576 |
| 1 000 000 | 762 | 186 | 4,1 | 829 | 71 | 11,6 | 18,95 | 1,000 | 1,264 | 2 097 152 |

*Tablo 1. Sorgu başına süre (`olcum/arama.csv`). Kontrol (bulunan indislerin toplamı) iki yöntemde aynıdır.*

- **Karma tablosu 2,3–4,1 kat hızlı** (10⁵ ve 10⁶; bulunan numara). İkili arama ≈ log₂ n inceleme yapar ve her inceleme 144 baytlık başka bir kayda dokunur (10⁶ kayıt = 144 MB: önbellek kaçırması); karma tablosu ortalama ≈ 1 yoklama + kaydın kendisi.
- **Bulunan numarada karma süresinin büyük kısmı kayda erişimdir:** olmayan numarada (yalnız tablo, kayda erişim yok) sorgu 10⁶'da 71 ns, bulunan numarada (tablo + 144 baytlık kayıt) 186 ns'dir. "O(1) arama" pratikte bir ya da iki önbellek kaçırmasıdır; ikili arama ise ≈ log₂ n kayda dokunur.
- **Ardışık numaralarda yoklama ≈ 1:** yük 0,38–0,48 iken ortalama başarılı yoklama 1,00–1,07'dir; rastgele anahtarlarla Knuth'un öngördüğü 1,31–1,46 olurdu (§ 8.4).

### 8.2 Dizinin büyüyerek kurulması: amortize O(1)

İş yükü: n kaydın numaraları, kapasite 8'den başlayan tabloya (eşik 0,7, × 2).

| n anahtar | süre | ns / ekleme | yeniden kurma | taşınan / n | yoklama / n | son kapasite | son yük α |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 100 000 | 23,4 ms | 234 | 15 | 1,835 | 2,958 | 262 144 | 0,381 |
| 200 000 | 28,5 ms | 143 | 16 | 1,835 | 3,065 | 524 288 | 0,381 |
| 500 000 | 64,7 ms | 129 | 17 | 1,468 | 2,633 | 1 048 576 | 0,477 |
| 1 000 000 | 186,2 ms | 186 | 18 | 1,468 | 2,653 | 2 097 152 | 0,477 |

*Tablo 2. n eklemenin toplamı (`olcum/arama.csv`, `karma_kur`). Taşınan anahtar her n'de 2n'den azdır (× 2 büyümede geometrik toplam): ekleme başına amortize O(1). 10⁶'da 18 yeniden kurma, 1 467 992 taşıma.*

Karma dizini 10⁶ kayıtta 186,2 ms'de kurulur (ekleme başına ≈ 186 ns; rastgele hücre yazımı). İkili arama için gereken sıra Mini-OBS'de v2.5'ten beri yüklemede zaten kurulur; karma tablosu sıralı dizinin yerini **almaz**: sıra gerektiren işler (listeleme, önek araması, aralık sorgusu) yine sıralı diziyle yapılır, tablo yalnız tam numara sorusunu hızlandırır.

### 8.3 Yinelenen numara: üç yöntem

İş yükü: uretec ile n kayıt, n/100 kasıtlı yinelenen (numaralar karışık sırada, ham CSV gibi).

| n kayıt | v2.1 tüm çiftler | v2.5 sırala + komşu | v2.9 karma kümesi | çiftler / karma | sıralama / karma | eşit çift |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 166,7 µs | 158,5 µs (136,7 µs–186,6 µs) | 10,8 µs (10,8 µs–16,9 µs) | 15 | 14,7 | 10 |
| 2 000 | 644,1 µs | 294,0 µs (270,2 µs–416,7 µs) | 21,6 µs (21,6 µs–21,7 µs) | 30 | 13,6 | 20 |
| 5 000 | 4,0 ms | 919,5 µs (759,3 µs–1,4 ms) | 116,0 µs (107,4 µs–116,5 µs) | 35 | 7,9 | 50 |
| 10 000 | 17,8 ms | 1,6 ms (1,5 ms–2,8 ms) | 135,1 µs (131,6 µs–143,9 µs) | 132 | 12,1 | 100 |
| 20 000 | 72,7 ms | 3,5 ms (3,5 ms–4,2 ms) | 381,6 µs (370,4 µs–393,3 µs) | 190 | 9,3 | 200 |
| 50 000 | 509,6 ms | 11,2 ms (9,7 ms–13,7 ms) | 3,0 ms (2,9 ms–3,2 ms) | 169 | 3,7 | 502 |
| 100 000 | 1,89 s | 22,9 ms (21,0 ms–28,8 ms) | 8,1 ms (7,5 ms–16,0 ms) | 232 | 2,8 | 1 008 |
| 200 000 | ≈ 7,56 s* | 46,6 ms (45,8 ms–49,3 ms) | 24,1 ms (21,7 ms–24,6 ms) | ≈ 314* | 1,9 | 2 010 |
| 500 000 | ≈ 47,24 s* | 127,8 ms (122,2 ms–131,0 ms) | 62,5 ms (61,7 ms–64,1 ms) | ≈ 756* | 2,0 | 5 025 |
| 1 000 000 | ≈ 188,96 s* | 297,2 ms (294,4 ms–324,3 ms) | 160,2 ms (155,3 ms–183,9 ms) | ≈ 1 180* | 1,9 | 10 055 |

*Tablo 3. Ortanca süre (`olcum/yinelenen.csv`); sıralama ve karma için üç sürecin ortancalarının ortancası (en az–en çok). \* Ölçülmedi: T(n) ≈ T(100 000)·(n/100 000)² kestirimi. Eşit çift sayısı üç yöntemde aynıdır (kestirimli satırlarda iki yöntemde).*

| n kayıt | v2.1 karşılaştırma n(n−1)/2 | v2.5 karşılaştırma | v2.5 taşıma (anahtar) | v2.9 yoklama |
|--:|--:|--:|--:|--:|
| 1 000 | 499 500 | 9 726 | 19 952 | 1 001 |
| 2 000 | 1 999 000 | 21 437 | 43 904 | 2 000 |
| 5 000 | 12 497 500 | 60 244 | 123 616 | 5 104 |
| 10 000 | 49 995 000 | 130 385 | 267 232 | 10 000 |
| 20 000 | 199 990 000 | 280 947 | 574 464 | 20 389 |
| 50 000 | 1 249 975 000 | 768 192 | 1 568 928 | 50 000 |
| 100 000 | 4 999 950 000 | 1 636 266 | 3 337 856 | 100 000 |
| 200 000 | 19 999 900 000 (formül) | 3 472 369 | 7 075 712 | 200 000 |
| 500 000 | 124 999 750 000 (formül) | 9 337 360 | 18 951 424 | 500 000 |
| 1 000 000 | 499 999 500 000 (formül) | 19 673 919 | 39 902 848 | 1 000 000 |

*Tablo 4. Temel işlem sayıları (sayaç açık çalıştırma; üç süreçte aynı).*

**Yorum.**

- **Sayaçlarda asimptotik sıra kesindir** (Tablo 4): n 10 kat büyüdüğünde n(n−1)/2 karşılaştırma ≈ 100 kat, sıralamanın karşılaştırma + taşıması ≈ 12–14 kat, karma kümesinin yoklaması 10 kat artar. **Süreler** bu oranlardan sapar: n × 10'da tüm çiftler 107, 106 kat, sıralama 10,3, 14,0, 13,0 kat, karma kümesi 12,5, 60,2, 19,7 kat (10³ → 10⁴ → 10⁵ → 10⁶) — karma kümesinde 10⁴ → 10⁵ adımında tablo 512 KiB'tan (2¹⁵ hücre) 4 MiB'a (2¹⁸ hücre) büyür ve L2'ye (2 MiB) sığmaz olur; sıçramanın olası açıklaması budur. Tüm çiftler 10⁵'te 1,89 s, karma kümesinin 232 katı; 10⁶'da kestirim ≈ 188,96 s. Bir karşılaştırma ≈ 0,38 ns'dir (≈ bir saat çevrimi; numaralar bitişik bir diziye kopyalandığı için önbellekte ve dal neredeyse hep aynı yöne gider) — Θ(n²)'yi yenen sabit çarpan değil, n'dir.
- **Karma ↔ sıralama: n ≤ 2·10⁴'te 7,9–14,7 kat, n ≥ 5·10⁴'te yalnız 1,9–3,7 kat.** İşlem sayısı farkı ≈ log₂ n kadar büyürken süre farkı küçülür: tablo L2'den (2 MiB) taşınca her yoklama rastgele bir önbellek kaçırmasıdır; birleştirmeli sıralama ise belleği **ardışık** okur ve yazar (donanım ön getirmesi). "Θ(n) Θ(n log n)'den hızlıdır" önermesi bu ölçekte sabit çarpanlara ve bellek erişim örüntüsüne bağlıdır — v2.7'nin dizi ↔ liste dersinin karma tablosundaki karşılığı.
- **Gürültü:** karma kümesinin süresi aynı n'de süreçten sürece %104'e kadar oynadı (n ≥ 2·10⁴; sıralamada en çok %36): rastgele erişim, bellek yerleşimine ve paylaşılan makinedeki öbür süreçlere duyarlıdır. Bu yüzden üç süreç ölçüldü; sayaçlar süreçten bağımsızdır.

### 8.4 Yük faktörü ve ortalama yoklama

İş yükü: 2²⁰ hücrelik tablo (büyüme kapalı) ⌊α·2²⁰⌋ anahtarla doldurulur; bütün anahtarlar (başarılı) ya da aynı sayıda olmayan anahtar (başarısız) aranır. Rastgele anahtarlar: ortak LCG'den 63 bit; ardışık: 2 400 000 001, 2 400 000 002, …

| α | başarılı (ölçülen) | Knuth ½(1 + 1/(1−α)) | başarısız (ölçülen) | Knuth ½(1 + 1/(1−α)²) | başarılı, ardışık | başarısız, ardışık | ns / başarılı | ns / başarısız |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0,100 | 1,056 | 1,056 | 1,12 | 1,12 | 1,000 | 1,00 | 68 | 67 |
| 0,200 | 1,125 | 1,125 | 1,28 | 1,28 | 1,000 | 1,00 | 62 | 66 |
| 0,300 | 1,214 | 1,214 | 1,52 | 1,52 | 1,000 | 1,03 | 65 | 75 |
| 0,400 | 1,331 | 1,333 | 1,89 | 1,89 | 1,000 | 1,08 | 74 | 119 |
| 0,500 | 1,500 | 1,500 | 2,51 | 2,50 | 1,002 | 1,32 | 73 | 94 |
| 0,600 | 1,751 | 1,750 | 3,64 | 3,62 | 1,016 | 1,56 | 75 | 104 |
| 0,700 | 2,173 | 2,167 | 6,09 | 6,06 | 1,026 | 2,12 | 92 | 194 |
| 0,800 | 3,017 | 3,000 | 13,10 | 13,00 | 1,045 | 3,01 | 132 | 226 |
| 0,900 | 5,551 | 5,500 | 51,52 | 50,50 | 1,197 | 5,88 | 109 | 333 |
| 0,950 | 10,794 | 10,500 | 210,13 | 200,50 | 1,284 | 12,60 | 208 | 703 |

*Tablo 5. Arama başına ortalama yoklama (`olcum/yuk.csv`). α ≤ 0,9'da rastgele anahtarlarla ölçülen değer Knuth'un formülünden en çok %2,0 sapar.*

- **Kuram tutuyor:** rastgele anahtarlarla ölçülen yoklama, düzgün karma varsayımından türetilen formüllere çok yakındır; α = 0,95'te başarısız arama 210 yoklamaya çıkar (birincil kümelenme). Eşik 0,7'de başarısız arama 6,1 yoklamadır.
- **Ardışık numaralar kuramdan iyi:** Fibonacci çarpanı ardışık anahtarları düzgün aralıklarla dağıtır (üç uzaklık teoremi; Knuth, 1998, Kısım 6.4); kümeler kısa kalır: α = 0,95'te başarısız arama 12,6 yoklama. Bu, Mini-OBS'nin numaralarının iyi davranmasının nedenidir — ama saldırganın seçtiği numaralar için güvence değildir (§ 8.5).
- **Süre yoklamayı izler:** rastgele anahtarla başarısız arama α = 0,1'de 67 ns, α = 0,95'te 703 ns sürer; yoklamalar ardışık hücrelerde olduğu için yoklama başına maliyet düşer (aynı önbellek satırı), ama küme uzadıkça satırlar da artar.

### 8.5 Karma taşkını saldırısı ve tohumlu çarpan

İş yükü: n numara, kapasite 8'den büyüyen tablo (eşik 0,7). Saldırı numaraları geçerli 10 basamaklı numaralardır (§ 4.4); "rastgele" satırı rastgele 10 basamaklı numaralardır.

| n numara | sabit çarpan: yoklama | süre | yoklama / n² | tohumlu: yoklama | süre | rastgele numara: yoklama | süre | yoklama oranı | süre oranı |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 844 318 | 792,1 µs | 0,844 | 3 379 | 38,7 µs | 4 419 | 44,0 µs | 250 | 20 |
| 2 000 | 3 373 713 | 4,5 ms | 0,843 | 8 593 | 84,8 µs | 8 957 | 93,0 µs | 393 | 53 |
| 4 000 | 13 488 859 | 21,9 ms | 0,843 | 21 031 | 196,9 µs | 18 340 | 207,6 µs | 641 | 111 |
| 8 000 | 53 938 839 | 62,5 ms | 0,843 | 47 161 | 547,3 µs | 36 412 | 887,5 µs | 1 144 | 114 |
| 16 000 | 215 717 554 | 216,0 ms | 0,843 | 102 596 | 784,3 µs | 73 028 | 2,0 ms | 2 103 | 275 |

*Tablo 6. n eklemenin toplamı (`olcum/saldiri.csv`); yoklama yeniden kurmadaki yoklamaları da içerir. Oranlar sabit çarpan / tohumlu.*

- **Sabit çarpanla Θ(n²):** yoklama / n² ≈ 0,84 sabit kalır (n eklemenin ½n² yoklaması + yeniden kurmalar); n iki katına çıkınca yoklama dört katına çıkar. 16 000 numarada 215 717 554 yoklama, 216,0 ms.
- **Aynı numaralar tohumlu çarpanla doğrusaldır:** 102 596 yoklama, 784,3 µs — rastgele numaralarla aynı mertebe. Savunmanın maliyeti bir çarpanın seçilmesidir.
- **Saldırganın maliyeti küçüktür:** 16 000 numara için 1 048 547 133 aday numara taranır (≈ 2¹⁶ adayda bir; son numara 3448547133, hâlâ 10 basamaklı) ve bu, bu makinede 1,51 s sürer (`olcer_karma`'nın stderr'i). 10⁵ numaralık bir saldırının ekleme süresi n² ile ölçeklenerek ≈ 8,44 s olurdu (kestirim; ölçülmedi) — tohumlu çarpanla milisaniyeler.
- Süreler milisaniyenin altında gürültülüdür (tohumlu ve rastgele satırları); karşılaştırmanın kesin ölçüsü yoklama sayısıdır.

### 8.6 Alt dizgi araması (10⁵ kayıt)

İş yükü: uretec ile 10⁵ kayıt; katlanmış "AD SOYAD\n" metni 1 357 400 bayt; her yöntem deseni içeren kayıtları bulur (q = 2³¹ − 1).

| desen (katlanmış) | kayıt | eşleşme | naif | bayt / pencere | Rabin–Karp | aday | sahte | strstr | RK / naif | naif / strstr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `yıl` → `YIL` | 7 533 | 7 533 | 3,3 ms | 1,031 | 16,4 ms | 7 533 | 0 | 409,4 µs | 5,0 | 8,0 |
| `öz` → `ÖZ` | 12 197 | 12 473 | 2,9 ms | 1,050 | 15,7 ms | 12 473 | 0 | 635,3 µs | 5,4 | 4,6 |
| `nur y` → `NUR Y` | 609 | 609 | 2,7 ms | 1,057 | 15,7 ms | 609 | 0 | 219,8 µs | 5,9 | 12,1 |
| `mehmet ali` → `MEHMET ALİ` | 2 539 | 2 539 | 2,6 ms | 1,076 | 15,2 ms | 2 539 | 0 | 482,5 µs | 5,9 | 5,3 |
| `xyz` → `XYZ` | 0 | 0 | 1,7 ms | 1,000 | 15,0 ms | 0 | 0 | 68,1 µs | 8,8 | 25,0 |

*Tablo 7. Ortanca süre (`olcum/desen.csv`). Üç yöntem aynı kayıtları ve eşleşme sayısını verir; "öz" bazı kayıtlarda iki kez geçer (ÖZLEM ÖZKAN).*

- **Doğal metinde naif yöntem kazanır:** pencere başına 1,00–1,08 bayt karşılaştırır (çoğu pencere ilk baytta düşer); Rabin–Karp pencere başına bir 64 bitlik mod alır (≈ 11,5 ns ↔ naif ≈ 2,0 ns). `strstr` (glibc; vektör komutları, uzun desenlerde iki yönlü algoritma) bir mertebe daha hızlıdır.
- **Rabin–Karp'ın değeri karma eşitliğinin seyrekliğindedir:** doğrulanan pencere sayısı = aday sayısıdır (sahte 0); naifin en kötü durumunda (n = 1 000 000 baytlık "AAA…A" içinde m = 32 baytlık "AA…AB") naif 31 999 008 karşılaştırma ve 22,4 ms, Rabin–Karp 0 aday ve 11,5 ms (2,0 kat hızlı; `olcum/desen_kotu.csv`). Çok desenli arama (aynı uzunlukta k desen, karmalar bir kümede) da Rabin–Karp'ın doğal kullanımıdır.

| q | aday | eşleşme | sahte | rastgele karma beklentisi (pencere − eşleşme)/q | süre |
|--:|--:|--:|--:|--:|--:|
| 2 | 734 671 | 7 533 | 727 138 | 674 932,5 | 20,8 ms |
| 13 | 130 079 | 7 533 | 122 546 | 103 835,8 | 17,7 ms |
| 101 | 13 092 | 7 533 | 5 559 | 13 365,0 | 15,9 ms |
| 1 009 | 12 565 | 7 533 | 5 032 | 1 337,8 | 15,2 ms |
| 10 007 | 7 533 | 7 533 | 0 | 134,9 | 15,6 ms |
| 2 147 483 647 | 7 533 | 7 533 | 0 | 0,00063 | 15,5 ms |

*Tablo 8. Desen "yıl", modül q'ya göre aday ve sahte eşleşme (`olcum/desen_q.csv`). Doğrulama sayesinde eşleşme sayısı her q'da aynıdır.*

- **q küçüldükçe sahte eşleşme artar, sonuç değişmez.** q = 101'de 5 559, q = 1009'da 5 032 sahte eşleşme; q = 10007'de 0.
- **"≈ pencere/q" yalnız rastgele metin içindir:** doğal metinde pencereler az sayıda farklı bayt üçlüsüdür; belirli bir q'da sık geçen bir üçlü desenle çakışırsa binlerce sahte eşleşme (q = 1009), çakışmazsa sıfır (q = 10007) görülür. Sahte eşleşme sayısını güvenceye almak için q büyük **ve** aramadan aramaya rastgele seçilir (Karp ve Rabin, 1987).

### 8.7 Sınırlılıklar

Süreler paylaşılan bir sanal makinede, yük altında ölçüldü (yukarıda); yoklama, karşılaştırma, pencere ve aday sayıları makineden bağımsızdır. Karma tablosu yalnız numara → indis eşlemesidir (kayıt kopyası tutmaz); tablonun kendi belleği ayrıca ölçülmedi, hesaplanır (hücre 16 bayt × kapasite: 10⁶ kayıtta 2²¹ hücre = 32 MiB); süreç tepe belleği § 8'in başındadır. Zincirlemeyle doğrudan karşılaştırma bu sürümde yoktur (ders notunun deneyi). Kestirimler (Tablo 3, *) ölçüm değildir.

## 9. Testler

- **Birim testleri** (`obs_test`): `389 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama + 23 böl-fethet + 19 öbek-doğrusal + 79 bağlı liste + 29 yığın-kuyruk + 36 karma-desen`. Karma-desen testleri: kapasite yuvarlama ve tek çarpan; 1..8'in Fibonacci evleri (bir permütasyon); negatif anahtar; ekle/bul/sil ve ZATEN VAR; `karma_yer`; çarpan 1 ile mezar taşı zinciri (yoklama 3 ve 4; ilk mezarın yeniden kullanımı; kasıtlı bozmada kaybolan anahtar ve `karma_gecerli_mi`); Şekil 1'in gerçek numaralı örneği (birincil kümelenme; yoklama 3 ve 5); 6. anahtarda × 2 büyüme; yalnız mezar temizleyen yeniden kurma; büyüme kapalıyken dolma; kapasite hesabı; tohumlu çarpan; numara dizini ve yinelenen numarada reddi; karma kümesiyle yinelenen = v2.1 = v2.5 (yinelenen_k3.csv), [5, 7, 7, 5] ve üçlü grup; Türkçe katlama ve UTF-8 gidiş-dönüş; sıra değeri ⇔ katlama denkliği; Horner karması; örtüşen eşleşmeler; q = 13'te sahte eşleşme; Şekil 2'nin örneği; naifin en kötü durumu; ad–soyad metni, kayıt eşleme ve büyük/küçük harf duyarsızlığı.
- **Kâhin testleri** (`test_kahin`): 300 denemede 670 897, 1 000 denemede 2 249 368 denetim (karma tablosu ve karma kümesi: 522 654; alt dizgi: 59 679), uyuşmazlık yok.
- **Kasıtlı hatalar.** (a) `--hata-goster mezar` — silinen hücre BOŞ yapılır; rastgele denemede değişmez denetimi yakalar, sonra çarpan 1 ile 1..4 işlemlik bütün diziler denenerek **gözlenebilir** en kısa karşı örnek basılır (4 işlem: `ekle(2); ekle(1); sil(2); bul(1)`):

```
$ ./test_kahin --hata-goster mezar
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : karma tablosu (karma.h)
  n          : 155
  Beklenen   : düz model (çarpan Fibonacci, kapasite 32, eşik %70, evren 34): 59. işlem sil
  Bulunan    : değişmez bozuk (karma_gecerli_mi)
  En kısa karşı örnek (çarpan 1: anahtarların hepsi 0. hücreye; 4 işlem): ekle(2); ekle(1); sil(2); bul(1) → bul(1): yok (beklenen var)
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster mezar
[çıkış kodu: 1]
```

  (b) `--hata-goster rk` — Rabin–Karp karma eşitliğini doğrulamadan eşleşme sayar; en kısa karşı örnek q = 3 ile metin "Ç", desen "B": "Ç"nin iki baytı (C3 = 195 ve 87 = 135) da 66 ≡ 0 (mod 3) ile aynı karmayı taşır — doğrulamasız sürüm bir harfin **içinde** 2 "eşleşme" bulur:

```
$ ./test_kahin --hata-goster rk
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : alt dizgi (desen.h)
  n          : 47
  Beklenen   : harf düzeyinde 2 eşleşme (metin "âA AAIaaİİâAçBI ıbIŞâ-şâAÂıBçÂAÂIIŞŞşB", desen "ç", q = 3)
  Bulunan    : Rabin–Karp: 16 eşleşme
  En kısa karşı örnek (q = 3): metin "Ç", desen "B" → 2 eşleşme (beklenen 0; karmalar eşit: 0 = 0)
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster rk
[çıkış kodu: 1]
```

## 10. Ders notu için özet (Hafta 10 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'ye bir **numara → kayıt karma tablosu** ekliyoruz (açık adresleme, doğrusal yoklama, mezar taşı, yük eşiği ve × 2 yeniden boyutlandırma), yinelenen numara tespitini **karma kümesiyle O(n)'e** indirip v2.1 (Θ(n²)) ve v2.5 (Θ(n log n)) ile aynı veride karşılaştırıyoruz ve ad–soyad içinde **büyük/küçük harf duyarsız alt dizgi araması** için naif yöntemi ve **Rabin–Karp**'ı yazıyoruz.

### Gereksinimler

- `karma.h/.c`: `long long` anahtar → `int` değer tablosu; açık adresleme + doğrusal yoklama; kapasite 2'nin kuvveti; Fibonacci karması `ev(k) = (A·k mod 2⁶⁴) >> (64 − p)`; hücre durumu BOŞ/DOLU/MEZAR; `karma_olustur`, `karma_bul`, `karma_ekle`, `karma_sil` (mezar taşı), `karma_yok_et`; yük (n + mezar)/kapasite > 0,7 olacaksa × 2 yeniden boyutlandırma; değişmez denetleyicisi.
- `karma_dizin_kur(t, sinif)`: numara → kayıt indisi; `ara --no N --karma` yoklama sayısını basar.
- `yinelenen_bul_karma`: v2.1 ile **aynı çiftler, aynı sözlük sırası**; `denetle --yontem karma`.
- `desen.h/.c`: katlanmış ad–soyad metni; `desen_ara` naif ve Rabin–Karp (d = 256, q asal; **karma eşitliği bayt bayt doğrulanır**; aday ve sahte eşleşme sayaçları); `ara --icinde DESEN` üç yöntemin (naif, Rabin–Karp, `strstr`) sonucunu karşılaştırır.
- Türkçe katlama: v2.4'ün sıra değeriyle uyumlu (`tr_katla`): "yıl" → "YIL", "ilgaz" → "İLGAZ", "âşık" → "AŞIK".
- Testler: karma tablosu ↔ düz model (rastgele işlem dizileri, her adımda değişmez); karma kümesi ↔ v2.1; desen ↔ harf düzeyinde kâhin ve `strstr`.
- Ölçüm: ikili arama ↔ karma (10⁵–10⁶); üçlü yinelenen n = 10³…10⁶ (Θ(n²) için süre bütçesi + işaretli kestirim); yük faktörüne göre ortalama yoklama ve Knuth'un formülleri; 10⁵ kayıtta alt dizgi araması (sahte eşleşme sayısıyla).

### İpuçları

- Kapasiteyi 2'nin kuvveti tutun: indis `(carpan * (uint64_t)k) >> (64 - p)`; `%` yok, negatif indis yok (H1'in kalan işareti tuzağı burada çıkmaz). İşaretli taşma tanımsızdır, **işaretsiz** taşma mod 2⁶⁴ sarar: çarpımı `uint64_t` ile yapın.
- Silmede hücreyi BOŞ yapmayın; MEZAR yapın. Aramada MEZAR'ın üzerinden geçin, eklemede ilk MEZAR'ı hatırlayın ama yokluğu BOŞ hücreye kadar doğrulayın.
- Eşiği (n + mezar) ile denetleyin; mezarlar da yoklamayı uzatır. Yeniden kurmada yalnız DOLU hücreleri taşıyın.
- Tabloyu `calloc` ile ayırın: hepsi BOŞ (durum 0) başlar. Yeniden kurmada yeni diziyi ayıramazsanız eskisini **bırakmayın** (tablo değişmesin).
- Yinelenen tespitinde değer olarak grubun **ilk** indisini, ayrıca her grubun sonunu ve boyunu tutun: çiftler sözlük sırasında yazılabilir, toplam Σ C(g, 2) yazmadan bulunur.
- Rabin–Karp'ta karma eşitliğinden sonra **mutlaka** baytları karşılaştırın; sayaçta aday = eşleşme + sahte olmalıdır. Küçük bir q (13, 101) ile sahte eşleşmeleri görün.
- Kaydırma formülünde çıkarmadan önce q ekleyin (`(k + q − x) % q`) ya da çıkan baytın payını önceden tablolayın; `uint64_t` ile d·k taşmaz.
- Katlamayı `toupper` ile değil, v2.4'ün tablosuyla yapın; desen ile metni **aynı** fonksiyonla katlayın.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri (389) ve `test_kahin` (300 deneme) geçer.
2. `./ara ornek_veri/ogrenciler.csv --no 2301010050 --karma` şu satırı basar: `Karma tablosu (doğrusal yoklama)  : sıra 6 · 1 yoklama (ev hücresi 5)`; ikili arama aynı kaydı (sıra 6) bulur.
3. 8 hücrelik tabloya (Fibonacci çarpanı) 2301010045, …050, …058 ve …042 eklenince hücreler 2–5 dolar; …050 silinince …058 3 yoklamada bulunur; …071 eklenince 5 yoklamayla [3] hücresine (mezara) yazılır. Kapasite 8'de 6. anahtar tabloyu 16'ya büyütür.
4. `./ara ornek_veri/ogrenciler.csv --icinde yıl` üç yöntemde de `2 kayıt · 2 eşleşme` ve `Üç yöntem: AYNI` basar; `--icinde ilgaz` 0 kayıt, `--icinde ılgaz` 1 kayıt (ILGAZ ŞAHİN) bulur.
5. `./ara ornek_veri/ogrenciler.csv --icinde a --q 13` Rabin–Karp için `Rabin–Karp : 7 kayıt · 12 eşleşme · 117 pencere · 23 aday · 11 sahte · 23 karakter karşılaştırması` basar (sahte eşleşmeler doğrulamayla elenir; eşleşme sayısı naifle aynı).
6. `./denetle testler/yinelenen_k3.csv --yontem karma` v2.1 ve v2.5 ile aynı üç çifti aynı sırada yazar ve 1 ile çıkar; `--erken` aynı ilk çifti (sıra 8 ↔ 11) verir.
7. `./test_kahin --hata-goster mezar` ve `--hata-goster rk` uyuşmazlık basar ve 1 ile çıkar; `make asan` ve `make valgrind` temizdir.
8. Ölçüm raporunda: üç yöntemin n = 10³…10⁶ süreleri (Θ(n²) için işaretli kestirimle) ve eşit çift sayılarının aynılığı; 10⁵–10⁶ kayıtta ikili arama ↔ karma; en az beş yük değerinde ölçülen ortalama yoklama ile Knuth'un formülü; 10⁵ kayıtta alt dizgi araması süresi ve sahte eşleşme sayısı.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | 8 hücre, anahtarlar 1..8'in evleri (Fibonacci) | [4] [1] [6] [3] [0] [5] [2] [7] (hepsi farklı) |
| 2 | ekle 10 → ekle 10 → bul 10 | EKLENDİ, ZATEN VAR (değer değişmez), bulundu |
| 3 | çarpan 1: ekle 1, 2, 3; sil 2; bul 3 | bulundu, 3 yoklama (mezarın üzerinden) |
| 4 | aynı tablo: bul 5 (yok) | yok, 4 yoklama ([3] BOŞ) |
| 5 | aynı tablo: ekle 4 | [1] hücresine (mezar) yazılır; mezar 0 |
| 6 | kapasite 8, 6 anahtar | 6.'da kapasite 16, yeniden kurma 1, taşınan 5 |
| 7 | büyüme kapalı (eşik %100), kapasite 8 | 7 anahtar girer, 8.'si reddedilir; arama sonlanır |
| 8 | numaralar [5, 7, 7, 5] | çiftler (0, 3), (1, 2); ilk çift (0, 3) |
| 9 | [9, 9, 9], azami 2 | dönüş 3, yazılan (0, 1), (0, 2) |
| 10 | `--icinde ilgaz` / `--icinde ılgaz` | 0 kayıt / ILGAZ ŞAHİN |
| 11 | "CAN YILMAZ" içinde "YIL", q = 29 | 2 aday, 1 sahte, eşleşme konum 4 |
| 12 | "AAAAAAAA" içinde "AAB" | naif 6 pencere × 3 = 18 karşılaştırma; Rabin–Karp 0 aday |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.8'iniz (ya da referans v2.8), `karma.h` ve `desen.h` (bildirimler, sözleşmeler, sahiplik), `tr_katla`'nın tablosu (v2.4'ün `turkce.c`'si), `olcer_karma`'nın ölçüm düzeneği (veri üretimi, sorgu dizisi, saldırı numaralarının üretimi), Şekil 1 ve 2'nin örnekleri.
- **Yazılır:** `karma.c` (bul, ekle, sil, yeniden kurma, değişmez), `yinelenen_bul_karma`, `desen.c` (naif, Rabin–Karp, ad–soyad metni), `ara` ve `denetle`'ye yeni seçenekler; testler (birim + kâhin); ölçüm ve yorum.
- **Değiştirilmez:** v1.0 kuralları ve menü, kayıt dizisinin numara sırası, v2.4'ün Türkçe sırası, ortak modüller.
- **Meydan okuma:** (a) ayrı zincirlemeli tablo yazın ve § 8.4'ün deneyini zincirlemede de yapın (beklenen 1 + α/2 ve α + e^(−α)); (b) robin hood yoklaması ya da geri kaydırmalı silme (mezarsız) ile karşılaştırın; (c) çok desenli Rabin–Karp (k desen, karmalar bir karma kümesinde); (d) KMP'yi yazın ve naifin en kötü durumunda üç yöntemi karşılaştırın.

## 11. Bilinen sınırlılıklar

- Numara dizini kayıt dizisi değişince geçersizleşir; `kayit` oturumundaki ekleme/silmeler dizini güncellemez (dizin yalnız `ara` ve ölçümlerde kurulur).
- Tohumlu çarpan kriptografik değildir; tohum komut satırından verilir (deterministik çıktı için). Rabin–Karp'ın q'su sabittir (varsayılan 2³¹ − 1); rastgele q seçimi yoktur.
- Katlama birincil sıra eşitliğidir: "HALE" ile "HÂLE" aynıdır; ikincil (bayt) farkı aramada yok sayılır. Yalnız Türkçe alfabe ve ASCII için büyük/küçük harf kuralı vardır.
- Süreler paylaşılan makinede yük altında ölçüldü; karma kümesinin süresi süreçten sürece oynuyor (§ 8.3).

## 12. Kaynaklar

- Aumasson, J.-P., & Bernstein, D. J. (2012). SipHash: A fast short-input PRF. In *Progress in Cryptology – INDOCRYPT 2012* (pp. 489–508). Springer.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Crosby, S. A., & Wallach, D. S. (2003). Denial of service via algorithmic complexity attacks. In *Proceedings of the 12th USENIX Security Symposium* (pp. 29–44). USENIX Association.
- Dietzfelbinger, M., Hagerup, T., Katajainen, J., & Penttonen, M. (1997). A reliable randomized algorithm for the closest-pair problem. *Journal of Algorithms, 25*(1), 19–51.
- Karp, R. M., & Rabin, M. O. (1987). Efficient randomized pattern-matching algorithms. *IBM Journal of Research and Development, 31*(2), 249–260.
- Knuth, D. E. (1998). *The art of computer programming: Vol. 3. Sorting and searching* (2nd ed.). Addison-Wesley.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
