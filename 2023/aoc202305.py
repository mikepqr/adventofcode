import tqdm

data = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


class RangeMap:
    def __init__(self, source, dest, length):
        self.source = source
        self.dest = dest
        self.length = length

    def __getitem__(self, key):
        i = key - self.source
        if 0 <= i < self.length:
            return self.dest + i
        else:
            raise KeyError


class Mapping:
    def __init__(self, rangemaps: list[RangeMap]):
        self.rangemaps = rangemaps

    def __getitem__(self, key):
        val = None
        for rangemap in self.rangemaps:
            try:
                val = rangemap[key]
            except KeyError:
                pass
        return val or key


def parse_block(block: str):
    rangemaps = []
    for line in block.splitlines()[1:]:
        dest, source, length = [int(token) for token in line.split()]
        rangemaps.append(RangeMap(source, dest, length))
    return Mapping(rangemaps)


def parse_input():
    blocks = data.split("\n\n")
    seeds = [int(seed) for seed in blocks[0].split(":")[1].split()]

    maps = [
        parse_block(blocks[1]),
        parse_block(blocks[2]),
        parse_block(blocks[3]),
        parse_block(blocks[4]),
        parse_block(blocks[5]),
        parse_block(blocks[6]),
        parse_block(blocks[7]),
    ]

    return seeds, maps


_, maps = parse_input()


def min_location(seeds):
    min_loc = 1e100
    for seed in tqdm.tqdm(seeds):
        print(seed)
        loc = maps[6][maps[5][maps[4][maps[3][maps[2][maps[1][maps[0][seed]]]]]]]
        min_loc = min(loc, min_loc)
    return min_loc


def part1():
    seeds, maps = parse_input()
    return min_location(seeds, maps)


def part2():
    seed_ranges, maps = parse_input()
    min_locations = []
    for i in range(0, len(seed_ranges), 2):
        min_locations.append(
            min_location(range(seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1]))
        )
    return min(min_locations)


# from multiprocessing import Pool


# def part2_multi():
#     seed_ranges, maps = parse_input()

#     min_locations = []
#     ranges = []
#     for i in range(0, len(seed_ranges), 2):
#         ranges.append(range(seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1]))
#     with Pool(10) as p:
#         min_locations = p.map(min_location, ranges)
#     print(min(min_locations))


# data = """
# seeds: 5844012 110899473 1132285750 58870036 986162929 109080640 3089574276 100113624 2693179996 275745330 2090752257 201704169 502075018 396653347 1540050181 277513792 1921754120 26668991 3836386950 66795009

# seed-to-soil map:
# 3547471595 1239929038 174680800
# 3052451552 758183681 481745357
# 0 1427884524 1775655006
# 2844087171 549819300 208364381
# 3767989253 4004864866 5194940
# 3534196909 1414609838 13274686
# 1775655006 114264781 435554519
# 4148908402 4010059806 146058894
# 2729822390 0 114264781
# 3773184193 4156118700 138848596
# 2211209525 3203539530 518612865
# 3912032789 3767989253 236875613

# soil-to-fertilizer map:
# 912405184 1056091028 152837752
# 194471272 1208928780 200072008
# 136115250 240819204 58356022
# 3502815281 3536983174 299994001
# 2321814552 2458149869 18748048
# 3173949445 2623931701 9591555
# 394543280 888648379 167442649
# 1990258415 3891640206 212931291
# 1068754270 54862533 153774684
# 1222528954 660792432 186471834
# 3340878967 3405750148 131233026
# 3472111993 3836977175 30703288
# 561985929 299175226 225501956
# 2942828492 4104571497 88527954
# 874532405 850775600 37872779
# 3031356446 3867680463 23959743
# 842350418 208637217 32181987
# 0 524677182 136115250
# 1065242936 847264266 3511334
# 2203189706 2339525023 118624846
# 1929736108 2563409394 60522307
# 3802809282 1847367009 492158014
# 1847367009 2790861223 82369099
# 2442430445 2873230322 500398047
# 3183541000 2633523256 157337967
# 3141827666 3373628369 32121779
# 787487885 0 54862533
# 3055316189 2476897917 86511477
# 2340562600 4193099451 101867845

