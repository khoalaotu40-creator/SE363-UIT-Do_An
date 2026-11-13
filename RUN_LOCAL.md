# Chạy MarketPulse cục bộ

1. Tạo dữ liệu mô phỏng: `make_finance_news_demo.py`.
2. Huấn luyện DCdetector trên tập bình thường.
3. Test để tạo `result/FINANCE_NEWS_scores.npz`.
4. Vẽ biểu đồ và replay alert bằng `stream_replay.py`.

`stream_replay.py` chỉ xuất cảnh báo cho analyst xem xét; không gửi lệnh giao
dịch và không gọi API broker. Xem lệnh đầy đủ trong `readme.md`.
