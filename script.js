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

const weatherResult = document.getElementById('weatherResult');
const forecastContainer = document.getElementById('forecastContainer');
const areaNameDisplay = document.getElementById('areaName');

areaSelect.addEventListener('change', (e) => {
    const areaCode = e.target.value;
    if (areaCode) {
        fetchWeather(areaCode);
    }
});

async function fetchWeather(code) {
    const WEATHER_URL = `https://www.jma.go.jp/bosai/forecast/data/forecast/${code}.json`;
    
    try {
        const response = await fetch(WEATHER_URL);
        const data = await response.json();
        
        // データの解析（気象庁のJSONは構造が複雑なので注意）
        const areaName = data[0].publishingOffice;
        const timeSeries = data[0].timeSeries[0]; // 報告日時と天気予報
        const areas = timeSeries.areas[0]; // 地域ごとの詳細
        
        areaNameDisplay.textContent = `${areas.area.name} の天気`;
        forecastContainer.innerHTML = ''; // クリア
        
        // 3日分の予報を表示
        timeSeries.timeDefines.forEach((time, index) => {
            const date = new Date(time).toLocaleDateString();
            const weather = areas.weathers[index];
            
            const div = document.createElement('div');
            div.className = 'forecast-item';
            div.innerHTML = `
                <p><strong>${date}</strong></p>
                <p>${weather}</p>
            `;
            forecastContainer.appendChild(div);
        });

    } catch (error) {
        console.error("天気情報の取得に失敗しました", error);
    }
}