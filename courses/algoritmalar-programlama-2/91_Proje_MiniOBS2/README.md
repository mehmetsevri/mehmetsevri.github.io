# Mini-OBS 2 — Dönem Projesi Yönergesi (Algoritma ve Programlama – II)

**AP-1'de programı kurduk, AP-2'de ölçekliyoruz.** AP-1'in son haftasında Mini-OBS v1.0'ı bitirdik: yapı dizisiyle tutulan öğrenci kayıtları, CSV ve ikili dosyada kalıcılık, dört modüllü bir C programı ve 99 birim doğrulama. Program sekiz öğrenciyle sorunsuz çalışıyordu. AP-2'de aynı programa **10⁶ öğrenci** veriyoruz ve her hafta o haftanın algoritmasıyla onu büyütüyoruz. Her iyileştirme bir **ölçümle** belgelenir ve her yeni algoritma, doğruluğu apaçık ama yavaş bir **kâhine** karşı sınanır. Dönemin sonunda (H14, [v3.0](v3.0/mini_obs_v3_0.md)) arama, sıralama, karma, liste/kuyruk, önkoşul grafı, sınav programı, ders seçimi optimizasyonu ve öneri modüllerini menü güdümlü tek bir uygulamada bütünleştiriyoruz (Yol Haritası, Ek A); final projesi bu sürümdür ([yönerge](FINAL_PROJE_YONERGESI.md)).

İlk ölçüm bunun neden gerekli olduğunu gösterir (v2.0): v1.0'ın yükleyicisi her kaydı eklerken mükerrer numara için bütün diziyi tarar; 10⁵ kayıt bu makinede 17,1 s'de yüklenir, 10⁶ kaydın yüklenmesi ise ≈ 1,6 saat sürerdi (kestirim). Aynı veride üç dersin istatistiği 0,1 saniyenin altındadır. **Darboğaz bir algoritmadır, dil ya da donanım değil** — ve dönem boyunca aynı problemi üç kez, her seferinde daha iyi bir algoritmayla çözeceğiz.

## 1. v1.0'dan devralınanlar

- **Veri modeli** (değişmez): `DersNotu { vize, final, ort }`, `Ogrenci { no, ad[32], soyad[32], DersNotu ders[3] }`, `Sinif { Ogrenci *kayit; int n, kapasite; }`; `sizeof(Ogrenci)` = 144 bayt (gcc, x86-64).
- **Dosya biçimleri** (değişmez): `;` ayraçlı UTF-8 CSV, başlık `no;ad;soyad;ALG_vize;ALG_final;MAT_vize;MAT_final;FIZ_vize;FIZ_final`, ondalık ayırıcı nokta, BOM ve CRLF kabul; ikili "MOBS" biçimi (16 baytlık başlık + kayıtlar). Dosyadan gelen her alan klavye girdisiyle aynı kurallarla denetlenir; bozuk dosya yarım yüklenmez; kaydetme önce `<yol>.tmp`'ye yazar.
- **Modüller**: `metin` (güvenli girdi, sayı çözümleme, Türkçe ad normalleştirme), `obs` (kurallar, istatistik, raporlar), `dosya` (kalıcılık), `main` (menü). RTEÜ not kuralları (%40 vize + %60 final, final barajı, harf notları, YANO) v1.0'daki gibidir.
- **Testler**: v1.0'ın 99 birim doğrulaması her sürümde aynen geçmelidir (regresyon güvencesi).
- **Kod alışkanlıkları**: `fgets` + `strtol`/`strtod` ile denetimli girdi; `const` doğru kullanım; tek temizlik yolu; ASan/UBSan/Valgrind temiz.

Kendi v1.0'ınızla başlayabilirsiniz; eksikleriniz varsa referans v1.0'ı (AP-1, `91_Proje_MiniOBS/v1.0`) kullanın. Her iki durumda da veri modeli ve dosya biçimi **aynı** kalmalıdır: veri üreteci, ölçüm araçları ve kâhinler buna dayanır.

## 2. Sürüm yol haritası

