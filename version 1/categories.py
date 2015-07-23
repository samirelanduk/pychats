import matplotlib.pyplot as plt
import datetime
import pickle

def get_MPM(person):
    months = []
    data = []
    messages = [x for x in person["messages"] if x["time"] >= datetime.datetime(2011,1,1,0,0,1)]
    try:
        first_month = datetime.datetime(messages[0]["time"].year, messages[0]["time"].month, 1)
    except:
        print(messages)
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

#Get the dump
dump = input("Where is the dump? ")
f = open(dump, "rb")
folks = pickle.load(f)

oldest = datetime.datetime.now()
newest = datetime.datetime(1900,1,1)
for person in folks:
    if person["messages"][0]["time"] < oldest: oldest = person["messages"][0]["time"]
    if person["messages"][-1]["time"] > newest: newest = person["messages"][-1]["time"]

#Get a list of all months
months = []
first_month = datetime.datetime(2011, 1, 1)
last_month = datetime.datetime(newest.year, newest.month, 1)
months.append(first_month)
while months[-1] != last_month:
    if months[-1].month == 12:
        months.append(datetime.datetime(months[-1].year+1,1,1))
    else:
        months.append(datetime.datetime(months[-1].year,months[-1].month+1,1))
months = [{"month":x, "total":0, "sms":0, "whatsapp":0, "facebook":0} for x in months][:-1]

#Add data to months
for person in [x for x in folks if x["messages"][-1]["time"] > datetime.datetime(2011,1,1)]:
    these_months, message_chars = get_MPM(person)
    d = dict(zip(these_months, message_chars))
    for sub_month in d.keys():
        for month in months:
            if sub_month == month["month"]:
                month["total"] += d[sub_month]

#Charts
#Total messages
ticks = [x for x in [y["month"] for y in months] if x.month == 1]
tick_labels = [str(x.day) + "/" + str(x.month) + "/" + str(x.year)[2:] for x in ticks]
plt.plot([y["month"] for y in months], [y["total"] for y in months], color="r")
plt.xticks(ticks, tick_labels)
plt.grid(b=True, which='major', color='k', linestyle='--')
plt.title("Total messages")
plt.xlabel("Date")
plt.ylabel("Messages (chars)")
dirname = "\\".join(dump.split("\\")[:-1])
plt.savefig(dirname + "\\html\\charts\\total.pdf")
