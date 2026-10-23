# AP-2 Final Projesi Yönergesi — Mini-OBS 2 v3.0 ya da seçenek havuzundan bir proje (Hafta 14)

**Ders:** Algoritma ve Programlama – II (C17) · RTEÜ Bilgisayar Mühendisliği, 1. sınıf, bahar yarıyılı · Dr. Öğr. Üyesi Mehmet Sevri

**Kapsam:** H1–H14 (dönemin bütün algoritmik modülleri) · **Veriliş:** H11 · **Konu seçimi:** H11 sonu · **Ara kontrol:** H12 sonu · **Teslim ve sunum:** H14 · **Çalışma biçimi:** bireysel · Kesin tarih, saat, teslim ortamı ve sunum sırası kurumun akademik takvimine göre belirlenir; derste ve ders sayfasında duyurulur.

Final projesi dönemin sentezidir. Dönem boyunca her hafta bir algoritmayla büyüttüğünüz programı (ya da seçenek havuzundan seçtiğiniz bir projeyi) **tek bir uygulamada** bütünleştirecek, **otomatik bir test paketiyle** doğrulayacak, ilk ve son gerçekleştirimleri aynı düzenekte **ölçüp** bir rapor yazacak ve H14'te **canlı demoyla sunacaksınız**. Projenin ölçme planındaki yeri Yol Haritası Tablo 10.1'dedir (Final projesi: H14, teslim ve sunum); ağırlığı dersin ölçme planında ve kurumun ölçme ve değerlendirme yönetmeliğinde belirtilir. Raporun bölümleri ve zorunlu tablo/grafikleri [rapor şablonunda](FINAL_RAPOR_SABLONU.md), başvuru örnekleri [v3.0 sürüm belgesinde](v3.0/mini_obs_v3_0.md) ve [v3.0 ölçüm raporunda](v3.0/mini_obs_v3_0_olcum_raporu.md), sunum için bir içerik planı [v3.0 sunum taslağında](v3.0/mini_obs_v3_0_sunum_taslagi.md) verilmiştir.

## 1. Amaç ve öğrenme çıktıları

Final projesinin temel öğrenme çıktısı **ÖÇ 14.5**'tir: *Dönem boyunca geliştirilen algoritmik modülleri bütünleştiren final projesini tasarlar, test eder, belgeler ve sunar.* Proje, H14'ün diğer öğrenme çıktılarını ve dönemin modüllerini de birlikte ölçer:

| Öğrenme çıktısı (Yol Haritası 5.14) | Projede karşılığı | Rubrik ölçütü (§ 8) |
|---|---|---|
| ÖÇ 14.1 — problemi uygun stratejiyle eşleştirir ve seçimini gerekçelendirir | her işlev için algoritma ve veri yapısı seçimi; kimlik kartları; ölçümle gerekçe | Algoritma seçimi ve analiz |
| ÖÇ 14.2 — problemleri bilinen problemlere indirger | ders planı → topolojik sıralama, sınav programı → graf boyama, ders seçimi → 0/1 sırt çantası (havuz projelerinde: kendi indirgemeleriniz) | Algoritma seçimi ve analiz |
| ÖÇ 14.3 — NP-zor problemlerde sezgisel ve yaklaşık yöntemlerin rolünü tartışır | sezgisel + alt sınır + küçük örnekte kesin çözüm; "sezgisel en iyidir" denmez | Algoritma seçimi ve analiz · Ölçüm raporu |
| ÖÇ 14.4 — performansı ölçer, darboğazı bulur, iyileştirmeyi deneysel olarak belgeler | dönem kıyaslaması (ilk ↔ son gerçekleştirim), stres testi, profil | Ölçüm raporu · Test ve doğrulama |
| **ÖÇ 14.5** — modülleri bütünleştiren projeyi tasarlar, test eder, belgeler ve sunar | tek uygulama, test paketi, rapor, sunum | bütün ölçütler |

Proje ayrıca dönem boyunca kurduğunuz mühendislik alışkanlıklarını değerlendirir: kâhinle test, deterministik çıktı, bellek güvenliği (ASan/Valgrind), tekrarlanabilir ölçüm ve dürüst raporlama.

## 2. Proje seçenekleri

### 2.1 Varsayılan proje: Mini-OBS 2 v3.0

Mini-OBS 2'nin v2.0–v2.12 modüllerini menü güdümlü **tek bir uygulamada** (`mini_obs`) bütünleştirirsiniz. Ayrıntılı gereksinimler, ipuçları, kabul ölçütleri ve test senaryoları v3.0 belgesinin "Ders notu için özet" bölümündedir ([v3.0 belgesi § 11](v3.0/mini_obs_v3_0.md)). Asgari kapsam:

| Alan | Gereksinim |
|---|---|
| Giriş kipleri | (1) v1.0 menüsü (v1.0 oturumları **aynen** çalışır) + menüden komut kipine geçiş; (2) betik kipi: `./mini_obs VERİ --betik DOSYA` ya da `--betik -` (stdin); (3) alt komut kipi: `./mini_obs VERİ KOMUT [ARGÜMAN …]` |
| Modüller | arama (ikili, karma; soyad öneki; ad içinde Rabin–Karp) · sıralama (çok ölçütlü, Türkçe, büyük veri) · karma · bekleme listesi ve kayıt kuyruğu · geri al/yinele · önkoşul grafı, ders planı ve **AKTS sınırlı dönem planı** · sınav programı (**gün sınırı, salon kapasitesi, öğrenci başına günde en çok bir sınav**) · ders seçimi optimizasyonu · "Bunu mu demek istediniz?" önerisi · istatistik ve not dağılımı |
| Bütünleştirme | ders kayıtları Mini-OBS kaydındaki öğrencilerle birleştirilir (yabancı numaralı kayıt dosyası reddedilir); önkoşul döngülerinin **hepsi** raporlanır (güçlü bağlı bileşenler); dizinler ve öneri sözlüğü **saklanır**, kayıt dizisi değişince geçersiz sayılır |
| Yapı | modül sınırları (`.h` sözleşmesi + `.c`); tek tip hata bildirimi (dönüş kodları → çıkış kodu 0/1/2); yapılandırma dosyası; bellek sahipliği tablosu **tek bir belgede** |
| Test paketi | `make test`: birim + kâhin + **stres** (rastgele işlem dizisi gölge modelle; 10⁵–10⁶ kayıt; sınır durumları) + regresyon (v1.0'ın 99 doğrulaması ve önceki sürümlerin çıktıları) |
| Kalite | `make asan`, `make valgrind` temiz; gcov ile satır kapsamı (`make kapsam` önerilir) |
| Ölçüm raporu | **dönem kıyaslaması**: her işlemin ilk (v2.0–v2.2 kaba kuvvet ya da işlemin ilk naif sürümü) ve son (algoritmik) gerçekleştirimi; algoritmik sürümler 10⁶ kayıtta, karesel sürümler 10⁴–10⁵'te ölçülüp 10⁶ için işaretli kestirimle |

**Ne verilir, ne yazılır?**

- **Verilir:** v2.0–v2.12 referans sürümleri ve belgeleri; v3.0'ın yeni başlık dosyalarının sözleşmeleri (v3.0 belgesi § 4–5'te: `hata.h`, `ayar.h`, `bilesen.h`, `donem.h`, `defter.h`, `uygulama.h`, `komut.h`); `mini_obs.ayar`, `ornek_veri/` ve `testler/` girdileri (betikler, iki döngülü katalog, yabancı numaralı kayıt dosyası, v1.0 oturumlarının altın çıktıları); ortak modüller; bu yönerge ve rapor şablonu.
- **Siz yazarsınız:** v3.0 modüllerinin `.c` dosyaları, `main.c`, komut katmanı, testler (birim, kâhin, stres, regresyon betiği), ölçüm aracı ve `make olcum`, ölçüm raporu ve onu CSV'den üreten betik, README, sunum.
- **Değiştirilmez:** v1.0 veri modeli, dosya biçimleri ve not kuralları; ortak modüller (`ortak_rastgele`, `zamanlayici`).
- **Referans sürümden alınan dosyalar:** v2.x'te tamamlayamadığınız bir modül için referans sürümün dosyasını kullanabilirsiniz; dosyayı raporun beyan ekinde **adıyla** belirtin. Bu dosyanın işlevleri İşlevsel doğruluk ölçütünde puan almaz; diğer ölçütler (bütünleştirme, test, ölçüm, sunum) bundan etkilenmez. v3.0 referans çözümünün kaynak kodunun teslimden önce paylaşılıp paylaşılmayacağına öğretim üyesi karar verir; paylaşılırsa aynı kural geçerlidir.

