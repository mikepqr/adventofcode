import itertools
import operator
import re
from dataclasses import dataclass
from typing import Literal

import tqdm

ACCEPTED = "A"
REJECTED = "R"


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int


Category = Literal["x", "m", "a", "s"]


class Predicate:
    def __init__(self, text: str):
        # weird syntax to keep type checkers happy
        self.text = text
        assert text[0] == "x" or text[0] == "m" or text[0] == "a" or text[0] == "s"
        self.category = text[0]
        self.cmp = operator.lt if text[1] == "<" else operator.gt
        self.val = int(text[2:])

    def __call__(self, part: Part) -> bool:
        return self.cmp(getattr(part, self.category), self.val)

    def __repr__(self):
        return self.text


class Rule:
    def __init__(self, text: str):
        predicate_str, self.dest = text.split(":")
        self.predicate = Predicate(predicate_str)

    def __call__(self, part: Part) -> str:
        if self.predicate(part):
            return self.dest
        else:
            raise ValueError

    def __repr__(self):
        return str(self.predicate) + "->" + self.dest


class Workflow:
    def __init__(self, text: str):
        *rule_strs, self.fallback = text.split(",")
        self.rules = [Rule(rule_str) for rule_str in rule_strs]

    def __call__(self, part: Part) -> str:
        for rule in self.rules:
            try:
                return rule(part)
            except ValueError:
                pass
        return self.fallback

    def __repr__(self):
        return ", ".join(str(rule) for rule in self.rules) + " OR " + self.fallback


class Pipeline:
    def __init__(self, workflows: dict[str, Workflow]):
        self.workflows = workflows

    def __call__(self, part: Part):
        loc = "in"
        while loc not in {ACCEPTED, REJECTED}:
            loc = self.workflows[loc](part)
        return loc


def parse_input() -> tuple[Pipeline, list[Part]]:
    workflows_str, parts_str = data.split("\n\n")
    workflows = {}
    for line in workflows_str.splitlines():
        match = re.search("(.+){(.*)}", line)
        if match:
            name, workflow_str = match.groups()
            workflows[name] = Workflow(workflow_str)
    pipeline = Pipeline(workflows)
    parts = []
    for line in parts_str.splitlines():
        parts_dict = {}
        for token in line[1:-1].split(","):
            parts_dict[token.split("=")[0]] = int(token.split("=")[1])
        parts.append(Part(**parts_dict))
    return pipeline, parts


def part1():
    pipeline, parts = parse_input()
    accepted = {part for part in parts if pipeline(part) == ACCEPTED}
    return sum(part.x + part.m + part.a + part.s for part in accepted)


def part2():
    pipeline, _ = parse_input()
    all_parts_ratings = itertools.combinations_with_replacement(range(1, 4001), 4)
    all_parts = (Part(*ratings) for ratings in all_parts_ratings)
    total = 0
    for part in tqdm.tqdm(all_parts, total=4000**4):
        if pipeline(part) == ACCEPTED:
            total += part.x + part.m + part.a + part.s


