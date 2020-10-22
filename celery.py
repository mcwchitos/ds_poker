from celery import Celery
import operator
from Card import *

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def sortCel(hand):
    result = []
    return result.append(sorted(hand, key=operator.attrgetter('VALUE')))

@app.task
def crtEvals(sortedHands, handEvals=None):
    result = []
    for srtdHnd in sortedHands:
        handEvals.append(HandEvaluator(srtdHnd))
    return result