### 2.2 Seçenek havuzu

Öne çıkmak isteyen öğrenciler, **ortak asgari gereksinimleri** (§ 2.3) karşılamak koşuluyla Mini-OBS 2 yerine aşağıdaki altı projeden birini seçebilir (Yol Haritası 10.3). Havuzdan seçenler konu seçiminde (§ 3) bir sayfalık **proje önerisi** verir: kapsam, veri, algoritmalar, ortak asgari gereksinimlerin karşılığı (§ 2.3 tablosu doldurulmuş olarak) ve dönem kıyaslamasının "ilk ↔ son" çiftleri. Öneri öğretim üyesinin onayıyla kesinleşir. Havuz projelerinde de bütün teknik kurallar (§ 4), teslim edilecekler (§ 6) ve rubrik (§ 8) aynıdır; "dönem kıyaslaması" yerine **taban çizgisi ↔ algoritmik gerçekleştirim** kıyaslaması yapılır.

#### (1) Kampüs navigasyonu

| | |
|---|---|
| **Kapsam** | Bina–yol grafında (yönsüz, ağırlıklı) en az durakla yol (BFS), en kısa yol (Dijkstra) ve bütün binaları en düşük toplam uzunlukla bağlayan ağ (en küçük kapsayan ağaç: Kruskal + birleşim–bul ya da Prim); harita dosyadan okunur; bina adıyla arama |
| **Asgari gereksinimler** | rehber biçiminde graf dosyası (`V E yonsuz`, `u v w`) + bina adları; komutlar: `yol A B`, `durak A B`, `ag`, `ara ÖNEK`; Dijkstra ikili öbekle (tembel silme yeterli) ve dizi tabanlı taban çizgisiyle (Θ(V²)); bağlantısız graf, negatif ağırlık (reddedilir) ve aynı bina sorguları; yol, uzaklıkla birlikte yazdırılır |
| **Kabul ölçütleri** | rastgele graflarda Dijkstra uzaklıkları Floyd–Warshall (küçük V) ya da Bellman–Ford kâhiniyle birebir; Kruskal ve Prim aynı toplam ağırlığı verir, küçük V'de kaba kuvvetle doğrulanır; eşitlik kuralı belgelenir (öbekte (uzaklık, köşe) çifti); 10⁵–10⁶ köşelik üretilmiş graflarda dizi ↔ öbek ölçümü (dizi yalnız 10⁴'e kadar, sonrası kestirim) |
| **Önerilen veri** | 30–60 binalık KURGUSAL kampüs haritası (elle); ortak LCG ile üretilen ızgara ve rastgele geometrik graflar (10³–10⁶ köşe). Açık lisanslı gerçek harita verisi kullanılırsa kaynağı ve lisansı rapora yazılır |
| **Zorluk notu** | orta. Zorluk Dijkstra'nın öbekle doğru ve belirleyici gerçekleştiriminde ve büyük graf üretiminde; dizi ↔ öbek kesişim noktası (yoğun graflarda dizi kazanır) güzel bir ölçüm bulgusudur |

#### (2) Mini arama motoru

| | |
|---|---|
| **Kapsam** | Metin derleminde (satır ya da paragraf = belge) ters dizin (terim → belge listesi; karma tablosu), VE/VEYA sorguları, sıralı sonuçlar (terim sıklığına dayalı puan, ilk-k öbekle) ve düzenleme uzaklığıyla öneri ("Bunu mu demek istediniz?") |
| **Asgari gereksinimler** | bayt düzeyinde UTF-8 ve Türkçe büyük/küçük harf katlaması (İ/ı); kendi karma tablonuz (32 bit, belirleyici); sonuç listelerinin kesişimi sıralı birleştirmeyle; ilk-k için öbek; öneri için terim sözlüğü ve uzunluk farkı budaması; komutlar: `ara TERİM…`, `veya TERİM…`, `ilk K TERİM…`, `oneri SÖZCÜK` |
| **Kabul ölçütleri** | rastgele sorgularda sonuç kümeleri doğrusal tarama kâhiniyle birebir; ilk-k bütün listenin sıralanmasıyla aynı (eşitlikte belge numarası); öneriler kaba kuvvet uzaklıkla aynı; ölçüm: doğrusal tarama ↔ ters dizin, sorgu başına süre 10³–10⁶ belgede; dizin kurma süresi ve belleği |
| **Önerilen veri** | H10'un kamu malı Ömer Seyfettin metinleri (`KAYNAK_NOTU` ile); ortak LCG ile üretilen Zipf dağılımlı yapay derlem (10⁶ belgeye kadar) |
| **Zorluk notu** | orta. Türkçe katlama ve UTF-8 ayrıntıları ile sonuç sıralamasındaki eşitlik kuralı en sık hata kaynağıdır |

#### (3) Sıralama laboratuvarı

| | |
|---|---|
| **Kapsam** | Algoritmaları aynı düzenekte karşılaştıran terminal aracı: girdi türleri, sayaçlar, kararlılık denetimi, CSV çıktısı ve rapor; ara projenin genişletilmiş ve **uyarlanabilir** hâli |
| **Asgari gereksinimler** | en az sekiz yöntem (araya ekleme, birleştirmeli, doğal birleştirmeli (koşu birleştirme), hızlı (iki pivot kuralı), öbek, sayma, taban, `qsort` başvuru olarak); beş girdi türü (karışık, sıralı, ters, çok tekrarlı, neredeyse sıralı); **DP:** en uzun artan alt dizi (Θ(n log n)) ile "sıralılık ölçüsü"; **graf:** permütasyonun döngü ayrışımıyla en az takas sayısı; ikili arama (ikili araya ekleme ya da sonuç doğrulama) |
| **Kabul ölçütleri** | her yöntem `qsort` + kimlik kâhiniyle; kararlılık çok tekrarlı girdide kontrol sağlamasıyla; LIS kaba kuvvetle (n ≤ 15), takas sayısı BFS ile (n ≤ 8); sayaçlar kapalı biçimlerle; uyarlanabilir yöntemlerin "neredeyse sıralı" girdide kazancının LIS uzunluğuyla ilişkisi raporlanır |
| **Önerilen veri** | ortak LCG; Mini-OBS kayıtları (10⁶) ve tamsayı anahtarlar |
| **Zorluk notu** | düşük–orta. Kodlama riski düşüktür; öne çıkmak için ölçümün **derinliği** (oran testleri, eğimler, önbellek etkisi, kesişim noktaları) ve uyarlanabilirlik analizi beklenir |

