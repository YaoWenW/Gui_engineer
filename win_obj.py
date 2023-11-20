import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, \
    QTableWidgetItem, QPushButton, QLineEdit, QLabel, QDialog, QScrollArea
from PyQt5.QtCore import Qt
import demo_main as demo


class MatrixCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('客观权重计算')
        self.resize(400, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()

        # 创建左侧部分的输入框和计算按钮
        input_layout = QVBoxLayout()
        input_label = QLabel("根据对盾构隧道防水性能影响的程度，输入评价指标的取值(单位为MPa):")
        input_layout.addWidget(input_label)

        scroll_area = QScrollArea()  # 创建QScrollArea用于放置输入框和标签
        scroll_widget = QWidget()  # 创建QWidget作为QScrollArea的子部件
        scroll_layout = QVBoxLayout(scroll_widget)  # 创建垂直布局用于放置输入框和标签

        self.input_lineedits = []
        self.cols = ['管片材料', '管片质量', '防水材料类型', '防水材料老化特性', '密封垫构型', '密封垫固定形式', '密封垫布置形式',
                     '纵缝接头刚度', '环缝抗剪刚度', '内部结构类型',
                     '水压', '不均匀地层', '温度影响', '水位影响',
                     '施工期上浮变形', '拼装精度', '姿态控制', '成型管片',
                     '水位影响', '纵向应力松弛']

        for i in range(len(self.cols)):
            ls = {0: '材料因素', 7: '结构抗变形因素', 11: '水文地质条件因素', 14: '施工期影响因素', 18: '运营期影响因素'}
            if i in ls:
                input_layout_input1 = QHBoxLayout()
                # 创建标签
                label = QLabel(ls[i])
                # 设置标签字体样式
                label.setStyleSheet(" color: red;")
                input_layout_input1.addWidget(label)
                scroll_layout.addLayout(input_layout_input1)

            input_layout_input = QHBoxLayout()
            input_label = QLabel(f'{self.cols[i]}:')
            # input_label.setToolTip(f"{self.info[i]}")  # 设置鼠标悬停提示
            input_label.setFixedWidth(120)  # 设置标签宽度
            input_edit = QLineEdit()
            input_edit.setFixedWidth(120)  # 设置输入框宽度
            input_edit.setAlignment(Qt.AlignLeft)  # 将输入框文本左对齐
            input_layout_input.addWidget(input_label)
            input_layout_input.addWidget(input_edit)
            scroll_layout.addLayout(input_layout_input)

            self.input_lineedits.append(input_edit)

        Y = [0.1, 0.2, 1.5, 1, 2, 0.033, 0.6, 0.885, 1.045, 0.51, 2.4, 0.35, 0.15, 0.225, 0.66, 0.198, 0.33, 2.04, 2.15,
             1]
        # Y = [100, 100, 100, 0.083, 2.8, 100, 100, 58, 30, 80, 0.72, 2.5, 6, 7.13]

        for i in range(len(self.input_lineedits)):
            self.input_lineedits[i].setText(str(Y[i]))

        scroll_area.setWidget(scroll_widget)  # 将QWidget设置为QScrollArea的子部件
        scroll_area.setWidgetResizable(True)  # 设置QScrollArea可以调整大小
        input_layout.addWidget(scroll_area)

        calculate_button = QPushButton('计算')
        calculate_button.clicked.connect(self.calculate)
        input_layout.addWidget(calculate_button)

        self.pushButton_clear = QPushButton('重置输入')
        self.pushButton_clear.clicked.connect(self.clearAllText)
        input_layout.addWidget(self.pushButton_clear)

        self.save_button = QPushButton('保存结果并返回')
        input_layout.addWidget(self.save_button)

        self.result_label = QLabel(self)
        input_layout.addWidget(self.result_label)
        #
        layout.addLayout(input_layout)
        central_widget.setLayout(layout)

    def calculate(self):
        self.obj_w = []
        if '' in [edit.text() for edit in self.input_lineedits]:
            return
        # 获取用户输入的值
        self.input_values = [float(edit.text()) for edit in self.input_lineedits]
        # 根据一定的公式计算矩阵
        max_eigenvalue, max_eigenvector, self.obj_w = demo.objective_W(self.input_values)
        print('输入值为：', self.input_values)
        print('全寿命周期阶段客观权重为：', self.obj_w)


        self.result_label.setText("计算成功!")

    def clearAllText(self):
        for edit in self.input_lineedits:
            edit.clear()
        self.result_label.setText("重置成功!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MatrixCalculator()
    window.show()
    sys.exit(app.exec_())
