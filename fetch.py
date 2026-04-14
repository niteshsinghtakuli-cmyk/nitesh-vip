import requests

URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def get_data():
    try:
        res = requests.get(URL, timeout=10).json()
        history = res["data"]["list"]

        results, periods, colors = [], [], []

        for item in history:
            num = int(item["number"])
            period = item["issueNumber"]

            results.append("BIG" if num >= 5 else "SMALL")

            if num in [1,3,7,9]:
                colors.append("GREEN")
            elif num in [2,4,6,8]:
                colors.append("RED")
            else:
                colors.append("VIOLET")

            periods.append(period)

        return results, periods, colors

    except:
        return ["BIG","SMALL"], ["0","1"], ["GREEN","RED"]