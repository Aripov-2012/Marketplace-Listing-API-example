"""
Seed script to populate comprehensive Categories, Subcategories, Sellers, and Listings
for the Listing API project.
"""
from app.core.database import SessionLocal, Base, engine
from app.models.category import Category, Subcategory
from app.models.seller import Seller
from app.models.listing import Listing
from app.services.slug import slugify


CATEGORIES_DATA = [
    {
        "id": 1,
        "name": "Amaliy ishlar",
        "subcategories": [
            {"id": 3, "name": "Ingliz tili"},
            {"id": 5, "name": "Dasturlash asoslari"},
            {"id": 6, "name": "Iqtisodiyot va Statistika"},
            {"id": 7, "name": "Fizika va Matematika"},
        ],
    },
    {
        "id": 2,
        "name": "Texnologiyalar",
        "subcategories": [
            {"id": 4, "name": "3D"},
            {"id": 8, "name": "Web dasturlash"},
            {"id": 9, "name": "Mobil ilovalar"},
            {"id": 10, "name": "Sun'iy intellekt va Botlar"},
        ],
    },
    {
        "id": 3,
        "name": "Dizayn va Grafika",
        "subcategories": [
            {"id": 11, "name": "UI/UX & Figma shablonlar"},
            {"id": 12, "name": "Prezentatsiya va Slaydlar"},
            {"id": 13, "name": "Brending va Logotiplar"},
        ],
    },
    {
        "id": 4,
        "name": "Biznes va Boshqaruv",
        "subcategories": [
            {"id": 14, "name": "Biznes rejalar"},
            {"id": 15, "name": "Shartnomalar va Yuridik hujjatlar"},
            {"id": 16, "name": "Marketing va SMM"},
        ],
    },
    {
        "id": 5,
        "name": "Elektron kitoblar va Qo'llanmalar",
        "subcategories": [
            {"id": 17, "name": "O'quv qo'llanmalar"},
            {"id": 18, "name": "Cheat sheet va Konspektlar"},
        ],
    },
]

SELLERS_DATA = [
    {"id": 1, "name": "Amaliyotchi Sotuvchi"},
    {"id": 2, "name": "Abdulaziz Aripov"},
    {"id": 3, "name": "Sardorbek Developer"},
    {"id": 4, "name": "Madina UI/UX Designer"},
    {"id": 5, "name": "Finansist Pro"},
    {"id": 6, "name": "OpenSource Tashkent"},
]

