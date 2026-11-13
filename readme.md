# MarketPulse — Giám sát tin tức và cảm xúc thị trường theo thời gian thực

MarketPulse chuyển dự án DCdetector sang bài toán phát hiện sớm một **sự kiện thị
trường cần chuyên viên xem xét** khi giá/khối lượng bất thường cùng xuất hiện với
thay đổi lớn trong tin tức và cảm xúc (sentiment). Nó không đặt lệnh tự động.

## Câu hỏi nghiên cứu

> Đặc trưng tin tức và sentiment có giúp phát hiện các giai đoạn biến động bất
> thường tốt hơn việc chỉ dùng giá và khối lượng hay không?

## Luồng xử lý

```text
Tin tức / earnings call / thông cáo ─┐
                                     ├─> sentiment + mật độ tin ─┐
Giá, khối lượng, biến động ──────────┘                            ├─> DCdetector ─> alert cho analyst
                                                                    │
Đặc trưng đa biến theo cửa sổ thời gian ───────────────────────────┘
```

DCdetector học mẫu hành vi bình thường từ sáu đặc trưng: `log_return`,
`realised_volatility`, `relative_volume`, `sentiment`,
`sentiment_dispersion`, và `news_intensity`. Khi cấu trúc giữa chúng đổi đồng
thời, mô hình sinh anomaly score. Điểm cao là tín hiệu để điều tra, không phải
khuyến nghị mua/bán.

## Dữ liệu demo

`make_finance_news_demo.py` tạo một luồng mô phỏng theo phút với ba sự kiện đã
gắn nhãn: earnings surprise tiêu cực, tin điều tra pháp lý, và guidance tích cực
bất ngờ. Các giá trị này **không phải dữ liệu thị trường thật**; nhãn chỉ phục
vụ đánh giá mô hình.

## Chạy trên Windows

```powershell
uv venv --python 3.11 .venv
uv --system-certs pip install --python .venv\Scripts\python.exe -r requirements-local.txt

.\.venv\Scripts\python.exe make_finance_news_demo.py
.\.venv\Scripts\python.exe main.py --mode train --dataset FINANCE_NEWS --data_path FINANCE_NEWS --input_c 6 --output_c 6 --win_size 60 --patch_size 3,5 --batch_size 64 --num_epochs 10 --use_gpu False --use_multi_gpu False
.\.venv\Scripts\python.exe main.py --mode test --dataset FINANCE_NEWS --data_path FINANCE_NEWS --input_c 6 --output_c 6 --win_size 60 --patch_size 3,5 --batch_size 64 --use_gpu False --use_multi_gpu False
.\.venv\Scripts\python.exe visualize_results.py --results result\FINANCE_NEWS_scores.npz --length 1500
.\.venv\Scripts\python.exe stream_replay.py --stream dataset\FINANCE_NEWS\finance_news_stream.csv --scores result\FINANCE_NEWS_scores.npz
```

## Kết nối dữ liệu thật

Thay CSV demo bằng luồng được cấp phép có cùng schema: lấy market data, lấy tin
từ RSS/API được phép, tính sentiment, rồi ghi một hàng mỗi phút. Cần lưu URL,
thời điểm thu thập, mã chứng khoán và phiên bản mô hình sentiment để kiểm toán.
Triển khai thực tế phải có deduplicate, kiểm tra thời điểm phát hành tin, giám sát
data drift và quy trình analyst duyệt alert.

## Đánh giá đề xuất

So sánh (1) price + volume, (2) price + volume + news/sentiment và (3) baseline
z-score. Báo cáo precision, recall, F1 theo event range, false alerts/day và
detection lead time. Không dùng point adjustment làm chỉ số duy nhất.

Mô hình lõi kế thừa từ *DCdetector: Dual Attention Contrastive Representation
Learning for Time Series Anomaly Detection* (KDD 2023); việc đổi domain không
tự chứng minh hiệu quả trên thị trường thật nếu chưa backtest đúng thời điểm và
đánh giá ngoài mẫu.