#### (4) Bulmaca çözücü

| | |
|---|---|
| **Kapsam** | Sudoku, labirent ve kakuro (en az ikisi) için geri izleme, BFS ve budama stratejilerinin karşılaştırması |
| **Asgari gereksinimler** | Sudoku: geri izleme + en kısıtlı hücre önce (MRV) + bit maskeleri; labirent: BFS en kısa yol, DFS ile labirent üretimi; kakuro (seçilirse): toplam kısıtları ve olası rakam kümelerinin ön hesabı (DP ya da tablo); ziyaret edilmiş durumlar için karma tablosu (ör. 8-bulmaca BFS); düğüm sayaçları |
| **Kabul ölçütleri** | her çözüm bağımsız bir doğrulayıcıdan geçer (O(n²)); küçük örneklerde kaba kuvvetle aynı çözüm sayısı; BFS yol uzunluğu kâhinle (ör. ikinci bir BFS ya da kaba kuvvet); ölçüm: budamasız ↔ budamalı düğüm sayısı ve süre, zorluk düzeyine göre |
| **Önerilen veri** | ortak LCG ile üretilmiş labirentler ve bulmacalar (çözülebilirliği programla doğrulanmış); kamu malı ya da kendi ürettiğiniz Sudoku örnekleri |
| **Zorluk notu** | orta–yüksek. Arama uzayı üsteldir: süre bütçesi, kestirim ve "en zor girdi" seçimi raporda dikkat ister |

#### (5) Huffman tabanlı dosya sıkıştırıcı

| | |
|---|---|
| **Kapsam** | Bayt sıklıkları, öbekle Huffman ağacı, kanonik kodlar, bit düzeyinde yazıcı/okuyucu ve sürümlü ikili dosya biçimi; sıkıştırma ve açma |
| **Asgari gereksinimler** | belirleyici eşitlik kuralı (sıklık, ikincil anahtar); kanonik kodlar için (uzunluk, simge) sıralaması; kod çözmede ikili arama ya da tablo; **graf:** ağaçta DFS ile kod uzunlukları; dosya başlığı (sihirli sayı, sürüm, özgün uzunluk, kod uzunlukları); boş dosya, tek simgeli dosya ve 256 simgeli dosya; bozuk dosyada açık hata iletisi (çıkış 1) |
| **Kabul ölçütleri** | sıkıştır → aç → `cmp` özdeş (rastgele ve gerçek dosyalarda); ortalama kod uzunluğu Shannon entropisiyle karşılaştırılır (H ≤ L < H + 1); öbek ↔ her adımda doğrusal en küçük arama taban çizgisi; 10³–10⁸ bayt ölçüm (süreç belleği ≈ 1,5 GB altında) |
| **Önerilen veri** | kamu malı metinler, kendi kaynak kodunuz, ortak LCG ile üretilmiş farklı entropili dosyalar (düzgün, tek simgeli, Zipf) |
| **Zorluk notu** | orta. Bit işlemleri, ikili dosya biçimi ve sınır durumları (son baytın doldurulması) en sık hata kaynağıdır. Öne çıkmak için uzunluk sınırlı kodlar ya da bir sözlük tabanlı ön aşama (karma tablosuyla yineleme bulma) |

#### (6) Ders/sınav çizelgeleyici

| | |
|---|---|
| **Kapsam** | Çakışma grafında sınav günlerinin atanması (graf boyama sezgiselleri), salon ataması (aralık bölümleme) ve kısıtlar; sezgisellerin kaba kuvvetle (küçük n) karşılaştırılması |
| **Asgari gereksinimler** | en az iki sezgisel (Welsh–Powell ve DSatur ya da rastgele sıralı açgözlü); alt sınır (klik); küçük n'de kesin kromatik sayı; kısıtlar: gün sınırı, salon kapasitesi, öğrenci başına günde en çok bir (ya da iki) sınav; yerel arama ile gün sayısını ya da ardışık sınav cezasını azaltma; kayıt verisinin üretimi (KURGUSAL) |
| **Kabul ölçütleri** | her program bağımsız doğrulayıcıdan geçer (çakışan iki sınav aynı günde değil; salonda çakışma yok; kapasite aşılmaz); kesin çözümle karşılaştırmada sezgisellerin en iyi olduğu örneklerin oranı raporlanır; 10⁵–10⁶ sınavlı üretilmiş verilerde ölçüm |
| **Önerilen veri** | ortak LCG ile üretilmiş kayıtlar (Mini-OBS v2.11 biçimi kullanılabilir); KURGUSAL ders kataloğu |
| **Zorluk notu** | orta. Mini-OBS v2.11/v3.0'ın sınav modülünü yeniden adlandırmak yeterli değildir: yeni sezgisel, yerel arama ve kısıt doğrulayıcısı beklenir. Problem NP-zordur: "sezgisel en iyidir" denmez, alt sınır ve kesin çözümle kıyaslanır |

### 2.3 Ortak asgari gereksinimler

Hangi proje seçilirse seçilsin aşağıdakilerin hepsi bulunur; havuz projelerinde öneri formunda bu tablo doldurulur:

| Gereksinim | Varsayılan projedeki karşılığı (örnek) | Kanıt |
|---|---|---|
| en az bir **arama** algoritması | ikili arama, karma tablosu, Rabin–Karp | kimlik kartı + kâhin |
| en az bir **sıralama** algoritması | birleştirmeli, sayma, öbek (ilk-k) | kimlik kartı + kâhin + kararlılık denetimi |
| en az bir **dinamik veri yapısı** | dinamik dizi, bağlı liste (bekleme), dairesel kuyruk, iki yığın (geri al), karma tablosu | bellek sahipliği tablosu + ASan/Valgrind |
| en az bir **graf ya da DP** algoritması | Kahn, güçlü bağlı bileşenler, Welsh–Powell, 0/1 sırt çantası, Levenshtein | kimlik kartı + kâhin |
| **kâhin testleri** | her algoritma sınanan koddan farklı bir yoldan hesaplayan kâhine karşı, tohumlu rastgele girdilerle | `make test` |
| **ölçüm raporu** | ilk ↔ son gerçekleştirim, tablo, grafik, kuramla karşılaştırma | [rapor şablonu](FINAL_RAPOR_SABLONU.md) |
| **C ile modüler gerçekleştirim** | C17, `.h` sözleşmesi + `.c`, Makefile | `make temiz && make` |

## 3. Takvim