Tablo A.1 (Yol Haritası, Ek A) — Mini-OBS 2 sürümleri, eklenen yetenekler ve kullanılan algoritmalar:

| Hafta | Sürüm | Eklenen yetenek | Algoritma / kavram |
|---|---|---|---|
| H1 | v2.0 | Sentetik veri üreteci (10³–10⁶ kayıt), zamanlayıcı modülü, kâhin test altyapısı | Ortak LCG, ölçüm düzeni, karşılaştırmalı test |
| H2 | v2.1 | İşlem sayaçlı istatistikler; yinelenen numara tespiti (O(n²)) | Asimptotik analiz, oran testi |
| H3 | v2.2 | AKTS aralığına uyan ders kombinasyonları | Geri izleme, budama |
| H4 | v2.3 | Numaraya göre ikili arama; soyad önekiyle arama | İkili arama, lower_bound |
| H5 | v2.4 | Çok ölçütlü sıralı listeler; Türkçe alfabetik karşılaştırıcı | Karşılaştırıcı, kararlılık |
| H6 | v2.5 | Büyük veri sıralama; şube listelerini birleştirme; ortanca not; O(n log n) yinelenen tespiti | Birleştirmeli sıralama, quickselect |
| H7 | v2.6 | Not dağılımı, ilk-k listesi, numaraya taban sıralaması, ölçüm raporu (ara proje) | Sayma/taban sıralaması, öbek |
| H8 | v2.7 | Bekleme listesi; sıralı listelerin birleştirilmesi | Bağlı liste, bellek sahipliği |
| H9 | v2.8 | Geri al/yinele; ders kayıt kuyruğu | Yığın, kuyruk |
| H10 | v2.9 | Numara → kayıt karma tablosu; O(n) yinelenen tespiti; ad içinde alt dizgi arama | Karma tablosu, Rabin–Karp |
| H11 | v2.10 | Önkoşul grafı, geçerli ders planı, en erken dönem | Topolojik sıralama, BFS |
| H12 | v2.11 | Sınav oturumu ataması; en az salon sayısı | Açgözlü boyama, aralık bölümleme |
| H13 | v2.12 | Ders seçimi optimizasyonu; “Bunu mu demek istediniz?” | 0/1 sırt çantası, düzenleme uzaklığı |
| H14 | v3.0 | Bütünleşik sistem, test paketi, ölçüm raporu ve sunum (final projesi) | Sentez |

Bu klasördeki referans sürümler: **v2.0–v3.0** (aşağıda, § 7). Ara proje (v2.3–v2.6): [yönerge](ARA_PROJE_YONERGESI.md) ve [rapor şablonu](ARA_PROJE_RAPOR_SABLONU.md). Modül III (v2.7–v2.9: bağlı liste, yığın/kuyruk, karma) ile birlikte bellek denetimi zorunlu hâle gelir: her sürüm `make asan` ve `make valgrind` ile sızıntısız doğrulanır ve sürüm belgesinde bir **bellek sahipliği** tablosu bulunur. Modül IV–V (v2.10–v2.12: graflar, açgözlü algoritmalar, dinamik programlama) önceki modülleri kullanır: ders kodu → köşe eşlemesi v2.9'un karma tablosuyla, sınav salonlarının bitiş zamanları v2.6'nın öbeğiyle, ders seçimi v2.2'nin geri izlemesiyle karşılaştırılarak, ad önerisi v2.4/v2.9'un Türkçe katlamasıyla yapılır. **Final projesi (H14): Mini-OBS 2 v3.0** — bütün modüllerin menü güdümlü tek uygulamada (`mini_obs`: menü, betik ve alt komut kipleri) bütünleştirilmesi, test paketi (birim + kâhin + stres + regresyon), dönem kıyaslaması ölçüm raporu ve sunum. Final projesi belgeleri: [yönerge](FINAL_PROJE_YONERGESI.md) (varsayılan proje ve altı seçenekli havuz, ortak asgari gereksinimler, takvim, rubrik, sunum) ve [rapor şablonu](FINAL_RAPOR_SABLONU.md); başvuru örnekleri: [v3.0 belgesi](v3.0/mini_obs_v3_0.md), [ölçüm raporu](v3.0/mini_obs_v3_0_olcum_raporu.md), [sunum taslağı](v3.0/mini_obs_v3_0_sunum_taslagi.md).

