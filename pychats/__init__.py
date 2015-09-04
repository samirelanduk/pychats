import copy
import random
import datetime
import calendar
from .outputs import BarChart, LineChart, PieChart, MultiLineChart, Figure

def get_facebook_backup(file, my_name=""):
    """Take a file connection to messages.htm, and make a Backup object of it"""
    from . import facebook
    from bs4 import BeautifulSoup

    #Need to know user's Facebook name
    if my_name == "":
        my_name = input("What is your Facebook name? ")

    #Open the file to get the html
    html = file.read()
    print("Getting soup (can take a few seconds)...")
    soup = BeautifulSoup(html)

    #Get conversations
    conversations = facebook.get_conversations(soup, my_name)

    #Divide into direct and group conversations
    directs = [x for x in conversations if len(x.members) == 1]
    groups = [x for x in conversations if len(x.members) > 1]

    #Define contacts as those with whom the user has spoken to directly
    contacts = list(set([conv.members[0] for conv in directs]))
    contacts = [Contact(x) for x in contacts]
    print("There are %i contacts here." % len(contacts))
    #Create a backup object to contain the contacts
    backup = Backup(contacts)

    #Give each contact their direct messages
    for conv in directs:
        person = backup.get_contact_by_name(conv.members[0])
        person.messages += conv.messages

    #Assign a weight of 1 to all messages currently in the backup
    for person in contacts:
        for message in person.messages:
            message.weight = 1

    #Give each contact their group messages
    for person in contacts:
        for conv in groups:
            if person.name in conv.members:
                for message in conv.messages:
                    new_message = copy.deepcopy(message)
                    if new_message.sender == my_name or new_message.sender == person.name:
                        new_message.weight = 1.0 / len(conv.members)
                    else:
                        new_message.weight = 0
                    person.messages.append(new_message)

    #Sort everything
    backup.sort_contacts()

    #Make Markov-ready
    backup.prime_for_markov()

    return backup

class Backup:
    """A collection of contacts and their associated messages"""
    def __init__(self, contacts):
        self.contacts = contacts
        self.start_date = None
        self.end_date = None

    def get_contact_by_name(self, name):
        """Get contact with specified full name"""
        for contact in self.contacts:
            if contact.name == name:
                return contact

    def set_range(self):
        """Assigns values to start_date and end_date according to current contacts.
        Requires contacts to have these set."""
        self.start_date = min([x.start_date for x in self.contacts])
        self.end_date = max([x.start_date for x in self.contacts])

    def sort_contacts(self):
        """Prep all contacts (sort their messages) and sort them, and update date range"""
        #Put all contact messages in correct order
        for contact in self.contacts:
            contact.sort_messages()

        #Sort contacts by score
        self.contacts = sorted(self.contacts, key = lambda k: k.score)
        self.contacts.reverse()

        #Assign the start and end points of the backup
        self.set_range()

    def prime_for_markov(self):
        """Make all contacts make themselves Markov-ready"""
        for contact in self.contacts:
            contact.prime_for_markov()

    def compare_contacts(self, contacts, colors=None):
        for contact in contacts:
            if "days_trend" not in contact.__dict__.keys(): contact.add_charts()
        chart = MultiLineChart([x.days_trend for x in contacts], colors=colors, labels=[x.name for x in contacts], xlabel="Date", ylabel="Chars per day (Moving average)", linewidth=2, title="Comparison of multiple contacts")
        return chart