| Zaman (öneri) | Adım | Çıktı |
|---|---|---|
| H11 | yönerge ve şablon verilir; seçenek havuzu tanıtılır | — |
| H11 sonu | **konu seçimi**: varsayılan proje ya da havuzdan bir seçenek | havuz için bir sayfalık öneri (§ 2.2); öğretim üyesi onayı |
| H12 sonu | **ara kontrol** (atölyede ≈ 10 dakika) | çalışan iskelet: `make`, `make test` (en az iki modül kâhinle), mimari diyagram taslağı, ölçüm planı (hangi çiftler, hangi n) |
| H13 | bütünleştirme ve stres testi; kod dondurma önerisi: H13 sonu | `make test`, `make asan`, `make valgrind` temiz |
| H13 sonu – H14 başı | `make olcum` (tek oturumda), rapor, sunum | CSV, rapor, slaytlar |
| **H14** | **teslim** (ilk dersin başı) ve **sunumlar** (H14 atölyeleri; Yol Haritası 5.14) | § 6'daki dosyalar |

Kesin tarih ve saatler, teslim ortamı ve sunum sırası kurumun akademik takvimine göre belirlenir ve ders sayfasında duyurulur. Geç teslim ve mazeret durumları ders izlencesindeki ve kurumun ölçme–değerlendirme yönetmeliğindeki kurallara göre değerlendirilir (Recep Tayyip Erdoğan Üniversitesi, 2025).

## 4. Teknik kurallar

### 4.1 Dil ve derleme

- Yalnızca **C17**: `gcc -std=c17 -Wall -Wextra -pedantic -O2 -g`; **sıfır uyarı**. `-O0 … -Os` düzeylerinde de uyarısız derlemeniz önerilir.
- Yalnızca standart kütüphane. Algoritmanın kendisi kütüphaneye devredilmez: `qsort`/`bsearch` yalnızca kâhin olarak ya da açıkça karşılaştırma için kullanılır.
- `rand()` kullanılmaz; rastgelelik ortak LCG'den (`ortak_rastgele`) gelir ve tohumla raporlanır.

### 4.2 Modüler yapı ve kod alışkanlıkları

- Her yetenek kendi modülündedir (`.h` sözleşmesi + `.c`); bir modül yalnızca gereken başlıkları ekler; döngüsel bağımlılık yoktur. Durum (veri, önbellekler, geçmiş) tek bir yapıda tutulur ve **tek temizlik yolu** vardır.
- Adlar Türkçe, ASCII, `snake_case`; satırlar ≤ 80 sütun. Her fonksiyonda ön/son koşul; döngülerde değişmez; analiz edilen fonksiyonlarda karmaşıklık yorumu (Yol Haritası 6.5).
- Bellek: her `malloc`/`realloc` dönüşü denetlenir (`realloc` önce geçici işaretçiye); ayıran her fonksiyonun yorumunda sahiplik sözleşmesi; programlar çıkmadan bütün belleği bırakır.
- **Tek tip hata bildirimi:** işlemler bir durum kodu döndürür (ör. `ObsDurum`: TAMAM, YOK, RED, DOSYA, BİÇİM, BELLEK, DOĞRULAMA, KULLANIM); ileti tek yerde biçimlenir; durum kodu çıkış koduna tek bir fonksiyonla çevrilir.
- **Yapılandırma:** değiştirilebilir parametreler (dosya yolları, kontenjan, sınırlar, tohumlar) tek bir yapıda; bir yapılandırma dosyasından okunur ve her değer atanırken denetlenir.

### 4.3 Makefile hedefleri

| Hedef | Ne yapar? |
|---|---|
| `make` | bütün programları derler |
| `make test` | birim, kâhin, stres ve regresyon testlerini derler ve çalıştırır; biri başarısızsa hata verir (kendi makinenizde ≈ 2 dakikayı aşmamalı) |
| `make olcum` | raporun bütün ölçümlerini yapar: `olcum/*.csv` ve `olcum/OLCUM_ORTAMI.txt` (≈ 6 dakikayı aşmamalı) |
| `make asan` | `-fsanitize=address,undefined -fno-sanitize-recover=all` ile testler ve örnek çalıştırmalar; rapor çıkmamalı |
| `make valgrind` | sanitizer'sız `-O0 -g` ikililerle testler ve örnek çalıştırmalar Valgrind altında: her çalıştırmada "ERROR SUMMARY: 0 errors" ve "definitely lost: 0 bytes" |
| `make kapsam` | (önerilir) gcov ile satır kapsamı: modül başına satır, çalışan satır, yüzde |
| `make temiz` | derleme ürünlerini ve geçici dosyaları siler |

AddressSanitizer ve Valgrind MinGW'de desteklenmez; `make asan` ve `make valgrind` için WSL ya da Linux kullanın.

### 4.4 Çıktı sözleşmesi (otomatik değerlendirme buna dayanır)

- **stdout deterministiktir:** aynı girdi ve argümanlarla bayt bayt aynı. **Süreler yalnızca stderr'e** ya da CSV'ye yazılır; adres (`%p`) yazdırılmaz.
- **Çıkış kodları:** 0 başarı; 1 dosya/bellek hatası, aranan kaydın yokluğu, iş kuralı reddi (ör. döngülü önkoşul grafı, karşılanamayan gün sınırı), başarısız test; 2 hatalı kullanım (bilinmeyen komut, eksik/geçersiz argüman).
- **Betik kipinde** her komut `> ` ile başlayan bir satırla yankılanır, ardından komutun çıktısı gelir; betik hatalı bir komutta durmaz; çıkış kodu oturumdaki en ağır hatadır (2 > 1 > 0).
- **Program, komut ve seçenek adları** (varsayılan proje) v3.0 belgesinin kullanım bölümündeki gibidir; havuz projelerinde README'de tanımlanır.
- **Çıktı biçimi serbesttir;** ancak denetlenen değerler — öğrenci numaraları, ders kodları, sayaçlar, ortanca ve ortalamalar, gün ve salon sayıları — çıktıda **ondalık noktayla ve binlik ayırıcısız** yazılır (ör. `77.5`, `4932`). Rapor ise Türkçe sayı biçimini kullanır (77,5; 4 932).

### 4.5 Test

- **Birim testleri:** her yeni algoritmanın elle izlenmiş en az bir testi (sonuç ve sayaçlar); v1.0'ın 99 doğrulaması ve önceki sürümlerin birim testleri her zaman geçer.
- **Kâhin testleri:** her algoritma sınanan koddan farklı bir yoldan hesaplayan kâhine karşı tohumlu rastgele girdilerle; uyuşmazlıkta tohum, n, beklenen/bulunan ve küçük bir karşı örnek basılır; `--tohum t --deneme 1` hatayı yeniden üretir. Varsayılan projede en az üç **kasıtlı hata** gösterimi: `--hata-goster kosaraju` (ikinci DFS ters grafta değil), `--hata-goster ayni_donem` (önkoşulu aynı dönemde planlayan sezgisel), `--hata-goster onbellek` (kayıt eklenince dizin geçersiz sayılmıyor); havuz projelerinde kendi seçtiğiniz üç hata.
- **Stres testleri:** (a) rastgele işlem dizisi (ekle, sil, güncelle, kayıt, bırakma, geri al, yinele, arama …) bütünleşik uygulamaya ve basit bir **gölge modele** aynı anda uygulanır, her işlemden sonra durumlar karşılaştırılır; (b) 10⁵–10⁶ kayıtla her modül kâhinine karşı; (c) sınır durumları (boş veri, tek kayıt, kapasite 1, geri al sınırı 1, döngülü graf).
- **Regresyon:** v1.0 menü oturumlarının çıktısı (yalnız sürüm başlığı gibi bilinen farklar süzülerek) ve önceki sürümlerin program çıktıları kaydedilmiş altın dosyalarla karşılaştırılır.