**Sarmallar (Yol Haritası Tablo 4.2).** Bazı problemler dönem boyunca yeniden çözülür ve her yeni sürüm bir öncekiyle **aynı sonucu** vermek zorundadır; önceki sürüm sonrakinin kâhinidir:

- *Yinelenen kayıt tespiti*: v2.1 tüm çiftler, O(n²) → v2.5 sırala ve komşuları karşılaştır, O(n log n) → v2.9 karma tablosu, ortalama O(n). (v1.0 yükleyicisindeki karesel denetim de bu sarmalda iyileştirilir.)
- *Ders seçimi*: v2.2 geri izleme, O(2ⁿ) → H12 açgözlü (yanlış sonuç; karşı örnek) → v2.12 0/1 sırt çantası, O(n·W). v2.12 dördünü (ve dal-sınırı) aynı girdide çalıştırır: geri izlemenin düğüm sayısı v2.2'ninkiyle aynıdır, DP aynı kümeyi bulur, açgözlü örnek havuzda 20 puan geride kalır.
- *Arama*: v1.0 doğrusal arama → v2.3 ikili arama → v2.9 karma tablosu.

## 3. Genel kurallar

### 3.1 Dil ve derleme

- Proje yalnızca **C17** ile geliştirilir: `gcc -std=c17 -Wall -Wextra -pedantic -O2 -g`. **Sıfır uyarı** zorunludur; kodun öbür optimizasyon düzeylerinde (`-O0 … -O3`) de uyarısız derlendiğini denetlemeniz önerilir.
- Girdi `fgets` + `strtol`/`strtod` ile, dönüş değerleri denetlenerek okunur; `rand()` kullanılmaz. Algoritmanın kendisi kütüphaneye devredilmez; `qsort`, `bsearch` gibi çağrılar **yalnızca kâhin** olarak ya da açıkça izin verilen yerlerde kullanılır (Yol Haritası 6.5).
- Her sürüm **kendi başına derlenir**: `v2.X/` klasörü, önceki sürümün kopyası üzerine kurulur; başka bir sürümün dosyalarına bağlanmaz.

### 3.2 Modüler yapı ve adlandırma

- v1.0'ın dört modülü korunur; her yeni yetenek kendi modülünde (`.h` + `.c`) toplanır (ör. `uretec`, `deney`, `sayac`, `yinelenen`, `secmeli`). Bir modül yalnızca gereken başlıkları ekler; öğrenci kaydını bilmesi gerekmeyen bir modül `obs.h`'yi eklemez.
- Adlar Türkçe, ASCII, `snake_case`: `yinelenen_bul`, `ders_istatistigi_say`, `havuz_oku`. Sabitler büyük harf (`HAVUZ_AZAMI`); türler `PascalCase` (`SecimSonucu`).
- Her fonksiyonun bildiriminde (ya da başında) **ön koşul / son koşul** ve — analiz edilen fonksiyonlarda — **T(n) ya da karmaşıklık** yorumu bulunur (Cormen vd., 2022). Satırlar ≤ 80 sütun.
- Ortak modüller (`ortak_rastgele.h/.c`, `zamanlayici.h/.c`; 90_Ortak_Varliklar/kod_ortak) **kopyalanır, değiştirilmez**.

### 3.3 Makefile hedefleri (her sürümde zorunlu)

