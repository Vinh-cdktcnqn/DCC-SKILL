# QCET Work Planning v1.0

Skill hỗ trợ lập, kiểm tra và theo dõi kế hoạch công tác Trung tâm Số - Truyền thông Trường Cao đẳng Kỹ thuật Công nghệ Quy Nhơn.

## Nội dung gói

- `SKILL.md` — hướng dẫn vận hành dành cho AI agent (Agent Skills).
- `references/` — phạm vi chức năng, quy tắc kỳ 25–24, hợp đồng dữ liệu, mẫu đầu ra, kịch bản nghiệm thu.
- `scripts/periods.py` — in kỳ công tác tháng và các tuần (chỉ đọc).
- `scripts/validate_plan.py` — kiểm tra JSON kế hoạch (chỉ đọc).
- `examples/plan-2026-10.sample.json` — dữ liệu MINH HỌA, **không phải kế hoạch thật**.
- `tests/` — kiểm thử chuẩn Python (không cần cài thư viện ngoài).
- `agents/openai.yaml` — mô tả hiển thị cho ChatGPT/Codex; không phải thành phần bắt buộc của OpenMausBot.

## Tương thích OpenMausBot

Đối chiếu với mã nguồn OpenMausBot tại `milind-soni/OpenMausBot`, nhánh `main`, ngày 09/11/2026:

1. **Cách được OpenMausBot hỗ trợ trực tiếp:** Skills trong cài đặt bot nhận địa chỉ GitHub repository, thư mục hoặc URL `.../SKILL.md`. Tải **toàn bộ thư mục** cùng tài nguyên đi kèm, rà soát và để skill ở trạng thái tắt trước khi chủ máy bật.
2. **Gói ZIP này là gói phân phối và sao lưu**, không phải định dạng nhập trực tiếp của hộp GitHub URL ở giao diện Skills.
3. **Không cần fork/mutate OpenMausBot.** Người dùng có thể đặt `qcet-work-planning/` vào một repo GitHub do mình quản lý và import địa chỉ thư mục.
4. **Lưu ý quyền riêng tư:** Cơ chế nhập URL GitHub công khai không phải cách lưu dữ liệu nội bộ bí mật; thư mục skill chỉ có quy tắc và ví dụ công khai/giả lập, không cho vào dữ liệu trường nhạy cảm. Với tài liệu nội bộ, sử dụng chế độ local mà bạn kiểm soát.
5. Những tệp dữ liệu thực tế, tên người phụ trách và bảng phân công chưa được đóng gói; bạn phải cung cấp và phê duyệt khi sử dụng.

### A. Import từ GitHub (đề xuất nếu muốn dùng UI Skills)

1. Giải nén `skill.zip` để nhận thư mục `qcet-work-planning/`.
2. Đưa thư mục này lên **repository GitHub của bạn**; ví dụ đường dẫn `qcet-work-planning/` nằm tại gốc repository. Không đưa file chứa mật khẩu, nhân sự riêng tư hoặc dữ liệu học sinh/sinh viên vào repository.
3. Mở OpenMausBot, chọn bot sẽ làm việc với kế hoạch; mở mục **Skills** trong cài đặt bot.
4. Nhập URL dạng `https://github.com/<account>/<repository>/tree/main/qcet-work-planning` (thay bằng repo và branch thực tế), rồi chọn Import.
5. Kiểm tra tên `qcet-work-planning`, nội dung và cảnh báo, sau đó bật skill nếu chấp thuận. Đặt bot ở chế độ **Ask for approval**, không cấp Full access khi chưa cần.
6. Gửi thử: `Dùng qcet-work-planning để tạo dự thảo khung kế hoạch tháng 10/2026 theo 5 nhóm; chưa ghi tệp, không bịa nhân sự hay khối lượng giờ.`

Nếu đặt `SKILL.md` ở gốc repo, nhập `https://github.com/<account>/<repository>/blob/main/SKILL.md`.

