import pandas as pd


def get_phone_brand(text: str, brands: set[str]) -> str:
    """
    Extracts the brand of a phone from a given text.
    """
    normalized_text = text.lower()

    if "galaxy" in normalized_text:
        return "samsung"
    
    for brand in brands:
        if brand in normalized_text:
            return brand

    return "unknown"


def get_platform_from_link(link: str, platforms: set[str]) -> str | None:
    """
    Extracts the platform from a given link.
    """
    for platform in platforms:
        if platform in link:
            return platform

    return None


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a pandas DataFrame as input and performs several data preparation steps.
    """

    platforms = ["shopee", "tiki", "lazada"]
    brands = [
        "apple", "xiaomi", "samsung", "oppo", "realme", "vertu", "asus", "redmi",
        "lg", "infinix", "sony", "google", "vsmart", "vivo", "kudixiong", "itel",
        "poco", "tecno", "nokia"
    ]

    # Filter rows for "Điện Thoại & Máy Tính Bảng" category and product name containing "điện thoại"
    phone_df = df[
        (df["Ngành hàng"].isin(["Điện Thoại & Máy Tính Bảng", "Chưa phân loại"]))
        & (df["Tên sản phẩm"].str.contains("điện thoại", case=False))
    ].copy()

    # Add a new column called "platform" by applying the `get_platform_from_link` function to the "Link shop" column
    phone_df["platform"] = phone_df["Link shop"].map(
        lambda link: get_platform_from_link(link, platforms)
    )

    # Calculate a new column called "Doanh số" by multiplying the "Số đã bán" and "Giá" columns
    phone_df["Doanh số"] = phone_df["Số đã bán"] * phone_df["Giá"]

    # Fill missing values in "Thương hiệu" column by applying the `get_phone_brand` function to the "Tên sản phẩm" column
    phone_df["Thương hiệu"].fillna(
        phone_df["Tên sản phẩm"].map(
            lambda text: get_phone_brand(text=text, brands=brands)
        ),
        inplace=True,
    )

    # Select necessary columns
    columns = ["Tên sản phẩm", "Thương hiệu", "Số đã bán", "Doanh số", "platform"]
    prepared_df = phone_df[columns]

    return prepared_df


if __name__ == "__main__":
    # Read the Excel file
    raw = pd.read_excel("./Data/DA_Excel.xlsx", sheet_name="Dữ liệu")

    phone_df = prepare(raw)

    # ====================== Question 1 =========================
    ans1 = phone_df.groupby(by="Thương hiệu")[["Số đã bán", "Doanh số"]].sum()
    # print(ans1)

    # ====================== Question 2 =========================

    brand_country_df = pd.read_csv("./Data/brand_country.csv")

    # combine with brand's countries
    merged = phone_df.merge(brand_country_df, how="outer", on="Thương hiệu")

    countries = ["Trung Quốc", "Mỹ", "Hàn Quốc"]

    ans2 = (
        merged.loc[merged["country"].isin(countries)]
        .groupby(by="country")[["Số đã bán"]]
        .sum()
        .sort_values("Số đã bán", ascending=False)
    )
    # print(ans2)

    # ====================== Question 3 =========================
    ans3 = (
        merged.loc[merged["country"].isin(countries)]
        .groupby(by="country")[["Doanh số"]]
        .sum()
        .sort_values("Doanh số", ascending=False)
    )
    # print(ans3)

    # ====================== Question 4 =========================
    samsung_phones = phone_df.loc[
        (phone_df["Thương hiệu"] == "samsung") & (phone_df["platform"] == "shopee")
    ]

    sum_s23_phones = samsung_phones.groupby(
        samsung_phones["Tên sản phẩm"].str.contains("s23", case=False)
    )[["Doanh số", "Số đã bán"]].sum()

    percentages = (sum_s23_phones / sum_s23_phones.sum() * 100).round(2).transpose()

    ans4 = percentages.rename(
        columns={True: "samsung galaxy s23", False: "others"},
    )
    print(ans4)

    # ===============================================
    # save to file

    with pd.ExcelWriter("./Results/answers.xlsx", engine="xlsxwriter") as writer:
        ans1.to_excel(writer)
        ans2.to_excel(writer, startcol=4)
        ans3.to_excel(writer, startcol=7)
        ans4.to_excel(writer, startcol=10)

    print("...Done!")
