# -*- coding: utf-8 -*-

import slackweb
import os


def send(message):
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(text=message)