| Hedef | Ne yapar? |
|---|---|
| `make` | bütün programları derler |
| `make test` | birim testleri (`obs_test`) ve kâhin testlerini (`test_kahin`) derler ve çalıştırır; biri başarısızsa `make` hata verir |
| `make olcum` | sürümün ölçümlerini yapar; sonuçları `olcum/*.csv`'ye, makine bilgisini `olcum/OLCUM_ORTAMI.txt`'ye yazar (toplam süre ≈ 3 dakikayı aşmamalı) |
| `make asan` | `-fsanitize=address,undefined -fno-sanitize-recover=all` ile testleri ve örnek çalıştırmaları yapar; rapor olmamalı |
| `make valgrind` | **(v2.7'den itibaren zorunlu)** sanitizer'sız `-O0 -g` ikililerle testleri ve örnek çalıştırmaları `valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=3` altında yapar; her çalıştırmada "ERROR SUMMARY: 0 errors" ve "definitely lost: 0 bytes" aranır, biri yoksa hedef başarısız olur |
| `make temiz` | derleme ürünlerini ve geçici dosyaları siler |

İsteğe bağlı: `make ornek` (örnek oturum); v2.0–v2.6'da `make valgrind` de isteğe bağlıdır. v3.0'da (final projesi) `make kapsam` önerilir: gcov ile satır kapsamı (modül başına satır, çalışan satır, yüzde).

### 3.4 Çıktı, çıkış kodları ve tekrarlanabilirlik

- **stdout deterministiktir**: aynı girdi ve argümanlarla her çalıştırmada bayt bayt aynı. **Süreler yalnızca stderr'e** (ya da CSV'ye) yazılır.
- Çıkış kodları: **0** başarı; **1** dosya/girdi/bellek hatası (test programlarında: başarısız test; denetim araçlarında: bulunan sorun); **2** hatalı kullanım (eksik/geçersiz argüman).
- Rastgelelik yalnızca ortak LCG'den gelir (`rastgele_tohum`, `rastgele_aralik`, `rastgele_karistir`). Veri üreteci aynı tohumla aynı dosyayı üretir; ölçümler ve testler tohumlarıyla raporlanır.

### 3.5 Kâhinle test

- Her yeni algoritma, doğruluğu apaçık bir **kâhine** karşı rastgele girdilerle sınanır: kaba kuvvet (tüm çiftler, bit maskesi), sıralama tabanlı hesap ya da önceki sürümün fonksiyonu.
- Kâhin sınanan koddan **farklı bir yoldan** hesaplar; aynı fonksiyonu iki kez çağırmak kâhin değildir.
- Her deneme bir **tohumdan** türetilir. Uyuşmazlıkta program tohumu, girdi boyutunu, beklenen/bulunan değeri ve (mümkünse küçültülmüş) **karşı örneği** basar, 1 ile çıkar; `--tohum t --deneme 1` hatayı aynen yeniden üretir.
- Sınır durumları (n = 0, 1, 2; eşit değerler; en iyi/en kötü durum) denemelerin bir bölümüne bilinçli olarak yönlendirilir.
- Testin kendisi de sınanır: kasıtlı hatalı bir sürümü (`--hata-goster`) kâhinin yakaladığı gösterilir.

### 3.6 Ölçüm raporu ilkeleri

