from pymongo.errors import BulkWriteError

from App.ext import MovieCollection, personCollection


def getData(doubanId):
    data = MovieCollection.find({'doubanId': doubanId}).to_list(None)
    if len(data) == 0:
        return None
    else:
        return data[0]


def insertOneData(data):
    MovieCollection.insert_one(data)


def getPersonData(doubanId):
    data = list(personCollection.find({'id': doubanId}))
    if len(data) == 0:
        return None
    else:
        return data[0]


def querySubjectCredits(doubanId):
    data = list(MovieCollection.find({'id': doubanId}))
    if len(data) == 0:
        return None
    else:
        if "subject_credits" in data[0] and data[0]['subject_credits'] is not None:
            return data[0]['subject_credits']
        else:
            return None


def querySubject(doubanId):
    data = list(MovieCollection.find({'id': doubanId}))
    if len(data) == 0:
        return None
    else:
        if "subjectArr" in data[0] and data[0]['subjectArr'] is not None:
            return data[0]['subjectArr']
        else:
            return None


def updateSubject(doubanId, items):
    res = MovieCollection.update_one({"id": doubanId}, {"$set": {"subjectArr": items}})


def updateSubjectCredits(doubanId, items):
    res = MovieCollection.update_one({"id": doubanId}, {"$set": {"subject_credits": items}})


def insertSearchData(data):
    print(data)
    rData = []
    for dataItem in data:
        if dataItem['target_type'] != "movie" and dataItem['target_type'] != "tv":
            continue
        dataItem['target'].pop('null_rating_reason')
        dataItem['target'].pop('has_linewatch')
        if "is_badge_chart" in dataItem['target']:
            dataItem['target'].pop('is_badge_chart')
        if "is_follow" in dataItem['target']:
            dataItem['target'].pop('is_follow')
        if "uri" in dataItem['target'].keys():
            dataItem['target'].pop('uri')
        if "controversy_reason" in dataItem['target'].keys():
            dataItem['target'].pop('controversy_reason')
        dataItem.pop('layout')
        dataItem.update(dataItem.pop('target'))
        rData.append(dataItem)
    if len(rData) > 0:
        insertData(rData)


def insertData(data):
    try:
        MovieCollection.insert_many(data, ordered=False)
    except BulkWriteError:
        pass


def insertPersonData(data):
    try:
        personCollection.insert_one(data)
    except BulkWriteError:
        pass


def querySearchData(q, count):
    pipeline = [{
        "$match": {
            'title': {"$regex": q}
        }
    }, {
        "$sort": {
            "title_equal": -1,
        }
    }, {
        "$limit": count
    }
    ]

    result = MovieCollection.aggregate(pipeline)
    return list(result)