### 4.6 Bellek güvenliği

- `make asan` ve `make valgrind` hedeflerinde testler, betikler, hatalı girdiler ve kasıtlı hata kipleri çalışır; sonuç rapora yazılır (çalıştırma sayısı, hata ve sızıntı özeti).
- Bellek yetmezliği yarım durum bırakmaz (ör. işlem kaydı işlemden önce ayrılır); hata yollarında da bütün bellek bırakılır.

## 5. Ölçüm raporu (özet)

Ayrıntılar ve tablo/grafik listesi [şablondadır](FINAL_RAPOR_SABLONU.md). Asgari kapsam:

- **Dönem kıyaslaması:** varsayılan projede en az sekiz işlem için ilk ve son gerçekleştirim (ör. yükleme v1.0 ↔ v2.5; numarayla arama v1.0 ↔ v2.9; yinelenen tespiti v2.1 ↔ v2.9; başarı listesi v2.4 ↔ v2.6; kayıt kuyruğu v2.7 ↔ v2.8; ders planı matris ↔ liste; ders seçimi v2.2 ↔ v2.12; öneri sözlüğü her sorguda ↔ saklanan). İki gerçekleştirim **aynı programda, aynı derlemeyle** ölçülür.
- **Ölçek:** algoritmik gerçekleştirimler 10⁶ kayıtta; karesel gerçekleştirimler 10⁴–10⁵'te ölçülüp 10⁶ için T(N) = T(n)·(N/n)² **kestirimiyle** (işaretli); üstel yöntemlerde düğüm sayısı ya da büyüme oranıyla kestirim.
- **Düzen:** her nokta için 1 ısınma + en az 3 tekrar, ortanca; süre bütçesini aşan noktada tek ölçüm (raporda belirtilir); `-O2`; sayaçlar süreden ayrı çalıştırmada (Sedgewick & Wayne, 2011). Ayrıca en az üç işlemde `-O0` ↔ `-O2` karşılaştırması (derleyici kazancı ↔ algoritma kazancı).
- **Kuramla karşılaştırma:** oran testleri, log–log eğimler, sayaçların kapalı biçimleri; sapmalar (önbellek, sabitler) ölçümle tartışılır (Cormen vd., 2022).
- **Tartışma:** sezgisel ↔ alt sınır ↔ kesin (NP-zor alt problemler), sınırlılıklar, makine bilgisi; ek olarak test kapsamı.
- **Biçim:** en çok 15 sayfa (ekler hariç), PDF + Markdown kaynağı; her sayı teslim edilen CSV'lerden betikle üretilir.

Referans rapordaki sayıları değil **kendi makinenizin** sayılarını raporlayın: süreler farklı olacaktır; büyüme sınıfları, sayaçlar ve karşılaştırmaların yönü aynı kalmalıdır.

## 6. Teslim edilecekler

1. **Kod:** `v3.0/` (ya da havuz projesinin klasörü) — kendi başına derlenir; `make temiz` yapılmış hâliyle.
2. **Makefile:** § 4.3'teki hedefler.
3. **Test paketi:** birim, kâhin (kasıtlı hata gösterimleriyle), stres ve regresyon testleri; `testler/` girdileri ve altın çıktılar.
4. **Ölçüm verisi ve raporu:** `olcum/*.csv`, `olcum/OLCUM_ORTAMI.txt` (raporda kullanılan çalıştırmanın kendisi); `rapor/final_raporu.pdf`, Markdown kaynağı, şekiller ve tabloları/grafikleri üreten betik.
5. **README.md:** derleme, kullanım (komut örnekleri), modüller, bilinen eksikler ve kabul ölçütlerinin ✓/✗ listesi (varsayılan projede v3.0 belgesinin "Kabul ölçütleri" listesi).
6. **Sunum:** `sunum/` altında PDF (10–12 slayt) ve canlı demo betiği (`sunum/demo.txt`: demoda çalıştıracağınız komutlar, sırasıyla).
7. **Beyan:** raporun Ek D'si — yararlanılan kaynaklar, referans sürümden alınan dosyalar, kullanılan araçlar ve amaçları.

```
numara_ad_soyad_final/
├── v3.0/                    ← ya da havuz projesinin klasörü
│   ├── *.h  *.c  Makefile  README.md  mini_obs.ayar
│   ├── ornek_veri/  testler/      (testler/beklenen/: altın çıktılar)
│   └── olcum/               ← *.csv, OLCUM_ORTAMI.txt
├── rapor/
│   ├── final_raporu.md  final_raporu.pdf
│   ├── sekiller/            ← *.png
│   └── uret.py              ← CSV → tablo ve grafik (ya da eşdeğeri)
└── sunum/
    ├── sunum.pdf
    └── demo.txt
```

Teslim biçimi (arşiv ya da depo bağlantısı + `v3.0`/`final` etiketi) duyuruyla bildirilir. Derleme ürünleri (`*.o`, programlar, `*_asan`, `*_vg`, `*.gcda`, `*.gcno`) ve büyük veri dosyaları (ör. 10⁶ kayıtlık CSV) teslime konmaz; veri, üretecin komutu ve tohumuyla belgelenir.

## 7. Kabul ölçütleri

### 7.1 Değerlendirmeye alınma koşulları

- [ ] `make temiz && make` derleme hatası vermez (hata değerlendirmeyi durdurur; uyarılar kod kalitesinden puan kaybettirir).
- [ ] `make test` çalışır; v1.0'ın 99 doğrulaması geçer (varsayılan proje).
- [ ] Rapor (PDF), raporun sayılarını üreten CSV'ler ve sunum dosyası teslimdedir; rapordaki sayılar CSV'lerle tutarlıdır.
- [ ] Havuz projelerinde: konu seçiminde onaylanmış bir öneri vardır.
- [ ] Teslimde derleme ürünü ve büyük veri dosyası yoktur.

### 7.2 İşlevsel kabul listesi (varsayılan proje)

Değerlendirmede aşağıdaki komutlar (ve benzerleri) teslim ettiğiniz klasörde otomatik çalıştırılır. Değerler stdout'ta bu sırayla görünmelidir; çıkış kodları birebir denetlenir. Ayrıntılı liste v3.0 belgesindedir; havuz projelerinde § 2.2'deki kabul ölçütleri ve README'nizdeki komutlar kullanılır.

