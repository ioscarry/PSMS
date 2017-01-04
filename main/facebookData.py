# -*- coding: utf-8 -*-
from __future__ import division
from main.has_permission import *
from flask import Blueprint, request
from main import db
from models import Offer, Token, Advertisers, TimePrice, Country
import json
import os
import datetime, time
import requests
from collections import Counter

facebookDate = Blueprint('facebookDate', __name__)

@facebookDate.route('/api/dashboard')
def dashboard():
    yesterday = (datetime.datetime.now()-datetime.timedelta(hours=24)).strftime("%Y-%m-%d")
    yesterday = "2016-08-27"
    token = Token.query.filter().first()
    accessToken = token.accessToken
    time_range = "{'since': "+"'"+str(yesterday)+"'"+", 'until': "+"'"+str(yesterday)+"'"+"}"
    url = "https://graph.facebook.com/v2.8/act_1004988846265857/insights"
    filed_lists = ["impressions","spend","clicks","cpc","ctr","actions"]
    result = []
    for i in filed_lists:
        params_impressions = {
            "access_token": accessToken,
            "level": "account",
            "fields": [i],
            "time_range": str(time_range)
        }
        result_impressions = requests.get(url=url, params=params_impressions)
        data_impressions = result_impressions.json()["data"]
        value = data_impressions[0].get(i)
        if i == "actions":
            i = "conversions"
            for action in data_impressions[0].get("actions"):
                if "offsite_conversion" in action["action_type"]:
                    conversions = action["value"]
                elif "link_click" in action["action_type"]:
                    conversions = action["value"]
                else:
                    conversions = 0
            value = conversions

        data = {
            i:value
        }
        result += [data]

    clicks = int(result[2].get("clicks"))
    if int(clicks) != int(0):
        cvr = '%0.2f'%(int(conversions) / int(clicks) * 100 )
    else:
        cvr = 0
    data_cvr = {
        "cvr": cvr
    }
    result += [data_cvr]
    if int(conversions) != 0:
        cpi = '%0.2f'%(float(result[1].get("spend"))/float(conversions))
    else:
        cpi = 0
    data_cpi = {
        "cpi": cpi
    }
    result += [data_cpi]
    revenue = float(conversions)*1.5
    data_revenue = {
        "revenue": str(revenue)
    }
    result += [data_revenue]
    profit = float(revenue) - float(result[1].get("spend"))
    data_profit = {
        "profit": str(profit)
    }
    result += [data_profit]
    response = {
        "code": 200,
        "message": "success",
        "result": result
    }
    return json.dumps(response)

