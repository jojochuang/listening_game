# 聽音辨字遊戲

以瀏覽器播放題目語音，從六個選項中選出正確答案的聽力練習遊戲。支援課本／課次選單、圖片＋注音與全注音兩種模式。

**純前端**：在 GitHub Pages 上可直接運行，無需後端；題庫透過 CORS 代理讀取 Google 試算表。

## 使用方式

### 方式一：GitHub Pages（推薦）

1. 在 repo 設定中啟用 **GitHub Pages**（Source: main branch）。
2. 開啟：**https://\<你的帳號\>.github.io/listening_game/**  
   或 **https://\<你的帳號\>.github.io/listening_game/listening_game.html**
3. 選課本、課次與模式後即可遊玩。試算表需設為「知道連結的任何人可檢視」。

### 方式二：本機伺服器

1. 執行：`python3 server.py`
2. 開啟：**http://localhost:5002/listening_game.html**  
   （使用本機 API 讀取試算表，不依賴外部代理。）

## 需求

- 題庫為 Google 試算表，需設為「知道連結的任何人可檢視」
- 建議使用 Chrome / Safari / Edge 以獲得較佳語音與相容性

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `listening_game.html` | 遊戲主頁（選單＋遊戲畫面） |
| `server.py` | 本機伺服器（靜態檔＋試算表 CSV 代理） |
| `BpmfSpecial/BpmfZihiOnly-R.ttf` | 注音字型（顯示題目注音） |

## 授權

遊戲介面與程式可自由使用。注音字型請依 `BpmfSpecial` 目錄內之授權說明使用。
