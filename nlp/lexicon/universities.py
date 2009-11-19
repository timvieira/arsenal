"""
Index of American Universities and webpages

Taken from University of Florida's Index of American Universities
<http://www.clas.ufl.edu/au/>

TODO:
    * add list of Canadian universities <http://www.uwaterloo.ca/canu/>
    * add list of international univerisities: http://www.findaschool.org/

    **** CLEAN UP HTML ENTITIES! *****

"""

def update_list(output_file):
    import re, pprint, urllib2

    url = 'http://www.clas.ufl.edu/au/'

    page = urllib2.urlopen(url)
    contents = page.read()
    body = re.findall('<body>([\w\W]*)</body>', contents)[0]
    links = re.findall('<p>\s*<a\s*href="(.*?)">(.*?)</a>\s*(?:<a\s*href="(.*?)">(.*?)</a>)?\s*</p>', body, re.IGNORECASE|re.MULTILINE)

    X = []
    for stuff in links[1:-2]:   # toss out the first and last two...
        ss = filter(None, map(str.strip, stuff))
        X.append(ss)

    with file(output_file,'wb') as f:
        pprint.pprint(X, f, indent=4, width=5000)



universities = [
    ['http://www.atsu.edu', 'A. T. Still University'],
    ['http://www.acu.edu/', 'Abilene Christian University'],
    ['http://stallion.abac.peachnet.edu/', 'Abraham Baldwin Agricultural College'],
    ['http://www.academyart.edu/', 'Academy of Art University'],
    ['http://www.adams.edu/', 'Adams State College'],
    ['http://www.adelphi.edu/', 'Adelphi University'],
    ['http://www.adrian.edu/', 'Adrian College'],
    ['http://www.agnesscott.edu/', 'Agnes Scott College'],
    ['http://www.afit.edu/', 'Air Force Institute of Technology'],
    ['http://www.au.af.mil/au', 'Air University'],
    ['http://www.aamu.edu/', 'Alabama A&M University'],
    ['http://www.alasu.edu/', 'Alabama State University'],
    ['http://www.akbible.edu/', 'Alaska Bible College'],
    ['http://www.alaskapacific.edu/', 'Alaska Pacific University'],
    ['http://www.acofi.edu/', 'http://www.albertus.edu/', 'Albertus Magnus College'],
    ['http://www.albion.edu/', 'Albion College'],
    ['http://www.albright.edu/', 'Albright College'],
    ['http://www.alcorn.edu', 'Alcorn State University'],
    ['http://www.ab.edu', 'Alderson-Broaddus College'],
    ['http://www.alfredstate.edu/', 'Alfred State College, State University of New York College of Technology'],
    ['http://www.alfred.edu/', 'Alfred University'],
    ['http://www.allegheny.edu', 'Allegheny College'],
    ['http://www.allencollege.edu', 'Allen College'],
    ['http://www.allenuniversity.edu', 'Allen University'],
    ['http://www.alliant.edu/', 'Alliant International University'],
    ['http://www.allied.edu', 'Allied University'],
    ['http://www.alma.edu/', 'Alma College'],
    ['http://www.alvernia.edu/', 'Alvernia College'],
    ['http://www.alverno.edu/', 'Alverno College'],
    ['http://www.amberton.edu/', 'Amberton University'],
    ['http://www.aaart.edu', 'American Academy of Art'],
    ['http://www.abcs.edu/', 'American Bible College and Seminary'],
    ['http://www.amercoastuniv.edu/', 'American Coastline University'],
    ['http://www.theamericancollege.edu', 'The American College'],
    ['http://www.americanglobalu.edu/', 'American Global University'],
    ['http://www.t-bird.edu/', 'American Graduate School of International Management'],
    ['http://www.aics.edu/', 'American Institute for Computer Sciences'],
    ['http://www.aiuniv.edu/', 'American InterContinental University'],
    ['http://www.aic.edu/', 'American International College'],
    ['http://www.apus.edu/amu', 'American Military University'],
    ['http://www.apus.edu/apu', 'American Public University'],
    ['http://www.american.edu/', 'American University'],
    ['http://www.auh.edu/', 'American University of Hawaii'],
    ['http://www.ajula.edu', 'American University of Judasim'],
    ['http://www.amherst.edu', 'Amherst College'],
    ['http://www.anderson-college.edu/', 'Anderson College'],
    ['http://www.anderson.edu/', 'Anderson University'],
    ['http://www.aju.edu/', 'Andrew Jackson University'],
    ['http://www.andrews.edu/', 'Andrews University'],
    ['http://www.angelo.edu/', 'Angelo State University'],
    ['http://www.anna-maria.edu/', 'Anna Maria College'],
    ['http://college.antioch.edu/', 'Antioch College'],
    ['http://www.antiochne.edu/', 'Antioch New England Graduate School'],
    ['http://www.antiochla.edu/', 'Antioch University Los Angeles'],
    ['http://www.antiochsb.edu/', 'Antioch University Santa Barbara'],
    ['http://www.seattleantioch.edu/', 'Antioch University Seattle'],
    ['http://www.antioch.edu/', 'Antioch University Yellow Springs OH'],
    ['http://www.apache-university.edu/', 'Apache University'],
    ['http://www.app-sch-law.edu/', 'Appalachian School of Law'],
    ['http://www.appstate.edu/', 'Appalachian State University'],
    ['http://www.aquinas.edu/', 'Aquinas College'],
    ['http://www.arcadia.edu/', 'Arcadia University'],
    ['http://www.argosy.edu', 'Argosy University'],
    ['http://www.azintl.edu/', 'Arizona International College'],
    ['http://www.asu.edu/', 'Arizona State University'],
    ['http://www.west.asu.edu/', 'Arizona State University West'],
    ['http://www.astate.edu/', 'Arkansas State University'],
    ['http://www.atu.edu/', 'Arkansas Tech University'],
    ['http://www.abconline.edu/', 'Arlington Baptist College'],
    ['http://www.armstrong.edu/', 'Armstrong Atlantic State University'],
    ['http://www.artcenter.edu/', 'Art Center College of Design'],
    ['http://www.artic.edu', 'Art Institute of Chicago'],
    ['http://www.aifl.edu', 'Art Institute of Ft Lauderdale'],
    ['http://www.aipx.edu/', 'The Art Institute of Phoenix'],
    ['http://www.aisc.edu/', 'The Art Institute of Southern California'],
    ['http://www.aii.edu/', 'The Art Institute of Washington'],
    ['http://www.asbury.edu/', 'Asbury College'],
    ['http://www.ashford.edu', 'Ashford University'],
    ['http://www.ashland.edu/', 'Ashland University'],
    ['http://www.aspen.edu', 'Aspen University'],
    ['http://www.assumption.edu:80/', 'Assumption College'],
    ['http://www.athena.edu/', 'Athena University'],
    ['http://www.athens.edu/', 'Athens State College'],
    ['http://www.atlanticuc.edu/', 'Atlantic Union College'],
    ['http://www.auburn.edu/', 'Auburn University'],
    ['http://www.aum.edu/', 'Auburn University, Montgomery'],
    ['http://www.augsburg.edu/', 'Augsburg College'],
    ['http://www.aug.edu/', 'Augusta State University'],
    ['http://www.augustana.edu/', 'Augustana College, Rock Island Illinois'],
    ['http://www.augie.edu/', 'Augustana College, Sioux Falls South Dakota'],
    ['http://www.aurora.edu/', 'Aurora University'],
    ['http://www.austincollege.edu/', 'Austin College'],
    ['http://www.apsu.edu/', 'Austin Peay State University'],
    ['http://www.averett.edu/', 'Averett College'],
    ['http://www.avila.edu/', 'Avila College'],
    ['http://apu.edu/', 'Azusa Pacific University'],
    ['http://www.babson.edu/', 'Babson College'],
    ['http://www.bacone.edu', 'Bacone College'],
    ['http://www.baker.edu/', 'Baker College'],
    ['http://www.bakeru.edu/', 'Baker University'],
    ['http://www.bw.edu/', 'Baldwin-Wallace College'],
    ['http://www.bsu.edu/', 'Ball State University'],
    ['http://www.bhu.edu/', 'Baltimore Hebrew University'],
    ['http://www.bnkst.edu/', 'Bank Street College of Education'],
    ['http://www.bbc.edu/', 'Baptist Bible College and Seminary'],
    ['http://www.baptistcollege.edu/', 'The Baptist College of Florida'],
    ['http://www.b-sc.edu', 'Barber-Scotia College'],
    ['http://www.bard.edu/', 'Bard College'],
    ['http://www.barclaycollege.edu/', 'Barclay College'],
    ['http://www.barnard.edu/', 'Barnard College'],
    ['http://www.barrington.edu/', 'Barrington University'],
    ['http://www.barry.edu/barryhome.html', 'Barry University'],
    ['http://www.barton.edu/', 'Barton College'],
    ['http://www.bastyr.edu/', 'Bastyr University'],
    ['http://www.bates.edu/', 'Bates College'],
    ['http://www.baypath.edu/', 'Bay Path College'],
    ['http://www.tambcd.edu/', 'Baylor College of Dentistry'],
    ['http://www.bcm.tmc.edu/', 'Baylor College of Medicine'],
    ['http://www.baylor.edu/', 'Baylor University'],
    ['http://www.belhaven.edu/', 'Belhaven College'],
    ['http://www.bellarmine.edu/', 'Bellarmine University'],
    ['http://www.bellevue.edu/', 'Bellevue University'],
    ['http://www.belmontabbeycollege.edu/', 'Belmont Abbey College'],
    ['http://www.belmont.edu/', 'Belmont University'],
    ['http://www.beloit.edu', 'Beloit College'],
    ['http://www.bemidjistate.edu', 'Bemidji State University'],
    ['http://www.benedict.edu/', 'Benedict College'],
    ['http://www.benedictine.edu/', 'Benedictine College'],
    ['http://www.ben.edu/', 'Benedictine University'],
    ['http://www.bennett.edu/', 'Bennett College'],
    ['http://www.bennington.edu/', 'Bennington College'],
    ['http://www.bentley.edu/', 'Bentley College'],
    ['http://www.berea.edu/', 'Berea College'],
    ['http://www.berkeleycollege.edu/', 'Berkeley College'],
    ['http://www.berklee.edu/', 'Berklee College of Music'],
    ['http://www.berry.edu/', 'Berry College'],
    ['http://www.bethany.edu/', 'Bethany Bible College'],
    ['http://www.bethanywv.edu', 'Bethany College, West Virginia'],
    ['http://www.bethanylb.edu/', 'Bethany College, Lindsborg, KS'],
    ['http://www.bethany.edu/', 'Bethany College, Scotts Valley, CA'],
    ['http://www.blc.edu/', 'Bethany Lutheran College'],
    ['http://www.bethel.edu/', 'Bethel College and Seminary, Saint Paul Minnesota'],
    ['http://www.bethel-college.edu/', 'Bethel College, McKenzie, Tennessee'],
    ['http://www.bethel-in.edu/', 'Bethel College, Mishawaka, Indiana'],
    ['http://www.bethelks.edu/', 'Bethel College, Newton, Kansas'],
    ['http://www.bethune.cookman.edu/', 'Bethune-Cookman College'],
    ['http://www.bienville.edu/', 'Bienville University'],
    ['http://www.biola.edu/', 'Biola University'],
    ['http://www.bsc.edu/', 'Birmingham-Southern College'],
    ['http://www.bsc.nodak.edu', 'Bismarck State College'],
    ['http://www.bhsu.edu/', 'Black Hills State University'],
    ['http://www.blackburn.edu', 'Blackburn College'],
    ['http://www.bloomfield.edu/', 'Bloomfield College'],
    ['http://www.bloomu.edu/', 'Bloomsburg University'],
    ['http://www.bmc.edu', 'Blue Mountain College'],
    ['http://www.bluefield.edu/', 'Bluefield College'],
    ['http://www.bluefield.wvnet.edu/', 'Bluefield State College'],
    ['http://www.bluffton.edu/', 'Bluffton University'],
    ['http://www.bju.edu/', 'Bob Jones University'],
    ['http://www.idbsu.edu/', 'Boise State University'],
    ['http://www.the-bac.edu/', 'The Boston Architectural Center'],
    ['http://www.bc.edu', 'Boston College'],
    ['http://www.bostonconservatory.edu/', 'Boston Conservatory'],
    ['http://web.bu.edu/', 'Boston University'],
    ['http://www.bowdoin.edu', 'Bowdoin College'],
    ['http://www.bowiestate.edu/', 'Bowie State University'],
    ['http://www.bgsu.edu/', 'Bowling Green State University'],
    ['http://www.bradford.edu/', 'Bradford College'],
    ['http://www.bradley.edu/', 'Bradley University'],
    ['http://www.brandeis.edu/', 'Brandeis University'],
    ['http://www.brenau.edu/', 'Brenau University'],
    ['http://www.brevard.edu', 'Brevard College'],
    ['http://www.bpc.edu/', 'Brewton-Parker College'],
    ['http://www.briarcliff.edu/', 'Briar Cliff University'],
    ['http://www.bridgewater.edu/', 'Bridgewater College'],
    ['http://www.bridgew.edu/', 'Bridgewater State College'],
    ['http://www.byu.edu/', 'Brigham Young University'],
    ['http://www.byuh.edu/', 'Brigham Young University Hawaii'],
    ['http://www.byui.edu/', 'Brigham Young University Idaho'],
    ['http://www.brooklyn.cuny.edu/', 'Brooklyn College'],
    ['http://www.brooklaw.edu/', 'Brooklyn Law School'],
    ['http://www.brooks.edu', 'Brooks Institute'],
    ['http://www.brown.edu/', 'Brown University'],
    ['http://www.bryan.edu', 'Bryan College'],
    ['http://www.bryant.edu/', 'Bryant College'],
    ['http://www.brynmawr.edu/', 'Bryn Mawr College'],
    ['http://www.bucknell.edu/', 'Bucknell University'],
    ['http://www.bvu.edu/', 'Buena Vista University'],
    ['http://www.buffalostate.edu/', 'http://www.butler.edu/', 'Butler University'],
    ['http://www.crdrewu.edu/', 'C. R. Drew University of Medicine and Science'],
    ['http://www.cabarruscollege.edu', 'Cabarrus College of Health Sciences'],
    ['http://www.cabrini.edu', 'Cabrini College'],
    ['http://www.caldwell.edu/', 'Caldwell College'],
    ['http://www.calbaptist.edu', 'California Baptist University'],
    ['http://www.calcoast.edu', 'California Coast University'],
    ['http://www.cca.edu', 'California College of the Arts'],
    ['http://www.cchs.edu/', 'California College for Health Sciences'],
    ['http://www.ccpm.edu/', 'California College of Podiatric Medicine'],
    ['http://www.calarts.edu/', 'California Institute of the Arts'],
    ['http://www.cihs.edu/', 'California Institute for Human Science'],
    ['http://www.ciis.edu/', 'California Institute of Integral Studies'],
    ['http://www.caltech.edu/', 'California Institute of Technology'],
    ['http://www.callutheran.edu/', 'California Lutheran University'],
    ['http://www.csum.edu/', 'The California Maritime Academy'],
    ['http://www.cnuas.edu/', 'California National University for Advanced Studies'],
    ['http://www.cpu.edu/', 'California Pacific University'],
    ['http://www.calpoly.edu/', 'California Polytechnic State University, San Luis Obispo'],
    ['http://www.csupomona.edu/', 'California State Polytechnic University, Pomona'],
    ['http://www.csubak.edu/', 'California State University, Bakersfield'],
    ['http://www.csuci.edu/', 'California State University, Channel Islands'],
    ['http://www.csuchico.edu/', 'California State University, Chico'],
    ['http://www.csudh.edu/', 'California State University, Dominguez Hills'],
    ['http://www.csufresno.edu/', 'California State University, Fresno'],
    ['http://www.fullerton.edu', 'California State University, Fullerton'],
    ['http://www.csuhayward.edu/', 'California State University, Hayward'],
    ['http://www.csulb.edu/', 'California State University, Long Beach'],
    ['http://www.calstatela.edu/', 'California State University, Los Angeles'],
    ['http://www.monterey.edu/', 'California State University, Monterey'],
    ['http://www.csun.edu/', 'California State University, Northridge'],
    ['http://www.csus.edu/', 'California State University, Sacramento'],
    ['http://www.csusb.edu/', 'California State University, San Bernardino'],
    ['http://www.csusm.edu/', 'California State University, San Marcos'],
    ['http://www.csustan.edu/', 'California State University, Stanislaus'],
    ['http://www.cup.edu/', 'California University of Pennsylvania'],
    ['http://www.ccsj.edu/', 'Calumet College of St. Joseph'],
    ['http://www.calvin.edu/', 'Calvin College'],
    ['http://www.cambridgecollege.edu', 'Cambridge College'],
    ['http://www.cameron.edu/', 'Cameron University'],
    ['http://www.campbell.edu/', 'Campbell University'],
    ['http://www.campbellsville.edu/', 'Campbellsville University'],
    ['http://www.canisius.edu/', 'Canisius College'],
    ['http://www.canyoncollege.edu/home.htm', 'Canyon College'],
    ['http://www.capella.edu/', 'Capella University'],
    ['http://www.capital.edu/', 'Capital University'],
    ['http://www.capitol-college.edu/', 'Capitol College'],
    ['http://www.stritch.edu/', 'Cardinal Stritch University'],
    ['http://www.carleton.edu/', 'Carleton College'],
    ['http://www.albizu.edu', 'Carlos Albizu University'],
    ['http://www.carlow.edu/', 'Carlow College'],
    ['http://www.ciw.edu/', 'Carnegie Institution of Washington'],
    ['http://www.cmu.edu/', 'Carnegie Mellon University'],
    ['http://www.cc.edu', 'Carrol University'],
    ['http://www.cn.edu/', 'http://www.carroll.edu/', 'Carroll College, Helena, MT'],
    ['http://www.cc.edu', 'http://www.cn.edu/', 'Carson-Newman College'],
    ['http://www.carthage.edu/', 'Carthage College'],
    ['http://www.cwru.edu/', 'Case Western Reserve University'],
    ['http://www.csc.vsc.edu/', 'Castleton State College'],
    ['http://www.catawba.edu/', 'Catawba College'],
    ['http://www.cua.edu/', 'The Catholic University of America'],
    ['http://www.cazenovia.edu', 'Cazenovia College'],
    ['http://www.cedarcrest.edu/', 'Cedar Crest College'],
    ['http://www.cedarville.edu/', 'Cedarville University'],
    ['http://www.centenary.edu/', 'Centenary College of Louisiana'],
    ['http://www.centenarycollege.edu/', 'Centenary College of New Jersey'],
    ['http://www.ccscad.edu/', 'Center for Creative Studies College of Art and Design'],
    ['http://www.cbcag.edu', 'Central Bible College'],
    ['http://www.cccb.edu', 'Central Christian College of the Bible'],
    ['http://www.centralchristian.edu', 'Central Christian College of Kansas'],
    ['http://www.central.edu/', 'Central College'],
    ['http://www.ccsu.edu/', 'Central Connecticut State University'],
    ['http://www.cmc.edu/', 'Central Methodist College'],
    ['http://www.cmich.edu/', 'Central Michigan University'],
    ['http://www.cmsu.edu/', 'Central Missouri State University'],
    ['http://www.centralpenn.edu', 'Central Pennsylvania College'],
    ['http://www.centralstate.edu/', 'Central State University'],
    ['http://www.cwu.edu/', 'Central Washington University'],
    ['http://www.centre.edu/', 'Centre College, Danville Kentucky'],
    ['http://www.centuryuniversity.edu/', 'Century University'],
    ['http://www.csc.edu/', 'Chadron State College'],
    ['http://www.chadwick.edu/', 'Chadwick University'],
    ['http://www.chaminade.edu/', 'Chaminade University of Honolulu, Hawaii'],
    ['http://www.champlain.edu', 'Champlain College'],
    ['http://www.chapman.edu', 'Chapman University'],
    ['http://www.cdrewu.edu/', 'Charles R. Drew University of Medicine and Science'],
    ['http://www.csuniv.edu', 'Charleston Southern'],
    ['http://www.cosc.edu/', 'Charter Oak State College'],
    ['http://www.chatham.edu', 'Chatham College'],
    ['http://www.cheyney.edu', 'Cheyney University of Pennsylvania'],
    ['http://www.kentlaw.edu', 'Chicago-Kent College of Law'],
    ['http://www.thechicagoschool.edu', 'Chicago School of Professional Psychology'],
    ['http://www.csu.edu/', 'Chicago State University'],
    ['http://www.chowan.edu/', 'Chowan College'],
    ['http://www.christendom.edu/', 'Christendom College'],
    ['http://www.cbcs-degree.com', 'Christian Bible College and Seminary'],
    ['http://www.cbu.edu/', 'Christian Brothers University'],
    ['http://www.cnu.edu/', 'Christopher Newport University'],
    ['http://www.biblecollege.edu/', 'Circleville Bible College'],
    ['http://www.citadel.edu/', 'The Citadel'],
    ['http://www.ccc.edu/', 'City Colleges of Chicago'],
    ['http://www.cityu.edu/', 'City University, Bellevue Washington'],
    ['http://www.cula.edu/', 'City University of Los Angeles'],
    ['http://www.cuny.edu/', 'City University of New York'],
    ['http://www.scicu.org/claflin/cchome.htm', 'Claflin College'],
    ['http://www.cgs.edu/', 'Claremont Graduate University'],
    ['http://www.cmc.edu', 'Claremont McKenna College'],
    ['http://www.clarion.edu/', 'Clarion University'],
    ['http://www.cau.edu/', 'Clark Atlanta University'],
    ['http://www.clark.edu/', 'Clark College'],
    ['http://www.clarku.edu/', 'Clark University'],
    ['http://www.clarke.edu/', 'Clarke College'],
    ['http://www.clarkson.edu/', 'Clarkson University'],
    ['http://www.clayton.edu/', 'Clayton College and State University'],
    ['http://www.ccnh.edu/', 'Clayton College of Natural Health'],
    ['http://www.clemson.edu/', 'Clemson University'],
    ['http://www.ccbbc.edu/', 'Clear Creek Baptist Bible College'],
    ['http://www.clearwater.edu', 'Clearwater Christian College'],
    ['http://www.cleary.edu/', 'Cleary University'],
    ['http://www.clevelandchiropractic.edu/', 'Cleveland Chiropractic College'],
    ['http://www.cia.edu/', 'Cleveland Institute of Art'],
    ['http://www.cim.edu/', 'Cleveland Institute of Music'],
    ['http://www.csuohio.edu/', 'Cleveland State University'],
    ['http://www.clinch.edu/', 'Clinch Valley College'],
    ['http://www.coastal.edu/', 'Coastal Carolina University'],
    ['http://www.coe.edu/', 'Coe College'],
    ['http://www.cogswell.edu/', 'Cogswell Polytechnical College'],
    ['http://www.coker.edu/', 'Coker College'],
    ['http://www.colby.edu/', 'Colby College'],
    ['http://www.colby-sawyer.edu/', 'Colby-Sawyer College'],
    ['http://www.colgate.edu/', 'Colgate University'],
    ['http://www.coleman.edu/', 'Coleman College'],
    ['http://www.aero.edu/', 'http://www.coa.edu/', 'College of the Atlantic'],
    ['http://www.cofc.edu/', 'College of Charleston'],
    ['http://www.ceu.edu/', 'College of Eastern Utah'],
    ['http://www.holycross.edu/', 'College of the Holy Cross'],
    ['http://www.collegeofidaho.edu', 'College of Idaho'],
    ['http://www.tci.edu/', 'The College of Insurance'],
    ['http://www.cms.edu/', 'The College of Metaphysical Studies'],
    ['http://www.misericordia.edu/', 'College Misericordia'],
    ['http://www.msj.edu/', 'College of Mount Saint Joseph'],
    ['http://www.mountsaintvincent.edu', 'College of Mount Saint Vincent'],
    ['http://www.tcnj.edu', 'The College of New Jersey'],
    ['http://www.cnr.edu/', 'College of New Rochelle'],
    ['http://www.ndm.edu/to_nn_cnd.html', 'College of Notre Dame of Maryland'],
    ['http://www.cofo.edu/', 'College of the Ozarks'],
    ['http://www.csbsju.edu/', 'College of Saint Benedict'],
    ['http://www.stkate.edu/', 'College of Saint Catherine'],
    ['http://www.cse.edu', 'College of Saint Elizabeth'],
    ['http://www.csj.edu', 'College of Saint Joseph'],
    ['http://www.csm.edu/', 'College of Saint Mary'],
    ['http://www.css.edu/', 'College of Saint Scholastica'],
    ['http://www.cstm.edu/', 'The College of Saint Thomas More'],
    ['http://www.strose.edu/', 'The College of Saint Rose'],
    ['http://www.csf.edu/', 'The College of Santa Fe'],
    ['http://www.wm.edu/', 'College of William and Mary'],
    ['http://www.wooster.edu/', 'The College of Wooster'],
    ['http://www.ccu.edu/', 'Colorado Christian University'],
    ['http://www.coloradocollege.edu', 'Colorado College'],
    ['http://www.mines.edu/', 'Colorado School of Mines'],
    ['http://www.colostate.edu/', 'Colorado State University'],
    ['http://www.colostate-pueblo.edu', 'Colorado State - Pueblo'],
    ['http://www.colotechu.edu/', 'Colorado Technical University'],
    ['http://www.colum.edu/', 'Columbia College'],
    ['http://www.columbiacollegesc.edu', 'Columbia College, South Carolina'],
    ['http://www.ccis.edu/', 'Columbia College of Missouri'],
    ['http://www.ciu.edu/', 'Columbia International University'],
    ['http://www.colsouth.edu/', 'Columbia Southern University'],
    ['http://www.cuc.edu/', 'Columbia Union College'],
    ['http://www.columbia.edu/', 'Columbia University'],
    ['http://www.ccad.edu', 'Columbus College of Art and Design'],
    ['http://www.colstate.edu/', 'Columbus State University'],
    ['http://www.concord.wvnet.edu/', 'Concord College'],
    ['http://www.ccaa.edu/', 'Concordia College, Ann Arbor Michigan'],
    ['http://www.cuis.edu/www/cus/cutx.html', 'Concordia College, Austin Texas'],
    ['http://www.concordia-ny.edu', 'Concordia College, Bronxville, New York'],
    ['http://www.cord.edu/', 'Concordia College, Moorhead Minnesota'],
    ['http://www.csp.edu/', 'Concordia College, Saint Paul Minnesota'],
    ['http://www.concordiaselma.edu', 'Concordia College, Selma Alabama'],
    ['http://www.cune.edu', 'Concordia College, Seward Nebraska'],
    ['http://www.cui.edu', 'Concordia University, Irvine California'],
    ['http://www.cuw.edu/', 'Concordia University, Mequon Wisconsin'],
    ['http://www.cu-portland.edu/', 'Concordia University, Portland Oregon'],
    ['http://www.cuchicago.edu', 'Concordia University, Chicago'],
    ['http://camel.conncoll.edu/', 'Connecticut College'],
    ['http://www.converse.edu/', 'Converse College'],
    ['http://www.csld.edu', 'Conway School of Landscape Design'],
    ['http://www.cooper.edu/', 'Cooper Union for the Advancement of Science and Art'],
    ['http://www.coppin.edu/', 'Coppin State College'],
    ['http://www.cornellcollege.edu', 'Cornell College, Iowa'],
    ['http://www.corcoran.org/college/', 'Corcoran College of Art + Design'],
    ['http://www.cornell.edu/', 'Cornell University'],
    ['http://www.cornerstone.edu/', 'Cornerstone University'],
    ['http://www.cornish.edu/', 'Cornish College of the Arts'],
    ['http://www.cottey.edu', 'Cottey College'],
    ['http://www.covenant.edu/', 'Covenant College'],
    ['http://www.creighton.edu/', 'Creighton University'],
    ['http://www.crichton.edu/', 'Crichton College'],
    ['http://www.crossroadscollege.edu', 'Crossroads College'],
    ['http://www.crown.edu/', 'Crown College'],
    ['http://www.culver.edu/', 'Culver-Stockton College'],
    ['http://www.cumber.edu/', 'Cumberland College'],
    ['http://www.cumberland.edu/', 'Cumberland University'],
    ['http://www.curry.edu:8080/', 'Curry College'],
    ['http://198.120.22.12/', 'Cypress College'],
    ['http://www.daemen.edu/', 'Daemen College'],
    ['http://www.dsu.edu/', 'Dakota State University'],
    ['http://www.dwu.edu/', 'Dakota Wesleyan University'],
    ['http://www.dbu.edu/', 'Dallas Baptist University'],
    ['http://dts.edu', 'Dallas Theological Seminary'],
    ['http://www.dana.edu/', 'Dana College'],
    ['http://www.dwc.edu/', 'Daniel Webster College'],
    ['http://www.dartmouth.edu/', 'Dartmouth College'],
    ['http://www.davenport.edu/', 'Davenport College'],
    ['http://www.davidson.edu/', 'Davidson College'],
    ['http://www.davisandelkins.edu', 'Davis and Elkins College'],
    ['http://www.davisny.edu', 'Davis College'],
    ['http://198.168.48.7/', 'Dawson College'],
    ['http://www.dean.edu', 'Dean College'],
    ['http://praxis.deepsprings.edu/', 'Deep Springs College'],
    ['http://www.defiance.edu/', 'Defiance College'],
    ['http://www.dsc.edu/', 'Delaware State University'],
    ['http://www.delval.edu/cms/index.php', 'Delaware Valley College'],
    ['http://www.delta.edu/', 'Delta College'],
    ['http://www.deltastate.edu', 'Delta State University'],
    ['http://www.denison.edu/', 'Denison University'],
    ['http://www.denverseminary.edu/', 'Denver Seminary'],
    ['http://www.depaul.edu/', 'DePaul University'],
    ['http://www.depauw.edu/', 'DePauw University'],
    ['http://www.desales.edu/', 'DeSales University'],
    ['http://www.devry.edu/', 'DeVry University'],
    ['http://www.devrycols.edu/', 'DeVry University, Columbus'],
    ['http://www.dvc.edu/', 'Diablo Valley College'],
    ['http://www.dickinson.edu/', 'Dickinson College'],
    ['http://www.dsu.nodak.edu/', 'Dickinson State University'],
    ['http://www.dmac.edu', 'Digital Media Arts College'],
    ['http://www.dillard.edu/', 'Dillard University'],
    ['http://www.dixie.edu/', 'Dixie State College'],
    ['http://www.doane.edu/', 'Doane College'],
    ['http://www.dc.edu/', 'Dominican College'],
    ['http://www.dom.edu/', 'Dominican University'],
    ['http://www.dominican.edu/', 'Dominican University of California'],
    ['http://www.dordt.edu:7000/', 'Dordt College'],
    ['http://www.dowling.edu/', 'Dowling College'],
    ['http://www.drake.edu', 'Drake University'],
    ['http://www.drew.edu/', 'Drew University'],
    ['http://www.drexel.edu/', 'Drexel University'],
    ['http://www.drury.edu/', 'Drury University'],
    ['http://www.duke.edu/', 'Duke University'],
    ['http://www.duq.edu/', 'Duquesne University'],
    ['http://www.dyc.edu/', "D'Youville College"],
    ['http://www.earlham.edu/', 'Earlham College'],
    ['http://www.ecu.edu/', 'East Carolina University'],
    ['http://www.ecok.edu/', 'East Central University, Ada Oklahoma'],
    ['http://www.esu.edu/', 'East Stroudsburg State University'],
    ['http://www.etsu.edu', 'East Tennessee State University'],
    ['http://www.etbu.edu', 'East Texas Baptist University'],
    ['http://www.eastwest.edu', 'East-West University'],
    ['http://www.eastern.edu/', 'Eastern College'],
    ['http://www.easternct.edu/', 'Eastern Connecticut State University'],
    ['http://www.eiu.edu/', 'Eastern Illinois University'],
    ['http://www.eku.edu/', 'Eastern Kentucky University'],
    ['http://www.emu.edu/', 'Eastern Mennonite University'],
    ['http://www.emich.edu/', 'Eastern Michigan University'],
    ['http://www.enc.edu/', 'Eastern Nazarene College'],
    ['http://www.enmu.edu/', 'Eastern New Mexico University'],
    ['http://www.eou.edu/', 'Eastern Oregon University'],
    ['http://www.ewu.edu/', 'Eastern Washington University'],
    ['http://www.eckerd.edu/', 'Eckerd College'],
    ['http://www.edgewood.edu/', 'Edgewood College'],
    ['http://www.edinboro.edu/', 'Edinboro University of Pennsylvania'],
    ['http://www.ewc.edu/', 'Edward Waters College'],
    ['http://www.ecsu.edu/', 'Elizabeth City State University'],
    ['http://www.etown.edu/', 'Elizabethtown College'],
    ['http://www.elmhurst.edu/', 'Elmhurst College'],
    ['http://www.elmira.edu/', 'Elmira College'],
    ['http://www.elms.edu/', 'Elms College'],
    ['http://www.elon.edu/', 'Elon University'],
    ['http://macwww.db.erau.edu/', 'Embry-Riddle Aeronautical University'],
    ['http://www.emerson.edu/', 'Emerson College'],
    ['http://www.emmanuel.edu/', 'Emmanuel College'],
    ['http://www.emmaus.edu/', 'Emmaus Bible College'],
    ['http://www.emory.edu/', 'Emory University'],
    ['http://www.ehc.edu/', 'Emory & Henry College'],
    ['http://www.esc.edu', 'Empire State College'],
    ['http://www.emporia.edu/', 'Emporia State University'],
    ['http://www.endicott.edu/', 'Endicott College'],
    ['http://www.erskine.edu/', 'Erskine College'],
    ['http://www.eureka.edu/', 'Eureka College'],
    ['http://www.evangel.edu/', 'Evangel University'],
    ['http://www.evergladesuniversity.edu', 'Everglades University'],
    ['http://www.evergreen.edu/', 'Evergreen State College'],
    ['http://www.excelsior.edu/', 'Excelsior College'],
    ['http://www.fairfield.edu/', 'Fairfield University'],
    ['http://www.fdu.edu/', 'Fairleigh Dickinson University'],
    ['http://www.fscwv.edu/', 'Fairmont State College'],
    ['http://www.faith.edu/', 'Faith Baptist Bible College and Theological Seminary'],
    ['http://www.faulkner.edu/', 'Faulkner University'],
    ['http://www.uncfsu.edu/', 'Fayetteville State University'],
    ['http://www.felician.edu/', 'Felician College'],
    ['http://www.ferris.edu/', 'Ferris State University'],
    ['http://www.ferrum.edu/', 'Ferrum College'],
    ['http://www.fielding.edu/', 'Fielding Graduate University'],
    ['http://www.finchcms.edu/', 'Finch University of Health Sciences/The Chicago Medical School'],
    ['http://www.finlandia.edu', 'Finlandia University'],
    ['http://www.fisk.edu/', 'Fisk University'],
    ['http://www.fsc.edu/', 'Fitchburg State College'],
    ['http://www.flagler.edu/', 'Flagler College'],
    ['http://www.famu.edu/', 'Florida A &amp M University'],
    ['http://www.fau.edu/', 'Florida Atlantic University'],
    ['http://www.fcc.edu/', 'Florida Christian College'],
    ['http://www.floridacollege.edu', 'Florida College'],
    ['http://www.fgcu.edu/', 'Florida Gulf Coast University'],
    ['http://www.fit.edu/', 'Florida Institute of Technology'],
    ['http://www.fiu.edu/', 'Florida International University'],
    ['http://www.fmc.edu/', 'Florida Memorial College'],
    ['http://www.cci.edu/', 'Florida Metropolitan University'],
    ['http://www.flsouthern.edu/', 'Florida Southern College'],
    ['http://www.fsu.edu/', 'Florida State University'],
    ['http://www.fontbonne.edu/', 'Fontbonne University'],
    ['http://www.fordham.edu/', 'Fordham University'],
    ['http://www.forestinstitute.org/', 'Forest Institute of Professional Psychology'],
    ['http://www.fhsu.edu/', 'Fort Hays State University'],
    ['http://www.fortlewis.edu/', 'Fort Lewis College'],
    ['http://www.fvsu.edu', 'Fort Valley State University'],
    ['http://www.framingham.edu/', 'Framingham State College'],
    ['http://www.fmarion.edu/', 'Francis Marion University'],
    ['http://www.franuniv.edu/', 'Franciscan University of Steubenville'],
    ['http://www.fandm.edu/', 'Franklin and Marshall College'],
    ['http://www.franklincollege.edu', 'Franklin College'],
    ['http://www.franklinpierce.edu', 'Franklin Pierce University'],
    ['http://www.fplc.edu/', 'Franklin Pierce Law Center'],
    ['http://www.franklin.edu/', 'Franklin University'],
    ['http://www.olin.edu', 'Franklin W. Olin College of Engineering'],
    ['http://www.fhu.edu/', 'Freed-Hardeman University'],
    ['http://www.fwbbc.edu/', 'Freewill Baptist Bible College'],
    ['http://www.fresno.edu/', 'Fresno Pacific University'],
    ['http://www.friends.edu/', 'Friends University'],
    ['http://www.fsu.umd.edu/', 'Frostburg State University'],
    ['http://www.fullsail.edu', 'Full Sail University'],
    ['http://www.fuller.edu/', 'Fuller Theological Seminary'],
    ['http://www.fullcoll.edu/', 'Fullerton College'],
    ['http://www.furman.edu/', 'Furman University'],
    ['http://www.gallaudet.edu/', 'Gallaudet University'],
    ['http://www.gannon.edu/', 'Gannon University'],
    ['http://www.gardner-webb.edu/', 'Gardner-Webb University'],
    ['http://www.geneva.edu/', 'Geneva College'],
    ['http://www.georgefox.edu/', 'George Fox University'],
    ['http://www.gmu.edu/', 'George Mason University'],
    ['http://www.gwu.edu', 'George Washington University'],
    ['http://www.georgetowncollege.edu/', 'Georgetown College'],
    ['http://www.georgetown.edu/', 'Georgetown University'],
    ['http://www.georgian.edu/', 'Georgian Court College'],
    ['http://www.gcsu.edu/', 'Georgia College and State University'],
    ['http://www.gatech.edu/', 'Georgia Institute of Technology'],
    ['http://www.gpc.peachnet.edu', 'Georgia Perimeter College'],
    ['http://www.georgiasouthern.edu', 'Georgia Southern University'],
    ['http://www.gsw.edu/', 'Georgia Southwestern State University'],
    ['http://www.gsu.edu/', 'Georgia State University'],
    ['http://www.georgian.edu/', 'Georgian Court College'],
    ['http://www.gettysburg.edu/', 'Gettysburg College'],
    ['http://www.globeuniversity.edu/', 'Globe University'],
    ['http://www.glenville.wvnet.edu/', 'Glenville State College'],
    ['http://www.globeinstitute.org/', 'Globe Institute of Technology'],
    ['http://www.goddard.edu/', 'Goddard College'],
    ['http://www.ggu.edu/', 'Golden Gate University'],
    ['http://www.gsbc.edu/', 'Golden State Baptist College'],
    ['http://goldey.gbc.edu/', 'Goldey-Beacom College'],
    ['http://www.gonzaga.edu/', 'Gonzaga University'],
    ['http://www.beaches.net/~gooding/', 'Gooding Institute of Nurse Anesthesia'],
    ['http://www.gordon.edu/', 'Gordon College'],
    ['http://www.gcts.edu/', 'Gordon-Conwell Theological Seminary'],
    ['http://www.goshen.edu/', 'Goshen College'],
    ['http://www.goucher.edu/', 'Goucher College'],
    ['http://www.govst.edu/', 'Governors State University'],
    ['http://www.grace.edu/', 'Grace College'],
    ['http://www.graceu.edu/', 'Grace University'],
    ['http://www.graceland.edu/', 'Graceland University'],
    ['http://www.gc.cuny.edu/', 'The Graduate Center, City University of New York'],
    ['http://www.gram.edu', 'Grambling State University'],
    ['http://www.grand-canyon.edu', 'Grand Canyon University'],
    ['http://www.gvsu.edu/', 'Grand Valley State University'],
    ['http://www.gvc.edu/', 'Grand View College'],
    ['http://www.granite.edu', 'Granite State College'],
    ['http://www.grantham.edu/', 'Grantham University'],
    ['http://www.nmc.edu/maritime', 'Great Lakes Maritime Academy'],
    ['http://greenmtn.edu/', 'Green Mountain College'],
    ['http://greenleaf.edu/', 'Greenleaf University'],
    ['http://gborocollege.edu/', 'Greensboro College'],
    ['http://www.greenville.edu/', 'Greenville College'],
    ['http://greenwich.edu/', 'Greenwich University'],
    ['http://www.grinnell.edu/', 'Grinnell College'],
    ['http://www.gcc.edu/', 'Grove City College'],
    ['http://www.guilford.edu/', 'Guilford College'],
    ['http://www.gac.edu/', 'Gustavus Adolphus College, Saint Peter, Minnesota'],
    ['http://www.gutenberg.edu', 'Gutenberg College'],
    ['http://www.gmc.edu/', 'Gwynedd-Mercy College'],
    ['http://www.hamilton.edu/', 'Hamilton College'],
    ['http://www.hamilton-university.edu/', 'Hamilton University'],
    ['http://www.hamline.edu/', 'Hamline University'],
    ['http://www.hsc.edu/', 'Hampden-Sydney College'],
    ['http://www.hampshire.edu/', 'Hampshire College'],
    ['http://www.hamptonu.edu/', 'Hampton University'],
    ['http://www.hlg.edu/', 'Hannibal-LaGrange College'],
    ['http://www.hanover.edu/', 'Hanover College'],
    ['http://www.hsutx.edu/', 'Hardin-Simmons University'],
    ['http://www.harding.edu/', 'Harding University'],
    ['http://www.interdesign.edu', 'Harrington College of Design'],
    ['http://www.hssc.edu/', 'Harris-Stowe State College'],
    ['http://www.hartwick.edu/', 'Hartwick College'],
    ['http://www.harvard.edu/', 'Harvard University'],
    ['http://www.hmc.edu/', 'Harvey Mudd College'],
    ['http://www.haskell.edu', 'Haskell Indian Nations University'],
    ['http://www.hastings.edu/', 'Hastings College'],
    ['http://www.haverford.edu/', 'Haverford College'],
    ['http://www.hpu.edu/', 'Hawaii Pacific University'],
    ['http://shamash.org/hc', 'Hebrew College'],
    ['http://www.heidelberg.edu/', 'Heidelberg College'],
    ['http://www.hsu.edu/', 'Henderson State Univerisity'],
    ['http://www.hendrix.edu/', 'Hendrix College'],
    ['http://www.henrycogswell.edu/', 'Henry Cogswell College'],
    ['http://www.heritage.edu/', 'Heritage University'],
    ['http://www.hesser.edu/', 'Hesser College'],
    ['http://www.hesston.edu/', 'Hesston College'],
    ['http://acme.highpoint.edu/', 'High Point University'],
    ['http://www.hilbert.edu/', 'Hilbert College'],
    ['http://www.hillsdale.edu/', 'Hillsdale College'],
    ['http://www.hc.edu/', 'Hillsdale Freewill Baptist College'],
    ['http://www.hiram.edu/', 'Hiram College'],
    ['http://www.hws.edu/', 'Hobart and William Smith Colleges'],
    ['http://www.hofstra.edu/', 'Hofstra University'],
    ['http://www.hollins.edu/', 'Hollins University'],
    ['http://www.hcc-nd.edu/', 'Holy Cross College, Notre Dame Indiana'],
    ['http://www.hfc.edu/', 'Holy Family College'],
    ['http://www.hnu.edu', 'Holy Names University'],
    ['http://www.hood.edu/', 'Hood College'],
    ['http://www.hope.edu/', 'Hope College'],
    ['http://www.houghton.edu/', 'Houghton College'],
    ['http://www.hbu.edu/', 'Houston Baptist University'],
    ['http://www.hputx.edu/', 'Howard Payne University'],
    ['http://www.howard.edu/', 'Howard University'],
    ['http://www.hult.edu', 'Hult International Business School'],
    ['http://www.humboldt.edu/', 'Humboldt State University'],
    ['http://www.hunter.cuny.edu/', 'Hunter College'],
    ['http://www.huntingdon.edu/', 'Huntingdon College'],
    ['http://www.huntington.edu', 'Huntington University'],
    ['http://www.huron.edu/', 'Huron University'],
    ['http://www.husson.edu/', 'Husson College'],
    ['http://www.htc.edu/', 'Huston-Tillotson College'],
    ['http://www.isu.edu/', 'Idaho State University'],
    ['http://www.ic.edu/', 'Illinois College'],
    ['http://www.iit.edu/', 'Illinois Institute of Technology'],
    ['http://www.ilstu.edu/', 'Illinois State University'],
    ['http://www.iwu.edu/', 'Illinois Wesleyan University'],
    ['http://www.immaculata.edu/', 'Immaculata College'],
    ['http://www.indianatech.edu', 'Indiana Institute of Technology'],
    ['http://www.indstate.edu/', 'Indiana State University'],
    ['http://www.indwes.edu/', 'Indiana Wesleyan University'],
    ['http://www.indiana.edu/', 'Indiana University'],
    ['http://www.iun.edu', 'Indiana University Northwest'],
    ['http://www.iup.edu/', 'Indiana University of Pennsylvania'],
    ['http://www.iusb.edu/', 'Indiana University at South Bend'],
    ['http://www.ius.edu', 'Indiana University Southeast'],
    ['http://www.columbus.iupui.edu/', 'Indiana University - Purdue University, Columbus'],
    ['http://www.ipfw.edu', 'Indiana University - Purdue University, Fort Wayne'],
    ['http://www.iupui.edu/', 'Indiana University - Purdue University, Indianapolis'],
    ['http://members.tripod.com/~InstituteCW/home.html', 'Institute for Christian Works'],
    ['http://www.ictcollege.edu/', 'Institute of Computer Technology'],
    ['http://www.ipst.edu/', 'Institute of Paper Science and Technology'],
    ['http://www.itp.edu/', 'Institute for Transpersonal Psychology'],
    ['http://metro.inter.edu/', 'Inter American University of Puerto Rico'],
    ['http://www.internationalcollege.edu/', 'International College'],
    ['http://www.ifac.edu/', 'International Fine Arts College'],
    ['http://www.aibt.edu/', 'International Institue of the Americas'],
    ['http://www.iru.edu/', 'International Reform University'],
    ['http://www.iona.edu/', 'Iona College'],
    ['http://www.iastate.edu/', 'Iowa State University'],
    ['http://www.iwc.edu/', 'Iowa Wesleyan College'],
    ['http://www.irvineuniversity.edu', 'Irvine University College of Law'],
    ['http://www.ithaca.edu/', 'Ithaca College'],
    ['http://www.jsums.edu', 'Jackson State University'],
    ['http://www.jsu.edu', 'Jacksonville State University'],
    ['http://www.ju.edu/', 'Jacksonville University'],
    ['http://www.jmu.edu/', 'James Madison University'],
    ['http://acc.jc.edu/', 'Jamestown College'],
    ['http://www.jarvis.edu/', 'Jarvis Christian College'],
    ['http://www.jtsa.edu/', 'Jewish Theological Seminary'],
    ['http://www.jbu.edu/', 'John Brown University'],
    ['http://www.jcu.edu/', 'John Carroll University'],
    ['http://www.jfku.edu/', 'John F. Kennedy University'],
    ['http://www.jjay.cuny.edu/', 'John Jay College of Criminal Justice'],
    ['http://www.jhu.edu/', 'The Johns Hopkins University'],
    ['http://www.jwu.edu/', 'Johnson and Wales University'],
    ['http://www.jcsu.edu/', 'http://www.jbc.edu', 'Johnson Bible College'],
    ['http://www.jwu.edu/', 'http://www.jcsu.edu/', 'Johnson C. Smith University'],
    ['http://www.jsc.vsc.edu', 'Johnson State College'],
    ['http://www.dia.mil/jmic.html', 'Joint Military Intelligence College'],
    ['http://www.jones.edu/', 'Jones College'],
    ['http://www.international.edu/', 'Jones International University'],
    ['http://home.judson.edu/', 'Judson College, Marion AL'],
    ['http://www.judson-il.edu/', 'Judson College, Elgin IL'],
    ['http://www.julliard.edu/', 'The Julliard School'],
    ['http://www.juniata.edu/', 'Juniata College'],
    ['http://www.kzoo.edu/', 'Kalamazoo College'],
    ['http://www.kcai.edu/', 'Kansas City Art Institute'],
    ['http://www.ksnewman.edu/', 'Kansas Newman College'],
    ['http://www.ksu.edu/', 'Kansas State University'],
    ['http://www.kwu.edu/', 'Kansas Wesleyan University'],
    ['http://www.kaplan.edu', 'Kaplan University'],
    ['http://www.kean.edu/', 'Kean University'],
    ['http://www.kgi.edu/', 'Keck Graduate Institute'],
    ['http://www.keene.edu/', 'Keene State College'],
    ['http://www.keiseruniversity.edu/', 'Keiser University'],
    ['http://www.kendall.edu', 'Kendall College'],
    ['http://kw.edu/', 'Kennedy-Western University'],
    ['http://www.kennesaw.edu/', 'Kennesaw State University'],
    ['http://www.kent.edu/', 'Kent State University'],
    ['http://www.kcc.edu/', 'Kentucky Christian College'],
    ['http://www.kysu.edu/', 'Kentucky State University'],
    ['http://www.kwc.edu/', 'Kentucky Wesleyan College'],
    ['http://www.kenyon.edu/', 'Kenyon College'],
    ['http://www.kettering.edu/', 'Kettering University'],
    ['http://www.keuka.edu/', 'Keuka College'],
    ['http://www.king.edu/', 'King College'],
    ['http://www.kings.edu/', "King's College, Wilkes-Barre, PA"],
    ['http://www.tkc.edu/', "The King's College, New York City, NY"],
    ['http://www.knox.edu/', 'Knox College'],
    ['http://www.knoxseminary.org/', 'Knox Theological Seminary'],
    ['http://www.knoxvillecollege.edu', 'Knoxville College'],
    ['http://www.kutztown.edu/', 'Kutztown University of Pennsylvania'],
    ['http://www.laroche.edu/', 'La Roche College'],
    ['http://www.lasalle.edu/', 'La Salle University'],
    ['http://www.lasierra.edu/', 'La Sierra University'],
    ['http://www.lafayette.edu/', 'Lafayette College'],
    ['http://www.lagrange.edu/', 'LaGrange College'],
    ['http://www.lakeerie.edu/', 'Lake Erie College'],
    ['http://www.lfc.edu/', 'Lake Forest College'],
    ['http://www.lakeforestmba.edu', 'Lake Forest Graduate School of Management'],
    ['http://www.lssu.edu/', 'Lake Superior State University'],
    ['http://www.lakeland.edu/', 'Lakeland College'],
    ['http://www.lamar.edu/', 'Lamar University'],
    ['http://www.lambuth.edu/', 'Lambuth University'],
    ['http://www.lbc.edu/', 'Lancaster Bible College'],
    ['http://www.lts.org/', 'Lancaster Theological Seminary'],
    ['http://www.lander.edu/', 'Lander University'],
    ['http://www.landmarkcollege.org/', 'Landmark College'],
    ['http://www.lunet.edu/', 'Langston University'],
    ['http://www.lanecollege.edu/', 'Lane College'],
    ['http://www.lasell.edu/', 'Lasell College'],
    ['http://www.ltu.edu/', 'Lawrence Technological University'],
    ['http://www.lawrence.edu/', 'Lawrence University'],
    ['http://www.lemoyne.edu/', 'Le Moyne College'],
    ['http://www.lvc.edu/', 'Lebanon Valley College'],
    ['http://www.lee.edu/', 'Lee College'],
    ['http://www.leeuniversity.edu/', 'Lee University'],
    ['http://www.lmc.edu/', 'Lees-McRae College'],
    ['http://www.lehigh.edu/', 'Lehigh Univervsity'],
    ['http:/www.lemoyne.edu', 'Le Moyne College'],
    ['http://www.lemoyne-owen.edu/', 'LeMoyne-Owen College'],
    ['http://www.lrc.edu/', 'Lenoir-Rhyne College'],
    ['http://members.aol.com/liwt/', 'Lenox Institute of Water Technology'],
    ['http://www.lesley.edu/', 'Lesley University'],
    ['http://www.letu.edu/', 'LeTourneau University'],
    ['http://www.lclark.edu/', 'Lewis &amp Clark College'],
    ['http://www.lcsc.edu/', 'Lewis-Clark State College'],
    ['http://www.lewisu.edu/', 'Lewis University'],
    ['http://www.liberty.edu/', 'Liberty University'],
    ['http://www.lifepacific.edu', 'Life Pacific College'],
    ['http://www.life.edu/', 'Life University'],
    ['http://www.limestone.edu/', 'Limestone College'],
    ['http://www.lccs.edu/', 'Lincoln Christian College and Seminary'],
    ['http://www.lincoln.mclean.il.us/', 'Lincoln College'],
    ['http://www.lmunet.edu/', 'Lincoln Memorial University'],
    ['http://www.lincolnu.edu/', 'Lincoln University, Jefferson City Missouri'],
    ['http://www.lincolnuca.edu/', 'Lincoln University, San Francisco California'],
    ['http://www.lincoln.edu/', 'Lincoln University of Pennsylvania'],
    ['http://www.lindenwood.edu/', 'Lindenwood College'],
    ['http://www.lindsey.edu/', 'Lindsey Wilson College'],
    ['http://www.linfield.edu/', 'Linfield College'],
    ['http://www.lipscomb.edu/', 'Lipscomb University'],
    ['http://www.lhup.edu/', 'Lock Haven University'],
    ['http://www.logan.edu/', 'Logan College of Chiropractic'],
    ['http://www.llu.edu/', 'Loma Linda University'],
    ['http://www.liunet.edu/', 'Long Island University'],
    ['http://www.lwc.edu/', 'Longwood College'],
    ['http://www.loras.edu/', 'Loras College'],
    ['http://www.louisburg.edu/', 'Louisburg College'],
    ['http://www.lbu.edu/', 'Louisiana Baptist Universty'],
    ['http://www.lacollege.edu/', 'Louisiana College'],
    ['http://www.lsua.edu/', 'Louisiana State University at Alexandria'],
    ['http://www.lsu.edu/', 'Louisiana State University at Baton Rouge'],
    ['http://www.lsumc.edu/', 'Louisiana State University Health Sciences Center New Orleans'],
    ['http://www.lsus.edu/', 'Louisiana State University at Shreveport'],
    ['http://www.latech.edu/', 'Louisiana Tech University'],
    ['http://www.lourdes.edu', 'Lourdes College'],
    ['http://www.loyola.edu/', 'Loyola College, Baltimore'],
    ['http://www.lmu.edu/', 'Loyola Marymount University'],
    ['http://www.luc.edu/', 'Loyola University, Chicago'],
    ['http://www.loyno.edu/', 'Loyola University, New Orleans'],
    ['http://www.lcu.edu/', 'Lubbock Christian University'],
    ['http://www.luther.edu/', 'Luther College'],
    ['http://www.luthersem.edu/', 'Luther Seminary'],
    ['http://www.lbi.edu/', 'Lutheran Bible Institute'],
    ['http://www.ltsg.edu/', 'Lutheran Theological Seminary at Gettysburg'],
    ['http://www.lycoming.edu/', 'Lycoming College'],
    ['http://lymeacademy.edu/', 'Lyme Academy of Fine Arts'],
    ['http://www.lynchburg.edu/', 'Lynchburg College'],
    ['http://www.lsc.vsc.edu/', 'Lyndon State College'],
    ['http://www.lynn.edu/', 'Lynn University'],
    ['http://www.lyon.edu/', 'Lyon College'],
    ['http://www.macalester.edu', 'Macalester College'],
    ['http://www.mac.edu/', 'MacMurray College'],
    ['http://www.madonna.edu', 'Madonna University'],
    ['http://www.magdalen.edu', 'Magdalen College'],
    ['http://mum.edu/', 'Maharishi University of Management'],
    ['http://www.meca.edu/', 'Maine College of Art'],
    ['http://www.state.me.us/maritime/mma.htm', 'Maine Maritime Academy'],
    ['http://www.malone.edu/', 'Malone College'],
    ['http://www.manchester.edu/', 'Manchester College'],
    ['http://www.mancol.edu/', 'Manhattan College'],
    ['http://www.manhattanville.edu/', 'Manhattanville College'],
    ['http://www.mnsfld.edu/', 'Mansfield University'],
    ['http://www.mbbc.edu/', 'Maranatha Baptist Bible College'],
    ['http://www.marian.edu/', 'Marian College'],
    ['http://www.marietta.edu/', 'Marietta College'],
    ['http://www.marlboro.edu/', 'Marlboro College'],
    ['http://www.gradcenter.marlboro.edu', 'Marlboro College Graduate Center'],
    ['http://www.marist.edu/', 'Marist College'],
    ['http://www.mu.edu/', 'Marquette University'],
    ['http://www.mhc.edu/', 'Mars Hill College'],
    ['http://www.marshall.edu/', 'Marshall University'],
    ['http://www.mbc.edu', 'Mary Baldwin College'],
    ['http://www.marygrove.edu', 'Marygrove College'],
    ['http://www.umw.edu', 'http://www.mica.edu/', 'Maryland Institute, College of Art'],
    ['http://www.marylhurst.edu/', 'Marylhurst University'],
    ['http://www.marymt.edu/', 'Marymount College'],
    ['http://marymount.mmm.edu/home.htm', 'Marymount Manhattan College'],
    ['http://www.marymount.edu/', 'Marymount University'],
    ['http://www.maryvillecollege.edu/', 'Maryville College'],
    ['http://www.maryvillestl.edu/', 'Maryville University of Saint Louis'],
    ['http://www.marywood.edu/', 'Marywood University'],
    ['http://www.massart.edu/', 'Massachusetts College of Art'],
    ['http://www.mcla.mass.edu/', 'Massachusetts College of Liberal Arts'],
    ['http://www.mcphs.edu', 'Massachusetts College of Pharmacy and Health Sciences'],
    ['http://web.mit.edu/', 'Massachusetts Institute of Technology'],
    ['http://www.mma.mass.edu/mma.html', 'Massachusetts Maritime Academy'],
    ['http://www.mspp.edu', 'Massachusetts School of Professional Psychology'],
    ['http://www.masters.edu/', "The Master's College"],
    ['http://www.mayo.edu/education/education.html', 'The Mayo Foundation'],
    ['http://www.masu.nodak.edu/', 'Mayville State University'],
    ['http://www.mcdaniel.edu', 'McDaniel College'],
    ['http://www.mcgregor.edu/', 'The McGregor School of Antioch University'],
    ['http://www.mckendree.edu/', 'McKendree College'],
    ['http://www.mcm.edu/', 'McMurry University'],
    ['http://www.mcneese.edu/', 'McNeese State University'],
    ['http://www.mcphu.edu/', 'MCP Hahnemann University'],
    ['http://www.mcpherson.edu/', 'McPherson College'],
    ['http://www.medaille.edu/', 'Medaille College'],
    ['http://www.mcg.edu/', 'Medical College of Georgia'],
    ['http://www.mco.edu/', 'Medical College of Ohio'],
    ['http://www.mcphu.edu/', 'Medical College of Pennsylvania and Hahnemann University'],
    ['http://www.mcw.edu/', 'Medical College of Wisconsin'],
    ['http://www.musc.edu/', 'Medical University of South Carolina'],
    ['http://www.mmc.edu/', 'Meharry Medical College'],
    ['http://www.menlo.edu/', 'Menlo College'],
    ['http://www.mercer.edu/', 'Mercer University'],
    ['http://www.mercy.edu', 'Mercy College'],
    ['http://www.mchs.edu/', 'Mercy College of Health Sciences'],
    ['http://www.mercyhurst.edu/', 'Mercyhurst College'],
    ['http://www.meredith.edu/', 'Meredith College'],
    ['http://www.merrimack.edu/', 'Merrimack College'],
    ['http://www.mesastate.edu/', 'Mesa State College'],
    ['http://www.messiah.edu/', 'Messiah College'],
    ['http://www.methodist.edu/', 'Methodist College'],
    ['http://www.mtso.edu/', 'Methodist Theological School in Ohio'],
    ['http://www.metropolitancollege.edu/', 'Metropolitan College'],
    ['http://www.metropolitan.edu', 'Metropolitan College of New York'],
    ['http://www.mscd.edu/', 'Metropolitan State College of Denver'],
    ['http://www.metro.msus.edu/', 'Metropolitan State University'],
    ['http://www.mcu.edu/', 'Miami Christian University'],
    ['http://www.muohio.edu/', 'Miami University of Ohio'],
    ['http://www.mji.edu', 'Michigan Jewish Institute'],
    ['http://www.msu.edu/', 'Michigan State University'],
    ['http://www.mtu.edu/', 'Michigan Technological University'],
    ['http://www.manc.edu/', 'Mid-America Nazarene University'],
    ['http://www.mgc.peachnet.edu/', 'Middle Georgia College'],
    ['http://www.mtsu.edu/', 'Middle Tennessee State University'],
    ['http://www.middlebury.edu/', 'Middlebury College'],
    ['http://www.midwesternbaptist.edu/', 'Midwestern Baptist College'],
    ['http://www.mwsu.edu/', 'Midwestern State University'],
    ['http://www.miles.edu/', 'Miles College'],
    ['http://www.millersv.edu/', 'Millersville University'],
    ['http://www.milligan.edu/', 'Milligan College'],
    ['http://www.millikin.edu/', 'Millikin University'],
    ['http://www.mills.edu/', 'Mills College'],
    ['http://www.millsaps.edu/', 'Millsaps College'],
    ['http://www.msoe.edu/', 'Milwaukee School of Engineering'],
    ['http://www.mcad.edu/', 'Minneapolis College of Art and Design'],
    ['http://www.mnsu.edu/', 'Minnesota State University Mankato'],
    ['http://www.mnstate.edu/', 'Minnesota State University Moorhead'],
    ['http://warp6.cs.misu.nodak.edu/', 'Minot State University'],
    ['http://www.misu-b.nodak.edu', 'Minot State University--Bottineau'],
    ['http://www.mc.edu/', 'Mississippi College'],
    ['http://www.msstate.edu/', 'Mississippi State University'],
    ['http://www.muw.edu/', 'Mississippi University for Women'],
    ['http://www.mvsu.edu/', 'Mississippi Valley State University'],
    ['http://www.mobap.edu/', 'Missouri Baptist College'],
    ['http://www.mssc.edu/', 'Missouri Southern State College'],
    ['http://www.missouristate.edu', 'Missouri State University'],
    ['http://www.motech.edu/', 'Missouri Tech'],
    ['http://www.mst.edu', 'Missouri University of Science and Technology'],
    ['http://www.moval.edu/', 'Missouri Valley College'],
    ['http://www.mwsc.edu/', 'Missouri Western State College'],
    ['http://www.mitchell.edu/', 'Mitchell College'],
    ['http://www.molloy.edu/', 'Molloy College'],
    ['http://www.monm.edu/', 'Monmouth College, Monmouth Illinois'],
    ['http://www.monmouth.edu/', 'Monmouth University, West Long Branch New Jersey'],
    ['http://www.monroecollege.edu/', 'Monroe College'],
    ['http://www.msubillings.edu/', 'Montana State University-Billings'],
    ['http://www.montana.edu/', 'Montana State University-Bozeman'],
    ['http://www.msugf.edu', 'Montana State University College of Technology, Great Falls'],
    ['http://polaris.nmclites.edu/', 'Montana State University-Northern Havre'],
    ['http://www.mtech.edu/', 'Montana Tech'],
    ['http://www.montclair.edu/', 'Montclair State University'],
    ['http://www.montereylaw.edu/', 'Monterey College of Law'],
    ['http://www.miis.edu/', 'Monterey Institute of International Studies'],
    ['http://www.montreat.edu/', 'Montreat College'],
    ['http://www.moravian.edu/', 'Moravian College'],
    ['http://www.morehead-st.edu/', 'Morehead State University'],
    ['http://www.morehouse.edu/', 'Morehouse College'],
    ['http://www.msm.edu/', 'Morehouse School of Medicine'],
    ['http://www.morgan.edu/', 'Morgan State University'],
    ['http://www.morningside.edu/', 'Morningside College'],
    ['http://www.morrisbrown.edu/', 'Morris Brown College'],
    ['http://www.scicu.org/morris/mchome.htm', 'Morris College'],
    ['http://www.mtaloy.edu/', 'Mount Aloysius College'],
    ['http://www.mtholyoke.edu/', 'Mount Holyoke College'],
    ['http://www.mountida.edu/', 'Mount Ida College'],
    ['http://www.mtmc.edu/', 'Mount Marty College'],
    ['http://www.mtmary.edu/', 'Mount Mary College'],
    ['http://www.mtmercy.edu/', 'Mount Mercy College'],
    ['http://www.moc.edu', 'Mount Olive College'],
    ['http://www.msmc.edu', 'Mount Saint Mary College'],
    ['http://www.msmary.edu/', "Mount St. Mary's College and Seminary, Emmitsburg Maryland"],
    ['http://www.msmc.la.edu/', "Mount St. Mary's College, Los Angeles California"],
    ['http://www.mscfs.edu/', 'Mount Senario College'],
    ['http://www.mtsierra.com/', 'Mt. Sierra College'],
    ['http://www.muc.edu/', 'Mount Union College'],
    ['http://www.mvnc.edu/', 'Mount Vernon Nazarene College'],
    ['http://www.mountainstate.edu/', 'Mountain State University'],
    ['http://www.muhlberg.edu/', 'Muhlenberg College'],
    ['http://www.murraystate.edu', 'Murray State University'],
    ['http://www.muskingum.edu/', 'Muskingum College'],
    ['http://www.naropa.edu/', 'Naropa University'],
    ['http://www.national.edu/', 'National American University'],
    ['http://www.ndu.edu/', 'National Defense University'],
    ['http://www.nationalgradschool.org/', 'The National Graduate School'],
    ['http://nlu.nl.edu/', 'National-Louis University'],
    ['http://www.ntu.edu/', 'National Technological University'],
    ['http://www.nu.edu/', 'National University'],
    ['http://www.nuhs.edu', 'National University of Health Sciences'],
    ['http://www.nps.navy.mil/', 'The Naval Postgraduate School'],
    ['http://www.nbc.edu/', 'Nazarene Bible College'],
    ['http://www.naz.edu/', 'Nazareth College'],
    ['http://www.methodistcollege.edu/', 'Nebraska Methodist College'],
    ['http://www.nebrwesleyan.edu/', 'Nebraska Wesleyan University'],
    ['http://www.neumann.edu/', 'Neumann College'],
    ['http://nsc.nevada.edu', 'Nevada State College'],
    ['http://www.nbts.edu/', 'New Brunswick Theological Seminary'],
    ['http://www.ncf.edu/', 'New College of Florida'],
    ['http://www.nec.edu', 'New England College'],
    ['http://www.neco.edu/', 'New England College of Optometry'],
    ['http://www.newenglandconservatory.edu/', 'New England Conservatory of Music'],
    ['http://www.neit.edu/', 'New England Institute of Technology'],
    ['http://www.nesl.edu', 'New England Law'],
    ['http://www.nescom.edu', 'New England School of Communications'],
    ['http://www.njcu.edu/', 'New Jersey City University'],
    ['http://www.njit.edu/', 'New Jersey Institute of Technology'],
    ['http://www.nmhu.edu/', 'New Mexico Highlands University'],
    ['http://www.nmt.edu/', 'New Mexico Institute of Mining and Technology'],
    ['http://www.nmsu.edu/', 'New Mexico State University'],
    ['http://www.nsa.edu', 'New Saint Andrews College'],
    ['http://www.newschoolarch.edu', 'New School of Architecture and Design'],
    ['http://www.newschool.edu/', 'New School University'],
    ['http://www.mdcc.edu/nwsa', 'New World School of the Arts'],
    ['http://www.nyaa.edu/', 'New York Academy of Art'],
    ['http://www.nyit.edu/', 'New York Institute of Technology'],
    ['http://www.nyls.edu/', 'New York Law School'],
    ['http://www.nyu.edu/', 'New York University'],
    ['http://www.newberry.edu/', 'Newberry College'],
    ['http://www.newport.edu/', 'Newport University'],
    ['http://www.niagara.edu/', 'Niagara University'],
    ['http://www.nicholls.edu/', 'Nicholls State University'],
    ['http://www.nichols.edu/', 'Nichols College'],
    ['http://www.nsu.edu/', 'Norfolk State University'],
    ['http://www.ncat.edu/', 'North Carolina Agricultural and Technical State University'],
    ['http://www.nccu.edu/', 'North Carolina Central University'],
    ['http://www.ncarts.edu/', 'North Carolina School of the Arts'],
    ['http://www.ncsu.edu/', 'North Carolina State University'],
    ['http://www.ncwc.edu/', 'North Carolina Wesleyan College'],
    ['http://www.noctrl.edu/', 'North Central College'],
    ['http://www.northcentral.edu/', 'North Central University'],
    ['http://www.ndsu.nodak.edu', 'North Dakota State University--Fargo'],
    ['http://www.ngcsu.edu/', 'North Georgia College and State University, the Military College of Georgia'],
    ['http://www.ngu.edu', 'North Greenville University'],
    ['http://www.northpark.edu/', 'North Park University'],
    ['http://www.ncu.edu/', 'Northcentral University'],
    ['http://www.neiu.edu', 'Northeastern Illinois University'],
    ['http://www.neu.edu', 'Northeastern University'],
    ['http://www.nsuok.edu', 'Northeastern State University'],
    ['http://www.nau.edu', 'Northern Arizona University'],
    ['http://www.niu.edu', 'Northern Illinois University'],
    ['http://www.nku.edu', 'Northern Kentucky University'],
    ['http://www.nmu.edu', 'Northern Michigan University'],
    ['http://www.northern.edu', 'Northern State University'],
    ['http://www.northland.edu', 'Northland College'],
    ['http://www.nwcc.edu/', 'Northwest Christian College'],
    ['http://www.nca.edu/', 'Northwest College of Art'],
    ['http://www.nwmissouri.edu/', 'Northwest Missouri State University'],
    ['http://www.nnu.edu/', 'Northwest Nazarene University'],
    ['http://www.northwestu.edu', 'Northwest University'],
    ['http://www.nwalva.edu/', 'Northwestern Oklahoma State University'],
    ['http://www.nsula.edu/', 'Northwestern State University, Louisiana'],
    ['http://www.nwciowa.edu/', 'Northwestern College, Iowa'],
    ['http://www.nwc.edu/', 'Northwestern College, Saint Paul, MN'],
    ['http://www.nmc.edu/', 'Northwestern Michigan College'],
    ['http://www.northwestern.edu/', 'Northwestern University'],
    ['http://www.northwood.edu/', 'Northwood University'],
    ['http://www.norwich.edu/', 'Norwich University'],
    ['http://www.ndc.edu/', 'Notre Dame College of Ohio'],
    ['http://www.ndnu.edu/', 'Notre Dame de Namur University'],
    ['http://www.nova.edu/', 'Nova Southeastern University'],
    ['http://www.nyackcollege.edu/', 'Nyack College'],
    ['http://www.oakland.edu', 'Oakland University'],
    ['http://www.oakwood.edu/', 'Oakwood College'],
    ['http://www.oberlin.edu/', 'Oberlin College'],
    ['http://www.oxy.edu/', 'Occidental College'],
    ['http://www.oglethorpe.edu/', 'Oglethorpe University'],
    ['http://www.ohiodominican.edu', 'Ohio Dominican University'],
    ['http://www.onu.edu/', 'Ohio Northern University'],
    ['http://www.osu.edu', 'The Ohio State University'],
    ['http://www.ohiou.edu/', 'Ohio University'],
    ['http://www.ovc.edu/', 'Ohio Valley College'],
    ['http://www.owu.edu/', 'Ohio Wesleyan University'],
    ['http://www.okbu.edu/', 'Oklahoma Baptist University'],
    ['http://www.oc.edu/', 'Oklahoma Christian University'],
    ['http://www.okcu.edu/', 'Oklahoma City University'],
    ['http://www.opsu.edu/', 'Oklahoma Panhandle State University'],
    ['http://www.okstate.edu/index.html', 'Oklahoma State University'],
    ['http://tulsa.okstate.edu', 'Oklahoma State University Tulsa'],
    ['http://www.okwu.edu', 'Oklahoma Wesleyan University'],
    ['http://www.odu.edu/', 'Old Dominion University'],
    ['http://www.olin.edu/', 'Olin College of Engineering'],
    ['http://www.olivetcollege.edu/', 'Olivet College'],
    ['http://www.olivet.edu/', 'Olivet Nazarene University'],
    ['http://www.openu.edu/', 'The Open University'],
    ['http://www.oru.edu/', 'Oral Roberts University'],
    ['http://www.ogi.edu/welcome.html', 'Oregon Graduate Institute of Science and Technology'],
    ['http://www.ohsu.edu/', 'Oregon Health Sciences University'],
    ['http://www.oit.edu', 'Oregon Institute of Technology'],
    ['http://osu.orst.edu/', 'Oregon State University'],
    ['http://www.otterbein.edu/', 'Otterbein College'],
    ['http://www.ottawa.edu/', 'Ottawa University'],
    ['http://www.obu.edu/', 'Ouachita Baptist University'],
    ['http://www.ollusa.edu/', 'Our Lady of the Lake University'],
    ['http://www.olhcc.edu/', 'Our Lady of Holy Cross College'],
    ['http://www.pace.edu/', 'Pace University'],
    ['http://www.pacificcollege.edu/', 'Pacific College of Oriental Medicine'],
    ['http://www.plu.edu/', 'Pacific Lutheran University'],
    ['http://www.pnca.edu/', 'Pacific Northwest College of Art'],
    ['http://www.pacificoaks.edu', 'Pacific Oaks College'],
    ['http://www.psuca.edu/', 'Pacific States University'],
    ['http://www.puc.edu/', 'Pacific Union College'],
    ['http://www.pacificu.edu/', 'Pacific University'],
    ['http://www.paine.edu/', 'Paine College'],
    ['http://www.pbac.edu/', 'Palm Beach Atlantic College'],
    ['http://www.palmer.edu/', 'Palmer College of Chiropractic'],
    ['http://www.park.edu/', 'Park College'],
    ['http://www.parsons.edu/', 'Parsons School of Design'],
    ['http://www.patten.edu/', 'Patten College'],
    ['http://www.phc.edu/', 'Patrick Henry College'],
    ['http://www.pqc.edu/', 'Paul Quinn College'],
    ['http://www.paulsmiths.edu/', "Paul Smith's College"],
    ['http://www.peace.edu/', 'Peace College'],
    ['http://www.pct.edu', 'Pennsylvania College of Technology'],
    ['http://www.psu.edu/', 'The Pennsylvania State University'],
    ['http://www.aa.psu.edu/', 'Pennsylvania State University at Altoona'],
    ['http://www.gv.psu.edu/', 'Pennsylvania State University, Great Valley'],
    ['http://www.hbg.psu.edu/', 'Pennsylvania State University at Harrisburg'],
    ['http://www.sn.psu.edu/', 'Pennsylvania State University, Worthington Scranton'],
    ['http://www.pcci.edu/', 'Pensacola Christian College'],
    ['http://www.pepperdine.edu/', 'Pepperdine University'],
    ['http://www.peru.edu/', 'Peru State College'],
    ['http://www.pfeiffer.edu/', 'Pfeiffer University'],
    ['http://www.pickering.edu/', 'Pickering University'],
    ['http://www.piedmont.edu/', 'Piedmont College'],
    ['http://www.pikeville.edu', 'Pikeville College'],
    ['http://www.pmc.edu/', 'Pine Manor College'],
    ['http://www.pittstate.edu/', 'Pittsburg State University'],
    ['http://www.pitzer.edu/', 'Pitzer College'],
    ['http://www.pbu.edu/', 'Philadelphia Biblical University'],
    ['http://www.philau.edu/', 'Philadelphia University'],
    ['http://www.philander.edu/', 'Philander Smith College'],
    ['http://www.phillips.edu/', 'Phillips University'],
    ['http://www.plymouth.edu/', 'Plymouth State University, Plymouth New Hampshire'],
    ['http://www.ptloma.edu/', 'Point Loma Nazarene College'],
    ['http://www.pointpark.edu', 'Point Park University'],
    ['http://www.poly.edu/', 'Polytechnic University of New York'],
    ['http://www.pupr.edu/', 'Polytechnic University of Puerto Rico'],
    ['http://www.pomona.edu/', 'Pomona College'],
    ['http://www.pucpr.edu', 'Pontifical University'],
    ['http://www.pdx.edu/', 'Portland State University'],
    ['http://www.potomac.edu/', 'Potomac College'],
    ['http://www.pvamu.edu/', 'Prairie View A &amp M University'],
    ['http://www.pratt.edu/', 'Pratt Institute'],
    ['http://www.presby.edu/', 'Presbyterian College'],
    ['http://www.prescott.edu', 'Prescott College'],
    ['http://www.preston.edu/', 'Preston University'],
    ['http://www.princeton.edu/', 'Princeton University'],
    ['http://www.prin.edu/', 'Principia College'],
    ['http://www.providence.edu/', 'Providence College'],
    ['http://www.purdue.edu/', 'Purdue University'],
    ['http://www.pnc.edu', 'Purdue University North Central'],
    ['http://www.queens.edu/', 'Queens College'],
    ['http://www.quincy.edu/', 'Quincy University'],
    ['http://www.quinnipiac.edu/', 'Quinnipiac College'],
    ['http://www.runet.edu/', 'Radford University'],
    ['http://www.ramapo.edu/', 'Ramapo College of New Jersey'],
    ['http://www.rmc.edu/', 'http://www.randolphcollege.edu', 'Randolph College'],
    ['http://www.rmc.edu/', 'Randolph-Macon College'],
    ['http://www.randolphcollege.edu', 'http://www.rasmussen.edu/', 'Rasmussen College'],
    ['http://www.reed.edu/', 'Reed College'],
    ['http://www.regent.edu/', 'Regent University'],
    ['http://www.regiscollege.edu/', 'Regis College'],
    ['http://www.regis.edu/', 'Regis University'],
    ['http://www.reinhardt.edu/', 'Reinhardt College'],
    ['http://www.remington.edu', 'Remington College'],
    ['http://www.rpi.edu/', 'Rensselaer Polytechnic Institute'],
    ['http://www.ric.edu/', 'Rhode Island College'],
    ['http://www.risd.edu/', 'Rhode Island School of Design'],
    ['http://www.rhodes.edu/', 'Rhodes College'],
    ['http://www.rice.edu/', 'Rice University'],
    ['http://www.stockton.edu/', 'The Richard Stockton College of New Jersey'],
    ['http://www.rider.edu/', 'Rider University'],
    ['http://www.rsad.edu/', 'Ringling School of Art and Design'],
    ['http://www.ripon.edu/', 'Ripon College'],
    ['http://www.rivier.edu/', 'Rivier College'],
    ['http://www.roanoke.edu/', 'Roanoke College'],
    ['http://www.robertmorris.edu/', 'Robert Morris College, Illinois'],
    ['http://www.robert-morris.edu/', 'Robert Morris College, Pittsburgh, PA'],
    ['http://www.rwc.edu/', 'Roberts Wesleyan College'],
    ['http://www.rit.edu/', 'Rochester Institute of Technology'],
    ['http://www.rc.edu/', 'Rochester College'],
    ['http://www.rockefeller.edu/', 'The Rockefeller University'],
    ['http://www.rockford.edu/', 'Rockford College'],
    ['http://www.rockhurst.edu/', 'Rockhurst University'],
    ['http://www.rocky.edu/', 'Rocky Mountain College'],
    ['http://www.rwu.edu/', 'Roger Williams University'],
    ['http://www.rsu.edu/', 'Rogers State University'],
    ['http://www.rollins.edu/', 'Rollins College'],
    ['http://www.roosevelt.edu/', 'Roosevelt University'],
    ['http://www.rose-hulman.edu/', 'Rose-Hulman Institute of Technology'],
    ['http://www.rosemont.edu/', 'Rosemont College'],
    ['http://www.rowan.edu/', 'Rowan University'],
    ['http://www.rushu.rush.edu/', 'Rush University'],
    ['http://www.sage.edu/', 'Russell Sage College'],
    ['http://www.rustcollege.edu/', 'Rust College'],
    ['http://www.rutgers.edu/', 'Rutgers University'],
    ['http://camden-www.rutgers.edu/', 'Rutgers University-Camden'],
    ['http://rutgers-newark.rutgers.edu/', 'Rutgers University-Newark'],
    ['http://www.ryokan.edu/', 'Ryokan College'],
    ['http://www.sacredheart.edu/', 'Sacred Heart University'],
    ['http://www.usc.clu.edu/', 'Sacred Heart University, Puerto Rico'],
    ['http://www.sage.edu/', 'The Sage Colleges'],
    ['http://www.svsu.edu/', 'Saginaw Valley State University'],
    ['http://www.sau.edu/', 'Saint Ambrose University'],
    ['http://www.sapc.edu/', 'Saint Andrews Presbyterian College'],
    ['http://www.anselm.edu/', 'Saint Anselm College'],
    ['http://www.sacn.edu/', 'Saint Anthony College of Nursing'],
    ['http://www.st-aug.edu/', "Saint Augustine's College"],
    ['http://www.sbu.edu/', 'Saint Bonaventure University'],
    ['http://www.stcloudstate.edu/', 'Saint Cloud State University'],
    ['http://www.stedwards.edu/home.htm', 'Saint Edwards University'],
    ['http://www.stfranciscollege.edu/', 'Saint Francis College, Brooklyn Heights, New York'],
    ['http://www.sfc.edu/', 'Saint Francis College, Fort Wayne, Indiana'],
    ['http://www.sfcpa.edu/', 'Saint Francis College, Loretto, Pennsylvania'],
    ['http://www.sgc.edu/', "Saint Gregory's University"],
    ['http://www.sjfc.edu/', 'Saint John Fisher College'],
    ['http://www.sjca.edu/', "Saint John's College"],
    ['http://www.csbsju.edu/', "Saint John's University, Collegeville Minnesota"],
    ['http://www.stjohns.edu/', "Saint John's University, Jamaica New York"],
    ['http://www.sjc.edu/', 'Saint Joseph College'],
    ['http://www.saintjoe.edu/', "Saint Joseph's College"],
    ['http://www.sjcme.edu/', "Saint Joseph's College of Maine"],
    ['http://www.sju.edu/', "Saint Joseph's University"],
    ['http://www.stlawu.edu/', 'Saint Lawrence University'],
    ['http://www.saintleo.edu/', 'Saint Leo University'],
    ['http://www.slu.edu/', 'Saint Louis University'],
    ['http://www.slcconline.edu', 'Saint Louis Christian College'],
    ['http://www.stmartin.edu/', "Saint Martin's University"],
    ['http://www.smwc.edu/', 'Saint Mary-of-the-Woods College'],
    ['http://www.saintmarys.edu/', 'http://www.stmarys-ca.edu/', "Saint Mary's College of California"],
    ['http://www.smcm.edu/', "Saint Mary's College of Maryland"],
    ['http://www.smumn.edu/', "Saint Mary's University of Minnesota"],
    ['http://www.stmarytx.edu/', "Saint Mary's University of San Antonio"],
    ['http://www.saintmeinrad.edu/theology/', "Saint Meinrad's School of Theology"],
    ['http://www.smcvt.edu/', "Saint Michael's College"],
    ['http://www.snc.edu/', 'Saint Norbert College'],
    ['http://www.stolaf.edu/', 'Saint Olaf College'],
    ['http://www.saintpauls.edu/', "Saint Paul's College"],
    ['http://www.spc.edu/', "Saint Peter's College"],
    ['http://www.spcollege.edu', 'Saint Petersburg College'],
    ['http://www.strose.edu/', 'Saint Rose College'],
    ['http://www.stac.edu/', 'Saint Thomas Aquinas College'],
    ['http://www.stu.edu/', 'Saint Thomas University'],
    ['http://www.stvincent.edu/', 'Saint Vincent College'],
    ['http://www.sxu.edu/', 'Saint Xavier University'],
    ['http://www.salem.edu/', 'Salem College'],
    ['http://www.salemiu.edu/', 'Salem International University'],
    ['http://www.salemstate.edu', 'Salem State College'],
    ['http://www.ssu.edu/', 'Salisbury State University'],
    ['http://www.salk.edu', 'The Salk Institute for Biological Studies'],
    ['http://www.salve.edu', 'Salve Regina University'],
    ['http://www.shsu.edu/', 'Sam Houston State University'],
    ['http://www.samford.edu', 'Samford University'],
    ['http://www.samuelmerritt.edu/', 'Samuel Merritt College'],
    ['http://www.sdsu.edu/', 'San Diego State University'],
    ['http://www.sanfranciscoart.edu/', 'San Francisco Art Institute'],
    ['http://www.sfls.edu/', 'San Francisco Law School'],
    ['http://www.sfsu.edu/', 'San Francisco State University'],
    ['http://www.sjcl.org/', 'San Joaquin College of Law'],
    ['http://www.sjchristiancol.edu/', 'San Jose Christian College'],
    ['http://www.sjsu.edu/', 'San Jose State University'],
    ['http://www.scu.edu/', 'Santa Clara University'],
    ['http://www.slc.edu/', 'Sarah Lawrence College'],
    ['http://www.saratogau.edu/', 'Saratoga University School of Law'],
    ['http://www.slc.edu/', 'Sarah Lawrence College'],
    ['http://www.scad.edu/', 'Savannah College of Art and Design'],
    ['http://www.savstate.edu/', 'Savannah State University'],
    ['http://www.saybrook.edu/', 'Saybrook Graduate School and Research Center'],
    ['http://www.schiller.edu/', 'Schiller International University'],
    ['http://www.sit.edu', 'School for International Training'],
    ['http://www.artic.edu/saic/saichome.html', 'School of the Art Institute of Chicago'],
    ['http://www.siss.edu/', 'School of Islamic and Social Sciences'],
    ['http://www.smfa.edu/', 'School of the Museum of Fine Arts, Boston'],
    ['http://www.sva.edu/', 'School of the Visual Arts'],
    ['http://www.schreiner.edu/', 'Schreiner College'],
    ['http://www.scrippscol.edu/', 'Scripps College'],
    ['http://www.scripps.edu/', 'The Scripps Research Institute'],
    ['http://www.spu.edu/', 'Seattle Pacific University'],
    ['http://www.seattleu.edu/', 'Seattle University'],
    ['http://www.shu.edu/', 'Seton Hall University'],
    ['http://www.setonhill.edu/', 'Seton Hill College'],
    ['http://www.shasta.edu/', 'Shasta Bible College'],
    ['http://www.shawnee.edu/', 'Shawnee State University'],
    ['http://www.shawuniversity.edu/', 'Shaw University'],
    ['http://www.sheffield.edu/', 'Sheffield School of Interior Design'],
    ['http://www.sheldonjackson.edu/', 'Sheldon Jackson College'],
    ['http://www.su.edu/', 'Shenandoah University'],
    ['http://www.shepherd.edu/', 'Shepherd College'],
    ['http://www.sherman.edu/', 'Sherman College of Straight Chiropractic'],
    ['http://www.shimer.edu/', 'Shimer College'],
    ['http://www.ship.edu/', 'Shippensburg University of Pennsylvania'],
    ['http://www.shorter.edu/', 'Shorter College'],
    ['http://www.siena.edu/', 'Siena College'],
    ['http://www.sienahts.edu/', 'Siena Heights University'],
    ['http://www.sierranevada.edu', 'Sierra Nevada College'],
    ['http://www.sl.edu/', 'Silver Lake College'],
    ['http://www.simmons.edu/', 'Simmons College'],
    ['http://www.simons-rock.edu/', "Simon's Rock College"],
    ['http://www.simpsonca.edu/', 'Simpson College, Redding California'],
    ['http://www.simpson.edu/', 'Simpson College, Indianola Iowa'],
    ['http://www.skidmore.edu/', 'Skidmore College'],
    ['http://www.sru.edu/', 'Slippery Rock University'],
    ['http://www.scbc.edu/', 'Smith Chapel Bible College'],
    ['http://www.smith.edu/', 'Smith College'],
    ['http://www.soka.edu/', 'Soka University of America'],
    ['http://www.sonoma.edu/', 'Sonoma State University'],
    ['http://www.scsu.edu/', 'South Carolina State University'],
    ['http://www.sdsmt.edu/', 'South Dakota School of Mines and Technology'],
    ['http://www.sdstate.edu/', 'South Dakota State University'],
    ['http://www.southpacificuniv.edu/', 'South Pacific University'],
    ['http://www.stcl.edu/', 'South Texas College of Law'],
    ['http://www.southampton.liunet.edu/', 'Southampton College'],
    ['http://www.sctmemphis.edu/', 'Southeast College of Technology'],
    ['http://www.semo.edu/', 'Southeast Missouri State University'],
    ['http://www.sebc.edu', 'Southeastern Bible College'],
    ['http://www.secollege.edu/', 'Southeastern College'],
    ['http://www.selu.edu/', 'Southeastern Louisiana University'],
    ['http://www.sosu.edu/', 'Southeastern Oklahoma State University'],
    ['http://www.seu.edu/', 'Southeastern University'],
    ['http://www.southern.edu/', 'Southern Adventist University'],
    ['http://www.saumag.edu/', 'Southern Arkansas University'],
    ['http://www.scuhs.edu/', 'Southern California University of Health Sciences'],
    ['http://www.scups.edu/', 'Southern California University of Professional Studies'],
    ['http://www.southernct.edu', 'Southern Connecticut State University'],
    ['http://www.siu.edu/', 'Southern Illinois University at Carbondale'],
    ['http://www.siue.edu/', 'Southern Illinois University at Edwardsville'],
    ['http://www.siumed.edu/', 'Southern Illinois University Medical School at Springsfield'],
    ['http://www.smu.edu/', 'Southern Methodist University'],
    ['http://www.snu.edu/', 'Southern Nazarene University'],
    ['http://www.snhu.edu/', 'Southern New Hampshire University'],
    ['http://www.sosc.edu/', 'Southern Oregon State College'],
    ['http://www.sou.edu', 'Southern Oregon University'],
    ['http://www.spsu.edu/', 'Southern Polytechnic State Univerisity'],
    ['http://www.svc.edu', 'Southern Vermont College'],
    ['http://www.southernvirginia.edu/', 'Southern Virginia University'],
    ['http://www.scicu.org/s_wesley/swhome.htm', 'Southern Wesleyan University'],
    ['http://www.subr.edu/', 'Southern University, Baton Rouge'],
    ['http://www.suno.edu/', 'Southern University, New Orleans'],
    ['http://www.susbo.edu/', 'Southern University, Shreveport-Bossier City'],
    ['http://www.suu.edu/', 'Southern Utah University'],
    ['http://www.sbuniv.edu/', 'Southwest Baptist University'],
    ['http://www.goodisgood.com/sbcs/', 'Southwest Bible College and Seminary'],
    ['http:/www.swfc.edu', 'Southwest Florida College'],
    ['http://www.southwestmsu.edu', 'Southwest Minnesota State University'],
    ['http://www.southwest.edu/', 'Southwest University'],
    ['http://www.swau.edu/', 'Southwestern Adventist University'],
    ['http://www.sagu.edu/', 'Southwestern Assemblies of God University'],
    ['http://www.sckans.edu/', 'Southwestern College, Kansas'],
    ['http://www.swc.edu', 'Southwestern College, New Mexico'],
    ['http://www.swosu.edu/', 'Southwestern Oklahoma State University'],
    ['http://www.southwestern.edu/', 'Southwestern University'],
    ['http://www.swlaw.edu/', 'Southwestern University School of Law'],
    ['http://www.spalding.edu/', 'Spalding University'],
    ['http://www.smcsc.edu/', 'Spartanburg Methodist College'],
    ['http://www.spelman.edu/', 'Spelman College'],
    ['http://www.spertus.edu/', 'Spertus College'],
    ['http://www.arbor.edu/', 'Spring Arbor College'],
    ['http://www.shc.edu/', 'Spring Hill College'],
    ['http://www.spfldcol.edu/', 'Springfield College'],
    ['http://www.stamford.edu/', 'Stamford International College'],
    ['http://www.stanford.edu/', 'Stanford University'],
    ['http://www.albany.edu/', 'State University of New York at Albany'],
    ['http://www.binghamton.edu/', 'State University of New York at Binghamton'],
    ['http://www.buffalo.edu/', 'State University of New York at Buffalo'],
    ['http://www.oswego.edu/', 'State University of New York at Oswego'],
    ['http://www.sunysb.edu/', 'State University of New York at Stony Brook'],
    ['http://www.cobleskill.edu/', 'State University of New York College of Agriculture and Technology, Cobleskill'],
    ['http://www.morrisville.edu/', 'State University of New York College of Agriculture and Technology, Morrisville'],
    ['http://www.acs.brockport.edu/', 'State University of New York College at Brockport'],
    ['http://www.buffalostate.edu', 'State University of New York College at Buffalo (Buffalo State College)'],
    ['http://www.cortland.edu/', 'State University of New York College at Cortland'],
    ['http://www.esf.edu/', 'State University of New York College of Environmental Science and Forestry'],
    ['http://www.farmingdale.edu/', 'State University of New York College at Farmingdale'],
    ['http://www.fredonia.edu/', 'State University of New York College at Fredonia'],
    ['http://mosaic.cc.geneseo.edu/', 'State University of New York College at Geneseo'],
    ['http://www.sunymaritime.edu/', 'State University of New York College Maritime College at Fort Schuyler'],
    ['http://www.newpaltz.edu/', 'State University of New York College at New Paltz'],
    ['http://www.oldwestbury.edu/', 'State University of New York College at Old Westbury'],
    ['http://www.oneonta.edu/', 'State University of New York College at Oneonta'],
    ['http://www.oswego.edu/', 'State University of New York College at Oswego'],
    ['http://www.plattsburgh.edu/', 'State University of New York College at Plattsburgh'],
    ['http://www.potsdam.edu/', 'State University of New York College at Potsdam'],
    ['http://www.purchase.edu/', 'State University of New York College at Purchase'],
    ['http://www.canton.edu/', 'State University of New York Institute of Technology at Canton'],
    ['http://www.delhi.edu/', 'State University of New York Institute of Technology at Delhi'],
    ['http://www.sunyit.edu/', 'State University of New York Institute of Technology at Utica/Rome'],
    ['http://www.stefan-university.edu/', 'The Stefan University'],
    ['http://www.sfasu.edu/', 'Stephen F. Austin State University'],
    ['http://www.stephens.edu/', 'Stephens College'],
    ['http://www.sterling.edu/', 'Sterling College, Sterling Kansas'],
    ['http://www.sterling.edu/', 'Sterling College, Kansas'],
    ['http://www.sterlingcollege.edu/', 'Sterling College, Vermont'],
    ['http://www.stetson.edu/', 'Stetson University'],
    ['http://www.stevenshenager.edu/', 'Stevens-Henager College'],
    ['http://www.stevens-tech.edu/', 'Stevens Institute of Technology'],
    ['http://www.vjc.edu/', 'Stevenson University'],
    ['http://www.stillman.edu/', 'Stillman College'],
    ['http://www.stonehill.edu/', 'Stonehill College'],
    ['http://www.stratford.edu', 'Stratford University'],
    ['http://www.strayer.edu/', 'Strayer University'],
    ['http://www.suffolk.edu/', 'Suffolk University'],
    ['http://www.sulross.edu/', 'Sul Ross State University'],
    ['http://www.summitunivofla.edu/', 'Summit University of Louisiana'],
    ['http://www.susqu.edu/', 'Susquehanna University'],
    ['http://www.swarthmore.edu/', 'Swarthmore College'],
    ['http://www.sbc.edu/', 'Sweet Briar College'],
    ['http://cwis.syr.edu/', 'Syracuse University'],
    ['http://www.tabor.edu/', 'Tabor College'],
    ['http://www.talladega.edu/', 'Talladega College'],
    ['http://www.tarleton.edu/', 'Tarleton State University'],
    ['http://www.tayloru.edu/', 'Taylor University'],
    ['http://www.tc.columbia.edu/', 'Teachers College'],
    ['http://geraldine.mcrest.edu/', 'Teikyo Marycrest University'],
    ['http://www.teikyopost.edu/', 'Teikyo Post University'],
    ['http://www.temple.edu/', 'Temple University'],
    ['http://www.tnstate.edu/', 'Tennessee State University'],
    ['http://www.tntech.edu/', 'Tennessee Technological University'],
    ['http://www.tntemple.edu/', 'Tennessee Temple University'],
    ['http://www.twcnet.edu/', 'Tennessee Wesleyan College'],
    ['http://www.tamiu.edu/', 'Texas A&M International University'],
    ['http://www.tamu.edu/', 'Texas A&M University'],
    ['http://www.tamu-commerce.edu', 'Texas A&M University, Commerce'],
    ['http://www.tamucc.edu/', 'Texas A&M University, Corpus Christi'],
    ['http://www.tamug.edu/', 'Texas A&M University, Galveston'],
    ['http://www.tamuk.edu/', 'Texas A&M University, Kingsville'],
    ['http://www.tamut.edu/', 'Texas A&M University, Texarkana'],
    ['http://www.texaschiro.edu', 'Texas Chiropractic College'],
    ['http://www.tcu.edu/', 'Texas Christian University'],
    ['http://www.txlutheran.edu/', 'Texas Lutheran University'],
    ['http://www.tsu.edu/', 'Texas Southern University'],
    ['http://www.txstate.edu', 'Texas State University'],
    ['http://www.ttu.edu/', 'Texas Tech University'],
    ['http://www.txwes.edu/', 'Texas Wesleyan University'],
    ['http://www.twu.edu/', "Texas Woman's University"],
    ['http://www.thiel.edu/', 'Thiel College'],
    ['http://www.thomasaquinas.edu/', 'Thomas Aquinas College, Santa Paula CA'],
    ['http://www.tesc.edu/', 'Thomas Edison State College'],
    ['http://www.thomas.edu/', 'Thomas College'],
    ['http://www.cooley.edu/', 'Thomas Cooley Law School'],
    ['http://www.thomasmore.edu/welcome.html', 'Thomas More College'],
    ['http://www.tju.edu/', 'Thomas Jefferson University'],
    ['http://www.thunderbird.edu', 'Thunderbird School of Global Management'],
    ['http://www.toccoafalls.edu/', 'Toccoa Falls College'],
    ['http://www.tougaloo.edu/', 'Tougaloo College'],
    ['http://www.touro.edu/', 'Touro College'],
    ['http://www.towson.edu/', 'Towson University'],
    ['http://www.transworld.edu/', 'The Transworld University'],
    ['http://www.transy.edu/', 'Transylvania University'],
    ['http://www.trevecca.edu/', 'Trevecca Nazarene University'],
    ['http://www.tbc.edu/', 'Trinity Baptist College'],
    ['http://www.trnty.edu/', 'Trinity Christian College'],
    ['http://www.trincoll.edu/', 'Trinity College, Hartford Connecticut'],
    ['http://www.trinitycollege.edu/', 'Trinity College of Florida'],
    ['http://www.trinitydc.edu/', 'Trinity College, Washington DC'],
    ['http://www.trin.edu/', 'Trinity International University'],
    ['http://www.trinity.edu/', 'Trinity University'],
    ['http://www.tristate.edu/', 'Tri-State University'],
    ['http://www.troyst.edu/', 'Troy State University'],
    ['http://www.tsud.edu/', 'Troy State University - Dothan'],
    ['http://www.truman.edu/', 'Truman State University'],
    ['http://www.tufts.edu/', 'Tufts University'],
    ['http://www.tulane.edu/', 'Tulane University'],
    ['http://www.tusculum.edu/', 'Tusculum College'],
    ['http://www.tusk.edu/', 'Tuskegee University'],
    ['http://www.usuhs.mil/', 'Uniformed Services Universty of the Health Sciences'],
    ['http://www.unionky.edu/', 'Union College, Barbourville KY'],
    ['http://www.union.edu/', 'Union College'],
    ['http://www.ucollege.edu', 'Union College'],
    ['http://www.uts.columbia.edu/', 'Union Theological Seminary'],
    ['http://www.uu.edu/', 'Union University'],
    ['http://www.tui.edu/', 'The Union Institute'],
    ['http://www.usafa.af.mil/', 'United States Air Force Academy'],
    ['http://www.cga.edu/', 'United States Coast Guard Academy'],
    ['http://www.usmma.edu/', 'United States Merchant Marine Academy'],
    ['http://www.usma.edu/', 'United States Military Academy'],
    ['http://www.nadn.navy.mil/', 'United States Naval Academy'],
    ['http://www.open.edu/', 'United States Open University'],
    ['http://www.ussa.edu', 'United States Sports Academy'],
    ['http://www.united.edu', 'United Theological Seminar'],
    ['http://www.unity.edu/', 'Unity College'],
    ['http://www.u-a-l.org/', 'http://www.uat.edu/', 'University of Advancing Technology'],
    ['http://www.uakron.edu/', 'University of Akron'],
    ['http://www.ua.edu/', 'University of Alabama'],
    ['http://www.uab.edu/', 'University of Alabama, Birmingham'],
    ['http://info.uah.edu/', 'University of Alabama, Huntsville'],
    ['http://www.uaa.alaska.edu/', 'University of Alaska, Anchorage'],
    ['http://www.uaf.edu', 'University of Alaska, Fairbanks'],
    ['http://www.jun.alaska.edu/', 'University of Alaska, Southeast'],
    ['http://www.arizona.edu/', 'University of Arizona'],
    ['http://www.uark.edu/', 'University of Arkansas, Fayetteville'],
    ['http://www.ualr.edu/', 'University of Arkansas at Little Rock'],
    ['http://cotton.uamont.edu/', 'University of Arkansas at Monticello'],
    ['http://www.uapb.edu/', 'University of Arkansas at Pine Bluff'],
    ['http://www.uarts.edu/', 'University of the Arts'],
    ['http://www.ubalt.edu/', 'University of Baltimore'],
    ['http://www.bridgeport.edu/', 'University of Bridgeport'],
    ['http://www.berkeley.edu/', 'University of California, Berkeley'],
    ['http://www.ucdavis.edu/', 'University of California, Davis'],
    ['http://www.uchastings.edu/', 'University of California, Hastings College of Law'],
    ['http://www.uci.edu/', 'University of California, Irvine'],
    ['http://www.ucla.edu/', 'University of California, Los Angeles'],
    ['http://www.ucmerced.edu/', 'University of California, Merced'],
    ['http://www.ucr.edu/', 'University of California, Riverside'],
    ['http://www.ucsd.edu/', 'University of California, San Diego'],
    ['http://www.ucsf.edu/', 'University of California, San Francisco'],
    ['http://www.ucsb.edu/', 'University of California, Santa Barbara'],
    ['http://www.ucsc.edu/', 'University of California, Santa Cruz'],
    ['http://www.uca.edu/', 'University of Central Arkansas'],
    ['http://www.ucf.edu/', 'University of Central Florida'],
    ['http://www.ucok.edu/', 'University of Central Oklahoma'],
    ['http://www.ucwv.edu', 'University of Charleston'],
    ['http://www.uchicago.edu/', 'University of Chicago'],
    ['http://www.uc.edu/', 'University of Cincinnati'],
    ['http://www.colorado.edu/', 'University of Colorado at Boulder'],
    ['http://www.uccs.edu/', 'University of Colorado, Colorado Springs'],
    ['http://www.cudenver.edu/', 'University of Colorado, Denver'],
    ['http://www.uconn.edu/', 'University of Connecticut'],
    ['http://www.udallas.edu/', 'University of Dallas'],
    ['http://www.udayton.edu/', 'University of Dayton'],
    ['http://www.udel.edu/', 'University of Delaware'],
    ['http://www.du.edu/', 'University of Denver'],
    ['http://www.udmercy.edu/', 'University of Detroit Mercy'],
    ['http://www.udc.edu/', 'University of the District of Columbia'],
    ['http://www.dbq.edu/', 'University of Dubuque'],
    ['http://www.evansville.edu/', 'University of Evansville'],
    ['http://www.findlay.edu/', 'University of Findlay'],
    ['http://www.ufl.edu/', 'University of Florida'],
    ['http://www.uga.edu/', 'University of Georgia'],
    ['http://www.ugf.edu/', 'University of Great Falls'],
    ['http://www.uog.edu', 'University of Guam'],
    ['http://www.hartford.edu/', 'University of Hartford'],
    ['http://www.hawaii.edu/uhinfo.html', 'University of Hawai`i'],
    ['http://www.uhh.hawaii.edu', 'University of Hawai`i, Hilo'],
    ['http://manoa.hawaii.edu', 'University of Hawai`i, Manoa'],
    ['http://www.hawaii.edu/uhinfo.html', 'http://www.uhwo.hawaii.edu/', 'University of Hawai`i, West O`ahu'],
    ['http://www.uhs.edu/', 'University of Health Sciences College of Osteopathic Medicine'],
    ['http://www.uh.edu/', 'University of Houston'],
    ['http://www.cl.uh.edu/', 'University of Houston, Clear Lake'],
    ['http://www.dt.uh.edu/', 'University of Houston, Downtown'],
    ['http://www.vic.uh.edu/', 'University of Houston, Victoria'],
    ['http://www.uidaho.edu/', 'University of Idaho'],
    ['http://www.uiw.edu/', 'University of the Incarnate Word'],
    ['http://www.uindy.edu/', 'University of Indianapolis'],
    ['http://www.uic.edu/', 'University of Illinois at Chicago'],
    ['http://www.uis.edu/', 'University of Illinois at Springfield'],
    ['http://www.uiuc.edu/', 'University of Illinois at Urbana-Champaign'],
    ['http://www.uiowa.edu/', 'University of Iowa'],
    ['http://www.ku.edu/', 'University of Kansas'],
    ['http://www.kumc.edu/', 'University of Kansas Medical Center'],
    ['http://www.uky.edu/', 'University of Kentucky'],
    ['http://www.ulaverne.edu/', 'University of La Vernee'],
    ['http://www.louisiana.edu/', 'University of Louisiana at Lafayette'],
    ['http://www.ulm.edu/', 'University of Louisiana at Monroe'],
    ['http://www.louisville.edu/', 'University of Louisville'],
    ['http://www.umaine.edu/', 'University of Maine'],
    ['http://www.umf.maine.edu', 'University of Maine at Farmington'],
    ['http://www.umfk.maine.edu/', 'University of Maine at Fort Kent'],
    ['http://www.umpi.maine.edu/', 'University of Maine at Presque Isle'],
    ['http://www.umhb.edu/', 'University of Mary Hardin-Baylor'],
    ['http://www.umw.edu', 'University of Mary Washington'],
    ['http://www.umbc.edu/', 'University of Maryland Baltimore County'],
    ['http://www.umaryland.edu/', 'University of Maryland at Baltimore'],
    ['http://www.umd.edu/', 'University of Maryland at College Park'],
    ['http://www.umes.edu/', 'University of Maryland Eastern Shore'],
    ['http://www.umuc.edu/', 'University of Maryland University College'],
    ['http://www.umass.edu/', 'University of Massachusetts at Amherst'],
    ['http://www.umb.edu/', 'University of Massachusetts at Boston'],
    ['http://www.umassd.edu/', 'University of Massachusetts at Dartmouth'],
    ['http://www.uml.edu/', 'University of Massachusetts at Lowell'],
    ['http://www.umassmed.edu/', 'University of Massachusetts Medical School'],
    ['http://njmsa.umdnj.edu/umdnj.html', 'University of Medicine and Dentistry of New Jersey'],
    ['http://www.memphis.edu', 'University of Memphis'],
    ['http://www.miami.edu/', 'University of Miami'],
    ['http://www.umich.edu/', 'University of Michigan-Ann Arbor'],
    ['http://www.umd.umich.edu/', 'University of Michigan-Dearborn'],
    ['http://www.flint.umich.edu/', 'University of Michigan-Flint'],
    ['http://www.crk.umn.edu/', 'University of Minnesota-Crookston'],
    ['http://www.d.umn.edu/', 'University of Minnesota-Duluth'],
    ['http://www.mrs.umn.edu/', 'University of Minnesota-Morris'],
    ['http://www.umn.edu/', 'University of Minnesota-Twin Cities'],
    ['http://www.olemiss.edu/', 'University of Mississippi'],
    ['http://www.missouri.edu/', 'University of Missouri-Columbia'],
    ['http://www.umkc.edu/', 'University of Missouri-Kansas City'],
    ['http://www.umsl.edu/', 'University of Missouri-Saint Louis'],
    ['http://www.umt.edu/', 'University of Montana, Missoula'],
    ['http://www.montevallo.edu/', 'University of Montevallo'],
    ['http://www.unaturalmedicine.edu/', 'University of Natural Medicine'],
    ['http://www.unk.edu/', 'University of Nebraska, Kearney'],
    ['http://www.unl.edu/index.html', 'University of Nebraska, Lincoln'],
    ['http://www.unomaha.edu/', 'University of Nebraska, Omaha'],
    ['http://www.unlv.edu/', 'University of Nevada, Las Vegas'],
    ['http://www.unr.edu/', 'University of Nevada, Reno'],
    ['http://www.une.edu/', 'University of New England'],
    ['http://www.unh.edu/', 'University of New Hampshire, Durham'],
    ['http://www.newhaven.edu/', 'University of New Haven'],
    ['http://www.unm.edu/', 'University of New Mexico'],
    ['http://www.uno.edu/', 'University of New Orleans'],
    ['http://www.newport.edu/', 'University of Newport'],
    ['http://www.una.edu/', 'University of North Alabama'],
    ['http://www.unca.edu/', 'University of North Carolina at Asheville'],
    ['http://www.unc.edu/', 'University of North Carolina at Chapel Hill'],
    ['http://www.uncc.edu/', 'University of North Carolina at Charlotte'],
    ['http://www.uncg.edu/', 'University of North Carolina at Greensboro'],
    ['http://www.uncp.edu/', 'University of North Carolina at Pembroke'],
    ['http://www.uncwil.edu/', 'University of North Carolina at Wilmington'],
    ['http://www.und.nodak.edu/', 'University of North Dakota'],
    ['http://www.it-club.und-lr.nodak.edu/', 'University of North Dakota--Lake Region'],
    ['http://www.unf.edu/', 'University of North Florida'],
    ['http://www.unt.edu/', 'University of North Texas'],
    ['http://www.unco.edu', 'University of Northern Colorado'],
    ['http://www.uni.edu/', 'University of Northern Iowa'],
    ['http://www.unw.edu/', 'http://www.nd.edu/', 'University of Notre Dame'],
    ['http://www.ou.edu/', 'University of Oklahoma'],
    ['http://www.uoregon.edu/', 'University of Oregon'],
    ['http://www.uo.edu/', 'University of Orlando'],
    ['http://www.uomhs.edu/', 'University of Osteopathic Medicine and Health Science'],
    ['http://www.ozarks.edu/', 'University of the Ozarks'],
    ['http://www.uop.edu/', 'University of the Pacific'],
    ['http://www.upenn.edu:80/', 'University of Pennsylvania'],
    ['http://www.phoenix.edu/', 'University of Phoenix'],
    ['http://www.pitt.edu/', 'University of Pittsburgh'],
    ['http://www.upb.pitt.edu/', 'University of Pittsburgh at Bradford'],
    ['http://www.pitt.edu/~upg', 'University of Pittsburgh at Greenburg'],
    ['http://www.pitt.edu/~upjweb', 'University of Pittsburgh at Johnstown'],
    ['http://www.uofport.edu/', 'University of Portland'],
    ['http://www.uprm.edu/', 'University of Puerto Rico, Mayaguez'],
    ['http://www.rrp.upr.edu/', 'University of Puerto Rico, Rio Piedras'],
    ['http://www.ups.edu/', 'University of Puget Sound'],
    ['http://www.redlands.edu/', 'University of Redlands'],
    ['http://www.uri.edu/', 'University of Rhode Island'],
    ['http://www.urich.edu/', 'University of Richmond'],
    ['http://www.urgrgcc.edu/', 'University of Rio Grande'],
    ['http://www.rochester.edu/', 'University of Rochester'],
    ['http://www.stfrancis.edu/', 'University of Saint Francis'],
    ['http://www.stmary.edu/', 'University of Saint Mary'],
    ['http://basil.stthom.edu/', 'University of Saint Thomas, Houston'],
    ['http://www.stthomas.edu/', 'University of Saint Thomas, Saint Paul'],
    ['http://www.sandiego.edu', 'University of San Diego'],
    ['http://www.usfca.edu/', 'University of San Francisco'],
    ['http://www.sarasota-online.com/university/univ.html/', 'University of Sarasota'],
    ['http://www.usao.edu/', 'University of Science and Arts of Oklahoma'],
    ['http://www.usip.edu/', 'University of the Sciences in Philadelphia'],
    ['http://www.uofs.edu/', 'University of Scranton'],
    ['http://www.thecoo.edu/', 'University of Sioux Falls'],
    ['http://www.sewanee.edu/', 'University of the South'],
    ['http://www.usouthal.edu/', 'University of South Alabama'],
    ['http://www.sc.edu/', 'University of South Carolina'],
    ['http://www.usca.scarolina.edu/', 'University of South Carolina, Aiken'],
    ['http://www.sc.edu/beaufort', 'University of South Carolina, Beaufort'],
    ['http://www.uscs.edu/', 'University of South Carolina, Spartanburg'],
    ['http://www.usd.edu/', 'University of South Dakota'],
    ['http://www.usf.edu/', 'University of South Florida'],
    ['http://www.usc.edu/', 'University of Southern California'],
    ['http://www.uscolo.edu/', 'http://www.usi.edu/', 'University of Southern Indiana'],
    ['http://www.usm.maine.edu/', 'University of Southern Maine'],
    ['http://www.usm.edu/', 'University of Southern Mississippi'],
    ['http://www.utampa.edu/', 'University of Tampa'],
    ['http://www.utc.edu/', 'University of Tennessee, Chattanooga'],
    ['http://www.utmem.edu/', 'University of Tennessee Health Science Center'],
    ['http://www.utk.edu/', 'University of Tennessee, Knoxville'],
    ['http://www.utm.edu/', 'University of Tennessee, Martin'],
    ['http://www.uta.edu/', 'University of Texas at Arlington'],
    ['http://www.utexas.edu/', 'University of Texas at Austin'],
    ['http://www.utb.edu/', 'University of Texas at Brownsville'],
    ['http://www.utdallas.edu/', 'University of Texas at Dallas'],
    ['http://www.utep.edu/', 'University of Texas at El Paso'],
    ['http://www.uth.tmc.edu/', 'University of Texas Health Science Center at Houston'],
    ['http://www.uthscsa.edu/', 'University of Texas Health Science Center at San Antonio'],
    ['http://pegasus.uthct.edu/UTHCT-Home/Welcome.html', 'University of Texas Health Center at Tyler'],
    ['http://www.utmb.edu/', 'University of Texas Medical Branch'],
    ['http://www.panam.edu/', 'University of Texas-Pan American'],
    ['http://www.utpb.edu/', 'University of Texas of the Permian Basin'],
    ['http://www.utsa.edu/', 'University of Texas at San Antonio'],
    ['http://www.uttyler.edu', 'University of Texas at Tyler'],
    ['http://www.swmed.edu/', 'University of Texas Southwestern Medical Center'],
    ['http://www.usw.edu', 'University of the Southwest'],
    ['http://www.utoledo.edu/', 'University of Toledo'],
    ['http://www.utulsa.edu/', 'University of Tulsa'],
    ['http://www.utah.edu/', 'University of Utah'],
    ['http://www.uvm.edu/', 'University of Vermont'],
    ['http://www.uvi.edu/', 'University of the Virgin Islands'],
    ['http://www.virginia.edu/', 'University of Virginia'],
    ['http://www.washington.edu/', 'University of Washington'],
    ['http://www.wla.edu', 'University of West Alabama'],
    ['http://www.uwf.edu/', 'University of West Florida'],
    ['http://www.westga.edu/', 'University of West Georgia'],
    ['http://www.uwgb.edu/', 'University of Wisconsin-Green Bay'],
    ['http://www.uwec.edu/', 'University of Wisconsin-Eau Claire'],
    ['http://www.uwlax.edu/', 'University of Wisconsin-La Crosse'],
    ['http://www.wisc.edu/', 'University of Wisconsin-Madison'],
    ['http://www.uwm.edu/', 'University of Wisconsin-Milwaukee'],
    ['http://www.uwosh.edu/', 'University of Wisconsin-Oshkosh'],
    ['http://www.uwp.edu/', 'University of Wisconsin-Parkside'],
    ['http://www.uwplatt.edu/', 'University of Wisconsin-Platteville'],
    ['http://www.uwsp.edu/', 'University of Wisconsin-Stevens Point'],
    ['http://www.uwstout.edu/', 'University of Wisconsin-Stout'],
    ['http://www.uwsuper.edu/', 'University of Wisconsin-Superior'],
    ['http://www.uwrf.edu/', 'University of Wisconsin-River Falls'],
    ['http://www.uww.edu/', 'University of Wisconsin-Whitewater'],
    ['http://www.uwyo.edu/', 'University of Wyoming'],
    ['http://www.uiu.edu/', 'Upper Iowa University'],
    ['http://www.urbana.edu/', 'Urbana University'],
    ['http://www.ursinus.edu/', 'Ursinus College'],
    ['http://www.ursuline.edu/', 'Ursuline College'],
    ['http://www.usu.edu/', 'Utah State University'],
    ['http://www.uvsc.edu/', 'Utah Valley State College'],
    ['http://www.utica.edu/', 'Utica College'],
    ['http://www.valdosta.edu', 'Valdosta State University'],
    ['http://www.vcsu.nodak.edu/', 'Valley City State University'],
    ['http://www.valpo.edu/', 'Valparaiso University'],
    ['http://www.vanderbilt.edu/', 'Vanderbilt University'],
    ['http://www.vanguard.edu/', 'Vanguard University'],
    ['http://www.vassar.edu/', 'Vassar College'],
    ['http://www.vaughn.edu', 'Vaughn College of Aeronautics'],
    ['http://www.vennard.edu/', 'Vennard College'],
    ['http://www.vtc.vsc.edu/', 'Vermont Technical College'],
    ['http://www.villanova.edu/', 'Villanova University'],
    ['http://www.vcu.edu/', 'Virginia Commonwealth University'],
    ['http://www.vic.edu/', 'Virginia Intermont College'],
    ['http://www.viu.edu/', 'Virginia International University'],
    ['http://www.vmi.edu/', 'Virginia Military Institute'],
    ['http://www.vt.edu/', 'Virginia Polytechnic Institute and State University'],
    ['http://www.vsu.edu/', 'Virginia State University'],
    ['http://www.vuu.edu/', 'Virginia Union University'],
    ['http://www.vulonline.net/', 'Virginia University of Lynchburg'],
    ['http://www.vwc.edu/', 'Virginia Wesleyan College'],
    ['http://www.viterbo.edu/', 'Viterbo College'],
    ['http://www.voorhees.edu', 'Voorhees College'],
    ['http://www.wabash.edu/', 'Wabash College'],
    ['http://www.wagner.edu/', 'Wagner College'],
    ['http://www.wfu.edu/www-data/start.html', 'Wake Forest University'],
    ['http://www.warnerpacific.edu/', 'Warner Pacific College'],
    ['http://www.wartburg.edu/', 'Wartburg College'],
    ['http://www.waldenu.edu/', 'Walden University'],
    ['http://www.waldorf.edu', 'Waldorf College'],
    ['http://www.wallawalla.edu/', 'Walla Walla University'],
    ['http://www.walsh.edu/', 'Walsh University'],
    ['http://www.warren-wilson.edu/', 'Warren Wilson College'],
    ['http://www.wuacc.edu/', 'Washburn University'],
    ['http://www.washjeff.edu/', 'Washington &  Jefferson College'],
    ['http://www.wlu.edu', 'Washington &  Lee University'],
    ['http://www.bible.edu/', 'Washington Bible College / Capital Bible Seminary'],
    ['http://www.washcoll.edu/', 'Washington College'],
    ['http://www.wsu.edu/', 'Washington State University'],
    ['http://www.wustl.edu/', 'Washington University in Saint Louis'],
    ['http://www.watkins.edu', 'Watkins College of Art, Design and Film'],
    ['http://www.wbu.edu/', 'Wayland Baptist University'],
    ['http://www.wsc.edu/', 'Wayne State College'],
    ['http://www.wayne.edu/', 'Wayne State University'],
    ['http://www.waynesburg.edu/', 'Waynesburg College'],
    ['http://www.webb-institute.edu/', 'Webb Institute'],
    ['http://www.weber.edu/', 'Weber State University'],
    ['http://www.webster.edu', 'Webster University'],
    ['http://www.webster.edu/jack', 'Webster University North Florida'],
    ['http://www.websterorlando.edu', 'Webster University Orlando'],
    ['http://www.wellesley.edu/', 'Wellesley College'],
    ['http://www.wells.edu/', 'Wells College'],
    ['http://www.wit.edu/', 'Wentworth Institute of Technology'],
    ['http://www.wesley.edu/', 'Wesley College'],
    ['http://www.wesleyancollege.edu/', 'Wesleyan College'],
    ['http://www.wesleyan.edu/', 'Wesleyan University'],
    ['http://katz.wcula.edu/', 'West Coast University'],
    ['http://www.wcupa.edu/', 'West Chester University of Pennsylvania'],
    ['http://www.wlsc.wvnet.edu/', 'West Liberty State College'],
    ['http://www.wtamu.edu/', 'West Texas A&M University'],
    ['http://www.wvstateu.edu', 'West Virginia State University'],
    ['http://www.wvu.edu/', 'West Virginia University'],
    ['http://www.wvup.wvnet.edu/', 'West Virginia University Parkersburg'],
    ['http://www.wvwc.edu', 'West Virginia Wesleyan College'],
    ['http://www.wbc.edu/', 'Western Baptist College'],
    ['http://www.wcu.edu/', 'Western Carolina University'],
    ['http://www.wcsu.ctstateu.edu/', 'Western Connecticut State University'],
    ['http://www.wgu.edu/', 'Western Governors University'],
    ['http://www.wiu.edu/', 'Western Illinois University'],
    ['http://www.wintu.edu/', 'Western International University'],
    ['http://www.wku.edu/', 'Western Kentucky University'],
    ['http://www.wmc.car.md.us/', 'Western Maryland College'],
    ['http://www.wmich.edu/', 'Western Michigan University'],
    ['http://www.wmc.edu/', 'Western Montana College'],
    ['http://www.wnec.edu/', 'Western New England College'],
    ['http://www.wnmu.edu/', 'Western New Mexico University'],
    ['http://www.wou.edu', 'Western Oregon University'],
    ['http://www.western.edu/', 'Western State College'],
    ['http://www.wsulaw.edu/', 'Western State University College of Law'],
    ['http://www.wschiro.edu/', 'Western States Chiropractic College'],
    ['http://www.westernu.edu/', 'Western University of Health Sciences'],
    ['http://www.wwu.edu/', 'Western Washington University'],
    ['http://www.wsc.mass.edu/', 'Westfield State College'],
    ['http://www.wcmo.edu/', 'Westminster College, Fulton Missouri'],
    ['http://www.westminster.edu/', 'Westminster College, New Wilmington Pennsylvania'],
    ['http://www.wcslc.edu/', 'Westminster College, Salt Lake City'],
    ['http://www.wts.edu/', 'Westminster Theological Seminary'],
    ['http://www.wtscal.edu/', 'Westminster Theological Seminary in California'],
    ['http://www.westmont.edu/', 'Westmont College'],
    ['http://www.westwoodcollegecalifornia.com/', 'Westwood College - California'],
    ['http://www.westwoodcollegecolorado.com/', 'Westwood College - Colorado'],
    ['http://www.westwoodcollegegeorgia.com/', 'Westwood College - Georgia'],
    ['http://www.westwoodcollegeillinois.com/', 'Westwood College - Illinois'],
    ['http://www.westwoodcollegetexas.com/', 'Westwood College - Texas'],
    ['http://www.westwoodcollegevirginia.com/', 'Westwood College - Virginia'],
    ['http://www.westwood.edu/', 'Westwood College of Technology'],
    ['http://www.wheaton.edu/', 'Wheaton College, Wheaton Illinois'],
    ['http://www.wheatonma.edu/', 'Wheaton College, Massachusetts'],
    ['http://www.wju.edu/', 'Wheeling Jesuit University'],
    ['http://www.wheelock.edu/', 'Wheelock College'],
    ['http://www.whitman.edu/', 'Whitman College'],
    ['http://www.whittier.edu/', 'Whittier College'],
    ['http://www.whitworth.edu/', 'Whitworth University'],
    ['http://www.wichita.edu/', 'Wichita State University'],
    ['http://www.widener.edu/', 'Widener University'],
    ['http://www.wilberforce.edu/', 'Wilberforce University'],
    ['http://www.wilkes.edu/', 'Wilkes University'],
    ['http://www.willamette.edu/', 'Willamette University'],
    ['http://www.wciu.edu/', 'William Carey International University'],
    ['http://www.taftu.edu/', 'William Howard Taft University'],
    ['http://www.jessup.edu', 'William Jessup University'],
    ['http://www.jewell.edu/', 'William Jewell College'],
    ['http://www.wmitchell.edu/', 'William Mitchell College of Law'],
    ['http://www.wpunj.edu', 'William Paterson University'],
    ['http://www.wmpenn.edu/', 'William Penn College'],
    ['http://www.wmwoods.edu/', 'William Woods University'],
    ['http://www.wbcoll.edu/', 'Williams Baptist College'],
    ['http://www.wmcarey.edu', 'William Carey University'],
    ['http://www.williams.edu/', 'Williams College'],
    ['http://www.wilmcoll.edu/', 'Wilmington College, New Castle Delaware'],
    ['http://www.wilmington.edu/', 'Wilmington College, Wilmington Ohio'],
    ['http://www.wilson.edu/', 'Wilson College'],
    ['http://www.wingate.edu/', 'Wingate University'],
    ['http://www.wssu.edu/', 'Winston-Salem State University'],
    ['http://www.winona.edu', 'Winona State University'],
    ['http://www.winthrop.edu/', 'Winthrop University'],
    ['http://www.wlc.edu/', 'Wisconsin Lutheran College'],
    ['http://www.wittenberg.edu/', 'Wittenberg University'],
    ['http://www.wofford.edu/', 'Wofford College'],
    ['http://www.woodbury.edu/', 'Woodbury University'],
    ['http://www.whoi.edu/', 'Woods Hole Oceanographic Institution'],
    ['http://www.wpi.edu/', 'Worcester Polytechnic Institute'],
    ['http://www.worchester.edu', 'Worcester State College'],
    ['http://www.wrightinst.edu/', 'Wright Institute'],
    ['http://www.wright.edu/', 'Wright State University'],
    ['http://www.xu.edu/', 'Xavier University, Cincinnati, OH'],
    ['http://www.xula.edu/', 'Xavier University of Louisiana'],
    ['http://www.yale.edu/', 'Yale University'],
    ['http://www.yu.edu/', 'Yeshiva University'],
    ['http://www.york.edu/', 'York College, York Nebraska'],
    ['http://www.ycp.edu/', 'York College of Pennsylvania'],
    ['http://www.ysu.edu/', 'Youngstown State University'],
    ['http://www.zbi.edu/', 'Zion Bible Institute']
]




