import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout
import qsm_w
import demo_main as demo
import random


class DynamicGridLayoutWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.obj_w = []

    def initUI(self):

        self.setWindowTitle("输入样本参数")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        self.add_row_button = QPushButton("新增样本", self)
        self.add_row_button.clicked.connect(self.add_row)
        self.main_layout.addWidget(self.add_row_button)

        self.remove_row_button = QPushButton("删除样本", self)
        self.remove_row_button.clicked.connect(self.remove_last_row)
        self.main_layout.addWidget(self.remove_row_button)

        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.labels = []  # 存储标签的列表
        self.inputs = []  # 存储输入框的列表

        self.cols = ['U1', 'U2', 'U3', 'U4', 'U5',
                     'U11', 'U12', 'U13', 'U14', 'U15', 'U16', 'U17',
                     'U21', 'U22', 'U23', 'U24',
                     'U31', 'U32', 'U33',
                     'U41', 'U42', 'U43', 'U44',
                     'U51', 'U52']

        # 初始化标签和输入框
        for row in range(3):
            label = QLabel(f"样本 {row + 1}:", self)
            self.grid_layout.addWidget(label, row + 1, 0)
            self.labels.append(label)

            row_inputs = []

            for col, col_name in enumerate(self.cols):
                if row == 0:
                    label1 = QLabel(col_name, self)
                    self.grid_layout.addWidget(label1, row, col + 1)

                input_field = QLineEdit(self)
                self.grid_layout.addWidget(input_field, row + 1, col + 1)
                row_inputs.append(input_field)

            self.inputs.append(row_inputs)

        # 添加确定按钮
        self.convert_button = QPushButton("重置输入", self)
        self.convert_button.clicked.connect(self.clearAllText)
        self.main_layout.addWidget(self.convert_button)

        self.convert_button = QPushButton("确定", self)
        self.convert_button.clicked.connect(self.convert_to_matrix)
        self.main_layout.addWidget(self.convert_button)

        self.save_button = QPushButton("保存并返回", self)
        self.main_layout.addWidget(self.save_button)

        self.result_label = QLabel(self)
        self.main_layout.addWidget(self.result_label)

        # 设置默认值
        v = [[81, 67, 81, 80, 77, 100, 100, 100, 7, 2.8, 100, 100, 58, 30, 80, 0.72, 2.5, 6, 7.13, 11.46, 1.1, 7, 1.5, 7,1],
            [83, 65, 78, 87, 75, 80, 80, 80, 4, 2, 80, 80, 40, 35, 60, 0.6, 1.25, 10, 5, 20, 1, 20, 2, 6, 0.5],
            [86, 63, 76, 85, 71, 90, 90, 90, 5, 3, 90, 90, 50, 40, 70, 0.75, 2.08, 5, 10, 15, 0.5, 10, 1, 4, 0.6]]
        for i in range(len(self.inputs)):
            for j in range(len(self.inputs[i])):
                self.inputs[i][j].setText(str(v[i][j]))

    def add_row(self):
        new_row = len(self.labels)

        # 添加新标签
        label = QLabel(f"样本 {new_row + 1}:", self)
        self.grid_layout.addWidget(label, new_row + 1, 0)
        self.labels.append(label)

        # 添加新输入框
        row_inputs = []
        for col in range(len(self.cols)):
            input_field = QLineEdit(self)
            self.grid_layout.addWidget(input_field, new_row + 1, col + 1)
            row_inputs.append(input_field)
        self.inputs.append(row_inputs)

    def remove_last_row(self):
        if self.labels:
            row = len(self.labels) - 1
            for widget in [self.labels[row]] + self.inputs[row]:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()

            self.labels.pop(row)
            self.inputs.pop(row)

            for i, label in enumerate(self.labels):
                label.setText(f"样本 {i + 1}:")

    def convert_to_matrix(self):
        matrix = []
        self.obj_w = []
        for row_inputs in self.inputs:
            row_data = [input_field.text() for input_field in row_inputs]
            if '' not in row_data:
                row_data = (list(map(float, row_data)))
                matrix.append(row_data)
            else:
                self.result_label.setText('请完整输入矩阵!')
                break

        matrix1 = [i[:5] for i in matrix]
        matrix2 = [i[5:] for i in matrix]

        self.obj_w = []

        for a in [matrix1, matrix2]:
            if a != [] and len(a) == len(self.inputs):
                self.obj_w.extend(demo.objective_W(a))

        if len(self.obj_w) == 25:
            self.result_label.setText('输入成功！')
            print('全寿命阶段客观权重为:', self.obj_w)

        # # 直接赋值，用于测试
        # self.obj_w = [0.238, 0.141, 0.151, 0.287, 0.183, 0.014, 0.014, 0.014, 0.037, 0.033, 0.014, 0.014,
        #               0.024, 0.041, 0.019, 0.019, 0.044, 0.112, 0.067, 0.09, 0.075, 0.177, 0.089, 0.05, 0.05]

    def clearAllText(self):
        # 遍历所有输入框，清空文本内容
        for row_input in self.inputs:
            for all_input in row_input:
                all_input.clear()
        self.result_label.setText("重置成功!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DynamicGridLayoutWidget()
    window.show()
    sys.exit(app.exec_())