@facebookDate.route('/api/report', methods=["POST","GET"])
def faceReport():
    if request.method == "POST":
        data = request.get_json(force=True)
        offerId = data["offer_id"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        dimension = data["dimension"]
        offer = Offer.query.filter_by(id=offerId).first()
        price_default = offer.price
        advertiser = Advertisers.query.filter_by(offer_id=int(offerId),type="facebook").first()
        accessToken = advertiser.token
        accessToken = "EAAHgEYXO0BABAO8dhDyFvLiFnIuBpaYDYp6bcSRtkJQg5cpFy7BCJiL9xyQrRkVpheDhP4EGZCgKzBqKeGh9y0Fdd7PPZBzHnT0Q7hvyEWxTpKgJXyB3EkZBZA01OC6wx7f9NdX9popYJksnTNT2ZCpiFHX8gqIncF9vvGGEQtAZDZD"
        advertise_groups = advertiser.advertise_groups.split(",")
        advertise_groups = ["6050664418448","6050664365648","6050357178448"]
        count_impressions = 0
        count_cost = 0
        count_clicks = 0
        count_conversions = 0
        count_ctr = 0
        count_cpc = 0
        if "geo" in dimension:
            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/"+str(i)+"/insights"
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["impressions"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_impressions += int(j["impressions"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["spend"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_cost += float(j["spend"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["clicks"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_clicks += float(j["clicks"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["actions"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    actions = j.get("actions",[])
                    for action in actions:
                        if "offsite_conversion" in action["action_type"]:
                            conversions = action["value"]
                            count_conversions += int(conversions)
                        elif "link_click" in action["action_type"]:
                            conversions = action["value"]
                            count_conversions += int(conversions)
                        else:
                            conversions = 0
                            count_conversions += conversions
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["ctr"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_ctr += float(j["ctr"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["cpc"],
                    "breakdowns": ["country"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_cpc += float(j["cpc"])
            count_cvr = '%0.2f' % (count_conversions / count_clicks * 100) if count_clicks != 0 else 0
            count_cpi = '%0.2f'% (count_cost / count_conversions) if count_conversions != 0 else 0
            revenue = count_conversions * 1.5
            profit = revenue - count_cost
            data_geo = {
                "count_impressions": str(count_impressions),
                "count_cost": '%0.2f'%(count_cost),
                "count_clicks": str(count_clicks),
                "count_conversions": str(count_conversions),
                "count_ctr": '%0.2f'%(float(count_ctr)),
                "count_cvr": count_cvr,
                "count_cpc": '%0.2f'% (float(count_cpc)),
                "count_cpi": count_cpi,
                "revenue": '%0.2f'%(revenue),
                "profit": '%0.2f'%(profit)
            }
        elif "date" in dimension and len(dimension)==1:
            #按着day维度的总数据
            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/"+str(i)+"/insights"
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["impressions"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_impressions += int(j["impressions"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["spend"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_cost += float(j["spend"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["clicks"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_clicks += float(j["clicks"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["actions"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    actions = j.get("actions",[])
                    for action in actions:
                        if "offsite_conversion" in action["action_type"]:
                            conversions = action["value"]
                            count_conversions += int(conversions)
                        elif "link_click" in action["action_type"]:
                            conversions = action["value"]
                            count_conversions += int(conversions)
                        else:
                            conversions = 0
                            count_conversions += conversions
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["ctr"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_ctr += float(j["ctr"])

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["cpc"],
                    "time_range": "{'since': " + "'" + str(start_date) + "'" + ", 'until': " + "'" + str(end_date) + "'" + "}"
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    count_cpc += float(j["cpc"])
            count_cvr = '%0.2f' % (count_conversions / count_clicks * 100) if count_clicks != 0 else 0
            count_cpi = '%0.2f'% (count_cost / count_conversions) if count_conversions != 0 else 0
            revenue = count_conversions * 1.5
            profit = revenue - count_cost
            data_geo = {
                "count_impressions": str(count_impressions),
                "count_cost": '%0.2f'%(count_cost),
                "count_clicks": str(count_clicks),
                "count_conversions": str(count_conversions),
                "count_ctr": '%0.2f'%(count_ctr),
                "count_cvr": count_cvr,
                "count_cpc": '%0.2f'%(count_cpc),
                "count_cpi": count_cpi,
                "revenue": '%0.2f'%(revenue),
                "profit": '%0.2f'%(profit)
            }


        all_date = ["2016-08-26","2016-08-27","2016-08-28","2016-08-29","2016-08-30","2016-08-31","2016-09-01","2016-09-02","2016-09-03","2016-09-04","2016-09-05","2016-09-06","2016-09-07","2016-09-08","2016-09-09","2016-09-10"]
        time_ranges = []
        for day in all_date[::-1]:
            time_ranges.append("{'since': " + "'" + str(day) + "'" + ", 'until': " + "'" + str(day) + "'" + "}")
        if "geo" in dimension:
            impressions_list = []
            cost_list = []
            clicks_list = []
            conversions_list = []
            ctr_list = []
            cpc_list = []
            cvr_list = []
            cpi_list = []
            revenue_list = []
            profit_list = []
            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/"+str(i)+"/insights"
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["impressions"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    impressions_list.append(j)

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["spend"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    cost_list.append(j)

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["clicks"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    clicks_list.append(j)

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["actions"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    actions = j.get("actions",[])
                    for action in actions:
                        if "offsite_conversion" in action["action_type"]:
                            conversions = int(action["value"])
                        elif "link_click" in action["action_type"]:
                            conversions = int(action["value"])
                        else:
                            conversions = 0
                        conver_data = {
                            "country": j["country"],
                            "date_stop": j["date_stop"],
                            "date_start": j["date_start"],
                            "conversions": conversions
                        }
                        conversions_list += [conver_data]
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["ctr"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    ctr_list.append(j)

                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["cpc"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    cpc_list.append(j)

            if len(conversions_list) >= len(clicks_list):
                len_difference = len(conversions_list) - len(clicks_list)
                for i in range(len_difference):
                    clicks_list += [
                        {
                            "country": conversions_list[-1].get("country"),
                            "clicks": 0,
                            "date_start": conversions_list[-1].get("date_start"),
                            "date_stop": conversions_list[-1].get("date_stop")
                        }
                    ]
            else:
                len_difference = len(clicks_list) - len(conversions_list)
                for i in range(len_difference):
                    conversions_list += [
                        {
                            "country": clicks_list[-1].get("country"),
                            "conversions": 0,
                            "date_start": clicks_list[-1].get("date_start"),
                            "date_stop": clicks_list[-1].get("date_stop")
                        }
                    ]
            for l in range(len(conversions_list)):
                if conversions_list[l].get("date_start") == clicks_list[l].get("date_start") and conversions_list[l].get("country") == clicks_list:
                    cvr = '%0.2f' % (int(conversions_list[l].get("conversions")) / int(clicks_list[l].get("clicks")) * 100) if int(clicks_list[l].get("clicks")) != 0 else 0
                    cvr_list += [
                        {
                            "country": conversions_list[l].get("country"),
                            "cvr": cvr,
                            "date_start": conversions_list[l].get("date_start"),
                            "date_stop": conversions_list[l].get("date_stop")
                        }
                    ]
                else:
                    cvr_list += [
                        {
                            "country": conversions_list[l].get("country"),
                            "cvr": 0,
                            "date_start": conversions_list[l].get("date_start"),
                            "date_stop": conversions_list[l].get("date_stop")
                        }
                    ]
            if len(conversions_list) > len(cost_list):
                len_difference = len(conversions_list) - len(cost_list)
                for i in range(len_difference):
                    cost_list += [
                        {
                            "country": conversions_list[-1].get("country"),
                            "spend": 0,
                            "date_start": conversions_list[-1].get("date_start"),
                            "date_stop": conversions_list[-1].get("date_stop")
                        }
                    ]
            else:
                len_difference = len(cost_list) - len(conversions_list)
                for i in range(len_difference):
                    conversions_list += [
                        {
                            "country": cost_list[-1].get("country"),
                            "conversions": 0,
                            "date_start": cost_list[-1].get("date_start"),
                            "date_stop": cost_list[-1].get("date_stop")
                        }
                    ]

            for l in range(len(conversions_list)):
                if conversions_list[l].get("date_start") == cost_list[l].get("date_start") and conversions_list[l].get("country") == cost_list[l].get("country"):
                    cpi = '%0.2f' % (float(cost_list[l].get("spend")) / float(conversions_list[l].get("conversions")) * 100) if conversions_list[l].get("conversions") != 0 else 0
                    cpi_dict = {
                        "country": conversions_list[l].get("country"),
                        "cpi": cpi,
                        "date_start": conversions_list[l].get("date_start"),
                        "date_stop": conversions_list[l].get("date_stop")
                    }

                else:
                    cpi_dict = {
                        "country": conversions_list[l].get("country"),
                        "cpi": 0,
                        "date_start": conversions_list[l].get("date_start"),
                        "date_stop": conversions_list[l].get("date_stop")
                    }
                cpi_list += [cpi_dict]

            for r in range(len(conversions_list)):
                country = conversions_list[r].get("country")
                date = conversions_list[r].get("date_start")
                conversion = float(conversions_list[r].get("conversions"))
                countries = Country.query.filter_by(shorthand=country).first()
                country_id = countries.id
                time_price = TimePrice.query.filter_by(country_id=country_id,date=date).first()
                if time_price:
                    price = time_price.price
                else:
                    price = price_default
                revenue_list += [
                    {
                        "country": country,
                        "revenue": float(conversion*price),
                        "date_start": date,
                        "date_stop": date
                    }
                ]

            # profit = revenue - count_cost
            for p in range(len(revenue_list)):
                if revenue_list[p].get("country") == cost_list[p].get("country") and revenue_list[p].get("date_start") == cost_list[p].get("date_start"):
                    profit = {
                        "country": revenue_list[p].get("country"),
                        "profit": float(revenue_list[p].get("revenue"))-float(cost_list[p].get("spend")),
                        "date_start": revenue_list[p].get("date_start"),
                        "date_stop": revenue_list[p].get("date_stop")
                    }

                else:
                    profit = {
                        "country": revenue_list[p].get("country"),
                        "profit": 0,
                        "date_start": revenue_list[p].get("date_start"),
                        "date_stop": revenue_list[p].get("date_stop")
                    }
                profit_list += [profit]

            data_geo_table = {
                "impressions_list": impressions_list,
                "cost_list": cost_list,
                "clicks_list": clicks_list,
                "conversions_list":conversions_list,
                "ctr_list": ctr_list,
                "cvr_list": cvr_list,
                "cpc_list": cpc_list,
                "cpi_list": cpi_list,
                "revenue_list": revenue_list,
                "profit_list": profit_list,
                "head": ["Date","Geo","Revenue","Profit","Cost","Impressions","Clicks","Conversions","CTR","CVR","CPC","CPA"]
            }
            data_date_table = {}

        elif "date" in dimension:
            data_geo_table = {}
            impressions_count = []
            costs_count = []
            clicks_count = []
            ctr_count = []
            cpc_count = []
            conversions_list = []
            revenue_list = []
            profit_list = []
            conversions_count_list = []

            for i in advertise_groups:
                url = "https://graph.facebook.com/v2.8/" + str(i) + "/insights"
                params = {
                    "access_token": accessToken,
                    "level": "adset",
                    "fields": ["actions"],
                    "breakdowns": ["country"],
                    "time_ranges": str(time_ranges)
                }
                result = requests.get(url=url, params=params)
                data = result.json()["data"]
                for j in data:
                    actions = j.get("actions", [])
                    for action in actions:
                        if "offsite_conversion" in action["action_type"]:
                            conversions = int(action["value"])
                        else:
                            if "link_click" in action["action_type"]:
                                conversions = int(action["value"])
                        conver_data = {
                            "country": j["country"],
                            "date_stop": j["date_stop"],
                            "date_start": j["date_start"],
                            "conversions": conversions
                        }
                        conversions_list += [conver_data]
                for r in range(len(conversions_list)):
                    country = conversions_list[r].get("country")
                    date = conversions_list[r].get("date_start")
                    conversion = float(conversions_list[r].get("conversions"))
                    countries = Country.query.filter_by(shorthand=country).first()
                    country_id = countries.id
                    time_price = TimePrice.query.filter_by(country_id=country_id, date=date).first()
                    if time_price:
                        price = time_price.price
                    else:
                        price = price_default
                    revenue_list += [
                        {
                            "country": country,
                            "revenue": float(conversion * price),
                            "date_start": date,
                            "date_stop": date
                        }
                    ]

                revenue_new_list = []
                for i in revenue_list:
                    if i not in revenue_new_list:
                        revenue_new_list.append(i)
                    else:
                        pass
                for j in range(len(revenue_new_list)):
                    if j+1 < len(revenue_new_list) and revenue_new_list[j+1].get("date_start") == revenue_new_list[j].get("date_start"):
                        revenue_new_list[j+1] = {
                            "revenue": '%0.2f'%(float(revenue_new_list[j].get("revenue"))+revenue_new_list[j+1].get("revenue")),
                            "date_start": revenue_new_list[j].get("date_start")
                        }
                        revenue_new_list[j] = revenue_new_list[j+1]
                        revenue_new_list.remove(revenue_new_list[j])

                    else:
                        pass

                dx = dict()
                for i in revenue_new_list:
                    dx.setdefault(i["date_start"], []).append(i["revenue"])

                for k in dx:
                    dx[k] = sum(float(i) for i in dx[k])

                revenue_new_list = [{"date_start": k, "revenue": str(v)} for k, v in dx.items()][::-1]

            for t in time_ranges:
                for i in advertise_groups:
                    url = "https://graph.facebook.com/v2.8/" + str(i) + "/insights"
                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["impressions"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data != []:
                        impressions_count.append(data)
            #
                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["spend"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url,params=params)
                    data = result.json()
                    if data != []:
                        costs_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["clicks"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data != []:
                        clicks_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["ctr"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data != []:
                        ctr_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["cpc"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()
                    if data != []:
                        cpc_count.append(data)

                    params = {
                        "access_token": accessToken,
                        "level": "adset",
                        "fields": ["actions"],
                        "time_range": str(t)
                    }
                    result = requests.get(url=url, params=params)
                    data = result.json()["data"]

                    if data != []:
                        if data[0]["actions"] != []:
                            for action in data[0]["actions"]:
                                if "offsite_conversion" in action["action_type"]:
                                    conversions = action["value"]
                                    date_start = data[0]["date_start"]
                                    con_data = {
                                        "conversions": int(conversions),
                                        "date_start": date_start
                                    }
                                else:
                                    if "link_click" in action["action_type"]:
                                        conversions = action["value"]
                                        date_start =data[0]["date_start"]
                                        con_data = {
                                            "conversions": int(conversions),
                                            "date_start": date_start
                                        }
                                conversions_count_list += [con_data]
            dx = dict()
            for i in conversions_count_list:
                dx.setdefault(i["date_start"], []).append(i["conversions"])
            for k in dx:
                dx[k] = sum(float(i) for i in dx[k])
            conversions_count_list = [{"date_start": k, "conversions": str(v)} for k, v in dx.items()]
            conversions_count_list = sorted(conversions_count_list, key=lambda k: k['date_start'])[::-1]

            impressions_count_list = []
            costs_count_list = []
            clicks_count_list = []
            cpc_count_list = []
            ctr_count_list = []
            cvr_count_list = []
            cpi_count_list = []
            for t_impression in impressions_count:
                if t_impression["data"] != []:
                    impression_data = {
                        "impressions":t_impression["data"][0].get("impressions"),
                        "date_start": t_impression["data"][0].get("date_start")
                    }
                    impressions_count_list+=[impression_data]
            dx = dict()
            for i in impressions_count_list:
                dx.setdefault(i["date_start"], []).append(i["impressions"])
            for k in dx:
                dx[k] = sum(float(i) for i in dx[k])
            impressions_count_list = [{"date_start": k, "impressions": str(v)} for k, v in dx.items()]
            impressions_count_list = sorted(impressions_count_list, key=lambda k: k['date_start'])[::-1]

            for t_cost in costs_count:
                if t_cost["data"] != []:
                    costs_data = {
                        "spend": float(t_cost["data"][0].get("spend")),
                        "date_start": t_cost["data"][0].get("date_start")
                    }
                    costs_count_list += [costs_data]
            dx = dict()
            for i in costs_count_list:
                dx.setdefault(i["date_start"], []).append(i["spend"])
            for k in dx:
                dx[k] = sum(float(i) for i in dx[k])
            costs_count_list = [{"date_start": k, "spend": str(v)} for k, v in dx.items()]
            costs_count_list = sorted(costs_count_list, key=lambda k: k['date_start'])[::-1]

            for t_clicks in clicks_count:
                if t_clicks["data"] != []:
                    clicks_data = {
                        "clicks": int(t_clicks["data"][0].get("clicks")),
                        "date_start": t_clicks["data"][0].get("date_start")
                    }
                    clicks_count_list += [clicks_data]
            dx = dict()
            for i in clicks_count_list:
                dx.setdefault(i["date_start"], []).append(i["clicks"])
            for k in dx:
                dx[k] = sum(float(i) for i in dx[k])
            clicks_count_list = [{"date_start": k, "clicks": str(v)} for k, v in dx.items()]
            clicks_count_list = sorted(clicks_count_list, key=lambda k: k['date_start'])[::-1]

            for t_cpc in cpc_count:
                if t_cpc["data"] != []:
                    cpc_data = {
                        "cpc": '%0.2f'%(float(t_cpc["data"][0].get("cpc"))),
                        "date_start": t_cpc["data"][0].get("date_start")
                    }
                    cpc_count_list += [cpc_data]
            dx = dict()
            for i in cpc_count_list:
                dx.setdefault(i["date_start"], []).append(i["cpc"])
            for k in dx:
                dx[k] = sum(float(i) for i in dx[k])
            cpc_count_list = [{"date_start": k, "cpc": str(v)} for k, v in dx.items()]
            cpc_count_list = sorted(cpc_count_list, key=lambda k: k['date_start'])[::-1]

            for t_ctr in ctr_count:
                if t_ctr["data"] != []:
                    ctr_data = {
                        "ctr": t_ctr["data"][0].get("ctr"),
                        "date_start": t_ctr["data"][0].get("date_start")
                    }
                    ctr_count_list += [ctr_data]
            dx = dict()
            for i in ctr_count_list:
                dx.setdefault(i["date_start"], []).append(i["ctr"])
            for k in dx:
                dx[k] = sum(float(i) for i in dx[k])
            ctr_count_list = [{"date_start": k, "ctr": str(v)} for k, v in dx.items()]
            ctr_count_list = sorted(ctr_count_list, key=lambda k: k['date_start'])[::-1]

            for l in range(len(conversions_count_list)):
                if conversions_count_list[l].get("date_start") == clicks_count_list[l].get("date_start"):
                    cvr = '%0.2f' % (float(conversions_count_list[l].get("conversions")) / float(clicks_count_list[l].get("clicks")) * 100) if float(clicks_count_list[l].get("clicks")) !=0 else 0
                    cvr_count_list += [
                        {
                            "cvr": cvr,
                            "date_start": conversions_count_list[l].get("date_start")
                        }
                    ]
                else:
                    cvr_count_list += [
                        {
                            "cvr": str(0),
                            "date_start": conversions_count_list[l].get("date_start")
                        }
                    ]

            for l in range(len(conversions_count_list)):
                if conversions_count_list[l].get("date_start") == costs_count_list[l].get("date_start"):
                    cpi = '%0.2f' % (float(costs_count_list[l].get("spend")) / float(conversions_count_list[l].get("conversions")) * 100) if float(conversions_count_list[l].get("conversions")) !=0 else 0
                    cpi_count_list += [
                        {
                            "cpi": cpi,
                            "date_start": conversions_count_list[l].get("date_start")
                        }
                    ]
                else:
                    cpi_count_list += [
                        {
                            "cpi": str(0),
                            "date_start": conversions_count_list[l].get("date_start")
                        }
                    ]

            if len(revenue_new_list) >= len(costs_count_list):
                count = len(costs_count_list)
                len_difference = len(revenue_new_list) - len(costs_count_list)
                for le in range(len_difference):
                    costs_count_list += [{
                        "spend": 0,
                        "date_start": revenue_new_list[count+le].get("date_start")
                    }]
            else:
                len_difference = len(costs_count_list) - len(revenue_new_list)
                count = len(revenue_new_list)
                for le in range(len_difference):
                    revenue_new_list += [{
                        "revenue": 0,
                        "date_start": costs_count_list[count+le].get("date_start")
                    }]

            for r in range(len(revenue_new_list)):
                if revenue_new_list[r].get("date_start") == costs_count_list[r].get("date_start"):
                    profit_list += [
                        {
                            "profit": '%0.2f' % (float(revenue_new_list[r].get("revenue"))-float(costs_count_list[r].get("spend"))),
                            "date_start": revenue_new_list[r].get("date_start")
                        }
                    ]
                else:
                    profit_list += [
                        {
                            "profit": str(0),
                            "date_start": revenue_new_list[r].get("date_start")
                        }
                    ]
            count_revenue = 0
            for a in revenue_new_list:
                count_revenue += float(a["revenue"])

            data_date_table = {
                "impressions_list": impressions_count_list,
                "cost_list": costs_count_list,
                "clicks_list": clicks_count_list,
                "conversions_list":conversions_count_list,
                "ctr_list": ctr_count_list,
                "cvr_list": cvr_count_list,
                "cpc_list": cpc_count_list,
                "cpi_list": cpi_count_list,
                "revenue_list": revenue_new_list,
                "profit_list": profit_list,
                "head": ["Date","Revenue","Profit","Cost","Impressions","Clicks","Conversions","CTR","CVR","CPC","CPA"]
            }
            data_geo_table ={}
            data_geo["revenue"] = str(count_revenue)
            data_geo["profit"] = float(count_revenue) - float(data_geo["count_cost"])
            date_range = []
            impressions_range = []
            cost_range = []
            revenue_range = []
            clicks_range = []
            conversions_range = []
            ctr_range = []
            cvr_range = []
            cpc_range = []
            cpi_range = []
            profit_range = []
            for i in revenue_new_list:
                date_range.append(i["date_start"])
                revenue_range.append(i["revenue"])
            for i in impressions_count_list:
                impressions_range.append(i["impressions"])
            for i in costs_count_list:
                cost_range.append(i["spend"])
            for i in clicks_count_list:
                clicks_range.append(i["clicks"])
            for i in conversions_count_list:
                conversions_range.append(i["conversions"])
            for i in ctr_count_list:
                ctr_range.append(i["ctr"])
            for i in cvr_count_list:
                cvr_range.append(i["cvr"])
            for i in cpc_count_list:
                cpc_range.append(i["cpc"])
            for i in cpi_count_list:
                cpi_range.append(i["cpi"])
            for i in profit_list:
                profit_range.append(i["profit"])

            data_range = {
                "date": date_range[::-1],
                "revenue": revenue_range[::-1],
                "impressions": impressions_range[::-1],
                "costs": cost_range[::-1],
                "clicks": clicks_range[::-1],
                "conversions": conversions_range[::-1],
                "ctr": ctr_range[::-1],
                "cvr": cvr_range[::-1],
                "cpc": cpc_range[::-1],
                "cpi": cpi_range[::-1],
                "profit": profit_range[::-1]
            }


        return json.dumps({
            "code": 200,
            "data_geo": data_geo,
            "data_geo_table": data_geo_table,
            "data_date_table": data_date_table,
            "data_range": data_range,
            "message": "success"
        })