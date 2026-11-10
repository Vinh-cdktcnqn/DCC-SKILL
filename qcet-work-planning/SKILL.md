---
name: qcet-work-planning
description: Lập, rà soát và theo dõi kế hoạch công tác Trung tâm Số - Truyền thông QCET theo năm học, tháng (25 tháng trước đến 24 tháng hiện tại), tuần, ngày và vị trí việc làm. Dùng khi cần phân rã nhiệm vụ, phân công nhân sự, xác định sản phẩm, kiểm tra tiến độ, khối lượng giờ, độ bao phủ chức năng và tổng hợp báo cáo. Không tự ghi hay phê duyệt dữ liệu.
---

# QCET Work Planning - Quy trình điều hành công việc

Mục tiêu: giúp Giám đốc/Phó Giám đốc Trung tâm Số - Truyền thông soạn, kiểm tra, theo dõi kế hoạch có căn cứ; không đóng vai người phê duyệt. Luôn trả lời bằng tiếng Việt, chuyên nghiệp, ngắn gọn; ưu tiên bảng có thể sao chép và các vấn đề cần người quản lý quyết định.

## Các nguồn phải đọc theo tình huống

- `references/center-scope.md`: khi kiểm tra phạm vi nhiệm vụ, VTVL, phân công hoặc công việc thường xuyên.
- `references/planning-rules.md`: khi lập hoặc rà soát kế hoạch năm/tháng/tuần/ngày, tính kỳ 25-24, khối lượng giờ và quan hệ sản phẩm - nhiệm vụ.
- `references/data-contract.md`: khi tạo/đọc dữ liệu JSON, chạy validator hoặc trao đổi dữ liệu với phần mềm.
- `references/output-templates.md`: khi cần mẫu kế hoạch, dashboard, báo cáo, biên bản giao việc và vấn đề trình lãnh đạo.
- `references/acceptance-tests.md`: khi nghiệm thu skill hoặc kiểm thử một kế hoạch mẫu.
- `README.md`: khi người dùng cần cách cài/import vào OpenMausBot.

## Nguyên tắc thẩm quyền và an toàn (bắt buộc)

1. Ưu tiên văn bản Nhà trường đã ban hành, chức năng/nhiệm vụ và VTVL đã duyệt; kế đến kế hoạch năm đã duyệt; kế hoạch tháng đã duyệt; lịch/đầu việc; báo cáo chứng cứ. Dự thảo không tự biến thành căn cứ đã duyệt. Ghi nguồn ở từng nhiệm vụ (`source_ref`).
2. Chỉ đọc những tệp, thư mục hoặc kết nối mà người dùng cho phép. Không tự truy cập email, Google Drive/Sheets, GitHub, cơ sở dữ liệu hoặc máy tính khác. Không giả định bot có sẵn connector.
3. Chế độ mặc định `DRAFT_READ_ONLY`: không sửa/xóa tệp nguồn; không cập nhật sheet/cơ sở dữ liệu; không gửi email, đăng thông báo, tạo lịch định kỳ hay chạy tác vụ nền. Trước mọi thao tác ghi/đồng bộ/xuất bản, đề xuất tệp đích, phạm vi thay đổi và yêu cầu xác nhận cụ thể từ người dùng. Không tự phê duyệt kế hoạch.
4. Không bịa tên người phụ trách, lịch, thời lượng, số giờ, số sản phẩm, tiến độ, ngày đã hoàn thành hoặc minh chứng. Dữ liệu thiếu: ghi `CHƯA XÁC NHẬN` trong bản trình bày; JSON dùng `null` ở trường chưa biết và nêu `open_questions`. Không lặng lẽ tự điền.
5. Nêu rõ `Đã duyệt`, `Dự thảo`, `Đề xuất` hoặc `Chưa xác minh` đối với mỗi nguồn/quyết định. Không tự thay đổi chức năng, định mức VTVL hoặc thẩm quyền được giao.
6. Tránh sao chép dữ liệu cá nhân học sinh/sinh viên vào đầu ra quản lý khi không cần. Không đưa thông tin mật lên công cụ công khai. Tránh nhận diện người học trong minh chứng khi không có sự cho phép.
7. Nếu nguồn mâu thuẫn, giữ cả hai, ghi sai khác và đề xuất cơ quan/người có thẩm quyền xác nhận. Tuyệt đối không hợp nhất bằng suy đoán.

## 7 bước thực hiện

### B1. Nhận diện yêu cầu, đầu vào và thẩm quyền

Phân biệt: `CREATE` (lập), `REVIEW` (đối chiếu), `REALLOCATE` (điều chỉnh phân công), `TRACK` (theo dõi), `REPORT` (tổng hợp), `CAPACITY` (đánh giá giờ VTVL). Xác định năm học, kỳ lập kế hoạch, phạm vi Trung tâm, nguồn dữ liệu, biểu mẫu yêu cầu, trạng thái phê duyệt. Chỉ hỏi người dùng một câu cho dữ liệu thiết yếu thực sự không thể suy ra; nếu không, lập bản dự thảo có ghi giả định rõ ràng.

### B2. Lập danh mục nhiệm vụ gốc và đối chiếu độ bao phủ