LISTINGS_DATA = [
    {
        "slug": "notogri-fellar-jadvali",
        "seller_id": 1,
        "subcategory_id": 3,
        "title": "Noto'g'ri fe'llar jadvali",
        "description": "English irregular verbs - 150+ noto'g'ri fe'llarning uchala shakli va tarjimalari bilan to'liq jadvali.",
        "price": 0,
        "file_name": "verbs.docx",
        "file_url": "/files/education/verbs.docx",
        "file_size": 32092,
    },
    {
        "slug": "zamonaviy-oshxona-3d-modeli-blender-fbx",
        "seller_id": 2,
        "subcategory_id": 4,
        "title": "Zamonaviy Oshxona 3D Modeli (Blender & FBX)",
        "description": "Blender 4.0 da yaratilgan, 4K PBR teksturalar va Cycles/Eevee render sozlamalari bilan jihozlangan fotorealistik interyer modeli.",
        "price": 45000,
        "file_name": "modern_kitchen_3d.zip",
        "file_url": "/files/3d/modern_kitchen_3d.zip",
        "file_size": 154200000,
    },
    {
        "slug": "fastapi-va-postgresql-bilan-rest-api-shablon",
        "seller_id": 2,
        "subcategory_id": 8,
        "title": "FastAPI va PostgreSQL bilan REST API Shablon",
        "description": "JWT autentifikatsiya, SQLAlchemy 2.0, Alembic migratsiyalari va Docker compose tayyor sozlangan professional backend shabloni.",
        "price": 35000,
        "file_name": "fastapi_pg_boilerplate.zip",
        "file_url": "/files/code/fastapi_pg_boilerplate.zip",
        "file_size": 1420000,
    },
    {
        "slug": "telegram-dokon-boti-python-aiogram-3x",
        "seller_id": 3,
        "subcategory_id": 10,
        "title": "Telegram Do'kon Boti (Python aiogram 3.x)",
        "description": "Click va Payme to'lov tizimlari ulangan, savatcha, qulay katalog va buyurtmalar admin paneli bilan to'liq tayyor Telegram bot manba kodi.",
        "price": 80000,
        "file_name": "telegram_shop_bot.zip",
        "file_url": "/files/bots/telegram_shop_bot.zip",
        "file_size": 3850000,
    },
    {
        "slug": "e-commerce-mobil-ilova-ui-ux-figma-dizayni",
        "seller_id": 4,
        "subcategory_id": 11,
        "title": "E-Commerce Mobil Ilova UI/UX Figma Dizayni",
        "description": "50+ ekran, to'liq dizayn tizimi (Auto-layout, Components, Variables) va interaktiv prototip bilan ta'minlangan zamonaviy mobil do'kon dizayni.",
        "price": 60000,
        "file_name": "ecommerce_app_figma.fig",
        "file_url": "/files/design/ecommerce_app_figma.fig",
        "file_size": 28400000,
    },
    {
        "slug": "startup-va-investorlar-uchun-pitch-deck-prezentatsiya",
        "seller_id": 4,
        "subcategory_id": 12,
        "title": "Startup va Investorlar uchun Pitch Deck Prezentatsiya",
        "description": "25 ta zamonaviy slayd, professional infografikalar, diagrammalar va animatsiyalar bilan tayyorlangan taqdimot shabloni.",
        "price": 25000,
        "file_name": "startup_pitch_deck.pptx",
        "file_url": "/files/slides/startup_pitch_deck.pptx",
        "file_size": 14500000,
    },
    {
        "slug": "qahvaxona-coffee-shop-ochish-boyicha-tayyor-biznes-reja",
        "seller_id": 5,
        "subcategory_id": 14,
        "title": "Qahvaxona (Coffee Shop) ochish bo'yicha tayyor Biznes Reja",
        "description": "3 yillik moliyaviy hisob-kitoblar, Excel modelli daromad va xarajatlar rejasi, bozor tahlili bilan batafsil tayyorlangan biznes reja.",
        "price": 120000,
        "file_name": "coffee_shop_business_plan.xlsx",
        "file_url": "/files/business/coffee_shop_business_plan.xlsx",
        "file_size": 4800000,
    },
    {
        "slug": "ozbekiston-qonunchiligi-boyicha-xizmat-korsatish-shartnomasi-namunasi",
        "seller_id": 5,
        "subcategory_id": 15,
        "title": "O'zbekiston Qonunchiligi bo'yicha Xizmat Ko'rsatish Shartnomasi Namunasi",
        "description": "Frilanserlar va IT mutaxassislar uchun buyurtmachi bilan tuziladigan yuridik jihatdan puxta namunaviy shartnoma (.docx formatida).",
        "price": 0,
        "file_name": "xizmat_korsatish_shartnomasi.docx",
        "file_url": "/files/legal/xizmat_korsatish_shartnomasi.docx",
        "file_size": 45200,
    },
    {
        "slug": "oliy-matematika-chiziqli-algebra-va-analitik-geometriya-kurs-ishi",
        "seller_id": 1,
        "subcategory_id": 7,
        "title": "Oliy Matematika: Chiziqli Algebra va Analitik Geometriya Kurs Ishi",
        "description": "Matritsalar, determinantlar va fazodagi to'g'ri chiziq tenglamalari yechimlari bilan to'liq rasmiylashtirilgan kurs ishi.",
        "price": 20000,
        "file_name": "oliy_matematika_kurs_ishi.pdf",
        "file_url": "/files/docs/oliy_matematika_kurs_ishi.pdf",
        "file_size": 2150000,
    },
    {
        "slug": "ielts-writing-task-2-50-ta-band-8-insho-namunasi",
        "seller_id": 1,
        "subcategory_id": 3,
        "title": "IELTS Writing Task 2: 50 ta Band 8+ Insho Namunasi",
        "description": "Dolzarb mavzulardagi namunaviy insholar, yuqori darajadagi lug'at (lexical resource) va tahliliy izohlar to'plami.",
        "price": 30000,
        "file_name": "ielts_writing_band8_essays.pdf",
        "file_url": "/files/education/ielts_writing_band8_essays.pdf",
        "file_size": 5600000,
    },
    {
        "slug": "low-poly-oyin-uchun-transportlar-toplami",
        "seller_id": 2,
        "subcategory_id": 4,
        "title": "Low-Poly O'yin Uchun Transportlar To'plami",
        "description": "Unity va Unreal Engine uchun moslashtirilgan 12 xil avtomobil modeli, rigging va optimallashtirilgan to'r (mesh).",
        "price": 50000,
        "file_name": "lowpoly_cars_pack.zip",
        "file_url": "/files/3d/lowpoly_cars_pack.zip",
        "file_size": 42300000,
    },
    {
        "slug": "python-boshlovchilar-uchun-amaliy-konspekt-va-vazifalar",
        "seller_id": 6,
        "subcategory_id": 5,
        "title": "Python Boshlovchilar Uchun Amaliy Konspekt va Vazifalar",
        "description": "Sintaksis, ma'lumotlar turlari, funksiyalar va OOP asoslari bo'yicha test topshiriqlari bilan ochiq o'quv qo'llanma.",
        "price": 0,
        "file_name": "python_asoslari_konspekt.pdf",
        "file_url": "/files/books/python_asoslari_konspekt.pdf",
        "file_size": 3800000,
    },
    {
        "slug": "nextjs-14-app-router-va-tailwind-css-boshlangich-shablon",
        "seller_id": 2,
        "subcategory_id": 8,
        "title": "Next.js 14 App Router va Tailwind CSS Boshlang'ich Shablon",
        "description": "TypeScript, shadcn/ui komponentlari, qorong'i rejim (dark mode) va SEO teglari oldindan sozlangan Next.js shabloni.",
        "price": 15000,
        "file_name": "nextjs_starter_template.zip",
        "file_url": "/files/code/nextjs_starter_template.zip",
        "file_size": 2900000,
    },
    {
        "slug": "restoran-va-kafe-brendingi-menyu-tashrif-qogoxi-va-forma-dizayni",
        "seller_id": 4,
        "subcategory_id": 13,
        "title": "Restoran va Kafe Brendingi: Menyu, Tashrif Qog'ozi va Forma Dizayni",
        "description": "Adobe Illustrator va Photoshop formatlarida chop etishga tayyor (CMYK 300dpi) to'liq vektor brending to'plami.",
        "price": 75000,
        "file_name": "cafe_branding_pack.zip",
        "file_url": "/files/design/cafe_branding_pack.zip",
        "file_size": 89000000,
    },
    {
        "slug": "smm-mutaxassisi-uchun-30-kunlik-kontent-reja-shablon",
        "seller_id": 5,
        "subcategory_id": 16,
        "title": "SMM Mutaxassisi Uchun 30 Kunlik Kontent-Reja Shablon",
        "description": "Instagram va Telegram kanallar uchun rubrikalar, post matnlari g'oyalari va stories ssenariylari jamlangan Notion & Excel shablon.",
        "price": 20000,
        "file_name": "smm_content_plan_30days.xlsx",
        "file_url": "/files/marketing/smm_content_plan_30days.xlsx",
        "file_size": 1200000,
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Categories & Subcategories
        print("--- Seeding Categories and Subcategories ---")
        for cat_data in CATEGORIES_DATA:
            category = db.query(Category).filter(Category.id == cat_data["id"]).first()
            if not category:
                category = Category(id=cat_data["id"], name=cat_data["name"])
                db.add(category)
                db.flush()
                print(f"Created category [{category.id}]: {category.name}")
            else:
                # Update name if changed
                category.name = cat_data["name"]

            for subcat_data in cat_data["subcategories"]:
                subcat = db.query(Subcategory).filter(Subcategory.id == subcat_data["id"]).first()
                if not subcat:
                    subcat = Subcategory(
                        id=subcat_data["id"],
                        category_id=category.id,
                        name=subcat_data["name"],
                    )
                    db.add(subcat)
                    print(f"  Created subcategory [{subcat.id}]: {subcat.name} (Cat {category.id})")
                else:
                    subcat.category_id = category.id
                    subcat.name = subcat_data["name"]

        db.commit()

        # 2. Seed Sellers
        print("\n--- Seeding Sellers ---")
        for seller_data in SELLERS_DATA:
            seller = db.query(Seller).filter(Seller.id == seller_data["id"]).first()
            if not seller:
                seller = Seller(id=seller_data["id"], name=seller_data["name"])
                db.add(seller)
                print(f"Created seller [{seller.id}]: {seller.name}")
            else:
                seller.name = seller_data["name"]

        db.commit()

        # 3. Seed Listings
        print("\n--- Seeding Listings ---")
        for listing_item in LISTINGS_DATA:
            slug = listing_item["slug"] or slugify(listing_item["title"])
            existing = db.query(Listing).filter(Listing.slug == slug).first()
            if not existing:
                listing = Listing(
                    slug=slug,
                    seller_id=listing_item["seller_id"],
                    subcategory_id=listing_item["subcategory_id"],
                    title=listing_item["title"],
                    description=listing_item.get("description"),
                    price=float(listing_item["price"]),
                    file_name=listing_item["file_name"],
                    file_url=listing_item["file_url"],
                    file_size=listing_item["file_size"],
                )
                db.add(listing)
                print(f"Created listing: '{slug}' - {listing.title}")
            else:
                # Update existing listing details
                existing.seller_id = listing_item["seller_id"]
                existing.subcategory_id = listing_item["subcategory_id"]
                existing.title = listing_item["title"]
                existing.description = listing_item.get("description")
                existing.price = float(listing_item["price"])
                existing.file_name = listing_item["file_name"]
                existing.file_url = listing_item["file_url"]
                existing.file_size = listing_item["file_size"]
                print(f"Updated listing: '{slug}'")

        db.commit()
        print("\nDatabase seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error while seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
