import pickle
import datetime
import calendar

f = open("backups//dump.p", "rb")
folks = pickle.load(f)

def printMessage(message, person):
    sender = ""
    if message["sender"] == "Sam Ireland" or message["sender"] == "Sam":
        sender = "me "
    else:
        sender = "them "
    html = "<div class = 'time " + sender + "'>&nbsp;&nbsp;" + str(message["time"]) + "</div>\n"
    html += "<div class='message "
    html += sender
    html += message["type"]
    if message["sender"] != "Sam" and message["sender"] != "Sam Ireland" and message["sender"] != "Them" and message["sender"] != person:
        html += " group" 
    html += "'>"
    html += message["text"]
    html += "</div>\n"
    return html        

def produceOutput(person):
    #Temp
    for m in person["messages"]:
        if "type" not in m.keys():
            m["type"] = "unknown"
    
    #The header stuff
    html = "<html>\n"
    html += "<head>\n"
    html += "<title>" + person["name"] + "</title>\n"
    html += """<style>body {font-family: Helvetica; font-size:90%;} .time {font-size: 75%; color: gray;} .message {margin-bottom: 20px; width: 300px; border: px solid; border-radius: 20px; padding: 10px;}
.me {margin-left: 200px} .facebook {border: 2px solid blue;} .sms {border: 2px solid red;} .whatsapp {border: 2px solid green;} .group {opacity: 0.25;} #nav {border: 1px solid black; display: inline-block; padding: 10px;}
#nav a {text-decoration: none;}</style>\n"""
    html += "</head>\n"
    html += "<body>\n"
    html += "<h1>" + person["name"] + "</h1>\n"
    print(html)

    #Get a dictionary of years and assign each all the messages
    year_list = set([int(m["time"].year) for m in person["messages"]])
    years = {y:{"messages":[]} for y in year_list}

    #Give each year its messages
    for message in person["messages"]:
        years[message["time"].year]["messages"].append(message)

    #For each year, get the months
    for year in year_list:
        months_list = set([m["time"].month for m in years[year]["messages"]])
        years[year]["months_list"] = months_list
        years[year]["months"] = {m:{"messages":[]} for m in months_list}
        for message in years[year]["messages"]:
            years[year]["months"][message["time"].month]["messages"].append(message)

    #make the nav bar
    html += "<div id='nav'>\n"
    for y in year_list:
        html += "<a href='#" + str(y) + "'>" + str(y) + "</a><br>"
        for m in years[y]["months_list"]:
            html += "&nbsp;&nbsp;&nbsp;&nbsp;<a href='#" + str(y) + str(m) + "'>" + calendar.month_name[int(m)] + "</a><br>"
    html += "</div>"

    #Print messages
    for y in year_list:
        years[y]["messages"] = sorted(years[y]["messages"], key=lambda k: k["time"])
        html += "<a id='" + str(y) + "'><h2>" + str(y) + "</h2></a>\n"
        for m in years[y]["months_list"]:
            html += "<a id='" + str(y) + str(m) + "'><h3>" + calendar.month_name[int(m)] + "</h3></a>\n"
            years[y]["months"][m]["messages"] = sorted(years[y]["months"][m]["messages"], key=lambda k: k["time"])
            for message in years[y]["months"][m]["messages"]:
                html += printMessage(message, person["name"])
        
    html += "</body>\n"
    html += "</html>"
    
    f = open("outputs/" + person["name"] + ".html", "w")
    for char in html:
        try:
            f.write(char)
        except:
            f.write("?")
    f.close()
