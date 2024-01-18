import pandas as pd


if __name__ == "__main__":
    df = pd.read_excel("./De/DA_Excel.xlsx", sheet_name="Dữ liệu")

    print("-" * 30, "column names", "-" * 30)
    print(df.columns)

    print("-" * 30, "Explore empty", "-" * 30)
    for field in df.columns:
        print(f"{field}: {df[field].isnull().sum()/len(df) * 100}%")

    # # # Can I do something with brand missing?
    # print(df[df["Thương hiệu"].isnull()][["Tên sản phẩm", "Thương hiệu"]])
    #
    # print("-" * 30, "Explore duplicates", "-" * 30)
    # for field in df.columns:
    #     print(f"{field}: {len(df[df[field].duplicated()])}")

    # df1 = df[df["Ngành hàng"] == "Chưa phân loại"]
    # df2 = df1[df1["Tên sản phẩm"].str.contains("điện thoại", case=True)]
    # print(df1[["Tên sản phẩm", "Số đã bán", "Tổng doanh số"]])

    # df1 = df[df["Tên sản phẩm"].str.contains("máy tính bảng", case=True)]

    # print(df[df["Tổng doanh số"].duplicated()][["Tên sản phẩm", "Tổng doanh số"]])

    # print(
    #     temp[df["Tên sản phẩm"].str.contains(pat="điện thoại", case=False)][
    #         ["Tên sản phẩm", "Số đã bán", "Ngành hàng"]
    #     ]
    # )

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
