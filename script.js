const AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json";
const areaSelect = document.getElementById('areaSelect');

// 地域リストを取得する関数
async function fetchAreas() {
    try {
        const response = await fetch(AREA_URL);
        const data = await response.json();
        
        // 気象庁APIのarea.jsonは「offices」という単位が一般的
        const offices = data.offices;
        
        areaSelect.innerHTML = '<option value="">地域を選択してください</option>';
        
        for (const code in offices) {
            const option = document.createElement('option');
            option.value = code;
            option.textContent = offices[code].name;
            areaSelect.appendChild(option);
        }
    } catch (error) {
        console.error("地域リストの取得に失敗しました", error);
    }
}

fetchAreas();