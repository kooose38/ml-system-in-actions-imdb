prep_slowからのリクエストを貯めるデータベースです。  
batch-serverにより推論実行されます。

### Job_id 
| columns | Description |
| ------:| -----------:|
| id | 予測する際の一意になるjob ID |
| prediction | バッチサーバーで実行される予測値、初期値は空文字 |

### Image_id
| columns | Description |
| ------:| -----------:|
| image_id   | "image_" + job_id |
| data | 予測する入力データ |