<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Housekeeping Checklist</title>

<style>
* {
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}

body {
    margin: 0;
    background: #f3f5f7;
    color: #222;
}

header {
    background: #1f4e79;
    color: white;
    padding: 20px;
    text-align: center;
}

header h1 {
    margin: 0 0 5px;
}

.container {
    max-width: 1100px;
    margin: auto;
    padding: 20px;
}

.room-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 15px;
}

.room-card {
    background: white;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}

.room-card h2 {
    margin-top: 0;
}

.status {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 13px;
    margin-bottom: 10px;
    background: #ffe8a1;
}

.progress-container {
    background: #ddd;
    border-radius: 10px;
    height: 10px;
    overflow: hidden;
    margin: 10px 0;
}

.progress {
    height: 100%;
    width: 0%;
    background: #28a745;
    transition: 0.3s;
}

.category {
    margin-top: 18px;
}

.category h3 {
    margin-bottom: 8px;
    color: #1f4e79;
}

label {
    display: block;
    padding: 8px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
}

label:hover {
    background: #f5f5f5;
}

input[type="checkbox"] {
    margin-right: 8px;
    transform: scale(1.2);
}

button {
    width: 100%;
    margin-top: 15px;
    padding: 11px;
    border: none;
    border-radius: 8px;
    background: #1f4e79;
    color: white;
    cursor: pointer;
    font-size: 15px;
}

button:hover {
    background: #163b5c;
}

.completed {
    background: #d4edda;
    color: #155724;
}

.employee {
    margin-bottom: 20px;
    background: white;
    padding: 15px;
    border-radius: 10px;
}

.employee input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
}
</style>
</head>

<body>

<header>
    <h1>🏨 HOUSEKEEPING CHECKLIST</h1>
    <p>Kiểm tra công việc nhân viên buồng phòng</p>
</header>

<div class="container">

    <div class="employee">
        <label>
            Tên nhân viên:
            <input
                type="text"
                id="employeeName"
                placeholder="Nhập tên nhân viên..."
            >
        </label>
    </div>

    <div class="room-list" id="roomList"></div>

</div>

<script>

const rooms = [
    "Phòng 101",
    "Phòng 102",
    "Phòng 103",
    "Phòng 104",
    "Phòng 105",
    "Phòng 106",
    "Phòng 107",
    "Phòng 108",
    "Phòng 109",
    "Phòng 110"
];

const checklist = {

    "Công việc chính": [
        "Dọn phòng",
        "Thay ga giường",
        "Thay vỏ gối",
        "Thay khăn",
        "Hút bụi sàn",
        "Lau sàn",
        "Lau bụi nội thất",
        "Kiểm tra mùi phòng",
        "Kiểm tra điều hòa",
        "Kiểm tra đèn điện"
    ],

    "Đồ đạc trong phòng": [
        "Mini bar",
        "Giường",
        "Tủ quần áo",
        "Bàn",
        "Ghế",
        "Rèm cửa",
        "Tivi",
        "Điện thoại",
        "Két an toàn",
        "Ấm đun nước",
        "Máy sấy tóc"
    ],

    "Đồ vệ sinh cá nhân": [
        "Dầu gội",
        "Sữa tắm",
        "Xà phòng",
        "Bàn chải đánh răng",
        "Kem đánh răng",
        "Mũ tắm",
        "Dao cạo râu",
        "Giấy vệ sinh",
        "Khăn mặt",
        "Khăn tay",
        "Khăn tắm"
    ],

    "Phòng tắm": [
        "Bồn cầu sạch",
        "Lavabo sạch",
        "Gương sạch",
        "Vòi sen sạch",
        "Sàn phòng tắm sạch",
        "Thùng rác",
        "Không có tóc/rác",
        "Kiểm tra nước nóng",
        "Kiểm tra thoát nước"
    ],

    "Kiểm tra cuối": [
        "Kiểm tra tài sản khách",
        "Kiểm tra đồ thất lạc",
        "Kiểm tra cửa phòng",
        "Kiểm tra khóa cửa",
        "Tắt các thiết bị không cần thiết",
        "Đóng cửa sổ",
        "Xịt khử mùi",
        "Phòng sẵn sàng đón khách"
    ]
};


// Tạo 10 phòng
function createRooms() {

    const roomList = document.getElementById("roomList");

    rooms.forEach((room, roomIndex) => {

        const card = document.createElement("div");

        card.className = "room-card";

        let html = `
            <h2>${room}</h2>

            <span
                class="status"
                id="status-${roomIndex}">
                Chưa hoàn thành
            </span>

            <div class="progress-container">
                <div
                    class="progress"
                    id="progress-${roomIndex}">
                </div>
            </div>

            <div id="checklist-${roomIndex}">
        `;

        let itemIndex = 0;

        for (const category in checklist) {

            html += `
                <div class="category">
                    <h3>${category}</h3>
            `;

            checklist[category].forEach(item => {

                const id =
                    `room-${roomIndex}-item-${itemIndex}`;

                html += `
                    <label>
                        <input
                            type="checkbox"
                            id="${id}"
                            onchange="updateRoom(${roomIndex})">
                        ${item}
                    </label>
                `;

                itemIndex++;
            });

            html += `</div>`;
        }

        html += `
            </div>

            <button
                onclick="completeRoom(${roomIndex})">
                ✓ Hoàn thành phòng
            </button>
        `;

        card.innerHTML = html;

        roomList.appendChild(card);
    });
}


// Cập nhật tiến độ phòng
function updateRoom(roomIndex) {

    const checkboxes = document.querySelectorAll(
        `#checklist-${roomIndex} input[type="checkbox"]`
    );

    const checked = [...checkboxes]
        .filter(item => item.checked)
        .length;

    const total = checkboxes.length;

    const percent = Math.round(
        (checked / total) * 100
    );

    document.getElementById(
        `progress-${roomIndex}`
    ).style.width = percent + "%";

    const status = document.getElementById(
        `status-${roomIndex}`
    );

    if (percent === 100) {

        status.innerText = "✓ Hoàn thành";
        status.classList.add("completed");

    } else if (percent > 0) {

        status.innerText =
            `Đang làm - ${percent}%`;

        status.classList.remove("completed");

    } else {

        status.innerText =
            "Chưa hoàn thành";

        status.classList.remove("completed");
    }
}


// Hoàn thành phòng
function completeRoom(roomIndex) {

    const checkboxes = document.querySelectorAll(
        `#checklist-${roomIndex} input[type="checkbox"]`
    );

    const unchecked = [...checkboxes]
        .filter(item => !item.checked);

    if (unchecked.length > 0) {

        alert(
            "⚠️ Phòng chưa hoàn thành tất cả checklist!"
        );

        return;
    }

    alert(
        `${rooms[roomIndex]} đã hoàn thành và sẵn sàng đón khách!`
    );
}


createRooms();

</script>

</body>
</html>
