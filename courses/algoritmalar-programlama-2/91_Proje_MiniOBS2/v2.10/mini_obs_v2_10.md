# Mini-OBS 2 v2.10 — Graflar: ders önkoşul grafı, geçerli ders planı ve en erken dönem (Hafta 11)

**Bu sürümün amacı:** Hafta 11'in graf temsillerini ve dolaşma algoritmalarını Mini-OBS'nin ders kataloğuna uygulamak. Önkoşul ilişkileri yönlü bir graftır (kenar ÖNKOŞUL → DERS): **geçerli bir ders planı** bu grafın **topolojik sırasıdır** (Kahn, 1962; eşitlikte küçük ders kodu), **hatalı önkoşul girişi** bir **yönlü döngüdür** (DFS, üç renk; döngüdeki dersler yazdırılır), bir dersin **en erken alınabileceği dönem** ise ona giden **en uzun** önkoşul zincirinin ders sayısıdır — BFS katmanı (en **kısa** zincir) bundan küçük olabilir ve örnek katalogda 48 dersin 15'inde küçüktür (§ 4.4). Ayrıca öğrencinin aldığı derslere göre **şimdi alınabilecek dersler** ve bir dersin **önkoşul uzaklığı** (ters grafta BFS) sorgulanır. Ders kodu → köşe eşlemesi v2.9'un karma tablosuyla yapılır. Veri: KURGUSAL 8 dönemlik bir katalog (48 ders, 52 önkoşul; bölümün gerçek kodları değildir) ve ortak LCG ile üretilen büyük DAG'lar. Ölçüm (§ 8): rastgele DAG'da (E = 4V) bütün plan — DFS + Kahn + katman + BFS — V = 10⁶ köşe, 4·10⁶ kenarda 1,03 s sürer; kenar sayaçları kuramla **birebir** (plan = 5E), süreler V + E ile büyür ama (V + E) başına süre önbellek sınırını geçince artar (V = 10³'te 44,4 ns, 10⁶'da 205,9 ns; log–log eğim 1,22). Komşuluk matrisiyle Kahn, V = 16 000 köşede listeyle Kahn'dan 249 kat yavaştır (Θ(V²) ↔ Θ(V + E)).

Dosyalar (satır sayılarıyla): **`graf.h`** (195) · **`graf.c`** (706) · **`onkosul.h`** (172) · **`onkosul.c`** (640) · **`ders_plani.c`** (562) · **`olcer_graf.c`** (429) · **`graf_uret.c`** (116) · `obek.h` (86) · `obek.c` (210) · `sayac.h` (67) · `sayac.c` (33) · `test_obs.c` (3093) · `test_kahin.c` (5190) · `Makefile` (700) · önceki sürümlerin bütün dosyaları · `ornek_veri/onkosul.txt` (117 satır) · `testler/onkosul_dongu.txt` · `testler/onkosul_bozuk.txt` · `testler/graf_kucuk.txt` · `olcum/graf.csv`, `olcum/sirali.csv`, `olcum/matris.csv`, `olcum/bicim.csv`, `olcum/yogunluk.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_10_ciktilar.txt` (1750 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_10_onkosul.png`, `mini_obs_v2_10_dfs.png`; grafik: `mini_obs_v2_10_olcum.png`.

Derleme: `make` (önceki programlar + **`ders_plani`**, **`olcer_graf`**, **`graf_uret`**), `make test`, `make olcum` (bu makinede 1 dakika 16 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 48 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0; 1 (dosya okunamadı ya da biçim hatası, önkoşul grafı döngülü — plan üretilemez —, öğrenci bulunamadı, bellek yetersiz; testlerde uyuşmazlık); 2 (hatalı kullanım, bilinmeyen ders kodu dahil).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 11 grafı **soyut bir model** olarak tanıtır (Cormen vd., 2022; Sedgewick ve Wayne, 2011): köşeler ve kenarlar; labirent, sosyal ağ ve ders önkoşul listesi aynı yapıdır (Haftanın Büyük Sorusu). Mini-OBS'de bu modelin dört sorusu vardır:

- **Temsil** (Konu: "komşuluk matrisi/listesi", Mühendis Gözüyle: "matris, liste ve CSR'nin bellek ve hız sonuçları"): önkoşul grafı **sıkıştırılmış satır (CSR)** biçiminde tek bitişik komşu dizisinde tutulur; matrisle karşılaştırması ölçülür (§ 4.1, § 8.2).
- **Topolojik sıralama** (Konu: "DAG ve topolojik sıralama: Kahn … ve DFS bitiş sırası"; ÖÇ 11.4): geçerli ders planı; eşitlikte küçük ders kodu (rehber 14.2) — bütün geçerli planlar içinde sözlükte en küçüğü (§ 4.2).
- **Döngü tespiti** (Konu: "yönlü döngü tespiti"): DFS'te gri köşeye giden kenar (geri kenar) döngüdür; hatalı önkoşul girişi böyle bulunur ve döngüdeki dersler yığından okunur (§ 4.3).
- **BFS ve katman** (Konu: "BFS, en kısa yol (ağırlıksız)"): BFS **en az kenarlı** yolu verir (Moore, 1959); "en erken dönem" ise **en uzun** zincirdir. İkisini ayırmak bu sürümün kavramsal düğümüdür (§ 4.4).
- **Kaputun Altında / Mühendis Gözüyle** ("üretim kodunda derin özyinelemeden kaçınma"): DFS **açık yığınla** yazılır; 10⁶ derslik bir önkoşul zincirinde de yığın taşmaz (§ 8.3).

Yol haritasındaki karşılığı (Tablo A.1): **H11 · v2.10 · Önkoşul grafı, geçerli ders planı, en erken dönem · Topolojik sıralama, BFS.**

## 2. v2.9'dan ne değişti?

| Konu | v2.9 (H10) | v2.10 (H11) |
|---|---|---|
| Graf | — | **`graf.h/.c`**: kenar dizisi (× 2), CSR (iki geçişli sayma sıralamasıyla, listeler artan), ters graf, rehber 14.3 dosya okuyucu/yazıcı, çok kaynaklı BFS, açık yığınlı DFS (üç renk, ilk döngü, bitiş sırası), Kahn (öbek ya da kuyruk), en uzun yol katmanı, komşuluk matrisi ve matrisle Kahn, rastgele DAG üreteci |
| Önkoşul kataloğu | — | **`onkosul.h/.c`**: ders kodlu katalog dosyası (rehber 14.3 + ders satırları; saf 14.3 de okunur), kod → köşe karma tablosu, plan (DFS + Kahn + katman + BFS), en uzun ve en kısa zincir, alınabilir dersler, eksik önkoşullu dersler, kalan zincir, önkoşul uzaklığı, öğrencinin başarılı dersleri |
| Öbek | v2.6 öbek kurma ve sıralama | + öncelik kuyruğu: `obek_ekle_say` (yukarı süzme), `obek_cikar_say` (Kahn'ın en küçük kaynağı; v2.11'de bitiş zamanları) |
| Sayaç | … yoklama | + `kenar` (okunan komşu; Θ(V + E) denetimi) |
| Programlar | — | **`ders_plani`** (plan, döngü, dönem, alınabilir, uzaklık), **`olcer_graf`** (ölçüm), **`graf_uret`** (büyük DAG dosyası) |
| Testler | 389 birim; kâhin 670 897 denetim | 414 birim (+25 graf-önkoşul); kâhin 675 383 denetim; `--hata-goster gri`, `--hata-goster katman` |

Menü (`mini_obs`) ve önceki programların çıktıları değişmedi (v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır; `mini_obs_v2_10_ciktilar.txt`, Regresyon bölümü).

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `graf` (**yeni**) | temsil (CSR), dosya, BFS, DFS, Kahn, katman, matris, üreteç | `dosya` (durum kodları), `metin`, `obek`, `ortak_rastgele`, `sayac` |
| `onkosul` (**yeni**) | katalog, kod dizini, plan ve sorgular | `graf`, `karma`, `obs` (öğrenci dersleri), `metin` |
| `obek` | + öncelik kuyruğu | `siralama` (karşılaştırıcı tipi), `sayac` |
| `ders_plani.c` (**yeni**) | komut satırı: plan, döngü, dönem, alınabilir, uzaklık, öğrenci | `onkosul`, `graf`, `karma`, `dosya`, `zamanlayici` |
| `olcer_graf.c`, `graf_uret.c` (**yeni**) | ölçüm ve büyük DAG dosyası | `graf`, `deney`, `ortak_rastgele` |
| diğerleri | v2.9'dan aynen | — |

Makefile'da `graf.o` ve `onkosul.o` `GRAF` grubundadır; testler ve `ders_plani` onları `KARMA` ve `SIRALAMA` gruplarıyla bağlar. `graf` modülü öğrenci kaydını **bilmez** (`obs.h`'yi eklemez): kayıtla ilgili tek iş, `onkosul`'un "öğrencinin başarılı dersi" kuralıdır.

## 4. Algoritmalar ve veri yapıları

### 4.1 Önkoşul grafı: dosya, kod → köşe, CSR

![Önkoşul grafı](mini_obs_v2_10_onkosul.png)

*Şekil 1. Örnek katalog (`ornek_veri/onkosul.txt`, KURGUSAL), derslerin en erken dönemlerine göre dizilmiş hâli; dönem başlığının altında o dönemdeki ders ve AKTS sayısı. Kırmızı: en uzun önkoşul zinciri (8 ders, FIZ101 → … → BLM406). BLM202'ye iki yol: yeşil uzun zincir (BLM101 → BLM102 → BLM201 → BLM202, dönem 4) ve turkuaz kısa zincir (MAT101 → BLM104 → BLM202, BFS katmanı 3). Sarı: BFS katmanı en erken dönemden küçük olan 15 ders.*

**Dosya biçimi.** Rehber 14.3'ün ortak graf biçimi (`V E yonlu`, sonra `u v` satırları) önkoşul grafı için **ders kodlu** olarak genişletilir; `#` satırları yorumdur:

```
48 52 yonlu                                ← 14.3 başlığı (önkoşul grafı yönlüdür)
BLM101 6 1 Algoritma ve Programlama I      ← V satır: KOD AKTS DÖNEM Ad
…
BLM101 BLM102                              ← E satır: ÖNKOŞUL DERS (kenar ÖNKOŞUL → DERS)
```

Kod 1–11 karakter (A–Z, 0–9; harfle başlar), katalogda tek; AKTS 1..30; DÖNEM katalogun **önerdiği** dönemdir (1..12; hesaplanan en erken dönemle karşılaştırılır); ad v1.0'ın ad kurallarına uyar. Bilinmeyen kod ve yinelenen önkoşul **biçim hatasıdır** (satır numarası ve Türkçe ileti, çıkış 1); öz döngü (`A A`) hata değildir — döngü denetimi bulur. Başlıktan sonraki ilk veri satırı rakamla başlıyorsa dosya **saf 14.3** biçimidir ve dersler `K0`, `K1`, … (sıfır dolgulu: `K07` < `K10`) adlarını alır; büyük sentetik DAG'lar (`graf_uret`) bu biçimde yazılır ve okunur.

**Kod → köşe (v2.9 karma tablosu).** Dersler **kod sırasında** numaralanır: köşe i, koda göre i. derstir. Böylece rehber 14.2'nin "eşitlikte küçük köşe numarası" kuralı, ders düzeyinde "eşitlikte küçük ders kodu" demektir. Kodlar karma tablosuna `long long` anahtar olarak girer: kod 37 tabanında **birebir** bir sayıya paketlenir (rakam 1..10, harf 11..36, boş konum 0; 11 basamak ⇒ 37¹¹ ≈ 1,8·10¹⁷ < 2⁶³). Dolgu değeri hiçbir karaktere eşit olmadığı için farklı kodların anahtarları farklıdır ve anahtar sırası kod sırasıyla aynıdır (birim testi). Yinelenen önkoşul denetimi de bir karma kümesiyle (anahtar u·V + v) yapılır.

```
Kod → köşe: karma tablosu (kapasite 128 · 48 anahtar · yük α = 0.375 · kurma 61 yoklama); köşeler kod sırasında
```

**CSR (sıkıştırılmış satır).** Komşuluk listesi, köşe başına ayrı bir dinamik dizi yerine **tek bitişik** bir komşu dizisidir: u'nun komşuları `kom[bas[u] .. bas[u+1] − 1]`. Kenar listesinden iki geçişli **sayma sıralamasıyla** (v2.6'nın iki basamaklı taban sıralaması) kurulur: önce hedefe, sonra kaynağa göre kararlı yerleştirme — her liste kendiliğinden artandır (rehber 14.2: komşular artan numarayla dolaşılır), Θ(V + E), karşılaştırma yok. Bellek (V + 1 + E) × 4 bayt (V = 10⁶, E = 4·10⁶ için ≈ 19 MiB); komşuluk matrisi V² hücre ister (10⁶ köşede 10¹² bayt — olanaksız). Ters graf (ders → önkoşul) aynı yolla kurulur; önkoşul uzaklığı ve zincir geri çıkarma onu kullanır.

