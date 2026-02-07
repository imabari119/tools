import pandas as pd


# 救急シート
def kyukyu_csv():
    df0 = (
        xl("救急データ[#すべて]", headers=True).set_index("name").stack().reset_index()
    )
    df1 = df0.rename(columns={0: "day"}).drop(columns=["level_1"]).copy()

    # 診察情報
    df1["day"] = df1["day"].astype(int)
    df1["time"] = "08:30～翌08:30"
    df1["medical"] = "指定なし"

    df1.set_index(["day", "name"], inplace=True)

    # 特別シート
    df2 = xl("特別データ[#すべて]", headers=True).dropna(subset=["day"])

    df2["day"] = df2["day"].astype(int)
    df2.set_index(["day", "name"], inplace=True)

    # 上書き更新
    df3 = df2.combine_first(df1).reset_index().copy()

    # 基準日
    start = pd.to_datetime(xl("基準日"))

    # 日から日付に変換
    df3["date"] = df3["day"].apply(lambda d: start.replace(day=d))

    # 日を削除
    df3.drop("day", axis=1, inplace=True)

    df3["kind"] = df3["medical"].map({"指定なし": 1, "整形外科": 4})

    # 曜日
    weeks = list("月火水木金土日")
    df3["week"] = df3["date"].dt.dayofweek.apply(lambda x: weeks[x] + "曜日")

    # 祝日
    holidays = xl("祝日データ[国民の祝日・休日月日]", headers=True).iloc[:, 0]
    df3["week"] = df3["week"].mask(df3["date"].isin(holidays), "祝日")

    # 並び替え
    result = df3.reindex(
        columns=["date", "week", "kind", "medical", "name", "time"]
    ).sort_values(["date", "kind", "time"])

    result.reset_index(drop=True)


# 内科シート
def naika_csv():
    df0 = xl("小児科データ[#すべて]", headers=True)

    df1 = df0.melt(var_name="name", value_name="date").dropna()
    df1["date"] = pd.to_datetime(df1["date"], errors="coerce")

    # 小児科で日曜日かつ医師会市民病院
    df2 = df1[
        (df1["name"] == "医師会市民病院") & (df1["date"].dt.day_of_week == 6)
    ].copy()

    # 診察情報
    df2["kind"] = 5
    df2["medical"] = "内科"
    df2["time"] = "09:00～17:30"

    # 曜日
    weeks = list("月火水木金土日")
    df2["week"] = df2["date"].dt.dayofweek.apply(lambda x: weeks[x] + "曜日")

    # 祝日
    holidays = xl("祝日データ[国民の祝日・休日月日]", headers=True)
    df2["week"] = df2["week"].mask(df2["date"].isin(holidays), "祝日")

    # 並び替え
    result = df2.reindex(
        columns=["date", "week", "kind", "medical", "name", "time"]
    ).sort_values(["date", "kind", "time"])

    result.reset_index(drop=True)


# 小児科シート
def shounika_csv():
    df0 = xl("小児科データ[#すべて]", headers=True)

    df1 = df0.melt(var_name="name", value_name="date").dropna()
    df1["date"] = pd.to_datetime(df1["date"], errors="coerce")

    # 診察情報
    df1["kind"] = 7
    df1["medical"] = "小児科"
    df1["time"] = "09:00～12:00 / 14:00～17:00"

    # 曜日
    weeks = list("月火水木金土日")
    df1["week"] = df1["date"].dt.dayofweek.apply(lambda x: weeks[x] + "曜日")

    # 祝日
    holidays = xl("祝日データ[国民の祝日・休日月日]", headers=True).iloc[:, 0]
    df1["week"] = df1["week"].mask(df1["date"].isin(holidays), "祝日")

    # 並び替え
    result = df1.reindex(
        columns=["date", "week", "kind", "medical", "name", "time"]
    ).sort_values(["date", "kind", "time"])

    result.reset_index(drop=True)


# 島しょ部シート
def shima_csv():
    df0 = xl("島しょ部データ[#すべて]", headers=True)

    df1 = df0.melt(var_name="name", value_name="date").dropna()
    df1["date"] = pd.to_datetime(df1["date"], errors="coerce")

    # 診察情報
    df1["kind"] = 9
    df1["medical"] = "指定なし"
    df1["time"] = "09:00～17:00"

    # 曜日
    weeks = list("月火水木金土日")
    df1["week"] = df1["date"].dt.dayofweek.apply(lambda x: weeks[x] + "曜日")

    # 祝日
    holidays = xl("祝日データ[国民の祝日・休日月日]", headers=True).iloc[:, 0]
    df1["week"] = df1["week"].mask(df1["date"].isin(holidays), "祝日")

    # 並び替え
    result = df1.reindex(
        columns=["date", "week", "kind", "medical", "name", "time"]
    ).sort_values(["date", "kind", "time"])

    result.reset_index(drop=True)
