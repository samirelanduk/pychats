import pickle
import datetime
import calendar
import matplotlib.pyplot as plt
import os

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

#Looks for svg.svg and returns its xml text
def getSVG():
    f = open("svg.svg", "r")
    xml = f.read()
    f.close()
    return xml

def addMessages(messages, name):
    html = "<table>\n\t<tr><td class='name'></td><td style='width: 200px;'></td><td></td><td style='width: 200px;'></td><td class='name'></td></tr>\n"
    for message in messages:
        html += "\t<tr>"
        if message["from_me"]:
            html += "<td></td><td></td>"
        else:
            html += "<td class='name left'>" + message["sender"].split(" ")[0] + "</td>"
        html += "<td colspan='2'>"
        html += "<div class='time'>" + str(message["time"].strftime("%Y-%m-%d %H:%M:%S")) + "</div>"
        html += "<p class='message "
        html += message["type"]
        if not message["from_me"]:
            html += " them"
        if message["group"]:
            html += " group"
        if not message["from_me"] and message["weight"] == 0:
            html += " fade"
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
        print("Couldn't find " + name)

def get_MPD(person):
    days = []
    data = []
    messages = [x for x in person["messages"] if x["time"] >= datetime.datetime(2011,1,1,0,0,1)]
    first_day = datetime.datetime(messages[0]["time"].year, messages[0]["time"].month, messages[0]["time"].day)
    last_day = datetime.datetime(newest.year, newest.month, newest.day)
    days.append(first_day)
    while days[-1] != last_day:
        days.append(days[-1] + datetime.timedelta(days=1))
    for day in days:
        value = 0
        for message in messages:
            if day.year == message["time"].year and day.month == message["time"].month and day.day == message["time"].day and message["text"] != None:
                value += (message["weight"] * len(message["text"]))
        data.append(value)
        value = 0
    return (days, data)


def get_maMPD(person):
    days, data = get_MPD(person)
    avg_data = []
    data = ([0] * 30) + data
    for x in range(len(days)):
        avg_data.append(sum(data[x:x+30])/30)
    
    return (days, avg_data)
                

def get_MPM(person):
    months = []
    data = []
    messages = [x for x in person["messages"] if x["time"] >= datetime.datetime(2011,1,1,0,0,1)]
    first_month = datetime.datetime(messages[0]["time"].year, messages[0]["time"].month, 1)
    last_month = datetime.datetime(newest.year, newest.month, 1)
    months.append(first_month)
    while months[-1] != last_month:
        if months[-1].month == 12:
            months.append(datetime.datetime(months[-1].year+1,1,1))
        else:
            months.append(datetime.datetime(months[-1].year,months[-1].month+1,1))
    for month in months:
        value = 0
        for message in messages:
            if month.year == message["time"].year and month.month == message["time"].month and message["text"] != None:
                value += (message["weight"] * len(message["text"]))
        data.append(value)
        value = 0
    return (months, data)


def get_maMPM(person):
    months, data = get_MPM(person)
    avg_data = []
    data = ([0] * 3) + data
    for x in range(len(months)):
        avg_data.append(sum(data[x:x+3])/3)
    
    return (months, avg_data)

