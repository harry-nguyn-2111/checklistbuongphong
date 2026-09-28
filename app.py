import os
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Housekeeping Checklist", page_icon="🏨", layout="wide")

rooms = [f"Phòng {i}" for i in range(101, 111)]

checklist = {
    "Công việc chính": [
        "Dọn phòng", "Thay ga giường", "Thay vỏ gối", "Thay khăn",
        "Hút bụi sàn", "Lau sàn", "Lau bụi nội thất",
        "Kiểm tra mùi phòng", "Kiểm tra điều hòa", "Kiểm tra đèn điện",
    ],
    "Đồ đạc trong phòng": [
        "Mini bar", "Giường", "Tủ quần áo", "Bàn", "Ghế", "Rèm cửa",
        "Tivi", "Điện thoại", "Két an toàn", "Ấm đun nước", "Máy sấy tóc",
    ],
    "Đồ vệ sinh cá nhân": [
        "Dầu gội", "Sữa tắm", "Xà phòng", "Bàn chải đánh răng",
        "Kem đánh răng", "Mũ tắm", "Dao cạo râu", "Giấy vệ sinh",
        "Khăn mặt", "Khăn tay", "Khăn tắm",
    ],
    "Phòng tắm": [
        "Bồn cầu sạch", "Lavabo sạch", "Gương sạch", "Vòi sen sạch",
        "Sàn phòng tắm sạch", "Thùng rác", "Không có tóc/rác",
        "Kiểm tra nước nóng", "Kiểm tra thoát nước",
    ],
    "Kiểm tra cuối": [
        "Kiểm tra tài sản khách", "Kiểm tra đồ thất lạc",
        "Kiểm tra cửa phòng", "Kiểm tra khóa cửa",
        "Tắt các thiết bị không cần thiết", "Đóng cửa sổ",
        "Xịt khử mùi", "Phòng sẵn sàng đón khách",
    ],
}

TOTAL_ITEMS = sum(len(v) for v in checklist.values())
HISTORY_FILE = "housekeeping_history.csv"

st.markdown("""
<style>
.main-title {background:#1f4e79;color:white;padding:20px;border-radius:12px;
text-align:center;margin-bottom:20px}
.room-card {background:white;border:1px solid #e5e7eb;border-radius:12px;
padding:12px;margin-bottom:8px}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
<h1>🏨 HOUSEKEEPING CHECKLIST</h1>
<p>Kiểm tra công việc nhân viên buồng phòng</p>
</div>
""", unsafe_allow_html=True)

employee = st.text_input("👤 Tên nhân viên", placeholder="Nhập tên nhân viên...")

def key(room_i, cat_i, item_i):
    return f"room_{room_i}_{cat_i}_{item_i}"

def room_progress(room_i):
    done = 0
    for cat_i, items in enumerate(checklist.values()):
        for item_i in range(len(items)):
            if st.session_state.get(key(room_i, cat_i, item_i), False):
                done += 1
    return done, (done / TOTAL_ITEMS if TOTAL_ITEMS else 0)

selected = st.selectbox("🚪 Chọn phòng", range(len(rooms)),
                        format_func=lambda i: rooms[i])

st.subheader(f"🛏️ {rooms[selected]}")

for cat_i, (category, items) in enumerate(checklist.items()):
    st.markdown(f"### 📌 {category}")
    for item_i, item in enumerate(items):
        st.checkbox(item, key=key(selected, cat_i, item_i))

done, progress = room_progress(selected)

c1, c2, c3 = st.columns(3)
c1.metric("Đã hoàn thành", f"{done}/{TOTAL_ITEMS}")
c2.metric("Tiến độ", f"{progress * 100:.0f}%")
c3.metric("Trạng thái", "✓ Hoàn thành" if progress == 1 else
          ("Đang làm" if progress > 0 else "Chưa hoàn thành"))
st.progress(progress)

if st.button("✓ Hoàn thành phòng", type="primary", use_container_width=True):
    if not employee.strip():
        st.warning("⚠️ Vui lòng nhập tên nhân viên.")
    elif progress < 1:
        st.warning("⚠️ Phòng chưa hoàn thành tất cả checklist.")
    else:
        record = pd.DataFrame([{
            "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nhân viên": employee.strip(),
            "Phòng": rooms[selected],
            "Đã hoàn thành": done,
            "Tổng checklist": TOTAL_ITEMS,
            "Tiến độ": "100%",
            "Trạng thái": "Hoàn thành",
        }])
        if os.path.exists(HISTORY_FILE):
            try:
                old = pd.read_csv(HISTORY_FILE)
                record = pd.concat([old, record], ignore_index=True)
            except Exception:
                pass
        record.to_csv(HISTORY_FILE, index=False, encoding="utf-8-sig")
        st.success(f"🎉 {rooms[selected]} đã hoàn thành và sẵn sàng đón khách!")

st.markdown("---")
st.subheader("🏨 Tổng quan 10 phòng")

cols = st.columns(5)
for i, room in enumerate(rooms):
    done_i, progress_i = room_progress(i)
    with cols[i % 5]:
        st.markdown(f'<div class="room-card"><strong>{room}</strong></div>',
                    unsafe_allow_html=True)
        st.progress(progress_i)
        st.caption(f"{done_i}/{TOTAL_ITEMS} — {progress_i * 100:.0f}%")

st.markdown("---")
st.subheader("📋 Nhật ký Housekeeping")

if os.path.exists(HISTORY_FILE):
    try:
        history = pd.read_csv(HISTORY_FILE)
        if not history.empty:
            st.dataframe(history.sort_values("Thời gian", ascending=False),
                         use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có dữ liệu.")
    except Exception as exc:
        st.error(f"Không thể đọc dữ liệu: {exc}")
else:
    st.info("Chưa có nhật ký Housekeeping.")
