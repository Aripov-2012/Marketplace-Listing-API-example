# Listing API — O'rnatish va Swagger orqali ishlatish bo'yicha to'liq qo'llanma

Ushbu qo'llanmada loyihani o'rnatish, ma'lumotlar bazasini tayyorlash, serverni ishga tushirish hamda **Swagger UI** (`/docs`) orqali API bilan ishlash qadamma-qadam tushuntirilgan.

---

## 1. Loyihani o'rnatish va ishga tushirish

### 1-qadam: Virtual muhitni (venv) yaratish va faollashtirish

Terminalni oching va loyiha papkasiga kiring:

**Linux / macOS:**
```bash
# Agar venv mavjud bo'lmasa, uni yarating:
python3 -m venv .venv

# Virtual muhitni faollashtiring:
source .venv/bin/activate
```

**Windows:**
```cmd
# Virtual muhitni faollashtiring:
.venv\Scripts\activate
```

> **Eslatma:** Virtual muhit faollashganda terminal boshida `(.venv)` yozuvi paydo bo'ladi.

---

### 2-qadam: Kerakli kutubxonalarni o'rnatish

Barcha kerakli kutubxonalar (`fastapi`, `uvicorn`, `sqlalchemy`, `pydantic` va h.k.) `requirements.txt` faylida ko'rsatilgan:

```bash
pip install -r requirements.txt
```

---

### 3-qadam: Konfiguratsiya faylini (`.env`) tekshirish

Loyiha ildizida `.env` fayli mavjudligiga ishonch hosil qiling (yoki `.env.example` dan nusxa oling):

```bash
cp .env.example .env
```

Fayl ichidagi standart sozlamalar:
```ini
PROJECT_NAME="Listing API"
API_V1_STR="/api/v1"
DATABASE_URL="sqlite:///./listings.db"
```

---

### 4-qadam: Ma'lumotlar bazasini dastlabki ma'lumotlar bilan to'ldirish (Seed)

Baza jadvallarini yaratish hamda namunaviy toifalar (kategoriyalar), subkategoriyalar, sotuvchilar va e'lonlarni qo'shish uchun `seed.py` skriptini ishga tushiring:

```bash
python seed.py
```

Muvaffaqiyatli yakunlangach, ekranda `Database seeded successfully!` xabari chiqadi.

---

### 5-qadam: Serverni ishga tushirish

Uvicorn serverini ishga tushiring:

```bash
uvicorn app.main:app --reload --port 8000
```

* `--reload`: Kod o'zgarganda server avtomatik qayta yuklanadi.
* `--port 8000`: API `8000`-portda ishlaydi.

Server muvaffaqiyatli ishga tushgach, quyidagi xabarni ko'rasiz:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 2. Swagger UI ga kirish

Brauzeringizni oching va quyidagi manzilga kiring:

👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** (yoki **http://localhost:8000/docs**)

> **Swagger UI nima?**  
> Bu FastAPI tomonidan avtomatik taqdim etiladigan interaktiv veb-interfeys bo'lib, Postman yoki boshqa dasturlarsiz to'g'ridan-to'g'ri brauzer orqali har bir so'rovni (GET, POST, PATCH) yuborish va natijalarni ko'rish imkonini beradi.

---

## 3. Swagger orqali API dan foydalanish (Qadamma-qadam)

Swagger oynasida har bir API so'rovini sinab ko'rish umumiy qoidasi:
1. Kerakli endpoint qatorini bosing (ochiladi).
2. O'ng tarafdagi **"Try it out"** tugmasini bosing.
3. Parametrlarni yoki JSON ma'lumotlarini kiriting.
4. Ko'k rangdagi **"Execute"** tugmasini bosing.
5. Pastda **"Server response"** bo'limida javob kodi (Status Code) va natijani ko'rasiz.

---

### 1) Barcha e'lonlar ro'yxatini olish (`GET /api/v1/listings`)

Barcha e'lonlarni ko'rish va filtrlash:

1. **`GET /api/v1/listings`** tugmasini bosing.
2. **"Try it out"** tugmasini bosing.
3. Kerakli parametrlarni kiritishingiz mumkin:
   * `skip` (standart: `0`): Qaysi elementdan boshlab olish (sahifalash uchun).
   * `limit` (standart: `100`): Bir vaqtda nechta e'lon olish.
   * `subcategory_id` (ixtiyoriy): Ma'lum bir subkategoriya bo'yicha saralash (masalan: `3`).
   * `seller_id` (ixtiyoriy): Ma'lum bir sotuvchi bo'yicha saralash (masalan: `1`).
4. **"Execute"** tugmasini bosing.

**Javob namunasi (Status 200 OK):**
```json
[
  {
    "slug": "notogri-fellar-jadvali",
    "title": "Noto'g'ri fe'llar jadvali",
    "description": "English irregular verbs",
    "price": 0,
    "seller_id": 1,
    "category": {
      "id": 1,
      "name": "Amaliy ishlar"
    },
    "subcategory": {
      "id": 3,
      "name": "Ingliz tili"
    },
    "file_name": "verbs.docx",
    "file_url": "/files/verbs.docx",
    "file_size": 32092
  }
]
```

---

### 2) Bitta e'lonni `slug` orqali ko'rish (`GET /api/v1/listings/{slug}`)

E'lonning ichki `id` raqami o'rniga uning unikal `slug` matni (identifikatori) ishlatiladi:

1. **`GET /api/v1/listings/{slug}`** bo'limini oching.
2. **"Try it out"** ni bosing.
3. `slug` maydoniga e'lon slug'ini yozing, masalan:
   ```text
   notogri-fellar-jadvali
   ```
4. **"Execute"** tugmasini bosing.

**Muvaffaqiyatli javob:** `200 OK` va tanlangan e'lonning to'liq ma'lumoti.  
**Agar slug topilmasa:** `404 Not Found` qaytadi.

---

### 3) Yangi e'lon qo'shish (`POST /api/v1/listings`)

Yangi e'lon yaratish. Bunda `slug` avtomatik tarzda `title`dan yasaladi (o'zbekcha tutuq belgilar tozalangan holda) yoki o'zingiz kiritishingiz ham mumkin:

