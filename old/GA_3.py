import math
import numpy as np
import matplotlib.pyplot as plt
import random
import turtle
import re

truck_allpath = []
truck_path = []
max_number = []
'''这个程序可以计算出货车承重为1的多辆货车的最短路径，输入需求点和供应点坐标，以及对应的货物量，就能求出最短路径'''
for yp in range(10):

    c_rate = 0.7

    coordinates1 = np.array(
        [[677, 3817], [4509, 1407], [4995, 913], [1499, 1294], [2734, 3141], [2700, 3730], [4374, 1215], [4168, 1643],
         [1842, 4170], [742, 1570], [2130, 2102], [3043, 4790], [2706, 1356], [2220, 1358], [4577, 4417], [2361, 1860],
         [284, 2006], [516, 4201], [4312, 291], [1071, 2173], [2967, 2750], [3775, 2902], [2116, 2286], [3995, 871],
         [1732, 532], [82, 1009], [4387, 1882], [1410, 4793], [2197, 4683], [3928, 2729], [3839, 2965], [2833, 4056],
         [569, 1859], [1724, 2066], [3655, 3042], [3129, 4734], [1728, 1122], [4474, 4016], [443, 3143], [3302, 2319],
         [4842, 1429], [1092, 3090], [1586, 1367], [3842, 1897], [1276, 4106], [1764, 3626], [2021, 4553], [431, 4190],
         [1315, 1251], [295, 1353], [393, 2866], [4251, 387], [1879, 1120], [1715, 2760], [4855, 1215], [384, 174],
         [4208, 269], [631, 1093], [2029, 1978], [3330, 4372], [2718, 2484], [4480, 3294], [4826, 3456], [3457, 23],
         [2449, 2563], [390, 4844], [4858, 4148], [1757, 3050], [540, 1430], [1739, 2575], [3551, 904], [4773, 1232],
         [2796, 4313], [195, 4761], [3165, 2833], [800, 2586], [1978, 3532], [4105, 4212], [202, 852], [4372, 3286],
         [3666, 3147], [4954, 2526], [3888, 4395], [1262, 2337], [1654, 2379], [3802, 4694], [2295, 3471], [4164, 2257],
         [551, 39], [3050, 4785], [1172, 4790], [1371, 3117], [736, 36], [682, 2463], [2042, 4230], [2241, 1852],
         [531, 2641], [2576, 1978], [3779, 938], [2946, 4847], [3562, 178], [3011, 4640], [3940, 2062], [2588, 2670],
         [3621, 1470], [2186, 1717], [3771, 347], [877, 1809], [2879, 1906], [3961, 1831], [544, 1860], [131, 3786],
         [4858, 672], [935, 1122], [1610, 4706], [2266, 4571], [1471, 4822], [3552, 4506], [4309, 3394], [4148, 1613],
         [4360, 647], [2858, 2631], [721, 2736], [4006, 4602], [1248, 86], [2831, 1050], [3857, 829], [3411, 1736],
         [40, 2157], [3903, 3437], [4014, 1865], [2594, 3043], [3322, 4400], [1966, 509], [1217, 491], [1229, 1482],
         [3431, 4919], [4019, 3024], [829, 4965], [352, 2890], [1200, 4796], [3215, 1812], [1032, 2706], [869, 3096],
         [497, 4921], [4892, 2033], [1486, 4200], [757, 152], [608, 3699], [2074, 3392], [4663, 2483], [87, 278],
         [908, 127], [4582, 1598], [3861, 3432], [3518, 3034], [1628, 647], [4938, 3408], [3798, 1635], [4932, 4328],
         [3540, 3578], [1701, 2877], [444, 3012], [1173, 1258], [4844, 1673], [1788, 4684], [2542, 996], [1997, 3799],
         [4040, 4657], [2884, 4579], [2155, 2341], [4372, 3071], [552, 4], [2545, 2857], [3818, 3511], [1207, 4325],
         [4829, 526], [1060, 3372], [3011, 1962], [2573, 4722], [3160, 4024], [3066, 430], [4802, 3126], [3827, 2222],
         [3047, 4255], [1851, 1114], [1481, 4350], [2204, 1866], [906, 1405], [1230, 1396], [2833, 3632], [447, 4705],
         [3238, 1045], [4587, 4846], [1307, 239], [4513, 4738], [3870, 2773], [1271, 4465], [4412, 4319], [4875, 2103],
         [303, 4009], [1917, 316], [4408, 4776], [735, 1509], [1469, 2181], [1490, 4345], [2994, 1522], [4575, 3185],
         [3778, 3039], [757, 4427], [3964, 3559], [2185, 1713], [493, 3087], [3813, 612], [2796, 2246], [3276, 1666],
         [4365, 1847], [1359, 4150], [213, 2812], [2129, 2162], [224, 2477], [3618, 3373], [1573, 4500], [1466, 2726],
         [3164, 3100], [777, 1956], [2610, 3231], [4238, 4706], [3546, 3621], [3175, 1383], [439, 4944], [3698, 4765],
         [2744, 4086], [439, 700], [4980, 264], [1103, 3787], [2743, 1041], [1441, 4234], [4960, 778], [3385, 4311],
         [4077, 2352], [2986, 2967], [4979, 2043], [4707, 4429], [265, 652], [3872, 3524], [4551, 1061], [1494, 3615],
         [1582, 1125], [3545, 769], [3283, 229], [1279, 3526], [303, 460], [4994, 1209], [4326, 2754], [869, 3193],
         [774, 4236], [1158, 4632], [1200, 3277], [2248, 2015], [3807, 3143], [2854, 2237], [1176, 3690], [1839, 752],
         [1804, 4334], [4911, 1541], [2966, 3259], [1100, 3782], [3930, 3525], [3252, 3593], [2660, 2442], [3830, 657],
         [4514, 4007], [4383, 834], [4715, 4339], [3521, 1721], [4948, 4091], [3926, 4391], [155, 1478], [3323, 4585],
         [4668, 4040], [4060, 1189], [1419, 1060], [432, 4034], [1290, 4224], [4627, 1757], [2736, 2839], [1098, 3039],
         [4663, 96], [2610, 1796], [4964, 2232], [4503, 4076], [3336, 3850], [1802, 446], [971, 8], [345, 3381],
         [1513, 3207], [1571, 851], [3213, 3650], [1226, 179], [4706, 2735], [2800, 1524], [2577, 1669], [4315, 856],
         [2647, 4936], [594, 2662], [1173, 716], [4837, 2097], [2116, 3220], [1003, 3966], [2220, 4052], [964, 1738],
         [2788, 2824], [940, 4473], [175, 1991], [2752, 495], [848, 969], [3017, 3145], [1470, 1903], [1790, 3712],
         [1270, 580], [4228, 3859], [3218, 2500], [825, 4541], [2764, 3179], [272, 235], [4794, 4739], [1329, 216],
         [4608, 575], [2741, 507], [4037, 3927], [1514, 56], [3838, 1669], [1217, 2235], [1974, 3081], [2511, 1352],
         [1210, 4252], [2774, 450], [3423, 442], [124, 1069], [3552, 4477], [1901, 396], [4681, 3531], [1097, 4144],
         [2725, 4126], [440, 2421], [3557, 3037], [1849, 1280], [415, 3466], [4506, 2096], [636, 2333], [205, 3888],
         [991, 4883], [1672, 3168], [2284, 581], [3027, 4080], [3510, 2057], [1571, 321], [4718, 3292], [3503, 1662],
         [24, 4389], [1621, 3823], [2082, 415], [4814, 2397], [3490, 1626], [4947, 1114], [2879, 2468], [3133, 2473],
         [847, 4915], [3153, 910], [851, 2655], [852, 1222], [378, 3516], [4354, 2227], [2165, 1622], [2603, 638],
         [1174, 2257], [2380, 2632], [1745, 2575], [4620, 3055], [3885, 1568], [4049, 2408], [917, 2594], [1835, 1124],
         [3250, 3675], [4067, 517], [2632, 1510], [3351, 42], [3197, 2709], [4998, 2021], [3948, 2744], [4763, 4739],
         [4179, 177], [527, 4513], [2948, 2449], [2455, 3339], [3951, 971], [533, 3564], [4476, 2978], [3243, 2482],
         [3985, 2572], [4510, 2354], [1769, 1137], [2467, 2580], [1314, 3124], [2167, 4803], [2195, 1508], [629, 499],
         [4760, 768], [2683, 3614], [1752, 3273], [3301, 1056], [1834, 2244], [4302, 3052], [4684, 3888], [2524, 1837],
         [3030, 4035], [4561, 4721], [3685, 689], [3759, 4599], [249, 3169], [4103, 4139], [3659, 3218], [3195, 3444],
         [848, 231], [4074, 2877], [873, 1103], [870, 4216], [3462, 2467], [3954, 2677], [2351, 2133], [318, 4328],
         [3998, 4459], [4509, 4939], [3240, 2924], [3963, 2602], [135, 2538], [1520, 1247], [1586, 3065], [3713, 746],
         [2001, 2217], [1905, 3651], [3629, 1278], [4362, 2602], [1339, 10], [2890, 1775], [438, 4528], [983, 834],
         [4721, 3170], [1153, 4991], [2136, 2788], [3132, 2485], [1700, 1534], [1196, 3636], [586, 4626], [3270, 1828],
         [3104, 4485], [2509, 2706], [3359, 1243], [4657, 3253], [2512, 4388], [980, 23], [814, 2524], [279, 3085],
         [2895, 2552], [935, 334], [4505, 2943], [2601, 1724], [1480, 3734], [584, 492], [4446, 1570], [2325, 4356],
         [348, 986], [2562, 3061], [660, 4833], [4850, 3771], [1825, 4327], [539, 4893], [3554, 3481], [2912, 1325],
         [2870, 3347], [2404, 4982], [4436, 4646], [4336, 3836], [3386, 3021], [676, 1415], [3569, 4110], [717, 1216],
         [683, 4002], [2137, 103], [1513, 128], [385, 2301], [3471, 1546], [1880, 2830], [3836, 1793], [2510, 1539],
         [2243, 4228], [763, 3869], [3093, 1313], [4120, 1094]])  # 需求地坐标

    coordinates2 = np.array(
        [[3014, 1972], [2860, 4324], [4860, 12], [1898, 4416], [3190, 2237], [458, 2004], [3591, 2343], [3706, 1537],
         [2802, 4435], [2435, 623], [4291, 1380], [333, 531], [1121, 287], [890, 271], [4124, 2542], [2722, 1671],
         [3702, 2980], [1484, 3008], [765, 728], [1111, 4906], [3862, 3830], [4397, 2019], [3069, 3322], [123, 2157],
         [1840, 1822], [1634, 3638], [2107, 4675], [1123, 2801], [811, 1972], [137, 3927], [141, 4284], [1350, 2044],
         [3869, 1211], [4968, 3832], [4414, 1546], [3858, 3341], [1499, 735], [4530, 875], [4925, 929], [2272, 2992],
         [2330, 2672], [2191, 2541], [4413, 677], [1966, 3412], [2108, 796], [1516, 1715], [3760, 2349], [3275, 4385],
         [2910, 3629], [2176, 2622], [3927, 3298], [3804, 3377], [3266, 3507], [3812, 1680], [2368, 1154], [3842, 817],
         [1364, 2415], [1470, 496], [2620, 587], [3029, 4178], [2791, 4154], [3444, 3490], [4255, 2945], [878, 2019],
         [4206, 3954], [2700, 517], [2480, 2032], [3756, 1635], [308, 1017], [3920, 779], [2856, 2570], [1450, 1602],
         [4336, 3299], [3654, 738], [150, 2923], [4995, 4621], [642, 3704], [4483, 4976], [1649, 1324], [1105, 2745],
         [1288, 572], [4729, 2329], [3493, 1374], [4321, 2418], [4832, 3400], [21, 849], [3509, 3328], [3975, 4574],
         [117, 2718], [4199, 2131], [2753, 4630], [1216, 4001], [2230, 1835], [3545, 4241], [1490, 4210], [3505, 2604],
         [828, 2343], [1715, 3772], [2835, 1221], [2983, 111], [2209, 2637], [4647, 3127], [775, 2494], [2439, 3459],
         [4691, 1640], [3771, 4411], [3659, 1375], [2571, 4186], [1890, 4680], [92, 4759], [4916, 2427], [4254, 3481],
         [3177, 2020], [4900, 3150], [2590, 1441], [2566, 132], [3569, 2465], [2642, 1445], [1314, 999], [2408, 2168],
         [2586, 4410], [1620, 56], [527, 1610], [2582, 47], [838, 1887], [988, 2454], [1284, 3347], [663, 1067],
         [3001, 1365], [3816, 4281], [3723, 494], [2051, 4633], [4669, 433], [2682, 4881], [485, 3333], [3939, 812],
         [3098, 768], [3690, 4387], [3078, 4292], [2538, 45], [1307, 275], [1983, 147], [4551, 4662], [4076, 4929],
         [1095, 1584], [912, 3754], [3724, 517], [1067, 4934], [1254, 4014], [1571, 2520], [4623, 3253], [4656, 2715],
         [3397, 3255], [3865, 8], [3858, 1616], [2416, 3880], [306, 3725], [2003, 4527], [3205, 2855], [2874, 571],
         [855, 837], [1230, 4049], [1521, 1629], [4015, 1527], [2652, 4949], [4287, 2636], [3113, 2920], [1159, 3921],
         [1350, 2967], [708, 1998], [2014, 915], [4665, 588], [3216, 1392], [1750, 490], [2446, 3365], [2145, 1681],
         [3309, 1151], [18, 338], [1205, 2979], [1137, 1048], [1882, 2288], [4083, 1822], [387, 4725], [1456, 270],
         [2944, 2228], [214, 4369], [4106, 4717], [1623, 91], [110, 2644], [3109, 293], [3919, 154], [4435, 3341],
         [1404, 1779], [78, 2045], [119, 1519], [2013, 969], [1772, 3524], [3503, 3407], [855, 3346], [1616, 3371],
         [2031, 3523], [3748, 2901], [4583, 1162], [3235, 4978], [4202, 1826], [3809, 2030], [1574, 790], [4131, 4835],
         [1449, 2409], [4450, 2529], [3240, 141], [647, 4672], [3104, 2372], [2286, 2599], [1506, 89], [3166, 1649],
         [2070, 1654], [2499, 3971], [4952, 3096], [3137, 2420], [2103, 1793], [3574, 2], [2268, 1683], [2902, 1652],
         [1904, 1910], [3473, 4724], [1881, 1378], [2676, 3632], [2233, 2128], [1902, 937], [3139, 1014], [4793, 1425],
         [664, 1789], [2374, 4009], [3825, 834], [971, 2855], [2200, 1982], [3730, 1140], [48, 1267], [4491, 696],
         [4011, 1744], [1863, 2263], [2928, 23], [181, 1457], [4500, 3100], [1273, 2123], [1910, 4284], [288, 3713],
         [3471, 106], [1821, 989], [3975, 2245], [3667, 4805], [3100, 3467], [3850, 863], [3021, 4775], [4056, 4652],
         [1720, 2576], [1400, 4680], [4341, 1277], [1373, 3777], [3922, 3197], [4844, 916], [2454, 1245], [2048, 3336],
         [1570, 3445], [2294, 2354], [1392, 1033], [2630, 1312], [2097, 2996], [3859, 3396], [260, 4548], [4294, 2974],
         [3174, 1347], [78, 1787], [3400, 546], [1263, 2284], [3441, 2057], [775, 3174], [1473, 70], [2632, 1386],
         [2771, 1493], [1450, 4469], [2048, 1475], [3534, 294], [4133, 3250], [4193, 4877], [1959, 1903], [2179, 446],
         [4312, 4003], [4018, 1045], [24, 3830], [1235, 4251], [2378, 3693], [3226, 1407], [341, 1810], [2045, 1501],
         [2607, 3791], [2861, 3849], [1143, 4493], [400, 2803], [2225, 1654], [2249, 2650], [2856, 667], [4313, 2632],
         [321, 4502], [1, 2327], [4088, 4034], [2443, 4666], [3694, 4877], [3561, 1445], [925, 2191], [3500, 3912],
         [1219, 1316], [4720, 2765], [4936, 238], [3801, 480], [2571, 218], [2160, 1974], [1699, 3179], [862, 1320],
         [3916, 176], [426, 1434], [429, 4833], [875, 4356], [1540, 3214], [1134, 1114], [747, 3266], [3602, 3835],
         [2514, 2017], [2346, 866], [4487, 3038], [4396, 3523], [4006, 2875], [553, 1917], [4738, 1939], [2433, 297],
         [1686, 1356], [4638, 1899], [3644, 3503], [3206, 4366], [3998, 2751], [487, 1511], [1899, 3992], [2085, 2088],
         [3213, 579], [2765, 4336], [2984, 3454], [2162, 4985], [1155, 2], [706, 3919], [1420, 1177], [1957, 3051],
         [1951, 3012], [4562, 622], [2776, 127], [3035, 3030], [4160, 1199], [2272, 3307], [2814, 3692], [881, 1916],
         [1653, 3309], [3593, 1154], [56, 2545], [1636, 1820], [2900, 3517], [3702, 2734], [4452, 1212], [1477, 4815],
         [3780, 2546], [2280, 3607], [3140, 1000], [1923, 4098], [1156, 3637], [3802, 1125], [3672, 454], [4616, 3977],
         [1053, 4234], [4578, 3587], [3271, 1492], [1576, 3063], [3158, 2541], [1585, 3507], [1571, 3149], [2109, 4279],
         [4416, 3872], [2898, 919], [2996, 419], [4896, 2905], [2752, 4922], [3445, 699], [1883, 71], [4357, 591],
         [4711, 3178], [416, 3816], [2322, 724], [3119, 4137], [974, 3751], [621, 4989], [1573, 2788], [2586, 1953],
         [1538, 2138], [3041, 3294], [4112, 846], [4510, 2242], [3082, 312], [3849, 2154], [2373, 304], [701, 3895],
         [1792, 2899], [534, 2720], [3940, 472], [426, 4688], [814, 461], [960, 20], [1208, 169], [1551, 822],
         [1500, 2595], [743, 3624], [4522, 329], [3701, 967], [43, 4433], [1680, 3804], [2666, 3956], [4242, 3045],
         [4921, 3002], [4971, 1359], [3595, 2474], [3763, 4071], [4258, 1730], [2912, 24], [2126, 1827], [3952, 3889],
         [3792, 3690], [2732, 2202], [1017, 972], [2281, 604], [2949, 3437], [4761, 2656], [888, 3973], [1799, 2642],
         [2161, 4196], [1506, 1867], [2520, 4827], [2319, 4245], [2714, 4208], [4169, 2235], [684, 2750], [3052, 724],
         [3693, 372], [946, 4024], [1252, 1458], [3189, 1103], [2211, 330], [3563, 4959], [2701, 526], [3710, 1436],
         [4256, 2982], [2348, 4481], [2942, 3784], [4207, 4293], [3558, 1641], [3038, 2438], [1812, 4011], [3018, 4539],
         [2509, 2968], [447, 718], [1498, 3671], [2205, 3485], [596, 1510], [226, 4885], [515, 3620], [478, 1493],
         [4368, 1062], [2955, 691], [71, 1721], [2441, 647], [4753, 4776], [1605, 4683], [3538, 305], [3272, 3718],
         [294, 2052], [2243, 689], [1171, 1654], [1323, 2138], [268, 3903], [4930, 3544], [4486, 1196], [4429, 762],
         [3332, 1513], [2380, 2642], [4949, 3774], [4443, 2745], [2468, 2793], [1994, 4816], [2012, 3579], [4096, 4377],
         [66, 589], [218, 904], [3574, 4230], [2631, 4654]])  # 供应地坐标

    coordinates1goods = []
    coordinates2goods = []


    def data():
        for i in range(len(coordinates1)):
            coordinates1goods.append(1)  # 首先生成两个个禁忌表，用遗传求出tsp
        for i in range(len(coordinates2)):
            coordinates2goods.append(1)


    data()

    truck_coordinates = [[4292, 4798, 1]]


    class Truck:
        def __init__(self, x, y):
            self.x = x
            self.y = y  # 起点设置为（0，0）
            self.lat_x = 0
            self.lat_y = 0
            self.goto = 0
            self.flag = 0  # 用来计数画图次数
            self.drivedistance = 0.0
            self.goal = "供应地"
            self.goods = 0
            self.buff = "待命"
            self.lujing = []
            self.drawpath = [[x, y]]
            self.lastdrive = 0
            self.current_capacity = 0  # 当前运载的货量

        def __str__(self):
            return '坐标: [{},{}],{}：{}当前运载的货量: {} 总共走了{}距离 正在前往{} 已经装运{}'. \
                format(self.x, self.y, self.buff, self.goto, self.current_capacity, self.drivedistance, self.goal,
                       self.goods)


    def lenth(x1, y1, x2, y2):
        return math.sqrt((int(x1) - int(x2)) ** 2 + (int(y1) - int(y2)) ** 2)  # 用于计算路径表


    def paixudistmat(distmat):  # 返回一个最近坐标表
        p = []
        # print(distmat[n].items())
        a = sorted(distmat.items(), key=lambda x: x[1])
        # print(a)
        for i in range(len(a)):
            p.append(a[i])
        return p


    def sousuodistance(listone):  # 输入的是一组路径   返回路径长度
        def soushuo(text, listone, i):
            distance = 0
            op = int(re.findall("\d+", listone[i])[0])
            op2 = int(re.findall("\d+", listone[i + 1])[0])
            # print(re.findall("\d+",listone[i])[0])
            # print(op)
            # print(op2)
            if (text == "到达供应地"):
                listtwo = checklist2(op)
                # print(listtwo)
                for j in range(len(listtwo)):
                    if (op2 == listtwo[j][0]):  # 利用正则表达式比较地点
                        distance = listtwo[j][1]
                        # print(distance)
                return distance

            if (text == "到达需求地"):
                listtwo = checklist1(op)
                # print(listtwo)
                for j in range(len(listtwo)):
                    if (op2 == listtwo[j][0]):  # 利用正则表达式比较地点
                        distance = listtwo[j][1]
                        # print(distance)
                return distance

        distance = 0
        for i in range(len(listone) - 1):
            if (listone[i][0:5] == "到达供应地"):
                distance += soushuo("到达供应地", listone, i)

            if (listone[i][0:5] == "到达需求地"):
                distance += soushuo("到达需求地", listone, i)
            # print(distance)
        return distance


    def checklist1(checknum):  # 最近供应地坐标
        list = []
        num = []
        for i in range(len(coordinates2)):
            list.append(
                lenth(coordinates1[checknum][0], coordinates1[checknum][1], coordinates2[i][0], coordinates2[i][1]))
        for i in range(len(coordinates2)):
            num.append(i)
        k = dict(zip(num, list))
        op = paixudistmat(k)
        return op


    totallist1 = []
    for i in range(len(coordinates1)):
        totallist1.append(checklist1(i))


    def checklist2(checknum):  # 最近需求地坐标
        list = []
        num = []
        for i in range(len(coordinates1)):
            list.append(
                lenth(coordinates2[checknum][0], coordinates2[checknum][1], coordinates1[i][0], coordinates1[i][1]))
        for i in range(len(coordinates1)):
            num.append(i)
        k = dict(zip(num, list))
        op = paixudistmat(k)
        return op


    totallist2 = []
    for i in range(len(coordinates2)):
        totallist2.append(checklist2(i))


    def check(text, checknum, totallist1, totallist2):
        if (text == "查找最近的供应地"):
            s = 0
            min = totallist1[checknum][0]
            for i in range(len(coordinates2)):
                if coordinates2goods[totallist1[checknum][i][0]] > 0:
                    s = totallist1[checknum][i][0]
                    min = totallist1[checknum][i][1]
                    return (s, min)

        if (text == "查找最近的需求地"):
            s = 0
            min = totallist2[checknum][0]
            for i in range(len(coordinates1)):
                if coordinates1goods[totallist2[checknum][i][0]] > 0:
                    s = totallist2[checknum][i][0]
                    min = totallist2[checknum][i][1]
                    return (s, min)


    # print(check("查找最近的需求地",0,totallist1,totallist2)) #      第一个参数是（查找） 第二个参数是 当前点序号  之后参数固定

    def jisuan(num):
        list = []
        for i in range(len(coordinates2)):
            # print(car_init[num].x,car_init_init[num].y, coordinates2[i][0],coordinates2[i][1])
            list.append(lenth(car_init[num].x, car_init[num].y, coordinates2[i][0], coordinates2[i][1]))
        # print(list)
        s = 0
        min = list[0]
        for i in range(len(coordinates2)):
            if list[i] < min:
                s = i
                min = list[i]
        return (s, min)  # 返回一个最小距离的下标和距离


    car_init = []
    for i in range(len(truck_coordinates)):
        car_init.append(Truck(truck_coordinates[i][0], truck_coordinates[i][1]))

    for i in range(len(truck_coordinates)):  # 给卡车初始化
        car_init[i].goto = jisuan(i)[0]
        coordinates2goods[car_init[i].goto] = 0
        car_init[i].drivedistance = jisuan(i)[1]
        car_init[i].x = coordinates2[car_init[i].goto][0]
        car_init[i].y = coordinates2[car_init[i].goto][1]
        car_init[i].drawpath.append([car_init[i].x, car_init[i].y])
        car_init[i].goal = "需求地"
        car_init[i].current_capacity = 1
        car_init[i].buff = "到达供应地"
        car_init[i].lujing.append(str(car_init[i].buff) + str(car_init[i].goto))
        print(car_init[i])


    def transport():
        def yusong2():
            op = check("查找最近的供应地", car_init[i].goto, totallist1, totallist2)
            car_init[i].lat_x = car_init[i].x
            car_init[i].lat_y = car_init[i].y
            car_init[i].x = coordinates2[op[0]][0]
            car_init[i].y = coordinates2[op[0]][1]
            # print(car_init[i].x,car_init[i].y)
            car_init[i].goto = op[0]
            car_init[i].buff = "到达供应地"
            car_init[i].goal = "需求地"
            car_init[i].lujing.append(str(car_init[i].buff) + str(car_init[i].goto))
            car_init[i].drawpath.append([car_init[i].x, car_init[i].y])  # 添加卡车走过的坐标
            car_init[i].drivedistance += op[1]
            car_init[i].lastdrive = op[1]
            coordinates2goods[op[0]] -= 1
            car_init[i].goods += 1
            # print(car_init[i])

        def yusong1():
            op = check("查找最近的需求地", car_init[i].goto, totallist1, totallist2)
            car_init[i].lat_x = car_init[i].x
            car_init[i].lat_y = car_init[i].y
            car_init[i].x = coordinates1[op[0]][0]
            car_init[i].y = coordinates1[op[0]][1]
            car_init[i].goto = op[0]
            car_init[i].buff = "到达需求地"
            car_init[i].goal = "供应地"
            car_init[i].lujing.append(str(car_init[i].buff) + str(car_init[i].goto))
            car_init[i].drawpath.append([car_init[i].x, car_init[i].y])
            car_init[i].drivedistance += op[1]
            car_init[i].lastdrive = op[1]
            coordinates1goods[op[0]] -= 1
            # print(car_init[i])

        while (True):
            if (max(coordinates1goods)) == 0:
                return 0
            elif (max(coordinates2goods) == 0):
                return 0

            for i in range(len(truck_coordinates)):  # 开始送货
                if (car_init[i].goal == "需求地"):
                    if (max(coordinates1goods) == 0):
                        return 0
                    elif (max(coordinates2goods) == 0):
                        return 0
                    yusong1()
                    yusong2()


    def drawpicture(p):
        color = ['b', 'g', 'r', 'c']
        flt = plt.figure()
        ax = flt.add_subplot(1, 1, 1)
        ax.set_xticks([0, 50, 100, 150, 200, 250, 5000])
        ax.set_yticks([0, 50, 100, 150, 200, 250, 5000])
        for i in range(len(coordinates1)):
            plt.plot(coordinates1[i][0], coordinates1[i][1], 'r', marker='o')  # 红色 需求点坐标为o
        for i in range(len(coordinates2)):
            plt.plot(coordinates2[i][0], coordinates2[i][1], 'b', marker='>')  # 蓝色 供应点坐标为>
        for i in range(len(truck_coordinates)):
            plt.plot(truck_coordinates[i][0], truck_coordinates[i][1], 'black', marker='1')  # 黑色 汽车初始位置
        for j in range(len(car_init[p].drawpath) - 1):
            plt.plot((car_init[p].drawpath[j][0], car_init[p].drawpath[j + 1][0]),
                     (car_init[p].drawpath[j][1], car_init[p].drawpath[j + 1][1]), color[p % 4])
        plt.title('car_init: ' + str(p), fontsize=30)
        # plt.title(r'$hello\ world$', fontsize=30)
        plt.show()
        plt.close()


    def drawpicture2(p):
        t = []
        colors = ["green", "blue", "red", "orange", "purple"]
        name = ["classic", "arrow", "square", "circle", "turtle", "triangle"]
        t1 = turtle.Pen()
        t1.speed(1)
        for i in range(len(coordinates1)):
            t1.penup()
            t1.goto(coordinates1[i][0], coordinates1[i][1])
            t1.write("需求地" + str(i), align="center", font=("Arial", 8))
            t1.dot(5, "blue")
        for i in range(len(coordinates2)):
            t1.goto(coordinates2[i][0], coordinates2[i][1])
            t1.write("供应地" + str(i), align="center", font=("Arial", 8))
            t1.dot(5, "green")

        for i in range(6):
            if (i == 0):
                t1.penup()
                t1.goto(i * 50, 0)
            else:
                t1.pendown()
                t1.goto(i * 50, 0)
                t1.write('*', font=("Arial Rounded", 5, "normal"))
                t1.write(str(i * 50))

        t1.goto(0, 0)
        t1.pendown()

        for i in range(6):
            t1.goto(0, i * 50)
            t1.write('*', font=("Arial Rounded", 5, "normal"))
            t1.write(str(i * 50))
        t1.hideturtle()
        for i in range(p):
            t.append(turtle.Pen())
            t[i].shape()
            t[i].shape(name[i % 6])
            t[i].pencolor(colors[i % 5])
            t[i].speed(1)
        for i in range(p):
            if (i == 0):
                t[i + 1].hideturtle()
            flag2 = 1
            while (flag2):
                if (car_init[i].flag == 0):
                    t[i].penup()
                    t[i].hideturtle()
                    t[i].goto(car_init[i].drawpath[car_init[i].flag][0], car_init[i].drawpath[car_init[i].flag][1])
                    t[i].showturtle()
                    t[i].pendown()
                    t[i].dot(5, "black")
                    car_init[i].flag += 1
                    if (car_init[i].flag >= len(car_init[i].drawpath)):
                        flag2 = 0

                else:
                    angle = math.degrees(math.atan(
                        (car_init[i].drawpath[car_init[i].flag][1] - car_init[i].drawpath[car_init[i].flag - 1][1]) / (
                                    car_init[i].drawpath[car_init[i].flag][0] -
                                    car_init[i].drawpath[car_init[i].flag - 1][0])))
                    if (((car_init[i].drawpath[car_init[i].flag][1] - car_init[i].drawpath[car_init[i].flag - 1][
                        1]) <= 0 and (
                                 car_init[i].drawpath[car_init[i].flag][0] - car_init[i].drawpath[car_init[i].flag - 1][
                             0])) < 0):
                        angle = 180 + angle
                    # print(angle)
                    t[i].setheading(angle)
                    t[i].goto(car_init[i].drawpath[car_init[i].flag][0], car_init[i].drawpath[car_init[i].flag][1])
                    car_init[i].flag += 1
                    if (car_init[i].flag >= len(car_init[i].drawpath)):
                        flag2 = 0


    transport()
    for i in range(len(coordinates1goods)):
        if (coordinates1goods[i] != 0):
            car_init[0].lujing.append("到达需求地" + str(i))
            car_init[0].x = coordinates1[i][0]
            car_init[0].y = coordinates1[i][1]
            car_init[0].goods += 1
            car_init[0].drawpath.append([car_init[0].x, car_init[0].y])
            car_init[0].drivedistance += lenth(car_init[0].x, car_init[0].y,
                                               car_init[0].drawpath[len(car_init[0].drawpath) - 2][0],
                                               car_init[0].drawpath[len(car_init[0].drawpath) - 2][1])

    for i in range(len(truck_coordinates)):  # 2是汽车数量，可以统计汽车输入的个数，将其换为变量
        print("卡车：" + str(i))
        print(car_init[i])
        print(car_init[i].lujing)
        print("卡车的路径坐标表:", car_init[i].drawpath)
        print('\n')

    mintime = []
    for i in range(len(truck_coordinates)):
        mintime.append(car_init[i].drivedistance)
    print("tsp需要最短时间为：", max(mintime))

    '''for p in range(len(truck_coordinates)):          #供应点与需求点太多，画图没有意义
        drawpicture(p)'''

    '''drawpicture2(len(truck_coordinates))'''

    # print("需求地物资",coordinates1goods)
    # print("供应地物资",coordinates2goods)'''

    '''判断结束的条件是，需求地物资全为0'''

    coordinates1goods = []

    coordinates2goods = []

    data()

    truck_coordinates = [[4292, 4798, 1]]


    class Truck:
        def __init__(self, x, y, volume):
            self.x = x
            self.y = y  # 起点设置为（0，0）
            self.lat_x = 0
            self.lat_y = 0
            self.goto = 0
            self.drivedistance = 0.0
            self.involume = 0
            self.lastinvolume = 0
            self.volume = volume
            self.goal = "供应地"
            self.goods = 0
            self.buff = "待命"
            self.lujing = []
            self.drawpath = [[x, y]]
            self.lastdrive = 0
            self.current_capacity = 0  # 当前运载的货量

        def __str__(self):
            return '坐标: [{},{}],{}：{}当前运载的货量: {} 总共走了{}距离 正在前往{} 已经装运{}  汽车容量为{}/{}'. \
                format(self.x, self.y, self.buff, self.goto, self.current_capacity, self.drivedistance, self.goal,
                       self.goods, self.involume, self.volume)


    def select(text, checknum, totallist1, totallist2):  # 轮盘赌法选择目标点
        sum = 0  # 距离越远，物资越少，去的概率越低
        coordinates1Arrivable = []
        if text == "查找下一个供应地":
            for i in range(len(totallist1[checknum])):
                sum = sum + (coordinates2goods[totallist1[checknum][i][0]] / totallist1[checknum][i][1])
            for i in range(len(totallist1[checknum])):
                # print((totallist1[checknum][i][0],totallist1[checknum][i][1]))
                coordinates1Arrivable.append((totallist1[checknum][i][0], (
                            coordinates2goods[totallist1[checknum][i][0]] / totallist1[checknum][i][
                        1]) / sum))  # 元组第一个是下标，第二个是到达的概率
            # print(coordinates1Arrivable)
            r_ = 0
            ran = random.random()
            for i in range(len(coordinates1Arrivable)):
                r_ += coordinates1Arrivable[i][1]
                # print("概率",ran,r_)
                if ran < r_:  break
            return coordinates1Arrivable[i][0]

        if text == "查找下一个需求地":
            for i in range(len(totallist2[checknum])):
                sum = sum + (coordinates1goods[totallist2[checknum][i][0]] / totallist2[checknum][i][1])
            for i in range(len(totallist2[checknum])):
                # print((totallist2[checknum][i][0],totallist2[checknum][i][1]))
                # print("货物",coordinates1goods[totallist2[checknum][i][0]],"距离",totallist2[checknum][i][1])
                coordinates1Arrivable.append((totallist2[checknum][i][0], (
                            coordinates1goods[totallist2[checknum][i][0]] / totallist2[checknum][i][
                        1]) / sum))  # 元组第一个是下标，第二个是到达的概率
            # print(coordinates1Arrivable)
            r_ = 0
            ran = random.random()
            for i in range(len(coordinates1Arrivable)):
                r_ += coordinates1Arrivable[i][1]
                # print("概率",ran,r_)
                if ran < r_:  break
            return coordinates1Arrivable[i][0]


    def check(text, checknum, totallist1, totallist2, volume, carnumber):  # 根据概率进行对目标点的选择和修改（因为选择的地点物资可能会出现0）
        if (text == "查找下一个供应地"):
            s = 0
            min = totallist1[checknum][0]
            flag = 1
            while (flag == 1):
                # print("供应地物资为",coordinates2goods)
                i = select("查找下一个供应地", checknum, totallist1, totallist2)
                # print("下标为",i)
                # print("供应地物资为",coordinates2goods)
                if (coordinates2goods[i] > 0):
                    flag = 0
            s = i
            for i in range(len(totallist1[checknum])):
                if totallist1[checknum][i][0] == s:
                    min = totallist1[checknum][i][1]
            if coordinates2goods[s] >= car[carnumber].volume - volume:  # 供应物资》车载空的物资时，供应物资减去车载物资，车载物资变满
                coordinates2goods[s] -= car[carnumber].volume - volume
                # print(car[carnumber].volume-volume)
                # print("需求地物资为",coordinates2goods[s])
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume = car[carnumber].volume

            else:  # 供应物资《车载物资时，车载物资加上供应物资，供应物资为0
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume += coordinates2goods[s]
                coordinates2goods[s] = 0
                # print("需求地物资为", coordinates2goods[s])
            return (s, min)

        if (text == "查找下一个需求地"):
            s = 0
            min = totallist2[checknum][0]
            flag = 1
            while (flag == 1):
                # print("需求地物资为",coordinates1goods)
                i = select("查找下一个需求地", checknum, totallist1, totallist2)
                # print("下标为",i)
                # print("需求地物资为",coordinates1goods)
                if (coordinates1goods[i] > 0):
                    flag = 0
            s = i
            for i in range(len(totallist2[checknum])):
                if totallist2[checknum][i][0] == s:
                    min = totallist2[checknum][i][1]
            if coordinates1goods[s] >= volume:  # 需求的物资>车载物资时，需求物资减去车载物资，车载物资为0
                coordinates1goods[s] -= volume
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume = 0
            else:  # 需求的物资《车载物资时，车载物资减去需求物资，需求物资为0
                car[carnumber].lastinvolume = car[carnumber].involume
                car[carnumber].involume -= coordinates1goods[s]
                coordinates1goods[s] = 0

            return (s, min)


    # print("最近供应地",totallist1)
    # print("最近需求地",totallist2)
    # print(check("查找下一个供应地",1,totallist1,totallist2))

    def jisuan(num):
        list = []
        for i in range(len(coordinates2)):
            # print(car[num].x,car[num].y, coordinates2[i][0],coordinates2[i][1])
            list.append(lenth(car[num].x, car[num].y, coordinates2[i][0], coordinates2[i][1]))
        # print(list)
        s = 0
        min = list[0]
        for i in range(len(coordinates2)):
            if list[i] < min:
                s = i
                min = list[i]
        return (s, min)  # 返回一个最小距离的下标和距离


    def transport():
        def yusong2():
            op = check("查找下一个供应地", car[i].goto, totallist1, totallist2, car[i].involume, i)
            car[i].lat_x = car[i].x
            car[i].lat_y = car[i].y
            car[i].x = coordinates2[op[0]][0]
            car[i].y = coordinates2[op[0]][1]
            # print(car[i].x,car[i].y)
            car[i].goto = op[0]
            car[i].buff = "到达供应地"
            car[i].goal = "需求地"
            car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
            car[i].drawpath.append([car[i].x, car[i].y])  # 添加卡车走过的坐标
            car[i].drivedistance += op[1]
            car[i].lastdrive = op[1]
            car[i].goods += car[i].volume
            # print(car[i])

        def yusong1():
            op = check("查找下一个需求地", car[i].goto, totallist1, totallist2, car[i].involume, i)
            car[i].lat_x = car[i].x
            car[i].lat_y = car[i].y
            car[i].x = coordinates1[op[0]][0]
            car[i].y = coordinates1[op[0]][1]
            car[i].goto = op[0]
            car[i].buff = "到达需求地"
            car[i].goal = "供应地"
            car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
            car[i].drawpath.append([car[i].x, car[i].y])
            car[i].drivedistance += op[1]
            car[i].lastdrive = op[1]
            # print(car[i])

        while (True):
            if (max(coordinates1goods)) == 0:
                return 0
            elif (max(coordinates2goods) == 0):
                return 0

            for i in range(len(truck_coordinates)):  # 开始送货
                if (car[i].goal == "需求地"):
                    if (max(coordinates1goods) == 0):
                        return 0
                    elif (max(coordinates2goods) == 0):
                        return 0
                    yusong1()
                    yusong2()


    def cross(parent1, parent2):  # parent1是要交换的基因    函数填（当前基因，之前基因）
        """交叉p1,p2的部分基因片段"""
        # print(parent1,parent2)
        if np.random.rand() > c_rate:
            return parent1
        # print(parent1)
        # print(parent2)
        index1 = np.random.randint(0, len(parent1))
        index2 = np.random.randint(index1, len(parent1))
        tempcar1 = parent1[index1:index2]
        tempcar2 = parent2[index1:index2]  # parent2 給 parant1交叉的基因片段
        # print(tempcar1)
        # print(tempcar2)
        if (tempcar1 == tempcar2):
            return parent1
        difference1 = list(set(tempcar1) - set(tempcar2))  # 差集，在tempGen1中但不在tempGen2中的元素
        difference2 = list(set(tempcar2) - set(tempcar1))  # 差集，在tempcar2中但不在tempcar1中的元素
        # print(difference1)
        # print(parent1)
        if (len(difference1) == 0):
            return parent1

        else:
            k = 0
            for i in range(len(tempcar2)):
                parent1[index1 + i] = tempcar2[i]
                # print(parent1)
            for i in range(0, index1):
                for j in range(len(difference2)):
                    if (parent1[i] == difference2[j]):
                        if (k < len(difference1) - 1):
                            parent1[i] = difference1[k]
                            k = k + 1
            # print(parent1)
            for i in range(index2, len(parent1) - 1):
                for j in range(len(difference2)):
                    if (parent1[i] == difference2[j]):
                        if (k < len(difference1) - 1):
                            parent1[i] = difference1[k]
                            k = k + 1
            # print(parent1)
            return parent1


    def drawpicture(p):
        color = ['b', 'g', 'r', 'c']
        for i in range(len(coordinates1)):
            plt.plot(coordinates1[i][0], coordinates1[i][1], 'r', marker='o')  # 红色 需求点坐标为o
        for i in range(len(coordinates2)):
            plt.plot(coordinates2[i][0], coordinates2[i][1], 'b', marker='>')  # 蓝色 供应点坐标为>
        for i in range(len(truck_coordinates)):
            plt.plot(truck_coordinates[i][0], truck_coordinates[i][1], 'black', marker='1')  # 黑色 汽车初始位置
        for j in range(len(car[p].drawpath) - 1):
            plt.plot((car[p].drawpath[j][0], car[p].drawpath[j + 1][0]),
                     (car[p].drawpath[j][1], car[p].drawpath[j + 1][1]), color[p % 4])
        plt.title('car: ' + str(p), fontsize=30)
        # plt.title(r'$hello\ world$', fontsize=30)
        plt.show()
        plt.close()


    allmintime = []
    alllujing = []
    for up in range(200):  # 在基因跑两百次tsp与贪心父本进行交叉互换，得到较优解，然后根据货量进行重复运输，直到满足需求量，得到最终解
        global car
        car = []
        for i in range(len(truck_coordinates)):
            car.append(Truck(truck_coordinates[i][0], truck_coordinates[i][1], truck_coordinates[i][2]))

        for i in range(len(truck_coordinates)):  # 给卡车初始化
            car[i].goto = jisuan(i)[0]
            car[i].drivedistance = jisuan(i)[1]
            car[i].x = coordinates2[car[i].goto][0]
            car[i].y = coordinates2[car[i].goto][1]
            car[i].drawpath.append([car[i].x, car[i].y])
            car[i].goal = "需求地"
            car[i].current_capacity = 1
            car[i].buff = "到达供应地"
            car[i].lujing.append(str(car[i].buff) + str(car[i].goto))
            # print(car[i])

        transport()
        if (max(coordinates1goods) > 0):
            up = up - 1
        else:
            for i in range(len(truck_coordinates)):  # 2是基因数量，可以统计基因输入的个数，将其换为变量
                print("基因：" + str(i))
                print(car[i].lujing)
                print("基因的路径坐标表:", car[i].drawpath)
                print('\n')
            mintime = []
            for i in range(len(truck_coordinates)):
                alllujing.append(car[i].lujing)
                mintime.append(car[i].drivedistance)
                if (up > 1):
                    # car[i].last_drivedistance=car
                    {}
            if (max(coordinates1goods) > 0):
                up = up - 1
            allmintime.append(max(mintime))
            print("该次路径需要最短时间为：", min(allmintime))

            op = len(allmintime)
            if (op > 1):
                if (allmintime[op - 2] > allmintime[op - 1]):
                    new_lujing = cross(car_init[0].drawpath, alllujing[op - 1])
                    print("新的路径", new_lujing)
                    new_mintime = sousuodistance((new_lujing))
                    if (new_mintime < allmintime[op - 1]):
                        alllujing[op - 2] = new_mintime
        for i in range(len(truck_coordinates)):
            if (car[i].buff == "到达供应地"):
                car[i].x = car[i].lat_x
                car[i].y = car[i].lat_y
                car[i].drivedistance -= car[i].lastdrive
                car[i].lujing.pop()
                car[i].involume = car[i].lastinvolume
                car[i].drawpath.pop()

        '''for i in range(len(truck_coordinates)):                  #2是汽车数量，可以统计汽车输入的个数，将其换为变量
            print("卡车："+str(i))
            print(car[i])
            print(car[i].lujing)
            print("卡车的路径坐标表:",car[i].drawpath)
            print('\n')'''

        mintime = []
        for i in range(len(truck_coordinates)):
            mintime.append(car[i].drivedistance)
        alllujing.append(car[0].lujing)
        allmintime.append(max(mintime))

        # print("该次路径需要最短时间为：",max(mintime))
        print("该次路径需要最短时间为：", min(allmintime))

        print("\n第{}次运输\n".format(up))
        # print("需求地物资", coordinates1goods)
        # print("供应地物资", coordinates2goods)

        coordinates1 = np.array(
            [[677, 3817], [4509, 1407], [4995, 913], [1499, 1294], [2734, 3141], [2700, 3730], [4374, 1215],
             [4168, 1643], [1842, 4170], [742, 1570], [2130, 2102], [3043, 4790], [2706, 1356], [2220, 1358],
             [4577, 4417], [2361, 1860], [284, 2006], [516, 4201], [4312, 291], [1071, 2173], [2967, 2750],
             [3775, 2902], [2116, 2286], [3995, 871], [1732, 532], [82, 1009], [4387, 1882], [1410, 4793], [2197, 4683],
             [3928, 2729], [3839, 2965], [2833, 4056], [569, 1859], [1724, 2066], [3655, 3042], [3129, 4734],
             [1728, 1122], [4474, 4016], [443, 3143], [3302, 2319], [4842, 1429], [1092, 3090], [1586, 1367],
             [3842, 1897], [1276, 4106], [1764, 3626], [2021, 4553], [431, 4190], [1315, 1251], [295, 1353],
             [393, 2866], [4251, 387], [1879, 1120], [1715, 2760], [4855, 1215], [384, 174], [4208, 269], [631, 1093],
             [2029, 1978], [3330, 4372], [2718, 2484], [4480, 3294], [4826, 3456], [3457, 23], [2449, 2563],
             [390, 4844], [4858, 4148], [1757, 3050], [540, 1430], [1739, 2575], [3551, 904], [4773, 1232],
             [2796, 4313], [195, 4761], [3165, 2833], [800, 2586], [1978, 3532], [4105, 4212], [202, 852], [4372, 3286],
             [3666, 3147], [4954, 2526], [3888, 4395], [1262, 2337], [1654, 2379], [3802, 4694], [2295, 3471],
             [4164, 2257], [551, 39], [3050, 4785], [1172, 4790], [1371, 3117], [736, 36], [682, 2463], [2042, 4230],
             [2241, 1852], [531, 2641], [2576, 1978], [3779, 938], [2946, 4847], [3562, 178], [3011, 4640],
             [3940, 2062], [2588, 2670], [3621, 1470], [2186, 1717], [3771, 347], [877, 1809], [2879, 1906],
             [3961, 1831], [544, 1860], [131, 3786], [4858, 672], [935, 1122], [1610, 4706], [2266, 4571], [1471, 4822],
             [3552, 4506], [4309, 3394], [4148, 1613], [4360, 647], [2858, 2631], [721, 2736], [4006, 4602], [1248, 86],
             [2831, 1050], [3857, 829], [3411, 1736], [40, 2157], [3903, 3437], [4014, 1865], [2594, 3043],
             [3322, 4400], [1966, 509], [1217, 491], [1229, 1482], [3431, 4919], [4019, 3024], [829, 4965], [352, 2890],
             [1200, 4796], [3215, 1812], [1032, 2706], [869, 3096], [497, 4921], [4892, 2033], [1486, 4200], [757, 152],
             [608, 3699], [2074, 3392], [4663, 2483], [87, 278], [908, 127], [4582, 1598], [3861, 3432], [3518, 3034],
             [1628, 647], [4938, 3408], [3798, 1635], [4932, 4328], [3540, 3578], [1701, 2877], [444, 3012],
             [1173, 1258], [4844, 1673], [1788, 4684], [2542, 996], [1997, 3799], [4040, 4657], [2884, 4579],
             [2155, 2341], [4372, 3071], [552, 4], [2545, 2857], [3818, 3511], [1207, 4325], [4829, 526], [1060, 3372],
             [3011, 1962], [2573, 4722], [3160, 4024], [3066, 430], [4802, 3126], [3827, 2222], [3047, 4255],
             [1851, 1114], [1481, 4350], [2204, 1866], [906, 1405], [1230, 1396], [2833, 3632], [447, 4705],
             [3238, 1045], [4587, 4846], [1307, 239], [4513, 4738], [3870, 2773], [1271, 4465], [4412, 4319],
             [4875, 2103], [303, 4009], [1917, 316], [4408, 4776], [735, 1509], [1469, 2181], [1490, 4345],
             [2994, 1522], [4575, 3185], [3778, 3039], [757, 4427], [3964, 3559], [2185, 1713], [493, 3087],
             [3813, 612], [2796, 2246], [3276, 1666], [4365, 1847], [1359, 4150], [213, 2812], [2129, 2162],
             [224, 2477], [3618, 3373], [1573, 4500], [1466, 2726], [3164, 3100], [777, 1956], [2610, 3231],
             [4238, 4706], [3546, 3621], [3175, 1383], [439, 4944], [3698, 4765], [2744, 4086], [439, 700], [4980, 264],
             [1103, 3787], [2743, 1041], [1441, 4234], [4960, 778], [3385, 4311], [4077, 2352], [2986, 2967],
             [4979, 2043], [4707, 4429], [265, 652], [3872, 3524], [4551, 1061], [1494, 3615], [1582, 1125],
             [3545, 769], [3283, 229], [1279, 3526], [303, 460], [4994, 1209], [4326, 2754], [869, 3193], [774, 4236],
             [1158, 4632], [1200, 3277], [2248, 2015], [3807, 3143], [2854, 2237], [1176, 3690], [1839, 752],
             [1804, 4334], [4911, 1541], [2966, 3259], [1100, 3782], [3930, 3525], [3252, 3593], [2660, 2442],
             [3830, 657], [4514, 4007], [4383, 834], [4715, 4339], [3521, 1721], [4948, 4091], [3926, 4391],
             [155, 1478], [3323, 4585], [4668, 4040], [4060, 1189], [1419, 1060], [432, 4034], [1290, 4224],
             [4627, 1757], [2736, 2839], [1098, 3039], [4663, 96], [2610, 1796], [4964, 2232], [4503, 4076],
             [3336, 3850], [1802, 446], [971, 8], [345, 3381], [1513, 3207], [1571, 851], [3213, 3650], [1226, 179],
             [4706, 2735], [2800, 1524], [2577, 1669], [4315, 856], [2647, 4936], [594, 2662], [1173, 716],
             [4837, 2097], [2116, 3220], [1003, 3966], [2220, 4052], [964, 1738], [2788, 2824], [940, 4473],
             [175, 1991], [2752, 495], [848, 969], [3017, 3145], [1470, 1903], [1790, 3712], [1270, 580], [4228, 3859],
             [3218, 2500], [825, 4541], [2764, 3179], [272, 235], [4794, 4739], [1329, 216], [4608, 575], [2741, 507],
             [4037, 3927], [1514, 56], [3838, 1669], [1217, 2235], [1974, 3081], [2511, 1352], [1210, 4252],
             [2774, 450], [3423, 442], [124, 1069], [3552, 4477], [1901, 396], [4681, 3531], [1097, 4144], [2725, 4126],
             [440, 2421], [3557, 3037], [1849, 1280], [415, 3466], [4506, 2096], [636, 2333], [205, 3888], [991, 4883],
             [1672, 3168], [2284, 581], [3027, 4080], [3510, 2057], [1571, 321], [4718, 3292], [3503, 1662], [24, 4389],
             [1621, 3823], [2082, 415], [4814, 2397], [3490, 1626], [4947, 1114], [2879, 2468], [3133, 2473],
             [847, 4915], [3153, 910], [851, 2655], [852, 1222], [378, 3516], [4354, 2227], [2165, 1622], [2603, 638],
             [1174, 2257], [2380, 2632], [1745, 2575], [4620, 3055], [3885, 1568], [4049, 2408], [917, 2594],
             [1835, 1124], [3250, 3675], [4067, 517], [2632, 1510], [3351, 42], [3197, 2709], [4998, 2021],
             [3948, 2744], [4763, 4739], [4179, 177], [527, 4513], [2948, 2449], [2455, 3339], [3951, 971], [533, 3564],
             [4476, 2978], [3243, 2482], [3985, 2572], [4510, 2354], [1769, 1137], [2467, 2580], [1314, 3124],
             [2167, 4803], [2195, 1508], [629, 499], [4760, 768], [2683, 3614], [1752, 3273], [3301, 1056],
             [1834, 2244], [4302, 3052], [4684, 3888], [2524, 1837], [3030, 4035], [4561, 4721], [3685, 689],
             [3759, 4599], [249, 3169], [4103, 4139], [3659, 3218], [3195, 3444], [848, 231], [4074, 2877], [873, 1103],
             [870, 4216], [3462, 2467], [3954, 2677], [2351, 2133], [318, 4328], [3998, 4459], [4509, 4939],
             [3240, 2924], [3963, 2602], [135, 2538], [1520, 1247], [1586, 3065], [3713, 746], [2001, 2217],
             [1905, 3651], [3629, 1278], [4362, 2602], [1339, 10], [2890, 1775], [438, 4528], [983, 834], [4721, 3170],
             [1153, 4991], [2136, 2788], [3132, 2485], [1700, 1534], [1196, 3636], [586, 4626], [3270, 1828],
             [3104, 4485], [2509, 2706], [3359, 1243], [4657, 3253], [2512, 4388], [980, 23], [814, 2524], [279, 3085],
             [2895, 2552], [935, 334], [4505, 2943], [2601, 1724], [1480, 3734], [584, 492], [4446, 1570], [2325, 4356],
             [348, 986], [2562, 3061], [660, 4833], [4850, 3771], [1825, 4327], [539, 4893], [3554, 3481], [2912, 1325],
             [2870, 3347], [2404, 4982], [4436, 4646], [4336, 3836], [3386, 3021], [676, 1415], [3569, 4110],
             [717, 1216], [683, 4002], [2137, 103], [1513, 128], [385, 2301], [3471, 1546], [1880, 2830], [3836, 1793],
             [2510, 1539], [2243, 4228], [763, 3869], [3093, 1313], [4120, 1094]])  # 需求地坐标

        coordinates1goods = []

        coordinates2 = np.array(
            [[3014, 1972], [2860, 4324], [4860, 12], [1898, 4416], [3190, 2237], [458, 2004], [3591, 2343],
             [3706, 1537], [2802, 4435], [2435, 623], [4291, 1380], [333, 531], [1121, 287], [890, 271], [4124, 2542],
             [2722, 1671], [3702, 2980], [1484, 3008], [765, 728], [1111, 4906], [3862, 3830], [4397, 2019],
             [3069, 3322], [123, 2157], [1840, 1822], [1634, 3638], [2107, 4675], [1123, 2801], [811, 1972],
             [137, 3927], [141, 4284], [1350, 2044], [3869, 1211], [4968, 3832], [4414, 1546], [3858, 3341],
             [1499, 735], [4530, 875], [4925, 929], [2272, 2992], [2330, 2672], [2191, 2541], [4413, 677], [1966, 3412],
             [2108, 796], [1516, 1715], [3760, 2349], [3275, 4385], [2910, 3629], [2176, 2622], [3927, 3298],
             [3804, 3377], [3266, 3507], [3812, 1680], [2368, 1154], [3842, 817], [1364, 2415], [1470, 496],
             [2620, 587], [3029, 4178], [2791, 4154], [3444, 3490], [4255, 2945], [878, 2019], [4206, 3954],
             [2700, 517], [2480, 2032], [3756, 1635], [308, 1017], [3920, 779], [2856, 2570], [1450, 1602],
             [4336, 3299], [3654, 738], [150, 2923], [4995, 4621], [642, 3704], [4483, 4976], [1649, 1324],
             [1105, 2745], [1288, 572], [4729, 2329], [3493, 1374], [4321, 2418], [4832, 3400], [21, 849], [3509, 3328],
             [3975, 4574], [117, 2718], [4199, 2131], [2753, 4630], [1216, 4001], [2230, 1835], [3545, 4241],
             [1490, 4210], [3505, 2604], [828, 2343], [1715, 3772], [2835, 1221], [2983, 111], [2209, 2637],
             [4647, 3127], [775, 2494], [2439, 3459], [4691, 1640], [3771, 4411], [3659, 1375], [2571, 4186],
             [1890, 4680], [92, 4759], [4916, 2427], [4254, 3481], [3177, 2020], [4900, 3150], [2590, 1441],
             [2566, 132], [3569, 2465], [2642, 1445], [1314, 999], [2408, 2168], [2586, 4410], [1620, 56], [527, 1610],
             [2582, 47], [838, 1887], [988, 2454], [1284, 3347], [663, 1067], [3001, 1365], [3816, 4281], [3723, 494],
             [2051, 4633], [4669, 433], [2682, 4881], [485, 3333], [3939, 812], [3098, 768], [3690, 4387], [3078, 4292],
             [2538, 45], [1307, 275], [1983, 147], [4551, 4662], [4076, 4929], [1095, 1584], [912, 3754], [3724, 517],
             [1067, 4934], [1254, 4014], [1571, 2520], [4623, 3253], [4656, 2715], [3397, 3255], [3865, 8],
             [3858, 1616], [2416, 3880], [306, 3725], [2003, 4527], [3205, 2855], [2874, 571], [855, 837], [1230, 4049],
             [1521, 1629], [4015, 1527], [2652, 4949], [4287, 2636], [3113, 2920], [1159, 3921], [1350, 2967],
             [708, 1998], [2014, 915], [4665, 588], [3216, 1392], [1750, 490], [2446, 3365], [2145, 1681], [3309, 1151],
             [18, 338], [1205, 2979], [1137, 1048], [1882, 2288], [4083, 1822], [387, 4725], [1456, 270], [2944, 2228],
             [214, 4369], [4106, 4717], [1623, 91], [110, 2644], [3109, 293], [3919, 154], [4435, 3341], [1404, 1779],
             [78, 2045], [119, 1519], [2013, 969], [1772, 3524], [3503, 3407], [855, 3346], [1616, 3371], [2031, 3523],
             [3748, 2901], [4583, 1162], [3235, 4978], [4202, 1826], [3809, 2030], [1574, 790], [4131, 4835],
             [1449, 2409], [4450, 2529], [3240, 141], [647, 4672], [3104, 2372], [2286, 2599], [1506, 89], [3166, 1649],
             [2070, 1654], [2499, 3971], [4952, 3096], [3137, 2420], [2103, 1793], [3574, 2], [2268, 1683],
             [2902, 1652], [1904, 1910], [3473, 4724], [1881, 1378], [2676, 3632], [2233, 2128], [1902, 937],
             [3139, 1014], [4793, 1425], [664, 1789], [2374, 4009], [3825, 834], [971, 2855], [2200, 1982],
             [3730, 1140], [48, 1267], [4491, 696], [4011, 1744], [1863, 2263], [2928, 23], [181, 1457], [4500, 3100],
             [1273, 2123], [1910, 4284], [288, 3713], [3471, 106], [1821, 989], [3975, 2245], [3667, 4805],
             [3100, 3467], [3850, 863], [3021, 4775], [4056, 4652], [1720, 2576], [1400, 4680], [4341, 1277],
             [1373, 3777], [3922, 3197], [4844, 916], [2454, 1245], [2048, 3336], [1570, 3445], [2294, 2354],
             [1392, 1033], [2630, 1312], [2097, 2996], [3859, 3396], [260, 4548], [4294, 2974], [3174, 1347],
             [78, 1787], [3400, 546], [1263, 2284], [3441, 2057], [775, 3174], [1473, 70], [2632, 1386], [2771, 1493],
             [1450, 4469], [2048, 1475], [3534, 294], [4133, 3250], [4193, 4877], [1959, 1903], [2179, 446],
             [4312, 4003], [4018, 1045], [24, 3830], [1235, 4251], [2378, 3693], [3226, 1407], [341, 1810],
             [2045, 1501], [2607, 3791], [2861, 3849], [1143, 4493], [400, 2803], [2225, 1654], [2249, 2650],
             [2856, 667], [4313, 2632], [321, 4502], [1, 2327], [4088, 4034], [2443, 4666], [3694, 4877], [3561, 1445],
             [925, 2191], [3500, 3912], [1219, 1316], [4720, 2765], [4936, 238], [3801, 480], [2571, 218], [2160, 1974],
             [1699, 3179], [862, 1320], [3916, 176], [426, 1434], [429, 4833], [875, 4356], [1540, 3214], [1134, 1114],
             [747, 3266], [3602, 3835], [2514, 2017], [2346, 866], [4487, 3038], [4396, 3523], [4006, 2875],
             [553, 1917], [4738, 1939], [2433, 297], [1686, 1356], [4638, 1899], [3644, 3503], [3206, 4366],
             [3998, 2751], [487, 1511], [1899, 3992], [2085, 2088], [3213, 579], [2765, 4336], [2984, 3454],
             [2162, 4985], [1155, 2], [706, 3919], [1420, 1177], [1957, 3051], [1951, 3012], [4562, 622], [2776, 127],
             [3035, 3030], [4160, 1199], [2272, 3307], [2814, 3692], [881, 1916], [1653, 3309], [3593, 1154],
             [56, 2545], [1636, 1820], [2900, 3517], [3702, 2734], [4452, 1212], [1477, 4815], [3780, 2546],
             [2280, 3607], [3140, 1000], [1923, 4098], [1156, 3637], [3802, 1125], [3672, 454], [4616, 3977],
             [1053, 4234], [4578, 3587], [3271, 1492], [1576, 3063], [3158, 2541], [1585, 3507], [1571, 3149],
             [2109, 4279], [4416, 3872], [2898, 919], [2996, 419], [4896, 2905], [2752, 4922], [3445, 699], [1883, 71],
             [4357, 591], [4711, 3178], [416, 3816], [2322, 724], [3119, 4137], [974, 3751], [621, 4989], [1573, 2788],
             [2586, 1953], [1538, 2138], [3041, 3294], [4112, 846], [4510, 2242], [3082, 312], [3849, 2154],
             [2373, 304], [701, 3895], [1792, 2899], [534, 2720], [3940, 472], [426, 4688], [814, 461], [960, 20],
             [1208, 169], [1551, 822], [1500, 2595], [743, 3624], [4522, 329], [3701, 967], [43, 4433], [1680, 3804],
             [2666, 3956], [4242, 3045], [4921, 3002], [4971, 1359], [3595, 2474], [3763, 4071], [4258, 1730],
             [2912, 24], [2126, 1827], [3952, 3889], [3792, 3690], [2732, 2202], [1017, 972], [2281, 604], [2949, 3437],
             [4761, 2656], [888, 3973], [1799, 2642], [2161, 4196], [1506, 1867], [2520, 4827], [2319, 4245],
             [2714, 4208], [4169, 2235], [684, 2750], [3052, 724], [3693, 372], [946, 4024], [1252, 1458], [3189, 1103],
             [2211, 330], [3563, 4959], [2701, 526], [3710, 1436], [4256, 2982], [2348, 4481], [2942, 3784],
             [4207, 4293], [3558, 1641], [3038, 2438], [1812, 4011], [3018, 4539], [2509, 2968], [447, 718],
             [1498, 3671], [2205, 3485], [596, 1510], [226, 4885], [515, 3620], [478, 1493], [4368, 1062], [2955, 691],
             [71, 1721], [2441, 647], [4753, 4776], [1605, 4683], [3538, 305], [3272, 3718], [294, 2052], [2243, 689],
             [1171, 1654], [1323, 2138], [268, 3903], [4930, 3544], [4486, 1196], [4429, 762], [3332, 1513],
             [2380, 2642], [4949, 3774], [4443, 2745], [2468, 2793], [1994, 4816], [2012, 3579], [4096, 4377],
             [66, 589], [218, 904], [3574, 4230], [2631, 4654]])  # 供应地坐标

        coordinates2goods = []  # 供应地物资
        data()
        truck_coordinates = [[4292, 4798, 1]]

        '''for p in range(len(truck_coordinates)):         #画出最优路径
            drawpicture(p)'''

    min_time = min(allmintime)  # 最短时间
    number = np.argmin(allmintime)  # 该次趟数
    '''print("\n所有路径需要最短时间为：",min_time)
    print("此次趟数是：",number)
    print("该次路径：",alllujing[number])'''

    l1 = alllujing[int(np.argmin(allmintime))]
    lst = []
    for el in l1:
        if lst.count(el) < 1:
            lst.append(el)

    '''print(lst)
    print(len(lst))'''


    class Truck2:
        def __init__(self, x, y, volume):
            self.init = 0  # 起始出发点
            self.drivedistance = 0.0  # 行驶距离
            self.goods = 0
            self.lujing = []
            self.last_lujing = []
            self.drawpath = [[x, y]]
            self.volume = volume
            self.involume = 0  # 当前运载的货量

        def __str__(self):
            return '出发点{} 总共走了{}距离 已经装运{}'. \
                format(self.init, self.drivedistance, self.goods)


    coordinates1goods = np.array(
        [10, 8, 5, 3, 6, 7, 10, 7, 1, 1, 10, 5, 1, 8, 9, 5, 10, 5, 2, 5, 5, 3, 6, 3, 7, 1, 8, 10, 2, 10, 1, 10, 6, 10,
         6, 6, 6, 2, 3, 1, 10, 10, 8, 5, 7, 2, 3, 2, 8, 10, 4, 2, 5, 7, 1, 9, 9, 8, 4, 9, 2, 2, 1, 10, 8, 8, 3, 7, 6,
         10, 2, 3, 6, 5, 9, 5, 7, 6, 6, 9, 3, 5, 7, 3, 5, 4, 6, 5, 4, 5, 2, 5, 10, 4, 10, 9, 8, 3, 1, 4, 9, 6, 3, 3, 8,
         2, 5, 5, 6, 4, 8, 2, 1, 3, 9, 5, 5, 2, 2, 5, 9, 6, 3, 5, 6, 5, 5, 5, 2, 6, 4, 9, 3, 9, 10, 5, 8, 2, 2, 1, 4, 7,
         7, 8, 7, 7, 5, 6, 2, 7, 6, 1, 1, 10, 4, 7, 9, 4, 4, 1, 5, 7, 6, 3, 10, 1, 7, 9, 1, 1, 6, 9, 3, 10, 2, 3, 5, 9,
         7, 7, 5, 10, 4, 3, 3, 9, 10, 2, 9, 2, 6, 3, 8, 6, 8, 9, 8, 10, 4, 5, 2, 5, 5, 7, 9, 9, 5, 6, 3, 4, 8, 1, 6, 9,
         2, 1, 4, 3, 8, 5, 10, 9, 1, 10, 8, 4, 7, 5, 9, 5, 9, 7, 8, 3, 1, 3, 8, 1, 4, 6, 1, 1, 8, 8, 10, 7, 9, 9, 8, 1,
         5, 3, 10, 1, 1, 1, 7, 6, 1, 4, 10, 6, 3, 7, 4, 7, 4, 5, 7, 6, 5, 2, 10, 9, 8, 10, 7, 6, 5, 5, 3, 2, 2, 8, 4, 6,
         6, 2, 4, 5, 2, 8, 8, 3, 10, 9, 8, 7, 9, 3, 2, 7, 4, 7, 5, 8, 2, 10, 6, 3, 2, 2, 10, 2, 9, 8, 5, 1, 8, 10, 5, 9,
         1, 9, 5, 9, 7, 9, 2, 7, 6, 5, 6, 10, 8, 6, 9, 2, 4, 3, 7, 4, 9, 5, 5, 7, 2, 1, 2, 5, 4, 3, 3, 7, 3, 6, 2, 8, 4,
         5, 7, 1, 10, 9, 8, 4, 10, 9, 7, 1, 7, 3, 5, 10, 8, 5, 8, 9, 7, 5, 4, 4, 5, 8, 1, 9, 6, 1, 2, 6, 10, 8, 2, 9, 6,
         3, 4, 10, 7, 1, 6, 4, 6, 8, 3, 7, 8, 9, 7, 8, 9, 1, 3, 7, 10, 4, 8, 3, 9, 1, 9, 8, 7, 6, 10, 5, 3, 6, 9, 8, 4,
         2, 6, 1, 6, 3, 10, 4, 6, 1, 5, 1, 10, 4, 9, 10, 3, 9, 6, 5, 3, 4, 8, 9, 6, 9, 9, 7, 10, 6, 2, 1, 2, 6, 3, 8, 5,
         1, 5, 1, 8, 4, 5, 9, 4, 8, 3, 3, 2, 7, 8, 2, 4, 10, 4, 5, 7, 2, 7, 7, 8, 3, 4, 1, 10, 7, 6, 7, 9, 5])  # 需求地物资

    coordinates2goods = np.array(
        [2, 7, 9, 4, 10, 1, 5, 8, 7, 7, 9, 1, 8, 4, 6, 5, 2, 5, 3, 9, 7, 6, 3, 7, 1, 3, 3, 7, 5, 4, 9, 10, 2, 5, 8, 3,
         1, 8, 10, 4, 5, 1, 8, 3, 5, 5, 1, 4, 7, 1, 4, 6, 4, 10, 10, 5, 5, 4, 9, 8, 1, 10, 4, 7, 8, 7, 3, 4, 7, 6, 4, 8,
         4, 7, 9, 8, 1, 3, 5, 7, 4, 4, 4, 10, 6, 4, 2, 4, 7, 1, 2, 3, 2, 7, 2, 2, 10, 4, 3, 10, 8, 2, 10, 1, 3, 2, 9, 7,
         7, 8, 4, 4, 5, 8, 5, 9, 9, 6, 2, 6, 6, 10, 10, 8, 9, 8, 9, 5, 4, 2, 10, 10, 3, 6, 10, 7, 8, 10, 7, 1, 7, 9, 9,
         8, 9, 8, 4, 9, 4, 9, 7, 6, 9, 9, 4, 5, 4, 6, 9, 10, 5, 9, 1, 9, 9, 9, 9, 7, 5, 6, 9, 3, 4, 6, 2, 1, 2, 7, 9, 2,
         7, 8, 2, 10, 3, 8, 4, 3, 7, 6, 3, 8, 8, 3, 2, 10, 6, 3, 10, 4, 5, 7, 6, 2, 4, 6, 1, 6, 10, 6, 6, 2, 5, 9, 1, 8,
         7, 3, 9, 1, 4, 6, 5, 6, 10, 3, 5, 4, 3, 9, 9, 2, 9, 2, 8, 1, 2, 6, 8, 9, 5, 8, 2, 1, 5, 1, 10, 2, 7, 6, 8, 9,
         5, 7, 7, 3, 1, 6, 5, 6, 9, 9, 2, 2, 10, 2, 8, 3, 4, 8, 6, 8, 1, 9, 1, 3, 10, 2, 7, 2, 1, 8, 7, 4, 8, 1, 7, 3,
         6, 7, 9, 10, 7, 10, 2, 4, 3, 1, 8, 7, 3, 4, 3, 8, 4, 9, 10, 6, 9, 3, 8, 5, 3, 3, 9, 5, 8, 6, 1, 7, 9, 7, 1, 2,
         9, 5, 7, 9, 9, 10, 9, 1, 8, 2, 9, 3, 5, 10, 5, 3, 2, 2, 3, 4, 4, 5, 1, 1, 10, 1, 4, 2, 3, 10, 1, 4, 5, 4, 1, 4,
         5, 4, 2, 7, 6, 10, 8, 2, 3, 10, 8, 1, 8, 3, 6, 1, 6, 8, 3, 10, 4, 1, 4, 8, 10, 4, 7, 2, 6, 3, 7, 3, 4, 8, 8, 6,
         5, 8, 4, 10, 5, 3, 6, 6, 4, 1, 8, 2, 7, 1, 1, 4, 6, 1, 9, 2, 3, 2, 2, 9, 9, 10, 5, 3, 8, 4, 7, 9, 4, 6, 1, 5,
         10, 5, 4, 2, 1, 3, 10, 9, 8, 10, 2, 3, 6, 5, 8, 9, 7, 3, 1, 2, 1, 6, 7, 3, 3, 4, 5, 9, 3, 1, 2, 6, 8, 2, 10, 3,
         2, 10, 8, 5, 1, 4, 5, 9, 7, 7, 3, 10, 6, 10, 10, 7, 7, 1, 8, 2, 2, 1, 6, 4, 4, 5, 9, 10, 3, 5, 7, 7])  # 供应地物资

    truck_coordinates = [[4292, 4798, 2], [2403, 1155, 3], [852, 4540, 5], [411, 4568, 4], [4389, 1851, 1]]

    truck = []
    for i in range(len(truck_coordinates)):
        truck.append(Truck2(truck_coordinates[i][0], truck_coordinates[i][1], truck_coordinates[i][2]))

    # print(sousuodistance(lst))
    '''def fenge():                #直接对基因列表中的数据进行分割
        sum=0
        j=1
        for i in range(len(truck_coordinates)):
            sum+=truck_coordinates[i][2]

        length=len(alllujing[int(np.argmin(allmintime))])
        last_j=0
        for i in range(len(truck_coordinates)-1):                   #分割列表
            a=int(length*(truck_coordinates[i][2]/sum))
            for j in range(len(the_bestluing)):
                if(j<last_j):
                    continue
                if(a+last_j==j):
                    last_j = j
                    if(the_bestluing[j][0:5]=="到达需求地"):
                        last_j = j-1
                        print(truck[i].lujing)
                        print(len(truck[i].lujing)-1)
                        truck[i].lujing.pop()
                    break
                else:
                    truck[i].lujing.append(the_bestluing[j])
        for j in range(last_j,len(the_bestluing)):
            truck[i+1].lujing.append(the_bestluing[j])

        for i in range(len(truck_coordinates)):
            print("无人机",i,"路径:",truck[i].lujing)

    fenge()             #对tsp进行分割'''

    '''def transport2():
        def updata(carnumber):
            for i in range():'''


    def fengge():
        new_flag = 0
        op = len(lst) // 5
        x0 = sousuodistance(lst)
        x1 = sousuodistance(lst) // 5
        # print(op)
        for i in range(op):
            truck[0].lujing.append(lst[i])
            # print(truck[0].lujing)
        while (x1 - sousuodistance(truck[0].lujing) > 0.014 * x0):
            # print(sousuodistance(truck[0].lujing) - x1)
            i = i + 1
            truck[0].lujing.append(lst[i])
            # print(truck[0].lujing)
        while (sousuodistance(truck[0].lujing) - x1 > 0.014 * x0):
            i = i - 1
            # print(truck[0].lujing)
            truck[0].lujing.pop()
        new_flag = i

        for i in range(op):
            truck[1].lujing.append(lst[i + new_flag])
        while (x1 - sousuodistance(truck[1].lujing) > 0.014 * x0):
            i = i + 1
            truck[1].lujing.append(lst[i])
        while (sousuodistance(truck[1].lujing) - x1 > 0.014 * x0):
            i = i - 1
            truck[1].lujing.pop()
        new_flag = i

        for i in range(op):
            truck[2].lujing.append(lst[i + new_flag])
        while (x1 - sousuodistance(truck[2].lujing) > 0.014 * x0):
            i = i + 1
            truck[2].lujing.append(lst[i])
        while (sousuodistance(truck[2].lujing) - x1 > 0.014 * x1):
            i = i - 1
            truck[2].lujing.pop()
        new_flag = i

        for i in range(op):
            truck[3].lujing.append(lst[i + new_flag])
        while (x1 - sousuodistance(truck[3].lujing) > 0.014 * x0):
            i = i + 1
            truck[3].lujing.append(lst[i])
        while (sousuodistance(truck[3].lujing) - x1 > 0.014 * x0):
            i = i - 1
            truck[3].lujing.pop()
        new_flag = i

        for i in range(op):
            truck[4].lujing.append(lst[i + new_flag])

        for i in range(len(truck_coordinates)):
            print("无人机", i, "路径:", truck[i].lujing)
            print(sousuodistance(truck[i].lujing))


    # fengge()           #对路径进行分割

    def truck_transport(i):  # i为无人机编号            根据路径运输
        if (truck[i].lujing[0][0:5] == "到达供应地"):
            for k in range(len(truck[i].lujing) - 1):
                if (k % 2 == 0):
                    op1 = int(re.findall("\d+", truck[i].lujing[k])[0])
                    op2 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
                else:
                    op2 = int(re.findall("\d+", truck[i].lujing[k])[0])
                    op1 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
                if (coordinates2goods[op1] > 0 and coordinates1goods[op2] > 0):
                    if (coordinates2goods[op1] >= coordinates1goods[op2]):
                        cha = coordinates2goods[op1] - coordinates1goods[op2]
                        for k2 in range(int(coordinates1goods[op2])):
                            truck[i].last_lujing.append(truck[i].lujing[k])
                            truck[i].last_lujing.append(truck[i].lujing[k + 1])
                        coordinates2goods[op1] = cha
                        coordinates1goods[op2] = 0

                    else:
                        cha = coordinates1goods[op2] - coordinates2goods[op1]
                        for k2 in range(int(coordinates2goods[op1])):
                            truck[i].last_lujing.append(truck[i].lujing[k])
                            truck[i].last_lujing.append(truck[i].lujing[k + 1])
                        coordinates2goods[op1] = 0
                        coordinates1goods[op2] = cha
        else:
            for k in range(len(truck[i].lujing) - 1):
                if (k % 2 == 0):
                    op1 = int(re.findall("\d+", truck[i].lujing[k])[0])
                    op2 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
                else:
                    op2 = int(re.findall("\d+", truck[i].lujing[k])[0])
                    op1 = int(re.findall("\d+", truck[i].lujing[k + 1])[0])
                if (coordinates1goods[op1] > 0 and coordinates2goods[op2] > 0):
                    if (coordinates1goods[op1] >= coordinates2goods[op2]):
                        cha = coordinates1goods[op1] - coordinates2goods[op2]
                        for k2 in range(int(coordinates2goods[op2])):
                            truck[i].last_lujing.append(truck[i].lujing[k + 1])
                            truck[i].last_lujing.append(truck[i].lujing[k])
                        coordinates1goods[op1] = cha
                        coordinates2goods[op2] = 0

                    else:
                        cha = coordinates2goods[op2] - coordinates1goods[op1]
                        for k2 in range(int(coordinates1goods[op1])):
                            truck[i].last_lujing.append(truck[i].lujing[k + 1])
                            truck[i].last_lujing.append(truck[i].lujing[k])
                        coordinates1goods[op1] = 0
                        coordinates2goods[op2] = cha
        '''print(coordinates1goods)
        print(coordinates2goods)'''


    '''truck[0].lujing.append(truck[1].lujing[0])
    truck_transport(0)
    truck_transport(1)
    print(sousuodistance(truck[0].last_lujing))
    print(sousuodistance(truck[1].last_lujing))
    print(truck[0].last_lujing)
    print(truck[1].last_lujing)
    '''

    truck[0].lujing = lst
    truck_transport(0)
    '''print(sousuodistance(truck[0].last_lujing))
    print(truck[0].last_lujing)'''

    lst = truck[0].last_lujing
    truck[0].lujing.clear()
    fengge()

    '''print(sousuodistance(truck[0].lujing))
    print(sousuodistance(truck[1].lujing))
    print(sousuodistance(truck[2].lujing))
    print(sousuodistance(truck[3].lujing))
    print(sousuodistance(truck[4].lujing))'''

    distance = []
    for i in range(len(truck_coordinates)):
        distance.append(sousuodistance(truck[i].lujing))
    max_number.append(max(distance))
    # print("完成运输至少需要时间：",max(distance))

    '''for i in range(len(truck_coordinates)):
        truck_path.append(truck[i].lujing)

    truck_allpath.append(truck_path)

print("truck_path",truck_allpath)
for i in range(len(truck_coordinates)):
    print("无人机",i,"的路径为：")
    print(truck_allpath[max_number.index(min(max_number))][i])
    print(sousuodistance(truck_allpath[max_number.index(min(max_number))][i]))'''

print("完成运输至少需要时间：", min(max_number))
print(max_number.index(min(max_number)))

'''for i in range(len(max_number)):
    print(max_number[i]) '''
