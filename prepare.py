import pandas as pd


def get_phone_brand(text: str, brands: list[str]) -> str:
    """
    Extracts the brand of a phone from a given text.
    """
    normalized_text = text.lower()

    for brand in brands:
        if brand in normalized_text:
            return brand

    if "galaxy" in normalized_text:
        return "samsung"

    return "unknown"


def get_platform_from_link(link: str, platforms: list[str]) -> str | None:
    """
    Extracts the platform from a given link.
    """
    for platform in platforms:
        if platform in link:
            return platform

    return None


if __name__ == "__main__":
    # Read the Excel file
    df = pd.read_excel("./De/DA_Excel.xlsx", sheet_name="Dữ liệu")

    platforms = ["shopee", "tiki", "lazada"]

    # Filter rows for "Điện Thoại & Máy Tính Bảng" category
    phone_df = df[
        (df["Ngành hàng"].isin(["Điện Thoại & Máy Tính Bảng", "Chưa phân loại"]))
        & (df["Tên sản phẩm"].str.contains("điện thoại", case=False))
    ]

    # get platforms
    phone_df["platform"] = phone_df["Link shop"].map(
        lambda link: get_platform_from_link(link, platforms)
    )

    phone_df["Doanh số"] = phone_df["Số đã bán"] * phone_df["Giá"]

    # Define a list of brands
    brands = [
        "apple",
        "xiaomi",
        "samsung",
        "oppo",
        "realme",
        "vertu",
        "asus",
        "redmi",
        "lg",
        "infinix",
        "sony",
        "google",
        "vsmart",
        "vivo",
        "kudixiong",
        "itel",
        "poco",
        "tecno",
        "nokia",
    ]

    # Fill missing values in "Thương hiệu" column
    phone_df["Thương hiệu"].fillna(
        phone_df["Tên sản phẩm"].map(
            lambda text: get_phone_brand(text=text, brands=brands)
        ),
        inplace=True,
    )

    # Select necessary columns
    columns = [
        "Tên sản phẩm",
        "Thương hiệu",
        "Số đã bán",
        "Doanh số",
        "platform",
    ]
    prepared_df = phone_df[columns]

    # save to file
    prepared_df.to_excel("./prepared.xlsx", index=False)
