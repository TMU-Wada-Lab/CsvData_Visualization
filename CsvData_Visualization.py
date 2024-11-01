import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
import matplotlib.animation as animation

# 初期のCSVファイルのパス（lowerを設定）
file_path = '../product_management_rtc/table/products_management_lower.csv'
last_data = None  # データの変更検出用
auto_update = False  # 自動更新フラグ

# 商品名に対応するラベルを設定
label_mapping = {0: 'rice', 1: 'sand', 2: 'juice', 3: 'stick', 4: 'box', 5: 'call'}

# グラフの描画設定
fig, ax = plt.subplots(figsize=(12, 10))
plt.subplots_adjust(bottom=0.3)  # ボタンの表示用スペースを確保

# グラフの範囲設定
ax.set_xlim(-450, 450)
ax.set_ylim(400, 800)

# グラフを描画する関数
def plot_data():
    global last_data
    df = pd.read_csv(file_path)

    # 前回のデータと比較して変化がない場合は更新しない
    if df.equals(last_data):
        return

    # データが変化した場合に更新
    last_data = df

    # グラフをクリアして最新データで再描画
    ax.clear()
    ax.set_xlim(-450, 450)
    ax.set_ylim(400, 800)
    ax.spines['top'].set_position('zero')
    ax.spines['left'].set_position('center')

    # 各列のデータを取得
    id_info = df['ID']
    product_name = df['TYPE']
    x_coords = df['CTR_POS_X']
    y_coords = df['CTR_POS_Y']

    # 各商品の情報に基づきプロット
    shape_mapping = {0: 'triangle', 1: 'right_triangle', 2: 'vertical_rect', 3: 'circle', 4: 'horizontal_rect', 5: 'square'}

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

    # グラフを更新
    plt.draw()

# 自動更新をトグルするボタンの機能
def toggle_auto_update(event):
    global auto_update
    auto_update = not auto_update
    auto_update_button.label.set_text("Stop Auto-Update" if auto_update else "Start Auto-Update")

# ファイルパスをupper/lowerで切り替えるボタンの機能
def toggle_file_path(event):
    global file_path
    if 'lower' in file_path:
        file_path = '../product_management_rtc/table/products_management_upper.csv'
        file_path_button.label.set_text("Switch to Lower")
    else:
        file_path = '../product_management_rtc/table/products_management_lower.csv'
        file_path_button.label.set_text("Switch to Upper")
    # 切り替えた際に即時更新
    plot_data()

# 自動更新を管理する関数
def update(frame):
    if auto_update:
        plot_data()

# ボタンの設定
ax_auto_update_button = plt.axes([0.35, 0.05, 0.2, 0.075])
auto_update_button = Button(ax_auto_update_button, "Start Auto-Update")
auto_update_button.on_clicked(toggle_auto_update)

# ファイルパス切り替えボタンの設定
ax_file_path_button = plt.axes([0.6, 0.05, 0.2, 0.075])
file_path_button = Button(ax_file_path_button, "Switch to Upper")
file_path_button.on_clicked(toggle_file_path)

# 初期プロット
plot_data()

# アニメーションで定期的に更新をチェック
ani = animation.FuncAnimation(fig, update, interval=2000)

# グラフの表示
plt.show()
