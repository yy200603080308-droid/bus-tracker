while True:
    data = get_data()

    print("取得データ:", data)  # ←これ追加（超重要）

    for item in data:
        print("チェック中:", item)  # ←これも追加

        if item.startswith(TARGET_BUS):
            print("一致した:", item)  # ←ここも

            if last_seen != item:
                print("通知発火！")  # ←確認用
                send(f"🚌 {TARGET_BUS} 動いた → {item}")
                last_seen = item

    time.sleep(20)
