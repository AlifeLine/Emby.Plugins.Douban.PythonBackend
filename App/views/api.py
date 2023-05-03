import datetime
import decimal
import json

from bson import ObjectId
from flask import Blueprint, request, jsonify

from App.ext import douBanClient, redis_client
from App.utiles.mongoUtiles import insertSearchData, querySearchData, insertPersonData, getPersonData, \
    querySubjectCredits, updateSubjectCredits, querySubject, updateSubject

# from App.ext import Alipay, piPay

apiBlue = Blueprint('api_blue', __name__, url_prefix='/api/v2')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


@apiBlue.route('/search/subjects')
async def search():
    data = request.args
    q = data.get('q')
    redisKey = f"search/subjects:{q}"
    rep = redis_client.get(redisKey)
    if rep is None:
        count = int(data.get('count'))
        rep = querySearchData(q, count)
        length = len(rep)
        if rep is None or length == 0:
            rep = (await douBanClient.search(q, count))['items']
            if len(rep) > 0:
                insertSearchData(rep)
        redis_client.set(redisKey, json.dumps(rep, cls=MyEncoder), ex=60 * 60 * 24 * 15)
    else:
        rep = json.loads(rep)
    return jsonify({"count": len(rep), "items": rep})


@apiBlue.route('/elessar/subject/<doubanId>')
async def getPersonInfo(doubanId):
    redisKey = f"elessar/subject:{doubanId}:credits"
    rep = redis_client.get(redisKey)
    if rep is None:
        rep = getPersonData(doubanId)
        if rep is None:
            rep = (await douBanClient.getPersonInfo(doubanId))
            if "greeting_action" in rep:
                del rep['greeting_action']
            if "is_followed" in rep:
                del rep['is_followed']
            if "greeting_beanshop" in rep:
                del rep['greeting_beanshop']
            if "ugc_tabs" in rep:
                del rep['ugc_tabs']
            if "header_bg_color" in rep:
                del rep['header_bg_color']
            if "color_scheme" in rep:
                del rep['color_scheme']
            if "received_greetings_count" in rep:
                del rep['received_greetings_count']
            if "followed_count" in rep:
                del rep['followed_count']
            if "sharing_url" in rep:
                del rep['sharing_url']
            if "modules" in rep:
                del rep['modules']
            if "created_at" in rep:
                del rep['created_at']
            if "uri" in rep:
                del rep['uri']
            insertPersonData(rep)
            del rep["_id"]
            redis_client.set(redisKey, json.dumps(rep), ex=60 * 60 * 24)
        return jsonify(rep)
    else:
        return jsonify(json.loads(rep))


@apiBlue.route('/<mediaType>/<doubanId>/credits')
async def getSubjectCredits(doubanId, mediaType):
    redisKey = f"{mediaType}:{doubanId}:credits"
    rep = redis_client.get(redisKey)
    if rep is None:
        rep = querySubjectCredits(doubanId)
        if rep is None:
            rep = await douBanClient.getSubjectCredits(doubanId, mediaType)
            items = rep['items']
            for item in items:
                del item['user']
                del item['sharing_url']
            updateSubjectCredits(doubanId, items)
            redis_client.set(redisKey, json.dumps(items), ex=60 * 60 * 24)
            return jsonify({"celebrities": items})
        redis_client.set(redisKey, json.dumps(rep), ex=60 * 60 * 24)
        return jsonify({"celebrities": rep})
    else:
        return jsonify({"celebrities": json.loads(rep)})


@apiBlue.route('/<mediaType>/<doubanId>')
async def getSubject(doubanId, mediaType):
    redisKey = f"{mediaType}:{doubanId}:subject"
    rep = redis_client.get(redisKey)
    if rep is None:
        rep = querySubject(doubanId)
        if rep is None:
            rep = await douBanClient.getSubject(doubanId, mediaType)
            needDel = ['interest_cmt_earlier_tip_desc', 'is_restrictive', 'aka', 'video', 'pre_release_desc',
                       'null_rating_reason', 'is_show',
                       'episodes_info', 'pre_playable_date', 'uri', 'release_date', 'rate_info',
                       'wechat_timeline_share', 'subject_collections',
                       'sharing_url', 'honor_infos', 'ticket_vendor_icons', 'is_douban_intro', 'header_bg_color',
                       'restrictive_icon_url', 'lineticket_url',
                       'durations', 'controversy_reason', 'last_episode_number', 'interest_control_info',
                       'body_bg_color', 'vendor_count', 'head_info', 'album_no_interact', 'ticket_price_info',
                       'webisode_count',
                       'can_rate', 'card_subtitle', 'forum_info', 'webisode', 'gallery_topic_count', 'languages',
                       'review_count', 'variable_modules', 'interest_cmt_earlier_tip_title',
                       'has_linewatch', 'vendors', 'ticket_promo_text', 'forum_topic_count', 'webview_info',
                       'is_released', 'comment_count', 'interest',
                       'episodes_count', 'color_scheme', 'linewatches', 'info_url', 'vendor_icons', 'tags']
            for k in needDel:
                if k in rep.keys():
                    del rep[k]
            updateSubject(doubanId, rep)
        return jsonify(rep)
    else:
        return jsonify(json.loads(rep))