##Alabama A&M University
##Alabama Aviation and Technical College
##Alabama State University
##Andrew Jackson University
##Auburn University
##Auburn University at Montgomery
##Barrington University
##Birmingham Southern College
##Bishop State Community College
##Central Alabama Community College
##Chadwick University
##Columbia Southern University
##Concordia College
##Faulkner University
##Huntingdon College
##Jacksonville State University
##Judson College
##Northwest Shoals Community College
##Oakwood College
##Samford University
##Spring Hill College
##Stillman College
##Talladega College
##Troy State University
##Troy State University- Montgomery
##Tuskegee University
##United States Sports Academy
##University of Alabama at Birmingham
##University of Alabama in Huntsville
##University of Alabama
##University of Mobile
##University of Montevallo
##University of North Alabama
##University of South Alabama
##University of West Alabama
##Alaska Pacific University
##University of Alaska
##University of Alaska Anchorage
##University of Alaska Fairbanks
##University of Alaska Southeast
##Wayland Baptist University - Alaska Campus
##American Graduate School of International Management
##Apache University
##Arizona State University
##Arizona State University East
##Arizona State University West
##Arizona Western College
##Art Institute of Arizona
##Central Arizona College
##Chandler-Gilbert Community College
##DeVry Institute of Technology - Phoenix
##Eastern Arizona College
##Embry-Riddle Aeronautical University - Prescott
##Estrella Mountain Community College
##Gateway Community College
##Glendale Community College
##Grand Canyon University
##Long Technical College
##Midwestern University
##North Central University
##Northern Arizona University
##Pima Community College
##Prescott College
##Scottsdale Community College
##University of Advancing Computer Technology
##University of Arizona
##University of Phoenix
##Western International University
##Arkansas State University
##Arkansas Tech University
##Harding University
##Henderson State University
##Hendrix College
##John Brown University
##Lyon College
##Ouachita Baptist University
##Philander Smith College
##Shorter College
##Southern Arkansas University Magnolia
##University of Arkansas at Little Rock
##University of Arkansas at Monticello
##University of Arkansas at Pine Bluff
##University of Arkansas for Medical Sciences
##University of Arkansas - Fayetteville
##University of Central Arkansas
##University of the Ozarks
##Academy of Art College
##Alliant International University
##American River College
##Antioch University - Los Angeles
##Armstrong University
##Art Institute of California
##Art Institute of Los Angeles
##Art Institute of Los Angeles - Orange County
##Art Institutes International at San Francisco
##Azusa Pacific University
##Bethany College
##Biola University
##Butte College
##California Coast University
##California College for Health Sciences
##California Institute for Human Science
##California Institute of Integral Studies
##California Institute of Technology
##California Institute of the Arts
##California Lutheran University
##California Polytechnic State University - San Luis Obispo
##California State Polytechnic University - Pomona
##California State University - Bakersfield
##California State University - Chico
##California State University - Dominguez Hills
##California State University - Fresno
##California State University - Fullerton
##California State University - Hayward
##California State University - Long Beach
##California State University - Los Angeles
##California State University - Monterey Bay
##California State University - Northridge
##California State University - Sacramento
##California State University - San Bernardino
##California State University - San Jose
##California State University - San Marcos
##California State University - Stanislaus
##Ca&ntilde;ada College
##Cerritos College
##Chabot College
##Chapman University
##Charles Drew University of Medicine and Science
##City University Los Angeles
##Claremont Graduate University
##Claremont McKenna College
##College of the Canyons
##College of the Siskiyous
##Columbia Pacific University
##Concordia University 
##Cosumnes River College
##Cuyamaca College
##Diablo Valley College
##Dominican College
##El Camino College
##The Fielding Institute
##Fresno Pacific University
##Fullerton College
##Golden Gate University
##Harvey Mudd College
##Heald College
##Hope International University
##Humboldt State University
##Keck Graduate Institute of Applied Life Sciences
##Lassen Community College
##La Sierra University
##Lincoln University
##Loma Linda University
##Los Angeles Film School
##Los Angeles Pierce College
##Loyola Marymount University
##Marymount College
##Monterey Institute of International Studies
##Mt. San Antonio College
##Mount St. Mary's College
##National Hispanic University
##National University
##Naval Postgraduate School
##New College of California
##Newport University California
##Notre Dame de Namur University
##Occidental College
##Pacific Western University
##Park College - Camp Pendleton
##Pepperdine University
##Phillips Graduate Institute
##Pitzer College
##Point Loma Nazarene University
##Pomona College
##Rudolf Steiner College
##Sacramento City College
##Saint Mary's College of California
##Samra University of Oriental Medicine
##San Diego State University
##San Francisco State University
##San Jos&eacute; State University
##Santa Clara University
##Sierra College
##Soka University of America
##Sonoma State University
##South Baylo University
##Southern California University for Professional Studies
##Southwestern College
##Southwestern University School of Law
##Stanford University
##Stefan University
##Touro University International
##Tokyo Language Arts College
##University of California
##University of California - Berkeley
##University of California - Davis
##University of California - Hastings College of the Law
##University of California - Irvine 
##University of California - Los Angeles
##University of California - Riverside
##University of California - San Diego
##University of California - San Francisco
##University of California - Santa Barbara
##University of California - Santa Cruz
##University of Judaism
##University of La Verne
##University of Phoenix
##University of Redlands
##University of San Diego
##University of San Francisco
##University of Santa Monica
##University of Southern California
##University of the Pacific
##University of West Los Angeles
##Vanguard Unversity
##Westmont College
##Westwood College
##Whittier College
##Adams State College
##American National University
##Art Institute of Colorado
##Colorado Christian University
##Colorado College
##Colorado School of Mines
##Colorado Space Grant College
##Colorado State University
##Economics Institute
##Fort Lewis College
##Jones International University
##Metropolitan State College of Denver
##Mesa State College
##National Technological University
##Nazarene Bible College
##Regis University
##Rocky Mountain Bible Institute
##United States Air Force Academy
##University of Colorado at Boulder
##University of Colorado at Denver
##University of Colorado at Colorado Springs
##University of Denver
##University of Northern Colorado
##University of Southern Colorado
##Webster University
##Western State College of Colorado
##Westwood College
##Bridgeport University
##Central Connecticut State University
##Charter Oak State College
##Connecticut College
##Fairfield University
##Goodwin College
##Naugatuck Valley Community College
##Quinnipiac College
##Saint Joseph College
##Sacred Heart University
##Southern Connecticut State University
##Trinity College
##University of Connecticut
##University of Hartford
##University of New Haven
##Wesleyan University
##Western Connecticut State University
##Yale University
##Delaware Technical and Community College
##Delaware State University
##Goldey-Beacom College
##University of Delaware
##Wesley College
##American Intercontinental University
##Art Institute of Fort Lauderdale
##Barry University
##Bethune-Cookman College
##Brevard Community College
##Broward Community College
##Carlos Albizu University
##Chipola Junior College
##Christian Leadership University
##Edward Waters College
##Embry-Riddle Aeronautical University
##Florida Agricultural & Mechanical University
##Florida Atlantic University
##Florida Christian College
##Florida Gulf Coast University
##Florida Hospital College of Health Sciences
##Florida Institute of Technology
##Florida International University
##Florida Memorial College
##Florida State University
##International College
##Jacksonville University
##Lynn University
##Miami-Dade Community College
##Miami Evangelical Theological Seminary
##New College of Florida
##New World School of the Arts
##Nova Southeastern University
##The Open University
##Palm Beach Atlantic College
##Ringling School of Art and Design
##Rollins College
##Schiller International University
##Stetson University
##Trinity Baptist College
##Troy State University - Florida Region
##University of Central Florida
##University of Florida
##University of Miami
##University of North Florida
##University of Phoenix
##University of Sarasota
##University of South Florida
##University of South Florida at Saint Petersburg
##University of Tampa
##University of West Florida
##Warner Southern College
##Webber College
##Webster University - North Florida Region
##Agnes Scott
##Albany State College
##Albany State University
##American InterContinental University
##Armstrong Atlantic State University
##Art Institute of Atlanta
##Augusta State University
##Berry College
##Brenau University
##Clark Atlanta University
##Covenant College
##Darton College
##DeKalb College
##DeVry Institute of Technology
##Emory University
##Fort Valley State University
##Georgia College & State University
##Georgia Institute of Technology
##Georgia Perimeter College
##Georgia Southern University
##Georgia Southwestern State University
##Georgia State University
##Kennesaw State University
##LaGrange College
##Mercer University
##Morehouse College
##Morris Brown College
##North Georgia College & State University 
##Oglethorpe University
##Paine College
##Savannah College of Art and Design
##Savannah State University
##Shorter College
##Southern College of Technology
##Southern Regional Electronic Campus
##Spelman College
##State University of West Georgia
##Thomas University
##Toccoa Falls College
##University of Georgia
##Valdosta State University
##Wesleyan College
##Young Harris College
##Brigham Young University Hawaii
##Chaminade University
##Greenwich University
##Hawaii Pacific University
##University of Hawaii
##University of Hawaii - West Oahu
##University of Phoenix - Hawaii
##Albertson College
##Boise State
##Canyon College
##Idaho State University
##Lewis and Clark State College
##Northwest Nazarene College
##University of Idaho
##Augustana College
##Aurora University
##Benedictine University
##Blackburn College
##Bradley University
##Chicago State University
##College of DuPage
##Columbia College
##Concordia University
##DePaul University
##DeVry Institute of Technology
##Eastern Illinois University
##Elmhurst College
##Eureka College
##Governors State University
##Greenville College
##Illinois College
##Illinois Institute of Art - Chicago
##Illinois Institute of Art - Schaumburg
##Illinois Institute of Technology
##Illinois Institute of Technology - Rice
##Illinois State University
##Illinois Wesleyan University
##John A. Logan College
##Judson College
##Kendall College
##Knox College
##Lake Forest College
##Lewis University
##Lincoln College
##Loyola University Chicago
##Midwestern University
##Millikin University
##National-Louis University
##North Central College
##Northeastern Illinois University
##Northern Illinois University
##Northwestern University
##Olivet Nazarene University
##Principia College
##Quincy University
##Rockford College
##Roosevelt University
##Rush University
##School of the Art Institute of Chicago
##Southern Illinois University at Carbondale
##Southern Illinois University at Edwardsville
##Trinity International University
##Triton College
##University of Chicago
##University of Illinois at Chicago
##University of Illinois at Springfield
##University of Illinois at Urbana-Champaign
##University of St. Francis
##Western Illinois University
##Westwood College
##Wheaton College
##William Rainey Harper College
##Ball State University
##Butler University
##Calumet College of St. Joseph
##DePauw University
##Earlham College
##Franklin College
##Goshen College
##Grace College
##Hanover College
##Huntington College
##Indiana State University
##Indiana University
##Indiana University Bloomington
##Indiana University Northwest
##Indiana University South Bend
##Indiana University Southeast
##Indiana University - Purdue University Columbus
##Indiana University - Purdue University Fort Wayne
##Indiana University - Purdue University Indianapolis
##Indiana Wesleyan University
##Ivy Tech State College
##Manchester College
##Purdue School of Engineering and Technology
##Purdue University
##Rose-Hulman Institute of Technology
##Saint Joseph's College
##Saint Mary-of-the-Woods College
##Saint Mary's College
##Taylor University
##University of Evansville
##University of Indianapolis
##University of Notre Dame
##University of Saint Francis
##University of Southern Indiana
##Valparaiso University
##Vincennes University
##Wabash College
##American Global University
##Briar Cliff College
##Buena Vista University
##Central College
##Clarke College
##Coe College
##Cornell College
##Dordt College
##Drake University
##Graceland College
##Grand View College
##Grinnell College
##Iowa State University
##Iowa Wesleyan College
##Kirkwood Community College
##Luther College
##Maharishi University of Management
##Morningside College
##Northwestern College
##St. Ambrose University
##Simpson College
##Teikyo Marycrest University
##University of Dubuque
##University of Iowa
##University of Northern Iowa
##Upper Iowa University
##Wartburg College
##William Penn College
##Baker University
##Barton County Community College
##Benedictine College
##Bethel College
##Emporia State University
##Friends University
##Fort Hays State University
##Hesston College
##Kansas State University
##MidAmerica Nazarene College
##McPherson College
##Ottawa University
##Pittsburg State University
##University of Kansas
##Washburn University
##Wichita State University
##Asbury College
##Berea College
##Brescia University
##Campbellsville University
##Centre College
##Cumberland College
##Eastern Kentucky University
##Georgetown College
##Kentucky State University
##Kentucky Wesleyan College
##Morehead State University
##Murray State University
##Northern Kentucky University
##Thomas More College
##Transylvania University
##Union College
##University of Kentucky - Lexington
##University of Louisville
##Western Kentucky University
##Bienville University
##Centenary College of Louisiana
##Columbus University
##Dillard University
##Grambling State University
##Louisiana Baptist University
##Louisiana College
##Louisiana State University
##Louisiana State University - Shreveport
##Louisiana Tech University
##Loyola University - New Orleans
##McNeese State University
##Nicholls State University
##Northwestern State University of Louisiana
##Our Lady of Holy Cross College
##Remington College
##Southeastern Louisiana University
##Southern University at Baton Rouge
##Southern University at New Orleans
##Tulane University
##University of Louisiana at Lafayette
##University of Louisiana at Monroe
##University of New Orleans
##University of Phoenix
##Xavier University of Louisiana
##Bates College
##Bowdoin University
##Colby College
##College of the Atlantic
##Maine Maritime Academy
##NetSchool of Maine
##New England School of Communications
##Thomas College
##University of New England
##University of Maine - Augusta
##University of Maine - Farmington
##University of Maine - Fort Kent
##University of Maine - Machias
##University of Maine - Orono
##University of Maine - Presque Isle
##University of Southern Maine
##York County Technical College
##Bowie State University
##Chesapeake College
##Columbia Union College
##Coppin State College
##Frostburg State University
##Goucher College
##Hood College
##Johns Hopkins University
##Loyola College of Maryland
##Maryland Institute, College of Art
##Morgan State University
##Mount Saint Mary's College
##Salisbury University
##St. John's College
##St. Mary's College of Maryland
##Strayer University
##Towson University
##Uniformed Services University
##United States Naval Academy
##University of Baltimore
##University of Maryland
##University of Maryland at Baltimore
##University of Maryland - Baltimore County
##University of Maryland - College Park
##University of Maryland - Eastern Shore
##University of Maryland, University College
##Villa Julie College
##Washington College
##Western Maryland College
##Assumption College
##Amherst College
##Babson College
##Becker College
##Bentley College
##Boston College
##Boston University
##Brandeis University
##Bridgewater State College
##Bristol Community College
##Clark University
##College of the Holy Cross
##Conway School of Landscape Design
##Eastern Nazarene College
##Elms College
##Emerson College
##Emmanuel College
##Hampshire College
##Harvard University
##Hebrew College
##Lesley College
##Massachusetts College of Pharmacy and Allied Health Sciences
##Massachusetts Communications College
##Massachusetts Institute of Technology
##Massachusetts School of Law
##Massachusetts School of Professional Psychology
##Mount Holyoke College
##Mount Ida College
##New England Institute of Art & Communications
##Northeastern University
##Olin College
##Pine Manor College
##Quinsigamond Community College
##Regis College
##The School of the Museum of Fine Arts, Boston
##Simmons College
##Simon's Rock College
##Smith College
##Springfield Technical Community College
##Stonehill College
##Suffolk University
##Tufts University
##University of Massachusetts at Boston
##University of Massachusetts at Amherst
##University of Massachusetts at Dartmouth
##University of Massachusetts at Lowell
##University of Massachusetts at Worcester
##Wellesley College
##Wentworth Institute of Technology
##Williams College
##Wheaton College
##Worcester Polytechnic Institute
##Worcester State College
##Adrian College
##Albion College
##Alcorn State University
##Alma College
##Andrews University
##Aquinas College
##Calvin College
##Central Michigan University
##Concordia College
##Cornerstone College
##Eastern Michigan University
##Faithway Baptist College
##Ferris State University
##Finlandia University
##Grand Valley State University
##Hillsdale College
##Hope College
##Kalamazoo College
##Kettering University
##Lake Superior State University
##Lawrence Technological University
##Michigan State University
##Michigan Technological University
##Northern Michigan University
##Northwestern Michigan College
##Oakland University
##Olivet College
##Rochester College
##Saginaw Valley State University
##Siena Heights University
##University of Detroit Mercy
##University of Michigan
##University of Michigan - Dearborn
##University of Michigan - Flint
##Wayne State University
##Western Michigan University
##Art Institutes International Minnesota
##Augsburg College
##Bemidji State University
##Bethany Lutheran College
##Bethel College
##Capella University
##Carleton College
##College of Saint Catherine
##College of Saint Scholastica
##Concordia College
##Crown College
##The Graduate School of America
##Gustavus Adolphus College
##Hamline University
##Macalester College
##Mankato State University
##Metropolitan State University
##Minnesota State University Moorhead
##North Central University
##Saint Cloud State University
##Saint John's University and College of Saint Benedict
##Saint Mary's University of Minnesota
##Saint Olaf College
##University of Minnesota
##University of Minnesota - Crookston
##University of Minnesota - Duluth
##University of Minnesota - Morris
##University of Minnesota - Twin Cities
##University of Saint Thomas
##Walden University
##Winona State University
##Alcorn State University
##Antonelli College
##Coahoma Community College
##Delta State University
##Jackson State University
##Mary Holmes College
##Millsaps College
##Mississippi College
##Mississippi State University
##Mississippi University for Women
##Mississippi Valley State University
##Tougaloo College
##University of Mississippi
##University of Southern Mississippi
##University of Southern Mississippi - Gulf Coast Campus
##Central Methodist College
##Central Missouri State University
##College of the Ozarks
##Cottey College
##Culver-Stockton University
##Drury University
##Fontbonne College
##Forest Institute of Professional Psychology
##Lincoln University of Missouri
##Missouri Baptist College
##Missouri Western State College
##Nazarene Theological Seminary
##Northwest Missouri State University
##Park University
##Rockhurst College
##Saint Louis College of Pharmacy
##Saint Louis University
##Southeast Missouri State University
##Southwest Baptist University
##Southwest Missouri State University
##Southwest Missouri State University - W
##Stephens College
##Truman State University
##University of Health Sciences
##University of Missouri at Columbia
##University of Missouri at Kansas City
##University of Missouri at Rolla
##University of Missouri at St. Louis
##The University of Missouri System
##Washington University in St. Louis
##Webster University
##Westminster College
##William Woods University
##Montana State University - Billings
##Montana State University - Bozeman
##Montana State University - Northern Havre
##Montana Tech of the University of Montana
##Rocky Mountain College
##University for Professional Studies
##University of Great Falls
##University of Montana
##Bellevue University
##Chadron State College
##Concordia College 
##Creighton University
##Dana College
##Doane College
##Metropolitan Community College
##Mid-Plains Community College
##Nebraska Wesleyan University
##Northeast Community College
##Peru State College
##Union College
##University of Nebraska at Kearney
##University of Nebraska at Lincoln
##University of Nebraska Medical Center at Omaha
##University of Nebraska at Omaha
##Western Nebraska Community College
##York College
##Art Institute of Las Vegas
##Morrison University
##Northern Nevada Community College
##Sierra Nevada College
##Truckee Meadows Community College
##University of Nevada - Las Vegas
##University of Nevada - Reno
##University of Phoenix
##Western Nevada Community College
##Antioch New England
##Daniel Webster College
##Dartmouth College
##Franklin Pierce College
##Keene State College
##New England College
##New Hampshire College
##Plymouth State College
##Rivier College
##Saint Anselm College
##University of New Hampshire
##Berkeley College
##Brookdale Community College
##Caldwell College
##College of New Jersey
##Drew University
##Fairleigh Dickinson University
##Kean College of New Jersey
##Jersey City State College
##Monmouth University
##Montclair State University
##New Jersey City University
##New Jersey Institute of Technology
##Princeton University
##Ramapo College of New Jersey
##Richard Stockton College
##Rider University
##Rowan University
##Rutgers University
##Rutgers University - Camden
##Rutgers University - Newark
##Seton Hall University
##Stevens Institute of Technology
##Thomas Edison State College
##William Paterson University
##Eastern New Mexico University
##New Mexico Highlands University
##New Mexico Institute of Mining and Technology
##New Mexico State University
##University of New Mexico
##University of Phoenix
##Western New Mexico University
##Adelphi University
##Albany College of Pharmacy
##Alfred University
##Bard College
##Berkeley College
##Brooklyn College
##Canisius College
##Christian Leadership University
##City University of New York
##Clarkson University
##Colgate University
##College of St. Rose
##College of Insurance
##College of Staten Island
##Columbia University
##Concordia College 
##Cooper Union for the Advancement of Science and Art
##Cornell University
##D'Youvlle College
##Daemen College
##DeVry New York
##Dominican College
##Elmira College
##Fashion Institute of Technology
##Fordham University
##Globe Institute of Technology
##Hamilton College
##Hartwick College
##Hobart and William Smith Colleges
##Hofstra University
##Houghton College
##Ithaca College
##Jewish Theological Seminary
##The King's College
##Le Moyne College
##Long Island University
##Manhattan College
##Manhattanville College
##Marist College
##Mercy College
##Monroe College
##Nassau Community College
##National Technical Institute for the Deaf
##Nazareth College
##New School University
##New York College for Wholistic Health Education and Research 
##New York Institute of Technology
##New York Restaurant School
##New York University
##North Country Community College
##Niagara University
##Pace University
##Parsons School of Design
##Paul Smith's College
##Polytechnic University of New York
##Plattsburgh State University
##Pratt Institute
##Rensselaer Polytechnic Institute
##Rochester Institute of Technology
##Rockefeller University
##Rockland Community College
##Sage Colleges
##Saint Bonaventure University
##St. John's University
##St. Lawrence University
##Sarah Lawrence College
##Siena College
##Skidmore College
##Southampton College
##Spanish University of America
##State University of New York - Albany
##State University of New York - Alfred
##State University of New York - Binghamton
##State University of New York - Brockport
##State University of New York - Buffalo
##State University of New York - Buffalo State
##State University of New York - Cobleskill
##State University of New York - Cortland
##State University of New York - Farmingdale
##State University of New York - Fredonia
##State University of New York - Geneseo
##State University of New York - Institute of Technology
##State University of New York - Maritime College
##State University of New York - Morrisville
##State University of New York - New Paltz
##State University of New York - Oneonta
##State University of New York - Oswego
##State University of New York - Plattsburgh
##State University of New York - Potsdam
##State University of New York - Purchase College
##State University of New York - Stony Brook
##State University of New York - Upstate Medical University
##Suffolk County Community College
##Syracuse University
##Technical Career Institutes
##Teacher's College, Columbia University
##Trocaire College
##U.S. Military Academy
##Union College
##University of Rochester
##University of Stuyvesant
##Utica College of Syracuse University
##Vassar College
##Wagner College
##Webb Institute
##Westchester Business Institute
##Yeshiva University
##Appalachian State University
##Art Institute of Charlotte
##Belmont Abbey College
##Bennett College
##Campbell University
##Catawba College
##Chowan College
##College of the Albemarle
##Davidson College
##Duke University
##East Carolina University
##Elizabeth City State University
##Elon College
##Fayetteville State University
##Gardner-Webb University
##Greensboro College
##Guilford College
##High Point University
##Johnson C. Smith University
##Lenoir-Rhyne College
##Meredith College
##Montreat College
##Mount Olive College
##North Carolina A&T State University
##North Carolina Central University
##North Carolina School of the Arts
##North Carolina State University
##Piedmont Baptist College
##Saint Augustine's College
##Salem College
##University of North Carolina
##University of North Carolina - Asheville
##University of North Carolina - Chapel Hill
##University of North Carolina - Charlotte
##University of North Carolina - Greensboro
##University of North Carolina - Pembroke
##University of North Carolina - Wilmington
##Wake Forest University
##Warren Wilson College
##Western Carolina University
##Wingate College
##Winston-Salem State University
##Dickinson State University
##Minot State University
##North Dakota State University
##North Dakota State University - Bottineau
##North Dakota State University - Fargo
##University of North Dakota
##Valley City State University
##Williston State College
##Air Force Institute of Technology
##Antioch College
##Antonelli College
##Art Academy of Cincinnati
##Ashland University
##Baldwin-Wallace College
##Bluffton College
##Bowling Green State University
##Capital University
##Case Western Reserve University
##Cedarville College
##Central State University
##Circleville Bible College
##Cleveland Institute of Art
##Cleveland Institute of Music
##Cleveland State University
##College of Mount St. Joseph
##Columbus State Community College
##David N. Myers College
##Denison University
##DeVRY Institute Of Technology
##Edison State Community College
##Franklin University
##Franciscan University of Steubenville
##Heidelberg College
##Hiram College
##John Carrol University
##Kent State University
##Kent State University - Trumbull
##Kenyon College
##Kettering College of Medical Arts
##Lima Technical College
##Malone College
##Marietta College
##Miami - Jacobs College
##Miami University of Ohio
##Mount Carmel College of Nursing
##Mount Union College
##Mount Vernon Nazarene College
##Muskingum College
##Notre Dame College of Ohio
##Oberlin College
##Ohio Dominican College
##Ohio Northern University
##Ohio State University
##Ohio University
##Ohio University - Lancaster
##Ohio University - Zanesville
##Ohio Wesleyan University
##Shawnee University
##Tiffin University
##University of Akron
##University of Cincinnati
##University of Dayton
##University of Findlay
##University of Toledo
##Ursuline College
##Wilberforce University
##Wilmington College
##Wittenberg University
##Wooster College
##Wright State Uniuversity
##Xavier University
##Youngstown State University
##Cameron University
##East Central University
##Langston University
##Metropolitan College
##Northeast State University
##Oklahoma Baptist University
##Oklahoma Christian University of Science and Art
##Oklahoma City University
##Oklahoma State University
##Oral Roberts University
##Rogers State University
##St. Gregory's University
##Southeastern Oklahoma State University
##Southern Nazarene University
##Spartan School of Aeronautics
##University of Central Oklahoma
##University of Oklahoma
##University of Oklahoma Health Sciences Center
##University of Science & Arts of Oklahoma
##University of Tulsa
##Art Institute of Portland
##Concordia College 
##Eastern Oregon University
##George Fox University
##Lewis and Clark College
##Linfield College
##Marylhurst University
##Mount Angel Abbey and Seminary
##Northwest Christian College
##Oregon Graduate Institute
##Oregon Health Sciences University
##Oregon Institute of Technology
##Oregon State University
##Pacific University in Oregon
##Pacific Northwest College of the Arts
##Portland Community College
##Portland State University
##Reed College
##Southern Oregon University
##University of Oregon
##University of Portland
##Warner Pacific College
##Western Baptist College
##Western Oregon University
##Western States Chiropractic College
##Willamette University
##Albright College
##Allegheny College
##Allentown College
##Arcadia University
##Art Institute of Philadelphia
##Art Institute of Pittsburgh
##Bloomsburg University
##Bucknell University
##Bucks College
##Bryn Mawr College
##California University of Pennsylvania
##Carnegie Mellon University
##Chatham College
##Chestnut Hill College
##Cheyney State University
##Clarion University
##College Misericordia
##Delaware Valley College
##DeSales University
##Dickinson College
##Drexel University
##Duquesne University
##Eastern College
##East Stroudsburg University
##Edinboro University of Pennsylvania
##Elizabethtown College
##Franklin & Marshall College
##Gannon University
##Geneva College
##Gettysburg College
##Grove City College
##Haverford College
##Indiana University of Pennsylvania
##Juniata College
##Keystone College
##King's College
##Kutztown University of Pennsylvania
##La Salle University
##Lafayette College
##Lebanon Valley College
##Lehigh University
##Lincoln University of Pennsylvania
##Lock Haven University
##Lycoming College
##MCP Hahnemann University
##Marywood College
##Mercyhurst College
##Messiah College
##Millersville University of Pennsylvania
##Moravian College
##Muhlenberg College
##Peirce College
##Pennsylvania Academy of Fine Arts
##Pennsylvania College of Optometry
##Pennsylvania College of Technology
##Pennsylvania State University
##Philadelphia Biblical University
##Philadelphia University
##Point Park College
##Saint Joseph's University
##Saint Vincent College
##Shippensburg University
##Slippery Rock University
##Susquehanna University
##Swarthmore College
##Temple University
##Thiel College
##Thomas Jefferson University
##University of the Arts
##University of Pennsylvania
##University of Pittsburgh
##University of Pittsburgh at Johnstown
##University of Scranton
##University of the Arts
##University of the Sciences in Philadelphia
##Ursinus College
##Valley Forge Christian College
##Villanova University
##Washington and Jefferson College
##Waynesburg College
##West Chester University
##Westminster College
##Widener University
##Wilkes University
##York College of Pennsylvania
##Colegio Universitario Tecnologico de Bayamon
##Interamerican University of Puerto Rico
##Polytechnic University of Puerto Rico
##Pontifical Catholic University of Puerto Rico
##Sacred Heart University
##Universidad Central de Bayam&oacute;n
##University of Puerto Rico
##University of Puerto Rico - Aguadilla
##University of Puerto Rico - Mayag&uuml;ez
##University of Puerto Rico - Rio Piedras
##Brown University
##Bryant College
##Fraunhofer Center for Research in Computer Graphics
##Johnson & Wales University
##Providence College
##Rhode Island School of Design
##Roger Williams University
##Salve Regina University
##University of Rhode Island
##Allen University
##Anderson College
##Bob Jones University
##Charleston Southern University
##The Citadel
##Claflin College
##Clemson University
##Coastal Carolina University
##College of Charleston
##Columbia College
##Erskine College
##Francis Marion University
##Furman University
##Independent Colleges and Universities of South Carolina
##Medical University of South Carolina
##Morris College
##Presbyterian College
##South Carolina State University
##Southern Wesleyan University
##Trident Technical College
##University of South Carolina
##University of South Carolina - Aiken
##University of South Carolina - Beaufort
##University of South Carolina - Columbia
##University of South Carolina - Spartanburg
##Voorhees College
##Winthrop University
##Wofford College
##Augustana College
##Dakota State University
##Northern State University
##South Dakota School of Mines and Technology
##South Dakota State University
##Stanton University
##University for Professional Studies
##University of Sioux Falls
##University of South Dakota
##Austin Peay State University
##Belmont University
##Carson-Newman College
##Christian Brothers University
##East Tennessee State University
##Fisk University
##Freed-Hardeman University
##Harding University Graduate School of Religion
##Knoxville College
##Lambuth University
##Lee University
##Lincoln Memorial University
##Lipscomb University
##Meharry Medical College
##Middle Tennessee State University
##Rhodes College
##Roane State Community College
##Sewanee, The University of the South
##Southern Adventist University
##Tennessee State University
##Tennessee Technological University
##Tennessee Temple University
##Trevecca Nazarene University
##Tusculum College
##Union University
##University of Memphis
##University of Tennessee
##University of Tennessee - Chattanooga
##Univeristy of Tennessee - Knoxville
##University of Tennessee - Martin
##University of Tennessee - Memphis
##University of Tennessee Space Institute
##Vanderbilt University
##Walters State Community College
##Abilene Christian University
##Angelo State University
##Art Institute of Dallas
##Art Institute of Houston
##Austin College
##Baylor University
##Bee County College
##Blinn College
##College of the Mainland
##Collin County Community College District
##Concordia College
##Dallas Baptist University
##Dallas County Community College District
##El Paso Community College
##Houston Community College System
##Huston-Tillotson College
##Lamar University
##LeTourneau University
##Lubbock Christian University
##McMurry University
##Midwestern State University
##Navarro College
##North Harris Montgomery Community College District
##Our Lady of the Lake University
##Paris Junior College
##Prairie View A&M University
##Rice University
##Saint Edward's University
##Saint Mary's University of San Antonio
##Sam Houston State University
##San Antonio College
##Schreiner College
##South Texas College of Law
##Southern Methodist University
##Southwestern University
##Southwest Texas State University
##Stephen F. Austin State University
##Sul Ross State University
##Tarleton State University
##Tarrant County College
##Texas A&M University
##Texas A&M University - Commerce
##Texas A&M University - Corpus Christi
##Texas A&M University - Galveston
##Texas A&M University - Kingsville
##Texas A&M University - Texarkana
##Texas Christian University
##Texas Lutheran University
##Texas Southern University
##Texas State Technical College - Harlingen
##Texas State Technical College at Waco
##Texas Tech University
##Texas Tech University Health Sciences Center
##Texas Wesleyan University
##Texas Woman's University
##Trinity University
##University of Dallas
##University of Houston
##University of Mary Hardin-Baylor
##University of North Texas
##University of St. Thomas
##University of Texas - Austin
##University of Texas - Arlington
##University of Texas - Brownsville
##University of Texas - Dallas
##University of Texas - El Paso
##University of Texas - Houston
##University of Texas - Pan American
##University of Texas - San Antonio
##University of Texas - TeleCampus
##University of Texas - Tyler
##University of Texas Medical Branch - Galveston
##University of Texas Southwestern Medical Center at Dallas
##University of the Incarnate Word
##Wayland Baptist University
##West Texas A&M University
##Westwood College
##Wiley College
##Brigham Young University
##College of Eastern Utah
##Dixie College
##Hawthorne University
##LDS Business College
##Salt Lake Community College
##Southern Utah University
##Snow College
##University of Phoenix
##University of Utah
##Utah State University
##Utah Valley State College
##Weber State University
##Westminster College of Salt Lake City
##Bennington College
##Castleton State College
##Green Mountain College
##Johnson State College
##Lyndon State College of Vermont
##Marlboro College
##Middlebury College
##Norwich University
##Saint Michael's University
##University of Vermont
##Vermont Technical College
##American Open University
##Art Institute of Washington
##Bridgewater College
##Christopher Newport University
##ECPI College of Technology
##Eastern Mennonite University
##George Mason University
##Germanna Community College
##Hampden-Sydney College
##Hampton University
##Hollins College
##Illawarra College
##James Madison University
##Liberty University
##Longwood College
##Lynchburg College
##Mary Baldwin College
##Mary Washington College
##Marymount University
##Norfolk State University
##Old Dominion University
##Radford University
##Randolph-Macon College
##Randolph-Macon Woman's College
##Regent University
##Roanoke College
##Saint Paul's College
##Shenandoah University
##Strayer University
##Sweet Briar College
##University of Richmond
##University of Virginia
##University of Virginia's College at Wise
##Virginia Commonwealth University
##Virginia International University
##Virginia Military Institute
##Virginia State University
##Virginia Tech
##Virginia Wesleyan College
##Washington & Lee University
##William & Mary
##Antioch University Seattle
##Art Institute of Seattle
##Central Washington University
##City University
##Eastern Washington University
##Evergreen State College
##Gonzaga University
##Henry Cogswell College
##Heritage College
##Northwest College of Art
##Pacific Lutheran University
##Saint Martin's College
##Seattle Pacific University
##Seattle University
##University of Puget Sound
##University of Washington
##Vancouver University Colleges World Wide
##Walla Walla College
##Washington State University
##Washington State University at Tri-Cities
##Washington State University Spokane
##Western Washington University
##Whitman College
##Whitworth College
##American InterContinental University
##American University
##Catholic University of America
##Gallaudet University
##George Washington University
##Georgetown University
##Howard University
##Southeastern University
##Strayer University
##Trinity College
##University of the District of Columbia
##Alderson-Broaddus College
##Bethany College
##Bluefield State College
##Concord College
##Davis and Elkins College
##Fairmont State College
##Glenville State College
##Marshall University
##Salem-Teikyo University
##Shepherd College
##University of Charleston
##West Liberty State College
##Wheeling Jesuit University
##West Virginia State College
##West Virginia University
##West Virginia Wesleyan College
##Alverno College
##Cardinal Stritch University
##Carroll College
##Carthage College
##Concordia University 
##Edgewood College
##Lakeland College
##Lawrence University
##Marian College
##Marquette University
##Milwaukee Institute of Art & Design
##Milwaukee School of Engineering
##Mount Mary College
##Mount Senario College
##Northland College
##Ripon College
##Saint Norbert College
##University of Wisconsin - Eau Claire
##University of Wisconsin - Green Bay
##University of Wisconsin - La Crosse
##University of Wisconsin - Madison
##University of Wisconsin - Milwaukee
##University of Wisconsin - Oshkosh
##University of Wisconsin - Parkside
##University of Wisconsin - Platteville
##University of Wisconsin - River Falls
##University of Wisconsin - Stevens Point
##University of Wisconsin - Stout
##University of Wisconsin - Superior
##University of Wisconsin - Wausau
##University of Wisconsin - Whitewater
##University of Wisconsin Colleges
##Casper College
##Hamilton University
##Northwest College
##University of Wyoming
##Western Wyoming Community College