| # | Komut (`v3.0/` içinde) | Beklenen |
|--:|:--|:--|
| 1 | `make temiz && make`; `make test` | sıfır uyarı; `make test` çıkış 0 (birim, kâhin, stres, regresyon) |
| 2 | `cp ornek_veri/ogrenciler.csv t2.csv && ./mini_obs t2.csv < testler/T2_ornek_veri.txt` | v1.0 oturumu: ders ortalamaları 71.12, 74.60, 56.65; çıkış 0 |
| 3 | `./mini_obs ornek_veri/ogrenciler.csv ara no 2301010050 hepsi` | 2301010050 EMRE ÇINAR; üç yöntem aynı sonuç; çıkış 0 |
| 4 | `./mini_obs ornek_veri/ogrenciler.csv ara soyad yıl` | 2301010045, 2301010048 (yalnız bu ikisi) |
| 5 | `./mini_obs ornek_veri/ogrenciler.csv oneri mehmet yilmas` | MEHMET ALİ, MEHMET ALİ KAYA, CAN YILMAZ (bu sırayla) |
| 6 | `./mini_obs ornek_veri/ogrenciler.csv liste soyad 0` | 2301010049, …050, …051, …046, …047, …052, …045, …048 (Türkçe sıra) |
| 7 | `./mini_obs ornek_veri/ogrenciler.csv istatistik` | ortancalar 77.50, 69.30, 55.30 |
| 8 | `./mini_obs ornek_veri/ogrenciler.csv yinelenen testler/yinelenen_k3.csv` | 2400000017, 2400000028, 2400000023; çıkış 1 |
| 9 | betik: `ayar kontenjan 2` · `kaydol BLM101` 2301010045, …046, …048 · `birak BLM101 2301010045` · `durum BLM101` · `geri` · `durum BLM101` | bırakmada 2301010048 kayıtlı listeye aktarılır; `geri` sonrası 2301010045 ve …046 kayıtlı, …048 bekleme listesinde |
| 10 | betik: `ara soyad ars` · `ekle 2301010060;Deniz;Arslan;80;85;70;75;90;95` · `ara soyad ars` · `geri` · `ara soyad ars` · `yinele` · `ara soyad ars` | 2301010060 yok / bulunur / bulunmaz / bulunur (saklanan dizin her değişiklikte geçersiz) |
| 11 | betik: `ayar kontenjan 5` · `istek BLM104` 2301010048, …046, …047 · `isle` | işlenme sırası 2301010048, …046, …047 (FIFO) |
| 12 | `./mini_obs ornek_veri/ogrenciler.csv kayit_oku testler/ders_kayit_yabanci.txt` | 2301019999 bildirilir; hiçbir kayıt yapılmaz; çıkış 1 |
| 13 | `./mini_obs ornek_veri/ogrenciler.csv plan ozet` | 48 ders, 52 önkoşul, döngü yok, en erken dönem 8 |
| 14 | betik: `ayar katalog testler/onkosul_iki_dongu.txt` · `plan` | üç döngüsel bileşen: {BLM201}, {BLM301, BLM302, BLM303}, {MAT102, MAT201}; çıkış 1 |
| 15 | `./mini_obs ornek_veri/ogrenciler.csv donem 2301010046` | 8 dönem; alt sınır ⌈234 / 30⌉ = 8 (en iyi); doğrulama EVET |
| 16 | `./mini_obs ornek_veri/ogrenciler.csv donem - 20` | 13 dönem; alt sınırlar 8 (zincir) ve ⌈240 / 20⌉ = 12 |
| 17 | `./mini_obs ornek_veri/ogrenciler.csv alinabilir 2301010046` | 9 ders: ATA202 BLM101 BLM103 BLM411 BLM412 FIZ102 ING101 MAT101 TDL101 |
| 18 | betik: `ayar kontenjan 3` · `kayit_oku ornek_veri/ders_kayitlari.txt` · `sinav ozet` | 12 sınav, 36 kenar, 5 gün (klik alt sınırı 5); öğrenci başına günde en çok bir sınav |
| 19 | aynı betik + `ayar sinav_gun 4` (ya da `ayar salon_kapasitesi 2`) + `sinav ozet` | gün sınırı karşılanamaz, çıkış 1 (salon kapasitesi 2: 20 parça, 3 salon, çıkış 0) |
| 20 | `./mini_obs ornek_veri/ogrenciler.csv secim 2301010046` | 335 puan, 30 AKTS: ATA202 BLM101 BLM103 FIZ102 ING101 MAT101 |
| 21 | `./mini_obs ornek_veri/ogrenciler.csv bilinmeyen` · `… goster 1` · `./mini_obs testler/bozuk.csv ozet` | çıkış 2 · 1 · 1; tek tip ileti |
| 22 | `./test_kahin --hata-goster kosaraju` (ayrıca `ayni_donem`, `onbellek`) | uyuşmazlık ve küçük karşı örnek; çıkış 1 |


### 7.3 Ölçümle ilgili kabul ölçütleri (kendi makinenizde)

| Ölçüt (v3.0 belgesi § 10) | Eşik | Referans makinede |
|:--|:--|--:|
| 10⁶ kayıtta yinelenen tespiti: tüm çiftler (kestirim) / karma kümesi | ≥ 500 kat | 1 958 kat |
| 10⁶ kaydın toplu yüklenmesi (v2.5) | < 1 dakika | 1,75 s |
| 10⁵ öğrencide toplu ders kaydı: v2.7 yolu / v3.0 yolu | ≥ 50 kat | 139 kat |
| 10⁶ kayıtta öneri sorgusu: her sorguda sözlük / saklanan sözlük | ≥ 100 kat | 8 209 kat |
| n = 35 ders (W = 45): geri izleme / DP | ≥ 10⁴ kat | 458 374 kat |
| V = 16 000 (E = 4V): matrisle / listeyle Kahn | ≥ 50 kat | 256 kat |
| 10⁶ kayıtta numarayla arama (sorgu başına): doğrusal / karma | ≥ 10⁴ kat | 242 274 kat |
| `make olcum` toplam süresi | ≤ 6 dakika | 4 dk 6 s |


Bir eşik kendi makinenizde sağlanmıyorsa bu otomatik bir kayıp değildir: nedenini raporda ölçümle tartışın (ör. sanal makine, güç tasarrufu, önbellek boyutu, başka süreçler). Açıklanmayan sapma puan kaybettirir. Kestirimler (k) ölçüm gibi sunulmaz.

## 8. Puanlama (100 puan)

Rubrik Yol Haritası Tablo 10.3'tür (öneri). Her ölçüt dört düzeyde değerlendirilir; düzey içinde puan, ölçütün alt kalemlerine (aşağıda) göre verilir.

