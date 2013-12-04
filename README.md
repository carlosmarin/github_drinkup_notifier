# GitHub Drinkup Notifier
=========================

Script to send me an e-mail when a new meetup is in town.

Usage:
`github_drinkup_notifier.py [-h] -u ATOM_FEED_URI -c CITY`

Sample crontab entry:
`0 11 * * * python /home/carlos.marin/github_drinkup_notifier/github_drinkup_notifier.py -u https://github.com/blog/drinkup.atom -c Austin`