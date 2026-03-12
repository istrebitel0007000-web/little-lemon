"""
Run this script from your Django project root:
    python download_menu_images.py

It will download all menu food images into:
    restaurant/static/images/menu/
"""

import os
import urllib.request

# Create the folder
SAVE_DIR = os.path.join("restaurant", "static", "images", "menu")
os.makedirs(SAVE_DIR, exist_ok=True)

images = {
    # Fast Food
    "burger_classic.jpg":     "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=220&fit=crop&auto=format&q=80",
    "burger_chicken.jpg":     "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=400&h=220&fit=crop&auto=format&q=80",
    "burger_smash.jpg":       "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400&h=220&fit=crop&auto=format&q=80",
    "nuggets.jpg":            "https://images.unsplash.com/photo-1562802378-063ec186a863?w=400&h=220&fit=crop&auto=format&q=80",
    "fish_chips.jpg":         "https://images.unsplash.com/photo-1544982503-9f984c14501a?w=400&h=220&fit=crop&auto=format&q=80",
    "hotdog.jpg":             "https://images.unsplash.com/photo-1619740455993-9d8f8c95c04f?w=400&h=220&fit=crop&auto=format&q=80",
    # Salads
    "caesar_salad.jpg":       "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&h=220&fit=crop&auto=format&q=80",
    "greek_salad.jpg":        "https://images.unsplash.com/photo-1551248429-40975aa4de74?w=400&h=220&fit=crop&auto=format&q=80",
    "chicken_salad.jpg":      "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=220&fit=crop&auto=format&q=80",
    "tuna_nicoise.jpg":       "https://images.unsplash.com/photo-1534482421-64566f976cfa?w=400&h=220&fit=crop&auto=format&q=80",
    "garden_salad.jpg":       "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&h=220&fit=crop&auto=format&q=80",
    "avocado_prawn.jpg":      "https://images.unsplash.com/photo-1515516969-d4008cc6241a?w=400&h=220&fit=crop&auto=format&q=80",
    # Pasta & Mains
    "carbonara.jpg":          "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400&h=220&fit=crop&auto=format&q=80",
    "arrabbiata.jpg":         "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=400&h=220&fit=crop&auto=format&q=80",
    "salmon.jpg":             "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&h=220&fit=crop&auto=format&q=80",
    "chicken_chop.jpg":       "https://images.unsplash.com/photo-1598103442097-8b74394b95c8?w=400&h=220&fit=crop&auto=format&q=80",
    "lamb_rack.jpg":          "https://images.unsplash.com/photo-1544025162-d76538a4b6c4?w=400&h=220&fit=crop&auto=format&q=80",
    "risotto.jpg":            "https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=400&h=220&fit=crop&auto=format&q=80",
    # Pizza
    "pizza_margherita.jpg":   "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=220&fit=crop&auto=format&q=80",
    "pizza_bbq.jpg":          "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=220&fit=crop&auto=format&q=80",
    "pizza_pepperoni.jpg":    "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&h=220&fit=crop&auto=format&q=80",
    "pizza_veggie.jpg":       "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=220&fit=crop&auto=format&q=80",
    # Snacks
    "fries.jpg":              "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&h=220&fit=crop&auto=format&q=80",
    "loaded_fries.jpg":       "https://images.unsplash.com/photo-1585109649139-366815a0d713?w=400&h=220&fit=crop&auto=format&q=80",
    "onion_rings.jpg":        "https://images.unsplash.com/photo-1639024471283-03518883512d?w=400&h=220&fit=crop&auto=format&q=80",
    "garlic_bread.jpg":       "https://images.unsplash.com/photo-1573140401552-3fab0b24306f?w=400&h=220&fit=crop&auto=format&q=80",
    "coleslaw.jpg":           "https://images.unsplash.com/photo-1621956838481-357d85e32ec9?w=400&h=220&fit=crop&auto=format&q=80",
    "wings.jpg":              "https://images.unsplash.com/photo-1527477396000-e27163b481c2?w=400&h=220&fit=crop&auto=format&q=80",
    # Desserts
    "lava_cake.jpg":          "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=220&fit=crop&auto=format&q=80",
    "cheesecake.jpg":         "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=400&h=220&fit=crop&auto=format&q=80",
    "tiramisu.jpg":           "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=220&fit=crop&auto=format&q=80",
    "ice_cream.jpg":          "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=400&h=220&fit=crop&auto=format&q=80",
    # Malaysian
    "nasi_lemak.jpg":         "https://images.unsplash.com/photo-1567982047351-76b6f93e38ee?w=400&h=220&fit=crop&auto=format&q=80",
    "nasi_lemak_ayam.jpg":    "https://images.unsplash.com/photo-1569050467447-ce54b3bbc37d?w=400&h=220&fit=crop&auto=format&q=80",
    "mee_goreng.jpg":         "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400&h=220&fit=crop&auto=format&q=80",
    "char_kuey_teow.jpg":     "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400&h=220&fit=crop&auto=format&q=80",
    "laksa_asam.jpg":         "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400&h=220&fit=crop&auto=format&q=80",
    "curry_laksa.jpg":        "https://images.unsplash.com/photo-1548943487-a2e4e43b4853?w=400&h=220&fit=crop&auto=format&q=80",
    "rendang.jpg":            "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=400&h=220&fit=crop&auto=format&q=80",
    "ayam_percik.jpg":        "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=220&fit=crop&auto=format&q=80",
    "roti_canai.jpg":         "https://images.unsplash.com/photo-1585325701954-2f661a0282c2?w=400&h=220&fit=crop&auto=format&q=80",
    "nasi_goreng.jpg":        "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400&h=220&fit=crop&auto=format&q=80",
    "satay.jpg":              "https://images.unsplash.com/photo-1529201888199-5f0db2fa4a8e?w=400&h=220&fit=crop&auto=format&q=80",
    "ikan_bakar.jpg":         "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=400&h=220&fit=crop&auto=format&q=80",
    # Chinese
    "wonton_noodle.jpg":      "https://images.unsplash.com/photo-1569050467447-ce54b3bbc37d?w=400&h=220&fit=crop&auto=format&q=80",
    "dim_sum.jpg":            "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=400&h=220&fit=crop&auto=format&q=80",
    "chicken_rice.jpg":       "https://images.unsplash.com/photo-1569050467447-ce54b3bbc37d?w=400&h=220&fit=crop&auto=format&q=80",
    "claypot_tofu.jpg":       "https://images.unsplash.com/photo-1547592180-85f173990554?w=400&h=220&fit=crop&auto=format&q=80",
    "kung_pao.jpg":           "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=220&fit=crop&auto=format&q=80",
    "sweet_sour_pork.jpg":    "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400&h=220&fit=crop&auto=format&q=80",
    "garlic_prawn.jpg":       "https://images.unsplash.com/photo-1552611052-33e04de081de?w=400&h=220&fit=crop&auto=format&q=80",
    "braised_duck.jpg":       "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=400&h=220&fit=crop&auto=format&q=80",
    "char_siu.jpg":           "https://images.unsplash.com/photo-1529201888199-5f0db2fa4a8e?w=400&h=220&fit=crop&auto=format&q=80",
    "bak_kut_teh.jpg":        "https://images.unsplash.com/photo-1569050467447-ce54b3bbc37d?w=400&h=220&fit=crop&auto=format&q=80",
    "yang_chow_rice.jpg":     "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400&h=220&fit=crop&auto=format&q=80",
    "prawn_noodle.jpg":       "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400&h=220&fit=crop&auto=format&q=80",
    # Thai
    "tom_yum.jpg":            "https://images.unsplash.com/photo-1569050467447-ce54b3bbc37d?w=400&h=220&fit=crop&auto=format&q=80",
    "tom_kha.jpg":            "https://images.unsplash.com/photo-1548943487-a2e4e43b4853?w=400&h=220&fit=crop&auto=format&q=80",
    "pad_thai.jpg":           "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400&h=220&fit=crop&auto=format&q=80",
    "green_curry.jpg":        "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400&h=220&fit=crop&auto=format&q=80",
    "massaman.jpg":           "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=400&h=220&fit=crop&auto=format&q=80",
    "som_tum.jpg":            "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400&h=220&fit=crop&auto=format&q=80",
    "larb_gai.jpg":           "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=220&fit=crop&auto=format&q=80",
    "basil_pork.jpg":         "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=220&fit=crop&auto=format&q=80",
    "mango_sticky.jpg":       "https://images.unsplash.com/photo-1519984388953-d2406bc725e1?w=400&h=220&fit=crop&auto=format&q=80",
    "pork_neck.jpg":          "https://images.unsplash.com/photo-1529201888199-5f0db2fa4a8e?w=400&h=220&fit=crop&auto=format&q=80",
    "pineapple_rice.jpg":     "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400&h=220&fit=crop&auto=format&q=80",
    "fish_cake.jpg":          "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=220&fit=crop&auto=format&q=80",
    # Drinks
    "hot_coffee.jpg":         "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=220&fit=crop&auto=format&q=80",
    "hot_tea.jpg":            "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=220&fit=crop&auto=format&q=80",
    "teh_tarik.jpg":          "https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=400&h=220&fit=crop&auto=format&q=80",
    "kopi_o.jpg":             "https://images.unsplash.com/photo-1497636577773-f1231844b336?w=400&h=220&fit=crop&auto=format&q=80",
    "iced_coffee.jpg":        "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=220&fit=crop&auto=format&q=80",
    "iced_teh.jpg":           "https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=400&h=220&fit=crop&auto=format&q=80",
    "lemon_tea.jpg":          "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=220&fit=crop&auto=format&q=80",
    "thai_iced_tea.jpg":      "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=220&fit=crop&auto=format&q=80",
    "cola.jpg":               "https://images.unsplash.com/photo-1629203432180-71b9f58e3b18?w=400&h=220&fit=crop&auto=format&q=80",
    "cola_zero.jpg":          "https://images.unsplash.com/photo-1594226801341-41427b4e5c22?w=400&h=220&fit=crop&auto=format&q=80",
    "pepsi.jpg":              "https://images.unsplash.com/photo-1531384441138-2736e62e0919?w=400&h=220&fit=crop&auto=format&q=80",
    "sprite.jpg":             "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400&h=220&fit=crop&auto=format&q=80",
    "fanta.jpg":              "https://images.unsplash.com/photo-1629203432180-71b9f58e3b18?w=400&h=220&fit=crop&auto=format&q=80",
    "water.jpg":              "https://images.unsplash.com/photo-1559839914-17aae19cec71?w=400&h=220&fit=crop&auto=format&q=80",
    "sparkling.jpg":          "https://images.unsplash.com/photo-1621263764928-df1444c5e859?w=400&h=220&fit=crop&auto=format&q=80",
    "orange_juice.jpg":       "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&h=220&fit=crop&auto=format&q=80",
    "watermelon_juice.jpg":   "https://images.unsplash.com/photo-1562547256-2c5ee93b60b7?w=400&h=220&fit=crop&auto=format&q=80",
    "mango_smoothie.jpg":     "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=400&h=220&fit=crop&auto=format&q=80",
    "sugarcane.jpg":          "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=220&fit=crop&auto=format&q=80",
    "bandung.jpg":            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=220&fit=crop&auto=format&q=80",
    "coconut.jpg":            "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=220&fit=crop&auto=format&q=80",
}

headers = {"User-Agent": "Mozilla/5.0"}
total = len(images)
ok = 0

for filename, url in images.items():
    dest = os.path.join(SAVE_DIR, filename)
    if os.path.exists(dest):
        print(f"  [skip] {filename} already exists")
        ok += 1
        continue
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(dest, "wb") as f:
                f.write(resp.read())
        print(f"  [ok]   {filename}")
        ok += 1
    except Exception as e:
        print(f"  [FAIL] {filename}: {e}")

print(f"\nDone: {ok}/{total} images saved to {SAVE_DIR}")
