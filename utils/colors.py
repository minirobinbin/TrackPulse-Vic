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
    
def getlineEmoji(type):
    if type == "Alamein":
        return('<:Alamein1:1298191533820084285><:Alamein2:1298191535854194720><:Alamein3:1298191746915893309>')
    if type == "Belgrave":
        return('<:Belgrave1:1298192329995456534><:Belgrave2:1298192428599083070><:Belgrave3:1298192440712499231>')
    if type == "Craigieburn":
        return('<:Craigieburn1:1299289280388272209><:Craigieburn2:1299289282761982032><:Craigieburn3:1299289284901081118><:Craigieburn4:1299289287782694922>')
    if type == "Cranbourne":
        return('<:Cranbourne1:1299289844131958815><:Cranbourne2:1299289846707126312><:Cranbourne3:1299289848565465160><:Cranbourne4:1299289851182714892>')
    if type == "Flemington Racecourse":
        return('<:FlemingtonRacecourse1:1299290568601636895><:FlemingtonRacecourse2:1299290570488811531><:FlemingtonRacecourse3:1299290572669849610><:FlemingtonRacecourse4:1299290574691504189><:FlemingtonRacecourse5:1299290577392766977><:FlemingtonRacecourse6:1299290580018397195><:FlemingtonRacecourse7:1299290583835213826><:FlemingtonRacecourse8:1299290585886228480>')
    if type == "Frankston":
        return('<:Frankston1:1299291143305170964><:Frankston2:1299291145355919412><:Frankston3:1299291147125915648><:Frankston4:1299291149323993168>')
    if type == "Glen Waverley":
        return('<:GlenWaverley1:1299291654364332083><:GlenWaverley2:1299291656805290025><:GlenWaverley3:1299291661867941950><:GlenWaverley4:1299291663830880287><:GlenWaverley5:1299291666490064907>')
    if type == "Hurstbridge":
        return('<:Hurstbridge1:1299603341021806604><:Hurstbridge2:1299603343358038066><:Hurstbridge3:1299603345136291850><:Hurstbridge4:1299603347556401153>')
    if type == "Lilydale":
        return('<:Lilydale1:1299603855604191344><:Lilydale2:1299603857831100487><:Lilydale3:1299603860335235082>')
    if type == "Mernda":
        return('<:Mernda1:1299604211629162556><:Mernda2:1299604213319335976><:Mernda3:1299604215282532393>')
    if type == "Pakenham":
        return('<:Pakenham1:1299604711896256544><:Pakenham2:1299604713930756137><:Pakenham3:1299604716237361182><:Pakenham4:1299604717961216073>')
    if type == "Sandringham":
        return('<:Sandringham1:1299606162647416872><:Sandringham2:1299606164471812127><:Sandringham3:1299606166598455296><:Sandringham4:1299606168464920657><:Sandringham5:1299606170733907979>')
    if type == "Stony Point":
        return('<:StonyPoint1:1299615026394431518><:StonyPoint2:1299615028659486761><:StonyPoint3:1299615030823747595><:StonyPoint4:1299615032346279989>')
    if type == "Sunbury":
        return('<:Sunbury1:1299615798272458762><:Sunbury2:1299615800293851166><:Sunbury3:1299615802210652200>')
    if type == "Upfield":
        return('<:Upfield1:1299615804467187762><:Upfield2:1299615806547689514><:Upfield3:1299615808896503859>')
    if type == "Werribee":
        return('<:Werribee1:1299616316273201194><:Werribee2:1299616318714150922><:Werribee3:1299616323386609714>')
    if type == "Williamstown":
        return('<:Williamstown1:1299616796265156688><:Williamstown2:1299616798081024061><:Williamstown3:1299616799997825085><:Williamstown4:1299616802023936030><:Williamstown5:1299616804297117716>')
    else:
        return ''