# fertilizer-to-water map:
# 798315344 439687669 1930292
# 1174979421 2966258900 475289790
# 439687669 778614573 55925503
# 3743699694 3453541232 155280637
# 2989334775 1659556189 96021468
# 1650269211 3441548690 11992542
# 3898980331 3608821869 395986965
# 1705125292 2123762646 842496254
# 3375514705 1755577657 368184989
# 646363825 441617961 94777173
# 1662261753 1616692650 42863539
# 495613172 627863920 150750653
# 2777061135 1174979421 212273640
# 741140998 834540076 57174346
# 800245636 536395134 91468786
# 2547621546 1387253061 229439589
# 3085356243 4004808834 290158462

# water-to-light map:
# 541719462 212840988 165903288
# 3437755571 1615831015 672632835
# 1051033542 2678450187 510773217
# 243353905 378744276 104057369
# 1561806759 3801474127 134575711
# 707622750 677109833 258560892
# 2580483557 1051033542 195631857
# 0 935670725 30512917
# 347411274 482801645 194308188
# 30512917 0 127836567
# 2190497220 2288463850 389986337
# 3068589955 1246665399 369165616
# 1754579039 3936049838 66442917
# 4110388406 3616895237 184578890
# 158349484 127836567 85004421
# 2776115414 4002492755 292474541
# 1821021956 3247419973 369475264
# 1696382470 3189223404 58196569

# light-to-temperature map:
# 338228166 2812162941 77503977
# 3123877206 693964345 40932068
# 3939438903 614787731 633466
# 3301169239 2299402886 215156012
# 3516325251 499164007 115623724
# 3852145506 3365439095 87293397
# 875755064 3565078024 729889272
# 2849390436 734896413 11914872
# 2861305308 215265512 77518872
# 4220385528 2056242491 68417151
# 2221674563 3167682469 34693717
# 2765973467 292784384 83416969
# 3198884011 1699097031 22283517
# 3164809274 2889666918 34074737
# 809366712 746811285 52314986
# 4096970661 1633036395 58945085
# 3221167528 2699611924 80001711
# 697021180 3452732492 112345532
# 2059345064 799126271 162329499
# 4155915746 629494563 64469782
# 2431111524 1721380548 334861943
# 684283267 2779613635 12737913
# 440342453 2923741655 243940814
# 3634265609 961455770 217879897
# 4288802679 3202376186 6164617
# 415732143 1691981480 4798917
# 1605644336 1179335667 453700728
# 420531060 2792351548 19811393
# 3631948975 1696780397 2316634
# 2938824180 2514558898 185053026
# 215265512 376201353 122962654
# 2256368280 2124659642 174743244
# 3940072369 3208540803 156898292
# 861681698 615421197 14073366

# temperature-to-humidity map:
# 841576398 2731200418 60836938
# 1860695540 395011682 292982985
# 1518037021 3432774193 53954373
# 1786573987 2461900019 55353430
# 2940303448 1995108352 6974538
# 3014069287 1664464874 53916789
# 753139746 2190061656 88436652
# 2351822957 2925825589 209990361
# 3079884326 3498626816 37609115
# 4067060121 4186346579 108620717
# 4175680838 4102322798 3778367
# 1571991394 2415899186 46000833
# 2841627583 1157034722 22534242
# 1841927417 2517253449 18768123
# 2153678525 47765849 108568164
# 3251281674 1179568964 226737882
# 3067986076 3486728566 11898250
# 1308101633 1785172964 209935388
# 2262246689 1406306846 89576268
# 902413336 2278498308 137400878
# 1039814214 3765380846 268287419
# 45422022 156334013 238677669
# 3617672799 2612163195 119037223
# 2947277986 1718381663 66791301
# 1617992227 1495883114 168581760
# 284099691 687994667 469040055
# 4214721882 4106101165 80245414
# 2839283756 45422022 2343827
# 3117493441 2792037356 133788233
# 2864161825 2536021572 76141623
# 4179459205 4067060121 35262677
# 3736710022 3135815950 296958243
# 3478019556 2002082890 139653243
# 2610138841 3536235931 229144915
# 2561813318 2141736133 48325523

# humidity-to-location map:
# 608325534 0 231346900
# 222429954 453776854 385895580
# 3710263359 3540956206 563631409
# 1193511298 1116937854 38719102
# 1702450793 1176729484 153572024
# 1694669826 1109156887 7780967
# 0 231346900 222429954
# 1856022817 1686715664 1854240542
# 1588644556 4104587615 106025270
# 1109156887 4210612885 84354411
# 4273894768 1155656956 21072528
# 1232230400 1330301508 356414156
# """

if __name__ == "__main__":
    # print(part1())
    print(part2())