1. **`POST /api/v1/listings`** bo'limini oching.
2. **"Try it out"** ni bosing.
3. **Request body** maydoniga quyidagi JSON ma'lumotni joylang:

```json
{
  "title": "Matematika bo'yicha qo'llanma",
  "description": "Oliy matematika fanidan formulalar to'plami",
  "price": 25000,
  "seller_id": 1,
  "subcategory_id": 7,
  "file_name": "matematika_qollanma.pdf",
  "file_url": "/uploads/matematika_qollanma.pdf",
  "file_size": 1048576
}
```

> **Izoh:**
> - `slug` maydonini kiritmasangiz, tizim sarlavhadan avtomatik `matematika-boyicha-qollanma` qilib yaratadi.
> - Agar xuddi shu nomli slug avval mavjud bo'lsa, tizim avtomatik `-2`, `-3` qo'shimchasini qo'shadi.

4. **"Execute"** tugmasini bosing.

**Javob (Status 201 Created):**
```json
{
  "slug": "matematika-boyicha-qollanma",
  "title": "Matematika bo'yicha qo'llanma",
  "description": "Oliy matematika fanidan formulalar to'plami",
  "price": 25000,
  "seller_id": 1,
  "category": {
    "id": 1,
    "name": "Amaliy ishlar"
  },
  "subcategory": {
    "id": 7,
    "name": "Fizika va Matematika"
  },
  "file_name": "matematika_qollanma.pdf",
  "file_url": "/uploads/matematika_qollanma.pdf",
  "file_size": 1048576
}
```

---

### 4) E'lonni yangilash (`PATCH /api/v1/listings/{slug}`)

E'lonning faqat o'zingiz xohlagan maydonlarini yangilash uchun ishlatiladi:

1. **`PATCH /api/v1/listings/{slug}`** bo'limini oching.
2. **"Try it out"** ni bosing.
3. `slug` maydoniga tahrir qilmoqchi bo'lgan e'loningiz slug'ini yozing (masalan: `matematika-boyicha-qollanma`).
4. **Request body**ga o'zgartirmoqchi bo'lgan maydonlaringizni yozing:

```json
{
  "price": 30000,
  "description": "Yangi tahrirdagi kengaytirilgan formulalar"
}
```

> **Eslatma:**
> - Faqat kiritilgan maydonlar yangilanadi, boshqa ma'lumotlar o'zgarishsiz qoladi.
> - Agar faqat `title` o'zgartirilsa, uning `slug`i eskicha qoladi (havolalar buzilmasligi uchun).
> - Agar `slug`ni ham o'zgartirmoqchi bo'lsangiz, uni tanada aniq ko'rsatishingiz kerak (`"slug": "yangi-slug"`).

5. **"Execute"** tugmasini bosing.

---

### 5) Server holatini tekshirish (`GET /health` va `GET /`)

- **`GET /health`**: Tizim ishlayotganini tekshiradi (`{"status": "ok"}`).
- **`GET /`**: Bosh sahifa xabari va hujjatlar yo'lini ko'rsatadi.

---

## 4. Javob kodlari (HTTP Status Codes) va xatolar

| Kod | Ma'nosi | Qachon sodir bo'ladi? |
|---|---|---|
| **200 OK** | Muvaffaqiyatli | Ma'lumot muvaffaqiyatli olindi yoki yangilandi. |
| **201 Created** | Yaratildi | Yangi e'lon muvaffaqiyatli qo'shildi. |
| **400 Bad Request** | Noto'g'ri so'rov | Kiritilgan `slug` formati noto'g'ri, `subcategory_id` yoki `seller_id` bazada mavjud emas. |
| **404 Not Found** | Topilmadi | Kiritilgan `slug` bo'yicha e'lon topilmadi. |
| **405 Method Not Allowed** | Ruxsat berilmagan usul | Masalan, e'lonni o'chirish (`DELETE`) taqiqlangan. |
| **422 Unprocessable Entity** | Validatsiya xatosi | JSON sintaksisi buzilgan yoki majburiy maydonlar to'ldirilmagan. |

---

## 5. Testlarni ishga tushirish

Barcha funksiyalar va validatsiyalar to'g'ri ishlayotganini avtomatik tekshirish uchun:

```bash
pytest -v
```
Barcha 17 ta test muvaffaqiyatli (`passed`) o'tishi kerak.
