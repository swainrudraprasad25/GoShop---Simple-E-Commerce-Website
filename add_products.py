from models import Category,Brand,Product

ALL_CATAGORY = [
    ("Electronics", "Laptops, audio and cameras","electronics.png"),      
    ("Fashion", "Clothing and accessories","fashion.png"),             
    ("Footwear", "Shoes for every day","footwear.png"),                 
    ("Home & Living", "Furniture and decor","living.png"),          
    ("Beauty", "Skincare and makeup","beauty.png"),                   
    ("Books", "Read more for less","books.png"),                    
    ("Sports", "Gear to get moving","sports.png"),                  
    ("Gaming", "Controllers and consoles","gaming.png"),             
]
BRANDS=[
    ("Dell", "Laptops and PCs","dell.png"),                         # id 1
    ("JBL", "Audio gear","jbl.png"),                               # id 2
    ("Noise", "Wearables","noise.png"),                              # id 3
    ("Canon", "Cameras","canon.png"),                                # id 4
    ("Nike", "Sportswear","nike.png"),                              # id 5
    ("Sony", "Electronics and gaming","sony.png"), 
    ("Godrej", "Furniture","godrej.png")
]
p = [
   ("Dell Inspiron Laptop", "Intel i5, 16GB RAM, 512GB SSD", 54999, 12, "dell_inspiron_laptop.png", 1, 1),
    ("JBL Wireless Headphones", "Deep bass, 40 hours battery", 3499, 40, "jbl_wireless_headphones.png", 1, 2),
    ("Noise Smartwatch", "Health tracking, Bluetooth calling", 2499, 25, "noise_smartwatch.png", 1, 3),
    ("Canon EOS R50", "24.2MP camera, 4K video, Wi-Fi", 67999, 5, "canon_eos_r50.png", 1, 4),
    ("Sony Bluetooth Speaker", "Portable speaker, 20 hours playtime", 5999, 18, "sony_speaker.png", 1, 6),
    ("Dell Wireless Mouse", "Silent clicks, 2.4GHz", 799, 60, "wireless_mouse.png", 1, 1),
    ("Yellow Cotton T-Shirt", "Regular fit, 100% cotton", 499, 80, "yellow_tshirt.png", 2, 5),
    ("Nike Running Shoes", "Lightweight daily trainer", 4999, 0, "nike_running_shoes.png", 3, 5),
    ("Teal Two-Seater Sofa", "Fabric sofa with solid wood legs", 18999, 4, "teal_sofa.png", 4, 7),
    ("Matte Lipstick Set", "Set of 3 shades", 899, 35, "lipstick_set.png", 5, 3),
    ("Classic Book Bundle", "Set of 4 paperbacks", 1199, 22, "book_bundle.png", 6, 3),
    ("Football Size 5", "Machine-stitched match ball", 999, 50, "football.png", 7, 5),
    ("Sony Wireless Controller", "Haptic feedback, USB-C", 5499, 15, "game_controller.png", 8, 6),
    ("Dell 24\" Monitor", "Full HD IPS, 75Hz", 8999, 0, "dell_monitor.png", 1, 1),
    ("Noise Earbuds", "Noise cancelling, 35 hours playback", 1799, 45, "noise_earbuds.png", 1, 3), 
]
def add(db):
    if db.query(Product).count() > 0:
        return
    for name , description , image in ALL_CATAGORY:
        category=Category(name=name,
                          description=description,
                          image=image)
        db.add(category)
    for name,description, logo in BRANDS:
        brand =Brand(name=name,
                     description=description,
                     logo=logo)
        db.add(brand)
    db.commit()
    for name, description, price, stock, image, cat_id, brand_id in p:
        product = Product(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock,
            image=image,
            is_active=True,             
            category_id=cat_id,            
            brand_id=brand_id,             
        )
        db.add(product)  
    db.commit()
