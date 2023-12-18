import heapq
import itertools
from collections import defaultdict
from dataclasses import dataclass
from functools import total_ordering
from typing import Literal

# data = """
# 2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533
# """.strip().splitlines()

# data = """
# 233233113311241121234343343214331245213144241553252132155521311253254232542552344353534322253245553142552222531524412411331424111421312212221
# 312332233233121234131122114442251122232145423545335523152214246544444232542642636454111211355541425253155441432121511431224122231421212331313
# 232122343233344323333222224215141321444135531541531234453364436333244664223335653336254441535433321225333134321355351432341342431342413121323
# 131222114244332211432122232142231525435152314444141422526445623462354266446443326254353463635254334131221553134122443334422121441341112322323
# 233133211411441143313442113153452524315442225143646332442336426246535626524342554364444525454231334511212414412422251453211114331442434444213
# 213214213214222123123455235245223351423214415223544325355523662235222222633365332643562366556225534342542551224122342512141421421114312214213
# 212232231242444114313223422114542323552455142225332542423634465326564252242433322634646636345242634641325133232352154142133344212414142442243
# 114413323422234232221333244142211222535332352443532452624665525644335233523324326263545663565563245366513231135235332112221411442421441412144
# 321324121114212122524341115553512322115662644254325426263654653234234456633534542443345542535566426424653451325123231441443423243434111141144
# 442341132313432124415254551353454441166252226325323556542254242552532223535355236424665222564634634525445342241144413341512534123441343311314
# 132222341111113415145141435344515544355232342234422363262326265624223234644463442422224453554646556253463552452343251144312244352221123312114
# 121242311243115443423124131553432522525235552422464562665443232662424543226324642636655344636463524425463633533451143443555132412312424323221
# 334231224223151513254512335215312253426552224523223322352425363324547345564522366652646232663355354564253524342251111354514134312134434124314
# 333141422241133233433351443322154344246644456632344642462264643633745363644733377534363552363553545635536663462615545144122253442342241124432
# 131443331143114445555415513523342524555462325432464524665544444367376357756577434733753625342426233662256643552224125124532411454532412322211
# 313122141123231442533245443546255552443364443233443645464666536666363564564736563373346654744234622466546344454345543433421423224312322224314
# 213211321435441155241342451463346353422546323553424634755574364673466547663436464456434556477262535653654226666533653534452221534533214132432
# 124222413312242315144524452652623545363323566536633374636565546637764375667466343354773767734633446266366443246466263422543131351524544132232
# 342332214523243154434552622436242646653265526365534767635443777475543677576746346736746345357546332622555235634452444645212115215241353133322
# 334134444124432312155142346226623666233543534643464767446355756574645757744464677345355456556563647734222463654264664334225352225434222541414
# 241221154542135451433523663435424362535345635774377445537563453773666755574746433734663745665647676534442655554363564535642515355445445122441
# 114312241342451234443336562232364535524435637346453774674563476534537575536567365765453576673575763745352253233344554554463244522541141444211
# 123123344313423414225625265652245635323436665434735333537365533377765465576757365546664763544373534634345542466543522422552412245315131415134
# 123253243152412135146344446554265344537737547547765735374656665674465636343737375443364767564636574474346564454655542363522654251253532312533
# 122355542444233251244534536624252252466337476354443467536555737557767566666743665535737467556443333467433644263244655344255435415452415113211
# 414454541421253355624256465235646647575546673647436536773754475854656485746745886585533467374563473333556446336222435333464336221113211151212
# 212355445455124455224654355253635675653635775343576437744857764777878774844667775685786345755644345774445445455324434356622566514145542123222
# 252211153124113344255563266625357663667555735377666575557785547878467588756466746767576647443374476365437436565462554645634543334213321255113
# 243133131453441236542425632222464644773643763464766765858548744554788677486554767564856645777345755643746456746632434454434555423254242435214
# 513311112543323423343646554522567576576766653653674667876764685657756455756577464447674584756436443636456454774766334464622252544331123132334
# 141422441521423334325456265344534553754745356333557484657684744475577866846764684556777584545544657744455656753646566662345263462151535541341
# 213535532335555455232645263353367736773753446448865687688846448665685548785785444668747456465858647363357754444367362235333645265642412112154
# 151313211514432232343453425543666656756555745477746574476768776476867586666757757464846485775754443777336344534735533525345533633541245233321
# 131245321543354265642654527533544474353435488585474574585775467784455677677848645854786475866664576664533334577354467422254354566423555343454
# 222224221226263562454355575333755544473446548467748885776674566447667476745477755678685674766847655665653377447355656365563542256253334222431
# 413315333555443642246235573467656777375764658678756568566446865656577554786478766575557555755547647644337553665736577346443623225536324552345
# 351352144123465223566326574634477777767457646875784548747585645778788696779665765457445476868554868884666736744575567354552643455224522244514
# 242132325452252422566563773466744764763568854686868645464545458558999559668795598877657758548666655456443573754655654746563356536565632214344
# 314525324552634223634476376534574773745558447548667547487777776867676855698767955577545854566888654776544454435365736666556336463323624521134
# 142121156636244333546566376333366374465446887555766755658767895577958969989876656975867745464684875865788444646456574337642322645565642251443
# 232311445462452355663656567765665535585577576475748665769988779578559559587967688677755655647658478465847474676756467457432562434632555343313
# 421143234326446662266775637766567568785585664784546885959778686585555855988787858678556978867847566787477656755636535774344664634336246432311
# 331112344342466236663357755744573656486744476666786997589667679687585876586798686765666987564745887586568685443577435657773353652346453313214
# 241332525436446424455475347453663546676574675757489977585757765767859657659989878656876576577458747846654744776637556456343725235623455233251
# 415445424366522233655744366444537588488866657748768767988878789995968866596585867877658797969567455874748754683574456443576644625643552244515
# 421414256535462523647737653754354467788674686668887797575759959797697795956586565678757889576868865866746755866763644347567355356652226666221
# 541554236534632224464363754536757865644785585688995869987875577667558799969995676667586999799896758476487574465466564635537662332526454546351
# 255156626366535527344547543746655786658786886885865566567786598995556969759866885767798986566579774564666786687844557366555634564655636665433
# 254552233443454323435676735345887447684844779676856889997777956977988967996995659659697756889669785455455657875457464556577774436342435564442
# 131145352564255253366666374675674584864856786855687799675776879799798666879778989555588996576795999677668584686483736573374367452365442623444
# 543424365446364334644353534766868554756555675966787999658598886899897978799766797977579795685999666776757848767466353374356767535622644446641
# 514346325564232473464744735466866774544845557587896575956756779787688777866899979986559756797556976674778888855744437777446547523264266236644
# 532435526446654366637653333345665855777664699558768977868686686798998788787768689786975956966857665857564454764488775674456554435563632455244
# 233444364542244364747547644577565877757785555575855956686777676896969779686778878877676669865978657697645774876576734474576766346252642243224
# 154622562433363634335553464878464848754879885998798985897768886666696778869797978888989865776585897856557788654668665755736744445423226354625
# 413353362533553456355334635586686668765466899679887859677797776777787666878676697777999875765989855775556678654447857444374376364655426234242
# 333635355452453574647544666876584667574695786988975677969978689796988869978767666676869977599789698796554868667686463636774465756536256236536
# 125243534356666676343675556465656767574957587989669967997796996896998969686967677787876866776668667676566746648685857436576373557566545524663
# 452264246532427746466557445445847657858975966878655879686698976779886699889986969979786678868869696796585567676766844535765773566534545566625
# 416545346666553535756577354668577566845576585868796766676766766668879778798987669889899788897967577785596555874544868536733345766225255526455
# 444653553556445477455557484867674574648856657997566778976696988877878879879977787986968776977588656669958664777447565445545463667736244526456
# 362252522523546665543346774675448567485865967978566988897666699878987988788988987976999886786969988889957774868787774844757733745645344566226
# 256664534666333555363777368744748748485656866667976976897876768679888778797889998766686776679978769568699876666684688454375445343332463363623
# 464435225266453757336566386555446845595796586767868966668789869888877988988998878677899899696755675595768857645586865457347577373744223522352
# 546325625455336357564475365545546667588795665979987866978898969797889879798979877796799886769657699895769985787567867465637553453555336322335
# 362436623323465346744475545585458655778966756976699679896999699987899799987788777986999679887956588597698568644764868743455757575434646462263
# 363442423332556555634535866647775655875976595777796689769669887879789988977797779768699977666769967779669794544578748544566375554332423465553
# 326533522646677354353743787878468556577586599568667678878677977987778787889987899978788887986769967996675758864656874883374657434576365223245
# 244432253254663376574554464577756458898575978898798696797896987798799889878998798877979866877785796989575875546557588587453564676643446644422
# 342343243243353734665564565547877854759657986989768676679976978798888879778799787988767969699669665578567797786454588765346446656562465532645
# 622332343545353757347575845674686857666768896869797878986786877999789899887787787997697979768677656755675874455448574556636353466473455436623
# 563563445346454754667776777464658486586586555888677668786869799798989779989877999979778788796798667558575555657756685555755644346656526634326
# 434226443646555374767577848545444544556685595986966688668776778899988787978878778998998878787679999876988985875658677665533364555673223453552
# 463244455265375545336653864684848576778557877757867788768778979878888998879978979776676988889867966956699955846475645683734534666445644254552
# 252354235632666433734336864885766758898579768766699887668968978789798878978878997988766888768885899979967574685446857685447436564455536564454
# 152643326455466434564545456785876546899797585876867899676697977987999877897988779989798696987868959888687767855588748576475566563646342334432
# 336663645254636434374573677444684784567757597759787986967669877977997888798978989899869667898996756956766785846877456756774466575665522542632
# 326355253533265543646436786587855448869979778755697987966676777897777877988987779866867876869979555886786978475575566536356446376453262455666
# 533622554655666454773367745667444785457978965598588769676788887999798999898779889986967669797777588969958578445564665647373656776346543355332
# 154664562234437334575443355775678654865866675966679679666868687898797988988778786886677878678865988996575778564758656737534474354365242466345
# 332424622352257464665555456846867464657677559599769878696987966887797799979987988877867898876995665685969555547865578735676557437523453436362
# 153243353633567554557334468687544666755676998699769689777879888989797978777878879878969998698879965955886966775784477477364774456656566564525
# 155423343525664656553553444474756546779565668595587676698878969679688897888976688768697667776596998558688668654888748453576776474625332445645
# 332642232546347764434437566758778848887886999888598969668798769676787677778878986978968689895587658869859455665584676645664353376546466422255
# 136462453423535366774456338645785778778576996559865768776987787669877976697776768697769787656875858559978586865564585576745533776532524456534
# 246464526635333563753556457585478457757558795988596897967798696797688976966886976769967778668557778788696455485887677566646776743522345266263
# 415342323264453574534743577866875445557598967965969799868979776878769889769697968699896896766587688676988674755884746756576676537355446365225
# 243652443252225455644363573545874655475579969768595688696766886969777879866999868797697969875589579796764476786477686447666475462242325256354
# 344565524255565375355577573654454675877667868887789656766698667777986677886696779986698897899776756666555844884588883367444733453355556246353
# 324545254562622666635474374375466465666547795967796887569896899786787797686997978678969976778656697855664648565785457456665654642222445556344
# 335352233425563567354335647744748767865444687898887689665668697896989887889887967778996569878669879974457864678488675454467456776424643555253
# 142265345642543266553364364576688746547654878595685786898878699686899867677978966966867996878995989575664456565546634467436467734552624423364
# 332342525643625644657553566776686866854584556577857566767786986877769968779697979899998667995968756566548866754686657547454646322253644422431
# 142223565264524255777567765654774886568576845589779885597966555666677996796697996757797666689578999664646647774685767446433345224532632232643
# 234326343634354645665735376473764678477848746678678567689567575956898886897677787765996569655799978677477478578644565654467656434422663256515
# 244522543623445533446564754374667675686578568987696998695896677667877878685577958669765697657679984656488788644646334675634547245666343226335
# 342124632665655535746663553475755476568884545576898897956596975665756765589676675869596578968697744586656548755637774766476634242525465636232
# 434323665436522446554343463743547665554565776585678689876775977857958995879586669657689876975896886567457758844534734375643675256563565445334
# 224424466443656562246757633437534644484865854585669668899855959677956999897577759667787588896776658688487585486653334343467746424564633561424
# 235542544645262533274744575757636444645688685587858576779576559795985897766556787776557787865667656456467864674465767664376736254343433353314
# 555251344536543334634465473767663756748668565854684987857556888666986596775675667895796567586474855666755687557673763537656363254524465633444
# 513452236456364625353673343646664476557647465546758545955986697879978888555658578867887987585654577765456564454573745656673363325643453331252
# 314315445353244652353453746757547573575777558645678445896589896778658859869986595567596865887746446587646677677643677465773265452563245532125
# 243444135365362422343636443474544565758666457756765485878598998779899787657687775685559845574757874858866664757535477535443643244553654343534
# 155445144342525222636337575646353537546454854447474666458566655656888767977856898575967668756765447844566544653467766477645563353655624422443
# 123524245664444555264565635765347534676444567565886688865688678676885859858776588748888464445647668746465757665453575635323362626464262125141
# 251215453454445234623365555445365536545478768586765645656866445567889998899576857888767684786578677774663356654653456333426655443323455151523
# 344135245433634342264546564747656677364466577668754648687547677465468846754758786456587658487764744476367454564777536566656435442622542522142
# 114243245524264652535255335644356367553365757464767677687564768586655744487566448555667478657846685644736354445543656535623543346425455431243
# 523351553514362343445355424436347355553443567764444758568458745576844644484747854584854466856788675843457576574735643643622242456662125343535
# 252513425421466446465536554656655376447765657657468854788764654547767548488778446756657568854654746335775675466333745625445432563345535311234
# 221315541253155533555252635376373573737775677577744548448478857577665885476648655754744574765666775545477677736633342265632256363243425212122
# 442453355232125433552525546425667576574654777535567867865876686764558888465756858647584656775566676745463657557544466332245434324241344232434
# 315145413215256233442466356636563376554443765636357786567756685876876468865457688748748687765447737774574343634355536366536363533144524445145
# 124225422543333426653426264522373734467374456775536378556468775546447554664558588457465566434436346674547576365762525453646325442531332344344
# 432212452125132256455426255654556367574353777735734576774485757754854564856847546764545484665375357766767344334653252324556232432421115543444
# 142443142245211224355553266653444364643657676735575564775668775888884756685776558486777376543556574637464337334352363354244234515413333314124
# 122522311532415552633452345344554436545737676565467436356654464678547446564465457553347355453647477774377743424625653452625563222535243154511
# 432311322312221334525635632462234463366554754645646674367553333675475484858685766667437574545355454354457743342666262556556263432413534445344
# 214424413214235235166666344352662236554663367354637775653763476535763663454755655353655633674744573737653362562243425635325221525353445311334
# 412224351123455344544452452264225262233435465535647554663637433453354647463757577754547533536746443765366232256522666455633511134251513332323
# 412231223354154435535332443246254526662535536774357474447765375755346447665344657654777556444635637746464352345466633634223513444155214442424
# 231242132433542414534232642534523363646526446533634353546443535447464553466443337657675334475566473736534554256334266236613411153421114254331
# 424321424323154122253214562252665526253524267743737333577456667636644565467646667575767647753575364763523562542234226364243222211431354414213
# 433443433245315313252254234646666265253553423345735445355734444467443574445363334656346543543755474366263536354646655564225444315212223111121
# 422413434335414333541354554362253245543226445337664363755443365447475577434773677366436563535535626342224536522223556311142433214254111122344
# 334343232115521222233532124666364233622442656664236457565555563477436555547735446645336467666636642622233425546456252435424515141535223434242
# 214432413313325232422443252542246664246456224643525674553555637667353754764767765577754447642242253463653543562265244544433344521144122213343
# 341441331422314131511525434226234466342466452656666665257456575456443344355643375473545646232245665345434354222422443242433331355154333432123
# 344413111422121551215321154513244645642546423266245542554543357336453544675467567632446455452653545544434646626311334433334431115341443441422
# 244431241213435221255552532325254622334552432333244665363342526665235773576325246345664366453535546463463326443552421442153112142523334133444
# 224324141224442113454442432433144446254324563644466464642336642635565525355232235266642522233434253665562465423434415555314341231311114223231
# 212333224312141351224121411322525336263446463636642663444442464633344354466443446224443566332333323633335555434444212441545215511142123312324
# 433323323342344231533423222221455352565253425524254454556262525555425236265645436323626355266562653465555315255422132214332441213113122132344
# 322311321434244443443321335324231112245364533436432656624432443466352554322265345553342225642225636444242332414141324122115344231332314311431
# 334241244143223223344452324343452135411114626344255662646636433266425564634654353544633523652555625566121514555433313535253213441411333241431
# 212213111413123343413315443413135454111334546443523664624643224556245446335552663542263364642332642535213525341242321421255324321434111342141
# 323243211214423212332113152434423141112555111632454524452546453342256663565623353646636322442326333441241332412425243254234312344334221344122
# 123224433331112214324244345251354221333453213451533542624554645622362543355653632335653645645631211353145133445543215352343324422123124213211
# 232222213121224333412322131151342143215554321312124332356226453435334363443426532622462423525525244151423154522335213153441444233421411421131
# 111231114441122122214123131121523355211415313331543221155325252554324344554244352436664515212244241135355545521534451322242144132411222121122
# """.strip().splitlines()