| Ölçüt | Ağırlık | Yetkin (%90–100) | Gelişmiş (%70–89) | Gelişmekte (%40–69) | Yetersiz (%0–39) |
|---|--:|---|---|---|---|
| **İşlevsel doğruluk** | %25 | bütün menü işlevleri ve komutlar beklenen çıktıyı üretir; sınır durumları (boş veri, tek kayıt, döngülü graf, karşılanamayan kısıt, yabancı numara, hatalı argüman) doğru ve tek tip iletiyle işlenir; çıktı sözleşmesine tam uyum; v1.0 oturumları aynen | bir iki küçük sapma (ileti, çıkış kodu, tek bir sınır durumu); algoritmaların sonuçları doğru | bir modül eksik ya da bazı girdilerde yanlış (ör. önbellek eskiyor, dönem planında önkoşul aynı dönemde); bütünleştirme yarım (modüller ayrı programlarda) | birden çok modül eksik; yanlış sonuçlar ya da çökme |
| **Algoritma seçimi ve analiz** | %25 | her işlev için seçilen algoritma ve veri yapısı ölçümle ya da kuramla gerekçeli; kimlik kartları ve karmaşıklıklar doğru; değişmez ve ön/son koşul yorumları eksiksiz; NP-zor alt problemlerde sezgisel + alt sınır + küçük örnekte kesin çözüm; alternatifler tartışılmış | analiz doğru, gerekçelerde küçük boşluklar | karmaşıklık iddialarında hatalar; gerekçe yüzeysel; sezgisel çözüm "en iyi" diye sunulmuş | analiz yok ya da büyük ölçüde yanlış |
| **Test ve doğrulama** | %15 | elle izlenmiş birim testleri; farklı yoldan hesaplayan tohumlu kâhinler; gölge modelli stres testi ve 10⁵–10⁶ kayıt; regresyon; en az üç kasıtlı hata ve küçük karşı örnek; hepsi `make test` ile otomatik | kâhin ve stres var; karşı örnek, sınır durumu ya da regresyon eksik | yalnızca birkaç elle test; kâhin sınanan fonksiyonu çağırıyor; stres testi yok | test yok ya da çalışmıyor |
| **Ölçüm raporu** | %15 | şablonun bütün bölümleri; ilk ↔ son gerçekleştirim aynı düzenekte; 10⁶ ölçüm ve işaretli kestirimler; ortanca ve tekrar; okunur log–log grafikler; oran, eğim ve sayaçlarla kuram karşılaştırması; derleyici ↔ algoritma; sapmalar açıklanmış; makine bilgisi, sınırlılıklar, test kapsamı | eksik bir deney ya da zayıf yorum; biçim kusurları | tablolar var ama kuramla karşılaştırma ya da düzen bilgisi eksik; doğrusal eksen; tek ölçüm; etiketsiz kestirim | rapor yok; sayılar CSV ile tutarsız ya da ölçülmemiş |
| **Kod kalitesi ve bellek güvenliği** | %10 | sıfır uyarı; ASan/UBSan ve Valgrind temiz; modüler, sözleşmeli, okunur kod (Yol Haritası 6.5); tek tip hata bildirimi; yapılandırma; tek bellek sahipliği tablosu; bütün Makefile hedefleri | birkaç uyarı ya da biçim kusuru; bir hedef eksik | ASan/Valgrind raporu ya da sızıntı; dağınık modüller; hata bildirimi tutarsız | derleme sorunları, çok sayıda bellek hatası |
| **Sunum** | %10 | süreye uyar; mimari, algoritma seçimleri ve ölçüm bulguları açık ve sayılarla; canlı demo temiz bir kopyadan sorunsuz; sorulara kendi kodundan ve raporundan doğru ve akıcı yanıt | küçük aksaklıklar (süre, bir demo adımı); yanıtlar büyük ölçüde doğru | demo yarım; slaytlar kod dökümü; yanıtlar yüzeysel | sunum yapılmadı ya da proje açıklanamıyor |

**Puanın dağılımı (ölçüt içinde).**

- *İşlevsel doğruluk (25):* varsayılan projede: kayıtlar, geçmiş ve v1.0 regresyonu 4 · arama ve öneri 4 · listeler ve istatistik 3 · ders kaydı ve kuyruk 4 · önkoşul grafı ve dönem planı 4 · sınav programı 3 · ders seçimi 1 · tek tip hata bildirimi ve yapılandırma 2. Havuz projelerinde: § 2.2'deki asgari gereksinimler eşit ağırlıkla 20 · sınır durumları ve hata bildirimi 5.
- *Algoritma seçimi ve analiz (25):* kimlik kartları ve karmaşıklıklar 8 · değişmez ve sözleşme yorumları 4 · seçimlerin ölçümle ya da kuramla gerekçesi (alternatifleriyle) 8 · NP-zor alt problemlerde sezgisel/alt sınır/kesin yaklaşımı ve indirgemeler 5.
- *Test ve doğrulama (15):* birim testleri 3 · kâhin testleri 4 · stres testi (gölge model + büyük veri + sınır durumları) 4 · kasıtlı hatalar ve regresyon 2 · otomatik çalıştırma ve kapsam bilgisi 2.
- *Ölçüm raporu (15):* yöntem, ortam ve kestirim yöntemi 3 · tablolar ve grafikler 4 · kuramla karşılaştırma (oran, eğim, sayaç) 4 · derleyici ↔ algoritma ve tartışma 2 · sınırlılıklar, yeniden üretilebilirlik ve test kapsamı eki 2.
- *Kod kalitesi ve bellek güvenliği (10):* uyarısız derleme 2 · ASan/UBSan ve Valgrind temiz 3 · modülerlik, adlandırma, sözleşme yorumları, 80 sütun, tek tip hata ve yapılandırma 3 · Makefile hedefleri 2.
- *Sunum (10):* içerik ve yapı (mimari, seçimler, bulgular) 4 · canlı demo 3 · sorular 3.

## 9. Sunum yönergesi

- **Süre:** öğrenci başına 15 dakika: **10 dakika sunum** (canlı demo dahil; demo en az 3 dakika) + **5 dakika soru**. Süre aşımında sunum durdurulur.
- **Slaytlar:** 10–12 slayt (PDF). Önerilen akış: problem ve kapsam (1) · mimari diyagramı (1–2) · algoritma seçimleri ve kimlik kartları (2) · doğrulama: test paketi, stres, bellek (1) · ölçüm bulguları: dönem kıyaslaması grafiği, kuramla karşılaştırma (2–3) · canlı demo (1) · öğrenilen dersler ve sınırlılıklar (1). Slaytta kod dökümü yok (en çok 10–15 satırlık bir kesit); her ölçüm sayısı raporunuzdaki CSV'den gelir. Başvuru içerik planı: [v3.0 sunum taslağı](v3.0/mini_obs_v3_0_sunum_taslagi.md).
- **Canlı demo:** sınıftaki bilgisayarda ya da kendi bilgisayarınızda, **temiz bir kopyadan**: `make temiz && make`, bir betik senaryosu (`sunum/demo.txt`: birkaç modülü uçtan uca gösteren 8–15 komut; en az bir hata durumu ve bir geri alma), büyük veride bir komut (ör. 10⁵–10⁶ kayıtta arama ya da öneri) ve bir ölçüm noktası. Demo bozulursa yedek olarak demo betiğinin önceden kaydedilmiş çıktısını gösterebilirsiniz; ama önce canlı denenir ve aksaklık sunumda açıklanır.
- **Sorular:** öğretim üyesi (ve isteğe bağlı olarak akranlar) şu türlerden sorar: kendi kodunuzdan bir fonksiyonun açıklaması (değişmez, karmaşıklık, sahiplik); bir tasarım kararının gerekçesi; raporunuzdaki bir bulgunun açıklaması (ör. kuramdan sapma); "şu girdide ne olur?" türünden bir sınır durumu; demoda küçük bir değişiklik (ör. bir ayarı değiştirip komutu yeniden çalıştırma).
- **Akran değerlendirmesi** (isteğe bağlı; öğretim üyesinin kararı): her dinleyici bir sunum için kısa geri bildirim formu doldurur; puana katılmaz.

## 10. Akademik dürüstlük ve yapay zekâ kullanımı

