# STEP Week3 Homework 

## 電卓プログラム

<br>

### 宿題1

モジュール化されたプログラムを変更して、「\*」「/」に対応しよう

#### 入力

- 厳密に「数+数+…+数」の形式に従う
  - 例: 「3.0+4*2−1/5」
  - 「2*-3」みたいな式には対応できない
- '1+'みたいな入力は対応できない
- 文字列に空白がある場合は対応できるようにしている
- 空文字列は対応できない



#### 方針

- 掛け算と割り算を最初に処理して、次に足し算と引き算を処理する
  - 例:「3.0+4\*2−1/5」に対してまずは「4\*2」と「1/5」を計算して、「3.0+8-0.2」という新しい式に変換して、最後に足し算と掛け算の計算を行う

- これを実現するためにevaluate()内で2回計算を実行する
  - 一回目は掛け算と割り算
    - もし「\*」と「/」が出たら、今のindexの2個前の数字と計算して結果を新しいtokens_listに保存する
    - もし「+」と「-」が出たら、新しいtokens_listに保存しておく
  - 二回目は足し算と引き算
    - 新しいtokens_listで計算する

- エラーについて
  - 割り算の除数が0ではいけない（0だったら一応対応できる）
  - 割り算と掛け算のパラメーターが不足の場合もエラー出る
    - 入力の制約条件にも関係あるが、判定は一応つけている



<br>

<br>

### 宿題2

書いたプログラムが正しく動いていることを確認するためのテストケースを追加しよう

#### テストケース

- 単一の数字
  - 「1」「1.5」など
- 足し算と引き算だけ
  - 「1+2」「1-2」「1+2-3」など
- 掛け算と割り算だけ
  - 「2\*3」「2/3」「2\*3/7」など
- 「+」「-」「\*」「/」同時にある
  - 「3.0+4*2−1/5」など
- 除数は0
  - 「1/0」
    - 予想通りエラーが出る
- パラメーター不足
  - 「\*9」は対応できるけど「9\*」はできない

- 空白がある
  - 「1 + 2」「1 \* 2」

<br>

<br>

### 宿題3

括弧に対応しよう

#### 入力

- 括弧の内は計算できる式
  - 例: 「(1+2)」「((1+2)*3)」
  - 「(1+)」みたいな式には対応できない
- 括弧はペアで入力される
  -  「(1+2」みたいな式には対応できない
- 空文字列は対応できない



#### 方針

- 始め括弧を見つけたらそれに対応する閉じ括弧を見つけていく
  - 多重括弧に対応できるようにちょっと再帰みたいなものを使った
  - こうすると括弧がないと計算ができないから人工的に括弧を挿入する
- 括弧内の結果をまず計算して新しいtokens_listに保存する
  - 例: 「(3.0+4\*(2−1))/5」→ (2-1)というペアを見つけて計算して「(3.0+4\*1)/5」になる→(3.0+4\*1)見つけて計算して「7.0/5」になる→「1.4」
- 実際に処理する時、「(2−1)」の結果を{TYPE: NUMBER}の1つのtokenとして保存したいが、indexが混乱になるので、NUMBER, SKIP, SKIP, SKIP, SKIPという形になって、tokenはSKIPの時に無視して次のtokenを読み込む
  - 実際に実装するとき、SKIPに関する判定がいらない状態で普通に動ける……



#### テストケース

- 宿題2のテストケースまずは入れておく
- 一重括弧だけある場合
  - 「(1)」「(1+2)」など
- 二重以上の括弧がある場合
  - 「((1))」「((1+2)\*(3+4))」など# STEP_Week3