data = """
24
32
32
32
32
""".strip().splitlines()

LEFT = (1, 0)
RIGHT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

DIRECTIONS = {LEFT, RIGHT, UP, DOWN}

PREV_DIRECTIONS = {
    LEFT: {LEFT, UP, DOWN},
    RIGHT: {RIGHT, UP, DOWN},
    UP: {UP, LEFT, RIGHT},
    DOWN: {DOWN, LEFT, RIGHT},
}


@total_ordering
@dataclass(frozen=True)
class Node:
    x: int
    y: int
    direction: Literal[LEFT, RIGHT, UP, DOWN]
    steps: int

    def __lt__(self, other):
        return self.x + self.y < other.x + other.y


def check_node(node, map):
    nx = len(map[0])
    ny = len(map)

    if node.x < 0 or node.x >= nx:
        return False
    if node.y < 0 or node.y >= ny:
        return False

    origin_x = node.x - node.direction[0] * node.steps
    origin_y = node.y - node.direction[1] * node.steps

    if origin_x < 0 or origin_x >= nx:
        return False
    if origin_y < 0 or origin_y >= ny:
        return False

    return True


def make_graph():
    g = defaultdict(list)
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            heatloss = int(c)
            for this_move in DIRECTIONS:
                prev_x = x - this_move[0]
                prev_y = y - this_move[1]
                for prev_move in PREV_DIRECTIONS[this_move]:
                    if this_move == prev_move:
                        for steps in {0, 1, 2}:
                            source = Node(prev_x, prev_y, prev_move, steps)
                            dest = Node(x, y, this_move, steps + 1)
                            if check_node(source, data):
                                g[source].append((dest, heatloss))
                    else:
                        for steps in {0, 1, 2, 3}:
                            source = Node(prev_x, prev_y, prev_move, steps)
                            dest = Node(x, y, this_move, 1)
                            if check_node(source, data):
                                g[source].append((dest, heatloss))
    return g