### 4.2 Geçerli ders planı: Kahn (en küçük kod önce)

```
algoritma KAHN(G)                                 ▷ Θ(V + E) kuyrukla, Θ(E + V log V) öbekle
    her v için gd[v] ← giriş derecesi             ▷ E kenar okunur
    A ← giriş derecesi 0 olan köşeler             ▷ en küçük öbek (v2.6)
    sıra ← boş
    A boş değilken:
        u ← A'dan EN KÜÇÜK numaralı köşe          ▷ eşitlik kuralı: küçük ders kodu
        sıra'ya u'yu ekle
        u → v her kenar için:  gd[v] ← gd[v] − 1;  0 olduysa v'yi A'ya ekle
    |sıra| < V ise: graf döngülü (kalanlar bir döngüde ya da döngüden ulaşılır)
```

- **Değişmez:** sıradaki her dersin bütün önkoşulları sıradadır; A tam olarak giriş derecesi 0'a inmiş ama henüz sıraya girmemiş derslerdir. Bir ders A'ya ancak son önkoşulu sıraya girince girer.
- **Birden çok geçerli plan vardır.** FIFO kuyruğu, DFS'nin ters bitiş sırası ve en küçük öbek üç farklı ama geçerli plan verir (`./ders_plani --yontem kuyruk|dfs`). Öbekli Kahn her adımda **seçilebilecek en küçük kodu** seçtiği için bütün topolojik sıralar içinde sözlükte en küçüğünü üretir — tek ve belirli bir yanıt (kâhin bunu ayrı bir yoldan doğrular, § 4.6).
- Öbek v2.6'nın modülüdür; Kahn için iki işlem eklendi: `obek_ekle_say` (sona koy, yukarı süz) ve `obek_cikar_say` (kökü al, sonu köke taşı, aşağı süz). Öbek "karşılaştırıcıya göre en sonda geleni" köke koyduğu için **ters** karşılaştırıcı verilir: en küçük numara kökte durur.
- Matrisle Kahn (`kahn_matris`) aynı seçimi Θ(V²) ile yapar: giriş dereceleri sütun toplamlarıdır, her adımda en küçük kaynak taranır ve u'nun bütün satırı okunur. Sonuç öbekli Kahn'ınkiyle **aynıdır** (ölçümde sağlama, testte kâhin).

Örnek katalogda plan (ilk 16 ders; sözlükte en küçük olduğu için 1. dönemin ATA202'si önce gelir, sonra BLM101'den açılan BLM102 …):

```
$ ./ders_plani
Katalog: ornek_veri/onkosul.txt · 48 ders · 52 önkoşul (yönlü)
Kod → köşe: karma tablosu (kapasite 128 · 48 anahtar · yük α = 0.375 · kurma 61 yoklama); köşeler kod sırasında
Döngü denetimi (DFS, üç renk, açık yığın): YOK (geri kenar 0) — graf yönlü döngüsüz (DAG)
Geçerli ders planı (Kahn; giriş derecesi 0 olanlardan en küçük kod önce; 48 ders):
  ATA202 BLM101 BLM102 BLM103 BLM201 BLM205 BLM206 BLM303
  BLM305 BLM306 BLM312 BLM409 BLM410 BLM411 BLM412 FIZ101
  FIZ102 BLM203 BLM204 BLM301 BLM307 BLM310 BLM403 BLM405
  BLM406 BLM408 ING101 ING102 MAT101 BLM104 BLM202 BLM208
```

### 4.3 Hatalı önkoşul: DFS üç renk ve döngünün yığından okunması

```
algoritma DFS-DÖNGÜ(G)                            ▷ Θ(V + E); açık yığın
    her köşe BEYAZ
    s = 0 .. V − 1 (BEYAZ ise):  s'yi GRİ yap, yığına koy
        yığın boş değilken:
            u ← yığının tepesi
            u'nun sıradaki komşusu v varsa:       ▷ komşular artan
                v BEYAZ ise  v'yi GRİ yap, yığına koy           ▷ ağaç kenarı
                v GRİ ise    GERİ KENAR: döngü = yığında v … u   ▷ ilk döngü saklanır
                v SİYAH ise  ileri ya da çapraz kenar — döngü DEĞİL
            yoksa  u'yu SİYAH yap, bitiş sırasına ekle, yığından çıkar
```

![DFS ve katman](mini_obs_v2_10_dfs.png)