1. **Düzen**: `-O2`; her boyut için 1 ısınma + en az 5 tekrar; **ortanca**. Pahalı boyutlarda tekrar sayısı azaltılabilir, ama raporda belirtilir. Ölçülen işin sonucu kullanılır/yazdırılır (derleyici işi silemesin).
2. **Ortam**: işlemci modeli, çekirdek sayısı, önbellek boyutları, derleyici sürümü ve bayraklar, tarih (`OLCUM_ORTAMI.txt`).
3. **Ham veri**: CSV (başlık satırı; birim sütun adında: `ortanca_ms`); deterministik sayaçlar (karşılaştırma, düğüm…) süreden ayrı sütunlarda.
4. **Tablo ve grafik**: n'e karşı süre; eksen adı, birim ve ölçek türü (doğrusal/logaritmik) yazılı; karesel ve üstel büyüme için log–log ya da yarı logaritmik grafik.
5. **Kuramla karşılaştırma**: sayaçlar kapalı biçim formülle **birebir**; süreler oran testiyle (n'i katlayınca T(2n)/T(n)) ve log–log eğimle (Sedgewick & Wayne, 2011).
6. **Kestirim**: ölçülemeyen büyüklükler (ör. karesel algoritmada 10⁶) yöntemiyle birlikte **açıkça "kestirim" diye** verilir.
7. **Yorum ve sınırlılıklar**: "bu makinede ölçülen"; gürültü, tek tekrar, önbellek ve kod hizalaması gibi etkiler. İki algoritma **aynı programda, aynı derlemeyle** karşılaştırılır (v2.1, bölüm 7.4).

## 4. Teslim ve klasör düzeni

Öğrenci deposu (Git önerilir; her sürüm bir etiketle işaretlenir, ör. `git tag v2.2`):

```
mini_obs2/
├── README.md                 ← derleme, kullanım, sürüm notları (kısa)
├── v2.0/                     ← her sürüm kendi başına derlenir
│   ├── *.h  *.c  Makefile
│   ├── ornek_veri/  testler/ ← örnek veriler ve test girdileri
│   ├── olcum/                ← make olcum çıktıları (*.csv, OLCUM_ORTAMI.txt)
│   └── RAPOR.md              ← sürüm notu: ne eklendi, kabul ölçütleri, ölçüm tablosu ve yorum
├── v2.1/  v2.2/  …
└── v3.0/                     ← final
```

- Derleme ürünleri (`*.o`, programlar) ve büyük üretilmiş veriler (ör. 10⁶ kayıtlık CSV) depoya konmaz; veri, tohumuyla birlikte `veri_uret` komutu olarak belgelenir.
- Her sürümün `RAPOR.md`'si o haftanın ders notundaki "Mini-OBS 2 adımı" kabul ölçütlerini madde madde işaretler ve ölçüm tablosunu içerir.

## 5. Değerlendirme

- **Haftalık adımlar.** Her haftanın ders notunda (bölüm 10, "Mini-OBS 2 adımı") gereksinimler, ipuçları, **kabul ölçütleri** ve **test senaryoları** verilir. Haftalık adımlar ara ve final projesinin yapı taşlarıdır; teslim biçimi ve ağırlıkları dersin ölçme planında belirtilir.
- **Ara proje — H7 (teslim: H8 başı).** Mini-OBS 2 **v2.6** + sıralama ölçüm raporu: arama ve sıralamanın bütünleştirilmesi (v2.3–v2.6); v2.0–v2.6 boyunca kurulan ölçüm altyapısıyla bütün sıralama algoritmalarının karşılaştırmalı ölçümü (tablo, grafik, kuramla karşılaştırma). Kapsam, teslim edilecekler, kabul ölçütleri ve puanlama: [ARA_PROJE_YONERGESI.md](ARA_PROJE_YONERGESI.md); raporun bölümleri ve zorunlu tablo/grafikler: [ARA_PROJE_RAPOR_SABLONU.md](ARA_PROJE_RAPOR_SABLONU.md). Başvuru raporu: [v2.6 ölçüm raporu](v2.6/mini_obs_v2_6_olcum_raporu.md).
- **Final projesi — H14 (teslim ve sunum).** Varsayılan seçenek Mini-OBS 2 **v3.0**: bütün modüllerin menü güdümlü tek uygulamada bütünleştirilmesi, test paketi (birim + kâhin + stres), ölçüm raporu ve sunum. Dönem kıyaslama raporunda ilk (kaba kuvvet) ve son (algoritmik) sürümlerin süreleri karşılaştırılır; algoritmik sürümler 10⁶ kayıtta ölçülür, karesel ilk sürümler 10⁴–10⁵ kayıtta ölçülüp 10⁶ için kestirilir. Kapsam, seçenek havuzu, takvim, teslim edilecekler, kabul ölçütleri, rubrik ve sunum yönergesi: [FINAL_PROJE_YONERGESI.md](FINAL_PROJE_YONERGESI.md); raporun bölümleri ve zorunlu tablo/grafikler: [FINAL_RAPOR_SABLONU.md](FINAL_RAPOR_SABLONU.md). Başvuru raporu: [v3.0 ölçüm raporu](v3.0/mini_obs_v3_0_olcum_raporu.md); sunum için içerik planı: [v3.0 sunum taslağı](v3.0/mini_obs_v3_0_sunum_taslagi.md).

Final projesi rubriği (Yol Haritası Tablo 10.3, öneri):

| Ölçüt | Ağırlık | Açıklama |
|---|---|---|
| İşlevsel doğruluk | %25 | Tüm menü işlevleri beklenen çıktıyı üretir; sınır durumları doğru işlenir. |
| Algoritma seçimi ve analiz | %25 | Her işlev için seçilen algoritma ve veri yapısı gerekçelendirilir; kimlik kartları ve karmaşıklık analizi doğrudur. |
| Test ve doğrulama | %15 | Birim, kâhinle karşılaştırmalı ve stres testleri; testlerin otomatik çalıştırılması. |
| Ölçüm raporu | %15 | İlk ve son sürümlerin karşılaştırmalı ölçümü; grafikler; kuramla tutarlılık yorumu. |
| Kod kalitesi ve bellek güvenliği | %10 | Kod standardına uyum (Yol Haritası § 6.5), uyarısız derleme, sızıntısız çalışma (ASan/Valgrind). |
| Sunum | %10 | Canlı demo, tasarım kararlarının ve ölçüm bulgularının anlatımı. |

**Seçenek havuzu.** Öne çıkmak isteyen öğrenciler, ortak asgari gereksinimleri (en az bir arama, bir sıralama, bir dinamik veri yapısı, bir graf ya da DP algoritması; kâhin testleri; ölçüm raporu; C ile modüler gerçekleştirim) karşılamak koşuluyla Mini-OBS 2 yerine şu projelerden birini seçebilir: kampüs navigasyonu, mini arama motoru, sıralama laboratuvarı, bulmaca çözücü, Huffman tabanlı dosya sıkıştırıcı, ders/sınav çizelgeleyici (ayrıntılar Yol Haritası 10.3; her seçeneğin kapsamı, asgari gereksinimleri, kabul ölçütleri, önerilen verisi ve zorluk notu [yönergede](FINAL_PROJE_YONERGESI.md) § 2.2).

## 6. Haftalık iş akışı (öneri)

1. Önceki sürümü `v2.X/` olarak kopyalayın; `make temiz && make && make test` ile temiz başlayın.
2. Yeni modülün başlığını (`.h`) sözleşmeleriyle yazın; önce **kâhini** ve birim testlerini, sonra algoritmayı yazın.
3. `make test` ve `make asan` temiz olana kadar ilerleyin; v1.0'ın 99 doğrulaması her zaman geçmeli.
4. `make olcum`; CSV'den tablo ve grafik; kuramla karşılaştırın.
5. `RAPOR.md`: kabul ölçütleri ✓/✗, ölçüm tablosu, yorum, sınırlılıklar.

## 7. Bu klasördeki referans sürümler

| Sürüm | Hafta | Yeni modül / program | Birim doğrulama | Kâhin (300 deneme) | Öne çıkan ölçüm (bu makinede) |
|---|---|---|---|---|---|
| [v2.0](v2.0/mini_obs_v2_0.md) | H1 | `uretec`, `deney`; `veri_uret`, `olcer`, `test_kahin` | 110 | 12 000 denetim | v1.0 yükleyicisi Θ(n²): 10⁵ kayıt 17,1 s; 10⁶ ≈ 1,6 saat (kestirim) |
| [v2.1](v2.1/mini_obs_v2_1.md) | H2 | `sayac`, `yinelenen`; `denetle` | 134 | 57 242 denetim | tüm çiftler: katlama oranı 3,78–4,48 (n ≥ 4 000), log–log eğim 2,02 |
| [v2.2](v2.2/mini_obs_v2_2.md) | H3 | `secmeli`; `ders_sec` | 150 | 59 342 denetim | 30 derste üst budama ziyaret oranı %0,13 (2³⁰ düğüme göre), 715 kat hızlı |
| [v2.3](v2.3/mini_obs_v2_3.md) | H4 | `arama`; `ara` | 177 | 297 205 denetim | 10⁵ kayıtta ikili arama doğrusal aramadan 730 kat hızlı; sıralı ekleme yüklemeyi hızlandırmaz (aynı ölçüm oturumunda v1.0 19,05 s, v2.3 20,75 s: 2 495 087 143 kayıt kaydırma; artan sıralı dosyada 176,8 ms) |
| [v2.4](v2.4/mini_obs_v2_4.md) | H5 | `turkce`, `siralama`, `liste`; `listele` | 203 | 345 505 denetim | n = 4 000 listede araya ekleme: karışık 146,2 ms, neredeyse sıralı 974,1 µs (`qsort` 6,5 ms); Türkçe karşılaştırıcı bayt karşılaştırıcısından 8,9 kat yavaş (10⁵ kayıt) |
| [v2.5](v2.5/mini_obs_v2_5.md) | H6 | `bolfethet`, `sube`; `ortanca`, `birlestir` | 226 | 350 751 denetim | toplu yükleyici 10⁶ kaydı 2,28 s sürede yükler (v2.0 kestirimi ≈ 1,6 saat); yinelenen tespiti 10⁵ kayıtta 4,33 s → 23,1 ms (187 kat) |
| [v2.6](v2.6/mini_obs_v2_6.md) | H7 | `obek`, `dogrusal`; `dagilim`, `ilk_k` | 245 | 354 990 denetim | 10⁶ numara: taban 79,3 ms, birleştirmeli 273,1 ms, `qsort` 257,7 ms, öbek 599,1 ms; 10⁵ kayıtta ilk-10 6,3 ms (bütün liste 383,0 ms); [ölçüm raporu](v2.6/mini_obs_v2_6_olcum_raporu.md) |
| [v2.7](v2.7/mini_obs_v2_7.md) | H8 | `dinamik`, `bekleme`, `kontenjan`, `kayit_listesi`; `kayit`, `olcer_yapi` | 324 | 446 295 denetim | FIFO 10⁵ işlem: kaydırmalı dizi 761,0 ms, bağlı liste 3,1 ms (247 kat); numarayla silmede (n = 32 000) dizi bitişik listeden 4,5, dağınık listeden 15,4 kat hızlı; Valgrind 25 çalıştırma temiz |
| [v2.8](v2.8/mini_obs_v2_8.md) | H9 | `kuyruk`, `geri_al`; `kayit_gunu` | 353 | 502 819 denetim | geri al 10⁵ işlemde 0,81 µs/işlem, geçmiş belleği ≈ 287 bayt/işlem (sınır 100: 31 520 bayt); kayıt günü (geliş 2 s): 2 gişe 1 601/5 000 istek reddi, 4 gişe 0; Valgrind 35 çalıştırma temiz |
| [v2.9](v2.9/mini_obs_v2_9.md) | H10 | `karma`, `desen`; `olcer_karma` | 389 | 670 897 denetim | 10⁶ kayıtta numarayla arama: ikili 762 ns, karma 186 ns; yinelenen tespiti 10⁵ kayıtta tüm çiftler 1,89 s → sıralama 22,9 ms → karma kümesi 8,1 ms; Rabin–Karp 10⁵ kayıt 16,4 ms (naif 3,3 ms); Valgrind 48 çalıştırma temiz |
| [v2.10](v2.10/mini_obs_v2_10.md) | H11 | `graf`, `onkosul`; `ders_plani`, `olcer_graf`, `graf_uret` | 414 | 675 383 denetim | 10⁶ dersli rastgele DAG'da (E = 4·10⁶) bütün plan (DFS + Kahn + katman + BFS) 1,03 s, okunan kenar tam 5E; matrisle Kahn 16 000 köşede listeyle Kahn'dan 249 kat yavaş; örnek katalogda 48 dersten 15 tanesinde BFS katmanı en erken dönemden küçük; Valgrind 62 çalıştırma temiz |
| [v2.11](v2.11/mini_obs_v2_11.md) | H12 | `sinav`; `sinav_programi`, `olcer_sinav` | 426 | 678 664 denetim | Welsh–Powell 10⁶ derste 164,9 ms (okunan komşu tam 2E); taç grafında açgözlü 4, en iyi 2 oturum; n = 10 derslik rastgele graflarda Welsh–Powell'in en iyi olduğu grafların oranı %88,0–%99,7 (rastgele sıra %60,5–%87,7); aralık bölümleme 10⁶ sınavda 414,2 ms, her n'de salon = derinlik; Valgrind 73 çalıştırma temiz |
| [v2.12](v2.12/mini_obs_v2_12.md) | H13 | `secim`, `oneri`; `ders_secimi`, `olcer_dp` | 439 | 686 464 denetim | W = 45, n = 35 derste v2.2 geri izlemesi 143 107 092 düğümle 651,9 ms, DP 1 656 hücreyle 1,6 µs; n = 60'ta geri izleme ≈ 7 dakika (kestirim; düğüm sayısı sayım DP'siyle kesin); örnek havuzda açgözlü 295 ↔ en iyi 315; 10⁵ kayıtta öneri sorgusu sözlükle 272,1 µs, sözlüksüz 38,1 ms; Valgrind 87 çalıştırma temiz |
| [v3.0](v3.0/mini_obs_v3_0.md) | H14 | `hata`, `ayar`, `bilesen`, `donem`, `defter`, `uygulama`, `komut`; bütünleşik `mini_obs` (menü, betik, alt komut), `test_stres`, `olcer_donem` | 490 | 728 163 denetim | dönem kıyaslaması (10⁶): yinelenen tespiti ≈ 5,6 dk (kestirim) → 172,0 ms, toplu ders kaydı ≈ 3,4 dk (kestirim) → 105,2 ms, öneri sorgusu 3,66 s → 446,2 µs; stres testi 20 000 işlem gölge modelle; satır kapsamı %90,0; Valgrind 104 çalıştırma temiz; [ölçüm raporu](v3.0/mini_obs_v3_0_olcum_raporu.md) |

