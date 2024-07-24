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