*Şekil 2. (a) `testler/graf_kucuk.txt`: K2'nin BFS katmanı 2, en erken dönemi 3 (§ 4.4). (b) `testler/onkosul_dongu.txt`'te geri kenar anı (kodlar kısaltılmış: 301 = BLM301): BLM101'den başlayan DFS'nin yığını BLM101 … BLM303 yoludur (hepsi gri); BLM303 → BLM301 kenarı gri bir köşeye gider — döngü yığındaki BLM301 BLM302 BLM303 parçasıdır. (c) 1 → 0 kenarı bitmiş (siyah) köşeye gider: çapraz kenardır, döngü değildir; gri/siyah ayrılmazsa sahte döngü bulunur (`--hata-goster gri`'nin en küçük karşı örneği, § 9).*

- **Gri ⇔ yığında:** yığındaki köşeler kökten başlayan bir yoldur ve tam olarak gri köşelerdir (değişmez). Gri bir köşeye kenar, o yolu kapatır: döngü yığının o köşeden tepeye kadar olan parçasıdır; ayrıca arama yapılmaz.
- **Siyah köşeye kenar döngü değildir.** Siyah köşenin bütün alt ağacı bitmiştir; oradan şimdiki yola dönen bir yol olsaydı o köşe hâlâ gri olurdu. Bu ayrım iki renkle (ziyaret edildi/edilmedi) yapılamaz.
- **Açık yığın:** özyinelemeli DFS her köşe için bir çağrı çerçevesi açar; 10⁶ derslik bir zincirde varsayılan 8 MiB'lık yığın taşabilir. `dfs_dolas` yığını ve "sıradaki komşu" göstergesini (`ilerle[u]`) kendi dizilerinde tutar; derinlik yalnız bellekle sınırlıdır (§ 8.3).
- **Ters bitiş sırası** DAG'da bir topolojik sıradır (`--yontem dfs`).

```
Katalog: testler/onkosul_dongu.txt · 7 ders · 8 önkoşul (yönlü)
Kod → köşe: karma tablosu (kapasite 16 · 7 anahtar · yük α = 0.438 · kurma 12 yoklama); köşeler kod sırasında
Döngü denetimi (DFS, üç renk, açık yığın): VAR — 1 geri kenar; hatalı önkoşul döngüsü (3 ders):
  BLM301 → BLM302 → BLM303 → BLM301
Kahn: 3/7 ders sıraya girdi; planlanamayan 4 ders (döngüde ya da döngüye bağlı):
  BLM301 BLM302 BLM303 BLM401
Sonuç: geçerli ders planı ÜRETİLEMEZ — önkoşul girişini düzeltin.
[çıkış kodu: 1]
```

Döngü varken plan da dönem de tanımsızdır: Kahn yalnızca 3 dersi sıraya koyabilir; döngüdeki üç ders ve döngüdeki BLM303'e bağlı BLM401 planlanamaz. Çıkış kodu 1'dir (hatalı girdi).

### 4.4 En erken dönem ≠ BFS katmanı

**Tanım.** Önkoşulsuz bir ders 1. dönemde alınabilir; bir ders, bütün önkoşulları tamamlandıktan sonraki dönemde alınabilir:

&nbsp;&nbsp;&nbsp;&nbsp;dönem(v) = 1 + max { dönem(u) : u → v },&nbsp;&nbsp;önkoşulsuz v için dönem(v) = 1.

Bu, v'de biten **en uzun** önkoşul zincirinin ders sayısıdır (DAG'da en uzun yol). Topolojik sırada tek geçişle hesaplanır (`dag_katman`): sıra u'ya geldiğinde u'nun bütün önkoşulları işlenmiştir, dönem(u) kesindir ve ardıllarına aday olarak iletilir — Θ(V + E). (Varsayım: dönem başına AKTS sınırı yok; sınırla en erken dönem bundan büyük olabilir, § 11.)

**BFS katmanı** ise önkoşulsuz derslerden (çok kaynaklı BFS) **en az kenarla** ulaşılan uzaklık + 1'dir: v'ye giden **en kısa** zincir. Bir dersin kısa bir yolu varken uzun bir zinciri de olabilir; dönem, zincirin uzun olanı tamamlanmadan gelmez. Örnek katalogda:

```
  BLM202   BFS katmanı 3, en erken dönem 4
           kısa zincir: MAT101 → BLM104 → BLM202
           uzun zincir: BLM101 → BLM102 → BLM201 → BLM202
  BLM401   BFS katmanı 3, en erken dönem 6
           kısa zincir: MAT101 → MAT203 → BLM401
           uzun zincir: BLM101 → BLM102 → BLM201 → BLM202 → BLM304 → BLM401
```

BLM202'nin önkoşulları BLM201 (dönem 3) ve BLM104 (dönem 2) olduğu için dönemi 1 + max(3, 2) = 4'tür; BFS, MAT101 → BLM104 → BLM202 yoluyla 3 der. Örnek katalogda BFS katmanı 15 derste en erken dönemden küçüktür (Şekil 1, sarı); rastgele DAG'larda bu oran çok daha yüksektir (V = 10⁵ dosyasında 97 966 ders; § 8). BFS katmanı **hiçbir zaman** en erken dönemden büyük değildir (en kısa yol en uzun yoldan uzun olamaz; birim testi her ders için denetler). Doğru tanım uygulanır; BFS katmanı ayrı bir soru olarak sunulur: **önkoşul uzaklığı** (§ 4.5) ve "en kısa zincir". Yanlış tanımı kodlayan kasıtlı hatalı sürüm (`--hata-goster katman`) kâhine yakalanır; en küçük karşı örnek 0 → 1 → 2 ve 0 → 2'dir (`testler/graf_kucuk.txt`, § 9).

```
En erken dönem = 1 + önkoşulların en büyük dönemi (en uzun önkoşul zinciri):
  Dönem 1 (9 ders, 43 AKTS):
    ATA202 BLM101 BLM103 BLM411 BLM412 FIZ101 ING101 MAT101
    TDL101
  Dönem 2 (7 ders, 35 AKTS):
    BLM102 BLM104 FIZ102 ING102 MAT102 MAT203 TDL102
  Dönem 3 (6 ders, 30 AKTS):
    BLM201 BLM203 BLM205 BLM208 IST201 MAT201
  Dönem 4 (9 ders, 44 AKTS):
    BLM202 BLM204 BLM206 BLM210 BLM303 BLM305 BLM308 BLM309
    IST301
  Dönem 5 (7 ders, 37 AKTS):
    BLM301 BLM302 BLM304 BLM306 BLM307 BLM312 BLM407
  Dönem 6 (5 ders, 25 AKTS):
    BLM310 BLM401 BLM403 BLM408 BLM409
  Dönem 7 (4 ders, 21 AKTS):
    BLM402 BLM404 BLM405 BLM410
  Dönem 8 (1 ders, 5 AKTS):
    BLM406
```

En uzun zincir 8 derstir — kurgusal katalog 8 dönemlik bir programa sığar:

```
En uzun önkoşul zinciri: 8 ders (FIZ101 → FIZ102 → BLM203 → BLM204 → BLM301 → BLM310 → BLM405 → BLM406)
Katalog dönemi en erken dönemden önce olan ders: 0 (müfredat tutarlı); sonra olan: 22
```

"Katalog dönemi en erken dönemden **önce** olan ders" sayısı müfredatın tutarlılık denetimidir: katalog bir dersi önkoşulları tamamlanmadan önerirse program bunu bildirir ve 1 ile çıkar. Sonra olan dersler (katalog önerisinin en erken dönemden geç olması) hata değildir: ATA202 gibi önkoşulsuz dersler ilk dönemden alınabilir.

**Zincirlerin geri çıkarılması.** `en_uzun_zincir(v)` ters grafta geriye yürür: dönemi i + 1 olan bir dersin dönemi tam i olan en az bir önkoşulu vardır (tanım); ters liste artan olduğu için ilk uyan **en küçük kodlu** önkoşuldur (belirli seçim). `bfs_zinciri(v)` BFS ağacının ebeveyn dizisini izler.

### 4.5 Şimdi alınabilecek dersler ve önkoşul uzaklığı

- **Alınabilir dersler** (`alinabilir_dersler`): alınmamış ve **bütün** önkoşulları alınmış dersler. Alınmış her u'nun ardıllarında bir sayaç artırılır; v için sayaç = giriş derecesi ise v alınabilir. Θ(V + E) — ama okunan kenar yalnız **alınmış** derslerin çıkış dereceleri toplamıdır. Önkoşulu alınmadan alınmış bir ders (tutarsız girdi) ayrıca uyarı olarak yazılır.
- **Kalan en uzun zincir** (`kalan_en_uzun_zincir`): alınmamış derslerden oluşan en uzun zincir = AKTS sınırı yok sayılırsa mezuniyete kalan en az dönem.
- **Önkoşul uzaklığı** (`onkosul_uzakligi`): **ters grafta** v'den BFS; u'nun uzaklığı, u'dan v'ye en kısa önkoşul zincirinin kenar sayısıdır (1 = doğrudan önkoşul). "BLM401'i almak için en az kaç adım geride hangi dersler var?" sorusunun yanıtıdır; dönem değildir.
- **Öğrenci kaydı:** `--ogrenci dosya --no N` öğrenciyi v2.9'un numara dizininde (karma tablosu) bulur; Mini-OBS kaydındaki üç ders (ALG, MAT, FIZ) katalogda BLM101, MAT101 ve FIZ101'e karşılık gelir ve ders **başarılıysa** (CC ve üstü; DC ise YANO ≥ 2,00 — v1.0 kuralı) alınmış sayılır.

```
$ ./ders_plani --ozet --alinan BLM101,MAT101,FIZ101,BLM102 --uzaklik BLM401
$ ./ders_plani --ozet --alinan BLM101,MAT101,FIZ101,BLM102 --uzaklik BLM401
Alınan dersler (4):
  BLM101 BLM102 FIZ101 MAT101
Şimdi alınabilecek dersler (12 ders, 57 AKTS; okunan kenar 8):
  ATA202   Atatürk İlkeleri ve İnkılap Tarihi  5 AKTS · en erken 1, katalog 4
  BLM103   Bilgisayar Mühendisliğine Giriş     4 AKTS · en erken 1, katalog 1
  BLM104   Ayrık Matematik                     5 AKTS · en erken 2, katalog 2
  BLM201   Veri Yapıları                       6 AKTS · en erken 3, katalog 3
  BLM205   Nesneye Yönelik Programlama         5 AKTS · en erken 3, katalog 3
  BLM411   Mühendislik Etiği                   4 AKTS · en erken 1, katalog 7
  BLM412   Girişimcilik                        4 AKTS · en erken 1, katalog 8
  FIZ102   Fizik II                            5 AKTS · en erken 2, katalog 2
  ING101   İngilizce I                         4 AKTS · en erken 1, katalog 1
  MAT102   Matematik II                        6 AKTS · en erken 2, katalog 2
  MAT203   Lineer Cebir                        5 AKTS · en erken 2, katalog 3
  TDL101   Türk Dili I                         4 AKTS · en erken 1, katalog 1
Alınmamış derslerin en uzun önkoşul zinciri: 7 ders → AKTS sınırı yok sayılırsa mezuniyete en az 7 dönem daha (zincirin son dersi: BLM406)
BLM401 Makine Öğrenmesi — önkoşul uzaklığı (ters grafta BFS; 1 = doğrudan önkoşul):
  1 adım (2 ders): BLM304 MAT203
  2 adım (3 ders): BLM202 IST201 MAT101
  3 adım (3 ders): BLM104 BLM201 MAT102
  4 adım (1 ders): BLM102
  5 adım (1 ders): BLM101
  Toplam 10 önkoşul (doğrudan ve dolaylı); okunan kenar 12
  En erken dönem 6 = en uzun zincir (6 ders): BLM101 → BLM102 → BLM201 → BLM202 → BLM304 → BLM401
  BFS katmanı 3 = en kısa zincir (3 ders): MAT101 → MAT203 → BLM401
[çıkış kodu: 0]
```

