def genColor(status):
    print(f"Line Status: {status}")
    if status == "Major Delays":
        return(0xef4135)
    if status == "Good Service":
        return(0x90af53)
    if status == "Minor Delays":
        return(0xe87801)
    if status == "Suspended":
        return(0x3d3d3d)
    if status == "Planned Works":
        return(0xffd500)
    
def statusEmoji(status):
    print(f"Line Status: {status}")
    if status == "Major Delays":
        return('<:majordisruptions:1267414600266289152>')
    if status == "Good Service":
        return('<:goodservice:1267414598353682463>')
    if status == "Minor Delays":
        return('<:MinorDelays:1267414596499538011>')
    if status == "Suspended" or status == 'Part Suspended':
        return('<:suspended:1267414594272362537>')
    if status == "Planned Works":
        return('<:Plannedworks:1267414592187924532>')

def getColor(type):
    if type == "metro" or type == "0":
        return(0x0072ce)
    if type == "tram" or type == "1":
        return(0x78be20)
    if type == "bus" or type =="2":
        return(0xff8400)
    if type == "vline" or type =="3":
        return(0x8f1a95)

def getEmojiColor(line):
    if line == "Lilydale" or line =="Belgrave" or line =="Alamein" or line =='Glen Waverley':
        return('<:burnley:1245673094509760562>')
    if line == "Pakenham" or line =="Cranbourne":
        return('<:metrotunnel:1245673090495680533>')
    if line == "Hurstbridge" or line =="Mernda":
        return('<:cliftonhill:1245673092655878174>')
    if line == "Frankston" or line =="Williamstown" or line =='Werribee' or line == 'Stony Point':
        return('<:frankston:1245673086360092735>')    
    if line == "Upfield" or line =="Sunbury" or line =='Craigieburn':
        return('<:northern:1245673088314638431>')    
    if line == "Sandringham":
        return('<:crosscity:1245673084187578368>')
    if line == 'City Loop':
        return('<:cityloop:1265627754473197630>')  
    else:
        return('<:other:1245674664647331860>')
    
def setEmoji(type):
    if type == "X'Trapolis 100":
        return('<:xtrapolis100_0_0:1287718276318625854><:xtrapolis100_1_0:1287718278554193955><:xtrapolis100_2_0:1287718281003663360><:xtrapolis100_3_0:1287718282962403390><:xtrapolis100_4_0:1287718288524054558><:xtrapolis100_5_0:1287718291267391509><:xtrapolis100_6_0:1287718293473464320><:xtrapolis100_7_0:1287718295436267553><:xtrapolis100_8_0:1287718297382551684><:xtrapolis100_9_0:1287718300138340383><:xtrapolis100_10_0:1287718302420041749><:xtrapolis100_11_0:1287718304751943722><:xtrapolis100_12_0:1287718306693910538><:xtrapolis100_13_0:1287718271172214836><:xtrapolis100_14_0:1287718273810432010>')
    if type == "EDI Comeng":
        return('<:edicomeng_0_0:1287720880788602900><:edicomeng_1_0:1287720883619758100><:edicomeng_2_0:1287720885695811657><:edicomeng_3_0:1287720888317251594><:edicomeng_4_0:1287720891228094474><:edicomeng_5_0:1287720893673635840><:edicomeng_6_0:1287720896399937616><:edicomeng_7_0:1287720898769457183><:edicomeng_8_0:1287720901479104562><:edicomeng_9_0:1287720909863522429><:edicomeng_10_0:1287720912170389546><:edicomeng_11_0:1287720914729042002><:edicomeng_12_0:1287720916905758740><:edicomeng_13_0:1287720919074082868><:edicomeng_14_0:1287720921414500444><:edicomeng_15_0:1287720924166098946>')
    if type == "Alstom Comeng":
        return('<:alstomcomeng_0_0:1287721815564746812><:alstomcomeng_1_0:1287721818320273459><:alstomcomeng_2_0:1287721820933455934><:alstomcomeng_3_0:1287721824377110590><:alstomcomeng_4_0:1287721833457520640><:alstomcomeng_5_0:1287721836271894598><:alstomcomeng_6_0:1287721838859911250><:alstomcomeng_7_0:1287721841133223958><:alstomcomeng_8_0:1287721843456741386><:alstomcomeng_9_0:1287721849282756699><:alstomcomeng_10_0:1287721851459731538><:alstomcomeng_11_0:1287721854404136990><:alstomcomeng_12_0:1287721856471662673><:alstomcomeng_13_0:1287721858690580541><:alstomcomeng_14_0:1287721861341253642><:alstomcomeng_15_0:1287721863748780103>')
    if type == "Siemens Nexas":
        return('<:siemens_0_0:1287724228409425941><:siemens_1_0:1287724231370477578><:siemens_2_0:1287724233832792176><:siemens_3_0:1287724236823330936><:siemens_4_0:1287724242129129503><:siemens_5_0:1287724245090304011><:siemens_6_0:1287724249104257086><:siemens_7_0:1287724252531003453><:siemens_8_0:1287724255219421256><:siemens_9_0:1287724258910277642><:siemens_10_0:1287724261569728603><:siemens_11_0:1287724263545114706><:siemens_12_0:1287724266283864124><:siemens_13_0:1287724268695846993><:siemens_14_0:1287724271023689760>')
    if type == "VLocity":
        return('<:vlocity_0_0:1287723159168225342><:vlocity_1_0:1287723162129137755><:vlocity_2_0:1287723164432076830><:vlocity_3_0:1287723166323572818><:vlocity_4_0:1287723168496222209><:vlocity_5_0:1287723170698235987><:vlocity_6_0:1287723177861976117><:vlocity_7_0:1287723179510333463><:vlocity_8_0:1287723182287093865><:vlocity_9_0:1287723184573124639><:vlocity_10_0:1287723186611552296><:vlocity_11_0:1287723188490600491><:vlocity_12_0:1287723190461665343><:vlocity_13_0:1287723192663937068><:vlocity_14_0:1287723194970800139><:vlocity_15_0:1287723197218816075><:vlocity_16_0:1287723199265505280><:vlocity_17_0:1287723201027375197><:vlocity_18_0:1287723264105386074><:vlocity_19_0:1287723206928498798>')
    else:
        return