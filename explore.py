import pandas as pd


if __name__ == "__main__":
    df = pd.read_excel("./De/DA_Excel.xlsx", sheet_name="Dữ liệu")

    print("-" * 30, "column names", "-" * 30)
    print(df.columns)

    print("-" * 30, "Explore empty", "-" * 30)
    # print(df["Thương hiệu"].unique())
    for field in df.columns:
        print(f"{field}: {df[field].isnull().sum()}")

    # # Can I do something with brand missing?
    print(df[df["Thương hiệu"].isnull()][["Tên sản phẩm", "Thương hiệu"]])

    print("-" * 30, "Explore duplicates", "-" * 30)
    for field in df.columns:
        print(f"{field}: {len(df[df[field].duplicated()])}")

    # # check Is every records that have empty "Giá phân loại cao nhất" field also empty "Giá phân loại nhỏ nhất" field?
    # print(
    #     len(
    #         df[
    #             df[["Giá phân loại cao nhất", "Giá phân loại nhỏ nhất"]]
    #             .isnull()
    #             .all(axis=1)
    #         ]
    #     )
    # )

    # # check duplicate shop's names and shop's not equal
    # shop_names = df["Tên shop"].unique()
    # for name in shop_names:
    #     shop_links = df[df["Tên shop"] == name]["Link shop"]
    #     # print(type(shop_links))
    #     num_links = shop_links.nunique()
    #     if num_links > 1:
    #         print(name, num_links, shop_links.unique())
