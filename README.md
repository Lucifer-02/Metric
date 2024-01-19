# Metric intervew

## Python
- Code: `answers.py`
- Kết quả: `Results/answers.xlsx`
- Thứ tự xử lý: đọc file `Data/DA_Excel.xlsx` và `Data/brand_country.csv` rồi sinh ra file `answers.xlsx`
- Các packages: pandas, openpyxl, xlsxwriter

## SQL
- Script nộp: `answers.sql`
- Thứ tự xử lý: Chuẩn bị dữ liệu trước tiên như làm sạch, chuyển đổi dữ liệu và tạo các bảng cần thiết. Sau đó mới truy vấn đưa ra câu trả lời
- Sử dụng MySQL




## Notes
 
- 1 shop có thể có nhiều links do trên nhiều sàn
- Không thể drop empty fields do ảnh hưởng >10% đến doanh số và số đã bán của hãng Samsung
- Tất của Category "Chưa phân loại" đều là điện thoại Samsung
- Sàn thương mại cần lấy từ "Link shop" thay vì "Link sản phẩm"
- "Số đã bán" có ở dạng thập phân và nguyên lẫn lộn
- Giá sản phẩm có thể là đồng thay vì nghìn đồng 

- Sử dụng MySQL thay vì SQLite không hỗ trợ case insensitive với UTF-8 