def outputPerson(person):
    #Add the header stuff
    html = "<html>\n"
    html += "<head>\n"
    html += "\t<title>" + person["name"] + "</title>\n"
    html += """\t<style>body {font-family: Georgia; text-align: center;}
svg {display: block; margin-left: auto; margin-right: auto;}
h1, h2, h3, h4 {text-align: center;}
h4 {margin-bottom: 3px;}
#nav {display: inline-block; padding: 30px; border-radius: 25px; margin-bottom: 30px; border: 1px solid black; margin-left: auto; margin-right: auto;}
#nav td {width: 70px;}
#nav a {text-decoration: none;}
table {border-collapse:collapse;width:700px;margin-left:auto;margin-right:auto;table-layout:fixed}
table#charts {width: 80%;}
.time {color: gray; font-size: 70%; margin-left: 10px; margin-bottom: 1px;}
td {word-wrap:break-word;}
td.name {width: 100px; padding: 0px;}
td.left {text-align: right; padding-right: 4px;}
td.right {text-align: left; padding-left: 4px;}
td p {margin-bottom: 20px; margin-top: 0px; padding: 10px; border-radius: 15px; font-family: Helvetica;}
p.SMS {border: 2px solid #66FF33; color: white; background-color: #66FF33;}
p.whatsapp {border: 2px solid #660033; color: white; background-color: #660033;}
p.facebook {border: 2px solid #00F; color: white; background-color: #00F;}
p.them {color: black; background-color: #DDD;}
p.group {border-style:dotted;}
p.fade {opacity: 0.3;}</style>\n"""
    html += "</head>\n"
    html += "<body>\n"
    html += "\t<h1>" + person["name"] + "</h1>\n"

    html += "<table id='charts'>\n"
    html += "<tr>\n"

    #Add a piechart
    data = {"SMS":0,"whatsapp":0,"facebook":0}
    for m in person["messages"]:
        data[m["type"]] += m["weight"]
    color = []
    if data["SMS"] != 0: color.append("Green")
    if data["whatsapp"] != 0: color.append("Purple")
    if data["facebook"] != 0: color.append("Blue")
    plt.pie([x for x in [data["SMS"], data["whatsapp"], data["facebook"]] if x != 0], labels=[x for x in ["SMS", "whatsapp", "facebook"] if data[x] != 0], colors=color,)
    plt.savefig("svg.svg")
    pie_svg = getSVG()
    html += "<td colspan='4' style='padding:30px;'>" + pie_svg + "</td></tr>\n"
    plt.clf()
    
    #Add days bar graph
    days, data = get_MPD(person)
    plt.bar(days, data, color="r", edgecolor="none", width=2)
    ticks = [x for x in days if x.month == 1 and x.day == 1]
    tick_labels = [str(x.day) + "/" + str(x.month) + "/" + str(x.year)[2:] for x in ticks]
    plt.xticks(ticks, tick_labels)
    plt.grid(b=True, which='major', color='k', linestyle='--')
    plt.title("Messages per day")
    plt.xlabel("Date")
    plt.ylabel("Messages (chars)")
    plt.savefig("svg.svg")
    bar1_svg = getSVG()
    html += "<tr><td colspan='4'>" + bar1_svg + "</td></tr>\n"
    plt.clf()

    #Add days line graph
    days, data = get_maMPD(person)
    plt.plot(days, data, color="r")
    plt.xticks(ticks, tick_labels)
    plt.grid(b=True, which='major', color='k', linestyle='--')
    plt.title("Messages per day (Moving average)")
    plt.xlabel("Date")
    plt.ylabel("Messages (chars)")
    plt.savefig("svg.svg")
    line1_svg = getSVG()    
    html += "<tr><td colspan='4'>" + line1_svg + "</td></tr>\n"
    plt.clf()

    html += "<tr>\n"

    #Add months bar graph
    months, data = get_MPM(person)
    plt.bar(months, data, color="c", width=15)
    ticks = [x for x in days if x.month == 1 and x.day == 1]
    tick_labels = [str(x.day) + "/" + str(x.month) + "/" + str(x.year)[2:] for x in ticks]
    plt.xticks(ticks, tick_labels)
    plt.grid(b=True, which='major', color='k', linestyle='--')
    plt.title("Messages per month")
    plt.xlabel("Date")
    plt.ylabel("Messages (chars)")
    plt.savefig("svg.svg")
    bar2_svg = getSVG()
    html += "<td colspan='4'>" + bar2_svg + "</td></tr>\n"
    plt.clf()

    #Add months line graph
    months, data = get_maMPM(person)
    plt.plot(months, data, color="c", linewidth=2)
    plt.xticks(ticks, tick_labels)
    plt.grid(b=True, which='major', color='k', linestyle='--')
    plt.title("Messages per month (3-month moving average)")
    plt.xlabel("Date")
    plt.ylabel("Messages (chars)")
    plt.savefig("svg.svg")
    line2_svg = getSVG()
    html += "<tr><td colspan='4'>" + line2_svg + "</td></tr>\n"
    plt.clf()
    html += "</table>\n"
    
    #Rejigger the messages into years, months and days
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
                html += addMessages(day["messages"], person["name"])
    
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
    os.remove("svg.svg")

def compareMulti(people):
    dicts = []
    first_day = datetime.datetime.now()
    last_day = datetime.datetime(newest.year,newest.month,newest.day)
    for person in people:
        if person["messages"][0]["time"] < first_day: first_day = person["messages"][0]["time"]
        days,values = get_maMPD(person)
        dicts.append(dict(zip(days,values)))
    first_day = datetime.datetime(first_day.year,first_day.month,first_day.day)
    days = [first_day]
    while days[-1] != last_day:
        days.append(days[-1] + datetime.timedelta(days=1))
    days = [x for x in days if x >= datetime.datetime(2011,1,1)]
    data = []
    for d in dicts:
        series = []
        for day in days:
            series.append(d[day]) if day in d.keys() else series.append(0)
        data.append(series)
    x = 0
    for d in data:
        plt.plot(days,d,label=people[x]["name"])
        x += 1
    ticks = [x for x in days if x.month == 1 and x.day == 1]
    tick_labels = [str(x.day) + "/" + str(x.month) + "/" + str(x.year)[2:] for x in ticks]
    plt.xticks(ticks, tick_labels)
    plt.legend()
    plt.show()


def compareGroups():
    #Get the pickled file with the groups
    f = open(dump[:len(dump) - dump[::-1].find("\\")] + "categories.p", "rb")
    categories = pickle.load(f)
    groups = {}
    for c in categories.keys():
        groups[c] = [findPerson(x) for x in categories[c] if x in [y["name"] for y in folks]]
        groups[c] = [get_maMPD(x) for x in groups[c]]
    first_day = datetime.datetime(2011,1,1)
    last_day = datetime.datetime(newest.year,newest.month,newest.day)
    days = [first_day]
    while days[-1] != last_day:
        days.append(days[-1] + datetime.timedelta(days=1))
    data = {}
    for g in groups.keys():
        data[g] = []
        for day in days:
            value = 0
            for pair in groups[g]:
                dic = dict(zip(pair[0],pair[1]))
                if day in dic.keys(): value += dic[day]
            data[g].append(value)
    plots= []
    for d in data.keys():
        plt.plot(days,data[d],label=d)
    plt.legend()
    ticks = [x for x in days if x.month == 1 and x.day == 1]
    tick_labels = [str(x.day) + "/" + str(x.month) + "/" + str(x.year)[2:] for x in ticks]
    plt.xticks(ticks, tick_labels)
    plt.show()
    
    