class Contact:
    """A person with whom you have spoken"""
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.start_date = None
        self.end_date = None
        self.score = 0
        self.initial_distribution = []
        self.chars_per_day = []
        self.chars_per_month = []

    def sort_messages(self):
        """Sort messages by date"""
        #Get messages in right order
        self.messages = sorted(self.messages, key = lambda k: k.time)

        #Update contact start and end dates
        self.start_date = self.messages[0].time
        self.end_date = self.messages[-1].time

        self.score = sum([len(x.text) * x.weight for x in self.messages])

    def prime_for_markov(self):
        """Assign markov words to each message, and create an initial state distribution"""
        for message in self.messages:
            message.set_markov_words()

        self.initial_distribution = [x.markov_words[0] for x in self.messages if len(x.markov_words) > 1 and x.sender == self.name]

    def get_first_word(self):
        """Get the first work in a Markov sentence"""
        if len(self.initial_distribution) != 0:
            return random.choice(self.initial_distribution)

    def get_second_word(self, first_word):
        """Get the second word in a Markov sentence"""
        possibles = []
        for message in [x for x in self.messages if x.text != ""]:
            x = 0
            for word in message.markov_words[:-1]:
                if word == first_word:
                    possibles.append(message.markov_words[x+1])
                x += 1

        return random.choice(possibles)

    def get_next_word(self, current_words):
        """Get the next word in a Markov sentence"""
        #Build up a list of possible next words
        possibles = []

        #Try and get a next word based on current two words
        for message in [x for x in self.messages if x.text != ""]:
            x = 0
            for word in message.markov_words[:-2]:
                if word == current_words[0] and message.markov_words[x+1] == current_words[1]:
                    possibles.append(message.markov_words[x+2])
                x += 1

        #If not possibele, get one based on most recent word only
        if len(possibles) <= 1:
            for message in [x for x in self.messages if x.text != ""]:
                x = 0
                for word in message.markov_words[:-1]:
                    if word == current_words[1]:
                        possibles.append(message.markov_words[x+1])
                    x += 1

        #Return a random possible word
        return random.choice(possibles)

    def generate_message(self):
        """Generate a message using Markov chains, based on exisiting messages"""
        message = []
        message.append(self.get_first_word())
        message.append(self.get_second_word(message[0]))

        while message[-1] != None:
            message.append(self.get_next_word(message[-2:]))

        return " ".join(message[:-1])
    #End Markov methods

    def add_charts(self):
        """Generate the five charts for this contact"""

        #Get days for which there is data
        self.days = [self.start_date.date()]
        while self.days[-1] != self.end_date.date():
            self.days.append(self.days[-1] + datetime.timedelta(days=1))

        #Get day ticks
        if self.end_date - self.start_date <= datetime.timedelta(days=365):
            self.day_ticks = [x for x in self.days if x.day == 1]
            self.day_width = 0.9
        else:
            self.day_ticks = [x for x in self.days if x.month == 1 and x.day == 1]
            self.day_width = 2
        self.day_labels = [str(x.day) + "/" + str(x.month) + "/" + str(x.year)[2:] for x in self.day_ticks]

        #Get months for which there is data
        self.months = [get_month(self.start_date)]
        while self.months[-1] != get_month(self.end_date):
            self.months.append(add_month(self.months[-1]))

        self._add_chars_per_day()
        self._add_chars_per_month()
        self._add_days_trend()
        self._add_months_trend()
        self._add_messages_piechart()
        self.multi_chart = Figure(2, 2, [self.chars_per_day_chart, self.days_trend, self.chars_per_month_chart, self.months_trend])

    def _add_chars_per_day(self):
        self.chars_per_day = [sum([len(m.text) * m.weight for m in self.messages if m.time.date() == day]) for day in self.days]
        self.chars_per_day_chart = BarChart(self.days, self.chars_per_day, color="#FF0000", edgecolor="none", width=self.day_width, xlabel="Date", xticks=self.day_ticks, xticklabels=self.day_labels, ylabel="Characters per day", title="%s - Characters per day over time" % self.name)

    def _add_chars_per_month(self):
        self.chars_per_month = [sum([len(m.text) * m.weight for m in self.messages if get_month(m.time) == month]) for month in self.months]
        self.chars_per_month_chart = BarChart(self.months, self.chars_per_month, color="#00FF00", edgecolor="b", width=25, xlabel="Date", xticks=self.day_ticks, xticklabels=self.day_labels, ylabel="Characters per month", title="%s - Characters per month over time" % self.name)

    def _add_days_trend(self):
        subset = 30
        self.days_MA = get_moving_average(self.chars_per_day, subset)
        self.days_trend = LineChart(self.days[subset-1:], self.days_MA, color="#FF0000", linewidth=2, xlabel="Date", xticks=self.day_ticks, xticklabels=self.day_labels, ylabel="Chars per day (moving average)", title="%s - Characters per day over time (moving average)" % self.name)

    def _add_months_trend(self):
        subset = 3
        self.months_MA = get_moving_average(self.chars_per_month, subset)
        self.months_trend = LineChart(self.months[subset-1:], self.months_MA, color="#00FF00", linewidth=2, xlabel="Date", xticks=self.day_ticks, xticklabels=self.day_labels, ylabel="Chars per month (moving average)", title="%s - Characters per month over time (moving average)" % self.name)

    def _add_messages_piechart(self):
        message_types = list(set([x.message_type for x in self.messages]))
        pie_data = {x:0 for x in message_types}
        for message in self.messages:
            pie_data[message.message_type] += message.weight

        self.messages_pie = PieChart([int(pie_data[x]) for x in message_types], message_types)


    def produce_chatlog(self, include_charts=True, dir=""):
        """Generate a html representation of a contact's messages"""
        #Head
        html = "<html>"
        html += self._produce_head_html()

        #Start body
        html += "<body><h1>%s</h1>" % self.name

        #Charts
        if include_charts:
            self.add_charts()
            html += self._produce_charts_html()

        #Nav bar
        years = self._produce_messages_structure()
        html += self._produce_nav_html(years)

        #Messages
        html += self._produce_messages_html(years)

        html += "</body></html>"
        #Produce HTML file
        f = open(dir + self.name + ".html", "w")
        for char in list(html):
            try:
                f.write(char)
            except:
                f.write("?")
        f.close()


    def _produce_head_html(self):
        head = "<head>"
        head += "<title>%s</title><style>" % self.name

        style = ["body {text-align: center; font-family: Georgia;}",
        "#charts table {margin-left: auto; margin-right: auto;}",
        "#nav {display: inline-block; padding: 30px; border: 2px solid black; border-radius: 15px; margin-bottom: 30px; margin-left: auto; margin-right: auto;}",
        "#nav table {border-spacing: 20px 0px; border-collapse: separate; width: auto;}",
        "#nav td {vertical-align: top; width: 70px;}",
        "#nav a {text-decoration: none;}",
        "#messages {width: 700px; margin-left: auto; margin-right: auto;}"
        "#messages table {width: 700px;}",
        "#messages td {word-break: break-word;}",
        ".time {color: gray; font-size: 70%; margin-left: 10px; margin-bottom: 1px;}",
        "td.name {width: 100px; padding: 0px;}",
        "td.left {text-align: right; padding-right: 4px;}",
        "td.right {text-align: left; padding-left: 4px}",
        "td p {margin-bottom: 20px; margin-top: 0px; padding: 10px; border-radius: 15px; font-family: Helvetica;}",
        "p.Facebook {border: 2px solid #00F; color: white; background-color: #00F}",
        "p.them {color: black; background-color: #DDD}",
        "p.group {border-style: dotted;}",
        "p.fade {opacity: 0.3;}"]
        style = " ".join(style)
        head += style
        head += "</style></head>"

        return head


    def _produce_charts_html(self):
        charts = "<div id=\"charts\"><table>"

        #Add message type pie chart
        charts += "<tr><td>" + self.messages_pie.to_svg() + "</td></tr>"

        #Add days bar chart
        charts = charts + "<tr><td>" + self.chars_per_day_chart.to_svg() + "</td></tr>"

        #Add days trend line
        charts = charts + "<tr><td>" + self.days_trend.to_svg() + "</td></tr>"

        #Add months bar chart
        charts = charts + "<tr><td>" + self.chars_per_month_chart.to_svg() + "</td></tr>"

        #Add months trend line
        charts = charts + "<tr><td>" + self.months_trend.to_svg() + "</td></tr>"

        charts += "</table></div>"
        return charts


    def _produce_messages_structure(self):
        class Day:
            def __init__(self, messages):
                self.value = messages[0].time.day
                self.day_messages = messages

        class Month:
            def __init__(self, messages):
                self.value = messages[0].time.month
                self.month_messages = messages
                self.day_list = set([m.time.day for m in messages])
                self.days = [Day([m for m in messages if m.time.day == x]) for x in self.day_list]

        class Year:
            def __init__(self, messages):
                self.value = messages[0].time.year
                self.year_messages = messages
                self.month_list = set([m.time.month for m in messages])
                self.months = [Month([m for m in messages if m.time.month == x]) for x in self.month_list]

        #What years are there?
        year_list = set([m.time.year for m in self.messages])
        years = [Year([m for m in self.messages if m.time.year == x]) for x in year_list]

        return years


    def _produce_nav_html(self, years):
        nav = "<div id=\"nav\"><table><tr>"

        for year in years:
            nav += "<td><a href=\"#%i\">%i</a><br>" % (year.value, year.value)
            for month in year.months:
                nav += "&nbsp;&nbsp;&nbsp;&nbsp;<a href=\"#%i%i\">%s</a><br>" % (year.value, month.value, calendar.month_name[month.value])
            nav += "</td>"
        nav += "</tr></table></div>"
        return nav

    def _produce_messages_html(self, years):
        messages = "<div id=\"messages\">"
        for year in years:
            messages += "<h2 id=\"%i\">%i</h2>" % (year.value, year.value)
            for month in year.months:
                messages += "<h3 id=\"%i%i\">%s</h3>" % (year.value, month.value, calendar.month_name[month.value])
                for day in month.days:
                    messages += "<h4>%i %s</h4>" % (day.value, calendar.month_name[month.value])
                    messages += "<table><tr><td class='name'></td><td style='width: 200px;'></td><td></td><td style='width: 200px;'></td><td class='name'></td></tr>"
                    for message in day.day_messages:
                        messages += message.to_tr()
                    messages += "</table>"

        return messages