**v3.0 (final projesi).** v2.12'nin arayüzlerini devralır (`graf`/`onkosul`, `sinav`, `secim`, `oneri`, `karma` ve ölçüm/kâhin altyapısı) ve sürüm belgelerinin "Bilinen sınırlılıklar"ındaki açık konuların beşini çözer: ders kayıtları Mini-OBS kaydıyla birleştirildi (kayıt defteri), önkoşul döngülerinin hepsi güçlü bağlı bileşenlerle raporlanıyor, AKTS sınırlı dönem planı (sezgisel + alt sınır + küçük örnekte kesin), sınav programında gün sınırı ve salon kapasitesi, dizinlerle öneri sözlüğünün saklanması; önkoşul kısıtlı ders seçimi ve artımlı önbellek güncellemesi final projesi genişletme seçenekleri olarak bırakıldı ([v3.0 belgesi](v3.0/mini_obs_v3_0.md) § 3.2). Bellek sahipliği v1.0–v3.0 için tek tabloda toplandı (§ 6).

Her sürüm klasöründe: kaynak kodlar, `Makefile`, `testler/`, `ornek_veri/`, `olcum/` (CSV ve ortam), sürüm belgesi `mini_obs_v2_X.md` (amaç, değişiklikler, mimari, kullanım, tasarım kararları, v2.7'den itibaren bellek sahipliği, ölçümler, **ders notu için özet**, sınırlılıklar), `mini_obs_v2_X_ciktilar.txt` (derleme, test, oturum, ölçüm, ASan ve — v2.7'den itibaren — Valgrind çıktıları; hepsi gerçek çalıştırma) ve diyagram/grafikler (`mini_obs_v2_X_*.png`); v2.6'da ayrıca ara projenin başvuru raporu `mini_obs_v2_6_olcum_raporu.md` (dokuz sıralama yöntemi × dört girdi türü; PDF'e dönüştürülebilir); v3.0'da final projesinin başvuru raporu `mini_obs_v3_0_olcum_raporu.md` (dönem kıyaslaması), sunum taslağı `mini_obs_v3_0_sunum_taslagi.md` ve gcov kapsam hedefi (`make kapsam`). Ölçümler 2 çekirdekli bir sanal makinede (Intel Xeon @ 2,80 GHz, gcc 13.3.0) yapılmıştır; öğrencilerden aynı ölçümleri kendi makinelerinde tekrarlamaları beklenir — sayılar değişir, büyüme sınıfları değişmez.

## 8. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
