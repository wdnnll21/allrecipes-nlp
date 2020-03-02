verbMap = {
    "Prepare":["chop","grate","mince","crush","squeeze","cut","scramble","level","pour","slice","spread","taste","blend","bread","deglaze","aerate",
               "baste","batter","beat","brush","butterfly","bone","can","chunk","chill","churn","core","clarify","congeal","cream","debone","dice","drain",
               "decorate","descale","devil","dry","ferment","mix","stir","flambe","fold","fillet","freeze","filter","garnish","grind","glaze","grease","hull","juice","julienne",
               "knead","leaven","marinate","mash","macerate","peel","pit","preserve","process","percolate","press","pulp","pare","pickle","prepare","puree","rub","refrigerate",
               "separate","sieve","sift","skewer","stuff","scoop","shred","souse","steep","skin","soak","strain","toss","thicken","whip","whisk","wash"],
    "Cook":["heat","cook","grill", "saute","sauté", "broil", "boil", "poach", "simmer", "bake","melt","fry","braise","blacken","brown","blanch","brew","barbecue","burn",
            "char-broil","coddle","caramelize","deep fry","escallop","fricassee","hard boil","microwave","pan fry","parboil","precook","pre-cook","pressure-cook", "pressure cook",
            "reduce","shirr","smoke","steam","sear","slow cook","stew","tenderize","toast","warm","roast"],
    "Combine":["add","layer","mix in","stir in","dip","bind","combine","decorate","season","drizzle","flavor","sweeten","salt","spray","sprinkle"],
    "Wait":["wait","cool","let"],
}

toolMap = {
    "knife":["chop","mince","crush","cut","chunk","bone","core","descale","peel","pit","slice","spread","skin","butterfly","pare","dice","debone"],
    "blender":["process","blend","puree","grind"],
    "grater":["grate","shred"],
    "sieve":["drain","strain","sieve","sift","filter"],
    "spoon":["mix","stir","scramble","toss","churn","scoop","mash","knead"],
    "whisk":["whisk"],
    "baster":["baste"],
    "stove":["cook","heat","fry","stew","steam","sear","saute","boil","simmer","melt","brown","poach"],
    "oven":["broil","bake","toast","tenderize","warm","roast"],
    "grill":["grill","smoke","blacken","barbecue","burn"]
}

aprimary = ["cook","heat","chop","pour","combine","add","mix","preheat","remove","set","is","are","have","repeat","use","place"]

specialCases = {"mix": "mix in", "stir": "stir in"}