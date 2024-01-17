import pandas as pd


def general_clean(df: pd.DataFrame) -> pd.DataFrame:
    # drop columns that unnecessary
    new_df = df.drop(
        [
            "Số lượt xem sản phẩm",
            "Số đánh giá",
            "Ngành hàng cấp 1",
            "Ngành hàng cấp 2",
            "Ngành hàng cấp 3",
            "Thumbnail",
        ],
        axis=1,
    )
    return new_df


def likely_phone(text: str) -> bool:
    assert text.islower()
    return "điện thoại" in text


def get_phone_brand(text: str, brands: list[str]) -> str:
    normalized_text = text.lower()

    if not likely_phone(normalized_text):
        return "unknown"

    for brand in brands:
        if brand in normalized_text:
            return brand

    # special cases
    if "galaxy" in normalized_text:
        return "samsung"

    return "unknown"


if __name__ == "__main__":
    # Read the Excel file
    raw = pd.read_excel("./De/DA_Excel.xlsx", sheet_name="Dữ liệu")

    # Select necessary columns
    df = raw[
        ["Tên sản phẩm", "Ngành hàng", "Thương hiệu", "Số đã bán", "Tổng doanh số"]
    ]

    # Replace uncategory
    df["Ngành hàng"].replace(
        "Chưa phân loại", "Điện Thoại & Máy Tính Bảng", inplace=True
    )

    # Filter rows for "Điện Thoại & Máy Tính Bảng" category
    phone_df = df[df["Ngành hàng"] == "Điện Thoại & Máy Tính Bảng"]

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

    # Fill missing values in "Thương hiệu" column using custom function
    phone_df["Thương hiệu"] = phone_df["Thương hiệu"].fillna(
        phone_df["Tên sản phẩm"].map(
            lambda text: get_phone_brand(text=text, brands=brands)
        )
    )

    # print(phone_df[phone_df["Thương hiệu"] == "unknown"])

    # Print the sum of "Số đã bán" column grouped by "Thương hiệu" column
    print(phone_df.groupby(by="Thương hiệu")[["Số đã bán", "Tổng doanh số"]].sum())
    # print(phone_df.groupby(by="Thương hiệu")["Tổng doanh số"].sum())
