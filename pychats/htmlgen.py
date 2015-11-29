import calendar

class Day:
    def __init__(self, messages):
        self.value = messages[0].datetime.day
        self.day_messages = messages

class Month:
    def __init__(self, messages):
        self.value = messages[0].datetime.month
        self.month_messages = messages
        self.day_list = set([m.datetime.day for m in messages])
        self.days = [Day([m for m in messages if m.datetime.day == x])
         for x in self.day_list]

class Year:
    def __init__(self, messages):
        self.value = messages[0].datetime.year
        self.year_messages = messages
        self.month_list = set([m.datetime.month for m in messages])
        self.months = [Month([m for m in messages if m.datetime.month == x])
         for x in self.month_list]


class HtmlGeneratingContact:
    """A contact capable of producing a html file representation of itself"""

    def produce_html_chatlog(self, dir=""):
        """Generate a html representation of a contact's messages"""
        #Head
        html = "<html>"
        html += self._produce_head_html()


        #Start body
        html += "<body><h1>%s</h1>" % self.name


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
        "td p {margin-bottom: 20px; margin-top: 0px; padding: 10px; border-radius: 15px; font-family: Helvetica;}"]

        for message_type in set([type(m) for m in self.messages]):
            style.append("p.%s {border: 2px solid #00F; color: white; background-color: %s}" %
             (message_type.name, message_type.color))

        style += ["p.them {color: black; background-color: #DDD}",
        "p.group {border-style: dotted;}",
        "p.fade {opacity: 0.3;}"]
        style = "\n".join(style)
        head += style
        head += "</style></head>"

        return head



    def _produce_messages_structure(self):

        #What years are there?
        year_list = set([m.datetime.year for m in self.messages])
        years = [Year([m for m in self.messages if m.datetime.year == x]) for x in year_list]

        return years


    def _produce_nav_html(self, years):
        nav = "<div id=\"nav\"><table><tr>"

        for year in years:
            nav += "<td><a href=\"#%i\">%i</a><br>" % (year.value, year.value)
            for month in year.months:
                nav += "&nbsp;&nbsp;&nbsp;&nbsp;<a href=\"#%i%i\">%s</a><br>" % (
                 year.value, month.value, calendar.month_name[month.value])
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
                        messages += message.generate_html_representation(self.log.my_name)
                    messages += "</table>"

        return messages



class HtmlGeneratingMessage:

    def generate_html_representation(self, my_name):
        """Produce html for this message to be slotted into a chatlog"""
        sender = ""
        if self.from_me:
            sender = my_name
        elif self.from_them:
            sender = self.contact.name
        else:
            sender = self.sender_name

        html = "<tr>"
        if self.from_me:
            #Make first two cells empty
            html += "<td></td><td></td>"
        else:
            #Put name in first cell
            html += "<td class='name left'>" + sender.split(" ")[0] + "</td>"
        #Message cell, spanning 2 normal cells
        html += "<td colspan='2'>"
        html += "<div class='time'>" + self.datetime.strftime("%Y-%m-%d %H:%M:%S") + "</div>"
        html += "<p class='message "
        html += self.name
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
            html += "<td class='name right'>" + sender.split(" ")[0] + "</td>"
        html += "</tr>"
        return html