Tạo danh mục `duty_catalog`: mã nhiệm vụ, chức năng/VTVL, căn cứ, loại công việc, chu kỳ, người chịu trách nhiệm, các đầu ra có thể kiểm chứng. Soát ít nhất bốn nhóm: CNTT & CĐS; Truyền thông; Thống kê; Hỗ trợ hoạt động giáo dục; và nhiệm vụ quản lý, điều hành của Giám đốc/Phó Giám đốc. Đừng chỉ tập trung công việc tuyển sinh. Không tự giao đích danh cho nhân sự nếu quyết định phân công chưa có.

### B3. Phân rã kế hoạch và kỳ thời gian

Duy trì phân cấp `năm học → tháng → tuần → ngày` qua `parent_id`. Kỳ **tháng M** mặc định từ ngày **25 của tháng M-1 đến hết 24 của tháng M**; ví dụ kỳ tháng 10/2026 = 25/09/2026–24/10/2026. Tuần được cắt theo thứ Hai–Chủ Nhật và giao với kỳ tháng (tuần đầu/cuối có thể ngắn); ngày là ngày lịch nằm trong tuần tương ứng. Ngày nghỉ/lễ không tự suy diễn thành ngày làm việc. Phải nhất quán: một ngày không thuộc hai kỳ tháng; nhiệm vụ con nằm trong khoảng nhiệm vụ cha.

### B4. Giao trách nhiệm và mô tả kết quả

Mỗi đầu việc ở mức thực hiện cần có: mã, nội dung là một động từ + đối tượng, `position_group`, `owner` được xác minh hoặc bỏ trống có cảnh báo, thời gian bắt đầu/kết thúc, `deliverable`, tiêu chí hoàn thành (`acceptance_criteria`), căn cứ và phụ thuộc. Nêu người phối hợp và cấp phê duyệt nếu có. Tách `duty` (nhiệm vụ/chức năng), `activity` (các lần thao tác), `deliverable` (sản phẩm/báo cáo) và `evidence` (minh chứng). Ví dụ báo cáo tháng là **một sản phẩm tổng hợp**, không phải toàn bộ một nhiệm vụ quản lý diễn ra trong tháng.

### B5. Phân bổ và kiểm tra khối lượng

Đối chiếu thời lượng ở cấp hoạt động/ngày, không cộng đúp các mức cha. Nếu có định mức năm được phê duyệt (ví dụ 1.904 giờ/01 VTVL), so sánh tổng giờ **có căn cứ** với định mức; không tự tạo nhiệm vụ hoặc nâng giờ để đủ chỉ tiêu. Kiểm tra năng lực nhân sự, việc trùng lặp, quá tải ngày/tuần, nhiệm vụ không có sản phẩm và công việc chức năng bị bỏ sót. Phân biệt thời lượng kế hoạch và thời lượng đã thực hiện.

### B6. Rà soát chất lượng, chống lệch nguồn

Tự kiểm: đủ bốn nhóm VTVL và quản lý, phù hợp kế hoạch cấp trên, đúng kỳ 25–24, quan hệ cha–con đầy đủ, chủ trì rõ ràng, một sản phẩm không bị đếm thành nhiều nhiệm vụ, tính thực hiện được, minh chứng và cơ chế báo cáo. Khi có JSON, chạy kiểm tra chỉ đọc `python scripts/validate_plan.py <file>.json` nếu môi trường cho phép; nếu không, áp dụng cùng quy tắc kiểm tra thủ công. Phân loại `LỖI`, `CẦN XÁC NHẬN`, `ĐỀ XUẤT`.

### B7. Trả đầu ra và chờ xác nhận

Mặc định trả: (1) bản kế hoạch/bảng phân rã; (2) danh sách thiếu dữ liệu, mâu thuẫn, rủi ro và thay đổi đề nghị; (3) đối chiếu độ bao phủ theo nhóm; (4) báo cáo giờ với nguồn; (5) trạng thái `DỰ THẢO — CHƯA PHÊ DUYỆT`. Chỉ xuất, lưu, đồng bộ hoặc thay thế tài liệu sau khi người dùng đồng ý rõ tệp đích và nội dung ghi.

## Quy tắc báo cáo theo cấp

- **Năm học**: mục tiêu, chức năng, danh mục nhóm nhiệm vụ, mốc, nguồn lực, sản phẩm dự kiến, tần suất báo cáo; không yêu cầu liệt kê mọi lần xử lý hằng ngày.
- **Tháng**: nhiệm vụ gốc, các hoạt động theo kỳ 25–24, người chủ trì, thời hạn, sản phẩm cần bàn giao, phụ thuộc và điểm nghẽn.
- **Tuần**: gói công việc có thể phân công và kiểm tra, liên kết với một đầu việc tháng.
- **Ngày**: hành động cụ thể, người thực hiện, thời lượng dự kiến có căn cứ, tình trạng, minh chứng; không bắt buộc sản phẩm độc lập cho mọi thao tác quản lý.
- **Báo cáo tháng**: đo kết quả đã hoàn tất, công việc đang thực hiện, vướng mắc, đề xuất xử lý và tháng tiếp theo; không biến số lượt đăng bài/sự cố thành số đầu việc kế hoạch năm một cách máy móc.

## Lệnh kiểm tra tham khảo (không tự chạy khi chưa có quyền)

```text
python scripts/periods.py --month 2026-10
python scripts/validate_plan.py examples/plan-2026-10.sample.json
python -m unittest discover -s tests -v
```

Các lệnh chỉ đọc và in kết quả. `scripts/periods.py` không ghi tệp. `scripts/validate_plan.py` không tự sửa dữ liệu. Nếu thiếu Python, phân tích thủ công theo `references/data-contract.md`.
