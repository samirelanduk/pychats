import pickle
import datetime
import calendar

#Get the dump
dump = input("Where is the dump? ")
f = open(dump, "rb")
folks = pickle.load(f)

#Spit out some general information
print("\nThere are " + str(len(folks)) + " people represented here.")

oldest = datetime.datetime.now()
newest = datetime.datetime(1900,1,1)
sms_count = 0
fb_count = 0
whatsapp_count = 0
for person in folks:
    if person["messages"][0]["time"] < oldest: oldest = person["messages"][0]["time"]
    if person["messages"][-1]["time"] > newest: newest = person["messages"][-1]["time"]
    for message in person["messages"]:
        if message["type"] == "SMS": sms_count += 1
        if message["type"] == "facebook": fb_count += 1
        if message["type"] == "whatsapp": whatsapp_count += 1
        
print("Messages range from " + str(oldest) + " to " + str(newest))
print("Messages breakdown:\n\tSMS: " + str(round(sms_count/(sms_count+fb_count+whatsapp_count)*100,1)) + "%\n\tFacebook: " + str(round(fb_count/(sms_count+fb_count+whatsapp_count)*100,1)) + "%\n\tWhatsapp: " + str(round(whatsapp_count/(sms_count+fb_count+whatsapp_count)*100,1)) + "%")

def addMessages(messages):
    html = "<table>\n\t<tr><td class='name'></td><td style='width: 200px;'></td><td></td><td style='width: 200px;'></td><td class='name'></td></tr>\n"
    for message in messages:
        html += "\t<tr>"
        if message["from_me"]:
            html += "<td></td><td></td>"
        else:
            html += "<td class='name left'>" + message["sender"].split(" ")[0] + "</td>"
        html += "<td colspan='2'>"
        html += "<div class='time'>" + str(message["time"]) + "</div>"
        html += "<p class='message "
        html += message["type"]
        if not message["from_me"]:
            html += " them"
        html += "'>"
        if message["text"] is None:
            html += "NONE_TEXT"
        else:
            html += message["text"]
        html += "</p></td>"
        if not message["from_me"]:
            html += "<td></td><td></td></tr>"
        else:
            html += "<td class='name right'>" + message["sender"].split(" ")[0] + "</td>"
        html += "\n"
    html += "</table>\n"
    return html

#This function depends on the global variable "folks". Yes you're not supposed to do that. No I'm not going to change it.
def findPerson(name):
    found = False
    for person in folks:
        if person["name"] == name:
            return person
        found = True
    if not found:
        print("Couldn't find them, not returning anything.")

        
def outputPerson(person):
    #Add the header stuff
    html = "<html>\n"
    html += "<head>\n"
    html += "\t<title>" + person["name"] + "</title>\n"
    html += """\t<style>body {font-family: Georgia; text-align: center;}
h1, h2, h3, h4 {text-align: center;}
h4 {margin-bottom: 3px;}
#nav {display: inline-block; padding: 30px; border-radius: 25px; margin-bottom: 30px; border: 1px solid black; margin-left: auto; margin-right: auto;}
#nav td {width: 70px;}
#nav a {text-decoration: none;}
table {border-collapse:collapse;width:700px;margin-left:auto;margin-right:auto;table-layout:fixed}
.time {color: gray; font-size: 70%; margin-left: 10px; margin-bottom: 1px;}
td {word-wrap:break-word;}
td.name {width: 100px; padding: 0px;}
td.left {text-align: right; padding-right: 4px;}
td.right {text-align: left; padding-left: 4px;}
td p {margin-bottom: 20px; margin-top: 0px; padding: 10px; border-radius: 15px; font-family: Helvetica;}
p.SMS {border: 2px solid #66FF33; color: white; background-color: #66FF33;}
p.them {color: black; background-color: #DDD;}</style>\n"""
    html += "</head>\n"
    html += "<body>\n"
    html += "\t<h1>" + person["name"] + "</h1>\n"

    #Rejigger the missages into years, months and days
    year_list = set([int(m["time"].year) for m in person["messages"]])
    years = [{"year":y, "messages":[], "month_list":[], "months":[]} for y in year_list]

    for year in years:
        year["messages"] = [m for m in person["messages"] if int(m["time"].year) == int(year["year"])]
        year["month_list"] = sorted(list(set([m["time"].month for m in person["messages"] if int(m["time"].year) == int(year["year"])])))
        year["months"] = [{"month":m, "messages":[], "day_list":[], "days":[]} for m in year["month_list"]]
        for month in year["months"]:
            month["messages"] = [m for m in year["messages"] if int(m["time"].month) == int(month["month"])]
            month["day_list"] = sorted(list(set([m["time"].day for m in year["messages"] if int(m["time"].month) == int(month["month"])])))
            month["days"] = [{"day":d, "messages":[]} for d in month["day_list"]]
            for day in month["days"]:
                day["messages"] = [m for m in month["messages"] if int(m["time"].day) == int(day["day"])]
        
    #Add the nav bar
    html += "<div id='nav'><table style='border-collapse: separate; width: auto; border-spacing: 20px 0px; margin-left: 0px; margin-right: 0px;'><tr>"
    for year in years:
        html += "<td style='vertical-align:top'><a href='#" + str(year["year"]) + "'>" + str(year["year"]) + "</a><br>"
        for month in year["month_list"]:
            html += "&nbsp;&nbsp;&nbsp;&nbsp;<a href='#" + str(year["year"]) + str(month) + "'>" + calendar.month_name[month] + "</a><br>"
        html += "</td>"
    html += "</tr></table></div>\n"

    #Add the messages
    for year in years:
        html += "<h2 id='" + str(year["year"]) + "'>" + str(year["year"]) + "</h2>\n"
        for month in year["months"]:
            html += "<h3 id='" + str(year["year"]) + str(month["month"]) + "'>" + calendar.month_name[month["month"]] + "</h3>\n"
            for day in month["days"]:
                html += "<h4>" + str(day["day"]) + " " + calendar.month_name[month["month"]] + "</h4>\n"
                html += addMessages(day["messages"])
    
    html += "</body>\n"
    html += "</html>"

    dirname = "\\".join(dump.split("\\")[:-1])
    f = open(dirname + "\\html\\" + person["name"] + ".html", "w")
    for char in list(html):
        try:
            f.write(char)
        except:
            f.write("?")
    f.close()
