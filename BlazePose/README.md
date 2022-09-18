### BlazePose API:
#### Konfigürasyon Ayarları
<br>

- STATIC_IMAGE_MODE : `bool` <br>
 Varsayılan değeri: `false`. `false` durumunda gelen girdiyi video akışı olarak değerlendirir. İlk olarak dedektör kısmı çalışır, görüntüde en belirgin olan insanı tespit edip insanın olduğu bölgeye bölütleme uygulayıp arkaplanı silikleştirir. Tespitin ardından izleyici(tracker) kısmı 33 işaretin yerini takip etmeye başlar. Hesaplama yükünü azaltmak ve gecikmeyi en aza indirmek için her frame'de tekrar dedektör kısmını çalıştırmaz. `true` olduğu durumlarda ise gelen girdiye ayrı bir frame gibi davranır, sadece dedektör kısmı çalışıp ilgili 33 nokta bulunur.
<hr>

- MODEL_COMPLEXITY : `int` <br>
Varsayılan değeri: `1`Pose tespit modelinin karmaşıklığını ifade eder. `0`, `1`, veya `2` değerlerini alabilir.`0` en düşüğü, `1` ortayı, `2` en yükseği temsil eder. Bu değişkenin değeri arttıkça tespit edilen 33 işaret noktasının doğruluğu(accuracy) artarken, gecikme süresi artar. Donanımımızın duruma göre uygun seçenek seçilmelidir.
<hr>

- SMOOTH_LANDMARKS : `bool` <br>
Varsayılan değeri: `true`. Bu durumda farklı frameler arasındaki titreşimi azaltmak için filtre uygular. Fakat STATIC_IMAGE_MODE de `true` değerine sahipse bu değişken dikkate alınmaz.
<hr>

- ENABLE_SEGMENTATION : `bool` <br>
Varsayılan değeri: `false`. `true` olduğu durumlarda insanın olduğu bölgeyi arkaplandan ayırt etmek için bölütleme uygulayıp arkaplanı silikleştirir.
<hr>

- SMOOTH_SEGMENTATION : `bool` <br>
Varsayılan değeri : `true`. `true` olduğu durumlarda titreşimi azaltmak için farklı frame'lere bölütleme maskesi uygular. Fakat ENABLE_SEGMENTATION `false` ise veya STATIC_IMAGE_MODE `true` ise dikkate alınmaz.
<hr>

- MIN_DETECTION_CONFIDENCE : `interval([0.0, 1.0])` <br>
Varsayılan değeri : `0.5`. Dedektör kısmın çalışmasının doğrulanması gereken eşiği belirtir. `1.0` seçilmesi durumunda dedektör algoritmasının 100% doğruluk ile çalışması isteniyor denmektedir bu da modelimizin özellikle kötü kamera koşullarında hiç pose tespit edememesi anlamına gelebilir. `0.0` seçildiğinde ise aslında insan olmayan nesnelerin tespit edilmesi söz konusu olabilir, bu nedenle ortalara bir değer seçmek daha uygundur.
<hr>

- MIN_TRACKING_CONFIDENCE : `interval([0.0, 1.0])` <br>
Varsayılan değeri : `0.5`. MIN_DETECTION_CONFIDENCE durumun izleyici(tracker) kısmı için olan versiyonudur. STATIC_IMAGE_MODE değişkeninin değerinin `true` olması durumunda dikkate alınmaz. 
<br>
<hr>
<hr>

#### Çıktılar

##### POSE_LANDMARKS

İşaret noktaları listesini ifade eder. Listenin her bir elemanı aşağıda verilen özelliklere sahiptir.

- x , y : <br>
İşaret noktalarının verilen girdinin genişlik ve uzunluklarına göre normalize edilip [0.0, 1.0] aralığındaki değerlerini ifade eder.
<hr>

- z : <br>

İşaret noktalarının derinliğini ifade eder. Değer ne kadar küçükse görüntüdeki insan kameraya o kadar yakın anlamına gelir. `x` ile ölçeğe sahiptir.
<hr>

- visibility : <br>
[0.0, 1.0] aralığında bir değer döndürür. İlgili işaret noktasının frame'de görünür olup olmadığını belirtmek için kullanılmıştır.
<hr>

##### POSE_WORLD_LANDMARKS
Belirlenen işaret noktalarının dünya koordinatlarına göre ifade edilmiş hallerini barındıran listedir. Listenin her bir elemanı aşağıda verilen özelliklere sahiptir.

- x, y, z : <br>
Görüntüdeki insanın kalçalarının ortası orijin belirlendikten sonra işaret noktalarının yerini orijine göre metre ölçeğinde döndürür.
<hr>

- visibility : <br>
[0.0, 1.0] aralığında bir değer döndürür. İlgili işaret noktasının frame'de görünür olup olmadığını belirtmek için kullanılmıştır.

##### SEGMENTATION_MASK

Yalnızca ENABLE_SEGMENTATION değerinin `true` olduğu durumlarda döndürülür. Verilen girdi ile aynı boyutlara sahiptir. [0.0, 1.0] aralığındaki değerlerden oluşur. 1.0 değeri yüksek olasılıkla insanın olduğu bölümleri ifade ederken 0.0 değeri yüksek olasılıkla arkaplanın olduğu bölümleri ifade eder.

<hr>
<hr>


