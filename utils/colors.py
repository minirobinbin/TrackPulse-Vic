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