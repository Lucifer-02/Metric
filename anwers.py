import pandas as pd


if __name__ == "__main__":
    # Read the Excel file
    phone_df = pd.read_excel("prepared.xlsx", index_col=0)

    # ====================== Question 1 =========================
    ans1 = phone_df.groupby(by="Thương hiệu")[["Số đã bán", "Tổng doanh số"]].sum()
    # print(ans1)

    # ====================== Question 2 =========================
    brand_country_df = pd.read_csv("brand_country.csv")

    # combine with brand's countries
    merged = phone_df.merge(brand_country_df, how="outer", on="Thương hiệu")

    countries = ["Trung Quốc", "Mỹ", "Hàn Quốc"]

    ans2 = (
        merged.loc[merged["country"].isin(countries)]
        .groupby(by="country", sort=True)[["Số đã bán"]]
        .sum()
        .sort_values("Số đã bán", ascending=False)
    )
    # print(ans2)

    # ====================== Question 3 =========================
    ans3 = (
        merged.loc[merged["country"].isin(countries)]
        .groupby(by="country")[["Tổng doanh số"]]
        .sum()
        .sort_values("Tổng doanh số", ascending=False)
    )
    # print(ans3)

    # ====================== Question 4 =========================
    samsung_phones = merged.loc[
        (merged["Thương hiệu"] == "samsung") & (merged["platform"] == "shopee")
    ]

    check_s23_phones = samsung_phones.loc[
        samsung_phones["Tên sản phẩm"].str.contains("s23", case=False)
    ]

    sum_s23_phones = samsung_phones.groupby(
        samsung_phones["Tên sản phẩm"].str.contains("s23", case=False)
    )[["Tổng doanh số", "Số đã bán"]].sum()

    percentages = (sum_s23_phones / sum_s23_phones.sum()).round(2).transpose()

    ans4 = percentages.rename(
        columns={True: "samsung galaxy s23", False: "others"}, errors="raise"
    )
    # print(ans4)

    # ===============================================
    # save to file

    with pd.ExcelWriter("./results/answers.xlsx", engine="xlsxwriter") as writer:
        # Add some text to the worksheet
        # ans1.to_excel(writer, sheet_name="Question 1",startrow=2)
        # ans2.to_excel(writer, sheet_name="Question 1", startcol=4, startrow=2)
        # ans3.to_excel(writer, sheet_name="Question 1", startcol=7, startrow=2)
        # ans4.to_excel(writer, sheet_name="Question 1", startcol=10, startrow=2)
        ans1.to_excel(writer, startrow=2)
        ans2.to_excel(writer, startcol=4, startrow=2)
        ans3.to_excel(writer, startcol=7, startrow=2)
        ans4.to_excel(writer, startcol=10, startrow=2)

        # Write the DataFrame to the Excel file
        # df.to_excel(writer, startrow=4, startcol=0)

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Add some text
        text1 = "hlo"
        text2 = "other text here"
        worksheet.write("A1", "Doanh số theo hãng")
        worksheet.write("E1", "Điện thoại Trung Quốc bán chạy nhất")
        worksheet.write("H1", "Doanh số bán điện thoại của Mỹ là tốt nhất")
        worksheet.write(
            "H1", "Tỉ lệ doanh số và số đã bán của S23 so với các mẫu khác của Samsung"
        )

    print("Done.")