### B. Dùng trên máy Windows không công khai skill lên GitHub

Giải nén thư mục skill vào vị trí do bạn quản lý. Với Claude Code, có thể chép thư mục vào `%USERPROFILE%\.claude\skills\qcet-work-planning`. Với Codex, vị trí dự án được hỗ trợ là `.agents\skills\qcet-work-planning` (đặt trong project agent của bạn). Việc OpenMausBot có nhìn thấy vị trí đó phụ thuộc cấu hình **engine** và thư mục làm việc của bot; hãy kiểm tra danh sách native skills sau khi khởi động lại/refresh.

Nếu đang sử dụng bản OpenMausBot có **headless CLI**, tài liệu `docs/headless-cli.md` mô tả `team apply` với `bots[].skills[].file` trỏ tới `SKILL.md` ở đường dẫn tương đối từ tệp cấu hình. Tùy cơ chế import CLI của bản phát hành, cần kiểm tra thực tế việc các tài nguyên bên cạnh `SKILL.md` có được nhập đủ trước khi dùng validator. Không coi ZIP là đã được ứng dụng cài tự động.

### C. Kiểm thử offline trên Windows PowerShell (cần Python 3)

```powershell
cd C:\duong-dan\qcet-work-planning
python scripts\periods.py --month 2026-10
python scripts\validate_plan.py examples\plan-2026-10.sample.json
python -m unittest discover -s tests -v
```

Không cần cài package Python. Nếu không cài Python, agent vẫn sử dụng các file Markdown để lập/rà soát thủ công, nhưng không chạy được script kiểm tra tự động.

## Cách sử dụng an toàn

**Mặc định chỉ đọc.** Không bật tự động lưu lên Google Sheets/Drive hoặc máy tính nếu chưa xem xét quyền của bot và kết nối dữ liệu. Hãy cung cấp cho skill tài liệu chức năng, vị trí việc làm, kế hoạch và nhân sự thực tế từ nguồn đã phê duyệt để tránh kế hoạch chỉ có cấu trúc mà thiếu căn cứ.

## Prompt thử nghiệm

```text
Hãy dùng qcet-work-planning. Đây là dự thảo kế hoạch năm học 2026-2027 và bảng phân công VTVL đã duyệt. Chỉ đọc tài liệu tôi cung cấp; lập khung kế hoạch tháng 11/2026 (25/10–24/11), phân cấp tháng-tuần-ngày; chỉ rõ việc, chủ trì, sản phẩm, minh chứng, nguồn và vướng mắc. Gồm nhiệm vụ Giám đốc, CNTT/CĐS, Truyền thông, Thống kê, Hỗ trợ giáo dục. Không điền tên hoặc giờ nếu chưa được xác minh. Trả dự thảo và bảng kiểm; không ghi tệp.
```

## Giới hạn

Skill là quy trình cho agent, không phải phần mềm quản lý nhiệm vụ có cơ sở dữ liệu. Nó không tự lấy dữ liệu từ Google Sheets, không tự đồng bộ, không tự tạo dashboard thời gian thực, không đặt lịch chạy nền, không thay thế phê duyệt và không đảm bảo nội dung nguồn nếu nguồn không được cung cấp.

## Nguồn đối chiếu OpenMausBot

- `https://github.com/milind-soni/OpenMausBot/blob/main/server/routes/bot-skills.ts` (API nhập nguồn GitHub và trạng thái bật/tắt)
- `https://github.com/milind-soni/OpenMausBot/blob/main/server/skill-folder.ts` (thư mục/tài nguyên, kiểm tra đường dẫn và giới hạn)
- `https://github.com/milind-soni/OpenMausBot/blob/main/src/components/bot-settings/SkillsSection.tsx` (giao diện nhập)
- `https://github.com/milind-soni/OpenMausBot/blob/main/docs/headless-cli.md` (đường dẫn tệp local trong cấu hình đội bot)
