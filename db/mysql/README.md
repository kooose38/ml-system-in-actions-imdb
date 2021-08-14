ログを収集するデータベースです。

### Prediction Tables 
| columns | Description |
| ------:| -----------:|
| log_id   | job_id。プライマリーキー |
| log | JSON型。主に推論器の出力データ |
| datetime    | 作成日時 |


### Outlier Tables 

| Option | Description |
| ------:| -----------:|
| log_id   | job_id。プライマリーキー |
| log | JSON型。主に入力データの外れ値検知の出力データ |
| datetime   | 作成日時 |