### 4.6 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `graf_kur`, `graf_ters`, `graf_kenar_var_mi` | kenar **listesi**: her köşenin derecesi, listelerin artanlığı, çoklu kenarların sayısı; ters grafta her u → v için v → u |
| `kahn_sirala` (öbek), `kahn_matris` | her adımda bütün öncülleri yerleşmiş **en küçük** köşeyi kenar listesini tarayarak seçen kaba yöntem (O(V·E) adım başına): aynı sıra, aynı adet |
| `kahn_sirala` (kuyruk) | aynı küme; her kenar sıradaysa ileri |
| `dfs_dolas` | **Floyd–Warshall geçişli kapanışı**: döngü ⇔ bir köşe kendine ulaşır; bulunan döngünün her ardışık kenarı listede var ve köşeleri farklı; DAG'da ters bitiş sırası topolojik |
| `dag_katman`, `plan_kur` (dönem) | Bellman–Ford tarzı **gevşetme** (topolojik sırasız, V tur): en uzun yol |
| `bfs` (çok kaynaklı), BFS katmanı, `onkosul_uzakligi` | Floyd–Warshall **en kısa yol** matrisi: aynı uzaklıklar; ebeveyn kenarı var ve uzaklık bir eksik; ziyaret sırası uzaklıkta azalmayan |
| `katalog_oku`, `katalog_bul` | rastgele kodlu katalog **dosyası** (dersler karışık sırada, araya yorum ve boş satır): köşe = `qsort` ile kod sırası; olmayan kod −1; kimi denemelerde yinelenen önkoşul satırı → biçim hatası ve doğru satır numarası |
| `en_uzun_zincir`, `bfs_zinciri`, `alinabilir_dersler`, `eksik_onkosullu_dersler`, `kalan_en_uzun_zincir` | tanımdan: zincir uzunluğu = dönem, ardışık kenarlar var, eşitlikte en küçük kod; alınabilirlik kenar listesinden; kalan zincir alınmamış köşelerde gevşetme |
| sayaçlar | Kahn: E + sıraya girenlerin dereceleri (DAG'da 2E); DFS ve katman: E; BFS: ulaşılan köşelerin dereceleri toplamı |

Kâhin graflar V = 0..40 köşelidir; yarısı rastgele yönlü graf (öz döngü, çoklu kenar ve döngü olabilir), yarısı gizli bir sıraya göre DAG'dır.

## 5. Bellek sahipliği

| Yapı | Kim ayırır | Kim serbest bırakır | Yaşam süresi |
|---|---|---|---|
| `KenarDizisi.a` | `kenar_ekle` (× 2, `realloc` geçici işaretçiyle) | `kenar_dizisi_birak` | okuma ve kurma boyunca |
| `Graf.bas`, `kom`, `agirlik` | `graf_kur`, `graf_ters` (hata yolunda hepsi geri verilir) | `graf_yok_et` | graf boyunca |
| `DfsSonucu.bitis`, `dongu` | `dfs_dolas` | `dfs_birak` | çağıran bitirene kadar |
| `Katalog` (`ders`, `g`, `ters`, `dizin`) | `katalog_oku` (hata yolunda `katalog_birak`) | `katalog_birak` | program boyunca |
| `Plan` (`sira`, `donem`, `bfs_katman`, `bfs_ebeveyn`, `dfs`) | `plan_kur` | `plan_birak` | program boyunca |
| BFS kuyruğu, Kahn öbeği, giriş dereceleri, DFS yığını | ilgili fonksiyon | aynı fonksiyon (her çıkış yolunda) | çağrı boyunca |
| komşuluk matrisi | `graf_matris_kur` | çağıran (`free`) | ölçüm boyunca |
| önceki sürümlerin yapıları | v2.9 § 5 | v2.9 § 5 | — |

Ayıran her fonksiyonun bildiriminde sahiplik sözleşmesi vardır; `katalog_oku` biçim hatasında yarım katalog bırakmaz (`goto bitir` ile tek temizlik yolu). Çıktı dizileri (sıra, uzaklık, dönem …) çağıranın en az V öğelik dizileridir. `make asan` (yeni programlar, büyük sentetik dosyalar, döngülü ve bozuk dosyalar, kasıtlı hata kipleri dahil) temiz; `make valgrind` 62 çalıştırmanın hepsinde "ERROR SUMMARY: 0 errors" ve "definitely lost: 0 bytes" (yeni ve test çalıştırmaları):

```
valgrind ./obs_test_vg → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 20 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 2 --hata-goster gri → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 3 --hata-goster katman → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_plani_vg → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_plani_vg --ozet --alinan BLM101,MAT101,FIZ101,BLM102 --uzaklik BLM401 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_plani_vg --ozet --ogrenci ornek_veri/ogrenciler.csv --no 2301010046 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_plani_vg testler/onkosul_dongu.txt → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_plani_vg testler/onkosul_bozuk.txt → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_plani_vg testler/graf_kucuk.txt --uzaklik K2 --yontem dfs → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./graf_uret_vg --v 2000 --pencere 3 --cikti vg_dag.txt → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./ders_plani_vg vg_dag.txt --ozet --yontem kuyruk → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_graf_vg plan --n 2,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_graf_vg kur --n 2,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_graf_vg kahn_kuyruk --n 300 --zincir --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_graf_vg kahn_matris --n 2,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
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

```
./ders_plani [katalog.txt] [--yontem kahn|kuyruk|dfs] [--alinan KOD[,KOD…]]
             [--ogrenci dosya --no N] [--uzaklik KOD] [--ozet]
./graf_uret --v V [--yogunluk D] [--pencere P] [--tohum T] [--dongu] --cikti dosya.txt
./olcer_graf İŞLEM [--n V1,V2,…] [--yogunluk D] [--pencere P] [--zincir] [--sirali]
             [--tekrar K] [--tohum T] [--csv dosya.csv [--ekle]]
```

Varsayılan katalog `ornek_veri/onkosul.txt`'tir. Öğrenci kaydıyla (`ornek_veri/ogrenciler.csv`; MEHMET ALİ KAYA'nın ALG notu FF, MAT notu DC ve YANO'su 2,00'nin altında):

```
$ ./ders_plani --ozet --ogrenci ornek_veri/ogrenciler.csv --no 2301010046
Öğrenci 2301010046 MEHMET ALİ KAYA (karma tablosu: 1 yoklama):
  ALG FF → BLM101 ALINMAMIŞ (başarısız)
  MAT DC → MAT101 ALINMAMIŞ (başarısız)
  FIZ CB → FIZ101 alınmış (başarılı)
Alınan dersler (1):
…
```

Saf rehber 14.3 dosyası ve biçim hataları:

```
$ cat testler/graf_kucuk.txt; ./ders_plani testler/graf_kucuk.txt --uzaklik K2
# Saf rehber 14.3 biçimi: V E yonlu, sonra E satır "u v" (köşeler 0..V−1).
# 0 → 1 → 2 ve 0 → 2: köşe 2'nin BFS katmanı 2, en erken dönemi 3.
3 3 yonlu
0 1
1 2
0 2
Katalog: testler/graf_kucuk.txt · 3 ders · 3 önkoşul (yönlü) · saf 14.3 biçimi (dersler K0, K1, …)
Kod → köşe: karma tablosu (kapasite 8 · 3 anahtar · yük α = 0.375 · kurma 3 yoklama); köşeler kod sırasında
Döngü denetimi (DFS, üç renk, açık yığın): YOK (geri kenar 0) — graf yönlü döngüsüz (DAG)
Geçerli ders planı (Kahn; giriş derecesi 0 olanlardan en küçük kod önce; 3 ders):
  K0 K1 K2
Doğrulama: 3 önkoşulun hepsinde önkoşul dersten önce: EVET
En erken dönem = 1 + önkoşulların en büyük dönemi (en uzun önkoşul zinciri):
  Dönem 1 (1 ders):
    K0
  Dönem 2 (1 ders):
    K1
  Dönem 3 (1 ders):
    K2
En uzun önkoşul zinciri: 3 ders (K0 → K1 → K2)
BFS katmanı (önkoşulsuz derslerden en KISA uzaklık + 1) en erken dönemden küçük: 1 ders
  K2       BFS katmanı 2, en erken dönem 3
           kısa zincir: K0 → K2
           uzun zincir: K0 → K1 → K2
K2 — önkoşul uzaklığı (ters grafta BFS; 1 = doğrudan önkoşul):
  1 adım (2 ders): K0 K1
  Toplam 2 önkoşul (doğrudan ve dolaylı); okunan kenar 3
  En erken dönem 3 = en uzun zincir (3 ders): K0 → K1 → K2
  BFS katmanı 2 = en kısa zincir (2 ders): K0 → K2
[çıkış kodu: 0]
```

```
$ ./ders_plani testler/onkosul_bozuk.txt; (yinelenen kod, yinelenen önkoşul, yönsüz başlık)
Hata: testler/onkosul_bozuk.txt okunamadı: dosya biçimi hatalı (satır 7: bilinmeyen ders kodu: BLM999)
Hata: g.txt okunamadı: dosya biçimi hatalı (satır 3: yinelenen ders kodu: A (ilk: 2. satır))
Hata: g.txt okunamadı: dosya biçimi hatalı (satır 5: yinelenen önkoşul: A B)
Hata: g.txt okunamadı: dosya biçimi hatalı (satır 1: başlık "V E yonlu" olmalı (önkoşul grafı yönlüdür; 1 <= V <= 1000000))
[çıkış kodu: 0]
```

Büyük sentetik DAG (`graf_uret`; üreteç aynı kenarı iki kez verebildiği için yinelenenler CSR üzerinden atılır, önkoşul dosyasında yinelenen satır hatadır):

```
$ ./graf_uret --v 100000 --cikti b.txt; head -4 b.txt; ./ders_plani b.txt --ozet --uzaklik K50000 | head -14
b.txt: 100000 köşe, 399917 kenar (400000 deneme, 83 yinelenen atıldı; yönlü, döngüsüz; yoğunluk 4, pencere 0, tohum 42)
# graf_uret --v 100000 --yogunluk 4 --pencere 0 --tohum 42 (Mini-OBS 2 v2.10; ortak LCG)
100000 399917 yonlu
0 62711
1 27551
Süre: katalog okuma 203.713 ms · plan (DFS + Kahn + katman + BFS) 50.672 ms
Katalog: b.txt · 100000 ders · 399917 önkoşul (yönlü) · saf 14.3 biçimi (dersler K0, K1, …)
Kod → köşe: karma tablosu (kapasite 262144 · 100000 anahtar · yük α = 0.381 · kurma 114660 yoklama); köşeler kod sırasında
Döngü denetimi (DFS, üç renk, açık yığın): YOK (geri kenar 0) — graf yönlü döngüsüz (DAG)
Doğrulama: 399917 önkoşulun hepsinde önkoşul dersten önce: EVET
En uzun önkoşul zinciri: 83 ders (K84993 → K01588 → K59611 → K34602 → K81122 → … (73 ders) … → K32291 → K03897 → K89299 → K86043 → K42
BFS katmanı (önkoşulsuz derslerden en KISA uzaklık + 1) en erken dönemden küçük: 97966 ders
K50000 — önkoşul uzaklığı (ters grafta BFS; 1 = doğrudan önkoşul):
  1 adım (5 ders): K14951 K19945 K38822 K42286 K68581
  2 adım (18 ders): K00564 K05360 K06961 K08936 K09958 K11642 K15531 K18361 K26638 K34496 K35627 K40470 K51249 K54504 K58363 K68093 … (+2)
  3 adım (75 ders): K00431 K02018 K02179 K02423 K04295 K04968 K05097 K06165 K06959 K08026 K12029 K13754 K15124 K15239 K15467 K19097 … (+59)
  4 adım (176 ders): K00743 K01191 K01348 K01588 K02120 K02324 K03412 K03864 K04347 K04620 K05438 K05664 K06763 K06983 K07383 K07500 … (+160)
  5 adım (170 ders): K00571 K00768 K01386 K02172 K02321 K04330 K05916 K06292 K06491 K06870 K07370 K08126 K08753 K08976 K09487 K10294 … (+154)
  6 adım (168 ders): K00148 K00494 K01483 K02611 K02617 K02659 K02702 K02796 K04050 K04082 K04255 K05459 K07264 K08081 K09985 K10528 … (+152)
  7 adım (102 ders): K00765 K01766 K02904 K04398 K04509 K06037 K06139 K08289 K09695 K10212 K10413 K11503 K13070 K13372 K15026 K19460 … (+86)
[çıkış kodu: 0]
```

V = 10⁵ dersli, 399 917 önkoşullu dosya bu makinede 203,7 ms'de okunur (satır ayrıştırma, kod tablosu, CSR ve ters graf) ve plan 50,7 ms'de kurulur. `--dongu` ilk kenarın tersini ekler; program döngüyü bulur ve 1 ile çıkar (`mini_obs_v2_10_ciktilar.txt`, bölüm 5).

## 7. Tasarım kararları

1. **CSR, köşe başına dinamik dizi değil.** Tek bitişik komşu dizisi: kurma iki sayma geçişi, dolaşma ardışık bellek okur, yok etme üç `free`. Bedeli: graf kurulduktan sonra kenar eklemek pahalıdır — önkoşul grafı dosyadan bir kez okunduğu için uygundur.
2. **Köşe = kod sırası.** Eşitlik kuralı ("küçük ders kodu") graf algoritmalarında "küçük köşe" olur; çıktılar ayrıca sıralanmadan kod sırasındadır. Kod → köşe eşlemesi karma tablosuyla (beklenen O(1)); kodların sıralanması okumada bir kez (`qsort`, rehber 14.1: araç).
3. **Kahn için öbek** (FIFO değil): belirli ve tek bir plan (sözlükte en küçük), bedeli V log V karşılaştırma (V = 10⁶'da 24 843 230 karşılaştırma, 21 167 291 taşıma; süre 601,5 ms ↔ kuyrukla 128,7 ms).
4. **Döngü için DFS, plan için Kahn.** Kahn döngünün **varlığını** (adet < V) ve etkilenen dersleri söyler, döngünün **kendisini** söylemez; DFS ilk geri kenarda döngüyü yığından okur. İkisi de Θ(V + E); plan ikisini de çalıştırır.
5. **En erken dönem = en uzun yol, BFS ayrı soru.** Ders planlamada doğru soru "en az kaç dönem?"dir ve en uzun zincire bağlıdır; BFS'nin yanıtı (en kısa zincir) "önkoşul uzaklığı" olarak sunulur ve ikisi yan yana yazılır.
6. **Açık yığın, özyineleme yok** (Mühendis Gözüyle). Zincir biçimli önkoşul grafları (uzun ders dizileri) derin özyinelemeyi tetikler; açık yığın derinliği yalnız bellekle sınırlar.
7. **Yinelenen önkoşul hatadır.** Aynı kenar iki kez yazılmışsa giriş derecesi yanlış olmaz ama girdi tutarsızdır; karma kümesi okuma sırasında satır numarasıyla bildirir.

## 8. Ölçümler

**Düzen:** `-O2`; her nokta için önce sayaç açık bir çalıştırma (kenar, karşılaştırma, taşıma), sonra 1 ısınma + 5 tekrar, ortanca; veri hazırlama (DAG üretimi, CSR, kaynaklar, hazır topolojik sıra) süre dışında. Graf: V köşeli rastgele DAG, E = 4V; her kenar gizli bir sıra π'de öne gider (öncül düzgün rastgele, "pencere" verilirse son P köşeden). Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB, L3 33 MiB; gcc 13.3.0, glibc 2.39; tarih 2026-10-22 08:02. `make olcum` 1 dakika 16 s sürdü; en büyük noktalarda süreç belleğinin tepesi 98 MiB (plan, V = 10⁶) ve 129 MiB (matrisle Kahn, V = 16 000). Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 2,29, sonda 2,11 idi (2 çekirdek; aynı anda başka ajanların derleme ve ölçümleri çalışıyordu: süreler gürültülüdür; kenar, karşılaştırma ve taşıma sayaçları değildir).

![Ölçümler](mini_obs_v2_10_olcum.png)

*Şekil 3. Sol üst: rastgele DAG'da süre ↔ V + E (log–log; noktalı çizgi eğim 1). Sağ üst: (V + E) başına süre; düz çizgi köşe numaraları karışık (π rastgele), kesikli çizgi aynı graf köşeleri topolojik sırada numaralanmış. Sol alt: komşuluk matrisi ↔ listesi (Kahn). Sağ alt: V = 10⁵'te derinliğe (en uzun zincir) göre (V + E) başına süre.*

### 8.1 V + E'ye göre süre

| V | E | CSR kurma | Kahn (öbek) | Kahn (kuyruk) | DFS | katman | BFS | plan | plan ns / (V + E) | derinlik | BFS < dönem |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 4 000 | 21,3 µs | 100,2 µs | 12,2 µs | 17,1 µs | 4,9 µs | 6,1 µs | 222,0 µs | 44,4 | 40 | 977 |
| 2 000 | 8 000 | 47,6 µs | 235,3 µs | 35,0 µs | 57,7 µs | 18,5 µs | 20,6 µs | 532,5 µs | 53,2 | 43 | 1 960 |
| 5 000 | 20 000 | 186,7 µs | 671,5 µs | 143,7 µs | 163,3 µs | 79,9 µs | 97,9 µs | 1,4 ms | 57,3 | 56 | 4 889 |
| 10 000 | 40 000 | 501,3 µs | 1,5 ms | 327,1 µs | 343,7 µs | 168,2 µs | 250,3 µs | 2,4 ms | 48,0 | 58 | 9 800 |
| 20 000 | 80 000 | 988,1 µs | 3,3 ms | 716,5 µs | 744,3 µs | 366,4 µs | 559,0 µs | 5,0 ms | 49,6 | 65 | 19 565 |
| 50 000 | 200 000 | 3,0 ms | 9,7 ms | 2,1 ms | 2,3 ms | 1,1 ms | 1,6 ms | 14,8 ms | 59,1 | 74 | 49 003 |
| 100 000 | 400 000 | 10,2 ms | 34,0 ms | 4,9 ms | 5,5 ms | 4,0 ms | 4,0 ms | 54,4 ms | 108,7 | 83 | 97 966 |
| 200 000 | 800 000 | 28,0 ms | 99,5 ms | 12,2 ms | 14,0 ms | 7,0 ms | 10,9 ms | 128,1 ms | 128,1 | 91 | 196 076 |
| 500 000 | 2 000 000 | 120,3 ms | 299,6 ms | 48,7 ms | 81,2 ms | 34,8 ms | 41,6 ms | 382,0 ms | 152,8 | 101 | 490 003 |
| 1 000 000 | 4 000 000 | 291,1 ms | 601,5 ms | 128,7 ms | 213,1 ms | 113,5 ms | 115,4 ms | 1,03 s | 205,9 | 108 | 980 072 |

*Tablo 1. Ortanca süre (`olcum/graf.csv`). "derinlik": en uzun önkoşul zinciri (ders); "BFS < dönem": BFS katmanı en erken dönemden küçük olan ders sayısı. Her V'de kenar sayaçları kuramla birebir: Kahn 2E, DFS = katman = BFS = E, plan = 5E; öbekli Kahn'ın sırası her V'de planınkiyle aynı (kontrol).*

| işlem | eğim 10³–2·10⁴ | eğim 10⁵–10⁶ | eğim 10³–10⁶ | ns / (V + E), V = 10³ | ns / (V + E), V = 10⁶ |
|---|--:|--:|--:|--:|--:|
| CSR kurma | 1,28 | 1,46 | 1,38 | 4,3 | 58,2 |
| Kahn (öbek) | 1,17 | 1,25 | 1,26 | 20,0 | 120,3 |
| Kahn (kuyruk) | 1,36 | 1,42 | 1,34 | 2,4 | 25,7 |
| DFS | 1,26 | 1,59 | 1,37 | 3,4 | 42,6 |
| katman | 1,44 | 1,46 | 1,46 | 1,0 | 22,7 |
| BFS | 1,51 | 1,46 | 1,43 | 1,2 | 23,1 |
| plan | 1,04 | 1,28 | 1,22 | 44,4 | 205,9 |

*Tablo 2. Log–log eğim (süre ↔ V + E) ve (V + E) başına süre.*

**Yorum.**

- **Sayaçlarda doğrusallık kesindir.** Okunan kenar sayısı her V'de 5E'dir; işin miktarı Θ(V + E)'dir. Öbekli Kahn'ın karşılaştırma sayısı ise V log V ile büyür (V = 10⁶'da 24 843 230).
- **Süre V + E ile büyür, ama (V + E) başına süre sabit değildir.** Planın (V + E) başına süresi 44,4 ns (V = 1 000), 49,6 ns (V = 20 000), 108,7 ns (V = 100 000), 205,9 ns (V = 1 000 000); log–log eğim V ≤ 2·10⁴'te planda 1,04 (tek tek işlemlerde 1,04–1,51), V = 10⁵ → 10⁶'da 1,25–1,59'dir. Sıçramalar önbellek düzeylerine denk gelir. Planın çalışma kümesi ≈ 4(V + 1 + E) bayt CSR + yaklaşık sekiz tane V öğelik `int` dizisi (giriş derecesi, sıra, katman, uzaklık, ebeveyn, kuyruk, renk, yığın …) ≈ 4(V + E) + 32V bayttır (hesap): V = 10³'te 51 KiB (çekirdek başına L1d 32 KiB'a yakın), 2·10⁴'te 1,0 MiB (çekirdek başına L2 1 MiB), 10⁵'te 5,0 MiB (L3'te), 10⁶'da 50 MiB (paylaşılan L3 33 MiB'ı aşar: ana bellek). Rastgele DAG'da komşular rastgele köşelerdir: `gd[v]`, `katman[v]`, `uzaklik[v]` erişimleri dağınıktır ve çalışma kümesi bir önbellek düzeyini aşınca her biri bir üst düzeye giden bir kaçırma olur. Θ(V + E) iddiası işlem sayısı içindir; bellek hiyerarşisi "sabit" çarpanı n'e bağlı yapar (v2.7'nin dizi ↔ liste ve v2.9'un karma ↔ sıralama dersleriyle aynı ders).
- **Kahn (öbek) en pahalı adımdır:** V = 10⁶'da 601,5 ms ↔ kuyrukla 128,7 ms (4,7 kat); belirli bir plan için ödenen bedel.

| V | plan, karışık | plan, sıralı | oran | DFS, karışık | DFS, sıralı | BFS, karışık | BFS, sıralı |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 222,0 µs | 208,6 µs | 1,06 | 17,1 µs | 15,6 µs | 6,1 µs | 6,0 µs |
| 2 000 | 532,5 µs | 460,3 µs | 1,16 | 57,7 µs | 47,9 µs | 20,6 µs | 19,0 µs |
| 5 000 | 1,4 ms | 1,3 ms | 1,06 | 163,3 µs | 158,4 µs | 97,9 µs | 97,9 µs |
| 10 000 | 2,4 ms | 2,8 ms | 0,84 | 343,7 µs | 368,7 µs | 250,3 µs | 249,9 µs |
| 20 000 | 5,0 ms | 5,9 ms | 0,84 | 744,3 µs | 765,8 µs | 559,0 µs | 557,2 µs |
| 50 000 | 14,8 ms | 16,2 ms | 0,91 | 2,3 ms | 2,4 ms | 1,6 ms | 1,6 ms |
| 100 000 | 54,4 ms | 36,1 ms | 1,51 | 5,5 ms | 5,9 ms | 4,0 ms | 4,6 ms |
| 200 000 | 128,1 ms | 81,6 ms | 1,57 | 14,0 ms | 17,4 ms | 10,9 ms | 9,2 ms |
| 500 000 | 382,0 ms | 257,9 ms | 1,48 | 81,2 ms | 74,7 ms | 41,6 ms | 36,3 ms |
| 1 000 000 | 1,03 s | 822,4 ms | 1,25 | 213,1 ms | 183,2 ms | 115,4 ms | 107,6 ms |

*Tablo 3. Aynı graflar, köşe numaraları karışık (π rastgele) ve topolojik sırada (π birim; `--sirali`, `olcum/sirali.csv`). Kenar sayaçları iki seride aynıdır.*

Köşeler topolojik sırada numaralandığında (ardışık köşeler ardışık bellekte) plan V = 10⁵'te 1,51, V = 10⁶'da 1,25 kat hızlanır; V = 10⁴–5·10⁴'te ise oran 1'in altına iner (en az 0,84): sıralı numarada öbekli Kahn daha çok karşılaştırma yapar (V = 10⁴'te 198 691 ↔ karışıkta 146 485; öbek işlemlerinin sayısı köşelerin numaralanmasına bağlıdır) ve küçük V'de önbellek kazancı bunu karşılamaz. Fark sınırlıdır, çünkü sıralı numarada da her köşenin öncülleri **rastgele** önceki köşelerdir (komşu erişimi yine dağınıktır). Graf işleme kütüphaneleri köşeleri bu tür yerellik için yeniden numaralar.

### 8.2 Komşuluk matrisi ↔ listesi

| V | E | matrisle Kahn | listeyle Kahn (öbek) | kat | okunan hücre (2V²) | okunan komşu (2E) | matris (MiB) |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 500 | 2 000 | 362,8 µs | 42,2 µs | 9 | 500 000 | 4 000 | 0,2 |
| 1 000 | 4 000 | 1,5 ms | 108,5 µs | 14 | 2 000 000 | 8 000 | 1,0 |
| 2 000 | 8 000 | 6,1 ms | 234,2 µs | 26 | 8 000 000 | 16 000 | 3,8 |
| 4 000 | 16 000 | 33,4 ms | 500,8 µs | 67 | 32 000 000 | 32 000 | 15,3 |
| 8 000 | 32 000 | 108,1 ms | 1,1 ms | 97 | 128 000 000 | 64 000 | 61,0 |
| 16 000 | 64 000 | 649,6 ms | 2,6 ms | 249 | 512 000 000 | 128 000 | 244,1 |

*Tablo 4. Matrisle Kahn Θ(V²) ↔ CSR ile Kahn Θ(E + V log V) (`olcum/matris.csv`). Matris kurma süre dışındadır; iki yöntemin sırası her V'de aynıdır (kontrol).*

V iki katına çıktıkça matrisle Kahn'ın süresi 4,2, 4,0, 5,5, 3,2, 6,0 kat artar (kuram: 4); okunan hücre tam 2V²'dir. V = 16 000 köşede matris 244 MiB'dır (bayt başına bir hücre; sıkıştırılmış bit matrisi 8 kat küçük olurdu) ve Kahn 249 kat yavaştır; V = 10⁶'da matris 10¹² bayt isterdi. Seyrek graf (E = 4V) için liste; yoğun graf (E ≈ V²) ya da "u → v var mı?" sorusunun O(1) olması gerektiğinde matris (Mühendis Gözüyle: temsil seçimi bir modelleme kararıdır). CSR'de bu soru ikili aramayla O(log derece)'dir (`graf_kenar_var_mi`).

### 8.3 Graf biçimi (derinlik) ve yoğunluk

| V | pencere | E | derinlik (en uzun zincir) | BFS < dönem | plan | DFS | BFS | plan ns / (V + E) |
|--:|---|--:|--:|--:|--:|--:|--:|--:|
| 100 000 | 0 (sığ) | 400 000 | 83 | 97 966 | 34,2 ms | 5,5 ms | 3,7 ms | 68,4 |
| 100 000 | 1000 | 400 000 | 964 | 97 969 | 31,9 ms | 5,6 ms | 3,6 ms | 63,8 |
| 100 000 | 100 | 400 000 | 7 440 | 97 968 | 29,6 ms | 5,8 ms | 3,8 ms | 59,3 |
| 100 000 | 10 | 400 000 | 42 480 | 97 937 | 33,5 ms | 7,6 ms | 5,0 ms | 67,0 |
| 100 000 | 2 | 400 000 | 2 788 | 97 490 | 37,6 ms | 5,8 ms | 4,0 ms | 75,2 |
| 100 000 | tek zincir | 99 999 | 100 000 | 0 | 12,6 ms | 4,0 ms | 3,3 ms | 63,0 |
| 1 000 000 | tek zincir | 999 999 | 1 000 000 | 0 | 840,0 ms | 310,4 ms | 255,3 ms | 420,0 |

*Tablo 5. V = 10⁵ (ve tek zincirde 10⁶), E = 4V; pencere P: her kenarın öncülü son P köşeden (`olcum/bicim.csv`).*

- **Süre derinlikten bağımsızdır.** En uzun zincir 83 dersten 42 480 derse çıkarken planın (V + E) başına süresi 59,3–75,2 ns aralığında kalır: Kahn, DFS ve katman her kenarı bir kez okur, zincirin uzunluğu işi değiştirmez.
- **Açık yığınlı DFS 10⁶ derinlikte taşmaz.** Tek zincirde (V = 10⁶) DFS 310,4 ms sürer; özyinelemeli bir DFS her köşe için bir çağrı çerçevesi açardı (8 MiB'lık varsayılan yığında çerçeve başına ≈ 8 bayttan fazlası taşmaya yeter — kestirim, ölçülmedi). Zincirde BFS katmanı her derste en erken döneme eşittir (tek yol vardır).
- **Rastgele DAG'da BFS katmanı neredeyse her derste küçüktür.** Kısa bir önkoşul yolu hemen her zaman vardır; "en erken dönem"i BFS ile hesaplamak gerçekçi graflarda hemen her ders için yanlış sonuç verirdi.

| D = E / V | E | plan | ns / (V + E) | ns / E | kaynak (önkoşulsuz) | derinlik | BFS < dönem |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | 100 000 | 32,4 ms | 162,1 | 324,3 | 36 741 | 22 | 35 936 |
| 2 | 200 000 | 32,6 ms | 108,7 | 163,1 | 13 621 | 41 | 80 461 |
| 4 | 400 000 | 36,8 ms | 73,7 | 92,1 | 1 876 | 83 | 97 966 |
| 8 | 800 000 | 53,9 ms | 59,9 | 67,3 | 36 | 149 | 99 963 |
| 16 | 1 600 000 | 62,3 ms | 36,7 | 39,0 | 1 | 274 | 99 998 |

*Tablo 6. V = 10⁵, yoğunluk D = E / V (`olcum/yogunluk.csv`).*

E 16 kat artınca plan 1,9 kat yavaşlar: köşe başına iş (öbek işlemleri, köşe dizilerinin başlatılması) E'den bağımsızdır; kenar başına süre E büyüdükçe düşer. Yoğunluk arttıkça kaynak (önkoşulsuz ders) sayısı azalır ve derinlik artar.

### 8.4 Sınırlılıklar

Süreler paylaşılan bir sanal makinede, yük altında ölçüldü; kenar, karşılaştırma ve taşıma sayaçları makineden bağımsızdır. Rastgele DAG gerçek müfredatlardan farklıdır (gerçek önkoşul grafları küçük ve sığdır); ölçek deneyleri algoritmanın büyüme sınıfı içindir. Dosya okuma süresi ayrıca ölçülmedi (`ders_plani`'nın stderr'indeki tek ölçüm, § 6). Özyinelemeli DFS'nin taşma sınırı kestirimdir.

## 9. Testler

- **Birim testleri** (`obs_test`): `414 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama + 23 böl-fethet + 19 öbek-doğrusal + 79 bağlı liste + 29 yığın-kuyruk + 36 karma-desen + 25 graf-önkoşul`. Graf-önkoşul testleri: CSR (artan listeler, çoklu kenar, yönsüz ve öz döngü, kapsam dışı köşe); ters graf; rehber 14.3 dosyası ve sekiz biçim hatası (satır numarasıyla); BFS (uzaklık, ebeveyn, sıra, sayaç); Kahn öbek ↔ FIFO (0 → 3, 1 → 2: 0 1 2 3 ↔ 0 1 3 2) ↔ matris; DFS: elmas DAG'da çapraz kenar geri kenar değil, döngünün yığından okunması, 10⁵ köşelik zincirde açık yığın; en uzun yol katmanı; öncelik kuyruğu; rastgele DAG üreteci (aynı tohum aynı kenarlar, döngüsüz); ders kodu anahtarı (sıra koruma); örnek katalog (köşe numaraları, plan, dönemler, zincirler, alınabilir dersler, kalan zincir, önkoşul uzaklığı); döngülü ve saf 14.3 kataloğu; dokuz biçim hatası; öğrencinin başarılı dersleri.
- **Kâhin testleri** (`test_kahin`): 300 denemede 675 383, 1 000 denemede 2 264 200 denetim (graf ve katalog: 14 832), uyuşmazlık yok.
- **Kasıtlı hatalar.** (a) `--hata-goster gri` — DFS'te gri/siyah ayrımı yok: ziyaret edilmiş her köşeye giden kenar geri kenar sayılır. Kâhin rastgele grafta sahte döngüyü yakalar; sonra V ≤ 3 köşeli bütün graflar denenerek en küçük karşı örnek basılır (2 köşe, 1 kenar: 1 → 0 — 0 önce bitmiştir, kenar çaprazdır):

```
$ ./test_kahin --hata-goster gri
KÂHİN UYUŞMAZLIĞI (tohum 2)
  İşlev      : dfs_dolas (üç renk)
  n          : 9
  Beklenen   : döngü VAR (geçişli kapanış)
  Bulunan    : döngü VAR: 0 7 (0 → 7 kenarı yok)
  En küçük karşı örnek (2 köşe, 1 kenar): 1 → 0
    dfs_dolas (üç renk): beklenen döngü YOK (geçişli kapanış); bulunan döngü VAR: 0 1
  Yeniden üretmek için: ./test_kahin --tohum 2 --deneme 1 --hata-goster gri
[çıkış kodu: 1]
```

  (b) `--hata-goster katman` — "en erken dönem = BFS katmanı" yanılgısı; en küçük karşı örnek `graf_kucuk.txt`'in grafıdır:

```
$ ./test_kahin --hata-goster katman
KÂHİN UYUŞMAZLIĞI (tohum 3)
  İşlev      : dag_katman (en erken dönem)
  n          : 29
  Beklenen   : en uzun yol (köşe): 3 1 2 5 3 1 4 1 5 1 3 1 2 5 4 2 1 3 2 1 3 2 1 1 1 2 2 2 4
  Bulunan    : katman: 2 1 2 2 3 1 2 1 2 1 3 1 2 2 2 2 1 2 2 1 2 2 1 1 1 2 2 2 2
  En küçük karşı örnek (3 köşe, 3 kenar): 0 → 1, 0 → 2, 1 → 2
    dag_katman (en erken dönem): beklenen en uzun yol (köşe): 1 2 3; bulunan katman: 1 2 2
  Yeniden üretmek için: ./test_kahin --tohum 3 --deneme 1 --hata-goster katman
[çıkış kodu: 1]
```

## 10. Ders notu için özet (Hafta 11 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'ye **ders önkoşul grafı** ekliyoruz: önkoşulları dosyadan okuyup yönlü bir graf (CSR) kuruyoruz; **Kahn** algoritmasıyla geçerli bir ders planı (eşitlikte küçük ders kodu), **DFS'nin üç rengiyle** hatalı önkoşul döngüsünü (döngüdeki derslerle) buluyoruz; her dersin **en erken dönemini** (en uzun önkoşul zinciri) hesaplıyor ve bunun **BFS katmanından** (en kısa zincir) neden farklı olduğunu gösteriyoruz; öğrencinin aldığı derslere göre **şimdi alınabilecek dersleri** listeliyoruz.

### Gereksinimler

- `graf.h/.c`: kenar dizisi; CSR kurma (komşular artan); rehber 14.3 dosyasını okuma (biçim hatasında satır numarası, çıkış 1); çok kaynaklı BFS; **açık yığınlı** DFS (beyaz/gri/siyah; ilk geri kenarın kapattığı döngü; bitiş sırası); Kahn (giriş derecesi 0 olanlardan **en küçük numaralı**: en küçük öbek); en uzun yol katmanı (topolojik sırada tek geçiş).
- `onkosul.h/.c`: ders kodlu katalog (`V E yonlu`; `KOD AKTS DÖNEM Ad`; `ÖNKOŞUL DERS`); köşeler kod sırasında; kod → köşe **v2.9 karma tablosuyla**; bilinmeyen kod ve yinelenen önkoşul biçim hatası.
- `ders_plani`: geçerli plan ve doğrulaması (her önkoşul dersinden önce); döngü varsa döngüdeki dersler ve planlanamayan dersler, çıkış 1; dönem tablosu ve en uzun zincir; BFS katmanının dönemden küçük olduğu dersler (kısa ve uzun zincirleriyle); `--alinan` / `--ogrenci` ile alınabilir dersler; `--uzaklik KOD` ile önkoşul uzaklığı.
- Testler: CSR ve dolaşmalar ↔ kenar listesi ve geçişli kapanış (Floyd–Warshall); Kahn ↔ kaba "en küçük hazır köşe" seçimi; dönem ↔ gevşetme; katalog okuma ↔ `qsort`'lu kod sırası.
- Ölçüm: V = 10³…10⁵ (isteğe bağlı 10⁶) rastgele DAG'da süre ↔ V + E; kenar sayacı = kuramın değeri; komşuluk matrisiyle kıyas.

### İpuçları

- Komşu listelerini **artan** tutun (CSR'yi iki kararlı sayma geçişiyle kurmak bunu bedavaya verir); BFS/DFS sırası, Kahn'ın eşitlik kuralı ve testlerin beklenen çıktıları buna bağlıdır.
- Kahn'da "giriş derecesi 0" adaylarını en küçük öbekte tutun: v2.6'nın öbeği "en sonda geleni" köke koyuyorsa karşılaştırıcıyı **ters** çevirin. Sıraya V'den az köşe girdiyse graf döngülüdür.
- DFS'de **iki** değil **üç** renk kullanın: siyah köşeye giden kenar döngü değildir (Şekil 2c). Döngüyü bulmak için ayrıca arama yapmayın: gri köşeden yığının tepesine kadar olan parça döngüdür (`konum[v]`: v'nin yığındaki yeri).
- Özyinelemeli DFS yerine açık yığın: her köşe için "sıradaki komşu" göstergesi (`ilerle[u]`) tutun.
- En erken dönem için BFS kullanmayın: dönem(v) = 1 + max(önkoşulların dönemi); Kahn'ın verdiği sırada tek geçiş yeter. Kendinizi `graf_kucuk.txt` ile sınayın (K2: BFS 2, dönem 3).
- Ders kodunu karma tablosuna anahtar yapmak için birebir bir sayıya çevirin (37 tabanı, boş konum 0) ya da v2.9'un tablosunu dizgi anahtarlı yapın; iki farklı kodun aynı anahtarı almadığını test edin.
- Alınabilir derslerde her ders için önkoşulları tek tek aramayın: alınmış derslerin ardıllarını sayın, sayaç = giriş derecesi ise ders alınabilir.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri (414) ve `test_kahin` (300 deneme) geçer.
2. `./ders_plani` şu satırları basar: `Döngü denetimi (DFS, üç renk, açık yığın): YOK (geri kenar 0) — graf yönlü döngüsüz (DAG)` ve `Doğrulama: 52 önkoşulun hepsinde önkoşul dersten önce: EVET`; plan `ATA202 BLM101 BLM102 BLM103` ile başlar.
3. Aynı çıktıda `En uzun önkoşul zinciri: 8 ders (FIZ101 → FIZ102 → BLM203 → BLM204 → BLM301 → BLM310 → BLM405 → BLM406)`, BFS katmanı en erken dönemden küçük 15 ders ve `BLM202   BFS katmanı 3, en erken dönem 4` vardır.
4. `./ders_plani testler/onkosul_dongu.txt` döngüyü `BLM301 → BLM302 → BLM303 → BLM301` olarak yazar, `Kahn: 3/7 ders sıraya girdi` der ve 1 ile çıkar; `./ders_plani testler/onkosul_bozuk.txt` `satır 7: bilinmeyen ders kodu: BLM999` iletisiyle 1 ile çıkar.
5. `./ders_plani --ozet --alinan BLM101,MAT101,FIZ101,BLM102` `Şimdi alınabilecek dersler (12 ders, 57 AKTS; okunan kenar 8)` basar; `--uzaklik BLM401` 1 adımda BLM304 ve MAT203'ü, toplam 10 önkoşulu, en erken dönem 6 ve BFS katmanı 3'ü verir.
6. `./ders_plani testler/graf_kucuk.txt --uzaklik K2`: K2'nin en erken dönemi 3, BFS katmanı 2.
7. `./test_kahin --hata-goster gri` ve `--hata-goster katman` uyuşmazlık ve en küçük karşı örnek basar, 1 ile çıkar; `make asan` ve `make valgrind` temizdir.
8. Ölçüm raporunda: V = 10³…10⁵ (en az dört nokta) süre tablosu ve log–log grafik; kenar sayacının kuramla (Kahn 2E, DFS/BFS/katman E) eşitliği; (V + E) başına süre ve yorumu; matrisle Kahn'ın en az üç V'de kıyası.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | 0 → 1 → 2, 0 → 2 (`graf_kucuk.txt`) | Kahn 0 1 2; K2: dönem 3, BFS katmanı 2 |
| 2 | 0 → 3, 1 → 2 | öbekli Kahn 0 1 2 3; FIFO 0 1 3 2 (ikisi de geçerli) |
| 3 | elmas 0 → 1, 0 → 2, 1 → 3, 2 → 3 | DFS döngü YOK; bitiş 3 1 2 0; 2 → 3 çapraz kenar |
| 4 | 0 → 1 → 2 → 0, 2 → 3, 3 → 3 | döngü 0 1 2; 2 geri kenar (öz döngü dahil); Kahn 0 köşe |
| 5 | 1 → 0 (iki köşe) | döngü YOK (0 siyah) — iki renkli DFS burada yanılır |
| 6 | `onkosul_dongu.txt` | döngü BLM301 BLM302 BLM303; planlanamayan 4 ders (BLM401 dahil); çıkış 1 |
| 7 | kenar satırında `BLM999` | biçim hatası, satır 7, çıkış 1 |
| 8 | aynı önkoşul iki kez | `yinelenen önkoşul: A B`, satır numarası |
| 9 | `--alinan BLM101,MAT101,FIZ101,BLM102` | 12 alınabilir ders; BLM201 var, BLM202 yok |
| 10 | `--alinan BLM101,BLM202` | UYARI: önkoşulu alınmadan alınmış 1 ders (BLM202) |
| 11 | hiç ders alınmamış | kalan en uzun zincir 8 (mezuniyete en az 8 dönem) |
| 12 | 10⁵ köşelik zincir | DFS taşmaz; dönem(son) = 10⁵ |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.9'unuz (ya da referans v2.9), `graf.h` ve `onkosul.h` (bildirimler, sözleşmeler, sahiplik), `ornek_veri/onkosul.txt` ve üç test dosyası, `graf_uret` ve `olcer_graf`'ın ölçüm düzeneği (DAG üretimi, sayaç ve süre), v2.6'nın öbeği (öncelik kuyruğu işlemlerini siz ekleyeceksiniz), Şekil 1 ve 2'nin örnekleri.
- **Yazılır:** `graf.c` (CSR, dosya, BFS, DFS, Kahn, katman), `onkosul.c` (katalog, plan, sorgular), `ders_plani.c`; testler (birim + kâhin); ölçüm ve yorum.
- **Değiştirilmez:** v1.0 kuralları ve menü, v2.9'un karma tablosu, rehber 14.3 dosya biçimi, ortak modüller.
- **Meydan okuma:** (a) Tarjan ya da Kosaraju ile kuvvetli bağlı bileşenleri bulup **bütün** döngüleri bildirin (yalnız ilki değil); (b) geçişli indirgeme ile gereksiz önkoşulları (A → C varken A → B → C) bulun; (c) dönem başına AKTS üst sınırıyla dönem ataması — liste çizelgeleme sezgiseliyle — ve en erken dönemle farkı; (d) DFS'yi özyinelemeli yazıp yığın sınırını ölçerek bulun (yalnız isteğe bağlı argümanla): C'de çerçeve küçük olduğundan 10⁵ köşelik zincirde `ulimit -s` sınırı (varsayılan 8 MiB) aşılmayabilir — H11'in ölçümünde (-O0) eşik ≈ 174 000 köşeydi; taşmayı 10⁶ köşelik zincirde ya da `ulimit -s` değerini düşürerek gözleyin.

## 11. Bilinen sınırlılıklar

- En erken dönem dönem başına **AKTS sınırını** ve dersin hangi yarıyılda açıldığını hesaba katmaz (alt sınırdır); örnek katalogda 1. dönemde 43 AKTS'lik ders "alınabilir" görünür.
- DFS yalnız **ilk** döngüyü yazar; geri kenar sayısı bütün geri kenarları sayar ama birden çok döngünün hepsi listelenmez (Kahn'ın planlanamayan dersler listesi etkilenen bütün dersleri verir).
- Kahn öbekle Θ(E + V log V)'dir; FIFO kuyruklu sürüm Θ(V + E) ama sözlükte en küçük planı vermez.
- Ders kodları yalnız ASCII büyük harf ve rakamdır (Türkçe harf yok); sayısal katalogda AKTS ve dönem bilgisi yoktur.
- Süreler paylaşılan makinede yük altında ölçüldü; rastgele DAG gerçek müfredatı temsil etmez (§ 8.4).

## 12. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Kahn, A. B. (1962). Topological sorting of large networks. *Communications of the ACM, 5*(11), 558–562. https://doi.org/10.1145/368996.369025
- Moore, E. F. (1959). The shortest path through a maze. In *Proceedings of an International Symposium on the Theory of Switching, Part II* (pp. 285–292). Harvard University Press.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
