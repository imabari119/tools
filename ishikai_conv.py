import pandas as pd

# ファイル名
fn = "202511.xlsx"


# 救急

df1 = (
    pd.read_excel(
        fn,
        sheet_name="救急",
        skiprows=2,
        nrows=10,
        index_col=0,
        usecols=range(0, 32),
    )
    .dropna(axis=1, how="all")
    .T.stack()
    .reset_index()
)

df1.columns = ["date", "name", "marker"]


def marker2type(row):
    match (row["marker"], row["name"]):
        case ("○", _):
            return 0, "指定なし", "08:30～翌08:30"
        case ("◎", "医師会市民病院"):
            return 20, "指定なし", "17:30～翌08:30"
        case ("◎", _):
            return 10, "指定なし", "08:30～17:30"
        case ("※", "三木病院"):
            return 15, "整形外科", "08:30～17:30"
        case ("●", "県立今治病院"):
            return 30, "指定なし", "08:30～17:15 / 22:30～翌08:30"
        case ("●", "今治セントラルクリニック"):
            return 31, "指定なし", "17:15～22:30"
        case _:
            return 99, "－", "－"


df1[["type", "medical", "time"]] = df1.apply(marker2type, axis=1, result_type="expand")

# 日付範囲

dates = df1["date"].unique()

# 内科

df3 = (
    pd.read_excel(fn, sheet_name="小児科")
    .melt(var_name="name", value_name="date")
    .dropna()
)

df2 = df3[df3["name"] == "医師会市民病院"].copy()

df2["type"] = 70
df2["medical"] = "内科"
df2["time"] = "09:00～17:30"


# 小児科

df3["type"] = 80
df3["medical"] = "小児科"
df3["time"] = "09:00～12:00 / 14:00～17:00"


# 島しょ部

df4 = (
    pd.read_excel(fn, sheet_name="島しょ部")
    .melt(var_name="name", value_name="date")
    .dropna()
)

df4["type"] = 90
df4["medical"] = "指定なし"
df4["time"] = "09:00～17:00"

# 結合

df = (
    pd.concat([df1, df2, df3, df4], ignore_index=True)
    .sort_values(["date", "type"])
    .reindex(columns=["date", "medical", "name", "time"])
)

df = df[df["date"].isin(dates)].reset_index(drop=True)

df.to_csv("result.tsv", index=False, sep="\t")
