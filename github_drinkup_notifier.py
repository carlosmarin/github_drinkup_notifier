import feedparser
import ConfigParser
import argparse
import smtplib
import os


def notify(atom_entry, city):

    email_from = config.get('email', 'from')
    email_to = config.get('email', 'to')
    email_subject = config.get('email', 'subject')

    header = 'To:' + email_to + '\n' + 'From: ' + email_from + '\n' + \
             'Subject: ' + email_subject + ' ' + city + ' \n'

    body = "%s\n%s" % (atom_entry.title, atom_entry.link)

    msg = header + '\n ' + body + ' \n\n'

    server = smtplib.SMTP(config.get('smtp', 'server'), int(config.get('smtp', 'port')))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config.get('smtp', 'username'), config.get('smtp', 'password'))
    server.sendmail(email_from, email_to, msg)
    server.close()


def check_feed(args):
    """
    Usage sample:
    github_drinkup_notifier.py --feed https://github.com/blog/drinkup.atom --city Austin --date 2013-11-08 --numdays 5
    """

    last_entry_date_published = config.get('notify', 'last_entry_date_published')
    last_entry_id = config.get('notify', 'last_entry_id')
    print "Last entry: ", last_entry_date_published, last_entry_id

    city = args['city'].upper()
    feed = feedparser.parse(args['atom_feed_uri'])

    new_meetup_found = False
    for entry in feed.entries:
        if city in entry.title.upper() and entry.published > last_entry_date_published:
            if last_entry_id != entry.id:
                new_meetup_found = True
                print "Found matching meetup published %s" % (entry.published)
                notify(entry, args['city'])
                config.set('notify', 'last_entry_date_published', entry.published)
                config.set('notify', 'last_entry_id', entry.id)
                with open(config_file, 'wb') as file:
                    config.write(file)

    if not new_meetup_found:
        print "No new matching meetup found up to %s since %s" % (entry.published, last_entry_date_published)


if __name__ == "__main__":
    config_file = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    parser = argparse.ArgumentParser(description="Notify on a city name match in title of an Atom feed's entry.")

    parser.add_argument('-u', '--atom_feed_uri', help='Full URI of the Atom Feed', required=True)
    parser.add_argument('-c', '--city', help='City name (looked for in title)', required=True)

    args = vars(parser.parse_args())

    check_feed(args)
