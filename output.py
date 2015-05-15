import pickle
import datetime
import calendar
import pygal
from pygal.style import Style

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


    html += "<table id='charts'>\n"
    html += "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>\n"
    html += "<tr>\n"

    #Add a piechart
    data = {"SMS":0,"whatsapp":0,"facebook":0}
    for m in person["messages"]:
        data[m["type"]] += m["weight"]
    pie_style = Style(colors=("#66FF33", "#660033", "#00F"))
    pie = pygal.Pie(style=pie_style)
    pie.title = "Messages by type"
    pie.add("SMS",data["SMS"])
    pie.add("whatsapp",data["whatsapp"])
    pie.add("facebook",data["facebook"])
    html += "<td></td><td></td><td colspan='4' style='padding:30px;'>" + pie.render().decode(encoding='UTF-8') + "</td><td></td><td></td></tr>\n"
    #Add days bar graph
    start_day = datetime.datetime(2011,1,1)
    end_day = datetime.datetime(newest.year, newest.month, newest.day)
    days = [start_day]
    while days[-1] <= end_day:
        days.append(days[-1] + datetime.timedelta(days=1))
    day_dict = {d:0 for d in days}
    for m in [m for m in person["messages"] if m["time"] >= start_day]:
        day = datetime.datetime(m["time"].year, m["time"].month, m["time"].day)
        if message["text"] is None:
            day_dict[day] += 0
        else:
            day_dict[day] += (message["weight"] * len(message["text"]))
    bar = pygal.Bar()
    bar.title = "Message rate"
    bar.x_labels = map(str, days)
    bar.add("Messages", [day_dict[d] for d in days])
    html += "<td colspan='4'>" + bar.render().decode(encoding='UTF-8') + "</td>\n"

    #Add days line graph
    avg_dates = days[30:]
    avg_dates_dict = {d:0 for d in avg_dates}
    for ad in range(len(avg_dates)):
        for d in days[ad:ad+30]:
            avg_dates_dict[avg_dates[ad]] += day_dict[d]
        avg_dates_dict[avg_dates[ad]] /= 30
    line = pygal.DateY(show_dots = False)
    line.title = "Moving Average"
    values = []
    for x in range(len(avg_dates)):
        values.append((avg_dates[x], avg_dates_dict[avg_dates[x]]))
    line.add("Messages", values)
    html += "<td colspan='4'>" + line.render().decode(encoding='UTF-8') + "</td>\n"
    html += "</tr>\n"

    html += "<tr>\n"

    month_style = Style(colors = ("#FF00FF", "#FFCCFF"))
    #Add months bar graph
    start_month = datetime.datetime(2011,1,1)
    end_month = datetime.datetime(newest.year, newest.month, 1)
    months = [start_month]
    while months[-1] < end_month:
        if months[-1].month == 12:
            months.append(datetime.datetime(months[-1].year+1,1,1))
        else:
            months.append(datetime.datetime(months[-1].year,months[-1].month+1,1))
    month_dict = {m:0 for m in months}
    for m in [m for m in person["messages"] if m["time"] >= start_day]:
        month = datetime.datetime(m["time"].year, m["time"].month, 1)
        if message["text"] is None:
            month_dict[month] += 0
        else:
            month_dict[month] += (message["weight"] * len(message["text"]))
    bar = pygal.StackedBar(style=month_style)
    bar.title = "Message rate"
    bar.x_labels = map(str, months)
    projection = [0] * (len(months) - 1)
    projected = ((month_dict[months[-1]] / newest.day) * 30) - month_dict[months[-1]]
    projection.append(projected)
    p_data = []
    for x in range(len(months)):
        p_data.append((months[x], projection[x]))
    bar.add("Messages", [month_dict[m] for m in months])
    bar.add("Projected", projection)
    html += "<td colspan='4'>" + bar.render().decode(encoding='UTF-8') + "</td>\n"

    #Add months line graph
    avg_months = months[3:]
    avg_months_dict = {m:0 for m in avg_months}
    for am in range(len(avg_months)):
        for m in months[am:am+3]:
            avg_months_dict[avg_months[am]] += month_dict[m]
        avg_months_dict[avg_months[am]] /= 3
    month_style = Style(colors = ("#FFCCFF", "#FF00FF"))
    line = pygal.DateY(show_dots = False, style=month_style)
    line.title = "Moving Average"
    values = []
    for x in range(len(avg_months)):
        values.append((avg_months[x], avg_months_dict[avg_months[x]]))
    avg_months_pro = months[3:]
    avg_months_dict_pro = {m:0 for m in avg_months_pro}
    for am in range(len(avg_months_pro)):
        for m in months[am:am+3]:
            if am == len(avg_months_pro) - 1:
                avg_months_dict_pro[avg_months_pro[am]] += projected + month_dict[m]
            else:
                avg_months_dict_pro[avg_months_pro[am]] += month_dict[m]
        avg_months_dict_pro[avg_months_pro[am]] /= 3
    values2 = []
    for x in range(len(avg_months_pro)):
        values2.append((avg_months_pro[x], avg_months_dict_pro[avg_months_pro[x]]))
    line.add("Projected", values2)
    line.add("Messages", values)
    html += "<td colspan='4'>" + line.render().decode(encoding='UTF-8') + "</td>\n"
    html += "</tr>\n"
    html += "</table>\n"
    
    
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
