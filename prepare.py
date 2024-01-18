import pandas as pd


def likely_phone(name: str) -> bool:
    """the text contain "điện thoại" likely a phone name"""
    assert name.islower()
    return "điện thoại" in name


def get_phone_brand(text: str, brands: list[str]) -> str:
    """
    Extracts the brand of a phone from a given text.
    """
    normalized_text = text.lower()

    if not likely_phone(normalized_text):
        return "unknown"

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
    raw = pd.read_excel("./De/DA_Excel.xlsx", sheet_name="Dữ liệu")

    platforms = ["shopee", "tiki", "lazada"]

    # Select necessary columns
    columns = [
        "Tên sản phẩm",
        "Link shop",
        "Ngành hàng",
        "Thương hiệu",
        "Số đã bán",
        "Tổng doanh số",
    ]
    df = raw[columns]

    # get platforms
    df["platform"] = df["Link shop"].map(
        lambda link: get_platform_from_link(link, platforms)
    )
    df.drop(columns=["Link shop"], inplace=True)

    # Replace uncategory
    df["Ngành hàng"].replace(
        "Chưa phân loại", "Điện Thoại & Máy Tính Bảng", inplace=True
    )

    # Filter rows for "Điện Thoại & Máy Tính Bảng" category
    phone_df = df[
        (df["Ngành hàng"] == "Điện Thoại & Máy Tính Bảng")
        & (df["Ngành hàng"].str.contains("điện thoại", case=False))
    ]

    # Define a list of brands
    brands = [
        "apple",
        "xiaomi", "samsung",
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

    # Fill missing values in "Thương hiệu" column using custom function
    phone_df["Thương hiệu"].fillna(
        phone_df["Tên sản phẩm"].map(
            lambda text: get_phone_brand(text=text, brands=brands)
        ),
        inplace=True,
    )

    # save to file
    phone_df.to_excel("./prepared.xlsx")
