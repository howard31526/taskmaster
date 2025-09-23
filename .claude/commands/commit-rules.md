---
description: Git Commit 訊息規則（繁中，Conventional Commits 標準）
---

# Commit 訊息規則
在提交訊息時，請遵循以下規則：

- 新功能：`feat(<scope>): <一句話描述>`  
- 修缺漏：`fix(<scope>): <一句話描述>`  
- 重構：`refactor(<scope>): <一句話描述>`
- 合併：`merge(<scope>): <一句話描述>`（不得改變對外行為）

範例：
- `feat(gui): 啟用登入按鈕於表單驗證通過後`
- `fix(api): 修正任務刪除時未正確回傳 404`
- `refactor(db): 抽離查詢函式以提升可維護性`
