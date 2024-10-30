import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button

# CSVファイルのパス
file_path = '../product_management_rtc/table/products_management_lower.csv'

# データを読み込み、グラフを描画する関数
def plot_data():
    df = pd.read_csv(file_path)

    # グラフをクリアして最新データで再描画
    ax.clear()

    # 各列のデータを取得
    id_info = df['ID']
    product_name = df['TYPE']
    x_coords = df['CTR_POS_X']
    y_coords = df['CTR_POS_Y']

    # 各商品の情報に応じた形状とラベルを設定
    shape_mapping = {0: 'triangle', 1: 'right_triangle', 2: 'vertical_rect', 3: 'circle', 4: 'horizontal_rect', 5: 'square'}
    label_mapping = {0: 'rice', 1: 'sand', 2: 'juice', 3: 'stick', 4: 'box', 5: 'call'}

    # グラフの範囲と軸の設定
    ax.set_xlim(-450, 450)
    ax.set_ylim(400, 800)
    ax.spines['top'].set_position('zero')
    ax.spines['left'].set_position('center')

    # 各商品の情報に基づきプロット
    for idx, (id_val, name_val, x, y) in enumerate(zip(id_info, product_name, x_coords, y_coords)):
        color = 'red' if id_val == -1 else 'green'
        shape = shape_mapping.get(name_val, 'circle')
        label = label_mapping.get(name_val, '')

        # 形状ごとのプロット処理
        if shape == 'triangle':
            ax.scatter(x, y, color=color, marker='^', s=100)
        elif shape == 'right_triangle':
            ax.scatter(x, y, color=color, marker='>', s=100)
        elif shape == 'vertical_rect':
            ax.add_patch(mpatches.Rectangle((x - 5, y - 10), 10, 20, color=color))
        elif shape == 'circle':
            ax.scatter(x, y, color=color, marker='o', s=100)
        elif shape == 'horizontal_rect':
            ax.add_patch(mpatches.Rectangle((x - 57.5, y - 92.5), 115, 185, color=color))
        elif shape == 'square':
            ax.add_patch(mpatches.Rectangle((x - 52.5, y - 52.5), 105, 105, color=color))

        # 商品ラベルを表示
        ax.text(x + 10, y, label, fontsize=12, ha='left', va='center')

    # タイトルとラベルの設定
    ax.set_title("baggage")
    ax.set_xlabel("x ")
    ax.set_ylabel("y ")
    ax.grid(True)

    # 画面を更新
    plt.draw()

# ボタンが押された時にグラフを更新する関数
def on_button_clicked(event):
    plot_data()

# 図と軸を作成
fig, ax = plt.subplots(figsize=(12, 10))
plt.subplots_adjust(bottom=0.2)  # ボタン表示のためスペースを確保

# 更新ボタンの作成
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])  # [左, 下, 幅, 高さ]
button = Button(ax_button, 'get new data')
button.on_clicked(on_button_clicked)

# 初期プロット
plot_data()

# グラフを表示
plt.show()
