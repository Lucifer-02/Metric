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


def general_transform(df: pd.DataFrame) -> pd.DataFrame:
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
        "xsmart",
        "kudixiong",
        "xiaomi youpin",
        "itel",
        "poco",
        "tecno",
        "nokia",
    ]

    df["Thương hiệu"] = df["Thương hiệu"].fillna(
        df["Tên sản phẩm"].map(lambda text: get_phone_brand(text=text, brands=brands))
    )

    return df


def get_phone_brand(text: str, brands: list[str]) -> str:
    normalized_text = text.lower()
    for brand in brands:
        if brand in normalized_text and "điện thoại" in normalized_text:
            return brand
    return "unknown"


if __name__ == "__main__":
    raw = pd.read_excel("./De/DA_Excel.xlsx", sheet_name="Dữ liệu")
    df = general_clean(raw)

    df = general_transform(df)
    print(df["Thương hiệu"].head(30))

    df.to_excel("test.xlsx")
