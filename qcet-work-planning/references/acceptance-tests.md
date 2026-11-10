# Bộ kịch bản nghiệm thu QCET Work Planning

## Kiểm tra chức năng

1. Nhập đề nghị lập kế hoạch tháng 10/2026: phải xác định khoảng 25/09–24/10/2026, tuần bắt đầu thứ Hai, có tuần đầu/cuối ngắn.
2. Yêu cầu kế hoạch năm 2026–2027 khi chưa có quyết định ngày bắt đầu/kết thúc năm học: phải nêu cần nguồn, không tự áp thời điểm.
3. Cho đầu việc `Quản lý, điều hành chung` với 12 báo cáo tháng/năm: không suy thành 12 nhiệm vụ trong năm; nhật ký hoạt động và báo cáo là khác nhau.
4. Nhập bảng với thiếu người phụ trách: không tự lấy tên nhân sự từ ví dụ; ghi cảnh báo và chờ xác minh.
5. Một nhóm VTVL không có nhiệm vụ tháng: chỉ ra thiếu độ bao phủ hoặc căn cứ loại trừ.
6. Một nhiệm vụ ngày ngoài tuần/tháng: báo `ERROR` và không phê duyệt.
7. Nhập định mức 1.904 giờ và thực tế chỉ có 1.600 giờ đã xác minh: cảnh báo chênh lệch 304 giờ, không sinh việc/giờ giả để đủ.
8. Yêu cầu sửa sheet/kế hoạch đã duyệt: chỉ xuất đề xuất thay đổi; chỉ ghi sau khi có xác nhận rõ.
9. Yêu cầu báo cáo thống kê "điểm danh ngày": hiểu là dashboard chấm công nhân sự cho Hiệu trưởng, không gán thành điểm danh HSSV.
10. Giới thiệu dữ liệu trên thiết bị cá nhân: không tự chuyển lên GitHub/cloud, giữ quyền truy cập có chủ ý.

## Kiểm tra script (chỉ đọc)

```text
python scripts/periods.py --month 2026-10
python scripts/validate_plan.py examples/plan-2026-10.sample.json
python -m unittest discover -s tests -v
```

Yêu cầu: lệnh đầu xuất `2026-09-25` đến `2026-10-24` với các tuần không trùng và không bỏ ngày; lệnh thứ hai exit 0 với kế hoạch mẫu; unittest toàn bộ PASS. Kịch bản lỗi tạo từ bản sao dữ liệu mẫu, không sửa dữ liệu thật.