def make_graph_part2():
    g = defaultdict(list)
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            heatloss = int(c)
            for this_move in DIRECTIONS:
                prev_x = x - this_move[0]
                prev_y = y - this_move[1]
                for prev_move in PREV_DIRECTIONS[this_move]:
                    if this_move == prev_move:
                        for steps in range(0, 10):
                            source = Node(prev_x, prev_y, prev_move, steps)
                            dest = Node(x, y, this_move, steps + 1)
                            if check_node(source, data):
                                g[source].append((dest, heatloss))
                    else:
                        for steps in range(4, 11):
                            source = Node(prev_x, prev_y, prev_move, steps)
                            dest = Node(x, y, this_move, 1)
                            if check_node(source, data):
                                g[source].append((dest, heatloss))
    return g


def shortest_dijkstra(g, start):
    prev = {}
    seen = {}
    dist = defaultdict(lambda: float("inf"))
    dist[start] = 0
    pqueue = [(0, start)]
    while pqueue:
        _, u = heapq.heappop(pqueue)
        # next three lines are optional for correctness but give a big speedup
        if u in seen:
            continue
        seen[u] = True
        for v, l in g[u]:
            if dist[u] + l < dist[v]:
                prev[v] = u
                dist[v] = dist[u] + l
                heapq.heappush(pqueue, (dist[u] + l, v))
    return dist


def process_dist(dist, map):
    nx = len(map[0])
    ny = len(map)
    return min(l for node, l in dist.items() if node.x == nx - 1 and node.y == ny - 1)


def part1():
    g = make_graph()
    dist = shortest_dijkstra(g, Node(0, 0, RIGHT, 0))
    return process_dist(dist, data)


def part2():
    g = make_graph_part2()
    dist = shortest_dijkstra(g, Node(0, 0, RIGHT, 0))
    return process_dist(dist, data)