class Message:
    """A generic message, of any kind"""
    def __init__(self):
        self.markov_words = []

    def set_markov_words(self):
        """Take the message and break into words for Markov purposes"""
        #This will do for now
        self.markov_words = self.text.split(" ") + [None]
        self.markov_words = [x for x in self.markov_words if x != ""]

    def to_tr(self):
        """Produce html for this message to be slotted into a chatlog"""
        html = "<tr>"
        if self.from_me:
            #Make first two cells empty
            html += "<td></td><td></td>"
        else:
            #Put name in first cell
            html += "<td class='name left'>" + self.sender.split(" ")[0] + "</td>"
        #Message cell, spanning 2 normal cells
        html += "<td colspan='2'>"
        html += "<div class='time'>" + str(self.time.strftime("%Y-%m-%d %H:%M:%S")) + "</div>"
        html += "<p class='message "
        html += self.message_type
        if not self.from_me:
            html += " them"
        if self.weight < 1 and not self.from_me:
            html += " group"
        if not self.from_me and self.weight == 0:
            html += " fade"
        html += "'>"
        if self.text is None or self.text == "":
            html += "[IMAGE]"
        else:
            html += self.text
        html += "</p></td>"
        if not self.from_me:
            html += "<td></td><td></td></tr>"
        else:
            html += "<td class='name right'>" + self.sender.split(" ")[0] + "</td>"
        html += "</tr>"
        return html





def get_month(d):
    """Take a datetime and return a datetime with only year and month info"""
    return datetime.datetime(d.year, d.month, 1)

def add_month(d):
    """Add one calendar month to any datetime"""
    if d.month == 12:
        return datetime.datetime(d.year+1, 1, 1)
    else:
        return datetime.datetime(d.year, d.month+1, 1)

def get_moving_average(data, subset):
    """Takes a sequence of numbers and returns moving average data. The returned sequence will be (subset - 1) shorter than the incoming sequence"""
    moving_average = []
    index = subset - 1
    for value in data[index:]:
        moving_average.append(sum(data[index-(subset-1):index+1])/float(subset))
        index += 1

    return moving_average