- Final projesi bireysel bir çalışmadır. Kurumun akademik dürüstlüğe ilişkin ilke ve düzenlemeleri ile ders izlencesindeki kurallar geçerlidir.
- Kitap, ders materyali, referans sürümler ve çevrim içi kaynaklardan yararlanabilirsiniz; yararlandığınız her kaynağı ve referans sürümden aldığınız her dosyayı beyan ekinde belirtin.
- **Yapay zekâ araçları:** kullanımları, kurumun ve dersin yürürlükteki politikasına bağlıdır. Kullandıysanız beyan ekinde hangi aracı, hangi amaçla ve hangi bölümler için kullandığınızı yazın. Teslim edilen kodun, raporun ve sunumun doğruluğundan ve açıklanabilirliğinden siz sorumlusunuz; sunumdaki sorular bunu da ölçer.
- **Ölçüm verisi:** rapordaki her sayı, teslim ettiğiniz CSV'lerden gelen kendi ölçümünüzdür. Başka bir kaynaktaki (referans rapor dahil) sayıları aktarmak ya da ölçülmemiş bir değeri ölçülmüş gibi sunmak veri uydurmadır; ölçülemeyen değerler yöntemiyle birlikte "kestirim" diye verilir.
- Öğretim üyesi, sunumda ya da ayrı bir görüşmede teslim edilen çalışmanın herhangi bir bölümünü açıklamanızı isteyebilir.

## 11. Sık yapılan hatalar

**Bütünleştirme ve tasarım**

- Modülleri ayrı programlarda bırakıp bir kabuk betiğiyle "bütünleştirmek"; durumun (kayıtlar, geçmiş, defter) komutlar arasında kaybolması.
- Saklanan dizinleri ve sözlüğü kayıt eklenip silinince **geçersiz saymamak** (eski sonuç) ya da her komutta yeniden kurmak (kazanç yok); geri al/yinele sonrasını unutmak.
- Ders kayıtlarını Mini-OBS'de olmayan numaralarla kabul etmek; yarım yüklenen kayıt dosyası.
- Hata iletilerini her modülde farklı biçimlendirmek; aynı hata türüne farklı çıkış kodları vermek; hatalı bir betik komutunda oturumu sonlandırmak.
- Önkoşul grafında yalnızca ilk döngüyü raporlamak; AKTS sınırını yok sayıp en erken dönemi "plan" diye sunmak.
- Bellek yetmezliğinde yarım durum bırakmak (ör. işlem yapılıp geçmiş kaydı ayrılamaması); hata yollarında sızıntı.

**Algoritma**

- NP-zor bir problemde (sınav günü sayısı, AKTS sınırlı dönem planı) sezgisel sonucu "en iyi" diye sunmak; alt sınırla ve küçük örnekte kesin çözümle karşılaştırmamak.
- Toplu işlemlerde (ör. binlerce kaydın deftere işlenmesi) her öğe için doğrusal denetim yaparak farkında olmadan Θ(n²)'ye düşmek — stres testi bunu yakalar.
- Eşitlik kurallarını belgelememek: aynı girdide farklı ama geçerli çıktılar, otomatik karşılaştırmayı bozar.

**Test**

- Kâhinin sınanan fonksiyonu çağırması (aynı hata iki tarafta da vardır); stres testinde gölge model yerine yalnızca "çökmedi mi?" denetimi.
- Yalnızca rastgele girdi: boş veri, tek kayıt, kapasite 1, döngülü graf denenmemiş; kasıtlı hatayla testin gücünü göstermemek.
- Regresyonu atlamak: v1.0 oturumları bütünleştirmeden sonra farklı çıktı veriyor.

**Ölçüm ve rapor**

- İlk ve son gerçekleştirimi farklı programlarda ya da farklı derlemelerle ölçmek; `-O0` ile ölçmek; tek ölçüm; ortanca yerine en iyi değeri raporlamak.
- Kestirimi ölçüm gibi sunmak ya da kestirimin dayandığı noktayı ve varsayımını (önbellek hiyerarşisi değişmez) yazmamak.
- Karesel ve n log n büyümeyi doğrusal eksenli grafikte karşılaştırmak; büyük oranları doğrusal çubukla göstermek.
- Tablo sayılarını elle kopyalamak; makine bilgisini ya da yük durumunu atlamak.
- Gürültülü bir ölçümü (ör. başka bir süreç çalışırken) açıklamadan kuramdan sapma diye yorumlamak.

**Sunum**

- Slaytları kodla doldurmak; ölçüm grafiğini okunamayacak kadar küçük göstermek.
- Demoyu hiç denemeden ya da önceden derlenmiş ikililerle yapmak; demo betiğini hazırlamamak.
- Süreyi aşmak; soruya kendi kodunu açarak yanıt verememek.

## 12. Teslim öncesi denetim listesi

- [ ] Temiz bir kopyada `make temiz && make` (sıfır uyarı), `make test`, `make asan`, `make valgrind`, `make kapsam`.
- [ ] Bölüm 7.2'deki komutlar (ya da havuz projesinin kabul ölçütleri) kendi klasörünüzde beklenen sonuçları ve çıkış kodlarını veriyor.
- [ ] `make olcum` tek oturumda çalıştırıldı; `olcum/*.csv` ve `OLCUM_ORTAMI.txt` raporla aynı çalıştırmaya ait.
- [ ] Rapordaki tablolar ve grafikler bu CSV'lerden betikle yeniden üretildi; kestirimler işaretli; şekillerde yazı okunur (≥ 9 pt), eksenlerde ad, birim ve ölçek var.
- [ ] Rapor şablonun bütün zorunlu bölümlerini içeriyor (mimari, tek bellek sahipliği tablosu, test kapsamı eki) ve PDF'i açılıyor (≤ 15 sayfa, ekler hariç).
- [ ] README'de kabul ölçütleri ✓/✗ işaretlendi; bilinen eksikler yazıldı.
- [ ] Sunum PDF'i (10–12 slayt) ve `sunum/demo.txt` hazır; demo temiz bir kopyada denendi ve süre tutuldu.
- [ ] Beyan eki dolduruldu.
- [ ] `make temiz`; teslimde derleme ürünleri ve büyük veri dosyaları yok.

## 13. Derleme, test ve ölçüm komutları

```bash
cd v3.0
make temiz && make && make test
make asan && make valgrind               # WSL ya da Linux
make kapsam                              # kapsam/KAPSAM.txt
make olcum                               # olcum/donem.csv ve olcum/OLCUM_ORTAMI.txt
./mini_obs ornek_veri/ogrenciler.csv --betik ornek_veri/betik_ornek.txt
./mini_obs ornek_veri/ogrenciler.csv donem 2301010046; echo "[çıkış kodu: $?]"
./olcer_donem yinelenen_karma --n 1000000 --tekrar 3   # tek nokta: stdout sayaçlar, stderr süre
./test_kahin --hata-goster ayni_donem; echo "[çıkış kodu: $?]"
```

## Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Knuth, D. E. (1974). Structured programming with go to statements. *ACM Computing Surveys, 6*(4), 261–301. https://doi.org/10.1145/356635.356640
- Recep Tayyip Erdoğan Üniversitesi. (2025). *Recep Tayyip Erdoğan Üniversitesi ön lisans ve lisans eğitim-öğretim ve sınav yönetmeliği* (Resmî Gazete, 14 Aralık 2025, Sayı: 33107; son değişiklik: Resmî Gazete, 27 Şubat 2026, Sayı: 33181).
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