data = """
xr{a<2738:hnx,nxz}
tnx{a>2206:R,s>1050:R,a>2105:R,R}
fq{x<3126:R,x<3349:R,x<3419:A,R}
jlv{s<1423:A,R}
xfj{a<3264:jk,x<1480:R,s>371:mjg,df}
pmn{m>568:A,R}
dt{m>3711:A,R}
vpv{m<2270:A,s<2876:R,A}
dgm{x>1168:R,m<1657:R,s>321:R,A}
tm{x>569:R,m>2103:A,a>2493:R,R}
nk{x<1590:A,x>1812:xv,a<2730:A,R}
tl{m<1299:A,x<326:R,s>3596:A,R}
vth{m<777:fh,a>958:ct,a>843:gbt,xvx}
ssf{a<2461:rvl,s>709:fs,a<3031:zjr,dj}
fk{x>976:A,a<3806:zcd,vr}
zbd{s>3482:A,m>2428:R,m>2268:A,A}
dhb{x<1242:A,x<1401:A,R}
nds{m>2792:R,dtr}
plb{a>3402:nns,x<3206:R,R}
cdh{s>2417:A,a<1027:R,x<1700:A,mjt}
hrv{x<2742:A,m<881:R,x<2775:R,R}
xh{m<2283:A,a<2206:A,R}
fvk{x>703:R,m<2096:A,m<2121:A,A}
lv{a<1074:A,x<262:R,a>1749:A,R}
qhr{m>2648:R,m<2530:A,m<2581:A,R}
mv{a>3151:R,ncd}
lfd{a>3333:A,A}
ldt{s>465:A,R}
qqz{x>2634:R,x>1467:A,m>134:A,A}
fqd{m>3145:A,s>337:A,A}
hmg{m>1999:A,s<1374:R,A}
dl{s<2343:R,A}
tnh{m>635:pht,m>250:vvf,a>2919:fjp,jjx}
hlj{a>1084:R,a>1067:A,A}
mk{a>1590:R,hkr}
hsx{m>2094:R,R}
hgn{m>1281:gjd,rl}
qm{s>110:A,x<981:R,R}
mjt{m<1253:A,R}
qqv{m>892:A,R}
ffr{x>3494:A,A}
jjx{s<537:qqz,a>2880:A,a<2848:ktd,ntm}
lz{a<1367:jxb,gpr}
mq{s<2569:R,s<2602:R,x>2631:A,A}
rlq{m<1606:R,a<3436:A,s>1030:R,A}
qvn{a>524:R,a<325:R,R}
mpf{s>346:mm,R}
pnp{x>3107:R,m<849:R,R}
fj{s>942:hv,cdj}
ml{m<932:A,m<1546:R,x<2968:R,A}
jk{x<2322:A,A}
mj{x<953:R,A}
src{x<2376:R,s<827:A,R}
sn{a<2735:A,x>2229:R,m<854:R,A}
hgl{x<3535:A,s<2734:A,R}
nr{x>2220:R,x<2124:A,x<2164:A,R}
mp{a<360:A,s>3629:R,A}
dxh{x<1732:jcp,rbd}
zr{a>785:R,a<547:nb,s>1372:A,fsq}
pkb{x<2264:R,s<1389:A,s>1562:A,R}
tk{m<2503:ql,vvt}
gv{x<1976:qvj,x>3112:kfs,x>2422:pdl,A}
xxf{s>779:A,a>565:R,A}
gf{a>2608:R,s<604:R,vsq}
pf{a>1065:A,a<1012:R,R}
hmz{s>2510:A,A}
gm{a>1801:A,R}
zfv{s>2589:R,hmz}
qkg{x<2039:R,x>2076:R,A}
zk{x<1131:A,a>3242:A,a<3132:nq,A}
sjt{x<3151:A,m<960:A,a<3687:A,R}
shr{m>2072:vjv,xpf}
gq{x<1024:mpf,a<2558:jq,s<450:mpz,gf}
cxb{a<3791:R,m<3248:A,R}
vh{m>1713:A,a<2750:R,x>3327:R,R}
vdt{s<1494:rgr,s>1601:hdz,m>2652:nl,qdz}
jl{x>774:R,fmv}
rqd{x<264:R,A}
qj{x<1450:R,R}
jb{a>591:A,A}
tlk{m<2442:A,s>3144:R,R}
tb{s>3603:R,x<2380:A,A}
lvg{a<3369:A,A}
fmv{x>489:A,a>3142:R,R}
nzc{x<1699:mnj,x<2687:snj,hhm}
nqd{x>1714:A,rb}
ffh{m>2056:R,s<999:A,R}
gkn{x>2114:A,a<3264:R,a>3434:R,R}
msm{m<2250:rf,m<2318:gt,nxh}
qfn{x<2674:A,m>2446:A,R}
qv{s<1234:A,x<698:R,x<1068:A,A}
lvl{x<741:R,A}
hsl{s<1364:R,a>2539:R,A}
ltm{s<556:A,A}
hnm{a>3612:A,a<3551:A,R}
qr{a<3123:R,a>3230:A,a>3172:R,A}
qhs{x<1385:A,x>1530:R,R}
ph{m>498:A,R}
pj{m<3141:A,x<1574:R,R}
pl{s>2852:R,a>2264:R,R}
thb{x<3288:A,s>44:R,A}
cgp{a<3718:A,A}
zx{m>1249:R,R}
hrc{s>467:R,a>369:R,A}
jn{s>478:R,R}
gxl{x>542:zxb,m<1766:A,a>3709:nt,A}
hf{m<1973:mb,m>2825:clp,ctv}
mnj{m<2896:A,a>3314:R,x>1091:jnx,R}
dhk{m<1408:A,a>2612:R,m<1964:R,A}
jbd{m>3608:A,a>3246:btv,s>108:jkg,A}
fv{a<2946:vh,x>3172:hgl,A}
skj{x<968:A,R}
rzn{a>966:A,a<427:R,A}
ncd{s>1952:R,s>1807:A,A}
dmq{a<2580:lmd,a<3301:hhg,s>3227:tk,cj}
qdz{s>1558:bbf,cmd}
kjl{m<1835:R,A}
jnx{s>596:R,x>1309:A,A}
rhg{s>1291:A,x<2642:A,a>868:A,R}
hql{a>715:ctp,a<469:mr,cbs}
ps{x<1604:nn,A}
hmx{a<2596:hsl,sgs}
glx{m>963:R,s>936:R,R}
px{x<1809:R,x<1867:A,R}
hv{m>2406:zcf,s>1014:pff,A}
btv{x<3252:R,x<3747:A,m>3479:A,R}
sfq{s>1562:R,x<2043:R,x<3301:mbb,ghj}
kkt{x>3042:R,A}
bnk{x<1916:A,A}
mtf{x>542:R,A}
gsh{a<3582:R,A}
kcl{x<2873:R,R}
rg{a<1665:fdx,m>2368:dh,a>2769:msm,czv}
jt{a<721:R,m>2323:A,a>886:R,R}
pxd{m>3549:R,R}
ctv{m>2433:A,s<602:A,cmv}
ghj{x>3625:A,m>3233:A,A}
dz{s>1616:R,s>1613:A,R}
gbk{a>3908:stx,x<3498:fq,x>3832:A,R}
vg{m<2209:A,a>880:A,x>447:A,A}
fg{a<2323:A,m<2298:R,a<2374:A,R}
ql{x<2022:vk,a<3625:tb,bfq}
vjv{m>2857:cnn,x>2663:lz,x>1248:dmq,rg}
fnl{m<3214:R,R}
xxj{s>286:A,s>175:A,a<2789:R,R}
mpz{x<1276:A,m<2304:dhk,R}
cqm{m<2396:gbk,a<3913:ktj,x<3333:qhd,rq}
nnt{m<2137:tm,R}
rhx{x<586:lv,A}
ms{s>869:R,A}
fn{m<3668:A,m<3806:A,m>3934:A,A}
lmb{m>2566:xmd,x>1354:ntr,dkx}
jcp{a<3756:R,s>2919:R,x<1535:A,A}
fh{m>444:R,a<922:ng,m>153:A,R}
brr{x<2563:znz,a>3775:cqm,x>3081:vz,ttt}
mbb{a<3572:R,R}
ks{a<596:xmv,m>673:nzk,gzq}
qx{s<258:A,a<3753:A,A}
gjd{a<3341:fv,x<3247:tmd,rk}
kfs{s<2117:A,a>1508:A,a<841:A,R}
rf{m>2134:R,fvk}
qp{x<3466:A,x<3649:R,a<2300:rfh,hbg}
hz{m>2042:dbc,dmf}
qd{s>340:R,a<1978:A,mj}
hdz{s>1664:lqr,m>1721:mjq,a>3675:qgh,qhc}
zf{s<1068:jt,hmg}
hnx{x>3334:R,x>3042:R,A}
rrn{a<1958:lx,sfs}
zb{a>264:R,a>132:R,R}
bp{s>262:dzp,m<688:R,x<725:vf,A}
fx{m>1759:jhp,s>2478:mq,R}
fjk{a>2746:ps,a<2722:cpf,x>2663:xr,mgv}
mrf{m<489:A,s<528:R,s>542:A,A}
srt{a<761:A,A}
gtc{a<2510:A,a>2530:A,x<1318:A,A}
cql{x>592:A,m<1360:R,kzl}
zjv{s<3081:A,m>2334:R,x<2919:A,R}
xq{s<2228:A,s>2357:R,x>3154:R,R}
rs{m>2291:R,A}
kt{s<1049:A,s>1143:A,A}
hjf{m>732:A,s>124:xpm,zfz}
hzp{m>458:A,m>277:R,R}
lj{m>1487:hj,s<352:hdk,a>2817:tnh,fjk}
hnv{a<1695:A,s<3347:R,R}
mfh{s>232:rhc,kgr}
mt{x<3500:A,x<3798:zbd,s<3651:gb,R}
bjz{m>932:A,x>1636:cgl,hzp}
jm{x<768:pz,a>3055:jnp,nk}
vhm{s>1096:R,x>3521:R,R}
nxz{s<492:A,m<516:R,A}
cmf{m<3598:A,s>2612:hnv,x>2417:xq,bnk}
kkz{a>1384:gm,xs}
bx{m<3495:A,x>2544:R,R}
rgs{x>846:A,m>3177:R,js}
rr{x>1771:tlr,gq}
vgl{m<1481:A,R}
nz{a<1090:tlk,s>3172:R,a<2062:A,pl}
qcr{a<3136:snf,zrv}
ng{x<2253:A,m<184:R,a>833:A,A}
nb{a>503:R,m<2471:A,m<2643:A,R}
htp{m<1676:R,R}
zp{m<2524:R,x<854:cxb,x<1523:dhb,zdc}
tnf{x<3229:A,m>2582:R,x>3273:A,A}
ggm{s>1813:A,s<1775:A,a<449:xf,R}
lzb{m<2892:xfj,kl}
thp{m>2931:R,m>2459:R,R}
pdl{a<982:R,m>1681:R,a<1895:R,A}
jj{x<547:R,a>3354:skj,A}
pff{a>1674:R,m<2017:A,A}
nrx{a<630:rqd,s>330:jn,m<2657:vg,A}
bfp{s>1004:R,A}
xps{m>2596:R,A}
kxq{m<2896:rs,m>3444:dt,znv}
xj{a>3487:pm,s>3022:jm,mxs}
qvj{m<1476:A,a>1321:R,R}
qlq{s>1326:A,s<1008:A,x<3562:R,A}
lnk{x<1260:A,x>1890:A,s>1573:R,A}
hvh{a<3906:R,s<325:R,R}
bjc{s>486:R,x>1980:A,m<223:A,A}
bj{m>1311:R,A}
tjs{m>3593:rhx,rgs}
ksz{a<334:A,a<430:A,A}
hp{x<2652:R,s>238:A,A}
qf{a>3769:A,x>2594:A,R}
lp{a<3244:A,m>3198:A,s<88:A,A}
rss{s>2234:R,R}
tzg{s<2882:jfc,s<3402:bkg,a<3428:sk,mqh}
txz{m<1810:R,m>2652:R,a>3588:R,R}
pvn{a>3803:hvh,bpl}
gft{a<2913:xxj,s>431:krz,A}
qcc{x<873:R,m<587:R,R}
dbc{s>1362:A,s>992:R,m<2907:A,R}
phq{s>3117:A,a>765:R,s<2609:R,lvl}
vjd{s>571:zjn,bdm}
rvl{a>1110:zzq,x<1998:nf,x>2809:lpz,rdv}
lx{m<855:R,x>1922:ms,m>1147:dg,glx}
qgh{s<1643:xvc,s<1651:R,R}
xf{x>2654:A,a>195:A,R}
vr{x>617:R,m<396:A,s<3191:A,A}
tlr{a>2609:qfn,dm}
kg{s<242:A,A}
vk{x<1653:R,m>2231:A,A}
lsr{a>935:A,x>1110:R,s>462:A,A}
pn{m<2216:A,a<1631:A,R}
zfz{x>2899:R,s<52:R,A}
stg{a>832:R,R}
gjb{s<23:A,a<3359:R,R}
jvf{s>119:A,a>2527:A,R}
dkx{a<3212:cql,s>119:jj,x>524:psl,xb}
qtc{x<2528:A,m<385:R,A}
fjp{a<2992:kn,a<3011:dqd,m<146:R,A}
vvt{x<1894:fbs,a>3605:zbk,R}
xz{m<1515:A,A}
js{s>2570:R,A}
hpt{m>1643:R,x<884:A,m<1598:A,R}
zq{a>1969:xh,m<1614:kdf,A}
hbp{x>2963:R,A}
cpf{m<604:bjc,A}
jkg{m>3490:A,a>3111:R,m<3422:R,R}
vrd{m<2920:R,a<3288:A,A}
jfd{s>397:R,m>3282:vgc,m<3165:trj,fnl}
rh{x<2285:lks,bx}
nzp{a<3752:A,R}
fmf{a<900:bp,a<977:fp,rc}
lsb{m>2743:A,gkn}
kdp{a>707:lmq,m>3143:rh,kf}
gg{m>3476:A,m>3387:A,m<3351:R,R}
nd{m<360:A,x>3509:R,R}
cxc{a>2240:A,x<1886:A,A}
ntm{a<2861:A,R}
nqg{x>3769:A,x>3742:A,A}
tg{s<2140:A,m>2294:R,m<2193:R,R}
sx{s>237:R,A}
dg{m<1286:R,a>1656:A,m<1382:A,R}
jsn{x>3365:A,vgl}
kf{a>393:mc,m<2579:R,tfx}
bpl{m>863:A,m>467:R,A}
tz{x<668:A,A}
db{m>3088:kj,x<1576:lzs,A}
jmm{s<779:jfd,tzj}
zrv{m>1431:R,R}
php{a<1585:R,a<2226:R,A}
zcf{s<1042:R,A}
mm{x<534:A,A}
hdk{s>153:txj,nqd}
zdt{x>3687:R,kkk}
hc{x<2498:A,m>1186:A,A}
vgd{m<176:R,a<842:A,a>1015:R,A}
zh{a>561:A,s<746:A,x<2554:R,A}
zjr{a<2709:rr,lj}
lpm{s<2577:R,a>2647:A,m<2316:R,A}
smk{a>3635:R,txz}
cr{s<270:tgc,m>465:pnp,ft}
tmd{s<3028:qf,R}
cqx{x<2020:R,x>2434:A,x>2175:A,A}
xlx{s>3190:R,A}
ttt{a<3554:tkh,tkq}
jz{x<1102:R,R}
hcz{a>3152:A,m<2410:R,x>2244:A,A}
zqj{s>101:A,s>67:R,m>2989:thb,A}
kn{m>162:A,s<496:A,s<633:A,R}
qt{a<1311:A,x>1063:A,A}
sxk{a<3632:R,x<2553:R,x<2625:A,A}
xv{s>3601:R,A}
snx{x<792:R,a<1919:pq,a<2022:hq,bz}
qmg{x>3327:R,a>3626:bl,a<3496:rlq,tnf}
gz{s<940:sms,hnk}
zs{a<2803:hmx,hc}
mbz{x<1001:zf,hz}
rl{s>2922:sc,x<3395:dl,zdt}
sqx{s<144:R,a<3398:R,x>2223:A,A}
cp{m<2323:A,A}
cmg{s>1623:A,a<3759:R,a>3876:A,R}
vtp{m>2564:A,m<979:psh,x>3832:A,nv}
bq{s<2169:R,s>2329:A,R}
sxr{s>548:R,R}
vb{m<1546:bj,m>1725:A,a<3717:hpt,R}
zl{x>2548:R,m>3433:fn,A}
kbx{m>2247:A,a>606:R,s>2848:hm,A}
hr{a<3560:R,x>1405:A,m>1584:A,A}
ktd{m<167:R,R}
bk{s<362:A,s>368:R,a>3369:A,A}
vz{x>3657:vtp,s<954:gsh,s<1183:qmg,jsn}
jq{m<2577:qhs,gtc}
nf{s>712:mbz,m>1866:szx,a<647:ss,fmf}
lmq{x<2537:R,m>2563:R,s>1064:rhg,R}
znz{x<887:gxl,ffh}
bdm{s<482:A,s>535:sxr,R}
mxs{s>2254:jl,x<1103:mv,lf}
sfd{m<431:A,R}
rz{x>1978:xn,A}
lvv{x<2871:A,s<2781:A,s>3509:kkt,R}
dj{s>417:jg,a>3559:mfh,s>214:vmr,lmb}
spn{m>417:R,R}
mc{m<2406:A,m<2653:R,R}
pvm{x<2944:R,A}
zcd{a<3691:A,m<386:A,s>2946:R,R}
vvf{x>2029:ph,a>2937:tp,x<790:A,A}
vmq{a<850:A,s<3476:A,x<2359:A,A}
mb{a>3737:xmc,s<542:hnm,x>2277:R,st}
xjb{m<1846:xpv,s<268:lsb,kxq}
nt{m<2677:A,x>326:R,R}
ngf{m<1114:kkz,s>2628:zg,s<2243:qzx,sr}
tmq{m<3330:R,m>3679:rzn,gg}
qjd{a>587:bxd,s<1370:kc,s>1572:ksz,hbp}
lpz{m<2004:ks,m<2966:kr,m<3545:jmm,rqx}
rhj{m>3073:A,m>2754:R,R}
vmk{a>1591:A,m>1701:R,m<1465:R,R}
df{a>3391:R,x>2887:R,x>2143:R,R}
gdb{s>3482:R,a>3109:A,R}
sms{x>2207:R,m<524:zb,rrl}
ss{m>735:mg,x<1028:tq,s<388:sx,kpc}
kgr{x<2041:zp,a<3722:smk,m<1354:hjf,zqj}
gbt{a<904:A,a>935:R,a<917:A,A}
cmd{x<2195:A,s>1535:lvn,sjt}
lgg{s<293:A,a>3249:A,A}
trj{m<3048:R,R}
mgv{x>1466:sn,vt}
bmj{x<1748:R,A}
hhg{m>2584:gs,x<2018:qpd,a<2959:vpv,vm}
jxb{s<2968:tf,a<806:bvq,mt}
txj{a<2865:kg,hp}
prp{s<1203:A,R}
rc{s>427:pf,a<1046:A,s>181:A,hlj}
cz{a<1470:rss,a>1953:cxc,tg}
ctp{x<2600:A,s<703:pg,vn}
hg{m>1875:A,R}
tgc{s>103:R,x>2902:R,A}
xpf{a<2558:ngf,x>2202:hgn,xj}
lms{m>2763:R,x<2186:R,a<3059:A,R}
pz{m>1122:xz,s<3366:R,s<3707:gdb,A}
pb{s<3209:R,x<440:A,lpk}
jg{a>3464:hf,m>1784:nzc,vjd}
rdv{m>1536:kdp,x>2427:hql,a<735:gz,vth}
kzc{a>655:A,x>3522:hrc,R}
st{x>1014:A,s<605:R,R}
dmf{a<482:R,a<895:A,a<970:A,A}
znv{a>3379:R,m>3168:A,R}
zbk{s>3588:R,m>2703:R,x<2271:R,A}
lks{s<670:A,x<2097:A,A}
mbq{x<2183:qd,m<1342:cr,ht}
xmd{x<2331:ntg,m>3377:jbd,fm}
zln{s>1431:cgp,a<3713:hr,cgk}
ntg{s>120:A,x>1443:R,a<3366:R,R}
tzj{x<3372:prp,x>3702:xp,m>3170:R,qlq}
xs{s<2731:R,m<561:R,vmq}
tf{x<3480:A,m>2455:A,R}
rln{a>1779:xdr,R}
nn{x>822:R,x>491:R,x>227:R,R}
pm{m<866:fk,s>2803:vb,s>2416:zfv,jgv}
xnp{s>2075:A,R}
hbg{s<2746:A,x<3803:A,m<2542:A,A}
stx{s>975:R,x>3496:R,s>885:R,R}
lpk{m<2670:A,m>2794:A,R}
rgr{s<1386:hsx,zln}
dm{s<338:jvf,m>2519:zgj,ml}
hrq{m>1466:A,s<3469:zx,s>3766:A,tl}
mg{m<1308:R,dgm}
xvx{a<776:srt,a<810:vj,stg}
tkr{m<2953:R,s<1185:A,a<3952:A,A}
lf{a>3172:R,s<1944:R,A}
zbz{m>2489:mnc,a>2239:cp,a<1874:zjv,ftn}
cdj{m<2436:qtj,a<1945:pj,src}
jnp{s<3395:R,A}
lt{x<624:A,a>3655:A,R}
nrv{x<2171:zk,a>3212:plb,m>3713:hsq,dr}
tq{m<344:mgz,R}
bvq{m>2442:mp,rjz}
hhm{m<3069:R,s>570:hl,s<505:A,zj}
rqx{x>3506:ddz,vl}
hkr{s<1564:R,x>2795:A,x>2548:A,R}
tzp{x>1878:R,x<1197:bk,x>1460:A,A}
xmc{a<3841:R,m>977:R,s<520:A,R}
kpc{s>553:A,a>373:R,s>489:mrf,A}
vgc{x>3361:A,s>257:A,m>3414:A,R}
nq{x>1800:A,m>3752:A,a>3082:A,R}
fsq{s>1258:R,m<2431:A,m>2772:A,A}
ktj{x<3300:rhj,kt}
nzk{a<786:vhm,A}
tp{s>516:A,A}
mgz{s<343:R,R}
hmk{m>2242:rbh,zs}
tr{s<580:A,m>1084:A,A}
in{s>1709:shr,ssf}
fbs{m>2660:A,m<2567:R,R}
clc{m<3471:jb,s>2669:xtx,s>2279:R,R}
zgj{x<2962:A,m>3024:R,A}
ftn{s<2594:A,s<3498:A,s>3737:R,R}
nmc{s>1639:A,a>3562:R,x<2452:R,A}
ls{a<994:R,x<2713:vmk,x>3155:htp,php}
bbf{x<2285:lnk,x>2861:A,R}
lm{x>2624:R,A}
rfh{a<1918:A,s<3053:A,m<2456:A,A}
bl{x>3168:R,R}
xn{s<1829:A,A}
hj{x>1386:gft,fqd}
snf{a>3072:R,R}
pg{s<294:A,m<831:A,m>1263:A,A}
kkk{a<3490:R,x<3523:R,R}
xpv{x<1729:lgg,A}
dzp{s>458:R,x<1321:A,A}
ntr{a<3241:qcr,bfr}
rk{m>1700:R,m>1433:R,x<3539:A,R}
vl{s<701:qvn,a>732:A,R}
hq{s<2487:A,s<3014:R,R}
dlc{x<3041:clc,tmq}
zg{x>1814:ls,x<686:hrq,jpr}
pdr{x>816:R,R}
tjb{a>1942:zl,cmf}
sgs{s>1230:R,R}
cnn{a>2517:tzg,x<1521:tjs,a<1469:dlc,tjb}
sfs{m<628:R,s>930:tnx,m>1168:R,R}
cgk{s>1412:A,s<1399:R,R}
xb{x<285:A,A}
xmj{s<3313:A,m<2698:R,R}
jhp{a>1163:A,R}
jgv{s>2059:vx,x>989:R,m<1617:R,kjl}
gpr{x>3160:qp,a<3047:zbz,lvv}
tfx{m<2941:R,x>2491:A,A}
sr{m<1525:cdh,fx}
fql{x<1418:R,A}
ts{a<2631:R,A}
bfr{m>1646:R,s<85:qqv,x<3051:sqx,A}
zj{x<3373:R,m>3389:A,m>3219:A,A}
sk{a<2840:ts,s<3691:qr,s<3876:A,R}
xtx{a>762:R,m>3708:R,A}
rx{s<2605:A,qhr}
vx{s<2277:R,a>3680:R,a>3593:A,R}
kdf{m<544:A,s<1477:A,A}
cmv{s<657:R,x<1700:A,a>3646:R,R}
xpm{m>331:A,R}
qzx{s>1906:gv,a<1113:ggm,rz}
qrm{x<2907:R,m<2572:A,a<3489:R,R}
dtr{m<2474:R,R}
cx{a<2460:fg,a<2572:R,lpm}
mnc{m>2641:R,m>2575:R,m>2533:A,R}
hsq{s<385:R,s>405:bs,m>3834:R,kcl}
jpr{m<1719:qt,hg}
hl{m<3427:A,a<3178:A,s>624:R,R}
vf{a<765:R,m>1268:A,s<141:R,R}
bhg{s<952:A,R}
gt{m<2287:qjq,a<3194:R,m<2303:xlx,lt}
gd{a>2980:R,m<1203:R,R}
cgl{s<397:R,A}
cbs{x>2658:hrv,m<812:qtc,zh}
psh{m>546:R,A}
tpg{s>2985:A,m<3486:R,R}
rsv{x<3495:fst,a<247:klf,jlv}
vm{m>2318:hcz,s>2480:A,hk}
hnk{m>736:pkb,nr}
qbg{a<629:A,s>3209:R,mtf}
vmr{s<336:xjb,m<2583:qjp,m<3422:lzb,nrv}
dqd{s<491:R,x>2458:A,R}
jfc{a<3378:R,lm}
mjq{m>3216:cmg,s>1624:A,s<1610:nzp,dz}
fm{m>3056:lp,s>98:qtf,A}
clp{x>2129:R,A}
zzq{s>1114:hst,s<609:mbq,m<1439:rrn,fj}
klf{a>120:A,a>56:A,A}
nl{a>3745:qj,sfq}
szx{x<761:nrx,db}
pq{a<1830:R,A}
rq{x>3602:R,a>3950:tn,a<3931:A,ffr}
lzs{a>569:R,x<1250:R,R}
qtf{a<3358:R,x<2905:R,A}
fph{a<3718:A,x<2225:R,R}
snj{x>2131:thp,x>1912:qkg,a>3243:ltm,px}
jc{x<2498:A,a>221:R,m>877:A,R}
gzj{x>1807:A,m>3696:jz,qv}
rb{m<919:R,s<98:R,s>121:R,A}
ht{s>399:A,x>3166:A,m<2596:R,A}
rjz{a<370:R,A}
mjg{s<392:A,x<2790:R,A}
qpd{a>2828:R,bmj}
nns{s<385:A,s>403:A,A}
xvc{x>1676:R,s>1628:A,m>687:A,R}
zxb{x>718:A,R}
tn{a<3977:R,x<3440:R,R}
zdc{s<105:A,x>1709:A,R}
dr{s>368:pxd,R}
krz{a>2955:A,R}
fs{a<3398:hmk,s<1304:brr,vdt}
kzl{x<251:R,x>411:R,s<95:A,A}
hnd{x>1357:R,A}
fdx{m>2361:pb,m<2198:phq,m>2290:qbg,kbx}
rhc{m>2517:scg,x<1676:pvn,x>2698:qfk,fph}
jh{a>3482:A,R}
ddz{x<3705:gj,x>3834:A,m<3795:nqg,xxf}
czv{a<2106:snx,m<2262:nnt,cx}
xhg{m<2396:R,x<2899:A,R}
kc{m<2522:A,s<1213:A,a>229:A,R}
vt{m>515:A,s>566:A,A}
kl{m>3081:xc,s<378:R,m<2962:vrd,hnd}
xmv{m>896:A,s>941:nd,pmn}
qjq{a<3471:R,A}
tkh{s<1068:jh,qrm}
cj{s<2474:zrc,dxh}
mcj{s>3215:cq,pn}
bxd{a<891:R,a<1032:R,m<2541:A,R}
mtc{x<2110:R,m<3035:R,R}
psl{m>1354:lfd,s<67:gjb,s>101:qm,R}
lmd{m>2534:cqx,s<2646:cz,m<2340:mcj,nz}
xc{s<372:R,a<3274:A,R}
gj{a<465:A,m>3758:A,x>3598:A,A}
bz{m<2223:R,x<963:R,x>1101:A,A}
vsq{x>1282:A,a<2591:A,A}
pht{a>2948:gd,s>499:tr,s>425:ldt,R}
lvn{m<928:R,R}
gb{m>2419:R,a>1135:R,m<2258:R,R}
ct{s>866:R,x>2173:R,R}
vj{s>1039:A,x>2171:A,A}
ft{a<1806:R,m<255:A,A}
mqh{a<3675:R,fql}
bkg{s>3166:R,tpg}
cq{x<1886:A,A}
zrc{m>2535:A,x<2119:xnp,x>2452:sxk,bq}
nv{a<3611:R,R}
zjn{m<1047:A,R}
qtj{a<1943:R,x>2213:A,s>778:A,R}
tkq{m<1388:R,a<3674:bhg,xhg}
qjp{s>376:bjz,tzp}
bfq{x<2368:A,x<2523:A,a>3761:R,A}
mr{x>2674:R,x>2564:R,jc}
zkg{x<2949:R,x>3122:A,m<3032:A,A}
hst{s<1346:rln,x<2070:zq,mk}
fp{m>930:lsr,a<930:qcc,pdr}
ljh{x>1503:R,x>966:A,A}
bs{s<411:A,s>415:R,A}
gzq{s>573:spn,s<216:A,m<286:vgd,A}
qfk{a<3832:R,a>3913:A,A}
nxh{s>2539:tz,R}
hk{a>3128:A,R}
xdr{m<2195:A,R}
scg{m<3346:mtc,x<1621:R,s<303:qx,A}
sc{x>3385:lvg,a<3360:R,m<676:sfd,A}
kj{s<354:A,m<3555:R,s<487:R,A}
kr{s<1061:kzc,x<3218:qjd,a>424:zr,rsv}
qhc{x<2149:R,x>2781:R,m<953:R,nmc}
qhd{a<3942:bfp,s<1085:zkg,a<3963:tkr,pvm}
gs{a<2897:A,s>2780:xmj,lms}
rbh{m<3151:nds,gzj}
rbd{m>2470:A,m<2224:R,R}
fst{s<1304:A,m>2596:A,x>3343:A,R}
hm{s<3488:A,s>3768:A,x>608:R,R}
vn{s<1194:R,A}
xp{m<3163:A,m>3391:R,s>1334:A,A}
dh{x>532:xps,rx}
lqr{m>2480:A,ljh}
rrl{s>375:A,x>2075:A,R}

{x=1741,m=2523,a=1038,s=869}
{x=427,m=395,a=33,s=3014}
{x=170,m=331,a=1510,s=1074}
{x=152,m=897,a=1242,s=952}
{x=1569,m=9,a=779,s=1744}
{x=454,m=751,a=1610,s=820}
{x=764,m=1526,a=319,s=1001}
{x=565,m=667,a=3092,s=133}
{x=717,m=127,a=2,s=1405}
{x=1484,m=340,a=1336,s=44}
{x=2043,m=256,a=1683,s=698}
{x=974,m=1247,a=1136,s=1947}
{x=1100,m=160,a=981,s=849}
{x=1433,m=2789,a=2062,s=11}
{x=1447,m=197,a=580,s=564}
{x=9,m=1277,a=1689,s=142}
{x=3014,m=1127,a=71,s=1035}
{x=2455,m=919,a=1403,s=1924}
{x=811,m=1025,a=373,s=1349}
{x=46,m=2453,a=991,s=1}
{x=1385,m=1299,a=225,s=1462}
{x=802,m=123,a=2922,s=2545}
{x=342,m=693,a=1722,s=1162}
{x=321,m=221,a=428,s=2130}
{x=3344,m=622,a=92,s=579}
{x=1349,m=1013,a=2894,s=1315}
{x=169,m=8,a=677,s=1053}
{x=1785,m=1334,a=1554,s=314}
{x=252,m=86,a=3588,s=1268}
{x=135,m=6,a=477,s=1356}
{x=75,m=3120,a=89,s=1078}
{x=2614,m=733,a=1553,s=1666}
{x=39,m=918,a=2810,s=2292}
{x=269,m=771,a=2312,s=996}
{x=1062,m=889,a=2333,s=1295}
{x=2178,m=1688,a=458,s=1039}
{x=45,m=148,a=1642,s=22}
{x=834,m=794,a=98,s=1313}
{x=972,m=863,a=877,s=731}
{x=2321,m=436,a=2342,s=874}
{x=96,m=647,a=297,s=901}
{x=822,m=710,a=600,s=1514}
{x=600,m=401,a=2863,s=683}
{x=1318,m=493,a=2953,s=595}
{x=1,m=327,a=1516,s=374}
{x=3193,m=1755,a=3006,s=872}
{x=1410,m=1798,a=1427,s=790}
{x=1526,m=831,a=69,s=777}
{x=1237,m=104,a=3914,s=412}
{x=36,m=415,a=79,s=2432}
{x=101,m=1571,a=17,s=788}
{x=3117,m=1449,a=163,s=309}
{x=517,m=1333,a=1122,s=336}
{x=2907,m=982,a=873,s=524}
{x=2907,m=1025,a=422,s=833}
{x=1111,m=1295,a=1088,s=1646}
{x=2188,m=1467,a=53,s=1973}
{x=34,m=3017,a=34,s=1428}
{x=240,m=3881,a=143,s=521}
{x=274,m=1911,a=31,s=1721}
{x=618,m=2495,a=1063,s=144}
{x=1000,m=478,a=944,s=2741}
{x=2445,m=132,a=4,s=809}
{x=1653,m=569,a=2011,s=608}
{x=827,m=1195,a=2518,s=504}
{x=401,m=711,a=905,s=777}
{x=1132,m=3298,a=1503,s=439}
{x=757,m=3640,a=1349,s=682}
{x=3850,m=164,a=1903,s=775}
{x=1285,m=662,a=454,s=561}
{x=216,m=161,a=172,s=183}
{x=1164,m=1043,a=1275,s=2226}
{x=2857,m=247,a=1301,s=31}
{x=855,m=1998,a=1484,s=1567}
{x=469,m=627,a=557,s=1481}
{x=2763,m=3064,a=1040,s=2434}
{x=2249,m=5,a=1411,s=279}
{x=454,m=3189,a=993,s=1560}
{x=140,m=1004,a=2119,s=898}
{x=1115,m=2195,a=259,s=510}
{x=343,m=2038,a=1527,s=1459}
{x=2066,m=899,a=675,s=2545}
{x=2436,m=923,a=608,s=342}
{x=100,m=42,a=1368,s=71}
{x=1477,m=153,a=2079,s=286}
{x=1838,m=1330,a=6,s=1383}
{x=1630,m=413,a=1027,s=631}
{x=247,m=651,a=49,s=347}
{x=409,m=467,a=1329,s=934}
{x=1367,m=1805,a=535,s=803}
{x=2157,m=2335,a=969,s=976}
{x=1778,m=1165,a=1341,s=89}
{x=162,m=1286,a=1595,s=491}
{x=1901,m=31,a=10,s=1900}
{x=102,m=1156,a=955,s=1226}
{x=138,m=256,a=1556,s=2215}
{x=2116,m=1849,a=83,s=1338}
{x=20,m=53,a=608,s=569}
{x=2861,m=369,a=1042,s=1528}
{x=194,m=10,a=964,s=297}
{x=2318,m=328,a=730,s=850}
{x=1958,m=2008,a=3122,s=1207}
{x=1221,m=2256,a=38,s=8}
{x=54,m=2430,a=53,s=936}
{x=1420,m=952,a=1419,s=59}
{x=1021,m=561,a=463,s=813}
{x=12,m=98,a=850,s=46}
{x=1155,m=1768,a=200,s=1668}
{x=140,m=1439,a=1916,s=193}
{x=754,m=397,a=23,s=314}
{x=1566,m=1054,a=1418,s=392}
{x=1482,m=1238,a=941,s=1459}
{x=491,m=551,a=1941,s=1376}
{x=1695,m=77,a=260,s=2519}
{x=144,m=204,a=45,s=334}
{x=351,m=412,a=2647,s=317}
{x=1176,m=2189,a=383,s=3006}
{x=298,m=1992,a=2519,s=1478}
{x=2,m=409,a=1668,s=95}
{x=38,m=871,a=2346,s=226}
{x=178,m=151,a=922,s=1006}
{x=271,m=717,a=498,s=26}
{x=704,m=1943,a=55,s=260}
{x=1281,m=1773,a=994,s=818}
{x=388,m=556,a=2899,s=455}
{x=2045,m=747,a=732,s=372}
{x=1,m=2749,a=109,s=852}
{x=402,m=2322,a=61,s=334}
{x=157,m=51,a=538,s=911}
{x=939,m=86,a=1732,s=228}
{x=55,m=742,a=1219,s=745}
{x=3336,m=2251,a=220,s=956}
{x=1194,m=289,a=1956,s=555}
{x=1639,m=120,a=423,s=315}
{x=1848,m=455,a=1014,s=1369}
{x=647,m=428,a=347,s=2516}
{x=95,m=1386,a=1425,s=1275}
{x=184,m=67,a=2116,s=440}
{x=311,m=740,a=2340,s=2521}
{x=410,m=579,a=575,s=2457}
{x=183,m=1462,a=540,s=31}
{x=2602,m=317,a=602,s=389}
{x=1202,m=34,a=67,s=284}
{x=609,m=929,a=112,s=2388}
{x=537,m=1214,a=315,s=2220}
{x=403,m=706,a=381,s=101}
{x=1990,m=14,a=3374,s=3250}
{x=1388,m=2477,a=694,s=489}
{x=307,m=76,a=414,s=119}
{x=22,m=1407,a=1937,s=377}
{x=1102,m=654,a=107,s=700}
{x=209,m=2473,a=3253,s=122}
{x=14,m=1115,a=926,s=642}
{x=1896,m=34,a=1674,s=321}
{x=1354,m=468,a=1001,s=1676}
{x=1097,m=2593,a=854,s=1015}
{x=520,m=1580,a=349,s=1897}
{x=1925,m=1372,a=3195,s=3561}
{x=326,m=172,a=829,s=233}
{x=1455,m=431,a=34,s=450}
{x=711,m=1946,a=1081,s=443}
{x=730,m=1041,a=3132,s=797}
{x=39,m=1887,a=878,s=910}
{x=1006,m=716,a=2966,s=39}
{x=239,m=2607,a=3282,s=133}
{x=1000,m=492,a=1097,s=673}
{x=134,m=912,a=41,s=147}
{x=1224,m=2150,a=116,s=1956}
{x=97,m=1096,a=3302,s=197}
{x=233,m=1029,a=1051,s=793}
{x=327,m=363,a=1155,s=428}
{x=680,m=478,a=3195,s=1672}
{x=696,m=878,a=2166,s=1045}
{x=518,m=244,a=944,s=1914}
{x=700,m=9,a=595,s=589}
{x=693,m=1652,a=1322,s=615}
{x=1613,m=781,a=1331,s=2268}
{x=2542,m=1739,a=2560,s=1474}
{x=970,m=1490,a=539,s=3847}
{x=203,m=119,a=511,s=1865}
{x=134,m=1484,a=165,s=1015}
{x=110,m=40,a=185,s=901}
{x=668,m=1023,a=497,s=518}
{x=795,m=1769,a=1478,s=577}
{x=482,m=112,a=329,s=2807}
{x=603,m=1999,a=548,s=1218}
{x=177,m=2294,a=1863,s=2}
{x=996,m=837,a=1121,s=1575}
{x=2244,m=2546,a=2166,s=97}
{x=335,m=2114,a=18,s=13}
{x=1683,m=281,a=256,s=373}
{x=1279,m=1367,a=702,s=786}
{x=153,m=226,a=646,s=623}
{x=124,m=4,a=63,s=2308}
{x=543,m=3722,a=156,s=150}
{x=117,m=403,a=779,s=831}
{x=15,m=1018,a=461,s=437}
{x=59,m=468,a=238,s=137}
{x=29,m=212,a=2308,s=68}
{x=662,m=244,a=2403,s=55}
"""

data = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".strip()

if __name__ == "__main__":
    print(part1())
    print(part2())
